"""Dependency-light metrics for the public GNN benchmark."""

from __future__ import annotations

from typing import Any


def compute_multitask_metrics(
    mechanism_logits: Any,
    severity_logits: Any,
    mechanism_targets: Any,
    severity_targets: Any,
    threshold: float = 0.5,
) -> dict[str, float]:
    import torch

    mechanism_probabilities = torch.sigmoid(mechanism_logits)
    mechanism_predictions = mechanism_probabilities >= threshold
    mechanism_truth = mechanism_targets.bool()

    true_positive = (mechanism_predictions & mechanism_truth).sum().float()
    false_positive = (mechanism_predictions & ~mechanism_truth).sum().float()
    false_negative = (~mechanism_predictions & mechanism_truth).sum().float()
    mechanism_f1_micro = _f1(true_positive, false_positive, false_negative)

    per_class_f1: list[float] = []
    for class_idx in range(mechanism_truth.size(1)):
        predictions = mechanism_predictions[:, class_idx]
        truth = mechanism_truth[:, class_idx]
        per_class_f1.append(
            _f1(
                (predictions & truth).sum().float(),
                (predictions & ~truth).sum().float(),
                (~predictions & truth).sum().float(),
            )
        )

    severity_predictions = severity_logits.argmax(dim=-1)
    severity_accuracy = (
        (severity_predictions == severity_targets).float().mean().item()
    )
    severity_f1_macro = _multiclass_macro_f1(
        severity_predictions.reshape(-1),
        severity_targets.reshape(-1),
        severity_logits.size(-1),
    )
    mechanism_brier = (
        (mechanism_probabilities - mechanism_targets).square().mean().item()
    )

    return {
        "mechanism_f1_micro": mechanism_f1_micro,
        "mechanism_f1_macro": sum(per_class_f1) / len(per_class_f1),
        "mechanism_brier": mechanism_brier,
        "severity_accuracy": severity_accuracy,
        "severity_f1_macro": severity_f1_macro,
    }


def _f1(true_positive: Any, false_positive: Any, false_negative: Any) -> float:
    denominator = 2 * true_positive + false_positive + false_negative
    if denominator.item() == 0:
        return 0.0
    return float((2 * true_positive / denominator).item())


def _multiclass_macro_f1(predictions: Any, targets: Any, classes: int) -> float:
    scores: list[float] = []
    for class_idx in range(classes):
        predicted_class = predictions == class_idx
        target_class = targets == class_idx
        scores.append(
            _f1(
                (predicted_class & target_class).sum().float(),
                (predicted_class & ~target_class).sum().float(),
                (~predicted_class & target_class).sum().float(),
            )
        )
    return sum(scores) / len(scores)
