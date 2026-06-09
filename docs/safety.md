# Safety Statement

Date: 2026-06-09

## Research-Only Boundary

Drug Intelligence is a research and portfolio project. It is not medical
software, not clinical decision support, and not a source of medical advice.

No output from this project should be used to diagnose, treat, prescribe,
recommend, or change medication use.

## Intended Uses

Appropriate uses:
- ML engineering demonstration
- biomedical AI research prototyping
- graph ML benchmark exploration
- knowledge graph schema exploration
- retrieval and evidence-grounding experiments
- educational review of model limitations

Inappropriate uses:
- patient care
- prescribing decisions
- medication management
- emergency medical guidance
- replacing pharmacist, physician, or clinical expert review

## Required Answer Behavior for Future Assistants

Any future retrieval or assistant component must:
- cite evidence when answering
- separate known source-backed facts from model predictions
- abstain when evidence is missing or weak
- avoid dosage or treatment recommendations
- include uncertainty when appropriate
- direct users to qualified medical professionals for clinical questions

## Model Risk Areas

Known risk areas:
- incomplete source data
- label noise
- data leakage across drug pairs
- class imbalance in rare interaction mechanisms
- hallucinated explanations from language models
- overconfident predictions on out-of-distribution drugs
- interaction context missing patient-specific factors

## Public Communication Rule

README files, reports, demos, and release notes must describe the system as a
research prototype. They must not imply clinical validation.
