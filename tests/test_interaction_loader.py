from pathlib import Path

from drug_intelligence.benchmarking.sample_dataset import load_interaction_pairs

ROOT = Path(__file__).resolve().parents[1]


def test_interaction_loader_maps_public_schema_to_targets() -> None:
    pairs = load_interaction_pairs(ROOT / "examples" / "sample_interactions.jsonl")

    assert len(pairs) == 1
    assert pairs[0].mechanism_targets[0] == 1.0
    assert pairs[0].severity_targets[0] == 1
    assert sum(pairs[0].mechanism_targets) == 1.0
