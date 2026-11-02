import unittest
import time
from edgeguard.verifier import SensorVerifier, VerificationResult
from edgeguard.quantizer import TensorQuantizer
from edgeguard.broker import LocalEdgeBroker
from edgeguard.runtime import EdgeRuntime, InferenceTask


class TestEdgeGuardVerifier(unittest.TestCase):
    def setUp(self):
        self.verifier = SensorVerifier(feature_dim=4, z_threshold=3.0, max_rate_of_change=10.0)
        # Calibrate around mean=[1.0, 2.0, 3.0, 4.0] with small std
        baseline = [
            [1.0 + (i * 0.01), 2.0 + (i * 0.01), 3.0 + (i * 0.01), 4.0 + (i * 0.01)]
            for i in range(50)
        ]
        self.verifier.calibrate(baseline)

    def test_normal_vector_verification(self):
        sample = [1.02, 2.01, 3.03, 4.01]
        res = self.verifier.verify(sample)
        self.assertTrue(res.is_valid)
        self.assertLess(res.anomaly_score, 1.0)
        self.assertIsNotNone(res.attestation_hash)
        self.assertGreater(res.latency_us, 0.0)

    def test_ood_anomaly_rejection(self):
        # Far outlier
        sample = [50.0, 2.0, 3.0, 4.0]
        res = self.verifier.verify(sample)
        self.assertFalse(res.is_valid)
        self.assertGreater(res.anomaly_score, 1.0)
        self.assertIn("OOD anomaly detected", res.rejection_reason)

    def test_dimension_mismatch(self):
        sample = [1.0, 2.0]
        res = self.verifier.verify(sample)
        self.assertFalse(res.is_valid)
        self.assertIn("dimension mismatch", res.rejection_reason)


class TestTensorQuantizer(unittest.TestCase):
    def test_quantization_roundtrip(self):
        original = [0.12, -0.45, 0.88, 0.01, -0.99]
        quantized, scale = TensorQuantizer.quantize_int8(original)
        self.assertEqual(len(quantized), len(original))
        self.assertTrue(all(-128 <= q <= 127 for q in quantized))

        reconstructed = TensorQuantizer.dequantize_int8(quantized, scale)
        metrics = TensorQuantizer.compute_fidelity_metrics(original, reconstructed)
        self.assertLess(metrics["mae"], 0.02)
        self.assertGreater(metrics["cosine_similarity"], 0.999)


class TestLocalEdgeBroker(unittest.TestCase):
    def test_pub_sub_dispatch(self):
        broker = LocalEdgeBroker(max_queue_size=100)
        received = []

        def on_event(topic, payload):
            received.append((topic, payload))

        broker.subscribe("sensor/anomaly", on_event)
        broker.start()

        broker.publish("sensor/anomaly", {"device_id": "rpi4-01", "score": 4.2}, priority=1)
        time.sleep(0.15)
        broker.stop()

        self.assertEqual(len(received), 1)
        self.assertEqual(received[0][0], "sensor/anomaly")
        self.assertEqual(received[0][1]["device_id"], "rpi4-01")


class TestEdgeRuntime(unittest.TestCase):
    def test_runtime_pipeline(self):
        verifier = SensorVerifier(feature_dim=2, z_threshold=3.0)
        verifier.calibrate([[1.0, 1.0], [1.1, 0.9], [0.9, 1.1]])

        runtime = EdgeRuntime(verifier=verifier, enable_quantization=True)
        runtime.register_model("dummy", lambda x: [x[0] + x[1]])

        # 1. Valid execution
        task_ok = InferenceTask(task_id="t1", model_name="dummy", input_data=[1.0, 1.0])
        res_ok = runtime.execute(task_ok)
        self.assertEqual(res_ok.status, "EXECUTED")
        self.assertAlmostEqual(res_ok.prediction[0], 2.0, places=1)
        self.assertGreater(res_ok.execution_time_ms, 0.0)

        # 2. Rejected execution
        task_bad = InferenceTask(task_id="t2", model_name="dummy", input_data=[99.0, 99.0])
        res_bad = runtime.execute(task_bad)
        self.assertEqual(res_bad.status, "REJECTED")
        self.assertIsNone(res_bad.prediction)


if __name__ == "__main__":
    unittest.main()
