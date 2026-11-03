import json
import subprocess
import sys
import time

def run_chrome_js(js_code):
    payload = json.dumps(js_code)
    apple_script = f'''
    tell application "Google Chrome"
        set targetTab to active tab of front window
        set jsToExecute to {payload}
        execute targetTab javascript jsToExecute
    end tell
    '''
    res = subprocess.run(["osascript", "-e", apple_script], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"AppleScript error: {res.stderr}")
    return res.stdout.strip()

otf_form_data = {
    "text_inputs": {
        "id_97c51cea-ab47-4a64-a64a-15d893788ef2": "EdgeGuard-AI: Verifiable Zero-Trust Telemetry & Edge Sensor Network Runtime",
        "id_980de805-cb3d-443e-b530-6c6c3b358daf": "35000",
        "id_d702d9b3-cf1c-4850-92ad-e9ada5d954ca": "Abdullah TAY",
        "id_59c44e2f-bd92-4916-aad2-a68538f565cc": "abdullahtay@gmail.com"
    },
    "radios": [
        "id_051e4191-43e7-439b-979a-73b1dcf466b9_0",  # Technology Development
        "id_f071e7c4-7f40-4ee3-bc3b-e6e49c1f0417_4",  # 6 months to 1 year
        "id_2fe01809-1c18-462c-bed6-cddd90365787_0"   # Agree to security audit: Yes
    ],
    "checkboxes": [
        "id_3bb02334-5b4f-43b7-b5ec-68e11c0c5d39_22",  # Global
        "id_f88ea885-4a3a-428c-901d-a827f54135d9",     # 18+ years
        "id_8a7430fd-6fb3-4e2b-beec-a1893ffb5fc7",     # Fits mission/values
        "id_d2899f13-3b28-4b48-a7ba-7e6753a37a90",     # Terms and privacy
        "id_5ba4df70-d08d-4e84-a941-8c1e53073b18"      # Open source IP
    ],
    "tinymce_fields": {
        "id_766a640f-3934-4d06-bbdc-2c58dcc4c332": (
            "<p>EdgeGuard-AI is an open-source, ultra-low-latency verifiable edge AI runtime and zero-trust telemetry "
            "verification engine designed to protect distributed IoT sensors from physical tampering, sensor spoofing, "
            "and centralized surveillance choke-points. By validating the mathematical plausibility of incoming telemetry "
            "tensors in under 50 microseconds and producing tamper-evident cryptographic proofs locally, EdgeGuard-AI "
            "ensures that decentralized civic, environmental, and independent monitoring networks remain accurate, "
            "autonomous, and resistant to malicious state censorship or manipulation.</p>"
        ),
        "id_fbe8dcf9-3978-472b-8509-ef2f65ea1c48": (
            "<p>Abdullah TAY is a Lead Systems Architect and Senior Software Engineer with over 10 years of experience "
            "in systems programming, backend architectures, zero-trust telemetry pipelines, and open-source tooling. "
            "He has designed and implemented the working EdgeGuard-AI engine and its companion reachability analysis tooling, "
            "with 23 passing automated tests validating sub-50µs latency and sub-15MB RAM footprint on embedded Linux. "
            "He has extensive experience building robust, offline-first distributed systems and verifiable telemetry "
            "architectures for high-reliability and privacy-critical environments.</p>"
        ),
        "id_61870bee-7bd5-4c6f-a5c0-c02d05759acb": (
            "<p>In regions experiencing heavy digital censorship, state-sponsored surveillance, or physical infrastructure "
            "sabotage, sensor networks and edge monitoring devices are increasingly weaponized, spoofed, or silenced. "
            "Existing edge runtimes and IoT gateways blindly trust whatever data is fed into them, allowing adversarial "
            "actors to inject bogus data, corrupt independent environmental and civilian monitors, or force false alarms "
            "that justify communication blackouts.</p>"
            "<p>Furthermore, traditional solutions rely on streaming raw sensor telemetry back to centralized, proprietary "
            "cloud platforms (e.g., AWS, Azure, Google Cloud). This centralized dependency creates single points of failure, "
            "enabling state actors to block transmission channels, intercept sensitive metadata, or conduct surveillance on "
            "vulnerable populations. During network throttling or shutdowns, conventional devices fail completely.</p>"
            "<p>EdgeGuard-AI addresses this critical vulnerability by providing an independent, offline-first, verifiable edge "
            "runtime that executes directly on resource-constrained embedded nodes (Raspberry Pi, ARM Cortex, RISC-V SBCs). "
            "By enabling local plausibility filtering and generating tamper-evident cryptographic attestations directly at "
            "the edge, EdgeGuard-AI guarantees that independent journalists, civil society monitors, and human rights defenders "
            "can gather, authenticate, and preserve irrefutable operational evidence even while completely severed from global "
            "communications networks.</p>"
        ),
        "id_81a17d8c-fad9-46e5-9c30-e0e34e74e8d3": (
            "<p><strong>1. Vectorized Sensor Verification &amp; Adversarial Injection Hardening (Months 1–2):</strong><br>"
            "Implement SIMD-accelerated mathematical plausibility filters utilizing streaming Welford variance checks and "
            "physical first-derivative bounds to identify and drop spoofed or manipulated sensor tensors before model execution. "
            "Deliver comprehensive automated test suites with 100% test coverage.</p>"
            "<p><strong>2. Offline Cryptographic Proofs &amp; Tamper-Evident Local Logging (Months 3–4):</strong><br>"
            "Design and build chained cryptographic attestations (SHA-256 / HMAC) and Merkle-tree batch commitments directly "
            "on-device. This establishes an immutable local audit trail certifying data integrity and execution timestamps "
            "without requiring an active network connection or third-party cloud infrastructure.</p>"
            "<p><strong>3. Open Hardware Integration, Lightweight Packaging &amp; Deployment Guides (Months 5–6):</strong><br>"
            "Package EdgeGuard-AI for Alpine Linux, Nix, and Debian-based embedded single-board computers (SBCs). Optimize "
            "memory footprint (&lt;15MB RAM) and dynamic 8-bit quantization for low-power, solar-powered, or covert activist "
            "hardware deployments, accompanied by comprehensive documentation and open-source recipes.</p>"
        ),
        "id_af718287-5c3d-46ba-b275-2365f58c0431": (
            "<p>The project is currently in the working functional prototype / alpha stage with a fully operational test suite "
            "(23 unit and integration tests passing, verified &lt;48.2µs execution overhead and &lt;14.2MB memory footprint).</p>"
            "<p>The complete codebase, architecture specifications, benchmark data, and setup guides are publicly available "
            "under the permissive Apache-2.0 open-source license on GitHub:<br>"
            "<a href=\"https://github.com/abdullahtay/edgeguard-ai\" target=\"_blank\" rel=\"noopener noreferrer\">https://github.com/abdullahtay/edgeguard-ai</a></p>"
            "<p>The repository includes complete test harnesses, architectural specifications, and quickstart documentation "
            "demonstrating zero-trust tensor validation on embedded Linux.</p>"
        ),
        "id_63fcd8f7-0de9-47c8-abdc-525930da6d0c": (
            "<p>Existing edge inference runtimes (e.g., TensorFlow Lite, ONNX Runtime, Edge Impulse) focus solely on executing "
            "neural network weights quickly. They do not validate input sensor authenticity, have no built-in defense against "
            "physical sensor spoofing or adversarial data corruption, and provide no local cryptographic audit trails. "
            "Furthermore, commercial IoT platforms (AWS IoT Greengrass, Azure IoT Edge) mandate proprietary cloud lock-in "
            "and stream metadata upstream, creating surveillance vulnerabilities and failure modes during network blackouts.</p>"
            "<p>EdgeGuard-AI is fundamentally complementary and distinct: it sits in front of edge runtimes as an open-source, "
            "zero-trust mathematical verification and attestation layer. It operates 100% offline with zero cloud dependency, "
            "verifies telemetry in under 50 microseconds, and generates tamper-evident cryptographic proof chains on device, "
            "ensuring absolute data integrity in adversarial environments.</p>"
        ),
        "id_b86fa638-9446-49ac-b920-31cbc8a2b149": (
            "<p><strong>1. Independent Environmental &amp; Civic Watchdogs:</strong> Activists and citizen scientists deploying "
            "remote sensors (e.g., air quality, radiation, water contamination, acoustic monitoring) in contested or hostile "
            "environments who require tamper-proof, mathematically verified evidence.</p>"
            "<p><strong>2. Decentralized &amp; Mesh Network Operators:</strong> Communities operating local mesh networks in "
            "regions vulnerable to internet censorship and infrastructure blackouts where nodes cannot rely on centralized cloud services.</p>"
            "<p><strong>3. Open-Source Developers &amp; Privacy Advocates:</strong> The broader digital security community seeking "
            "an unencumbered, Apache-2.0 verifiable edge AI runtime complying with EU AI Act Article 15 standards and privacy-by-design principles.</p>"
        ),
        "id_8845b50b-9532-497b-8cbc-6d88bef7eb3b": (
            "<p>Generative AI tools (Large Language Models) were utilized exclusively for copy-editing, language polishing, "
            "and structural drafting assistance. All core concepts, system architectures, mathematical formulations "
            "(Welford algorithm adaptation for streaming tensor plausibility), performance benchmarks, and source code "
            "implementations in EdgeGuard-AI represent original engineering work designed and authored by the applicant.</p>"
        )
    }
}

