"""Command-Line Interface (CLI) for VeriReach."""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from verireach import __version__
from verireach.callgraph import CallGraphBuilder
from verireach.engine import VeriReachEngine
from verireach.purl import PackageURL


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="verireach",
        description="VeriReach: Symbol-Level Reachability & Automated OpenVEX Generator",
    )
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # scan subcommand
    scan_p = subparsers.add_parser("scan", help="Scan SBOM and source code to generate VEX statements")
    scan_p.add_argument("--sbom", required=True, help="Path to CycloneDX or SPDX SBOM JSON file")
    scan_p.add_argument("--src", required=True, help="Directory containing application source code")
    scan_p.add_argument("--entrypoint", default=None, help="Application entrypoint file or symbol (e.g., main.py)")
    scan_p.add_argument("--advisories", default=None, help="Path to custom advisory database JSON")
    scan_p.add_argument("--online-osv", action="store_true", help="Enable online OSV.dev fallback queries")
    scan_p.add_argument(
        "--format",
        choices=["openvex", "cyclonedx", "summary"],
        default="openvex",
        help="Output VEX document format (default: openvex)",
    )
    scan_p.add_argument("--output", "-o", default=None, help="Save output to file path (defaults to stdout)")

    # callgraph subcommand
    cg_p = subparsers.add_parser("callgraph", help="Generate and inspect source code call graph")
    cg_p.add_argument("--src", required=True, help="Directory containing application source code")
    cg_p.add_argument("--entrypoint", default=None, help="Entrypoint file (e.g., main.py)")
    cg_p.add_argument("--target", default=None, help="Target function symbol to test reachability against")
    cg_p.add_argument("--output", "-o", default=None, help="Save call graph JSON to file")

    # purl subcommand
    purl_p = subparsers.add_parser("purl", help="Parse, validate, and normalize Package-URLs (ECMA-427)")
    purl_p.add_argument("purl_string", help="Package URL string (e.g., pkg:pypi/requests@2.28.1)")
    purl_p.add_argument("--json", action="store_true", help="Print structured JSON output")

    return parser


def handle_scan(args: argparse.Namespace) -> int:
    engine = VeriReachEngine(
        advisories_file=args.advisories,
        enable_online_osv=args.online_osv,
    )

    try:
        report = engine.run_scan(
            sbom_path=args.sbom,
            source_dir=args.src,
            entrypoint=args.entrypoint,
        )
    except Exception as e:
        sys.stderr.write(f"Error during scan: {e}\n")
        return 1

    # Print summary to stderr
    sys.stderr.write(report.summary_text() + "\n\n")

    if args.format == "openvex":
        out_content = report.vex_document.to_json(indent=2)
    elif args.format == "cyclonedx":
        out_content = json.dumps(report.vex_document.to_cyclonedx_dict(), indent=2)
    else:
        out_content = json.dumps(
            {
                "metrics": report.metrics.__dict__,
                "details": report.results_detail,
            },
            indent=2,
        )

    if args.output:
        Path(args.output).write_text(out_content, encoding="utf-8")
        sys.stderr.write(f"Output saved to: {args.output}\n")
    else:
        sys.stdout.write(out_content + "\n")

    return 0


def handle_callgraph(args: argparse.Namespace) -> int:
    builder = CallGraphBuilder(base_dir=Path(args.src))
    graph = builder.build_from_directory(args.src, entrypoint_file=args.entrypoint)

    if args.target:
        res = graph.check_reachability(args.target, explicit_entrypoint=args.entrypoint)
        sys.stdout.write(res.summary() + "\n")
        if res.is_reachable:
            sys.stdout.write("Execution chain: " + " -> ".join(res.call_path) + "\n")
        return 0

    graph_dict = {
        "nodes": sorted(list(graph.nodes)),
        "entrypoints": sorted(list(graph.entrypoints)),
        "edges": {caller: sorted(list(callees)) for caller, callees in graph.adj.items()},
    }
    out_content = json.dumps(graph_dict, indent=2)

    if args.output:
        Path(args.output).write_text(out_content, encoding="utf-8")
        sys.stderr.write(f"Call graph saved to: {args.output}\n")
    else:
        sys.stdout.write(out_content + "\n")

    return 0


def handle_purl(args: argparse.Namespace) -> int:
    try:
        p = PackageURL.from_string(args.purl_string)
        if args.json:
            sys.stdout.write(
                json.dumps(
                    {
                        "type": p.type,
                        "namespace": p.namespace,
                        "name": p.name,
                        "version": p.version,
                        "qualifiers": p.qualifiers,
                        "subpath": p.subpath,
                        "canonical": p.to_string(),
                    },
                    indent=2,
                )
                + "\n"
            )
        else:
            sys.stdout.write(f"Valid PURL: {p.to_string()}\n")
            sys.stdout.write(f"  Type      : {p.type}\n")
            sys.stdout.write(f"  Namespace : {p.namespace or '(none)'}\n")
            sys.stdout.write(f"  Name      : {p.name}\n")
            sys.stdout.write(f"  Version   : {p.version or '(none)'}\n")
        return 0
    except Exception as e:
        sys.stderr.write(f"Invalid PURL: {e}\n")
        return 1


def main() -> None:
    parser = create_parser()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    args = parser.parse_args()
    if args.command == "scan":
        sys.exit(handle_scan(args))
    elif args.command == "callgraph":
        sys.exit(handle_callgraph(args))
    elif args.command == "purl":
        sys.exit(handle_purl(args))
    else:
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
