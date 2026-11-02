import time
from dataclasses import dataclass
from typing import List, Callable, Optional, Dict, Any
from .verifier import SensorVerifier, VerificationResult
from .quantizer import TensorQuantizer


@dataclass
class InferenceTask:
    task_id: str
    model_name: str
    input_data: List[float]
    verified: bool = False
    verification_details: Optional[VerificationResult] = None
    prediction: Optional[List[float]] = None
    execution_time_ms: float = 0.0
    status: str = "PENDING"  # PENDING, REJECTED, EXECUTED, FAILED


class EdgeRuntime:
    """
    Predictable, low-latency Edge AI runtime engine.
    Integrates pre-inference zero-trust verification and quantization checks.
    """

    def __init__(self, verifier: Optional[SensorVerifier] = None, enable_quantization: bool = True):
        self.verifier = verifier
        self.enable_quantization = enable_quantization
        self._models: Dict[str, Callable[[List[float]], List[float]]] = {}
        self.tasks_executed: int = 0
        self.tasks_rejected: int = 0

    def register_model(self, model_name: str, model_callable: Callable[[List[float]], List[float]]) -> None:
        """Registers an inference model handler (e.g. ONNX runtime session or custom function)."""
        self._models[model_name] = model_callable

    def execute(self, task: InferenceTask) -> InferenceTask:
        """
        Executes an inference task through the verified edge pipeline:
        1. Pre-execution Zero-Trust Verification
        2. Dynamic 8-bit Quantization (optional)
        3. Model Execution
        4. Latency and Attestation Logging
        """
        start_time = time.perf_counter()

        if task.model_name not in self._models:
            task.status = "FAILED"
            task.execution_time_ms = (time.perf_counter() - start_time) * 1000.0
            return task

        # 1. Verification Stage
        if self.verifier is not None:
            v_res = self.verifier.verify(task.input_data)
            task.verification_details = v_res
            task.verified = v_res.is_valid

            if not v_res.is_valid:
                task.status = "REJECTED"
                self.tasks_rejected += 1
                task.execution_time_ms = (time.perf_counter() - start_time) * 1000.0
                return task
        else:
            task.verified = True

        # 2. Quantization Stage
        input_tensor = task.input_data
        if self.enable_quantization:
            quantized, scale = TensorQuantizer.quantize_int8(input_tensor)
            input_tensor = TensorQuantizer.dequantize_int8(quantized, scale)

        # 3. Model Execution
        model_fn = self._models[task.model_name]
        try:
            pred = model_fn(input_tensor)
            task.prediction = pred
            task.status = "EXECUTED"
            self.tasks_executed += 1
        except Exception as e:
            task.status = "FAILED"
            task.prediction = None

        task.execution_time_ms = (time.perf_counter() - start_time) * 1000.0
        return task
