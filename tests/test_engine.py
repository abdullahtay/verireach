import unittest
from pathlib import Path
from verireach.engine import VeriReachEngine


class TestVeriReachEngine(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = Path(__file__).parent / "fixtures"
        self.sbom_path = self.fixtures_dir / "sample_sbom.json"
        self.src_dir = self.fixtures_dir / "vulnerable_app"
        self.advisory_file = self.fixtures_dir / "mock_advisories.json"

    def test_end_to_end_triage(self):
        engine = VeriReachEngine(advisories_file=self.advisory_file)
        report = engine.run_scan(
            sbom_path=self.sbom_path,
            source_dir=self.src_dir,
            entrypoint="main.py",
        )

        m = report.metrics
        self.assertEqual(m.total_advisories, 2)
        self.assertEqual(m.reachable_affected, 1)
        self.assertEqual(m.unreachable_not_affected, 1)
        self.assertAlmostEqual(m.false_positive_reduction_rate, 50.0)

        # Check statement details
        statements = report.vex_document.statements
        self.assertEqual(len(statements), 2)

        # Find statements by vulnerability
        s_crypto = next(s for s in statements if s.vulnerability == "CVE-2024-99001")
        self.assertEqual(s_crypto.status, "not_affected")
        self.assertEqual(s_crypto.justification, "vulnerable_code_not_in_execute_path")

        s_jwt = next(s for s in statements if s.vulnerability == "CVE-2024-99002")
        self.assertEqual(s_jwt.status, "affected")


if __name__ == "__main__":
    unittest.main()
