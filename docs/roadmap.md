# Roadmap

Date: 2026-06-09

## Milestone 1: Public-Safe Foundation

Target outcome:
- clean public repository skeleton
- publication boundary
- licensing notes
- safety statement
- CI and tests
- no restricted data or secrets

Status:
- complete, pushed to GitHub, and covered by CI

## Milestone 2: Chemistry Feature Extraction and Legacy Baseline Audit

Target outcome:
- extract RDKit feature generation into tested modules
- define drug, interaction, reference, and molecular feature schemas
- create synthetic fixtures
- convert historical GNN results into a model card with caveats

Status:
- complete, pushed to GitHub, and covered by CI

Evidence:
- `src/drug_intelligence/data/schemas.py`
- `src/drug_intelligence/chemistry/rdkit_features.py`
- `src/drug_intelligence/chemistry/graph_conversion.py`
- `examples/sample_drugs.jsonl`
- `examples/sample_interactions.jsonl`
- `examples/sample_references.jsonl`
- `docs/data-card-public-fixtures.md`
- `docs/model-card-gnn-baseline.md`
- `reports/2026-06-09-legacy-baseline-audit.md`

## Milestone 3: Reproducible GNN Benchmark

Target outcome:
- package GATv1, GATv2, GIN, TransformerConv, MPNN, and pair-prediction heads
- add command-line training and evaluation
- support random, drug-disjoint, and scaffold-style splits
- emit metrics JSON and Markdown reports

Status:
- public fixture benchmark implementation complete locally
- pushed to GitHub and covered by CI
- full scientific benchmark pending a legal, versioned dataset manifest

Evidence:
- `src/drug_intelligence/models/`
- `src/drug_intelligence/evals/`
- `src/drug_intelligence/benchmarking/`
- `scripts/train_gnn_baseline.py`
- `configs/sample-gin.toml`
- `docs/gnn-benchmark.md`
- `reports/sample-benchmark/`

## Milestone 4: Biomedical Knowledge Graph Layer

Target outcome:
- define KG node and edge schema
- export sample triples and Neo4j Cypher
- add validation checks and example queries

Status:
- public fixture KG foundation complete locally
- pending GitHub push and CI validation for this milestone

Evidence:
- `src/drug_intelligence/graph/`
- `scripts/export_kg_sample.py`
- `docs/knowledge-graph.md`
- `reports/sample-kg/sample-kg.json`
- `reports/sample-kg/sample-kg.cypher`
- `tests/test_knowledge_graph.py`

## Milestone 5: Evidence-Grounded Retrieval Assistant

Target outcome:
- build retrieval over legal-safe fixture corpus
- answer with citations
- abstain when evidence is missing
- evaluate retrieval and citation coverage

## Milestone 6: Multimodal Interaction Modeling

Target outcome:
- combine molecular graphs, pharmacology text, KG neighborhoods, and evidence
- compare unimodal and multimodal baselines
- publish ablations and failure analysis

## Milestone 7: Continuous Public Experiment Publishing

Target outcome:
- tagged releases
- experiment reports
- model cards
- data cards
- public issues and milestones
