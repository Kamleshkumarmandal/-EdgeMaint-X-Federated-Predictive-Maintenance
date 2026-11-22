"""Leakage-aware splitting helpers for vibration windows."""
from __future__ import annotations

import numpy as np


def split_by_recording(
    features: np.ndarray,
    labels: np.ndarray,
    recording_ids: np.ndarray,
    *,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Return row indices split by source recording, never by individual windows.

    This helper deliberately uses NumPy only, so dataset preparation and its
    tests do not require the optional scikit-learn training dependencies.
    """
    x = np.asarray(features)
    y = np.asarray(labels)
    groups = np.asarray(recording_ids)
    if x.shape[0] != y.shape[0] or y.shape[0] != groups.shape[0]:
        raise ValueError("features, labels, and recording_ids must have equal row counts.")
    if x.shape[0] < 2:
        raise ValueError("At least two window records are required.")
    if not 0 < test_size < 1:
        raise ValueError("test_size must be strictly between 0 and 1.")

    unique_groups = np.unique(groups)
    if unique_groups.size < 2:
        raise ValueError("At least two distinct source recordings are required.")

    rng = np.random.default_rng(random_state)
    shuffled_groups = rng.permutation(unique_groups)
    target_test_rows = max(1, int(np.ceil(x.shape[0] * test_size)))
    selected_test_groups: list[object] = []
    selected_rows = 0

    # Leave at least one complete source recording for training.
    for group in shuffled_groups[:-1]:
        if selected_test_groups and selected_rows >= target_test_rows:
            break
        selected_test_groups.append(group)
        selected_rows += int(np.count_nonzero(groups == group))

    test_mask = np.isin(groups, np.asarray(selected_test_groups))
    train_indices = np.flatnonzero(~test_mask)
    test_indices = np.flatnonzero(test_mask)
    if train_indices.size == 0 or test_indices.size == 0:
        raise ValueError("Unable to create non-empty recording-level train and test splits.")
    if set(groups[train_indices]).intersection(set(groups[test_indices])):
        raise RuntimeError("Recording leakage detected across the split.")
    return train_indices, test_indices
