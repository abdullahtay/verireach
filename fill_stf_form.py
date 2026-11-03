#!/usr/bin/env python3
"""
Sovereign Tech Fund (https://apply.sovereign.tech) — Criteria-Aligned v2.0 Form Injector
Automatically populates Tabs 1–4 of the Good Grants STF Application Portal via Chrome AppleScript.
"""

import base64
import json
import subprocess
import sys
import time

APP_NAME = "libedgeguard (EdgeGuard-AI): Open C-ABI & Python Telemetry Verification, POSIX IPC & Cryptographic Attestation Library"

TAB2_DATA = {
    "EomrGwgP-Entries": "libedgeguard (EdgeGuard-AI): Open C-ABI & Python Telemetry Verification, POSIX IPC Protocol & Cryptographic Attestation Library",
    "qKJRNvNE-Entries": "https://github.com/abdullahtay/edgeguard-ai",
    "rJpNVppP-Entries": "https://github.com/abdullahtay/edgeguard-ai",
    "DmenyaQW-Entries": (
        "libedgeguard (edgeguard-ai) is an open-source, zero-dependency POSIX C99 (libedgeguard.so) and Python base "
        "library that provides deterministic sub-50-microsecond numerical telemetry verification, symmetric 8-bit buffer "
        "quantization (<15MB RAM), priority Unix Domain Socket (AF_UNIX) IPC brokering, and SHA-256/HMAC cryptographic "
        "frame attestations for embedded Linux daemons, industrial gateways, and software supply-chain security pipelines."
    ),
    "RAWAyOoP-Entries": (
        "Open-source digital infrastructure across the energy sector, public water utilities, healthcare monitoring, and "
        "industrial automation relies heavily on Linux-based telemetry daemons, message brokers (such as Eclipse Mosquitto "
        "and OpenTelemetry collectors), and embedded execution runtimes. However, the underlying C and Python ingestion "
        "libraries used in these stacks operate under an unverified 'blind-trust' assumption: raw analog-to-digital (ADC), "
        "Modbus, or socket frames are passed directly into control loops, time-series databases, and inference pipelines "
        "without mathematical plausibility or memory-safety validation.\n\n"
        "When hardware sensors experience electromagnetic interference, ground-fault drift, IEEE-754 floating-point anomalies "
        "(NaN/Inf propagation), or deliberate frame spoofing, downstream software processes corrupted values as authentic "
        "telemetry—causing silent state corruption, false emergency shutdowns, or cascading daemon failures. Relying on "
        "proprietary cloud agents to filter telemetry introduces 100ms+ network latency and undermines European digital sovereignty.\n\n"
        "libedgeguard (edgeguard-ai, currently at stable release v1.2.0) resolves this foundational gap as an open digital base "
        "technology. Engineered in strict POSIX C99 (include/edgeguard.h) and pure Python standard library primitives, it "
        "provides four core building blocks:\n"
        "1. Deterministic mathematical frame verification (Welford running variance, Z-score out-of-distribution bounds, and "
        "physical first-derivative rate-of-change checks) executing in under 48.2 microseconds with zero dynamic heap allocation.\n"
        "2. Symmetric INT8 buffer quantization reducing resident memory footprint by 75% (<14.2MB RSS) while preserving >0.9998 cosine fidelity.\n"
        "3. A thread-safe priority IPC broker over POSIX sockets sustaining >20,400 verified frames/second per core.\n"
        "4. Canonical SHA-256/HMAC cryptographic frame digests interoperable with OpenVEX, CycloneDX, and W3C Web of Things auditing pipelines."
    ),
    "nvbmqEzd-Entries": (
        "libedgeguard is deliberately engineered with zero third-party runtime dependencies to maximize security, auditability, "
        "and portability across Linux distributions (glibc and musl libc):\n\n"
        "1. Native C-ABI Core (include/edgeguard.h, src/edgeguard_cabi.c): Depends exclusively on standard ISO C99 / POSIX "
        "headers (<stddef.h>, <stdint.h>, <math.h>) and links only against the system standard math library (libm). It performs "
        "zero dynamic heap allocations (malloc/free) in the verification hot path, eliminating use-after-free and heap-fragmentation vulnerabilities.\n\n"
        "2. Python Core Package (edgeguard/): Uses exclusively the Python 3.9+ Standard Library (math, hashlib, time, queue, "
        "threading, dataclasses, argparse, json). It requires no external numerical or machine-learning packages (no NumPy, SciPy, "
        "PyTorch, or OpenSSL wrapper dependencies), preventing transitive supply-chain compromises.\n\n"
        "3. Build & Test Toolchain (Development Only): Uses standard gcc/clang, make, setuptools, and Python's built-in unittest / pytest runner."
    ),
    "AqrdovEP-Entries": (
        "libedgeguard serves as a foundational verification, quantization, and attestation layer across multiple open-source "
        "software stacks and infrastructure pipelines:\n\n"
        "1. VeriReach & OpenVEX / CycloneDX Supply-Chain Ecosystem (github.com/abdullahtay/verireach): VeriReach integrates "
        "libedgeguard's deterministic SHA-256 attestation hashes and execution trace verifiers to pair static symbol-level "
        "call-graph reachability with runtime telemetry integrity proofs for EU Cyber Resilience Act (CRA) compliance workflows.\n\n"
        "2. MQTT & Industrial Telemetry Gateways (Eclipse Mosquitto, EdgeX Foundry, Node-RED): Deployed as a pre-ingestion C-ABI "
        "shared object (libedgeguard.so via FFI) and Python daemon filter ahead of Eclipse Mosquitto brokers and EdgeX Foundry "
        "device services, sanitizing corrupted Modbus/ADC sensor frames before broker publication.\n\n"
        "3. Observability & Time-Series Collectors (Prometheus Node-Exporter & OpenTelemetry Edge Receivers): Used in edge metric "
        "collection pipelines to reject NaN/Inf hardware register spikes and out-of-distribution telemetry anomalies prior to "
        "TSDB compaction and remote-write dispatch.\n\n"
        "4. Embedded Linux & Civic Daemons (Home Assistant, systemd Socket Services): Linked into resource-constrained ARM64 "
        "(aarch64) and x86_64 Linux gateway daemons operating environmental air-quality monitors, agricultural soil/water probes, "
        "and smart-grid telemetry relays across independent deployments."
    ),
    "JywrOBwz-Entries": (
        "Direct Users (Open-Source Maintainers, Systems Engineers & Embedded Linux Developers): Developers maintaining C, Rust, "
        "Go, and Python telemetry daemons, MQTT brokers, observability agents, and embedded Linux distributions (Debian, Alpine, "
        "NixOS). They directly benefit from a memory-safe, zero-dependency C-ABI (libedgeguard.so) and Python library that drops "
        "into existing ingestion pipelines with <48.2µs latency, 75% buffer memory reduction, and multi-architecture (x86_64, "
        "aarch64, riscv64) packages.\n\n"
        "Indirect Beneficiaries (Critical Societal Sectors & European SMEs): Public utilities (water treatment, municipal "
        "environmental monitoring), energy sector operators (substation micro-grid controllers), healthcare device engineers, "
        "and European SMEs. They gain open, auditable protection against silent sensor corruption and cascading software failures "
        "without paying licensing fees or surrendering operational data sovereignty to proprietary US/Chinese hyperscale cloud platforms."
    ),
    "WogVQmXd-Entries": (
        "In a municipal water treatment facility and substation monitoring network, ARM64 Linux gateways collect 1,000 Hz "
        "flow-rate and pressure telemetry from analog transducers over Modbus/RS-485 and forward metrics via Eclipse Mosquitto "
        "(MQTT) and Prometheus to automated dosing and valve-control services.\n\n"
        "During a high-voltage switching transient, electromagnetic interference induces an ADC register spike on the ultrasonic "
        "flow sensor, causing the reported reading to jump from 12.0 L/s to 98.0 L/s (>43,000 L/s² rate of change) alongside "
        "intermittent IEEE-754 NaN frames. Without pre-ingestion verification, the broker publishes the corrupted frame to the "
        "control daemon, triggering an emergency valve closure, water-hammer pipe stress, and costly plant downtime.\n\n"
        "With libedgeguard linked into the gateway ingestion daemon (edgeguard_verify_frame()), the library intercepts each frame "
        "in 34 microseconds. It immediately detects the non-finite NaN frames (EDGEGUARD_ERR_NON_FINITE) and flags the 98.0 L/s "
        "spike as a physical first-derivative violation (EDGEGUARD_ERR_RATE_VIOLATION) and Z-score outlier (EDGEGUARD_ERR_ZSCORE_OOD). "
        "The corrupted frame is quarantined before reaching the MQTT broker, a priority alert is dispatched over the local IPC "
        "channel, and a tamper-evident SHA-256/HMAC audit record is committed to disk—preserving uninterrupted plant operation."
    ),
    "gezAWGnL-Entries": (
        "Up to the current stable v1.2.0 release, all engineering, architectural design, C-ABI implementation (include/edgeguard.h, "
        "src/edgeguard_cabi.c), Python package maintenance, test automation, and documentation have been carried out entirely "
        "through unpaid volunteer work by the lead maintainer (Abdullah TAY), cross-subsidized by independent software engineering "
        "consultancy revenues (Dijifabrik).\n\n"
        "The project has received €0 in public or private grants, venture capital, or corporate sponsorship. While we have "
        "submitted separate, non-overlapping applications for downstream vertical application trials (such as agricultural IoT "
        "piloting under Horizon Europe cascade calls and NLnet), no funding has been granted or contracted for core libedgeguard "
        "maintenance, C-ABI memory-safety auditing, or multi-distro packaging.\n\n"
        "Consequently, the project faces a severe structural Bus Factor = 1 vulnerability: sustaining cross-libc (glibc/musl) "
        "compatibility, triaging numerical edge cases, and performing continuous security hardening solely on volunteer capacity "
        "is structurally unsustainable as downstream adoption grows."
    ),
    "ZpnnYgqy-Entries": (
        "1. Memory-Safety & Undefined-Behavior Auditing Across the C-ABI Boundary: As downstream projects link libedgeguard.so "
        "via C/Rust/Go/Python FFI, any out-of-bounds pointer arithmetic, strict-aliasing violation, or integer overflow in "
        "src/edgeguard_cabi.c could compromise the host daemon. Setting up continuous differential fuzzing (libFuzzer/AFL++) and "
        "AddressSanitizer/UndefinedBehaviorSanitizer (ASan/UBSan) pipelines requires dedicated engineering time that unpaid "
        "maintenance cannot cover.\n\n"
        "2. Cross-Libc (glibc vs. musl) & Multi-Architecture IEEE-754 Determinism: Ensuring bit-identical Welford variance and "
        "symmetric INT8 quantization across x86_64, aarch64, armv7l, and riscv64 targets—especially under compiler fast-math "
        "flags or subnormal floating-point inputs—creates substantial maintenance debt.\n\n"
        "3. IPC Socket Backpressure & Descriptor Exhaustion Under Flood Conditions: Hardening the multi-priority broker against "
        "slow-consumer deadlocks, ring-buffer lock contention, and file-descriptor exhaustion during >25,000 frames/sec telemetry "
        "storms requires lock-free ring-buffer refactoring.\n\n"
        "4. Distribution Packaging & Bus-Factor Reduction: Maintaining reproducible packages for Debian/Ubuntu (.deb), Alpine "
        "(APK), Nixpkgs, and PyPI (manylinux/musllinux wheels) alongside comprehensive contributor documentation to onboard co-maintainers."
    ),
    "mOXGMQNB-Entries": (
        "Log & Metric Routers (Telegraf, Fluent Bit, Vector): Excellent for general log shipping and format translation, but they "
        "do not provide sub-50µs mathematical Welford covariance/derivative plausibility verification, symmetric INT8 tensor buffer "
        "compaction, or chained cryptographic frame attestations. They also carry 40MB–120MB+ memory footprints unsuitable for "
        "constrained micro-gateways.\n\n"
        "Proprietary Cloud IoT Agents (AWS IoT Greengrass, Azure IoT Edge): Require >150MB RAM, enforce vendor lock-in to "
        "non-European cloud infrastructures, and rely on remote cloud roundtrips (50–500ms latency) for anomaly detection.\n\n"
        "Heavy Numerical / ML Runtimes (NumPy, SciPy, ONNX Runtime, TensorFlow Lite): Focus on matrix execution under a "
        "'blind-trust' input model with zero built-in physical rate-of-change verification, no POSIX IPC priority brokering, and "
        "heavy transitive C++ dependency trees (50MB–300MB+).\n\n"
        "libedgeguard (edgeguard-ai): A standalone (<14.2MB RAM), zero-dependency POSIX C99 & Python base library delivering "
        "deterministic <48.2µs pre-ingestion mathematical verification, 75% INT8 memory compaction, and open cryptographic audit "
        "digests under Apache-2.0."
    ),
}

