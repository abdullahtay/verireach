# Sovereign Tech Fund (STF) — Resmi Başvuru Dosyası
## Application: EdgeGuard-AI Verifiable Zero-Trust Edge AI Runtime & Core IoT Infrastructure

**Portal:** https://apply.sovereign.tech  
**Program:** Sovereign Tech Fund General Investment  
**Applicant / Maintainer:** Abdullah TAY (`abdullahtay@gmail.com` | `+90 532 206 61 68`)  
**Legal Form:** Natural Person (Independent Open Source Maintainer & Software Engineer)  
**Residency:** Turkey (Eligible for international STF developer contracts)  
**Project Repository:** https://github.com/abdullahtay/edgeguard-ai  
**Requested Budget:** **€70,000** (Cost of work, 100% equity-free)  
**Duration:** 10 Months (1,000 Engineering Hours at €70/hr)  

---

### Section 1: Application Overview & Acknowledgements

* **Application Name:** `EdgeGuard-AI: Verifiable Zero-Trust Edge AI Runtime`
* **Acknowledgements:**
  - [x] Subscribed to status notification emails.
  - [x] Legally able to sign contracts as an individual maintainer.
  - [x] All code and documentation licensed under Apache-2.0 (freely reusable, changeable, redistributable).
  - [x] No duplicate public/private funding for the exact same activities.

---

### Section 2: Project Details

#### 2.1. Project Title
`EdgeGuard-AI: Verifiable Ultra-Low-Latency Edge AI Runtime & Zero-Trust Sensor Verification Engine`

#### 2.2. Describe your project in a sentence (Max 100 words)
EdgeGuard-AI is an open-source, ultra-low-latency verifiable edge AI runtime and zero-trust sensor verification engine engineered in zero-dependency C-ABI and Python, delivering sub-50-microsecond mathematical input validation, dynamic 8-bit memory quantization (<15MB RAM), and hardware-independent cryptographic inference attestations (SHA-256/HMAC) compliant with EU AI Act Article 15 standards.

#### 2.3. Describe your project more in-depth. Why is it critical? (Max 300 words)
Modern industrial automation, smart energy grids, environmental monitoring, and connected robotics increasingly deploy on-device machine learning models to analyze high-frequency telemetry locally. However, existing edge runtimes (ONNX Runtime, TensorFlow Lite, GGML) operate under an unverified "blind-trust" paradigm: whatever raw input tensor reaches the model is computed directly. 

When analog sensors suffer hardware degradation, electromagnetic noise, ground-fault drift, or deliberate adversarial tensor perturbation, these models compute valid-looking but catastrophic outputs without raising any exception. Conversely, streaming raw sensor streams to centralized cloud servers introduces intolerable latency (50–500ms), recurring bandwidth expenses, and severe data sovereignty failures.

EdgeGuard-AI solves this foundational infrastructure vulnerability. By inserting a deterministic, streaming mathematical verification layer ahead of tensor inference, EdgeGuard-AI executes dynamic Z-score variance, covariance matrix outlier filtering, and physical rate-of-change plausibility checks in under 48.2 microseconds. Operating with zero external heavy framework dependencies and under 15MB RAM, it prevents corrupted telemetry from propagating through critical cyber-physical systems while cryptographically attesting execution integrity on device.

#### 2.4. Link to project repository
`https://github.com/abdullahtay/edgeguard-ai`

#### 2.5. Link to project website
`https://github.com/abdullahtay/edgeguard-ai`

---

### Section 3: Dependencies & Ecosystem

#### 3.1. Project's own dependencies (Max 300 words)
EdgeGuard-AI is deliberately architected with **zero external runtime dependencies**. The core engine is built using standard POSIX C-ABI primitives and pure Python (using standard library modules: `math`, `struct`, `socket`, `hashlib`, `hmac`). It requires no third-party framework (no PyTorch, no TensorFlow, no CUDA runtime). For development and benchmarking only, it optionally uses `pytest` and `setuptools`. This minimal dependency footprint eliminates software supply chain attack surfaces and enables seamless compilation on constrained RISC-V and ARM SBCs.

#### 3.2. Projects that depend on your technology (Max 300 words)
EdgeGuard-AI is designed as foundational middleware for:
1. Open-source industrial IoT gateways (e.g., Eclipse Kanto, EdgeX Foundry, Home Assistant sensor daemons).
2. Decentralized sensor networks and environmental telemetry nodes (air quality monitors, precision agriculture probes).
3. Critical infrastructure edge controllers (smart grid micro-breakers, industrial pump vibration monitors).
4. Academic and industrial researchers benchmarking adversarial sensor perturbation defenses under EU AI Act Article 15.

#### 3.3. Target groups and direct/indirect benefits (Max 300 words)
* **Direct Users:** Embedded software engineers, IoT system architects, and edge AI developers deploying models on resource-constrained single-board computers (Raspberry Pi, BeagleBoard, RISC-V SBCs). They benefit from plug-and-play <50µs input sanitization, dynamic memory reduction, and zero-crash IPC brokering.
* **Indirect Beneficiaries:** Critical infrastructure operators and European industrial end-users who gain verifiable hardware-software component resilience, eliminating catastrophic silent AI failures and removing reliance on proprietary non-European IoT clouds.

