"""Utilities for reading MATLAB bearing recordings from a local CWRU download."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.io import loadmat

from ml.preprocessing.signal import validate_signal


@dataclass(frozen=True)
class BearingRecording:
    path: str
    variable_name: str
    channel: str
    sample_rate_hz: float
    samples: np.ndarray


def discover_mat_files(root: str | Path) -> list[Path]:
    """Return sorted MATLAB files below root; never downloads data automatically."""
    directory = Path(root)
    if not directory.exists():
        raise FileNotFoundError(f"Dataset directory does not exist: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(str(directory))
    return sorted(path for path in directory.rglob("*.mat") if path.is_file())


def load_cwru_recording(
    path: str | Path,
    *,
    channel: str = "DE",
    sample_rate_hz: float = 12_000.0,
) -> BearingRecording:
    """Load the first matching *_DE_time or *_FE_time vector from a CWRU MAT file.

    CWRU has recordings with different sampling rates. The rate is therefore an
    explicit argument and must be selected using the dataset file's metadata.
    """
    channel = channel.upper()
    if channel not in {"DE", "FE"}:
        raise ValueError("channel must be 'DE' or 'FE'.")
    if sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be positive.")

    file_path = Path(path)
    if file_path.suffix.lower() != ".mat":
        raise ValueError("Expected a MATLAB .mat file.")

    contents = loadmat(file_path)
    suffix = f"_{channel}_time"
    candidates = sorted(
        (name, value)
        for name, value in contents.items()
        if not name.startswith("__") and name.endswith(suffix)
    )
    if not candidates:
        raise ValueError(f"No {suffix} vibration variable found in {file_path.name}.")

    variable_name, raw_values = candidates[0]
    samples = validate_signal(np.asarray(raw_values).squeeze(), min_points=256)
    return BearingRecording(
        path=str(file_path),
        variable_name=variable_name,
        channel=channel,
        sample_rate_hz=float(sample_rate_hz),
        samples=samples,
    )
