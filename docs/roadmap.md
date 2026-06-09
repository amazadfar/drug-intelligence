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
- complete locally; not yet published to GitHub

## Milestone 2: Chemistry Feature Extraction and Legacy Baseline Audit

Target outcome:
- extract RDKit feature generation into tested modules
- define drug, interaction, reference, and molecular feature schemas
- create synthetic fixtures
- convert historical GNN results into a model card with caveats

## Milestone 3: Reproducible GNN Benchmark

Target outcome:
- package GATv1, GATv2, GIN, TransformerConv, MPNN, and pair-prediction heads
- add command-line training and evaluation
- support random, drug-disjoint, and scaffold-style splits
- emit metrics JSON and Markdown reports

## Milestone 4: Biomedical Knowledge Graph Layer

Target outcome:
- define KG node and edge schema
- export sample triples and Neo4j Cypher
- add validation checks and example queries

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
