"""Time- and frequency-domain features for vibration windows."""
from __future__ import annotations

import numpy as np
from scipy.stats import kurtosis, skew


FEATURE_NAMES = (
    "mean", "std", "rms", "peak_to_peak", "crest_factor",
    "skewness", "kurtosis", "dominant_frequency_hz",
    "spectral_centroid_hz", "spectral_entropy",
)


def extract_features(window: np.ndarray, sample_rate_hz: float) -> dict[str, float]:
    """Extract deterministic signal features from a single finite 1-D window."""
    signal = np.asarray(window, dtype=np.float64)
    if signal.ndim != 1 or signal.size < 8:
        raise ValueError("window must be one-dimensional with at least 8 samples.")
    if not np.isfinite(signal).all():
        raise ValueError("window contains NaN or infinite values.")
    if sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be positive.")

    centered = signal - np.mean(signal)
    rms = float(np.sqrt(np.mean(np.square(signal))))
    peak = float(np.max(np.abs(signal)))
    spectrum = np.abs(np.fft.rfft(centered))
    frequencies = np.fft.rfftfreq(signal.size, d=1.0 / sample_rate_hz)
    power = np.square(spectrum)
    power_total = float(power.sum())
    if power_total > 0:
        probabilities = power / power_total
        dominant_frequency = float(frequencies[int(np.argmax(power))])
        centroid = float(np.sum(frequencies * power) / power_total)
        nonzero = probabilities[probabilities > 0]
        entropy = float(-np.sum(nonzero * np.log2(nonzero)))
    else:
        dominant_frequency = 0.0
        centroid = 0.0
        entropy = 0.0

    return {
        "mean": float(np.mean(signal)),
        "std": float(np.std(signal)),
        "rms": rms,
        "peak_to_peak": float(np.ptp(signal)),
        "crest_factor": peak / rms if rms else 0.0,
        "skewness": float(skew(signal, bias=False)) if np.std(signal) else 0.0,
        "kurtosis": float(kurtosis(signal, fisher=False, bias=False)) if np.std(signal) else 0.0,
        "dominant_frequency_hz": dominant_frequency,
        "spectral_centroid_hz": centroid,
        "spectral_entropy": entropy,
    }


def extract_feature_matrix(windows: np.ndarray, sample_rate_hz: float) -> tuple[np.ndarray, list[str]]:
    """Convert a [window, sample] array to a dense feature matrix."""
    data = np.asarray(windows, dtype=np.float32)
    if data.ndim != 2 or data.shape[0] == 0:
        raise ValueError("windows must be a non-empty 2-D array.")
    rows = [extract_features(row, sample_rate_hz) for row in data]
    names = list(rows[0])
    matrix = np.asarray([[row[name] for name in names] for row in rows], dtype=np.float32)
    return matrix, names
