import json
import unittest
from verireach.callgraph import ReachabilityResult
from verireach.purl import PackageURL
from verireach.vex import VEXGenerator, VEXStatement


class TestVEXGenerator(unittest.TestCase):
    def test_openvex_not_affected_statement(self):
        purl = PackageURL.from_string("pkg:pypi/fast-crypto@1.2.0")
        reach = ReachabilityResult(
            symbol="insecure_des_decrypt",
            is_reachable=False,
            entrypoint="main.py",
            notes="No execution path found.",
        )
        stmt = VEXGenerator.create_statement(purl, "CVE-2024-99001", reach)
        self.assertEqual(stmt.status, "not_affected")
        self.assertEqual(stmt.justification, "vulnerable_code_not_in_execute_path")

        doc = VEXGenerator.generate_document([stmt])
        d = doc.to_dict()
        self.assertEqual(d["@context"], "https://openvex.dev/ns/v0.2.0")
        self.assertEqual(len(d["statements"]), 1)
        self.assertEqual(d["statements"][0]["status"], "not_affected")

    def test_openvex_affected_statement(self):
        purl = PackageURL.from_string("pkg:pypi/jwt-auth-helper@2.4.1")
        reach = ReachabilityResult(
            symbol="verify_token_weak",
            is_reachable=True,
            entrypoint="main",
            call_path=["main", "process_request", "verify_token_weak"],
        )
        stmt = VEXGenerator.create_statement(purl, "CVE-2024-99002", reach)
        self.assertEqual(stmt.status, "affected")
        self.assertIn("verify_token_weak", stmt.action_statement)

    def test_cyclonedx_vex_export(self):
        purl = PackageURL.from_string("pkg:pypi/fast-crypto@1.2.0")
        reach = ReachabilityResult(
            symbol="insecure_des_decrypt",
            is_reachable=False,
            entrypoint="main.py",
        )
        stmt = VEXGenerator.create_statement(purl, "CVE-2024-99001", reach)
        doc = VEXGenerator.generate_document([stmt])
        cyclone = doc.to_cyclonedx_dict()

        self.assertEqual(cyclone["bomFormat"], "CycloneDX")
        self.assertEqual(len(cyclone["vulnerabilities"]), 1)
        vuln = cyclone["vulnerabilities"][0]
        self.assertEqual(vuln["id"], "CVE-2024-99001")
        self.assertEqual(vuln["analysis"]["state"], "not_affected")
        self.assertEqual(vuln["analysis"]["justification"], "code_not_reachable")


if __name__ == "__main__":
    unittest.main()
