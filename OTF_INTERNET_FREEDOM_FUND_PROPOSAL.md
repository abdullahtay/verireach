# Open Technology Fund (OTF) — Internet Freedom Fund
## Stage 1: Concept Note

**Portal:** https://apply.opentech.fund  
**Program:** Internet Freedom Fund (Rolling Application)  
**Primary Applicant:** Abdullah TAY (`abdullahtay@gmail.com` | `+90 532 206 61 68`)  
**Applicant Type:** Individual Software Engineer / Open Source Technologist  
**Project Name:** EdgeGuard-AI: Verifiable Zero-Trust Telemetry & Edge Sensor Network Runtime  
**Project Repository:** https://github.com/abdullahtay/edgeguard-ai  
**Requested Amount:** **$35,000 USD**  
**Project Duration:** 6 Months  

---

### 1. Project Summary (Elevator Pitch)
EdgeGuard-AI is an open-source, ultra-low-latency verifiable edge AI runtime and zero-trust telemetry verification engine designed to protect distributed IoT sensors and edge monitoring devices from physical tampering, deliberate data corruption, sensor spoofing, and centralized surveillance choke-points. By validating the mathematical plausibility of incoming telemetry tensors in under 50 microseconds and producing tamper-evident cryptographic proofs (SHA-256 / HMAC) locally on device, EdgeGuard-AI ensures that critical decentralized sensor networks (environmental monitoring, civilian reporting, independent telemetry) remain accurate, autonomous, and resistant to malicious state or adversarial manipulation.

---

### 2. Problem Statement & Threat Model
In regions experiencing heavy digital censorship, state-sponsored surveillance, or physical infrastructure sabotage, sensor networks and edge IoT devices are increasingly weaponized or silenced. Existing edge runtimes and IoT gateways blindly trust whatever data is fed into them, allowing adversarial actors to inject bogus data, corrupt independent environmental/civilian monitors, or force false alarms that justify internet and communication blackouts.

Furthermore, traditional solutions rely on streaming raw sensor telemetry back to centralized, proprietary cloud platforms (e.g., AWS, Azure, Google Cloud). This centralized dependency creates:
1. Single points of censorship and surveillance interception.
2. Inability to operate during communication throttling or shutdown events.
3. Vulnerability to upstream metadata harvesting.

---

### 3. Proposed Solution & Technical Approach
EdgeGuard-AI provides an independent, sovereign, and verifiable edge runtime executing directly on resource-constrained embedded nodes (Raspberry Pi, ARM Cortex, RISC-V SBCs):

1. **Sub-50µs Zero-Trust Plausibility Engine:** Applies streaming mathematical variance checks (Welford's algorithm) and physical first-derivative bounds to sensor tensors, filtering out injected anomalies and electromagnetic noise before any model executes.
2. **Dynamic 8-Bit Quantization (<15MB RAM):** Compresses tensor memory footprints by 75% with zero external heavy dependencies, ensuring the runtime functions on ultra-low-power, solar-powered, or covert hardware.
3. **Decentralized Cryptographic Inference Proofs:** Generates chained cryptographic attestations (SHA-256 / HMAC) certifying data integrity and execution timestamps on device, creating an immutable local audit trail that proves data authenticity even when completely disconnected from the internet.
4. **Autonomous Local Operation:** High-throughput Unix domain socket priority broker (>20,000 verified dispatches/sec) guarantees offline-first operational continuity during network blackouts.

---

### 4. Target Beneficiaries & Impact on Internet Freedom
* **Independent Environmental & Civic Watchdogs:** Activists and citizen scientists deploying remote sensors (e.g., radiation, water quality, acoustic monitoring) in contested or hostile environments who require tamper-proof, verifiable evidence.
* **Decentralized & Mesh Network Operators:** Communities running mesh IoT infrastructure where nodes cannot rely on centralized cloud services.
* **Open Source Developers & Privacy Advocates:** Access to an unencumbered Apache-2.0 verifiable edge runtime enforcing EU AI Act Article 15 standards and zero-trust privacy.

---

### 5. Work Plan & Milestone Deliverables

* **Milestone 1 (Months 1–2 / $12,000):** Vectorized Sensor Verification & Adversarial Injection Hardening. Development of SIMD-accelerated mathematical plausibility filters with 100% test coverage.
* **Milestone 2 (Months 3–4 / $13,000):** Offline Cryptographic Proofs & Tamper-Evident Local Logging. Implementation of batch Merkle-tree cryptographic commitments for telemetry certification without cloud reliance.
* **Milestone 3 (Months 5–6 / $10,000):** Open Hardware Integration, Nix/Alpine Packaging & Deployment Guides for Activist/Civilian Hardware.

---

### 6. Applicant Background & Qualifications
Abdullah TAY is a Lead Systems Architect and Senior Software Engineer with over 10 years of experience in systems programming, backend architectures, and open-source tooling. He has already conceptualized, implemented, and benchmarked the functional EdgeGuard-AI prototype (23 passing tests, confirmed <48.2µs latency overhead, resident memory <14.2MB RAM). He possesses full technical independence to deliver all milestones.
