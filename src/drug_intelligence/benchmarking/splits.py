"""Deterministic pair-level split strategies."""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class PairExample:
    drug_id_a: str
    drug_id_b: str
    mechanism_targets: tuple[float, ...]
    severity_targets: tuple[int, ...]


@dataclass(frozen=True)
class SplitIndices:
    train: tuple[int, ...]
    validation: tuple[int, ...]
    test: tuple[int, ...]
    dropped: tuple[int, ...] = ()


def split_pairs(
    pairs: list[PairExample],
    strategy: str = "random",
    validation_fraction: float = 0.2,
    test_fraction: float = 0.2,
    seed: int = 42,
    group_by_drug: dict[str, str] | None = None,
) -> SplitIndices:
    if not pairs:
        raise ValueError("At least one pair is required.")
    _validate_fractions(validation_fraction, test_fraction)

    if strategy == "random":
        return _random_split(pairs, validation_fraction, test_fraction, seed)
    if strategy in {"drug_disjoint", "scaffold_disjoint"}:
        groups = (
            {drug_id: drug_id for pair in pairs for drug_id in (pair.drug_id_a, pair.drug_id_b)}
            if strategy == "drug_disjoint"
            else group_by_drug
        )
        if groups is None:
            raise ValueError("scaffold_disjoint requires group_by_drug.")
        return _group_disjoint_split(
            pairs,
            groups,
            validation_fraction,
            test_fraction,
            seed,
        )
    raise ValueError(f"Unsupported split strategy {strategy!r}.")


def murcko_scaffold_groups(smiles_by_drug: dict[str, str]) -> dict[str, str]:
    """Map drug IDs to Bemis-Murcko scaffold SMILES for scaffold splits."""

    try:
        from rdkit.Chem.Scaffolds import MurckoScaffold
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "RDKit is required for scaffold grouping. Install `.[chem]`."
        ) from exc

    groups: dict[str, str] = {}
    for drug_id, smiles in smiles_by_drug.items():
        scaffold = MurckoScaffold.MurckoScaffoldSmiles(
            smiles=smiles,
            includeChirality=True,
        )
        groups[drug_id] = scaffold or f"acyclic:{drug_id}"
    return groups


def _random_split(
    pairs: list[PairExample],
    validation_fraction: float,
    test_fraction: float,
    seed: int,
) -> SplitIndices:
    indices = list(range(len(pairs)))
    random.Random(seed).shuffle(indices)
    test_count = max(1, round(len(indices) * test_fraction))
    validation_count = max(1, round(len(indices) * validation_fraction))
    test = indices[:test_count]
    validation = indices[test_count : test_count + validation_count]
    train = indices[test_count + validation_count :]
    if not train:
        raise ValueError("Split fractions leave no training examples.")
    return SplitIndices(tuple(train), tuple(validation), tuple(test))


def _group_disjoint_split(
    pairs: list[PairExample],
    group_by_drug: dict[str, str],
    validation_fraction: float,
    test_fraction: float,
    seed: int,
) -> SplitIndices:
    unique_groups = sorted(set(group_by_drug.values()))
    random.Random(seed).shuffle(unique_groups)
    test_count = max(1, round(len(unique_groups) * test_fraction))
    validation_count = max(1, round(len(unique_groups) * validation_fraction))
    test_groups = set(unique_groups[:test_count])
    validation_groups = set(unique_groups[test_count : test_count + validation_count])
    train_groups = set(unique_groups[test_count + validation_count :])

    partitions = {
        "train": train_groups,
        "validation": validation_groups,
        "test": test_groups,
    }
    assigned: dict[str, list[int]] = {name: [] for name in partitions}
    dropped: list[int] = []

    for index, pair in enumerate(pairs):
        group_a = group_by_drug[pair.drug_id_a]
        group_b = group_by_drug[pair.drug_id_b]
        partition = next(
            (
                name
                for name, groups in partitions.items()
                if group_a in groups and group_b in groups
            ),
            None,
        )
        if partition is None:
            dropped.append(index)
        else:
            assigned[partition].append(index)

    if not all(assigned.values()):
        raise ValueError(
            "Disjoint split produced an empty partition. Add more groups or "
            "adjust split fractions."
        )
    return SplitIndices(
        tuple(assigned["train"]),
        tuple(assigned["validation"]),
        tuple(assigned["test"]),
        tuple(dropped),
    )


def _validate_fractions(validation_fraction: float, test_fraction: float) -> None:
    if validation_fraction <= 0 or test_fraction <= 0:
        raise ValueError("Validation and test fractions must be positive.")
    if validation_fraction + test_fraction >= 1:
        raise ValueError("Validation and test fractions must sum to less than one.")
