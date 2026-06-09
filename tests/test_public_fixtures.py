import json
from pathlib import Path

from drug_intelligence.data import DrugRecord, InteractionRecord, ReferenceRecord

ROOT = Path(__file__).resolve().parents[1]


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def test_public_drug_fixtures_are_valid() -> None:
    rows = _read_jsonl(ROOT / "examples" / "sample_drugs.jsonl")

    records = [DrugRecord(**row) for row in rows]

    assert len(records) == 2
    assert all(record.source == "synthetic" for record in records)
    assert all(record.validate() == [] for record in records)


def test_public_interaction_fixtures_are_valid() -> None:
    rows = _read_jsonl(ROOT / "examples" / "sample_interactions.jsonl")

    records = [
        InteractionRecord(
            interaction_id=row["interaction_id"],
            drug_id_a=row["drug_id_a"],
            drug_id_b=row["drug_id_b"],
            mechanism_labels=tuple(row["mechanism_labels"]),
            severity_by_mechanism=row["severity_by_mechanism"],
            evidence=row["evidence"],
            source=row["source"],
        )
        for row in rows
    ]

    assert len(records) == 1
    assert records[0].source == "synthetic"
    assert records[0].validate() == []


def test_public_reference_fixtures_are_valid() -> None:
    rows = _read_jsonl(ROOT / "examples" / "sample_references.jsonl")

    records = [ReferenceRecord(**row) for row in rows]

    assert len(records) == 1
    assert records[0].source == "synthetic"
    assert records[0].validate() == []
