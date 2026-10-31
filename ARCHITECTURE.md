# VeriReach Architecture & Technical Design

## 1. Executive Summary

**VeriReach** is a high-precision, open-source static reachability analysis engine designed to eliminate false positives in Software Bill of Materials (SBOM) vulnerability scans.

By bridging package-level vulnerability databases (via **PURL / ECMA-427**) with symbol-level Abstract Syntax Tree (AST) call-graph traversals, VeriReach determines whether a vulnerable function or method is actually invoked along any execution path from the application's entrypoints. It emits cryptographically verifiable **OpenVEX** (`@context: https://openvex.dev/ns/v0.2.0`) and **CycloneDX 1.5/1.6 VEX** documents with the standard justification:
```
vulnerable_code_not_in_execute_path
```

---

## 2. The Core Problem: Alert Fatigue & The False Positive Crisis

Traditional vulnerability scanners (Trivy, Syft, Grype, ScanCode) operate at the **package granularity**:
1. An SBOM lists `pkg:pypi/cryptography@3.4.8`.
2. The scanner looks up CVEs matching that package version.
3. Every CVE flags the application as vulnerable.

However, modern empirical research shows that **over 80% of transitive vulnerabilities reside in unused code paths, deprecated utilities, or dead functions**. This creates:
* **Severe Alert Fatigue:** Developers spend hours triaging vulnerabilities that cannot be triggered at runtime.
* **EU Cyber Resilience Act (CRA) Burden:** Starting in 2026/2027, software manufacturers distributing software in the EU must account for known vulnerabilities and provide automated machine-readable VEX statements.

---

## 3. High-Level System Architecture

```
  +------------------+         +----------------------+
  | CycloneDX / SPDX |         | Source Code Tree /   |
  |     SBOM JSON    |         | Application Files    |
  +--------+---------+         +----------+-----------+
           |                              |
           v                              v
  +------------------+         +----------------------+
  |   SBOM Parser    |         |   CallGraphBuilder   |
  | (PURL Extraction)|         |  (AST & Import Graph)|
  +--------+---------+         +----------+-----------+
           |                              |
           v                              |
  +------------------+                    |
  | Advisory Resolver|                    |
  | (VulnerableCode/ |                    |
  |   OSV API)       |                    |
  +--------+---------+                    |
           |                              |
           | Mapped CVEs + Symbols        | Directed Inter-procedural
           +--------------+---------------+ Call Graph
                          |
                          v
               +----------------------+
               | Reachability Engine  |
               | (BFS Shortest Path)  |
               +----------+-----------+
                          |
             +------------+------------+
             |                         |
       [Reachable]               [Unreachable]
             |                         |
      Status: affected         Status: not_affected
      Trace: [A -> B -> C]     Justification:
                               vulnerable_code_not_in_execute_path
             |                         |
             +------------+------------+
                          |
                          v
               +----------------------+
               |    VEX Generator     |
               | (OpenVEX & CycloneDX)|
               +----------------------+
```

---

## 4. Component Deep Dive

### 4.1. Package-URL (PURL) Normalizer (`verireach/purl.py`)
Conforms to the **ECMA-427 standard**:
`pkg:<type>/<namespace>/<name>@<version>?<qualifiers>#<subpath>`
* Preserves canonical namespace escaping (including scoped npm packages like `pkg:npm/@angular/core@12.3.1`).
* Enables deterministic component identity matching across diverse package ecosystems (pypi, npm, cargo, golang, maven).

### 4.2. SBOM Parser (`verireach/sbom.py`)
* Supports **CycloneDX 1.4, 1.5, 1.6** and **SPDX 2.2, 2.3, 3.0** JSON schemas.
* Automatically extracts nested components, licenses, descriptions, and canonical PURLs.

### 4.3. Advisory Resolver (`verireach/advisory.py`)
* Connects component PURLs with CVE IDs and the specific vulnerable symbols (function/method names).
* Supports offline local advisory catalogs (`advisories.json`) and online OSV / VulnerableCode feeds.
* Heuristic extractor for symbols mentioned in CVE prose or patch commit diffs.

### 4.4. Call-Graph Builder & Reachability Solver (`verireach/callgraph.py`)
* Constructs an inter-procedural call graph using Python's native AST parser:
  * Function definitions (`ast.FunctionDef`, `ast.AsyncFunctionDef`)
  * Method invocations (`ast.Call`)
  * Module imports (`ast.Import`, `ast.ImportFrom`)
* **Sound Over-Approximation:** When dynamic dispatch or reflection is present, the engine conservatively avoids emitting false negative `not_affected` statements.
* **Transitive Path Solver:** Employs Breadth-First Search (BFS) with cycle detection to compute deterministic execution traces from entrypoints to vulnerable targets.

### 4.5. VEX Generator (`verireach/vex.py`)
* Emits **OpenVEX v0.2.0** compliant documents with full provenance and action statements.
* Emits **CycloneDX 1.5/1.6 VEX** JSON with `analysis.state: not_affected` and `analysis.justification: code_not_reachable`.

---

## 5. NLnet Foundation & Horizon Europe Alignment

VeriReach directly addresses the objectives of:
1. **CodeSupply Fund (`nlnet.nl/codesupply`):** Part of the EU Horizon Europe Open Internet Stack initiative, partnering with *AboutCode* (creators of `VulnerableCode` and `PurlDB`), *Edsger Institute*, and *NLnet*. VeriReach natively consumes PURLs and provides the symbol reachability data needed by VulnerableCode.
2. **Restack — Open Internet Stack (`nlnet.nl/restack`):** €7M initiative supporting resilient, transparent, and autonomous open-source developer tooling.

---

## 6. License

Licensed under the **Apache License, Version 2.0**.
See [LICENSE](LICENSE) for details.
