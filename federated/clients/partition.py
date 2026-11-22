"""Deterministic IID and Dirichlet non-IID partitions for virtual clients."""
from __future__ import annotations

import numpy as np


def make_client_partitions(
    labels: np.ndarray,
    num_clients: int,
    *,
    mode: str = "iid",
    alpha: float = 0.5,
    seed: int = 42,
) -> list[np.ndarray]:
    """Return row-index partitions while leaving the caller's samples untouched.

    Dirichlet mode allocates each class across clients using a Dirichlet draw,
    creating different label proportions across virtual industrial sites.
    """
    y = np.asarray(labels)
    if y.ndim != 1 or y.size == 0:
        raise ValueError("labels must be a non-empty one-dimensional array.")
    if num_clients < 2:
        raise ValueError("num_clients must be at least 2.")
    if mode not in {"iid", "dirichlet"}:
        raise ValueError("mode must be 'iid' or 'dirichlet'.")
    if alpha <= 0:
        raise ValueError("alpha must be positive.")

    rng = np.random.default_rng(seed)
    if mode == "iid":
        shuffled = rng.permutation(y.size)
        return [part.astype(np.int64) for part in np.array_split(shuffled, num_clients)]

    client_indices: list[list[int]] = [[] for _ in range(num_clients)]
    for label in np.unique(y):
        indices = np.flatnonzero(y == label)
        rng.shuffle(indices)
        proportions = rng.dirichlet(np.full(num_clients, alpha))
        boundaries = (np.cumsum(proportions)[:-1] * len(indices)).astype(int)
        chunks = np.split(indices, boundaries)
        for client, chunk in zip(client_indices, chunks, strict=True):
            client.extend(int(i) for i in chunk)

    result = []
    for indices in client_indices:
        rng.shuffle(indices)
        result.append(np.asarray(indices, dtype=np.int64))
    return result
