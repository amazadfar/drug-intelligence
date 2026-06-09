"""Torch Geometric graph encoders used by the reproducible benchmark."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _load_gnn_dependencies() -> dict[str, Any]:
    try:
        import torch
        from torch import nn
        from torch_geometric.nn import (
            GATConv,
            GATv2Conv,
            GINConv,
            TransformerConv,
            global_mean_pool,
        )
    except ImportError as exc:  # pragma: no cover - exercised without gnn extras
        raise RuntimeError(
            "PyTorch and PyTorch Geometric are required. "
            "Install the GNN extra with `pip install -e '.[gnn]'`."
        ) from exc

    return {
        "GATConv": GATConv,
        "GATv2Conv": GATv2Conv,
        "GINConv": GINConv,
        "TransformerConv": TransformerConv,
        "global_mean_pool": global_mean_pool,
        "nn": nn,
        "torch": torch,
    }


@dataclass(frozen=True)
class EncoderConfig:
    name: str = "gin"
    node_dim: int = 6
    edge_dim: int = 3
    hidden_dim: int = 32
    num_layers: int = 3
    num_heads: int = 2
    dropout: float = 0.2


def build_graph_encoder(config: EncoderConfig) -> Any:
    """Build a supported graph encoder from a serializable config."""

    deps = _load_gnn_dependencies()
    name = config.name.lower()
    if name == "gin":
        return _GINEncoder(config, deps)
    if name == "gat":
        return _AttentionEncoder(config, deps, conv_name="gat")
    if name == "gatv2":
        return _AttentionEncoder(config, deps, conv_name="gatv2")
    if name == "transformer":
        return _AttentionEncoder(config, deps, conv_name="transformer")
    if name == "mpnn":
        return _MPNNEncoder(config, deps)
    raise ValueError(f"Unsupported encoder {config.name!r}.")


class _GINEncoder:
    def __new__(cls, config: EncoderConfig, deps: dict[str, Any]) -> Any:
        nn = deps["nn"]
        global_mean_pool = deps["global_mean_pool"]

        class GINEncoder(nn.Module):
            output_dim = config.hidden_dim

            def __init__(self) -> None:
                super().__init__()
                self.dropout = config.dropout
                self.convs = nn.ModuleList()
                self.norms = nn.ModuleList()
                for layer_idx in range(config.num_layers):
                    input_dim = config.node_dim if layer_idx == 0 else config.hidden_dim
                    mlp = nn.Sequential(
                        nn.Linear(input_dim, config.hidden_dim),
                        nn.ReLU(),
                        nn.Linear(config.hidden_dim, config.hidden_dim),
                    )
                    self.convs.append(deps["GINConv"](mlp))
                    self.norms.append(nn.BatchNorm1d(config.hidden_dim))

            def forward(self, data: Any) -> Any:
                x = data.x
                for conv, norm in zip(self.convs, self.norms, strict=True):
                    x = conv(x, data.edge_index)
                    x = norm(x).relu()
                    x = nn.functional.dropout(x, p=self.dropout, training=self.training)
                return global_mean_pool(x, data.batch)

        return GINEncoder()


class _AttentionEncoder:
    def __new__(
        cls,
        config: EncoderConfig,
        deps: dict[str, Any],
        conv_name: str,
    ) -> Any:
        nn = deps["nn"]
        global_mean_pool = deps["global_mean_pool"]

        class AttentionEncoder(nn.Module):
            output_dim = config.hidden_dim

            def __init__(self) -> None:
                super().__init__()
                self.dropout = config.dropout
                self.convs = nn.ModuleList()
                self.norms = nn.ModuleList()
                for layer_idx in range(config.num_layers):
                    input_dim = config.node_dim if layer_idx == 0 else config.hidden_dim
                    kwargs = {
                        "in_channels": input_dim,
                        "out_channels": config.hidden_dim,
                        "heads": config.num_heads,
                        "concat": False,
                        "dropout": config.dropout,
                    }
                    if conv_name in {"gatv2", "transformer"}:
                        kwargs["edge_dim"] = config.edge_dim
                    conv_cls = {
                        "gat": deps["GATConv"],
                        "gatv2": deps["GATv2Conv"],
                        "transformer": deps["TransformerConv"],
                    }[conv_name]
                    self.convs.append(conv_cls(**kwargs))
                    self.norms.append(nn.BatchNorm1d(config.hidden_dim))

            def forward(self, data: Any) -> Any:
                x = data.x
                for conv, norm in zip(self.convs, self.norms, strict=True):
                    if conv_name in {"gatv2", "transformer"}:
                        x = conv(x, data.edge_index, data.edge_attr)
                    else:
                        x = conv(x, data.edge_index)
                    x = norm(x).relu()
                    x = nn.functional.dropout(x, p=self.dropout, training=self.training)
                return global_mean_pool(x, data.batch)

        return AttentionEncoder()


class _MPNNEncoder:
    def __new__(cls, config: EncoderConfig, deps: dict[str, Any]) -> Any:
        nn = deps["nn"]
        torch = deps["torch"]
        global_mean_pool = deps["global_mean_pool"]
        try:
            from torch_geometric.nn import MessagePassing
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("PyTorch Geometric MessagePassing is unavailable.") from exc

        class EdgeMessageLayer(MessagePassing):
            def __init__(self, input_dim: int) -> None:
                super().__init__(aggr="mean")
                self.message_mlp = nn.Sequential(
                    nn.Linear(input_dim + config.edge_dim, config.hidden_dim),
                    nn.ReLU(),
                    nn.Linear(config.hidden_dim, config.hidden_dim),
                )
                self.update_mlp = nn.Sequential(
                    nn.Linear(input_dim + config.hidden_dim, config.hidden_dim),
                    nn.ReLU(),
                )

            def forward(self, x: Any, edge_index: Any, edge_attr: Any) -> Any:
                return self.propagate(edge_index, x=x, edge_attr=edge_attr)

            def message(self, x_j: Any, edge_attr: Any) -> Any:
                return self.message_mlp(torch.cat([x_j, edge_attr], dim=-1))

            def update(self, aggr_out: Any, x: Any) -> Any:
                return self.update_mlp(torch.cat([x, aggr_out], dim=-1))

        class MPNNEncoder(nn.Module):
            output_dim = config.hidden_dim

            def __init__(self) -> None:
                super().__init__()
                self.dropout = config.dropout
                self.convs = nn.ModuleList()
                self.norms = nn.ModuleList()
                for layer_idx in range(config.num_layers):
                    input_dim = config.node_dim if layer_idx == 0 else config.hidden_dim
                    self.convs.append(EdgeMessageLayer(input_dim))
                    self.norms.append(nn.BatchNorm1d(config.hidden_dim))

            def forward(self, data: Any) -> Any:
                x = data.x
                for conv, norm in zip(self.convs, self.norms, strict=True):
                    x = conv(x, data.edge_index, data.edge_attr)
                    x = norm(x).relu()
                    x = nn.functional.dropout(x, p=self.dropout, training=self.training)
                return global_mean_pool(x, data.batch)

        return MPNNEncoder()
