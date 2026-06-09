# Data Card: Public Fixtures

Date: 2026-06-09

Status: Active for Milestone 2.

## Dataset Name

Drug Intelligence public fixtures.

## Purpose

The fixtures exercise schemas, molecular feature extraction, graph conversion,
and future retrieval/benchmark scaffolding without publishing restricted data.

## Contents

Files:
- `examples/sample_drugs.jsonl`
- `examples/sample_interactions.jsonl`
- `examples/sample_references.jsonl`

Current record counts:
- drugs: 10
- interactions: 1
- references: 1

## Source

The fixtures are hand-authored synthetic records. They are not copied from
DrugBank, DDInter, or another restricted source.

The SMILES strings are common chemistry examples used only to exercise RDKit
feature extraction. They do not imply clinical claims.

## Intended Use

Appropriate uses:
- schema validation
- chemistry feature smoke tests
- graph conversion tests
- documentation examples
- future CI smoke workflows

Inappropriate uses:
- model performance claims
- biological or clinical inference
- benchmarking
- medical advice

## Known Limitations

- Too small for ML training.
- The GNN smoke benchmark derives synthetic pair labels from these molecules only
  to validate training and evaluation plumbing.
- Not representative of real pharmacology distributions.
- Interaction labels are synthetic and do not encode real clinical evidence.
- No patient, dosage, route, timing, or disease context is represented.

## License

The fixture records are part of this repository and follow the repository code
license unless stated otherwise.

Third-party dataset licenses are not inherited by these synthetic fixtures.
