"""Convert molecular feature records into tensor-like graph specs.

The output is intentionally framework-neutral. Milestone 3 can adapt this
structure to Torch Geometric without coupling public data contracts to PyTorch.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from drug_intelligence.data import MolecularFeatureRecord


@dataclass(frozen=True)
class GraphTensorSpec:
    """Framework-neutral graph tensor specification."""

    node_feature_names: tuple[str, ...]
    edge_feature_names: tuple[str, ...]
    global_feature_names: tuple[str, ...]
    x: list[list[float]]
    edge_index: list[tuple[int, int]]
    edge_attr: list[list[float]]
    u: list[float]


def to_graph_tensor_spec(
    record: MolecularFeatureRecord,
    node_feature_names: tuple[str, ...],
    edge_feature_names: tuple[str, ...],
    global_feature_names: tuple[str, ...],
) -> GraphTensorSpec:
    """Convert a molecular feature record into numeric graph arrays."""

    issues = record.validate()
    if issues:
        joined = "; ".join(f"{issue.field}: {issue.message}" for issue in issues)
        raise ValueError(f"Invalid molecular feature record: {joined}")

    return GraphTensorSpec(
        node_feature_names=node_feature_names,
        edge_feature_names=edge_feature_names,
        global_feature_names=global_feature_names,
        x=[
            [_to_float(node.get(name)) for name in node_feature_names]
            for node in record.node_features
        ],
        edge_index=record.edge_index,
        edge_attr=[
            [_to_float(edge.get(name)) for name in edge_feature_names]
            for edge in record.edge_features
        ],
        u=[_to_float(record.global_features.get(name)) for name in global_feature_names],
    )


def _to_float(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, int | float):
        return float(value)
    raise TypeError(f"Value {value!r} cannot be converted to a numeric graph feature.")
