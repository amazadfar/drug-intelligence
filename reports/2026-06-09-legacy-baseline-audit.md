# Legacy Baseline Audit

Date: 2026-06-09

Status: Historical evidence extracted from legacy workspace; not rerun in the
public repository.

## Scope

This audit summarizes the legacy GNN baseline evidence that motivated the public
project. It does not validate the old benchmark as final science.

Inspected legacy areas:
- `chem-graph-network/graph_nn.py`
- `chem-graph-network/models/gcn.py`
- `chem-graph-network/models/gnn.py`
- `chem-graph-network/models/nn.py`
- `chem-data-collection/modules/processors.py`
- `chem-graph-network/docs/PROMPT TO BE CONTINUED.txt`

## Facts

- The legacy model used molecular graphs generated from drug molecular features.
- Drug pairs were passed through a shared GNN encoder.
- Each drug graph embedding was concatenated with global molecular features.
- The two drug embeddings were concatenated and passed through a multi-task
  neural network.
- The model predicted mechanism labels and severity labels.
- Legacy code explored GATv1, GATv2, GIN, TransformerConv, and MPNN-style
  encoders.
- The strongest embedded result was GIN + MTNN.

## Historical Result: GIN + MTNN

Embedded test-set metrics after 50 epochs:

| Task | Metric | Value |
|---|---:|---:|
| Mechanism prediction | F1 micro | 0.8096 |
| Mechanism prediction | F1 macro | 0.6657 |
| Mechanism prediction | ROC AUC | 0.9562 |
| Severity prediction | Accuracy | 0.8774 |
| Severity prediction | F1 macro | 0.6434 |

Mechanism report excerpt:

| Mechanism | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| metabolism | 0.81 | 0.80 | 0.80 | 3456 |
| synergy | 0.84 | 0.89 | 0.87 | 8248 |
| antagonism | 0.64 | 0.79 | 0.71 | 995 |
| distribution | 0.46 | 0.62 | 0.53 | 58 |
| excretion | 0.65 | 0.53 | 0.58 | 215 |
| absorption | 0.69 | 0.71 | 0.70 | 581 |
| others | 0.42 | 0.54 | 0.47 | 560 |

## Historical Result: GATv2 + MTNN

Embedded test-set metrics after 50 epochs:

| Task | Metric | Value |
|---|---:|---:|
| Mechanism prediction | F1 micro | 0.6760 |
| Mechanism prediction | F1 macro | 0.4240 |
| Mechanism prediction | ROC AUC | 0.8397 |
| Severity prediction | Accuracy | 0.8025 |
| Severity prediction | F1 macro | 0.4822 |

## Inferences

- The GIN encoder was materially stronger than the GATv2 encoder in the legacy
  run.
- Rare classes such as `distribution` had low support, so macro metrics are more
  informative than accuracy alone.
- Severity accuracy is likely inflated by the prevalence of severity class `0`.
- Severity support is larger than interaction-pair support because severity was
  evaluated over mechanism slots.

## Unknowns

- Whether train/test split leakage exists at drug or scaffold level.
- Whether interaction labels were generated consistently.
- Whether the old labels reflect source evidence, inferred mechanism tags, or
  preprocessing artifacts.
- Whether the result is stable across seeds.
- Whether model performance holds under drug-disjoint or scaffold-disjoint
  evaluation.

## Publication Decision

The historical metrics may be published only with caveats. They should appear as
"legacy baseline evidence" rather than "validated model performance."

## Required Follow-Up

Milestone 3 must rerun the benchmark with:
- explicit dataset manifest
- deterministic split seed
- random split
- drug-disjoint split
- scaffold-style split when available
- leakage checks
- calibration metrics
- full per-class reports
- saved metrics JSON
- model card update
