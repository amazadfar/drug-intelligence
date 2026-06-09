import json
from pathlib import Path

from drug_intelligence.benchmarking import BenchmarkConfig, run_sample_benchmark

ROOT = Path(__file__).resolve().parents[1]


def test_sample_benchmark_writes_reproducible_artifacts(tmp_path: Path) -> None:
    result = run_sample_benchmark(
        BenchmarkConfig(
            encoder="gin",
            hidden_dim=8,
            num_layers=1,
            epochs=1,
            batch_size=8,
            seed=7,
        ),
        fixtures_path=ROOT / "examples" / "sample_drugs.jsonl",
        output_dir=tmp_path,
    )

    metrics_path = tmp_path / "sample-benchmark-metrics.json"
    report_path = tmp_path / "sample-benchmark-report.md"

    assert result["scientific_claim"] is False
    assert result["dataset"]["drugs"] == 10
    assert result["dataset"]["pairs"] == 45
    assert metrics_path.exists()
    assert report_path.exists()
    assert json.loads(metrics_path.read_text())["config"]["seed"] == 7
    assert "not scientific claims" in report_path.read_text()


def test_benchmark_config_loads_from_toml() -> None:
    config = BenchmarkConfig.from_toml(ROOT / "configs" / "sample-gin.toml")

    assert config.encoder == "gin"
    assert config.epochs == 5
    assert config.split_strategy == "random"
