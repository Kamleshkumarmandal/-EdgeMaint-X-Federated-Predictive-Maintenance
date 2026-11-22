import numpy as np
import pytest

from federated.clients.partition import make_client_partitions


def test_iid_partitions_cover_each_sample_once():
    labels = np.arange(101) % 3
    partitions = make_client_partitions(labels, 4, mode="iid", seed=9)
    combined = np.concatenate(partitions)
    assert len(combined) == len(labels)
    assert set(combined.tolist()) == set(range(len(labels)))


def test_dirichlet_partitions_are_reproducible():
    labels = np.repeat(np.arange(3), 30)
    first = make_client_partitions(labels, 3, mode="dirichlet", alpha=0.3, seed=11)
    second = make_client_partitions(labels, 3, mode="dirichlet", alpha=0.3, seed=11)
    for left, right in zip(first, second, strict=True):
        assert np.array_equal(left, right)


def test_partition_validation():
    with pytest.raises(ValueError):
        make_client_partitions(np.asarray([]), 3)
    with pytest.raises(ValueError):
        make_client_partitions(np.arange(5), 1)
