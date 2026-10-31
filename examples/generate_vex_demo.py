#!/usr/bin/env python3
"""VeriReach Demo: Demonstrating symbol-level reachability and VEX generation."""

import sys
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from verireach.engine import VeriReachEngine


def main():
    root = Path(__file__).resolve().parent.parent
    sbom_path = root / "tests" / "fixtures" / "sample_sbom.json"
    src_dir = root / "tests" / "fixtures" / "vulnerable_app"
    advisories_file = root / "tests" / "fixtures" / "mock_advisories.json"

    print("=================================================================")
    print(" VeriReach: Automated Reachability Analysis & VEX Generation")
    print("=================================================================\n")

    engine = VeriReachEngine(advisories_file=advisories_file)
    report = engine.run_scan(
        sbom_path=sbom_path,
        source_dir=src_dir,
        entrypoint="main.py",
    )

    print(report.summary_text())
    print("\nGenerated OpenVEX Document (Sample Statement):")
    for stmt in report.vex_document.statements:
        print(f"\n  - Vuln ID       : {stmt.vulnerability}")
        print(f"    Product       : {stmt.products[0]}")
        print(f"    Status        : {stmt.status.upper()}")
        if stmt.justification:
            print(f"    Justification : {stmt.justification}")
        if stmt.status_notes:
            print(f"    Notes         : {stmt.status_notes}")

    print("\nDemo finished successfully.")


if __name__ == "__main__":
    main()
