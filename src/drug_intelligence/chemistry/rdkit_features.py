"""RDKit-backed molecular feature extraction.

This module is optional at import time. RDKit is only required when feature
extraction is executed, which keeps the base public package lightweight.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from drug_intelligence.data import MolecularFeatureRecord


class RDKitUnavailableError(RuntimeError):
    """Raised when RDKit-backed features are requested without RDKit installed."""


def _load_rdkit() -> dict[str, Any]:
    try:
        from rdkit import Chem, RDLogger
        from rdkit.Chem import AllChem, Crippen, Descriptors, Lipinski, rdMolDescriptors
    except ImportError as exc:  # pragma: no cover - covered by environments without RDKit
        raise RDKitUnavailableError(
            "RDKit is required for chemistry feature extraction. "
            "Install the chemistry extra with `pip install -e '.[chem]'`."
        ) from exc

    RDLogger.DisableLog("rdApp.*")
    return {
        "AllChem": AllChem,
        "Chem": Chem,
        "Crippen": Crippen,
        "Descriptors": Descriptors,
        "Lipinski": Lipinski,
        "rdMolDescriptors": rdMolDescriptors,
    }


class RDKitFeatureExtractor:
    """Extract atom, bond, and global molecular features into public schemas."""

    def __init__(self, add_hydrogens: bool = True, optimize_geometry: bool = True) -> None:
        self.add_hydrogens = add_hydrogens
        self.optimize_geometry = optimize_geometry

    def from_smiles(self, drug_id: str, smiles: str) -> MolecularFeatureRecord:
        rdkit = _load_rdkit()
        mol = rdkit["Chem"].MolFromSmiles(smiles)
        return self._record_from_mol(
            drug_id=drug_id,
            representation=smiles,
            representation_type="smiles",
            mol=mol,
            rdkit=rdkit,
        )

    def from_inchi(self, drug_id: str, inchi: str) -> MolecularFeatureRecord:
        rdkit = _load_rdkit()
        mol = rdkit["Chem"].MolFromInchi(inchi)
        return self._record_from_mol(
            drug_id=drug_id,
            representation=inchi,
            representation_type="inchi",
            mol=mol,
            rdkit=rdkit,
        )

    def _record_from_mol(
        self,
        drug_id: str,
        representation: str,
        representation_type: str,
        mol: Any,
        rdkit: dict[str, Any],
    ) -> MolecularFeatureRecord:
        warnings: list[str] = []
        if mol is None:
            return MolecularFeatureRecord(
                drug_id=drug_id,
                representation=representation,
                representation_type=representation_type,
                node_features=[],
                edge_index=[],
                edge_features=[],
                global_features={},
                warnings=("invalid molecular representation",),
            )

        if self.add_hydrogens:
            mol = rdkit["Chem"].AddHs(mol)

        try:
            rdkit["AllChem"].ComputeGasteigerCharges(mol)
        except Exception:  # pragma: no cover - RDKit-dependent edge case
            warnings.append("failed to compute gasteiger charges")

        try:
            rdkit["AllChem"].Compute2DCoords(mol)
            rdkit["AllChem"].EmbedMolecule(mol)
        except Exception:  # pragma: no cover - RDKit-dependent edge case
            warnings.append("failed to embed molecule")

        if self.optimize_geometry:
            try:
                rdkit["AllChem"].UFFOptimizeMolecule(mol)
            except Exception:  # pragma: no cover - RDKit-dependent edge case
                warnings.append("failed to optimize geometry")

        node_features = [self._atom_features(atom) for atom in mol.GetAtoms()]
        edge_index, edge_features = self._bond_features(mol)
        global_features = self._global_features(mol, node_features, rdkit)

        return MolecularFeatureRecord(
            drug_id=drug_id,
            representation=representation,
            representation_type=representation_type,
            node_features=node_features,
            edge_index=edge_index,
            edge_features=edge_features,
            global_features=global_features,
            warnings=tuple(warnings),
        )

    @staticmethod
    def _atom_features(atom: Any) -> dict[str, Any]:
        charge = atom.GetProp("_GasteigerCharge") if atom.HasProp("_GasteigerCharge") else "nan"
        try:
            charge_value = float(charge)
        except ValueError:
            charge_value = None

        return {
            "symbol": atom.GetSymbol(),
            "atomic_number": atom.GetAtomicNum(),
            "atomic_mass": atom.GetMass(),
            "formal_charge": atom.GetFormalCharge(),
            "hybridization": str(atom.GetHybridization()),
            "explicit_valence": atom.GetExplicitValence(),
            "implicit_valence": atom.GetImplicitValence(),
            "degree": atom.GetDegree(),
            "num_explicit_hydrogens": atom.GetNumExplicitHs(),
            "num_implicit_hydrogens": atom.GetNumImplicitHs(),
            "num_radical_electrons": atom.GetNumRadicalElectrons(),
            "is_aromatic": atom.GetIsAromatic(),
            "is_in_ring": atom.IsInRing(),
            "is_chiral_center": atom.GetChiralTag().name != "CHI_UNSPECIFIED",
            "gasteiger_charge": charge_value,
        }

    @staticmethod
    def _bond_features(mol: Any) -> tuple[list[tuple[int, int]], list[dict[str, Any]]]:
        edge_index: list[tuple[int, int]] = []
        edge_features: list[dict[str, Any]] = []

        for bond in mol.GetBonds():
            begin_idx = bond.GetBeginAtomIdx()
            end_idx = bond.GetEndAtomIdx()
            features = {
                "bond_type": bond.GetBondTypeAsDouble(),
                "is_conjugated": bond.GetIsConjugated(),
                "is_in_ring": bond.IsInRing(),
            }

            edge_index.append((begin_idx, end_idx))
            edge_features.append(features)
            edge_index.append((end_idx, begin_idx))
            edge_features.append(features.copy())

        return edge_index, edge_features

    @staticmethod
    def _global_features(
        mol: Any,
        node_features: list[dict[str, Any]],
        rdkit: dict[str, Any],
    ) -> dict[str, Any]:
        symbols = Counter(node["symbol"] for node in node_features)
        return {
            "num_atoms": mol.GetNumAtoms(),
            "formula": rdkit["rdMolDescriptors"].CalcMolFormula(mol),
            "exact_molecular_weight": rdkit["rdMolDescriptors"].CalcExactMolWt(mol),
            "logp": rdkit["Crippen"].MolLogP(mol),
            "topological_polar_surface_area": rdkit["Descriptors"].TPSA(mol),
            "rotatable_bonds": rdkit["Descriptors"].NumRotatableBonds(mol),
            "hydrogen_bond_donors": rdkit["Lipinski"].NumHDonors(mol),
            "hydrogen_bond_acceptors": rdkit["Lipinski"].NumHAcceptors(mol),
            "fraction_csp3": rdkit["Descriptors"].FractionCSP3(mol),
            "num_rings": rdkit["rdMolDescriptors"].CalcNumRings(mol),
            "aromatic_rings": rdkit["rdMolDescriptors"].CalcNumAromaticRings(mol),
            "aliphatic_rings": rdkit["rdMolDescriptors"].CalcNumAliphaticRings(mol),
            "element_counts": dict(symbols),
        }