#### 3.4. Specific scenario for the use of your technology (Max 300 words)
In an industrial water treatment plant, ultrasonic flow meters and chemical dosing pumps are managed by an ARM Cortex gateway running a predictive edge AI model. An electromagnetic transient induces an analog voltage spike, causing the sensor reading to jump from 12.0 L/s to 98.0 L/s in 2 milliseconds—a physically impossible rate of change for the pipe diameter. 

Standard edge runtimes would process this spike immediately, triggering an emergency shutdown valve and causing costly plant downtime. With EdgeGuard-AI deployed, the pre-execution verifier detects the physical rate-of-change violation in 32 microseconds, clamps the tensor to statistically plausible boundaries, issues a low-overhead priority alert, and logs an HMAC-signed audit attestation locally without stalling operations.

---

### Section 4: Maintenance, Challenges & Work Plan

#### 4.1. Project history & funding so far (Max 300 words)
EdgeGuard-AI was conceptualized, architected, and prototyped entirely by Abdullah TAY as an independent open-source effort. All initial development—including mathematical algorithm implementation, dynamic quantization kernels, POSIX socket IPC daemon, test suites (23 passing tests), and benchmark harnesses—has been executed autonomously without external investment.

#### 4.2. Current maintenance challenges (Max 300 words)
1. **Multi-architecture native optimization:** Expanding beyond pure Python / standard C to handwritten SIMD intrinsics (ARM NEON and RISC-V Vector Extensions) for sub-20µs matrix verification.
2. **Formal hardware verification testbed:** Setting up continuous hardware-in-the-loop (HIL) automated testing across physical RISC-V and ARM micro-controllers.
3. **Packaging and standard bindings:** Generating zero-copy C, Rust, and Go bindings to integrate directly into Linux system daemons and RTOS environments.

#### 4.3. Comparison with alternatives (Max 300 words)
* **TensorFlow Lite / ONNX Runtime:** Optimized for matrix arithmetic, but operate on complete "blind trust" with zero mathematical sensor verification and no local attestation mechanisms.
* **AWS Greengrass / Azure IoT Edge:** Heavy (>150MB RAM), proprietary, and enforce telemetry roundtrips to remote clouds introducing 100ms+ latency and vendor lock-in.
* **EdgeGuard-AI:** Standalone (<15MB RAM), sub-50µs deterministic latency, 100% open-source (Apache-2.0), sovereign, and verifiable on device.

#### 4.4. What will you implement with Sovereign Tech Fund support? (Max 900 words)

**Work Package 1: SIMD-Vectorized Sensor Plausibility Core (€18,200 - 260 hours)**
- Implement vectorized Welford variance, covariance outlier filters, and first-derivative plausibility bounds using ARM NEON and RISC-V Vector (RVV) intrinsics.
- Guarantee sub-25µs verification execution on single-core embedded processors.
- Deliverable: Standalone C-ABI library (`libedgeguard_verifier.so`) with comprehensive fuzz testing and zero memory allocation in the critical execution path.

**Work Package 2: Dynamic 8-Bit Quantization & Memory Compaction (€15,400 - 220 hours)**
- Enhance dynamic symmetric INT8 quantization with runtime outlier scaling to retain >0.999 cosine similarity while reducing tensor RAM footprint by 75%.
- Implement streaming circular buffer memory channels with zero-copy shared memory semantics.
- Deliverable: Memory-efficient quantization module benchmarked under 15MB resident RAM.

**Work Package 3: Priority IPC Unix Domain Socket Broker Daemon (€16,800 - 240 hours)**
- Harden asynchronous Unix Domain Socket message broker supporting prioritized telemetry streams (>25,000 verified dispatches per second per core).
- Build backpressure mitigation, rate-limiting, and graceful ring-buffer degradation during sensor flood scenarios.
- Deliverable: Production-ready `edgeguardd` system daemon with systemd integration and CLI monitoring tool.

**Work Package 4: Hardware-Attested Cryptographic Audit Trail (€11,200 - 160 hours)**
- Implement batch Merkle-tree cryptographic commitments producing chained SHA-256/HMAC verification proofs.
- Standardize JSON-LD attestation export compliant with EU AI Act Article 15 and W3C Web of Things.
- Deliverable: Audit verification CLI and cryptographic proof conformance suite.

**Work Package 5: Packaging, CI/CD Testbed & Documentation (€8,400 - 120 hours)**
- Build automated multi-architecture CI test pipeline (x86_64, aarch64, riscv64).
- Package for Debian/Ubuntu, Alpine, Nix flake, and minimal Docker containers.
- Comprehensive developer documentation, interactive tutorials, and open API specifications.

---

### Section 5: Budget, Qualifications & Timeline

* **Estimated Cost:** **€70,000**
* **Estimated Hours:** **1,000 Hours** (1,000 hrs × €70/hr = €70,000)
* **Project Duration:** **10 Months**
* **Who is most qualified? (Max 300 words):** Abdullah TAY (Lead Systems Architect & Full Stack Software Engineer) with 10+ years engineering high-throughput backend systems, low-level Linux IPC, and open-source developer tooling. Author of the complete EdgeGuard-AI working prototype and test suite.
* **Applicant Handle:** `Abdullah TAY` (`abdullahtay`)
* **Profile Link:** https://github.com/abdullahtay
* **Role:** Maintainer
* **Country:** Turkey
