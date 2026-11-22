"""Framework-independent FedAvg tensor aggregation for local experiments."""
from __future__ import annotations

from collections import OrderedDict
from collections.abc import Sequence

try:
    import torch
except ImportError as exc:  # pragma: no cover - optional ML dependency
    raise ImportError("Install the ML dependencies with: pip install -r requirements-ml.txt") from exc


def aggregate_state_dicts(
    client_states: Sequence[dict[str, torch.Tensor]],
    num_examples: Sequence[int],
) -> OrderedDict[str, torch.Tensor]:
    """Aggregate parameters weighted by each client's training-example count.

    Floating tensors are weighted averages. Non-floating buffers use element-wise
    maximum, which is suitable for counters such as BatchNorm's batch counter.
    """
    if not client_states or len(client_states) != len(num_examples):
        raise ValueError("Provide one positive example count for each client state.")
    if any(count <= 0 for count in num_examples):
        raise ValueError("Client example counts must all be positive.")

    reference_keys = list(client_states[0].keys())
    reference_shapes = {key: client_states[0][key].shape for key in reference_keys}
    for state in client_states[1:]:
        if list(state.keys()) != reference_keys:
            raise ValueError("All client state dictionaries must have identical keys.")
        for key in reference_keys:
            if state[key].shape != reference_shapes[key]:
                raise ValueError(f"Tensor shape mismatch for parameter '{key}'.")

    total_examples = float(sum(num_examples))
    aggregated: OrderedDict[str, torch.Tensor] = OrderedDict()
    for key in reference_keys:
        tensors = [state[key].detach().clone() for state in client_states]
        if torch.is_floating_point(tensors[0]) or torch.is_complex(tensors[0]):
            weighted = torch.zeros_like(tensors[0])
            for tensor, count in zip(tensors, num_examples, strict=True):
                weighted.add_(tensor, alpha=float(count / total_examples))
            aggregated[key] = weighted
        else:
            aggregated[key] = torch.stack(tensors).amax(dim=0)
    return aggregated
