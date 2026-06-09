"""Public-safe schema contracts for drug intelligence workflows.

The schemas in this module are intentionally small and dependency-free. They
define the records that public fixtures, importers, feature extractors, and
future model pipelines should exchange.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

MECHANISM_LABELS: tuple[str, ...] = (
    "metabolism",
    "synergy",
    "antagonism",
    "distribution",
    "excretion",
    "absorption",
    "other",
)

SEVERITY_LABELS: dict[int, str] = {
    0: "none_or_unknown",
    1: "minor",
    2: "moderate",
    3: "major",
}


@dataclass(frozen=True)
class ValidationIssue:
    """A validation finding that can be surfaced without raising immediately."""

    field: str
    message: str


@dataclass(frozen=True)
class DrugRecord:
    """Minimal public-safe drug entity contract."""

    drug_id: str
    name: str
    normalized_name: str | None = None
    smiles: str | None = None
    inchi: str | None = None
    drug_type: str | None = None
    description: str | None = None
    source: str = "synthetic"
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if not self.drug_id.strip():
            issues.append(ValidationIssue("drug_id", "Drug ID is required."))
        if not self.name.strip():
            issues.append(ValidationIssue("name", "Drug name is required."))
        if not self.smiles and not self.inchi:
            issues.append(
                ValidationIssue("smiles", "At least one molecular representation is required.")
            )
        return issues


@dataclass(frozen=True)
class InteractionRecord:
    """Drug-pair interaction contract for public fixtures and model inputs."""

    interaction_id: str
    drug_id_a: str
    drug_id_b: str
    mechanism_labels: tuple[str, ...] = ()
    severity_by_mechanism: dict[str, int] = field(default_factory=dict)
    evidence: str | None = None
    source: str = "synthetic"
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if not self.interaction_id.strip():
            issues.append(ValidationIssue("interaction_id", "Interaction ID is required."))
        if not self.drug_id_a.strip():
            issues.append(ValidationIssue("drug_id_a", "First drug ID is required."))
        if not self.drug_id_b.strip():
            issues.append(ValidationIssue("drug_id_b", "Second drug ID is required."))
        if self.drug_id_a == self.drug_id_b:
            issues.append(ValidationIssue("drug_id_b", "Interaction pair must contain two drugs."))

        unknown_mechanisms = sorted(set(self.mechanism_labels) - set(MECHANISM_LABELS))
        if unknown_mechanisms:
            issues.append(
                ValidationIssue(
                    "mechanism_labels",
                    f"Unknown mechanism labels: {', '.join(unknown_mechanisms)}.",
                )
            )

        for mechanism, severity in self.severity_by_mechanism.items():
            if mechanism not in MECHANISM_LABELS:
                issues.append(
                    ValidationIssue(
                        "severity_by_mechanism",
                        f"Unknown severity mechanism: {mechanism}.",
                    )
                )
            if severity not in SEVERITY_LABELS:
                issues.append(
                    ValidationIssue(
                        "severity_by_mechanism",
                        f"Invalid severity {severity!r} for mechanism {mechanism}.",
                    )
                )
        return issues


@dataclass(frozen=True)
class ReferenceRecord:
    """Evidence/reference metadata contract."""

    reference_id: str
    title: str
    url: str | None = None
    abstract: str | None = None
    source: str = "synthetic"
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if not self.reference_id.strip():
            issues.append(ValidationIssue("reference_id", "Reference ID is required."))
        if not self.title.strip():
            issues.append(ValidationIssue("title", "Reference title is required."))
        return issues


@dataclass(frozen=True)
class MolecularFeatureRecord:
    """Serializable chemistry feature contract.

    `node_features`, `edge_index`, `edge_features`, and `global_features` are
    intentionally Python-native lists so the public data layer does not require
    PyTorch or Torch Geometric.
    """

    drug_id: str
    representation: str
    representation_type: str
    node_features: list[dict[str, Any]]
    edge_index: list[tuple[int, int]]
    edge_features: list[dict[str, Any]]
    global_features: dict[str, Any]
    warnings: tuple[str, ...] = ()

    def validate(self) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if not self.drug_id.strip():
            issues.append(ValidationIssue("drug_id", "Drug ID is required."))
        if self.representation_type not in {"smiles", "inchi"}:
            issues.append(
                ValidationIssue(
                    "representation_type",
                    "Representation type must be either 'smiles' or 'inchi'.",
                )
            )
        if not self.node_features:
            issues.append(ValidationIssue("node_features", "At least one atom node is required."))
        if len(self.edge_index) != len(self.edge_features):
            issues.append(
                ValidationIssue(
                    "edge_features",
                    "Edge index and edge feature lengths must match.",
                )
            )
        return issues
