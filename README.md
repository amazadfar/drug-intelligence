# Drug Intelligence

Research-grade biomedical AI scaffolding for drug interaction reasoning.

This repository is the public-safe foundation for an end-to-end drug intelligence platform. The project focuses on the engineering and research layers required to turn heterogeneous pharmacology data into reliable AI systems: molecular featurization, graph representations, knowledge graph design, graph neural network benchmarks, evidence retrieval, and safety-aware evaluation.

## Status

This public repository has completed the public-safe foundation, chemistry
contracts, legacy baseline audit, and public-fixture GNN benchmark plumbing.

Included now:
- repository structure for a clean Python package
- publication boundary and licensing documentation
- safety statement for research-only use
- CI, tests, issue templates, and roadmap
- sample-data directories without restricted data
- stdlib data schemas for drug, interaction, reference, and molecular feature records
- optional RDKit feature extraction module
- framework-neutral molecular graph conversion
- legacy GNN baseline audit and model card
- config-driven CPU GNN benchmark with five encoder families
- random, drug-disjoint, and scaffold-group split APIs
- synthetic benchmark metrics/report artifacts

Not included:
- raw DrugBank data
- scraped DrugBank-derived dumps
- credentials or browser/session material
- large pickle/model/checkpoint artifacts
- vendored DeepChem source
- legacy IDE/project files

## Why This Exists

The private legacy workspace contains prototype work across:
- drug data collection and normalization
- RDKit molecular descriptor and graph feature extraction
- Neo4j-style knowledge graph construction
- Torch Geometric graph neural network experiments
- historical DDI mechanism and severity benchmarks

The public project will turn that work into a reproducible portfolio-grade research platform without publishing restricted data or unsafe credentials.

## Public-Safe Corpus Policy

This repo publishes code, schemas, documentation, synthetic or license-safe fixtures, and experiment reports. It does not publish restricted third-party datasets.

For full-scale experiments, users must bring their own properly licensed data. See:
- [Publication Boundary](docs/publication-boundary.md)
- [Licensing Notes](docs/licensing.md)
- [Safety Statement](docs/safety.md)
- [Public Fixture Data Card](docs/data-card-public-fixtures.md)
- [Legacy GNN Model Card](docs/model-card-gnn-baseline.md)

## Planned Architecture

```text
data ingestion
  -> entity normalization
  -> RDKit molecular featurization
  -> graph and KG construction
  -> graph ML benchmarks
  -> evidence retrieval
  -> safety-aware evaluation
```

## Roadmap

Milestone progress is tracked in [docs/roadmap.md](docs/roadmap.md):

1. Public-safe foundation
2. Chemistry feature extraction and legacy baseline audit
3. Reproducible GNN benchmark infrastructure
4. Biomedical knowledge graph layer
5. Evidence-grounded retrieval assistant
6. Multimodal interaction modeling
7. Continuous public experiment publishing

## Research Safety

This project is not medical software, not clinical decision support, and not a source of medical advice. Any generated or predicted interaction information must be treated as research output requiring expert review and source verification.

## Development

Create an isolated environment:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

Run local checks:

```bash
python -m compileall src tests
python -m pytest -q
python -m ruff check .
```

Install optional chemistry dependencies when working on RDKit-backed features:

```bash
python -m pip install -e ".[dev,chem]"
```

Install GNN dependencies:

```bash
python -m pip install -e ".[dev,chem,gnn]"
```

Run the public synthetic smoke benchmark:

```bash
python scripts/train_gnn_baseline.py \
  --config configs/sample-gin.toml \
  --output-dir artifacts/sample-benchmark
```

See [docs/gnn-benchmark.md](docs/gnn-benchmark.md) for supported encoders,
split strategies, output contracts, and limitations.

## Repository Layout

```text
docs/                  public boundary, licensing, safety, roadmap
examples/              legal-safe fixtures only
src/drug_intelligence/ Python package
tests/                 CPU-safe tests
scripts/               future reproducible workflows
notebooks/             future reviewed notebooks
reports/               future experiment reports
```

## License

Code in this repository is licensed under Apache-2.0. Dataset licenses are separate and must be respected independently. See [docs/licensing.md](docs/licensing.md).
