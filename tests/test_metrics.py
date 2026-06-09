import torch

from drug_intelligence.evals import compute_multitask_metrics


def test_metrics_are_perfect_for_perfect_predictions() -> None:
    mechanism_targets = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
    mechanism_logits = torch.tensor([[10.0, -10.0], [-10.0, 10.0]])
    severity_targets = torch.tensor([[2, 0], [0, 3]])
    severity_logits = torch.full((2, 2, 4), -10.0)
    severity_logits[0, 0, 2] = 10.0
    severity_logits[0, 1, 0] = 10.0
    severity_logits[1, 0, 0] = 10.0
    severity_logits[1, 1, 3] = 10.0

    metrics = compute_multitask_metrics(
        mechanism_logits,
        severity_logits,
        mechanism_targets,
        severity_targets,
    )

    assert metrics["mechanism_f1_micro"] == 1.0
    assert metrics["mechanism_f1_macro"] == 1.0
    assert metrics["severity_accuracy"] == 1.0
    assert metrics["severity_f1_macro"] == 0.75
