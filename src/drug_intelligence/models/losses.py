"""Multi-task objective for mechanism and severity prediction."""

from __future__ import annotations

from typing import Any


class MultiTaskLoss:
    def __new__(
        cls,
        severity_weight: float = 1.0,
        mechanism_pos_weight: Any | None = None,
    ) -> Any:
        try:
            from torch import nn
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("PyTorch is required for multi-task loss.") from exc

        class Loss(nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.severity_weight = severity_weight
                self.mechanism_loss = nn.BCEWithLogitsLoss(
                    pos_weight=mechanism_pos_weight,
                )
                self.severity_loss = nn.CrossEntropyLoss()

            def forward(
                self,
                mechanism_logits: Any,
                severity_logits: Any,
                mechanism_targets: Any,
                severity_targets: Any,
            ) -> tuple[Any, dict[str, float]]:
                mechanism_loss = self.mechanism_loss(
                    mechanism_logits,
                    mechanism_targets,
                )
                severity_loss = self.severity_loss(
                    severity_logits.reshape(-1, severity_logits.size(-1)),
                    severity_targets.reshape(-1),
                )
                total = mechanism_loss + self.severity_weight * severity_loss
                return total, {
                    "mechanism_loss": float(mechanism_loss.detach().cpu()),
                    "severity_loss": float(severity_loss.detach().cpu()),
                    "total_loss": float(total.detach().cpu()),
                }

        return Loss()
