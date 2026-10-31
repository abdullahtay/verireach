"""Security Advisory models and Vulnerability Symbol extraction."""

from __future__ import annotations
import json
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from verireach.purl import PackageURL


@dataclass
class VulnerabilityAdvisory:
    """Represents a vulnerability advisory mapped to package and specific affected symbols."""

    id: str  # e.g., "CVE-2024-38816", "GHSA-xxxx"
    purl: PackageURL
    summary: str
    details: str = ""
    severity: str = "HIGH"
    affected_symbols: List[str] = field(default_factory=list)  # e.g., ["verify_signature", "decode_header"]
    fixed_version: Optional[str] = None
    references: List[str] = field(default_factory=list)


class AdvisoryResolver:
    """Resolves vulnerability advisories and identifies affected function/method symbols."""

    def __init__(self, local_advisories_file: Optional[str | Path] = None):
        self._local_advisories: Dict[str, List[VulnerabilityAdvisory]] = {}
        if local_advisories_file:
            self.load_local_advisories(local_advisories_file)

    def load_local_advisories(self, file_path: str | Path) -> None:
        """Load advisory database from a JSON file."""
        p = Path(file_path)
        if not p.is_file():
            return

        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)

        advisories_list = data if isinstance(data, list) else data.get("advisories", [])
        for entry in advisories_list:
            purl_str = entry.get("purl")
            if not purl_str:
                continue
            try:
                purl = PackageURL.from_string(purl_str)
                adv = VulnerabilityAdvisory(
                    id=entry.get("id", "UNKNOWN-CVE"),
                    purl=purl,
                    summary=entry.get("summary", ""),
                    details=entry.get("details", ""),
                    severity=entry.get("severity", "MEDIUM"),
                    affected_symbols=entry.get("affected_symbols", []),
                    fixed_version=entry.get("fixed_version"),
                    references=entry.get("references", []),
                )
                key = f"{purl.type}/{purl.name}".lower()
                self._local_advisories.setdefault(key, []).append(adv)
            except Exception:
                continue

    def add_advisory(self, advisory: VulnerabilityAdvisory) -> None:
        """Manually register an advisory."""
        key = f"{advisory.purl.type}/{advisory.purl.name}".lower()
        self._local_advisories.setdefault(key, []).append(advisory)

    def query_for_component(self, purl: PackageURL) -> List[VulnerabilityAdvisory]:
        """Find matching advisories for a given component PURL."""
        key = f"{purl.type}/{purl.name}".lower()
        candidates = self._local_advisories.get(key, [])
        matches: List[VulnerabilityAdvisory] = []

        for adv in candidates:
            # Check version match if version is present
            if adv.purl.version and purl.version:
                if adv.purl.version == purl.version:
                    matches.append(adv)
            else:
                matches.append(adv)

        return matches

    def query_online_osv(self, purl: PackageURL, timeout_sec: float = 3.0) -> List[VulnerabilityAdvisory]:
        """Query the public OSV API for open vulnerabilities (optional online mode)."""
        url = "https://api.osv.dev/v1/query"
        payload = {"package": {"purl": purl.to_string()}}

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json", "User-Agent": "VeriReach/0.1.0"},
            )
            with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            results: List[VulnerabilityAdvisory] = []
            for vuln in data.get("vulns", []):
                vuln_id = vuln.get("id", "UNKNOWN")
                summary = vuln.get("summary", "")
                details = vuln.get("details", "")

                # Extract affected symbols from ecosystem_specific metadata if present
                symbols: List[str] = []
                for aff in vuln.get("affected", []):
                    eco_specific = aff.get("ecosystem_specific", {})
                    if "symbols" in eco_specific and isinstance(eco_specific["symbols"], list):
                        symbols.extend(eco_specific["symbols"])
                    # Check imports / functions
                    if "imports" in eco_specific:
                        for imp in eco_specific["imports"]:
                            symbols.extend(imp.get("symbols", []))

                # If no symbols are explicitly specified in OSV, fallback to detecting common function names in summary/details
                if not symbols:
                    symbols = self._extract_symbols_from_prose(details)

                results.append(
                    VulnerabilityAdvisory(
                        id=vuln_id,
                        purl=purl,
                        summary=summary,
                        details=details,
                        severity=vuln.get("database_specific", {}).get("severity", "MEDIUM"),
                        affected_symbols=symbols,
                    )
                )
            return results
        except Exception:
            return []

    @staticmethod
    def _extract_symbols_from_prose(text: str) -> List[str]:
        """Heuristic extractor for function/method names mentioned in CVE prose."""
        import re

        symbols = set()
        # Look for pattern like `function_name()`, `Class.method()` or `method()`
        matches = re.findall(r"`([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)?)\(\)`", text)
        for m in matches:
            if not m.startswith("http") and len(m) > 2:
                symbols.add(m)
        return list(symbols)
