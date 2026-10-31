"""VeriReach: Symbol-Level Reachability & Automated OpenVEX Generator.

Bridges SBOM package-level vulnerabilities (via PURL) with AST/binary call-graph
reachability analysis to deterministically emit OpenVEX and CycloneDX VEX statements.
"""

__version__ = "0.1.0"
__author__ = "Abdullah TAY"
__license__ = "Apache-2.0"

from verireach.purl import PackageURL
from verireach.sbom import SBOMParser, SBOMComponent
from verireach.callgraph import CallGraph, CallGraphBuilder, ReachabilityResult
from verireach.vex import VEXGenerator, VEXDocument, VEXStatement
from verireach.engine import VeriReachEngine

__all__ = [
    "PackageURL",
    "SBOMParser",
    "SBOMComponent",
    "CallGraph",
    "CallGraphBuilder",
    "ReachabilityResult",
    "VEXGenerator",
    "VEXDocument",
    "VEXStatement",
    "VeriReachEngine",
]
