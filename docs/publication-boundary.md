# Publication Boundary

Date: 2026-06-09

Status: Active boundary for the public repository.

## Purpose

This document defines what may be published in this repository and what must stay
private. The project is intended to demonstrate biomedical AI engineering and
research capabilities without redistributing restricted data, exposing secrets,
or implying clinical readiness.

## Public Repository Scope

The public repository may include:
- project-owned source code
- package metadata and CI configuration
- data schemas and validation contracts
- legal-safe synthetic or tiny hand-authored fixtures
- documentation, architecture diagrams, model cards, and data cards
- experiment reports that do not expose restricted source records
- scripts that run on legal-safe fixtures by default
- importer interfaces for users who bring their own properly licensed data

## Public Repository Exclusions

The public repository must not include:
- raw DrugBank data
- scraped DrugBank-derived dumps
- account-specific browser/session artifacts
- `.env`, `keys.env`, API keys, passwords, cookies, or tokens
- hardcoded usernames or passwords
- raw private data exports
- large pickle datasets
- model checkpoints trained on non-redistributable data unless release rights are confirmed
- backup archives
- vendored `deepchem/` source
- IDE/project metadata such as `.idea/`
- claims that the system is medical advice or clinical decision support

## Legacy Workspace Boundary

The legacy workspace is source material only. It is not itself the public
artifact.

Known legacy paths that must stay out of the public repository:
- `chem-data-collection/data/`
- `chem-data-collection/keys.env`
- `chem-data-collection/drugbank/collecting.py` until credentials are removed
- `chem-graph-network/data/`
- `chem-graph-network/.git/`
- `chem-graph-network/.idea/`
- `deepchem/`
- any `*.pkl`, `*.pth`, `*.pt`, `*.ckpt`, `*.zip`, `*.tar`, or large raw JSON dump

## Public Data Policy

The public repo should use one of these data categories:

1. Synthetic fixtures
   - Hand-authored examples that resemble the schema but do not copy restricted
     records.

2. License-safe public fixtures
   - Records from sources whose terms allow the intended public use, with
     attribution and license notes.

3. Bring-your-own-data workflows
   - Scripts and schemas that operate on user-provided licensed data kept outside
     Git.

DrugBank-derived bulk data is excluded unless a written license explicitly
permits the intended public release.

## Model Artifact Policy

Model checkpoints must not be committed to Git.

Allowed:
- tiny fixture-trained weights only if useful and legal-safe
- model cards
- metric JSON files that do not expose restricted examples
- release assets only after licensing review

Not allowed:
- checkpoints trained on restricted data unless release rights are confirmed
- checkpoints larger than Git-friendly size
- serialized datasets disguised as model artifacts

## Claim Boundary

Allowed claims:
- "research prototype"
- "public-safe scaffolding"
- "reproducible sample workflow"
- "historical baseline, with caveats"
- "not medical advice"

Disallowed claims:
- "clinical decision support"
- "validated for patient care"
- "medical recommendation system"
- "safe for prescribing"
- "state of the art" without rigorous baseline comparisons

## First Release Gate

Before the repository is made public:
- [ ] no restricted raw data is present
- [ ] no secrets are present
- [ ] no large binary artifacts are present
- [ ] `README.md` states the research-only boundary
- [ ] `docs/licensing.md` is present
- [ ] `docs/safety.md` is present
- [ ] tests and import checks pass
- [ ] a fresh clone can run the sample checks
