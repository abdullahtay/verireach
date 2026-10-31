"""Main pipeline engine linking SBOM parsing, advisory resolution, call-graph analysis, and VEX generation."""

from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from verireach.advisory import AdvisoryResolver, VulnerabilityAdvisory
from verireach.callgraph import CallGraph, CallGraphBuilder, ReachabilityResult
from verireach.purl import PackageURL
from verireach.sbom import SBOMComponent, SBOMParser
from verireach.vex import VEXDocument, VEXGenerator, VEXStatement


@dataclass
class ScanMetric:
    """Summary metrics of the VeriReach reachability triage."""

    total_components: int = 0
    components_with_vulns: int = 0
    total_advisories: int = 0
    reachable_affected: int = 0
    unreachable_not_affected: int = 0
    false_positive_reduction_rate: float = 0.0


@dataclass
class EngineReport:
    """Complete output of a VeriReach analysis run."""

    metrics: ScanMetric
    vex_document: VEXDocument
    results_detail: List[Dict[str, Any]] = field(default_factory=list)

    def summary_text(self) -> str:
        m = self.metrics
        return (
            f"=== VeriReach Symbol-Level Reachability Report ===\n"
            f"Components Analyzed        : {m.total_components}\n"
            f"Vulnerable Components Mapped: {m.components_with_vulns}\n"
            f"Total Advisory Findings     : {m.total_advisories}\n"
            f"Real Affected (Reachable)   : {m.reachable_affected}\n"
            f"False Positives Eliminated : {m.unreachable_not_affected}\n"
            f"Noise Reduction Rate        : {m.false_positive_reduction_rate:.1f}%\n"
            f"Generated VEX Statements   : {len(self.vex_document.statements)}"
        )


class VeriReachEngine:
    """Orchestrates end-to-end vulnerability reachability assessment."""

    def __init__(
        self,
        advisories_file: Optional[str | Path] = None,
        enable_online_osv: bool = False,
    ):
        self.advisory_resolver = AdvisoryResolver(local_advisories_file=advisories_file)
        self.enable_online_osv = enable_online_osv

    def run_scan(
        self,
        sbom_path: str | Path,
        source_dir: str | Path,
        entrypoint: Optional[str] = None,
        author: str = "VeriReach Analysis Engine",
    ) -> EngineReport:
        """Run complete scan from SBOM and source code directory."""
        # 1. Parse SBOM
        components = SBOMParser.parse_file(sbom_path)

        # 2. Build Call Graph
        src_path = Path(source_dir).resolve()
        builder = CallGraphBuilder(base_dir=src_path)
        call_graph = builder.build_from_directory(src_path, entrypoint_file=entrypoint)

        # 3. Match Advisories and Analyze Reachability
        vex_statements: List[VEXStatement] = []
        details: List[Dict[str, Any]] = []

        total_vulns = 0
        vuln_comps = set()
        reachable_count = 0
        unreachable_count = 0

        for comp in components:
            if not comp.purl:
                continue

            # Check advisories
            advisories = self.advisory_resolver.query_for_component(comp.purl)
            if not advisories and self.enable_online_osv:
                advisories = self.advisory_resolver.query_online_osv(comp.purl)

            if not advisories:
                continue

            vuln_comps.add(comp.purl.to_string())

            for adv in advisories:
                total_vulns += 1
                symbols = adv.affected_symbols or [adv.purl.name]

                # Check reachability for each affected symbol
                any_reachable = False
                best_reach: Optional[ReachabilityResult] = None

                for sym in symbols:
                    reach = call_graph.check_reachability(sym, explicit_entrypoint=entrypoint)
                    if reach.is_reachable:
                        any_reachable = True
                        best_reach = reach
                        break
                    elif best_reach is None:
                        best_reach = reach

                if best_reach is None:
                    # Fallback reachability
                    best_reach = ReachabilityResult(
                        symbol=symbols[0] if symbols else "unknown",
                        is_reachable=False,
                        entrypoint=entrypoint or "unknown",
                        notes="No affected symbols resolved in AST.",
                    )

                if any_reachable:
                    reachable_count += 1
                else:
                    unreachable_count += 1

                stmt = VEXGenerator.create_statement(
                    purl=comp.purl,
                    vulnerability_id=adv.id,
                    reachability=best_reach,
                )
                vex_statements.append(stmt)

                details.append({
                    "purl": comp.purl.to_string(),
                    "vulnerability": adv.id,
                    "affected_symbols": symbols,
                    "is_reachable": best_reach.is_reachable,
                    "call_path": best_reach.call_path,
                    "entrypoint": best_reach.entrypoint,
                })

        # Calculate metrics
        reduction_rate = 0.0
        if total_vulns > 0:
            reduction_rate = (unreachable_count / total_vulns) * 100.0

        metrics = ScanMetric(
            total_components=len(components),
            components_with_vulns=len(vuln_comps),
            total_advisories=total_vulns,
            reachable_affected=reachable_count,
            unreachable_not_affected=unreachable_count,
            false_positive_reduction_rate=reduction_rate,
        )

        vex_doc = VEXGenerator.generate_document(vex_statements, author=author)

        return EngineReport(
            metrics=metrics,
            vex_document=vex_doc,
            results_detail=details,
        )
