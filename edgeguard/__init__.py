"""
EdgeGuard-AI: Verifiable Low-Latency Edge AI Runtime & Zero-Trust Anomaly Verification.
Open-source research prototype designed for Horizon Europe Cloud-Edge-IoT FSTP calls.
"""

__version__ = "0.1.0"
__author__ = "Abdullah TAY"
__license__ = "Apache-2.0"

from .verifier import SensorVerifier, VerificationResult
from .runtime import EdgeRuntime, InferenceTask
from .quantizer import TensorQuantizer
from .broker import LocalEdgeBroker

__all__ = [
    "SensorVerifier",
    "VerificationResult",
    "EdgeRuntime",
    "InferenceTask",
    "TensorQuantizer",
    "LocalEdgeBroker",
]
