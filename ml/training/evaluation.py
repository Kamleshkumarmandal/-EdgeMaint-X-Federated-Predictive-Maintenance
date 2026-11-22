"""Evaluation helpers with macro-averaged metrics for imbalanced fault classes."""
from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


def evaluate_predictions(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    labels: list[int] | None = None,
) -> dict[str, Any]:
    truth = np.asarray(y_true)
    predicted = np.asarray(y_pred)
    if truth.ndim != 1 or predicted.ndim != 1 or truth.shape != predicted.shape or truth.size == 0:
        raise ValueError("y_true and y_pred must be non-empty 1-D arrays with equal lengths.")

    inferred_labels = sorted(set(truth.tolist()) | set(predicted.tolist()))
    target_labels = labels if labels is not None else inferred_labels
    return {
        "accuracy": float(accuracy_score(truth, predicted)),
        "macro_precision": float(precision_score(truth, predicted, labels=target_labels, average="macro", zero_division=0)),
        "macro_recall": float(recall_score(truth, predicted, labels=target_labels, average="macro", zero_division=0)),
        "macro_f1": float(f1_score(truth, predicted, labels=target_labels, average="macro", zero_division=0)),
        "labels": target_labels,
        "confusion_matrix": confusion_matrix(truth, predicted, labels=target_labels).tolist(),
        "classification_report": classification_report(truth, predicted, labels=target_labels, zero_division=0, output_dict=True),
    }