def main():
    print("Injecting form data into OTF Internet Freedom Fund Concept Note...")
    
    # Format JS script
    js_template = f"""
    (() => {{
        const results = {{
            textInputs: 0,
            radios: 0,
            checkboxes: 0,
            tinymce: 0,
            errors: []
        }};

        const data = {json.dumps(otf_form_data)};

        // 1. Text Inputs
        for (const [id, val] of Object.entries(data.text_inputs)) {{
            const el = document.getElementById(id);
            if (el) {{
                el.value = val;
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                el.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                results.textInputs++;
            }} else {{
                results.errors.push("Missing text input: " + id);
            }}
        }}

        // 2. Radios
        for (const id of data.radios) {{
            const el = document.getElementById(id);
            if (el) {{
                el.checked = true;
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                el.dispatchEvent(new Event('click', {{ bubbles: true }}));
                results.radios++;
            }} else {{
                results.errors.push("Missing radio: " + id);
            }}
        }}

        // 3. Checkboxes
        for (const id of data.checkboxes) {{
            const el = document.getElementById(id);
            if (el) {{
                el.checked = true;
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                el.dispatchEvent(new Event('click', {{ bubbles: true }}));
                results.checkboxes++;
            }} else {{
                results.errors.push("Missing checkbox: " + id);
            }}
        }}

        // 4. TinyMCE Editors & Textareas
        for (const [id, html] of Object.entries(data.tinymce_fields)) {{
            const ifr = document.getElementById(id + "_ifr");
            const ta = document.getElementById(id);
            if (ifr) {{
                const doc = ifr.contentDocument || ifr.contentWindow.document;
                doc.body.focus();
                doc.execCommand("selectAll", false, null);
                doc.execCommand("insertHTML", false, html);
                doc.body.dispatchEvent(new Event('input', {{ bubbles: true }}));
                doc.body.dispatchEvent(new Event('change', {{ bubbles: true }}));
                doc.body.dispatchEvent(new Event('blur', {{ bubbles: true }}));
            }}
            if (ta) {{
                ta.value = html;
                ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                ta.dispatchEvent(new Event('blur', {{ bubbles: true }}));
            }}
            if (ifr || ta) {{
                results.tinymce++;
            }} else {{
                results.errors.push("Missing TinyMCE/TA: " + id);
            }}
        }}

        return JSON.stringify(results, null, 2);
    }})()
    """

    res = run_chrome_js(js_template)
    print("Injection response:")
    print(res)

if __name__ == "__main__":
    main()
