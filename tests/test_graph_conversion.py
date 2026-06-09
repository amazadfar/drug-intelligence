from drug_intelligence.chemistry import to_graph_tensor_spec
from drug_intelligence.data import MolecularFeatureRecord


def test_graph_conversion_creates_framework_neutral_arrays() -> None:
    record = MolecularFeatureRecord(
        drug_id="drug-a",
        representation="CC",
        representation_type="smiles",
        node_features=[
            {"atomic_number": 6, "is_aromatic": False},
            {"atomic_number": 6, "is_aromatic": False},
        ],
        edge_index=[(0, 1), (1, 0)],
        edge_features=[
            {"bond_type": 1.0, "is_conjugated": False},
            {"bond_type": 1.0, "is_conjugated": False},
        ],
        global_features={"num_atoms": 2, "logp": 1.1},
    )

    graph = to_graph_tensor_spec(
        record,
        node_feature_names=("atomic_number", "is_aromatic"),
        edge_feature_names=("bond_type", "is_conjugated"),
        global_feature_names=("num_atoms", "logp"),
    )

    assert graph.x == [[6.0, 0.0], [6.0, 0.0]]
    assert graph.edge_index == [(0, 1), (1, 0)]
    assert graph.edge_attr == [[1.0, 0.0], [1.0, 0.0]]
    assert graph.u == [2.0, 1.1]
