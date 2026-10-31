import unittest
from pathlib import Path
from verireach.callgraph import CallGraph, CallGraphBuilder


class TestCallGraph(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = Path(__file__).parent / "fixtures"
        self.app_dir = self.fixtures_dir / "vulnerable_app"

    def test_callgraph_construction(self):
        builder = CallGraphBuilder(base_dir=self.app_dir)
        graph = builder.build_from_directory(self.app_dir, entrypoint_file="main.py")

        self.assertTrue(len(graph.nodes) > 0)
        self.assertTrue(len(graph.entrypoints) > 0)

    def test_symbol_reachability_positive(self):
        """verify_token_weak is called in main.py -> process_request -> verify_token_weak."""
        builder = CallGraphBuilder(base_dir=self.app_dir)
        graph = builder.build_from_directory(self.app_dir, entrypoint_file="main.py")

        res = graph.check_reachability("verify_token_weak")
        self.assertTrue(res.is_reachable)
        self.assertTrue(len(res.call_path) >= 2)
        self.assertIn("verify_token_weak", res.call_path[-1])

    def test_symbol_reachability_negative(self):
        """insecure_des_decrypt is defined in lib_crypto but NEVER called by main.py."""
        builder = CallGraphBuilder(base_dir=self.app_dir)
        graph = builder.build_from_directory(self.app_dir, entrypoint_file="main.py")

        res = graph.check_reachability("insecure_des_decrypt")
        self.assertFalse(res.is_reachable)
        self.assertEqual(len(res.call_path), 0)


if __name__ == "__main__":
    unittest.main()
