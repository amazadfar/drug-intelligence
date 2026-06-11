# Experiment Log

Date: 2026-06-09

This file will index public experiment reports.

## Format

Each experiment should include:
- hypothesis
- dataset or fixture version
- method
- metrics
- evidence artifacts
- limitations
- decision

## Entries

### 2026-06-09: Synthetic GIN Benchmark Smoke

- report: `reports/sample-benchmark/sample-benchmark-report.md`
- metrics: `reports/sample-benchmark/sample-benchmark-metrics.json`
- purpose: validate benchmark plumbing only
- scientific claim: false
- dataset: 10 public synthetic molecules, 45 derived synthetic pairs
- encoder: GIN
- epochs: 5
- split: deterministic random split

### 2026-06-11: Public Fixture Knowledge Graph Export

- JSON artifact: `reports/sample-kg/sample-kg.json`
- Neo4j Cypher artifact: `reports/sample-kg/sample-kg.cypher`
- purpose: validate KG schema, provenance rules, deterministic export, and sample query generation
- scientific claim: false
- dataset: 10 public synthetic molecule records, 1 synthetic interaction, 1 synthetic reference
- graph size: 26 nodes, 37 relationships
- validation: duplicate node/relationship checks, required node properties, endpoint existence, relationship provenance