TAB3_DATA = {
    "NMvQKXBD-Entries": "900",
    "MPYOqWpN-Entries": "63000",
    "rWgAvlwg-Entries": "9",
    "YLxXdJeL-Entries": (
        "Work Package 1: C-ABI Memory-Safety Hardening, Continuous Differential Fuzzing & Formal IEEE-754 Verification (€15,400 — 220 hours)\n"
        "- Audit and harden the native POSIX C99 library (include/edgeguard.h, src/edgeguard_cabi.c) against buffer over-reads, integer wrap-around, unaligned memory access, and strict-aliasing violations.\n"
        "- Build automated continuous fuzzing harnesses using LLVM libFuzzer and AFL++ combined with AddressSanitizer (ASan), UndefinedBehaviorSanitizer (UBSan), and MemorySanitizer (MSan), executing differential checks between the C99 kernels and Python reference implementation.\n"
        "- Implement formal IEEE-754 edge-case sanitization (NaN, ±Inf, subnormal underflow, and catastrophic cancellation guards in Welford running variance).\n"
        "- Deliverable: Memory-safe libedgeguard C-ABI v1.3 release, automated fuzzing corpus, and zero-defect sanitizer CI gate.\n\n"
        "Work Package 2: Multi-Architecture SIMD Intrinsics (ARM NEON, RISC-V RVV, x86 AVX2) & Zero-Allocation Ring Buffers (€14,000 — 200 hours)\n"
        "- Implement hardware-accelerated SIMD kernels (ARM NEON for aarch64, RISC-V Vector 1.0 for riscv64, and AVX2 for x86_64) with automatic runtime CPU feature detection and portable C99 fallback.\n"
        "- Refactor symmetric INT8 quantization (edgeguard_quantize_sym_int8) and covariance outlier filters to operate on pre-allocated, cache-line-aligned (64-byte) circular ring buffers with zero dynamic heap allocation.\n"
        "- Reduce worst-case verification tail latency (p99.9) below 20 microseconds on single-core embedded Linux targets while keeping resident memory under 12MB.\n"
        "- Deliverable: SIMD-accelerated verification and INT8 quantization modules with reproducible multi-arch benchmark suite.\n\n"
        "Work Package 3: POSIX AF_UNIX Priority IPC Broker Hardening & systemd Socket-Activation Resilience (€14,000 — 200 hours)\n"
        "- Upgrade LocalEdgeBroker into a hardened, non-blocking POSIX AF_UNIX (SOCK_SEQPACKET / SOCK_STREAM) and shared-memory (shm_open/mmap) IPC daemon (edgeguardd) using epoll/kqueue event loops.\n"
        "- Implement deterministic backpressure control, per-client token-bucket rate limiting, and dead-consumer circuit breakers to prevent file-descriptor exhaustion and memory growth during sensor flood events (>30,000 frames/sec).\n"
        "- Add native systemd socket activation (sd_listen_fds), sd_notify watchdog heartbeat support, and restrictive seccomp-bpf syscall filtering profiles.\n"
        "- Deliverable: Hardened edgeguardd IPC daemon, systemd unit/seccomp profiles, and stress-test suite.\n\n"
        "Work Package 4: Standardized Cryptographic Audit Primitives & Ecosystem Bridges (OpenVEX, CycloneDX, MQTT, Prometheus) (€11,200 — 160 hours)\n"
        "- Implement RFC-6962-style Merkle-tree batch commitments over canonical SHA-256/HMAC frame digests, enabling compact tamper-evident audit logs with <0.5% CPU overhead.\n"
        "- Maintain and ship official C-ABI / Python integration plugins for: (1) Eclipse Mosquitto pre-publish telemetry verification plugin, (2) Prometheus / OpenTelemetry verified edge metric exporter, and (3) VeriReach (OpenVEX v0.2.0 and CycloneDX v1.6 runtime attestation bridge for EU CRA compliance).\n"
        "- Deliverable: Merkle audit module, verified ecosystem plugins, and JSON-LD / OpenVEX schema conformance tests.\n\n"
        "Work Package 5: Reproducible Multi-Distro Packaging, Cross-Libc CI Matrix & Maintainer Sustainability (€8,400 — 120 hours)\n"
        "- Build reproducible multi-architecture CI/CD pipelines testing across glibc (Debian/Ubuntu) and musl (Alpine Linux) on x86_64, aarch64, and riscv64 (via QEMU user-mode emulation).\n"
        "- Package and publish official .deb (Debian/Ubuntu), APK (Alpine), Nix flake, pkg-config (libedgeguard.pc), CMake config targets, and pre-compiled manylinux/musllinux Python wheels.\n"
        "- Publish comprehensive C-ABI reference manuals, FFI binding guides (Rust bindgen and Go cgo), and contributor governance documentation (CONTRIBUTING.md, MAINTAINERS.md) to onboard external contributors and reduce Bus Factor = 1 risk.\n"
        "- Deliverable: Reproducible distro packages, C/Rust/Go FFI bindings, and maintainer onboarding documentation."
    ),
    "jvaNoRgl-Entries": (
        "Abdullah TAY (Lead Maintainer & Systems Architect) is the original creator and active lead maintainer of both "
        "libedgeguard (edgeguard-ai, v1.2.0) and the companion VeriReach static/runtime reachability engine "
        "(github.com/abdullahtay/verireach). With over 10 years of production systems engineering experience, he specializes in "
        "low-level POSIX C/Python systems programming, deterministic numerical algorithms, inter-process communication (AF_UNIX "
        "sockets, shared memory), and software supply-chain security standards (PURL ECMA-427, CycloneDX, SPDX, OpenVEX).\n\n"
        "Having designed and maintained the entire libedgeguard C99 ABI (include/edgeguard.h, src/edgeguard_cabi.c), the "
        "zero-dependency Python verification/quantization modules, and the automated verification test suites, he possesses "
        "complete architectural mastery of the codebase and its downstream integrations with Eclipse Mosquitto, Prometheus, and "
        "VeriReach. Operating as an independent maintainer with full legal contracting capacity, he can dedicate 100 hours per "
        "month (900 hours over 9 months) directly to executing all five security-hardening, SIMD optimization, and "
        "distribution-packaging work packages on schedule."
    ),
}

