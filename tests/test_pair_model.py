from pathlib import Path

import pytest
import torch
from torch_geometric.data import Batch

from drug_intelligence.benchmarking.sample_dataset import (
    EDGE_FEATURES,
    GLOBAL_FEATURES,
    NODE_FEATURES,
    build_sample_graphs,
)
from drug_intelligence.data import MECHANISM_LABELS, SEVERITY_LABELS
from drug_intelligence.models import (
    DrugPairInteractionModel,
    EncoderConfig,
    build_graph_encoder,
)

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("encoder_name", ["gin", "gat", "gatv2", "transformer", "mpnn"])
def test_pair_model_is_symmetric(encoder_name: str) -> None:
    torch.manual_seed(7)
    graphs = build_sample_graphs(ROOT / "examples" / "sample_drugs.jsonl")
    first, second = list(graphs.values())[:2]
    encoder = build_graph_encoder(
        EncoderConfig(
            name=encoder_name,
            node_dim=len(NODE_FEATURES),
            edge_dim=len(EDGE_FEATURES),
            hidden_dim=8,
            num_layers=1,
            dropout=0.0,
        )
    )
    model = DrugPairInteractionModel(
        encoder=encoder,
        global_feature_dim=len(GLOBAL_FEATURES),
        hidden_dim=8,
        mechanism_classes=len(MECHANISM_LABELS),
        severity_levels=len(SEVERITY_LABELS),
        dropout=0.0,
    )
    model.eval()
    batch_a = Batch.from_data_list([first])
    batch_b = Batch.from_data_list([second])

    with torch.no_grad():
        forward = model(batch_a, batch_b)
        reversed_pair = model(batch_b, batch_a)

    assert torch.allclose(forward[0], reversed_pair[0])
    assert torch.allclose(forward[1], reversed_pair[1])
