"""SBOM Parser for CycloneDX and SPDX JSON formats, extracting normalized PURLs."""

from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from verireach.purl import PackageURL


@dataclass
class SBOMComponent:
    """Represents a component extracted from an SBOM."""

    name: str
    version: Optional[str] = None
    purl: Optional[PackageURL] = None
    raw_purl: Optional[str] = None
    component_type: str = "library"
    description: Optional[str] = None
    licenses: List[str] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)


class SBOMParser:
    """Parses CycloneDX and SPDX SBOM JSON documents."""

    @classmethod
    def parse_file(cls, file_path: str | Path) -> List[SBOMComponent]:
        """Parse an SBOM JSON file from path."""
        p = Path(file_path)
        if not p.is_file():
            raise FileNotFoundError(f"SBOM file not found: {file_path}")

        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)

        return cls.parse_json(data)

    @classmethod
    def parse_json(cls, data: Dict[str, Any]) -> List[SBOMComponent]:
        """Detect format and parse components from dictionary."""
        # Detect CycloneDX
        if "bomFormat" in data and data.get("bomFormat") == "CycloneDX":
            return cls._parse_cyclonedx(data)
        elif "components" in data and isinstance(data["components"], list):
            # Most likely CycloneDX even without explicit bomFormat header
            return cls._parse_cyclonedx(data)

        # Detect SPDX 2.x
        if "spdxVersion" in data and "packages" in data:
            return cls._parse_spdx(data)

        # Direct simple PURL list or array of objects
        if isinstance(data, list):
            components: List[SBOMComponent] = []
            for item in data:
                if isinstance(item, str) and item.startswith("pkg:"):
                    purl_obj = PackageURL.from_string(item)
                    components.append(
                        SBOMComponent(
                            name=purl_obj.name,
                            version=purl_obj.version,
                            purl=purl_obj,
                            raw_purl=item,
                        )
                    )
            return components

        raise ValueError("Unsupported SBOM format: expected CycloneDX or SPDX JSON.")

    @classmethod
    def _parse_cyclonedx(cls, data: Dict[str, Any]) -> List[SBOMComponent]:
        """Parse CycloneDX components."""
        components: List[SBOMComponent] = []
        raw_components = data.get("components", [])

        # Include root metadata component if present
        metadata = data.get("metadata", {})
        if "component" in metadata:
            root_comp = metadata["component"]
            parsed_root = cls._cyclonedx_component_to_obj(root_comp, is_root=True)
            if parsed_root:
                components.append(parsed_root)

        for comp_data in raw_components:
            parsed = cls._cyclonedx_component_to_obj(comp_data)
            if parsed:
                components.append(parsed)

        return components

    @classmethod
    def _cyclonedx_component_to_obj(
        cls, comp: Dict[str, Any], is_root: bool = False
    ) -> Optional[SBOMComponent]:
        """Convert CycloneDX component dict to SBOMComponent."""
        name = comp.get("name", "").strip()
        if not name:
            return None

        version = comp.get("version")
        raw_purl = comp.get("purl")
        purl_obj = None

        if raw_purl:
            try:
                purl_obj = PackageURL.from_string(raw_purl)
            except Exception:
                purl_obj = None
        elif version:
            # Synthetic PURL fallback if generic library
            try:
                purl_obj = PackageURL(type="generic", name=name, version=str(version))
                raw_purl = purl_obj.to_string()
            except Exception:
                pass

        licenses: List[str] = []
        for lic_entry in comp.get("licenses", []):
            if "license" in lic_entry:
                lic = lic_entry["license"]
                lic_id = lic.get("id") or lic.get("name")
                if lic_id:
                    licenses.append(str(lic_id))

        return SBOMComponent(
            name=name,
            version=str(version) if version is not None else None,
            purl=purl_obj,
            raw_purl=raw_purl,
            component_type="application" if is_root else comp.get("type", "library"),
            description=comp.get("description"),
            licenses=licenses,
            properties=comp.get("properties", {}),
        )

    @classmethod
    def _parse_spdx(cls, data: Dict[str, Any]) -> List[SBOMComponent]:
        """Parse SPDX packages."""
        components: List[SBOMComponent] = []
        packages = data.get("packages", [])

        for pkg in packages:
            name = pkg.get("name", "").strip()
            if not name:
                continue

            version = pkg.get("versionInfo")
            raw_purl = None
            purl_obj = None

            # Check externalRefs for PURL
            for ref in pkg.get("externalRefs", []):
                ref_type = ref.get("referenceType", "")
                if ref_type == "purl" or "package-url" in ref_type:
                    raw_purl = ref.get("referenceLocator")
                    if raw_purl:
                        try:
                            purl_obj = PackageURL.from_string(raw_purl)
                        except Exception:
                            purl_obj = None
                    break

            license_concluded = pkg.get("licenseConcluded")
            licenses = [license_concluded] if license_concluded and license_concluded != "NOASSERTION" else []

            components.append(
                SBOMComponent(
                    name=name,
                    version=str(version) if version is not None else None,
                    purl=purl_obj,
                    raw_purl=raw_purl,
                    component_type="package",
                    description=pkg.get("description") or pkg.get("summary"),
                    licenses=licenses,
                )
            )

        return components