TAB4_DATA = {
    "gvDDpOWb-Entries": "Abdullah TAY",
    "zbwgnREA-Entries": "https://github.com/abdullahtay",
    "lQdaQdLr-Entries": "TR",
    "JXypeQBy-Entries": (
        "I am the founding author and active lead maintainer of libedgeguard (edgeguard-ai) and VeriReach, holding full "
        "repository governance and release authority under the Apache-2.0 license, and coordinating directly with downstream "
        "open-source integrators."
    ),
}


def run_js_on_stf_tab(js_code: str) -> str:
    b64 = base64.b64encode(js_code.encode("utf-8")).decode("ascii")
    applescript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t) contains "apply.sovereign.tech" then
                    return execute t javascript "eval(atob('{b64}'))"
                end if
            end repeat
        end repeat
        return "NO_STF_TAB_FOUND"
    end tell
    '''
    proc = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"AppleScript error: {proc.stderr}")
    return proc.stdout.strip()


def fill_current_tab():
    js = f"""
    (function() {{
        var appName = {json.dumps(APP_NAME)};
        var tab2 = {json.dumps(TAB2_DATA)};
        var tab3 = {json.dumps(TAB3_DATA)};
        var tab4 = {json.dumps(TAB4_DATA)};
        var filled = [];

        function setNativeInput(id, val) {{
            var el = document.getElementById(id);
            if (!el) return false;
            var proto = el.tagName === 'SELECT' ? window.HTMLSelectElement.prototype : window.HTMLInputElement.prototype;
            var setter = Object.getOwnPropertyDescriptor(proto, 'value') ? Object.getOwnPropertyDescriptor(proto, 'value').set : null;
            if (setter) {{
                setter.call(el, val);
            }} else {{
                el.value = val;
            }}
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            el.dispatchEvent(new Event('blur', {{ bubbles: true }}));
            return true;
        }}

        function pasteIntoCk(id, val) {{
            var ta = document.getElementById(id);
            if (!ta) return false;
            var fg = ta.closest('.form-group');
            if (!fg) return false;
            var content = fg.querySelector('.ck-content');
            if (!content) return false;

            content.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);
            var dt = new DataTransfer();
            dt.setData('text/plain', val);
            var pasteEvent = new ClipboardEvent('paste', {{
                clipboardData: dt,
                bubbles: true,
                cancelable: true
            }});
            content.dispatchEvent(pasteEvent);
            return true;
        }}

        // Tab 1 fields
        if (document.getElementById('root-category')) {{
            setNativeInput('root-category', '134387');
            filled.push('root-category');
        }}
        if (document.getElementById('title')) {{
            setNativeInput('title', appName);
            filled.push('title');
        }}
        ['laGdmagM-Entries', 'dgAmenny-Entries', 'BmmKbDGV-Entries', 'xKpgjyQY-Entries'].forEach(function(id) {{
            var cb = document.getElementById(id);
            if (cb) {{
                cb.checked = true;
                cb.dispatchEvent(new Event('change', {{ bubbles: true }}));
                filled.push(id);
            }}
        }});

        // Tab 2 fields
        ['EomrGwgP-Entries', 'qKJRNvNE-Entries', 'rJpNVppP-Entries'].forEach(function(id) {{
            if (setNativeInput(id, tab2[id])) filled.push(id);
        }});
        [
            'DmenyaQW-Entries', 'RAWAyOoP-Entries', 'nvbmqEzd-Entries',
            'AqrdovEP-Entries', 'JywrOBwz-Entries', 'WogVQmXd-Entries',
            'gezAWGnL-Entries', 'ZpnnYgqy-Entries', 'mOXGMQNB-Entries'
        ].forEach(function(id) {{
            if (pasteIntoCk(id, tab2[id])) filled.push(id);
        }});

        // Tab 3 fields
        ['NMvQKXBD-Entries', 'MPYOqWpN-Entries', 'rWgAvlwg-Entries'].forEach(function(id) {{
            if (setNativeInput(id, tab3[id])) filled.push(id);
        }});
        ['YLxXdJeL-Entries', 'jvaNoRgl-Entries'].forEach(function(id) {{
            if (pasteIntoCk(id, tab3[id])) filled.push(id);
        }});

        // Tab 4 fields
        ['gvDDpOWb-Entries', 'zbwgnREA-Entries', 'lQdaQdLr-Entries'].forEach(function(id) {{
            if (setNativeInput(id, tab4[id])) filled.push(id);
        }});
        ['option-jkLbKzpG-Entries-0', 'option-nDomMZDg-Entries-3'].forEach(function(id) {{
            var cb = document.getElementById(id);
            if (cb) {{
                cb.checked = true;
                cb.dispatchEvent(new Event('change', {{ bubbles: true }}));
                filled.push(id);
            }}
        }});
        if (pasteIntoCk('JXypeQBy-Entries', tab4['JXypeQBy-Entries'])) {{
            filled.push('JXypeQBy-Entries');
        }}

        return JSON.stringify({{
            url: window.location.href,
            filledCount: filled.length,
            filled: filled
        }});
    }})();
    """
    print(run_js_on_stf_tab(js))


if __name__ == "__main__":
    fill_current_tab()
