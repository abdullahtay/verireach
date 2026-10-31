"""OpenVEX and CycloneDX VEX document generators."""

from __future__ import annotations
import datetime
import json
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from verireach.callgraph import ReachabilityResult
from verireach.purl import PackageURL


@dataclass
class VEXStatement:
    """Represents a single VEX vulnerability assertion."""

    vulnerability: str  # e.g., "CVE-2024-38816"
    products: List[str]  # List of PURLs
    status: str  # "not_affected", "affected", "fixed", "under_investigation"
    justification: Optional[str] = None  # e.g. "vulnerable_code_not_in_execute_path"
    impact_statement: Optional[str] = None
    action_statement: Optional[str] = None
    status_notes: Optional[str] = None


@dataclass
class VEXDocument:
    """Represents an OpenVEX document according to OpenVEX v0.2.0 specification."""

    context: str = "https://openvex.dev/ns/v0.2.0"
    id: str = ""
    author: str = "VeriReach Symbol-Level Reachability Engine"
    role: str = "Automated Static Analysis Tool"
    timestamp: str = ""
    version: int = 1
    tooling: str = "VeriReach v0.1.0 (NLnet / EU CRA Compliance)"
    statements: List[VEXStatement] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.id:
            self.id = f"https://openvex.dev/docs/public/vex-{uuid.uuid4()}"
        if not self.timestamp:
            self.timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert OpenVEX document to standard JSON dictionary."""
        out_stmts = []
        for s in self.statements:
            stmt_dict: Dict[str, Any] = {
                "vulnerability": {"name": s.vulnerability},
                "products": [{"@id": p} for p in s.products],
                "status": s.status,
            }
            if s.justification:
                stmt_dict["justification"] = s.justification
            if s.impact_statement:
                stmt_dict["impact_statement"] = s.impact_statement
            if s.action_statement:
                stmt_dict["action_statement"] = s.action_statement
            if s.status_notes:
                stmt_dict["status_notes"] = s.status_notes
            out_stmts.append(stmt_dict)

        return {
            "@context": self.context,
            "@id": self.id,
            "author": self.author,
            "role": self.role,
            "timestamp": self.timestamp,
            "version": self.version,
            "tooling": self.tooling,
            "statements": out_stmts,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def to_cyclonedx_dict(self) -> Dict[str, Any]:
        """Convert to CycloneDX 1.5/1.6 VEX structure."""
        cyclone_vulns = []
        for s in self.statements:
            state = "exploitable" if s.status == "affected" else "not_affected"
            justification = (
                "code_not_reachable"
                if s.justification == "vulnerable_code_not_in_execute_path"
                else (s.justification or "code_not_reachable")
            )
            affects = [{"ref": p} for p in s.products]

            v_entry: Dict[str, Any] = {
                "id": s.vulnerability,
                "source": {"name": "NVD", "url": f"https://nvd.nist.gov/vuln/detail/{s.vulnerability}"},
                "analysis": {
                    "state": state,
                    "justification": justification if state == "not_affected" else None,
                    "detail": s.impact_statement or s.status_notes,
                },
                "affects": affects,
            }
            # Clean None values in analysis
            v_entry["analysis"] = {k: v for k, v in v_entry["analysis"].items() if v is not None}
            cyclone_vulns.append(v_entry)

        return {
            "bomFormat": "CycloneDX",
            "specVersion": "1.5",
            "serialNumber": f"urn:uuid:{uuid.uuid4()}",
            "version": 1,
            "metadata": {
                "timestamp": self.timestamp,
                "tools": [{"vendor": "VeriReach", "name": "verireach", "version": "0.1.0"}],
            },
            "vulnerabilities": cyclone_vulns,
        }


class VEXGenerator:
    """Generates VEX statements from reachability analysis outcomes."""

    @classmethod
    def create_statement(
        cls,
        purl: PackageURL,
        vulnerability_id: str,
        reachability: ReachabilityResult,
    ) -> VEXStatement:
        """Create a single VEXStatement from ReachabilityResult."""
        product_id = purl.to_string()

        if reachability.is_reachable:
            chain_str = " -> ".join(reachability.call_path)
            return VEXStatement(
                vulnerability=vulnerability_id,
                products=[product_id],
                status="affected",
                action_statement=(
                    f"Vulnerable symbol '{reachability.symbol}' is called in runtime execution path. "
                    f"Upgrade package or refactor calling code."
                ),
                status_notes=(
                    f"Symbol reachability confirmed via call chain: [{chain_str}] "
                    f"from entrypoint '{reachability.entrypoint}'."
                ),
            )
        else:
            return VEXStatement(
                vulnerability=vulnerability_id,
                products=[product_id],
                status="not_affected",
                justification="vulnerable_code_not_in_execute_path",
                impact_statement=(
                    f"Static call-graph analysis verified that vulnerable symbol '{reachability.symbol}' "
                    f"is dead code or never invoked from entrypoint '{reachability.entrypoint}'. "
                    f"Zero execution paths exist."
                ),
                status_notes=reachability.notes,
            )

    @classmethod
    def generate_document(
        cls,
        statements: List[VEXStatement],
        author: str = "VeriReach Reachability Engine",
    ) -> VEXDocument:
        """Bundle statements into an OpenVEX document."""
        return VEXDocument(
            author=author,
            statements=statements,
        )
