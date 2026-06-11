"""Knowledge graph primitives for the public biomedical graph layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class NodeLabel(StrEnum):
    DRUG = "Drug"
    DRUG_TYPE = "DrugType"
    INTERACTION = "Interaction"
    MECHANISM = "Mechanism"
    SEVERITY = "Severity"
    REFERENCE = "Reference"
    MOLECULE_FEATURE = "MoleculeFeature"
    SOURCE = "Source"


class RelationshipType(StrEnum):
    DERIVED_FROM = "DERIVED_FROM"
    HAS_TYPE = "HAS_TYPE"
    HAS_MOLECULAR_FEATURE = "HAS_MOLECULAR_FEATURE"
    INVOLVES = "INVOLVES"
    HAS_MECHANISM = "HAS_MECHANISM"
    HAS_SEVERITY = "HAS_SEVERITY"
    SUPPORTED_BY = "SUPPORTED_BY"


NODE_LABEL_DESCRIPTIONS: dict[NodeLabel, str] = {
    NodeLabel.DRUG: "Drug or molecule entity.",
    NodeLabel.DRUG_TYPE: "Public-safe type/category grouping.",
    NodeLabel.INTERACTION: "Drug-pair interaction assertion or prediction target.",
    NodeLabel.MECHANISM: "Interaction mechanism label.",
    NodeLabel.SEVERITY: "Severity level for a mechanism or interaction assertion.",
    NodeLabel.REFERENCE: "Evidence or citation metadata.",
    NodeLabel.MOLECULE_FEATURE: "Molecular representation or feature summary.",
    NodeLabel.SOURCE: "Dataset, fixture, importer, or provenance source.",
}

RELATIONSHIP_DESCRIPTIONS: dict[RelationshipType, str] = {
    RelationshipType.DERIVED_FROM: "Connects graph facts to their source/provenance.",
    RelationshipType.HAS_TYPE: "Connects a drug to a type/category node.",
    RelationshipType.HAS_MOLECULAR_FEATURE: "Connects a drug to molecular representation data.",
    RelationshipType.INVOLVES: "Connects an interaction to participating drugs.",
    RelationshipType.HAS_MECHANISM: "Connects an interaction to mechanism labels.",
    RelationshipType.HAS_SEVERITY: "Connects an interaction to severity labels.",
    RelationshipType.SUPPORTED_BY: "Connects an interaction to evidence/reference records.",
}

NODE_UNIQUE_KEYS: dict[NodeLabel, str] = {
    label: "id" for label in NodeLabel
}

REQUIRED_NODE_PROPERTIES: dict[NodeLabel, tuple[str, ...]] = {
    NodeLabel.DRUG: ("id", "name", "source"),
    NodeLabel.DRUG_TYPE: ("id", "name", "source"),
    NodeLabel.INTERACTION: ("id", "source"),
    NodeLabel.MECHANISM: ("id", "name", "source"),
    NodeLabel.SEVERITY: ("id", "level", "name", "source"),
    NodeLabel.REFERENCE: ("id", "title", "source"),
    NodeLabel.MOLECULE_FEATURE: ("id", "representation", "representation_type", "source"),
    NodeLabel.SOURCE: ("id", "name"),
}


@dataclass(frozen=True)
class KGNode:
    """A provenance-aware knowledge graph node."""

    id: str
    labels: tuple[NodeLabel, ...]
    properties: dict[str, Any]

    def primary_label(self) -> NodeLabel:
        if not self.labels:
            raise ValueError(f"Node {self.id!r} has no labels.")
        return self.labels[0]


@dataclass(frozen=True)
class KGRelationship:
    """A typed relationship between two graph nodes."""

    id: str
    source_id: str
    target_id: str
    relationship_type: RelationshipType
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class KGGraph:
    """A framework-neutral knowledge graph container."""

    nodes: tuple[KGNode, ...]
    relationships: tuple[KGRelationship, ...]
    metadata: dict[str, Any] = field(default_factory=dict)

    def node_by_id(self) -> dict[str, KGNode]:
        return {node.id: node for node in self.nodes}
