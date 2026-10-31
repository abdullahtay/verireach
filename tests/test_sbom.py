import json
import unittest
from pathlib import Path
from verireach.sbom import SBOMParser


class TestSBOMParser(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = Path(__file__).parent / "fixtures"
        self.sample_sbom = self.fixtures_dir / "sample_sbom.json"

    def test_parse_cyclonedx_file(self):
        components = SBOMParser.parse_file(self.sample_sbom)
        self.assertEqual(len(components), 4)  # 1 root + 3 library components

        names = [c.name for c in components]
        self.assertIn("fast-crypto", names)
        self.assertIn("jwt-auth-helper", names)
        self.assertIn("logging-utils", names)

        # Check PURL extraction
        crypto = next(c for c in components if c.name == "fast-crypto")
        self.assertIsNotNone(crypto.purl)
        self.assertEqual(crypto.purl.name, "fast-crypto")
        self.assertEqual(crypto.purl.version, "1.2.0")

    def test_parse_spdx_dict(self):
        spdx_data = {
            "spdxVersion": "SPDX-2.3",
            "packages": [
                {
                    "name": "urllib3",
                    "versionInfo": "1.26.5",
                    "externalRefs": [
                        {
                            "referenceType": "purl",
                            "referenceLocator": "pkg:pypi/urllib3@1.26.5"
                        }
                    ]
                }
            ]
        }
        components = SBOMParser.parse_json(spdx_data)
        self.assertEqual(len(components), 1)
        self.assertEqual(components[0].name, "urllib3")
        self.assertIsNotNone(components[0].purl)
        self.assertEqual(components[0].purl.type, "pypi")


if __name__ == "__main__":
    unittest.main()
