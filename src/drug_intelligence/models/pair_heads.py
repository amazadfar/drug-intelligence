"""Symmetric drug-pair prediction model."""

from __future__ import annotations

from typing import Any


def _load_torch() -> tuple[Any, Any]:
    try:
        import torch
        from torch import nn
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("PyTorch is required for pair prediction.") from exc
    return torch, nn


class DrugPairInteractionModel:
    """Factory-backed wrapper that returns an `nn.Module` instance.

    The pair representation uses sum, absolute difference, and element-wise
    product. It is invariant to swapping drug A and drug B.
    """

    def __new__(
        cls,
        encoder: Any,
        global_feature_dim: int,
        hidden_dim: int,
        mechanism_classes: int,
        severity_levels: int,
        dropout: float = 0.2,
    ) -> Any:
        torch, nn = _load_torch()
        drug_embedding_dim = encoder.output_dim + global_feature_dim
        pair_input_dim = drug_embedding_dim * 3

        class PairModel(nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.encoder = encoder
                self.mechanism_classes = mechanism_classes
                self.severity_levels = severity_levels
                self.shared = nn.Sequential(
                    nn.Linear(pair_input_dim, hidden_dim),
                    nn.ReLU(),
                    nn.Dropout(dropout),
                    nn.Linear(hidden_dim, hidden_dim),
                    nn.ReLU(),
                )
                self.mechanism_head = nn.Linear(hidden_dim, mechanism_classes)
                self.severity_head = nn.Linear(
                    hidden_dim,
                    mechanism_classes * severity_levels,
                )

            def forward(self, drug_a: Any, drug_b: Any) -> tuple[Any, Any]:
                embedding_a = torch.cat([self.encoder(drug_a), drug_a.u], dim=-1)
                embedding_b = torch.cat([self.encoder(drug_b), drug_b.u], dim=-1)
                pair_embedding = torch.cat(
                    [
                        embedding_a + embedding_b,
                        torch.abs(embedding_a - embedding_b),
                        embedding_a * embedding_b,
                    ],
                    dim=-1,
                )
                hidden = self.shared(pair_embedding)
                mechanism_logits = self.mechanism_head(hidden)
                severity_logits = self.severity_head(hidden).view(
                    hidden.size(0),
                    self.mechanism_classes,
                    self.severity_levels,
                )
                return mechanism_logits, severity_logits

        return PairModel()
