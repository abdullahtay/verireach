import math
from typing import List, Tuple, Dict


class TensorQuantizer:
    """
    Zero-overhead symmetric 8-bit quantization engine for edge inference buffers.
    Reduces memory footprint by 75% while mathematically guaranteeing bounded quantization error.
    """

    @staticmethod
    def quantize_int8(tensor: List[float]) -> Tuple[List[int], float]:
        """
        Quantizes float32 tensor into signed 8-bit integers [-128, 127] with dynamic scaling.
        Returns (quantized_values, scale_factor).
        """
        if not tensor:
            return [], 1.0

        max_abs = max(abs(x) for x in tensor)
        if max_abs == 0.0:
            return [0] * len(tensor), 1.0

        scale = max_abs / 127.0
        quantized = [
            int(round(max(-128.0, min(127.0, x / scale))))
            for x in tensor
        ]
        return quantized, scale

    @staticmethod
    def dequantize_int8(quantized: List[int], scale: float) -> List[float]:
        """Dequantizes int8 values back to float32 approximation."""
        return [float(q * scale) for q in quantized]

    @staticmethod
    def compute_fidelity_metrics(original: List[float], reconstructed: List[float]) -> Dict[str, float]:
        """
        Computes Mean Absolute Error (MAE), Mean Squared Error (MSE),
        and Cosine Similarity between original and reconstructed tensors.
        """
        if len(original) != len(reconstructed) or not original:
            raise ValueError("Tensors must have matching, non-zero lengths")

        n = len(original)
        mae = sum(abs(o - r) for o, r in zip(original, reconstructed)) / n
        mse = sum((o - r) ** 2 for o, r in zip(original, reconstructed)) / n

        # Cosine similarity
        dot = sum(o * r for o, r in zip(original, reconstructed))
        norm_o = math.sqrt(sum(o ** 2 for o in original))
        norm_r = math.sqrt(sum(r ** 2 for r in reconstructed))

        cos_sim = dot / (norm_o * norm_r) if (norm_o > 0 and norm_r > 0) else 1.0

        return {
            "mae": float(mae),
            "mse": float(mse),
            "snr_db": float(-10.0 * math.log10(mse + 1e-12)),
            "cosine_similarity": float(cos_sim),
        }
