# Public Safety Audit

Date: 2026-06-09

Status: Milestone 1 audit, local validation pass complete.

## Scope

This audit covers the new clean public repository under:

```text
public/drug-intelligence/
```

The legacy workspace remains outside the public release boundary.

## Legacy Risk Findings

Known risks in the legacy workspace:
- top-level legacy workspace is not a Git repository
- nested Git repository exists under `chem-graph-network/.git`
- nested Git repository exists under `deepchem/.git`
- credential file exists at `chem-data-collection/keys.env`
- hardcoded DrugBank credentials were observed in legacy collection code during
  planning
- large raw data artifacts exist under `chem-data-collection/data/`
- large model/data artifacts exist under `chem-graph-network/data/`
- vendored third-party source exists under `deepchem/`

These legacy paths are intentionally excluded from the public repo skeleton.

## Public Repository Contents

Allowed content currently added:
- package metadata
- README
- Apache-2.0 license
- public boundary docs
- safety and licensing docs
- CI workflow
- issue templates
- tiny metadata-only Python package
- CPU-safe package metadata tests
- empty/sample-safe directories with README guardrails

No raw data or model artifacts were intentionally added.

## Validation Commands

Run from `public/drug-intelligence/`:

```bash
find . -type f -size +1M -print
rg -n "(password|api[_-]?key|secret|token|DrugBank|public_user_password|keys\\.env)" .
python -m compileall src tests
python -m pytest -q
```

If available, also run:

```bash
gitleaks detect --no-git --source .
trufflehog filesystem .
```

## Validation Results

Executed locally on 2026-06-09 from the isolated repo environment:

```text
.venv/bin/python -m compileall src tests
result: passed

.venv/bin/python -m pytest -q
result: passed, 2 tests

.venv/bin/python -m ruff check .
result: passed

find . -path './.git' -prune -o -path './.venv' -prune -o -type f -size +1M -print
result: no files found

rg -n "(public_user_password|keys\\.env|api[_-]?key|secret|token|password|DrugBank)" .
result: documentation-only warnings; no secret values found
```

Not executed because tools were not installed in this environment:

```text
gitleaks
trufflehog
```

## Release Gate

- [x] local validation commands pass
- [x] no files over 1MB unless explicitly justified
- [x] no credential pattern findings except documentation warnings
- [x] no raw restricted data present
- [x] no model checkpoints present
- [x] no vendored third-party source present
- [x] CI workflow exists
- [x] README links to safety and licensing docs

## Notes

The terms `DrugBank`, `password`, `token`, and `keys.env` may appear in
documentation because the public boundary explicitly names what must not be
published. These documentation-only matches are acceptable if no actual secret
values are present.
