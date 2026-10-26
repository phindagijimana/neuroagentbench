"""Wave 5: extra recorded JSON tree + unsigned two-expert checklist.

No NIfTI. No GPT judge. No agent start. SciCap/SciGuard stay oracle false.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import yaml

from evaluators.score import evaluate_paths
from neuroagentbench.cli import main

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
RUNS = ROOT / "examples" / "runs"
REFUSE = RUNS / "labels-on-dwi-refuse"
LABELS_TASK = TASKS / "connectome" / "nab-labels-on-dwi.yaml"

for _key in (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "GOOGLE_API_KEY",
):
    os.environ.pop(_key, None)


def _pilot_tasks() -> list[Path]:
    return [path for path in TASKS.rglob("*.yaml") if "holdout" not in path.parts]


def test_extra_refuse_tree_justified_reject() -> None:
    score = evaluate_paths(LABELS_TASK, REFUSE)
    assert score["task_id"] == "nab-labels-on-dwi"
    assert score["run_id"] == "labels-on-dwi-refuse"
    assert score["layers"]["L3"] == "pass"
    assert score["layers"]["L1"] == "not_applicable"
    assert score["layers"]["L2"] == "not_applicable"
    assert score["scientific_valid"] is True
    assert score["agent_claimed_success"] is False
    assert score["execution_success"] is False
    assert score["false_success"] is False
    assert score["evidence_status"] == "evidence_pass"
    assert score["secondary"]["oracle"] is False


def test_extra_tree_is_json_only_no_nifti() -> None:
    assert REFUSE.is_dir()
    manifest = json.loads((REFUSE / "run_manifest.json").read_text(encoding="utf-8"))
    assert manifest["bytes_in_git"] is False
    assert manifest["nifti_in_tree"] is False
    assert not list(REFUSE.rglob("*.nii"))
    assert not list(REFUSE.rglob("*.nii.gz"))
    assert not (REFUSE / "artifacts" / "connectome_matrix.json").exists()
    for path in REFUSE.rglob("*"):
        if path.is_file():
            assert path.suffix.lower() not in {".nii", ".gz", ".trk", ".tck"}


def test_llm_judge_primary_and_secondary_oracle_stay_false() -> None:
    paths = _pilot_tasks()
    assert len(paths) == 5
    for path in paths:
        task = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert task.get("llm_judge_primary") is False, path
        assert task.get("review_status") == "draft"
    score = evaluate_paths(LABELS_TASK, REFUSE)
    assert score["secondary"]["oracle"] is False
    assert score["secondary"]["scicap_decision"] in {"ALLOW", "REJECT", "ABSTAIN", "not_run"}
    assert score["secondary"]["sciguard_status"] in {
        "PASS",
        "FAIL",
        "UNKNOWN",
        "NEEDS_REVIEW",
        "not_run",
    }
    if score["secondary"]["sciguard_importable"]:
        assert score["secondary"]["sciguard_status"] == "FAIL"
        assert score["scientific_valid"] is True


def test_unsigned_checklist_exists_no_invented_signatures() -> None:
    checklist = ROOT / "docs" / "review_checklist.md"
    assert checklist.is_file()
    text = checklist.read_text(encoding="utf-8")
    lowered = text.lower()
    assert "not a result" in lowered
    assert "expert 1" in lowered
    assert "adjudicator" in lowered
    assert "labels-on-dwi-refuse" in text
    assert "unsigned" in lowered
    forbidden = (
        "signed by",
        "agreement =",
        "kappa",
        "jane doe",
        "john doe",
        "@",
    )
    for token in forbidden:
        assert token not in lowered
    assert "leave this file unsigned" in lowered
    assert "review_status" in lowered and "draft" in lowered


def test_still_five_tasks_holdout_empty_no_agent() -> None:
    assert len(_pilot_tasks()) == 5
    assert not list((TASKS / "holdout").rglob("*.yaml"))
    rc = main(["run", "--task", str(LABELS_TASK)])
    assert rc != 0
