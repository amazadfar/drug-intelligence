from pathlib import Path

from drug_intelligence.graph import (
    RelationshipType,
    build_fixture_knowledge_graph,
    export_cypher,
    export_json,
    validate_graph,
)

ROOT = Path(__file__).resolve().parents[1]


def _graph():
    return build_fixture_knowledge_graph(
        ROOT / "examples" / "sample_drugs.jsonl",
        ROOT / "examples" / "sample_interactions.jsonl",
        ROOT / "examples" / "sample_references.jsonl",
    )


def test_fixture_knowledge_graph_is_valid_and_provenance_aware() -> None:
    graph = _graph()

    assert validate_graph(graph) == []
    assert graph.metadata["drugs"] == 10
    assert graph.metadata["interactions"] == 1
    assert graph.metadata["references"] == 1
    assert {relationship.relationship_type for relationship in graph.relationships} >= {
        RelationshipType.DERIVED_FROM,
        RelationshipType.HAS_MOLECULAR_FEATURE,
        RelationshipType.HAS_TYPE,
        RelationshipType.INVOLVES,
        RelationshipType.HAS_MECHANISM,
        RelationshipType.HAS_SEVERITY,
        RelationshipType.SUPPORTED_BY,
    }
    assert all("source" in relationship.properties for relationship in graph.relationships)


def test_exported_cypher_contains_constraints_and_queries(tmp_path: Path) -> None:
    graph = _graph()
    output = tmp_path / "sample-kg.cypher"

    export_cypher(graph, output)

    text = output.read_text()
    assert "CREATE CONSTRAINT drug_id_unique IF NOT EXISTS" in text
    assert "MERGE (n:Drug {id:" in text
    assert "MERGE (source)-[r:INVOLVES" in text
    assert "MERGE (source)-[r:SUPPORTED_BY" in text
    assert "Trace provenance" in text


def test_exported_json_preserves_graph_shape(tmp_path: Path) -> None:
    graph = _graph()
    output = tmp_path / "sample-kg.json"

    export_json(graph, output)

    text = output.read_text()
    assert '"nodes"' in text
    assert '"relationships"' in text
    assert '"SUPPORTED_BY"' in text
