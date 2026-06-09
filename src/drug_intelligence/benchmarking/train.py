"""Deterministic CPU-safe training loop for the sample GNN benchmark."""

from __future__ import annotations

import json
import random
import sys
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from drug_intelligence.benchmarking.sample_dataset import (
    EDGE_FEATURES,
    GLOBAL_FEATURES,
    NODE_FEATURES,
    build_graphs_from_jsonl,
    build_sample_graphs,
    build_sample_pairs,
    load_interaction_pairs,
)
from drug_intelligence.benchmarking.splits import PairExample, split_pairs
from drug_intelligence.data import MECHANISM_LABELS, SEVERITY_LABELS
from drug_intelligence.evals import compute_multitask_metrics
from drug_intelligence.models import (
    DrugPairInteractionModel,
    EncoderConfig,
    MultiTaskLoss,
    build_graph_encoder,
)


@dataclass(frozen=True)
class BenchmarkConfig:
    encoder: str = "gin"
    hidden_dim: int = 32
    num_layers: int = 2
    num_heads: int = 2
    dropout: float = 0.1
    epochs: int = 5
    batch_size: int = 8
    learning_rate: float = 1e-3
    severity_weight: float = 0.5
    split_strategy: str = "random"
    seed: int = 42

    @classmethod
    def from_toml(cls, path: Path) -> BenchmarkConfig:
        content = tomllib.loads(path.read_text())
        return cls(**content["benchmark"])


class _PairDataset:
    def __new__(
        cls,
        pairs: list[PairExample],
        graphs: dict[str, Any],
    ) -> Any:
        import torch

        class Dataset(torch.utils.data.Dataset):
            def __len__(self) -> int:
                return len(pairs)

            def __getitem__(self, index: int) -> tuple[Any, Any, Any, Any]:
                pair = pairs[index]
                return (
                    graphs[pair.drug_id_a],
                    graphs[pair.drug_id_b],
                    torch.tensor(pair.mechanism_targets, dtype=torch.float32),
                    torch.tensor(pair.severity_targets, dtype=torch.long),
                )

        return Dataset()


def _collate_pair_batch(batch: list[tuple[Any, Any, Any, Any]]) -> tuple[Any, ...]:
    import torch
    from torch_geometric.data import Batch

    drugs_a, drugs_b, mechanisms, severities = zip(*batch, strict=True)
    return (
        Batch.from_data_list(list(drugs_a)),
        Batch.from_data_list(list(drugs_b)),
        torch.stack(mechanisms),
        torch.stack(severities),
    )


