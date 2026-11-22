import numpy as np
import pytest

from ml.preprocessing.signal import segment_signal, summarize_signal, validate_signal


def test_validate_signal_rejects_non_finite_values():
    with pytest.raises(ValueError, match="NaN or infinite"):
        validate_signal([0.0] * 255 + [float("nan")])


def test_segment_signal_produces_expected_overlapping_windows():
    values = np.arange(4096, dtype=np.float32)
    windows = segment_signal(values, window_size=1024, stride=512)
    assert windows.shape == (7, 1024)
    assert np.array_equal(windows[0], values[:1024])
    assert np.array_equal(windows[1], values[512:1536])


def test_signal_summary_has_finite_values():
    values = np.sin(np.linspace(0, 10 * np.pi, 2048))
    summary = summarize_signal(values)
    assert summary.sample_count == 2048
    assert summary.rms > 0
    assert summary.peak_to_peak > 1.9
    assert np.isfinite(summary.kurtosis)
