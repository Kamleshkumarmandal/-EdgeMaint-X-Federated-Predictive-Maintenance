import numpy as np
import pytest
from scipy.io import savemat

from ml.data_ingestion.cwru import discover_mat_files, load_cwru_recording
from ml.data_ingestion.splitting import split_by_recording


def test_cwru_mat_loader_reads_drive_end_channel(tmp_path):
    file_path = tmp_path / "100.mat"
    expected = np.linspace(-1.0, 1.0, 1024, dtype=np.float32).reshape(-1, 1)
    savemat(file_path, {"X100_DE_time": expected, "X100_FE_time": expected / 2})
    record = load_cwru_recording(file_path, channel="DE", sample_rate_hz=12000)
    assert record.variable_name == "X100_DE_time"
    assert record.samples.shape == (1024,)
    assert record.sample_rate_hz == 12000
    assert discover_mat_files(tmp_path) == [file_path]


def test_split_keeps_source_recordings_separate():
    x = np.zeros((12, 4))
    y = np.asarray([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2])
    groups = np.repeat(["record-a", "record-b", "record-c"], 4)
    train, test = split_by_recording(x, y, groups, test_size=0.34)
    assert set(groups[train]).isdisjoint(set(groups[test]))


def test_split_rejects_single_recording():
    with pytest.raises(ValueError, match="two distinct"):
        split_by_recording(np.zeros((4, 2)), np.zeros(4), np.repeat("only", 4))
