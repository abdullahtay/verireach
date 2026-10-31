"""Package-URL (PURL) parser, normalizer, and validator according to ECMA-427 / packageurl-js spec."""

from __future__ import annotations
import urllib.parse
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass(frozen=True)
class PackageURL:
    """Represents a standard Package-URL (PURL) according to ECMA-427."""

    type: str
    namespace: Optional[str] = None
    name: str = ""
    version: Optional[str] = None
    qualifiers: Dict[str, str] = field(default_factory=dict)
    subpath: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.type:
            raise ValueError("PURL 'type' is required and cannot be empty.")
        if not self.name:
            raise ValueError("PURL 'name' is required and cannot be empty.")
        # Type must be lowercase ASCII
        object.__setattr__(self, "type", self.type.strip().lower())
        object.__setattr__(self, "name", self.name.strip())
        if self.namespace:
            object.__setattr__(self, "namespace", self.namespace.strip().strip("/"))
        if self.version:
            object.__setattr__(self, "version", self.version.strip())

    @classmethod
    def from_string(cls, purl_str: str) -> "PackageURL":
        """Parse a PURL string into a PackageURL object."""
        if not purl_str or not isinstance(purl_str, str):
            raise ValueError("PURL must be a non-empty string.")

        purl_str = purl_str.strip()
        if not purl_str.startswith("pkg:"):
            raise ValueError(f"Invalid PURL scheme: must start with 'pkg:', got '{purl_str}'")

        remainder = purl_str[4:]

        # Extract subpath (#...)
        subpath = None
        if "#" in remainder:
            remainder, subpath_raw = remainder.split("#", 1)
            subpath = urllib.parse.unquote(subpath_raw).strip("/")

        # Extract qualifiers (?...)
        qualifiers: Dict[str, str] = {}
        if "?" in remainder:
            remainder, qualifiers_raw = remainder.split("?", 1)
            for pair in qualifiers_raw.split("&"):
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    k = urllib.parse.unquote(k).strip()
                    v = urllib.parse.unquote(v).strip()
                    if k:
                        qualifiers[k.lower()] = v

        # Extract version (@...)
        # In PURL, version is separated by '@'. However, a namespace might contain '@' (e.g., pkg:npm/@angular/core@12.3.1).
        # The version '@' is never preceded by a '/' (it follows the package name).
        version = None
        ver_idx = -1
        for i in range(len(remainder) - 1, -1, -1):
            if remainder[i] == "@":
                if i > 0 and remainder[i - 1] != "/":
                    ver_idx = i
                    break

        if ver_idx != -1:
            version = urllib.parse.unquote(remainder[ver_idx + 1:])
            remainder = remainder[:ver_idx]

        # Now remainder contains type and optional namespace/name
        parts = [p for p in remainder.split("/") if p]
        if not parts:
            raise ValueError("PURL must contain a type and a name.")

        pkg_type = parts[0].lower()
        if len(parts) == 1:
            raise ValueError("PURL must contain a package name.")
        elif len(parts) == 2:
            namespace = None
            name = urllib.parse.unquote(parts[1])
        else:
            namespace = "/".join(urllib.parse.unquote(p) for p in parts[1:-1])
            name = urllib.parse.unquote(parts[-1])

        return cls(
            type=pkg_type,
            namespace=namespace,
            name=name,
            version=version,
            qualifiers=qualifiers,
            subpath=subpath,
        )

    def to_string(self) -> str:
        """Serialize PackageURL back to standard canonical string."""
        encoded_type = urllib.parse.quote(self.type.lower(), safe="")
        result = f"pkg:{encoded_type}"

        if self.namespace:
            encoded_ns = "/".join(urllib.parse.quote(part, safe="@") for part in self.namespace.split("/"))
            result += f"/{encoded_ns}"

        encoded_name = urllib.parse.quote(self.name, safe="")
        result += f"/{encoded_name}"

        if self.version:
            encoded_version = urllib.parse.quote(self.version, safe="")
            result += f"@{encoded_version}"

        if self.qualifiers:
            sorted_q = sorted(self.qualifiers.items())
            q_str = "&".join(
                f"{urllib.parse.quote(k)}={urllib.parse.quote(v)}" for k, v in sorted_q
            )
            result += f"?{q_str}"

        if self.subpath:
            encoded_subpath = "/".join(urllib.parse.quote(part, safe="") for part in self.subpath.split("/"))
            result += f"#{encoded_subpath}"

        return result

    def matches_identity(self, other: "PackageURL", ignore_version: bool = False) -> bool:
        """Check if two PURLs identify the same package component."""
        if self.type != other.type:
            return False
        if (self.namespace or "").lower() != (other.namespace or "").lower():
            return False
        if self.name.lower() != other.name.lower():
            return False
        if not ignore_version:
            if self.version and other.version and self.version != other.version:
                return False
        return True

    def __str__(self) -> str:
        return self.to_string()
