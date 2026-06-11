"""Export the public fixture knowledge graph to JSON and Neo4j Cypher."""

from __future__ import annotations

import argparse
from pathlib import Path

from drug_intelligence.graph import build_fixture_knowledge_graph, export_cypher, export_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--drugs", type=Path, default=Path("examples/sample_drugs.jsonl"))
    parser.add_argument(
        "--interactions",
        type=Path,
        default=Path("examples/sample_interactions.jsonl"),
    )
    parser.add_argument(
        "--references",
        type=Path,
        default=Path("examples/sample_references.jsonl"),
    )
    parser.add_argument("--output-dir", type=Path, default=Path("reports/sample-kg"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    graph = build_fixture_knowledge_graph(args.drugs, args.interactions, args.references)
    export_json(graph, args.output_dir / "sample-kg.json")
    export_cypher(graph, args.output_dir / "sample-kg.cypher")
    print(
        {
            "nodes": len(graph.nodes),
            "relationships": len(graph.relationships),
            "output_dir": str(args.output_dir),
        }
    )


if __name__ == "__main__":
    main()
