"""Validation and lightweight summaries for one-dimensional vibration signals."""
from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
from scipy.stats import kurtosis


@dataclass(frozen=True)
class SignalSummary:
    sample_count: int
    mean: float
    standard_deviation: float
    rms: float
    peak_to_peak: float
    crest_factor: float
    kurtosis: float

    def to_dict(self) -> dict[str, int | float]:
        return asdict(self)


def validate_signal(
    values: list[float] | np.ndarray,
    *,
    min_points: int = 256,
    max_points: int = 200_000,
) -> np.ndarray:
    """Convert input to a finite float32 vector and enforce size limits."""
    signal = np.asarray(values, dtype=np.float32)
    if signal.ndim != 1:
        raise ValueError("Signal must be one-dimensional.")
    if signal.size < min_points:
        raise ValueError(f"Signal must contain at least {min_points} samples.")
    if signal.size > max_points:
        raise ValueError(f"Signal exceeds the {max_points}-sample limit.")
    if not np.isfinite(signal).all():
        raise ValueError("Signal contains NaN or infinite values.")
    return signal


def segment_signal(
    signal: np.ndarray,
    *,
    window_size: int = 2048,
    stride: int = 1024,
    drop_incomplete: bool = True,
) -> np.ndarray:
    """Create overlapping windows without padding or modifying raw signal data."""
    data = np.asarray(signal, dtype=np.float32)
    if data.ndim != 1:
        raise ValueError("Signal must be one-dimensional.")
    if window_size <= 0 or stride <= 0:
        raise ValueError("window_size and stride must be positive.")
    if data.size < window_size:
        raise ValueError("Signal is shorter than one complete window.")

    starts = list(range(0, data.size - window_size + 1, stride))
    if not drop_incomplete and starts and starts[-1] + window_size < data.size:
        starts.append(data.size - window_size)
    return np.stack([data[start : start + window_size] for start in starts])


def summarize_signal(signal: np.ndarray) -> SignalSummary:
    """Calculate basic time-domain indicators; this is not a fault diagnosis."""
    data = np.asarray(signal, dtype=np.float64)
    if data.ndim != 1 or data.size < 2 or not np.isfinite(data).all():
        raise ValueError("A finite one-dimensional signal with at least 2 samples is required.")

    rms = float(np.sqrt(np.mean(np.square(data))))
    peak = float(np.max(np.abs(data)))
    crest = peak / rms if rms > 0 else 0.0
    kurt = float(kurtosis(data, fisher=False, bias=False)) if np.std(data) > 0 else 0.0
    return SignalSummary(
        sample_count=int(data.size),
        mean=float(np.mean(data)),
        standard_deviation=float(np.std(data)),
        rms=rms,
        peak_to_peak=float(np.ptp(data)),
        crest_factor=float(crest),
        kurtosis=kurt,
    )
