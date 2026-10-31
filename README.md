# VeriReach

> **Symbol-Level Call-Graph Reachability & Automated OpenVEX Generator for PURL and SBOM Ecosystems**

[![CI](https://github.com/abdullahtay/verireach/actions/workflows/ci.yml/badge.svg)](https://github.com/abdullahtay/verireach/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![OpenVEX Compliant](https://img.shields.io/badge/OpenVEX-v0.2.0-green.svg)](https://openvex.dev/)
[![CycloneDX VEX](https://img.shields.io/badge/CycloneDX-VEX_1.5-brightgreen.svg)](https://cyclonedx.org/)

---

## What is VeriReach?

**VeriReach** is an open-source software supply chain security tool that eliminates false-positive vulnerability alerts. 

Traditional vulnerability scanners (Trivy, Syft, Grype, ScanCode) report any package version that matches a known CVE. However, **over 80% of reported vulnerabilities in transitive dependencies reside in functions that are never called by the downstream application**.

VeriReach solves this by constructing a static call graph of your application, resolving vulnerability advisories down to individual function/method symbols, and mathematically verifying whether an execution path exists from your application entrypoints to the vulnerable symbol.

If no path exists, VeriReach automatically generates a compliant **OpenVEX** or **CycloneDX VEX** attestation with justification:
```
vulnerable_code_not_in_execute_path
```

This drastically reduces alert fatigue and enables automated compliance with the **EU Cyber Resilience Act (CRA)**.

---

## Key Features

- **PURL Native (ECMA-427):** First-class support for standard Package-URLs across `pkg:pypi`, `pkg:npm`, `pkg:cargo`, `pkg:golang`, `pkg:maven`, etc.
- **Multi-Format SBOM Ingestion:** Ingests CycloneDX (1.4 / 1.5 / 1.6) and SPDX (2.2 / 2.3 / 3.0) JSON documents.
- **Symbol-Level Advisory Resolution:** Maps CVEs directly to affected function and method symbols using VulnerableCode and OSV formats.
- **Inter-Procedural Call Graph Analysis:** Deterministic BFS traversal resolving cross-module calls, imports, and shortest execution traces.
- **Dual VEX Output:** Generates standard [OpenVEX v0.2.0](https://openvex.dev/) and [CycloneDX 1.5/1.6 VEX](https://cyclonedx.org/) JSON.
- **Zero Runtime Dependencies:** Built strictly using the Python Standard Library (`ast`, `json`, `argparse`, `urllib`) for deterministic, secure deployment in any CI/CD environment.

---

## Architecture Overview

```
 [ CycloneDX / SPDX SBOM ]             [ Source Code Tree ]
            │                                    │
            ▼                                    ▼
     [ SBOM Parser ]                   [ Call-Graph Builder ]
     (PURL Extraction)                   (AST Node Traversal)
            │                                    │
            ▼                                    │
 [ Advisory Resolver (PURL) ]                    │
 (OSV / VulnerableCode Mappings)                 │
            │                                    │
            └─────────────────┬──────────────────┘
                              │
                              ▼
                 [ Reachability Engine ]
                 (BFS Path Verification)
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
       [ Reachable Path ]           [ Zero Execution Path ]
        Status: affected             Status: not_affected
        Trace: [A -> B -> C]         Justification:
                                     vulnerable_code_not_in_execute_path
               │                             │
               └──────────────┬──────────────┘
                              │
                              ▼
                     [ VEX Generator ]
                  (OpenVEX & CycloneDX VEX)
```

---

## Installation

```bash
git clone https://github.com/abdullahtay/verireach.git
cd verireach
pip install -e .
```

---

## Quickstart & CLI Usage

### 1. Perform an End-to-End Reachability Scan

Scan an SBOM against your source code directory and generate OpenVEX statements:

```bash
verireach scan \
  --sbom tests/fixtures/sample_sbom.json \
  --src tests/fixtures/vulnerable_app \
  --entrypoint main.py \
  --advisories tests/fixtures/mock_advisories.json \
  --format openvex
```

#### Output Example:

```json
=== VeriReach Symbol-Level Reachability Report ===
Components Analyzed        : 4
Vulnerable Components Mapped: 2
Total Advisory Findings     : 2
Real Affected (Reachable)   : 1
False Positives Eliminated : 1
Noise Reduction Rate        : 50.0%
Generated VEX Statements   : 2

{
  "@context": "https://openvex.dev/ns/v0.2.0",
  "@id": "https://openvex.dev/docs/public/vex-...",
  "author": "VeriReach Analysis Engine",
  "role": "Automated Static Analysis Tool",
  "statements": [
    {
      "vulnerability": {
        "name": "CVE-2024-99001"
      },
      "products": [
        {
          "@id": "pkg:pypi/fast-crypto@1.2.0"
        }
      ],
      "status": "not_affected",
      "justification": "vulnerable_code_not_in_execute_path",
      "impact_statement": "Static call-graph analysis verified that vulnerable symbol 'insecure_des_decrypt' is dead code or never invoked from entrypoint 'main.py'. Zero execution paths exist."
    },
    {
      "vulnerability": {
        "name": "CVE-2024-99002"
      },
      "products": [
        {
          "@id": "pkg:pypi/jwt-auth-helper@2.4.1"
        }
      ],
      "status": "affected",
      "action_statement": "Vulnerable symbol 'verify_token_weak' is called in runtime execution path. Upgrade package or refactor calling code.",
      "status_notes": "Symbol reachability confirmed via call chain: [main.main -> main.process_request -> vendor.lib_auth.verify_token_weak] from entrypoint 'main.main'."
    }
  ]
}
```

### 2. Export CycloneDX 1.5/1.6 VEX

```bash
verireach scan \
  --sbom tests/fixtures/sample_sbom.json \
  --src tests/fixtures/vulnerable_app \
  --entrypoint main.py \
  --advisories tests/fixtures/mock_advisories.json \
  --format cyclonedx \
  --output report.cyclonedx.json
```

### 3. Test Target Symbol Reachability via Call Graph

Check if a specific function is reachable from application entrypoints:

```bash
verireach callgraph --src tests/fixtures/vulnerable_app --target verify_token_weak
```

```text
AFFECTED (Reachable): verify_token_weak is called via [main.main -> main.process_request -> vendor.lib_auth.verify_token_weak] from entrypoint 'main.main'
Execution chain: main.main -> main.process_request -> vendor.lib_auth.verify_token_weak
```

### 4. Parse and Validate Package-URLs (PURL)

```bash
verireach purl "pkg:npm/@angular/core@12.3.1" --json
```

---

## Running Tests

VeriReach includes a comprehensive test suite covering PURL parsing, SBOM ingestion, AST call-graph traversals, and end-to-end VEX generation:

```bash
python3 -m unittest discover -s tests -v
```

---

## NLnet Foundation & Horizon Europe

VeriReach is designed as a public digital commons under the **NLnet Foundation** open calls ([CodeSupply](https://nlnet.nl/codesupply) and [Restack — Open Internet Stack](https://nlnet.nl/restack)), supported by the European Commission's Horizon Europe framework.

It specifically integrates with and supports the open-source **AboutCode** ecosystem (`VulnerableCode`, `ScanCode`, and `PurlDB`), providing the symbol-level reachability layer needed for automated EU CRA compliance.

---

## License

Distributed under the **Apache License, Version 2.0**. See [`LICENSE`](LICENSE) for details.
