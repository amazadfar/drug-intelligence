"""Run the public synthetic GNN benchmark."""

from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path

from drug_intelligence.benchmarking import (
    BenchmarkConfig,
    run_jsonl_benchmark,
    run_sample_benchmark,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/sample-gin.toml"),
    )
    parser.add_argument(
        "--encoder",
        choices=("gin", "gat", "gatv2", "transformer", "mpnn"),
        default=None,
    )
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument(
        "--split",
        choices=("random", "drug_disjoint", "scaffold_disjoint"),
        default=None,
    )
    parser.add_argument(
        "--fixtures",
        type=Path,
        default=Path("examples/sample_drugs.jsonl"),
    )
    parser.add_argument(
        "--interactions",
        type=Path,
        default=None,
        help="Optional licensed interaction JSONL. Omit for synthetic pair labels.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/sample-benchmark"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = BenchmarkConfig.from_toml(args.config)
    config = replace(
        config,
        encoder=args.encoder or config.encoder,
        epochs=args.epochs if args.epochs is not None else config.epochs,
        seed=args.seed if args.seed is not None else config.seed,
        split_strategy=args.split or config.split_strategy,
    )
    if config.split_strategy == "scaffold_disjoint":
        raise SystemExit(
            "The sample CLI does not infer scaffold groups yet. "
            "Use the split_pairs API with an explicit group_by_drug mapping."
        )
    if args.interactions is None:
        result = run_sample_benchmark(
            config,
            fixtures_path=args.fixtures,
            output_dir=args.output_dir,
        )
    else:
        result = run_jsonl_benchmark(
            config,
            drugs_path=args.fixtures,
            interactions_path=args.interactions,
            output_dir=args.output_dir,
        )
    print(result["test_metrics"])


if __name__ == "__main__":
    main()
