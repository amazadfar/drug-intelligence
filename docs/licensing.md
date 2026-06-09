# Licensing Notes

Date: 2026-06-09

This repository separates code licensing from data licensing.

## Repository Code

Project-owned code in this repository is licensed under Apache-2.0 unless a file
states otherwise.

The Apache-2.0 license applies to this repository's source code and
documentation. It does not grant rights to third-party datasets, third-party
database content, or private artifacts.

## DrugBank

DrugBank data must be treated as restricted unless the user has a license that
explicitly permits the intended use and redistribution.

Relevant public terms:
- https://trust.drugbank.com/drugbank-trust-center/drugbank-terms-of-service
- https://go.drugbank.com/press

Operational rule for this repository:

> Do not publish raw DrugBank content, scraped DrugBank-derived dumps, or model
> artifacts that expose non-redistributable DrugBank content unless written
> permission or a suitable license permits that exact release.

Allowed public materials:
- importer code
- schemas
- validation logic
- documentation
- synthetic examples
- "bring your own licensed data" instructions

## DDInter

DDInter states that its data is under Creative Commons
Attribution-NonCommercial-ShareAlike 4.0 International.

Relevant public page:
- https://ddinter.scbdd.com/terms/

Operational rule for this repository:

> DDInter-derived examples may only be used if attribution, non-commercial, and
> share-alike obligations are satisfied. Prefer synthetic fixtures for the first
> public milestone.

## DeepChem

Do not vendor the legacy local `deepchem/` checkout into this repository.

If DeepChem is needed later, depend on it through normal package management and
respect its upstream license.

## Model Weights and Reports

Model weights, metrics, and reports inherit obligations from the data used to
produce them.

Before publishing a checkpoint or full benchmark artifact, verify:
- source dataset license
- redistribution rights
- whether examples or labels can be reconstructed from the artifact
- whether the artifact contains protected or private information

## Citation and Attribution

Future data cards and model cards should include:
- source names
- source URLs
- access dates
- license or terms summary
- permitted uses
- redistribution limitations
- citation format

## Current Release Decision

For Milestone 1, this repository publishes no raw third-party dataset content.
It contains only code, docs, package metadata, and empty/sample-safe directories.
