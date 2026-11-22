import numpy as np
import pytest

from ml.features.statistical import extract_feature_matrix, extract_features


def test_feature_extraction_returns_expected_keys():
    signal = np.sin(np.linspace(0, 2 * np.pi * 20, 1024))
    features = extract_features(signal, sample_rate_hz=12000)
    assert features["rms"] > 0
    assert features["dominant_frequency_hz"] > 0
    assert set(features) >= {"mean", "std", "rms", "kurtosis", "spectral_entropy"}


def test_feature_matrix_shape_and_names():
    windows = np.random.default_rng(7).normal(size=(4, 256)).astype(np.float32)
    matrix, names = extract_feature_matrix(windows, sample_rate_hz=12000)
    assert matrix.shape == (4, len(names))
    assert matrix.dtype == np.float32


def test_features_reject_invalid_input():
    with pytest.raises(ValueError):
        extract_features(np.asarray([1.0, 2.0]), 12000)
