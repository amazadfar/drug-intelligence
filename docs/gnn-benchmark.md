# Reproducible GNN Benchmark

Date: 2026-06-09

Status: Synthetic public-fixture smoke benchmark.

## Purpose

This benchmark validates the graph ML training and evaluation pipeline without
using restricted data. It is not a scientific drug-interaction benchmark.

## Supported Encoders

- GIN
- GAT
- GATv2 with edge features
- TransformerConv with edge features
- MPNN-style message passing with edge features

The implementation follows current PyTorch Geometric APIs for graph convolution,
edge features, batching, and global mean pooling.

## Pair Model

Drug pairs are represented symmetrically using:
- embedding sum
- absolute embedding difference
- element-wise embedding product

Swapping drug A and drug B therefore produces the same prediction.

## Tasks

- multi-label interaction mechanism prediction
- per-mechanism severity classification

The public sample labels are deterministic synthetic labels. They carry no
biological or clinical meaning.

## Split Strategies

- `random`
- `drug_disjoint`
- `scaffold_disjoint` through an explicit scaffold-group mapping

Cross-partition pairs are dropped for disjoint splits, preventing the same drug
group from appearing in multiple partitions.

## Run

```bash
python scripts/train_gnn_baseline.py \
  --config configs/sample-gin.toml \
  --output-dir artifacts/sample-benchmark
```

Run on user-provided, properly licensed JSONL records:

```bash
python scripts/train_gnn_baseline.py \
  --config configs/sample-gin.toml \
  --fixtures /private/path/drugs.jsonl \
  --interactions /private/path/interactions.jsonl \
  --output-dir artifacts/licensed-benchmark
```

Override selected config values:

```bash
python scripts/train_gnn_baseline.py \
  --config configs/sample-gin.toml \
  --encoder gatv2 \
  --epochs 3 \
  --seed 7
```

## Outputs

- `sample-benchmark-metrics.json`
- `sample-benchmark-report.md`

The output explicitly sets `scientific_claim` to `false`.

## Metrics

- mechanism micro F1
- mechanism macro F1
- mechanism Brier score
- severity accuracy
- severity macro F1

## Limitations

- synthetic labels
- tiny molecule set
- no real interaction evidence
- no hyperparameter tuning
- no external baselines
- CPU smoke objective only

The full scientific benchmark remains a future milestone requiring a legal,
versioned dataset manifest and leakage-resistant evaluation.
