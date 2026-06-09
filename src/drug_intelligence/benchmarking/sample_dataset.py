"""Build a deterministic synthetic benchmark from public molecule fixtures."""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
from typing import Any

from drug_intelligence.benchmarking.splits import PairExample
from drug_intelligence.chemistry import RDKitFeatureExtractor, to_graph_tensor_spec
from drug_intelligence.data import MECHANISM_LABELS, InteractionRecord

NODE_FEATURES = (
    "atomic_number",
    "atomic_mass",
    "formal_charge",
    "degree",
    "is_aromatic",
    "is_in_ring",
)
EDGE_FEATURES = ("bond_type", "is_conjugated", "is_in_ring")
GLOBAL_FEATURES = (
    "exact_molecular_weight",
    "logp",
    "topological_polar_surface_area",
    "rotatable_bonds",
)


def build_graphs_from_jsonl(fixtures_path: Path) -> dict[str, Any]:
    import torch
    from torch_geometric.data import Data

    extractor = RDKitFeatureExtractor(add_hydrogens=False, optimize_geometry=False)
    drugs = [
        json.loads(line)
        for line in fixtures_path.read_text().splitlines()
        if line.strip()
    ]
    graphs: dict[str, Any] = {}
    for drug in drugs:
        record = extractor.from_smiles(drug["drug_id"], drug["smiles"])
        graph = to_graph_tensor_spec(
            record,
            node_feature_names=NODE_FEATURES,
            edge_feature_names=EDGE_FEATURES,
            global_feature_names=GLOBAL_FEATURES,
        )
        edge_index = torch.tensor(graph.edge_index, dtype=torch.long).t().contiguous()
        graphs[drug["drug_id"]] = Data(
            x=torch.tensor(graph.x, dtype=torch.float32),
            edge_index=edge_index,
            edge_attr=torch.tensor(graph.edge_attr, dtype=torch.float32),
            u=torch.tensor([graph.u], dtype=torch.float32),
            drug_id=drug["drug_id"],
        )
    return graphs


def load_interaction_pairs(interactions_path: Path) -> list[PairExample]:
    """Load validated interaction records into benchmark targets."""

    rows = [
        json.loads(line)
        for line in interactions_path.read_text().splitlines()
        if line.strip()
    ]
    pairs: list[PairExample] = []
    for row in rows:
        record = InteractionRecord(
            interaction_id=row["interaction_id"],
            drug_id_a=row["drug_id_a"],
            drug_id_b=row["drug_id_b"],
            mechanism_labels=tuple(row.get("mechanism_labels", [])),
            severity_by_mechanism=row.get("severity_by_mechanism", {}),
            evidence=row.get("evidence"),
            source=row.get("source", "user_provided"),
            metadata=row.get("metadata", {}),
        )
        issues = record.validate()
        if issues:
            joined = "; ".join(f"{issue.field}: {issue.message}" for issue in issues)
            raise ValueError(f"Invalid interaction {record.interaction_id}: {joined}")
        mechanism_targets = tuple(
            1.0 if mechanism in record.mechanism_labels else 0.0
            for mechanism in MECHANISM_LABELS
        )
        severity_targets = tuple(
            record.severity_by_mechanism.get(mechanism, 0)
            for mechanism in MECHANISM_LABELS
        )
        pairs.append(
            PairExample(
                drug_id_a=record.drug_id_a,
                drug_id_b=record.drug_id_b,
                mechanism_targets=mechanism_targets,
                severity_targets=severity_targets,
            )
        )
    return pairs


build_sample_graphs = build_graphs_from_jsonl


def build_sample_pairs(drug_ids: list[str]) -> list[PairExample]:
    pairs: list[PairExample] = []
    for pair_index, (drug_id_a, drug_id_b) in enumerate(combinations(drug_ids, 2)):
        primary_mechanism = pair_index % len(MECHANISM_LABELS)
        secondary_mechanism = (
            (pair_index + 3) % len(MECHANISM_LABELS)
            if pair_index % 4 == 0
            else None
        )
        mechanism_targets = [0.0] * len(MECHANISM_LABELS)
        severity_targets = [0] * len(MECHANISM_LABELS)
        mechanism_targets[primary_mechanism] = 1.0
        severity_targets[primary_mechanism] = 1 + pair_index % 3
        if secondary_mechanism is not None:
            mechanism_targets[secondary_mechanism] = 1.0
            severity_targets[secondary_mechanism] = 1 + (pair_index + 1) % 3
        pairs.append(
            PairExample(
                drug_id_a=drug_id_a,
                drug_id_b=drug_id_b,
                mechanism_targets=tuple(mechanism_targets),
                severity_targets=tuple(severity_targets),
            )
        )
    return pairs
