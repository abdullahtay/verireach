"""
libedgeguard (EdgeGuard-AI): Zero-Dependency C-ABI & Python Telemetry Verification,
Binary Quantization, POSIX IPC Protocol & Cryptographic Attestation Library.
"""

__version__ = "1.2.0"
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
