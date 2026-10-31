import unittest
from pathlib import Path
from verireach.advisory import AdvisoryResolver, VulnerabilityAdvisory
from verireach.purl import PackageURL


class TestAdvisoryResolver(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = Path(__file__).parent / "fixtures"
        self.advisory_file = self.fixtures_dir / "mock_advisories.json"
        self.resolver = AdvisoryResolver(local_advisories_file=self.advisory_file)

    def test_load_and_query_advisories(self):
        purl = PackageURL.from_string("pkg:pypi/fast-crypto@1.2.0")
        matches = self.resolver.query_for_component(purl)
        self.assertEqual(len(matches), 1)
        adv = matches[0]
        self.assertEqual(adv.id, "CVE-2024-99001")
        self.assertIn("insecure_des_decrypt", adv.affected_symbols)

    def test_version_isolation(self):
        # Query patched version
        purl = PackageURL.from_string("pkg:pypi/fast-crypto@1.2.1")
        matches = self.resolver.query_for_component(purl)
        self.assertEqual(len(matches), 0)

    def test_prose_symbol_extraction(self):
        prose = "An issue was discovered in lib where `parse_jwt_header()` fails to validate `alg`."
        symbols = AdvisoryResolver._extract_symbols_from_prose(prose)
        self.assertIn("parse_jwt_header", symbols)


if __name__ == "__main__":
    unittest.main()
