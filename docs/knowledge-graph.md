# Biomedical Knowledge Graph

Date: 2026-06-11

Status: Public fixture KG foundation.

## Purpose

The knowledge graph layer turns public-safe drug, interaction, molecule, source,
and reference records into a provenance-aware graph that can be inspected,
validated, exported to JSON, and loaded into Neo4j with generated Cypher.

This milestone is infrastructure. It does not make clinical claims.

## Node Labels

| Label | Meaning |
|---|---|
| `Drug` | Drug or molecule entity. |
| `DrugType` | Public-safe category or type grouping. |
| `MoleculeFeature` | Molecular representation or feature summary. |
| `Interaction` | Drug-pair interaction assertion or prediction target. |
| `Mechanism` | Interaction mechanism label. |
| `Severity` | Severity level for a mechanism or interaction assertion. |
| `Reference` | Evidence or citation metadata. |
| `Source` | Dataset, fixture, importer, or provenance source. |

## Relationship Types

| Type | Meaning |
|---|---|
| `DERIVED_FROM` | Connects graph facts to their source/provenance. |
| `HAS_TYPE` | Connects a drug to a type/category node. |
| `HAS_MOLECULAR_FEATURE` | Connects a drug to molecular representation data. |
| `INVOLVES` | Connects an interaction to participating drugs. |
| `HAS_MECHANISM` | Connects an interaction to mechanism labels. |
| `HAS_SEVERITY` | Connects an interaction to severity labels. |
| `SUPPORTED_BY` | Connects an interaction to evidence/reference records. |

## Provenance Rule

Every relationship must include a `source` property. Source nodes are first-class
graph nodes so downstream RAG and evaluation workflows can trace where a graph
fact came from.

## Neo4j Export

Run:

```bash
python scripts/export_kg_sample.py --output-dir reports/sample-kg
```

Outputs:
- `reports/sample-kg/sample-kg.json`
- `reports/sample-kg/sample-kg.cypher`

The Cypher export includes:
- `CREATE CONSTRAINT ... IF NOT EXISTS` uniqueness constraints
- deterministic `MERGE` statements for nodes
- deterministic `MERGE` statements for relationships
- sample provenance and interaction queries

The generated Cypher follows current Neo4j Cypher syntax for named constraints
and `CREATE CONSTRAINT ... IF NOT EXISTS`.

## Example Query

```cypher
MATCH (interaction:Interaction)-[:INVOLVES]->(drug:Drug)
OPTIONAL MATCH (interaction)-[:HAS_MECHANISM]->(mechanism:Mechanism)
OPTIONAL MATCH (interaction)-[severityRel:HAS_SEVERITY]->(severity:Severity)
RETURN interaction.id AS interaction_id,
       collect(DISTINCT drug.name) AS drugs,
       collect(DISTINCT mechanism.name) AS mechanisms,
       collect(DISTINCT {mechanism: severityRel.mechanism, severity: severity.name}) AS severities;
```

## Validation

The graph validator checks:
- duplicate node IDs
- duplicate relationship IDs
- missing required node properties
- missing relationship endpoints
- missing relationship provenance

## Limitations

- The public graph is built from synthetic fixtures.
- Molecular feature nodes currently store representations, not full RDKit
  descriptor vectors.
- The Cypher exporter is static and deterministic; it is not a live Neo4j
  ingestion client.
- Full-scale graph construction requires a licensed, versioned dataset manifest.
