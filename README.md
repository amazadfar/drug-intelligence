# Drug Intelligence

Research-grade biomedical AI scaffolding for drug interaction reasoning.

This repository is the public-safe foundation for an end-to-end drug intelligence platform. The project focuses on the engineering and research layers required to turn heterogeneous pharmacology data into reliable AI systems: molecular featurization, graph representations, knowledge graph design, graph neural network benchmarks, evidence retrieval, and safety-aware evaluation.

## Status

This public repository is in its first milestone: publication-safe foundation.

Included now:
- repository structure for a clean Python package
- publication boundary and licensing documentation
- safety statement for research-only use
- CI, tests, issue templates, and roadmap
- sample-data directories without restricted data

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

The current milestone is focused on a public-safe foundation. Upcoming milestones are tracked in [docs/roadmap.md](docs/roadmap.md):

1. Public-safe foundation
2. Chemistry feature extraction and legacy baseline audit
3. Reproducible GNN benchmark
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
