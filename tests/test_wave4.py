"""Wave 4: secondary SciCap/SciGuard flags, construction fields, holdout empty.

Not this paper's oracle. No GPT judge. No 50-task suite. No website. No MRI.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import yaml

from evaluators.run_tree import load_task
from evaluators.score import evaluate_paths, evaluate_run
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


def _pilot_tasks() -> list[Path]:
    return [path for path in TASKS.rglob("*.yaml") if "holdout" not in path.parts]


def test_secondary_flags_on_score_not_oracle() -> None:
    score = evaluate_paths(TASKS / "anat" / "nab-valid-stub.yaml", RUNS / "valid-stub")
    secondary = score["secondary"]
    assert secondary["oracle"] is False
    assert secondary["scicap_decision"] in {"ALLOW", "REJECT", "ABSTAIN", "not_run"}
    assert secondary["sciguard_status"] in {
        "PASS",
        "FAIL",
        "UNKNOWN",
        "NEEDS_REVIEW",
        "not_run",
    }
    assert score["scientific_valid"] is True
    assert score["layers"]["L3"] == "pass"
    if not secondary["scicap_importable"]:
        assert secondary["scicap_decision"] == "not_run"
    if not secondary["sciguard_importable"]:
        assert secondary["sciguard_status"] == "not_run"


def test_labels_on_dwi_sciguard_secondary_never_fake_pass() -> None:
    task = load_task(TASKS / "connectome" / "nab-labels-on-dwi.yaml")
    score = evaluate_run(task, RUNS / "labels-on-dwi")
    secondary = score["secondary"]
    assert secondary["oracle"] is False
    assert score["scientific_valid"] is False
    assert score["false_success"] is True
    if secondary["sciguard_importable"]:
        assert secondary["sciguard_status"] == "FAIL"
    else:
        assert secondary["sciguard_status"] == "not_run"
    assert secondary["sciguard_status"] != "PASS"


def test_secondary_does_not_replace_l3_on_atlas_wrong() -> None:
    score = evaluate_paths(
        TASKS / "connectome" / "nab-atlas-wrong.yaml", RUNS / "atlas-wrong"
    )
    assert score["layers"]["L3"] == "fail"
    assert score["scientific_valid"] is False
    assert score["false_success"] is True
    assert score["secondary"]["oracle"] is False


def test_llm_judge_primary_false_on_every_task() -> None:
    paths = _pilot_tasks()
    assert paths
    for path in paths:
        task = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert task.get("llm_judge_primary") is False, path


def test_construction_fields_on_every_pilot_task() -> None:
    schema = json.loads((ROOT / "schemas" / "task.schema.json").read_text(encoding="utf-8"))
    required = set(schema["required"])
    assert {
        "review_status",
        "license",
        "equivalent_solutions",
        "dataset_snapshot",
        "compute_tier",
        "llm_judge_primary",
    } <= required
    assert schema["properties"]["llm_judge_primary"].get("const") is False
    paths = _pilot_tasks()
    assert len(paths) == 5
    for path in paths:
        task = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert task.get("review_status")
        assert task.get("license")
        assert isinstance(task.get("equivalent_solutions"), list)
        assert task.get("dataset_snapshot")
        assert task.get("compute_tier")
        assert task.get("split") != "holdout"
        assert task.get("llm_judge_primary") is False


def test_holdout_empty_of_tasks() -> None:
    holdout = TASKS / "holdout"
    assert holdout.is_dir()
    assert not list(holdout.rglob("*.yaml"))


def test_run_without_recorded_tree_still_refuses(capsys) -> None:
    rc = main(["run", "--task", str(TASKS / "anat" / "nab-valid-stub.yaml")])
    assert rc != 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["reason"] == "evaluate_first_no_agent"
    assert payload["ok"] is False


def test_no_fifty_task_suite_no_website_no_gpt_judge() -> None:
    assert len(_pilot_tasks()) == 5
    assert not (ROOT / "website").exists()
    assert not list(ROOT.glob("index.html"))
    score_src = (ROOT / "evaluators" / "score.py").read_text(encoding="utf-8")
    assert "openai" not in score_src.lower()
    assert "gpt" not in score_src.lower()
    layer_dir = ROOT / "evaluators"
    for path in layer_dir.glob("l*.py"):
        text = path.read_text(encoding="utf-8").lower()
        assert "openai" not in text
        assert "gpt" not in text
