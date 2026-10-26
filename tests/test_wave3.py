"""Wave 3: handbook, construction fields, seed on score, dry-run run. No MRI. No model."""

from __future__ import annotations

import json
import os
from pathlib import Path

import yaml

from neuroagentbench.cli import main

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
RUNS = ROOT / "examples" / "runs"

for _key in (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "GOOGLE_API_KEY",
):
    os.environ.pop(_key, None)


def test_handbook_exists_and_has_no_results() -> None:
    handbook = ROOT / "docs" / "handbook.md"
    assert handbook.is_file()
    text = handbook.read_text(encoding="utf-8")
    assert "L0" in text and "L5" in text
    assert "false_success" in text
    assert "evidence_unknown" in text
    assert "abstain" in text and "reject" in text
    assert "not a result" in text.lower()


def test_construction_fields_on_every_task() -> None:
    schema = json.loads((ROOT / "schemas" / "task.schema.json").read_text(encoding="utf-8"))
    required = set(schema["required"])
    assert {"split", "equivalent_solutions", "review_status", "license"} <= required
    paths = [path for path in TASKS.rglob("*.yaml") if "holdout" not in path.parts]
    assert paths
    for path in paths:
        task = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert task.get("split") in {"dev", "public_verified"}
        assert task.get("split") != "holdout"
        assert isinstance(task.get("equivalent_solutions"), list)
        assert task.get("review_status")
        assert task.get("license")
        assert task.get("llm_judge_primary") is False


def test_holdout_empty_of_tasks() -> None:
    holdout = TASKS / "holdout"
    assert holdout.is_dir()
    assert not list(holdout.rglob("*.yaml"))


def test_evaluate_seed_0_writes_seed(capsys) -> None:
    rc = main(
        [
            "evaluate",
            "--task",
            str(TASKS / "anat" / "nab-valid-stub.yaml"),
            "--run",
            str(RUNS / "valid-stub"),
            "--seed",
            "0",
        ]
    )
    assert rc == 0
    score = json.loads(capsys.readouterr().out)
    assert score["seed"] == 0
    assert "layers" in score


def test_run_without_recorded_tree_refuses(capsys) -> None:
    rc = main(["run", "--task", str(TASKS / "anat" / "nab-valid-stub.yaml")])
    assert rc != 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["reason"] == "evaluate_first_no_agent"
    assert payload["ok"] is False


def test_run_from_recorded_aliases_evaluate(capsys) -> None:
    rc = main(
        [
            "run",
            "--task",
            str(TASKS / "anat" / "nab-valid-stub.yaml"),
            "--from-recorded",
            str(RUNS / "valid-stub"),
            "--seed",
            "0",
        ]
    )
    assert rc == 0
    score = json.loads(capsys.readouterr().out)
    assert score["seed"] == 0
    assert score["scientific_valid"] is True


def test_llm_judge_primary_false() -> None:
    for path in TASKS.rglob("*.yaml"):
        if "holdout" in path.parts:
            continue
        task = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert task.get("llm_judge_primary") is False
