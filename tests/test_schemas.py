from drug_intelligence.data import DrugRecord, InteractionRecord, MolecularFeatureRecord


def test_drug_record_requires_identity_and_representation() -> None:
    record = DrugRecord(drug_id="", name="", smiles=None, inchi=None)

    issues = record.validate()

    assert {issue.field for issue in issues} == {"drug_id", "name", "smiles"}


def test_interaction_record_validates_mechanism_and_severity() -> None:
    record = InteractionRecord(
        interaction_id="int-1",
        drug_id_a="drug-a",
        drug_id_b="drug-b",
        mechanism_labels=("metabolism", "unknown-mechanism"),
        severity_by_mechanism={"metabolism": 2, "absorption": 7},
    )

    issues = record.validate()

    assert len(issues) == 2
    assert all(issue.field in {"mechanism_labels", "severity_by_mechanism"} for issue in issues)


def test_molecular_feature_record_requires_matching_edge_lengths() -> None:
    record = MolecularFeatureRecord(
        drug_id="drug-a",
        representation="CCO",
        representation_type="smiles",
        node_features=[{"atomic_number": 6}],
        edge_index=[(0, 1), (1, 0)],
        edge_features=[{"bond_type": 1.0}],
        global_features={"num_atoms": 2},
    )

    issues = record.validate()

    assert len(issues) == 1
    assert issues[0].field == "edge_features"
