"""Build a public-safe knowledge graph from fixture JSONL records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from drug_intelligence.data import InteractionRecord, ReferenceRecord
from drug_intelligence.graph.schema import (
    KGGraph,
    KGNode,
    KGRelationship,
    NodeLabel,
    RelationshipType,
)
from drug_intelligence.graph.validation import validate_graph


def build_fixture_knowledge_graph(
    drugs_path: Path,
    interactions_path: Path,
    references_path: Path,
) -> KGGraph:
    """Build a provenance-aware KG from public fixture records."""

    nodes: dict[str, KGNode] = {}
    relationships: dict[str, KGRelationship] = {}

    drugs = _read_jsonl(drugs_path)
    interactions = _read_jsonl(interactions_path)
    references = _read_jsonl(references_path)

    sources = {_source(row) for row in drugs + interactions + references}
    for source in sorted(sources):
        _add_node(
            nodes,
            KGNode(
                id=f"source:{source}",
                labels=(NodeLabel.SOURCE,),
                properties={"id": f"source:{source}", "name": source},
            ),
        )

    for row in drugs:
        drug_id = row["drug_id"]
        source = _source(row)
        drug_node_id = f"drug:{drug_id}"
        _add_node(
            nodes,
            KGNode(
                id=drug_node_id,
                labels=(NodeLabel.DRUG,),
                properties={
                    "id": drug_node_id,
                    "drug_id": drug_id,
                    "name": row["name"],
                    "normalized_name": row.get("normalized_name"),
                    "description": row.get("description"),
                    "source": source,
                },
            ),
        )
        _add_relationship(
            relationships,
            KGRelationship(
                id=f"{drug_node_id}:derived_from:{source}",
                source_id=drug_node_id,
                target_id=f"source:{source}",
                relationship_type=RelationshipType.DERIVED_FROM,
                properties={"source": source},
            ),
        )
        _add_drug_type(nodes, relationships, drug_node_id, row)
        _add_molecular_feature(nodes, relationships, drug_node_id, row)

    for row in references:
        record = ReferenceRecord(**row)
        _raise_if_invalid(record.reference_id, record.validate())
        source = record.source
        reference_node_id = f"reference:{record.reference_id}"
        _add_node(
            nodes,
            KGNode(
                id=reference_node_id,
                labels=(NodeLabel.REFERENCE,),
                properties={
                    "id": reference_node_id,
                    "reference_id": record.reference_id,
                    "title": record.title,
                    "url": record.url,
                    "abstract": record.abstract,
                    "source": source,
                },
            ),
        )
        _add_relationship(
            relationships,
            KGRelationship(
                id=f"{reference_node_id}:derived_from:{source}",
                source_id=reference_node_id,
                target_id=f"source:{source}",
                relationship_type=RelationshipType.DERIVED_FROM,
                properties={"source": source},
            ),
        )

    for row in interactions:
        record = InteractionRecord(
            interaction_id=row["interaction_id"],
            drug_id_a=row["drug_id_a"],
            drug_id_b=row["drug_id_b"],
            mechanism_labels=tuple(row.get("mechanism_labels", [])),
            severity_by_mechanism=row.get("severity_by_mechanism", {}),
            evidence=row.get("evidence"),
            source=row.get("source", "synthetic"),
            metadata=row.get("metadata", {}),
        )
        _raise_if_invalid(record.interaction_id, record.validate())
        _add_interaction(nodes, relationships, record)

    graph = KGGraph(
        nodes=tuple(nodes.values()),
        relationships=tuple(relationships.values()),
        metadata={
            "builder": "fixture",
            "drugs": len(drugs),
            "interactions": len(interactions),
            "references": len(references),
        },
    )
    issues = validate_graph(graph)
    if issues:
        joined = "; ".join(f"{issue.scope}:{issue.identifier}:{issue.message}" for issue in issues)
        raise ValueError(f"Invalid fixture knowledge graph: {joined}")
    return graph


def _add_drug_type(
    nodes: dict[str, KGNode],
    relationships: dict[str, KGRelationship],
    drug_node_id: str,
    row: dict[str, Any],
) -> None:
    drug_type = row.get("drug_type") or "unknown"
    source = _source(row)
    node_id = f"drug_type:{_slug(drug_type)}"
    _add_node(
        nodes,
        KGNode(
            id=node_id,
            labels=(NodeLabel.DRUG_TYPE,),
            properties={"id": node_id, "name": drug_type, "source": source},
        ),
    )
    _add_relationship(
        relationships,
        KGRelationship(
            id=f"{drug_node_id}:has_type:{node_id}",
            source_id=drug_node_id,
            target_id=node_id,
            relationship_type=RelationshipType.HAS_TYPE,
            properties={"source": source},
        ),
    )


def _add_molecular_feature(
    nodes: dict[str, KGNode],
    relationships: dict[str, KGRelationship],
    drug_node_id: str,
    row: dict[str, Any],
) -> None:
    representation = row.get("smiles") or row.get("inchi")
    if not representation:
        return
    representation_type = "smiles" if row.get("smiles") else "inchi"
    source = _source(row)
    node_id = f"molecule_feature:{row['drug_id']}"
    _add_node(
        nodes,
        KGNode(
            id=node_id,
            labels=(NodeLabel.MOLECULE_FEATURE,),
            properties={
                "id": node_id,
                "representation": representation,
                "representation_type": representation_type,
                "source": source,
            },
        ),
    )
    _add_relationship(
        relationships,
        KGRelationship(
            id=f"{drug_node_id}:has_molecular_feature:{node_id}",
            source_id=drug_node_id,
            target_id=node_id,
            relationship_type=RelationshipType.HAS_MOLECULAR_FEATURE,
            properties={"source": source},
        ),
    )


def _add_interaction(
    nodes: dict[str, KGNode],
    relationships: dict[str, KGRelationship],
    record: InteractionRecord,
) -> None:
    source = record.source
    interaction_node_id = f"interaction:{record.interaction_id}"
    _add_node(
        nodes,
        KGNode(
            id=interaction_node_id,
            labels=(NodeLabel.INTERACTION,),
            properties={
                "id": interaction_node_id,
                "interaction_id": record.interaction_id,
                "evidence": record.evidence,
                "source": source,
            },
        ),
    )
    _add_relationship(
        relationships,
        KGRelationship(
            id=f"{interaction_node_id}:derived_from:{source}",
            source_id=interaction_node_id,
            target_id=f"source:{source}",
            relationship_type=RelationshipType.DERIVED_FROM,
            properties={"source": source},
        ),
    )
    for role, drug_id in (("a", record.drug_id_a), ("b", record.drug_id_b)):
        _add_relationship(
            relationships,
            KGRelationship(
                id=f"{interaction_node_id}:involves:{role}:{drug_id}",
                source_id=interaction_node_id,
                target_id=f"drug:{drug_id}",
                relationship_type=RelationshipType.INVOLVES,
                properties={"role": role, "source": source},
            ),
        )
    for mechanism in record.mechanism_labels:
        mechanism_node_id = f"mechanism:{mechanism}"
        _add_node(
            nodes,
            KGNode(
                id=mechanism_node_id,
                labels=(NodeLabel.MECHANISM,),
                properties={"id": mechanism_node_id, "name": mechanism, "source": source},
            ),
        )
        _add_relationship(
            relationships,
            KGRelationship(
                id=f"{interaction_node_id}:has_mechanism:{mechanism}",
                source_id=interaction_node_id,
                target_id=mechanism_node_id,
                relationship_type=RelationshipType.HAS_MECHANISM,
                properties={"source": source},
            ),
        )
    for mechanism, severity in record.severity_by_mechanism.items():
        severity_node_id = f"severity:{severity}"
        _add_node(
            nodes,
            KGNode(
                id=severity_node_id,
                labels=(NodeLabel.SEVERITY,),
                properties={
                    "id": severity_node_id,
                    "level": severity,
                    "name": _severity_name(severity),
                    "source": source,
                },
            ),
        )
        _add_relationship(
            relationships,
            KGRelationship(
                id=f"{interaction_node_id}:has_severity:{mechanism}:{severity}",
                source_id=interaction_node_id,
                target_id=severity_node_id,
                relationship_type=RelationshipType.HAS_SEVERITY,
                properties={"mechanism": mechanism, "source": source},
            ),
        )
    for reference_id in record.metadata.get("reference_ids", []):
        _add_relationship(
            relationships,
            KGRelationship(
                id=f"{interaction_node_id}:supported_by:{reference_id}",
                source_id=interaction_node_id,
                target_id=f"reference:{reference_id}",
                relationship_type=RelationshipType.SUPPORTED_BY,
                properties={"source": source},
            ),
        )


def _add_node(nodes: dict[str, KGNode], node: KGNode) -> None:
    nodes.setdefault(node.id, node)


def _add_relationship(
    relationships: dict[str, KGRelationship],
    relationship: KGRelationship,
) -> None:
    relationships.setdefault(relationship.id, relationship)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _source(row: dict[str, Any]) -> str:
    return row.get("source") or "synthetic"


def _raise_if_invalid(identifier: str, issues: list[Any]) -> None:
    if issues:
        joined = "; ".join(f"{issue.field}: {issue.message}" for issue in issues)
        raise ValueError(f"Invalid record {identifier}: {joined}")


def _slug(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def _severity_name(severity: int) -> str:
    return {
        0: "none_or_unknown",
        1: "minor",
        2: "moderate",
        3: "major",
    }.get(severity, "unknown")
