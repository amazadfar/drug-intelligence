from drug_intelligence.benchmarking import PairExample, split_pairs


def _pairs() -> list[PairExample]:
    drug_ids = [f"drug-{index}" for index in range(10)]
    return [
        PairExample(a, b, (1.0,), (1,))
        for index, a in enumerate(drug_ids)
        for b in drug_ids[index + 1 :]
    ]


def test_random_split_is_deterministic() -> None:
    first = split_pairs(_pairs(), strategy="random", seed=7)
    second = split_pairs(_pairs(), strategy="random", seed=7)

    assert first == second
    assert set(first.train).isdisjoint(first.validation)
    assert set(first.train).isdisjoint(first.test)
    assert set(first.validation).isdisjoint(first.test)


def test_drug_disjoint_split_has_no_cross_partition_drugs() -> None:
    pairs = _pairs()
    split = split_pairs(pairs, strategy="drug_disjoint", seed=7)

    partition_drugs = {
        name: {
            drug_id
            for index in indices
            for drug_id in (pairs[index].drug_id_a, pairs[index].drug_id_b)
        }
        for name, indices in {
            "train": split.train,
            "validation": split.validation,
            "test": split.test,
        }.items()
    }

    assert partition_drugs["train"].isdisjoint(partition_drugs["validation"])
    assert partition_drugs["train"].isdisjoint(partition_drugs["test"])
    assert partition_drugs["validation"].isdisjoint(partition_drugs["test"])
    assert split.dropped
