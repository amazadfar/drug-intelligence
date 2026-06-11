"""Knowledge graph validation rules."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from drug_intelligence.graph.schema import REQUIRED_NODE_PROPERTIES, KGGraph


@dataclass(frozen=True)
class GraphValidationIssue:
    scope: str
    identifier: str
    message: str


def validate_graph(graph: KGGraph) -> list[GraphValidationIssue]:
    issues: list[GraphValidationIssue] = []
    node_ids = [node.id for node in graph.nodes]
    relationship_ids = [relationship.id for relationship in graph.relationships]

    for node_id, count in Counter(node_ids).items():
        if count > 1:
            issues.append(GraphValidationIssue("node", node_id, "Duplicate node ID."))

    for relationship_id, count in Counter(relationship_ids).items():
        if count > 1:
            issues.append(
                GraphValidationIssue("relationship", relationship_id, "Duplicate relationship ID.")
            )

    node_by_id = graph.node_by_id()
    for node in graph.nodes:
        if not node.labels:
            issues.append(GraphValidationIssue("node", node.id, "Node has no labels."))
            continue
        missing = [
            prop
            for prop in REQUIRED_NODE_PROPERTIES[node.primary_label()]
            if prop not in node.properties or node.properties[prop] in {None, ""}
        ]
        for prop in missing:
            issues.append(
                GraphValidationIssue(
                    "node",
                    node.id,
                    f"Missing required property {prop!r}.",
                )
            )

    for relationship in graph.relationships:
        if relationship.source_id not in node_by_id:
            issues.append(
                GraphValidationIssue(
                    "relationship",
                    relationship.id,
                    f"Missing source node {relationship.source_id!r}.",
                )
            )
        if relationship.target_id not in node_by_id:
            issues.append(
                GraphValidationIssue(
                    "relationship",
                    relationship.id,
                    f"Missing target node {relationship.target_id!r}.",
                )
            )
        if "source" not in relationship.properties:
            issues.append(
                GraphValidationIssue(
                    "relationship",
                    relationship.id,
                    "Missing provenance property 'source'.",
                )
            )

    return issues
