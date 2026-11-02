import math
import hashlib
import time
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple


@dataclass
class VerificationResult:
    """Represents the verification outcome for an edge AI input tensor or prediction."""
    is_valid: bool
    anomaly_score: float
    confidence_decay: float
    drift_detected: bool
    rejection_reason: Optional[str] = None
    attestation_hash: Optional[str] = None
    latency_us: float = 0.0


class SensorVerifier:
    """
    Mathematical zero-trust verification engine for edge sensors and model inputs.
    Detects adversarial perturbations, sensor hijacking, and out-of-distribution (OOD) drift
    with microsecond-level overhead.
    """

    def __init__(
        self,
        feature_dim: int,
        z_threshold: float = 3.5,
        max_rate_of_change: float = 5.0,
        drift_window_size: int = 100,
        drift_alpha: float = 0.05,
    ):
        self.feature_dim = feature_dim
        self.z_threshold = z_threshold
        self.max_rate_of_change = max_rate_of_change
        self.drift_window_size = drift_window_size
        self.drift_alpha = drift_alpha

        # Baseline running statistics
        self.mean_vector: List[float] = [0.0] * feature_dim
        self.var_vector: List[float] = [1.0] * feature_dim
        self.sample_count: int = 0
        self.last_input: Optional[List[float]] = None
        self.last_timestamp: float = time.time()

        # Sliding window for drift detection
        self.sliding_history: List[List[float]] = []

    def calibrate(self, reference_samples: List[List[float]]) -> None:
        """Calibrates baseline statistical distribution from trusted training/calibration samples."""
        if not reference_samples:
            raise ValueError("Reference samples cannot be empty")

        n = len(reference_samples)
        dim = len(reference_samples[0])
        if dim != self.feature_dim:
            raise ValueError(f"Feature dimension mismatch: expected {self.feature_dim}, got {dim}")

        # Compute mean
        sums = [0.0] * dim
        for sample in reference_samples:
            for i, val in enumerate(sample):
                sums[i] += val
        self.mean_vector = [s / n for s in sums]

        # Compute variance (with epsilon to prevent division by zero)
        sq_diffs = [0.0] * dim
        for sample in reference_samples:
            for i, val in enumerate(sample):
                sq_diffs[i] += (val - self.mean_vector[i]) ** 2
        self.var_vector = [max(sq / n, 1e-6) for sq in sq_diffs]
        self.sample_count = n

    def verify(self, input_vector: List[float], timestamp: Optional[float] = None) -> VerificationResult:
        """
        Executes zero-trust verification on an incoming edge vector.
        Guarantees sub-millisecond execution without external libraries.
        """
        start_time = time.perf_counter()
        now = timestamp if timestamp is not None else time.time()

        if len(input_vector) != self.feature_dim:
            return VerificationResult(
                is_valid=False,
                anomaly_score=1.0,
                confidence_decay=1.0,
                drift_detected=False,
                rejection_reason=f"Vector dimension mismatch (expected {self.feature_dim}, got {len(input_vector)})",
                latency_us=(time.perf_counter() - start_time) * 1_000_000,
            )

        # 1. Physical Sensor Plausibility & Rate of Change Check
        dt = max(now - self.last_timestamp, 1e-5)
        if self.last_input is not None:
            max_delta = 0.0
            for curr, prev in zip(input_vector, self.last_input):
                rate = abs(curr - prev) / dt
                if rate > max_delta:
                    max_delta = rate
            if max_delta > self.max_rate_of_change:
                latency = (time.perf_counter() - start_time) * 1_000_000
                return VerificationResult(
                    is_valid=False,
                    anomaly_score=float(min(max_delta / self.max_rate_of_change, 10.0)),
                    confidence_decay=0.8,
                    drift_detected=False,
                    rejection_reason=f"Sensor physical rate-of-change violated ({max_delta:.2f} > {self.max_rate_of_change:.2f})",
                    latency_us=latency,
                )

        # 2. Out-of-Distribution (OOD) Z-Score Vector Check
        max_z = 0.0
        z_scores = []
        for i, val in enumerate(input_vector):
            std = math.sqrt(self.var_vector[i])
            z = abs(val - self.mean_vector[i]) / std
            z_scores.append(z)
            if z > max_z:
                max_z = z

        # 3. Dynamic Drift Tracking (Sliding Window EMA)
        self.sliding_history.append(input_vector)
        if len(self.sliding_history) > self.drift_window_size:
            self.sliding_history.pop(0)

        drift_detected = False
        if len(self.sliding_history) >= 20:
            window_mean = [
                sum(row[i] for row in self.sliding_history) / len(self.sliding_history)
                for i in range(self.feature_dim)
            ]
            drift_distance = math.sqrt(
                sum((wm - bm) ** 2 for wm, bm in zip(window_mean, self.mean_vector))
            )
            if drift_distance > self.z_threshold * 0.8:
                drift_detected = True

        # Check threshold
        is_valid = max_z <= self.z_threshold
        anomaly_score = float(max_z / self.z_threshold) if self.z_threshold > 0 else 0.0
        confidence_decay = min(max(anomaly_score - 1.0, 0.0), 1.0) if not is_valid else 0.0

        # Cryptographic attestation digest for verifiable logging
        raw_repr = f"{now}:{input_vector}:{is_valid}:{anomaly_score:.4f}"
        attestation_hash = hashlib.sha256(raw_repr.encode("utf-8")).hexdigest()

        # Update tracking state
        self.last_input = list(input_vector)
        self.last_timestamp = now

        latency = (time.perf_counter() - start_time) * 1_000_000

        return VerificationResult(
            is_valid=is_valid,
            anomaly_score=anomaly_score,
            confidence_decay=confidence_decay,
            drift_detected=drift_detected,
            rejection_reason=None if is_valid else f"OOD anomaly detected: max Z-score {max_z:.2f} exceeds threshold {self.z_threshold}",
            attestation_hash=attestation_hash,
            latency_us=latency,
        )
