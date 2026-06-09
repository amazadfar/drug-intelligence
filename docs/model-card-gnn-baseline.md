# Model Card: Legacy GNN Baseline

Date: 2026-06-09

Status: Historical baseline only.

## Model Summary

The legacy project explored pairwise drug interaction prediction using molecular
graphs and graph neural networks.

The best historical result found in the legacy source was a GIN encoder paired
with a multi-task neural network head. The model predicted:
- mechanism labels across seven mechanisms
- severity level per mechanism

## Architecture

High-level architecture:

```text
drug A molecular graph -> GNN encoder -> graph embedding + global features
drug B molecular graph -> GNN encoder -> graph embedding + global features
concatenate both drug embeddings
  -> multi-task neural network
  -> mechanism predictions
  -> per-mechanism severity predictions
```

Explored GNN encoder families:
- MPNN-style message passing
- GATv1
- GATv2 with edge attributes
- GIN
- TransformerConv scaffold

## Historical Metrics

The following metrics were embedded in the legacy `chem-graph-network/graph_nn.py`
source comments. They have not yet been rerun in the public repository.

GIN + MTNN, 50 epochs:

| Task | Metric | Value |
|---|---:|---:|
| Mechanism prediction | F1 micro | 0.8096 |
| Mechanism prediction | F1 macro | 0.6657 |
| Mechanism prediction | ROC AUC | 0.9562 |
| Severity prediction | Accuracy | 0.8774 |
| Severity prediction | F1 macro | 0.6434 |

GATv2 + MTNN, 50 epochs:

| Task | Metric | Value |
|---|---:|---:|
| Mechanism prediction | F1 micro | 0.6760 |
| Mechanism prediction | F1 macro | 0.4240 |
| Mechanism prediction | ROC AUC | 0.8397 |
| Severity prediction | Accuracy | 0.8025 |
| Severity prediction | F1 macro | 0.4822 |

## Major Caveats

These metrics are not final research claims.

Known concerns:
- label provenance needs audit
- split strategy was random and may permit drug-level leakage
- severity support counts reflect per-mechanism severity slots, not only unique
  interaction pairs
- class imbalance is severe for rare mechanisms and severity levels
- no calibration report exists yet
- no confidence intervals exist yet
- no external benchmark comparison exists yet
- the public repository has not rerun the experiment

## Appropriate Use

Appropriate:
- historical context
- baseline target for rerun
- architecture documentation
- roadmap input

Inappropriate:
- clinical decision-making
- state-of-the-art claims
- final scientific claims
- model deployment

## Next Validation Steps

Before this model can be treated as a credible benchmark:
- rerun on a reproducible dataset manifest
- add drug-disjoint split
- add scaffold-style split
- add leakage checks
- add calibration metrics
- add per-class and per-severity error analysis
- compare against fingerprint/MLP and text/KG baselines
