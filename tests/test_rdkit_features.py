import pytest

from drug_intelligence.chemistry import RDKitFeatureExtractor

pytest.importorskip("rdkit")


def test_rdkit_feature_extractor_builds_bidirectional_bond_features() -> None:
    record = RDKitFeatureExtractor(add_hydrogens=False, optimize_geometry=False).from_smiles(
        drug_id="ethanol",
        smiles="CCO",
    )

    assert record.validate() == []
    assert record.global_features["num_atoms"] == 3
    assert len(record.node_features) == 3
    assert len(record.edge_index) == 4
    assert len(record.edge_features) == 4
    assert record.warnings == ()
