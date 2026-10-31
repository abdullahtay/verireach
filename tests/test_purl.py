import unittest
from verireach.purl import PackageURL


class TestPackageURL(unittest.TestCase):
    def test_basic_purl_parsing(self):
        purl_str = "pkg:pypi/requests@2.28.1"
        p = PackageURL.from_string(purl_str)
        self.assertEqual(p.type, "pypi")
        self.assertIsNone(p.namespace)
        self.assertEqual(p.name, "requests")
        self.assertEqual(p.version, "2.28.1")
        self.assertEqual(p.to_string(), purl_str)

    def test_namespaced_purl(self):
        purl_str = "pkg:npm/@angular/core@12.3.1"
        p = PackageURL.from_string(purl_str)
        self.assertEqual(p.type, "npm")
        self.assertEqual(p.namespace, "@angular")
        self.assertEqual(p.name, "core")
        self.assertEqual(p.version, "12.3.1")
        self.assertIn("@angular", p.to_string())

    def test_purl_with_qualifiers_and_subpath(self):
        purl_str = "pkg:golang/google.golang.org/genproto@abcd123?vcs_url=git%3A//example.com#sub/dir"
        p = PackageURL.from_string(purl_str)
        self.assertEqual(p.type, "golang")
        self.assertEqual(p.subpath, "sub/dir")
        self.assertEqual(p.qualifiers.get("vcs_url"), "git://example.com")

    def test_purl_identity_matching(self):
        p1 = PackageURL.from_string("pkg:pypi/cryptography@3.4.8")
        p2 = PackageURL.from_string("pkg:pypi/cryptography@3.4.8")
        p3 = PackageURL.from_string("pkg:pypi/cryptography@4.0.0")
        p4 = PackageURL.from_string("pkg:npm/cryptography@3.4.8")

        self.assertTrue(p1.matches_identity(p2))
        self.assertFalse(p1.matches_identity(p3))
        self.assertTrue(p1.matches_identity(p3, ignore_version=True))
        self.assertFalse(p1.matches_identity(p4, ignore_version=True))

    def test_invalid_purls(self):
        with self.assertRaises(ValueError):
            PackageURL.from_string("")
        with self.assertRaises(ValueError):
            PackageURL.from_string("http://example.com")
        with self.assertRaises(ValueError):
            PackageURL.from_string("pkg:")


if __name__ == "__main__":
    unittest.main()
