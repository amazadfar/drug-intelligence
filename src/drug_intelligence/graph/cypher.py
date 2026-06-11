"""Export framework-neutral KG records to JSON and Neo4j Cypher."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from drug_intelligence.graph.schema import NODE_UNIQUE_KEYS, KGGraph, KGNode, KGRelationship
from drug_intelligence.graph.validation import validate_graph


def export_json(graph: KGGraph, output_path: Path) -> None:
    _raise_if_invalid(graph)
    payload = {
        "metadata": graph.metadata,
        "nodes": [
            {
                "id": node.id,
                "labels": [label.value for label in node.labels],
                "properties": node.properties,
            }
            for node in graph.nodes
        ],
        "relationships": [
            {
                "id": relationship.id,
                "source_id": relationship.source_id,
                "target_id": relationship.target_id,
                "type": relationship.relationship_type.value,
                "properties": relationship.properties,
            }
            for relationship in graph.relationships
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def export_cypher(graph: KGGraph, output_path: Path) -> None:
    _raise_if_invalid(graph)
    sections = [
        _render_constraints(),
        _render_nodes(graph.nodes),
        _render_relationships(graph.relationships),
        _render_sample_queries(),
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n\n".join(sections) + "\n")


def _render_constraints() -> str:
    lines = ["// Uniqueness constraints"]
    for label, prop in NODE_UNIQUE_KEYS.items():
        lines.append(
            f"CREATE CONSTRAINT {label.value.lower()}_{prop}_unique IF NOT EXISTS "
            f"FOR (n:{label.value}) REQUIRE n.{prop} IS UNIQUE;"
        )
    return "\n".join(lines)


def _render_nodes(nodes: tuple[KGNode, ...]) -> str:
    lines = ["// Nodes"]
    for node in sorted(nodes, key=lambda item: item.id):
        labels = ":".join(label.value for label in node.labels)
        lines.append(
            f"MERGE (n:{labels} {{id: {_cypher_value(node.id)}}})\n"
            f"SET n += {_cypher_map(node.properties)};"
        )
    return "\n".join(lines)


def _render_relationships(relationships: tuple[KGRelationship, ...]) -> str:
    lines = ["// Relationships"]
    for relationship in sorted(relationships, key=lambda item: item.id):
        lines.append(
            f"MATCH (source {{id: {_cypher_value(relationship.source_id)}}})\n"
            f"MATCH (target {{id: {_cypher_value(relationship.target_id)}}})\n"
            f"MERGE (source)-[r:{relationship.relationship_type.value} "
            f"{{id: {_cypher_value(relationship.id)}}}]->(target)\n"
            f"SET r += {_cypher_map({'id': relationship.id, **relationship.properties})};"
        )
    return "\n".join(lines)


def _render_sample_queries() -> str:
    return """// Sample queries
// List synthetic drug interactions with mechanisms and severities.
MATCH (interaction:Interaction)-[:INVOLVES]->(drug:Drug)
OPTIONAL MATCH (interaction)-[:HAS_MECHANISM]->(mechanism:Mechanism)
OPTIONAL MATCH (interaction)-[severityRel:HAS_SEVERITY]->(severity:Severity)
RETURN interaction.id AS interaction_id,
       collect(DISTINCT drug.name) AS drugs,
       collect(DISTINCT mechanism.name) AS mechanisms,
       collect(DISTINCT {mechanism: severityRel.mechanism, severity: severity.name}) AS severities;

// Trace provenance for interaction facts.
MATCH (interaction:Interaction)-[:DERIVED_FROM]->(source:Source)
RETURN interaction.id AS interaction_id, source.name AS source;"""


def _cypher_map(properties: dict[str, Any]) -> str:
    pairs = [
        f"{_cypher_key(key)}: {_cypher_value(value)}"
        for key, value in sorted(properties.items())
        if value is not None
    ]
    return "{" + ", ".join(pairs) + "}"


def _cypher_key(key: str) -> str:
    if key.isidentifier():
        return key
    return f"`{key.replace('`', '``')}`"


def _cypher_value(value: Any) -> str:
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, int | float):
        return str(value)
    if isinstance(value, list | tuple):
        return "[" + ", ".join(_cypher_value(item) for item in value) + "]"
    if isinstance(value, dict):
        return _cypher_map(value)
    raise TypeError(f"Unsupported Cypher value type: {type(value).__name__}")


def _raise_if_invalid(graph: KGGraph) -> None:
    issues = validate_graph(graph)
    if issues:
        joined = "; ".join(f"{issue.scope}:{issue.identifier}:{issue.message}" for issue in issues)
        raise ValueError(f"Cannot export invalid graph: {joined}")