def run_sample_benchmark(
    config: BenchmarkConfig,
    fixtures_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    graphs = build_sample_graphs(fixtures_path)
    pairs = build_sample_pairs(sorted(graphs))
    return _run_benchmark(
        config,
        graphs,
        pairs,
        output_dir,
        benchmark_name="synthetic-public-fixture-smoke",
        artifact_prefix="sample-benchmark",
        scientific_claim=False,
    )


def _run_benchmark(
    config: BenchmarkConfig,
    graphs: dict[str, Any],
    pairs: list[PairExample],
    output_dir: Path,
    benchmark_name: str,
    artifact_prefix: str,
    scientific_claim: bool,
) -> dict[str, Any]:
    import torch

    _set_deterministic_seed(config.seed, torch)
    device = torch.device("cpu")
    split = split_pairs(pairs, strategy=config.split_strategy, seed=config.seed)
    loaders = {
        name: torch.utils.data.DataLoader(
            _PairDataset([pairs[index] for index in indices], graphs),
            batch_size=config.batch_size,
            shuffle=name == "train",
            collate_fn=_collate_pair_batch,
            generator=torch.Generator().manual_seed(config.seed),
        )
        for name, indices in {
            "train": split.train,
            "validation": split.validation,
            "test": split.test,
        }.items()
    }

    encoder = build_graph_encoder(
        EncoderConfig(
            name=config.encoder,
            node_dim=len(NODE_FEATURES),
            edge_dim=len(EDGE_FEATURES),
            hidden_dim=config.hidden_dim,
            num_layers=config.num_layers,
            num_heads=config.num_heads,
            dropout=config.dropout,
        )
    )
    model = DrugPairInteractionModel(
        encoder=encoder,
        global_feature_dim=len(GLOBAL_FEATURES),
        hidden_dim=config.hidden_dim,
        mechanism_classes=len(MECHANISM_LABELS),
        severity_levels=len(SEVERITY_LABELS),
        dropout=config.dropout,
    ).to(device)
    objective = MultiTaskLoss(severity_weight=config.severity_weight)
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)

    history: list[dict[str, float]] = []
    for epoch in range(config.epochs):
        model.train()
        losses: list[float] = []
        for drug_a, drug_b, mechanism_targets, severity_targets in loaders["train"]:
            optimizer.zero_grad()
            mechanism_logits, severity_logits = model(drug_a, drug_b)
            loss, _ = objective(
                mechanism_logits,
                severity_logits,
                mechanism_targets,
                severity_targets,
            )
            loss.backward()
            optimizer.step()
            losses.append(float(loss.detach()))
        validation_metrics = _evaluate(model, loaders["validation"])
        history.append(
            {
                "epoch": float(epoch + 1),
                "train_loss": sum(losses) / len(losses),
                **{f"validation_{key}": value for key, value in validation_metrics.items()},
            }
        )

    result = {
        "benchmark": benchmark_name,
        "scientific_claim": scientific_claim,
        "config": asdict(config),
        "dataset": {
            "drugs": len(graphs),
            "pairs": len(pairs),
            "train_pairs": len(split.train),
            "validation_pairs": len(split.validation),
            "test_pairs": len(split.test),
            "dropped_pairs": len(split.dropped),
        },
        "test_metrics": _evaluate(model, loaders["test"]),
        "history": history,
        "environment": {
            "device": str(device),
            "python_version": sys.version.split()[0],
            "torch_version": torch.__version__,
        },
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{artifact_prefix}-metrics.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    (output_dir / f"{artifact_prefix}-report.md").write_text(
        _render_report(result)
    )
    return result


def run_jsonl_benchmark(
    config: BenchmarkConfig,
    drugs_path: Path,
    interactions_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    """Run the benchmark on user-provided, properly licensed JSONL records."""

    graphs = build_graphs_from_jsonl(drugs_path)
    pairs = load_interaction_pairs(interactions_path)
    unknown_drugs = sorted(
        {
            drug_id
            for pair in pairs
            for drug_id in (pair.drug_id_a, pair.drug_id_b)
            if drug_id not in graphs
        }
    )
    if unknown_drugs:
        raise ValueError(
            f"Interactions reference missing drug IDs: {', '.join(unknown_drugs)}"
        )
    return _run_benchmark(
        config,
        graphs,
        pairs,
        output_dir,
        benchmark_name="user-provided-jsonl",
        artifact_prefix="benchmark",
        scientific_claim=False,
    )


def _evaluate(model: Any, loader: Any) -> dict[str, float]:
    import torch

    model.eval()
    mechanisms: list[Any] = []
    severities: list[Any] = []
    mechanism_targets: list[Any] = []
    severity_targets: list[Any] = []
    with torch.no_grad():
        for drug_a, drug_b, batch_mechanisms, batch_severities in loader:
            mechanism_logits, severity_logits = model(drug_a, drug_b)
            mechanisms.append(mechanism_logits)
            severities.append(severity_logits)
            mechanism_targets.append(batch_mechanisms)
            severity_targets.append(batch_severities)
    return compute_multitask_metrics(
        torch.cat(mechanisms),
        torch.cat(severities),
        torch.cat(mechanism_targets),
        torch.cat(severity_targets),
    )


def _set_deterministic_seed(seed: int, torch: Any) -> None:
    random.seed(seed)
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)


def _render_report(result: dict[str, Any]) -> str:
    metrics = result["test_metrics"]
    config = result["config"]
    dataset = result["dataset"]
    return (
        "# GNN Benchmark Report\n\n"
        f"Benchmark: `{result['benchmark']}`\n\n"
        f"Scientific claim: `{str(result['scientific_claim']).lower()}`\n\n"
        "This run validates benchmark plumbing. Its metrics are not scientific claims.\n\n"
        "## Configuration\n\n"
        f"- encoder: `{config['encoder']}`\n"
        f"- epochs: `{config['epochs']}`\n"
        f"- seed: `{config['seed']}`\n"
        f"- split: `{config['split_strategy']}`\n\n"
        "## Dataset\n\n"
        f"- drugs: `{dataset['drugs']}`\n"
        f"- pairs: `{dataset['pairs']}`\n"
        f"- train/validation/test: `{dataset['train_pairs']}` / "
        f"`{dataset['validation_pairs']}` / `{dataset['test_pairs']}`\n\n"
        "## Test Metrics\n\n"
        f"- mechanism F1 micro: `{metrics['mechanism_f1_micro']:.4f}`\n"
        f"- mechanism F1 macro: `{metrics['mechanism_f1_macro']:.4f}`\n"
        f"- mechanism Brier score: `{metrics['mechanism_brier']:.4f}`\n"
        f"- severity accuracy: `{metrics['severity_accuracy']:.4f}`\n"
        f"- severity F1 macro: `{metrics['severity_f1_macro']:.4f}`\n"
    )
