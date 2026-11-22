"""Compact 1D-CNN for fixed-length vibration windows (optional PyTorch)."""
from __future__ import annotations

try:
    import torch
    from torch import nn
except ImportError as exc:  # pragma: no cover - depends on optional ML environment
    raise ImportError("Install the ML dependencies with: pip install -r requirements-ml.txt") from exc


class BearingCNN1D(nn.Module):
    """Small baseline network; input shape is [batch, 1, samples]."""

    def __init__(self, num_classes: int, dropout: float = 0.25) -> None:
        super().__init__()
        if num_classes < 2:
            raise ValueError("num_classes must be at least 2.")
        self.features = nn.Sequential(
            nn.Conv1d(1, 16, kernel_size=9, padding=4),
            nn.BatchNorm1d(16),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(2),
            nn.Conv1d(16, 32, kernel_size=7, padding=3),
            nn.BatchNorm1d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(2),
            nn.Conv1d(32, 64, kernel_size=5, padding=2),
            nn.BatchNorm1d(64),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool1d(1),
            nn.Flatten(),
            nn.Dropout(dropout),
        )
        self.classifier = nn.Linear(64, num_classes)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        if inputs.ndim != 3 or inputs.shape[1] != 1:
            raise ValueError("Expected input shape [batch, 1, samples].")
        if inputs.shape[-1] < 16:
            raise ValueError("Input window must contain at least 16 samples.")
        return self.classifier(self.features(inputs))
