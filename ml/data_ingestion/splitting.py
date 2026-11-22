"""Leakage-aware splitting helpers for vibration windows."""
from __future__ import annotations

import numpy as np
from sklearn.model_selection import GroupShuffleSplit


def split_by_recording(
    features: np.ndarray,
    labels: np.ndarray,
    recording_ids: np.ndarray,
    *,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Return row indices split by source recording, never by individual windows."""
    x = np.asarray(features)
    y = np.asarray(labels)
    groups = np.asarray(recording_ids)
    if x.shape[0] != y.shape[0] or y.shape[0] != groups.shape[0]:
        raise ValueError("features, labels, and recording_ids must have equal row counts.")
    if x.shape[0] < 2:
        raise ValueError("At least two window records are required.")
    if not 0 < test_size < 1:
        raise ValueError("test_size must be strictly between 0 and 1.")
    if np.unique(groups).size < 2:
        raise ValueError("At least two distinct source recordings are required.")

    splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
    train_indices, test_indices = next(splitter.split(x, y, groups))
    if set(groups[train_indices]).intersection(set(groups[test_indices])):
        raise RuntimeError("Recording leakage detected across the split.")
    return train_indices, test_indices
