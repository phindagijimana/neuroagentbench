"""Same recorded trees through B0 file-exists and L0–L5 evaluate.

Behavioral assertions only. No fabricated results. No model API. No MRI.
"""

from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path

import pytest
import yaml

from evaluators.file_exists import grade_paths
from evaluators.run_tree import load_task
from evaluators.score import evaluate_paths

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "examples" / "runs"
TASKS = ROOT / "tasks"

TREES = {
    "valid-stub": {
        "task": TASKS / "anat" / "nab-valid-stub.yaml",
        "run": RUNS / "valid-stub",
    },
    "atlas-wrong": {
        "task": TASKS / "connectome" / "nab-atlas-wrong.yaml",
        "run": RUNS / "atlas-wrong",
    },
    "labels-on-dwi": {
        "task": TASKS / "connectome" / "nab-labels-on-dwi.yaml",
        "run": RUNS / "labels-on-dwi",
    },
    "no-tools-matrix": {
        "task": TASKS / "connectome" / "nab-no-tools-matrix.yaml",
        "run": RUNS / "no-tools-matrix",
    },
    "missing-evidence": {
        "task": TASKS / "connectome" / "nab-register-001.yaml",
        "run": RUNS / "missing-evidence",
    },
}

for _key in (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "GOOGLE_API_KEY",
):
    os.environ.pop(_key, None)


def _both(name: str) -> tuple[dict, dict]:
    spec = TREES[name]
    return grade_paths(spec["task"], spec["run"]), evaluate_paths(spec["task"], spec["run"])


def test_valid_stub_file_exists_and_scientific_valid() -> None:
    file_exists, score = _both("valid-stub")
    assert file_exists["passed"] is True
    assert score["scientific_valid"] is True
    assert score["layers"]["L3"] == "pass"
    assert score["false_success"] is False


def test_atlas_wrong_file_exists_pass_l3_fail_false_success() -> None:
    file_exists, score = _both("atlas-wrong")
    assert file_exists["passed"] is True
    assert score["layers"]["L3"] == "fail"
    assert score["scientific_valid"] is False
    if score["agent_claimed_success"] or score["execution_success"]:
        assert score["false_success"] is True


def test_labels_on_dwi_gold_reject_running_is_false_success() -> None:
    spec = TREES["labels-on-dwi"]
    task = load_task(spec["task"])
    file_exists, score = _both("labels-on-dwi")
    assert task["gold_action"] == "reject"
    matrix = spec["run"] / "artifacts" / "connectome_matrix.json"
    if matrix.is_file():
        assert file_exists["passed"] is True
    assert score["scientific_valid"] is False
    assert score["false_success"] is True


def test_no_tools_matrix_file_exists_pass_evidence_fail_not_pass() -> None:
    file_exists, score = _both("no-tools-matrix")
    assert file_exists["passed"] is True
    assert score["evidence_status"] == "evidence_fail"
    assert score["evidence_status"] != "evidence_pass"
    assert score["scientific_valid"] is False


def test_missing_evidence_file_exists_fail_or_empty_unknown_not_fail() -> None:
    file_exists, score = _both("missing-evidence")
    assert file_exists["status"] in {"fail", "empty"}
    assert file_exists["passed"] is False
    assert score["evidence_status"] == "evidence_unknown"
    assert score["evidence_status"] != "evidence_fail"


def test_llm_judge_primary_false_on_holistic_tasks() -> None:
    for spec in TREES.values():
        task = yaml.safe_load(spec["task"].read_text(encoding="utf-8"))
        assert task.get("llm_judge_primary") is False


def test_construction_holdout_empty_no_factorial_v0() -> None:
    holdout = TASKS / "holdout"
    assert holdout.is_dir()
    assert not list(holdout.rglob("*.yaml")), "holdout must stay empty in v0"
    experiments = ROOT / "experiments"
    assert not experiments.exists() or not list(experiments.rglob("*"))
    score_schema = json.loads((ROOT / "schemas" / "score.schema.json").read_text(encoding="utf-8"))
    assert "seed" in score_schema["properties"]
    gold = (json.loads((ROOT / "schemas" / "task.schema.json").read_text(encoding="utf-8"))["properties"]["gold_action"]["enum"])
    assert {"complete", "abstain", "reject"} <= set(gold)


def test_optional_sciguard_condition_on_labels_on_dwi_not_nab_novelty() -> None:
    """SciGuard report is a secondary condition, not NeuroAgentBench novelty."""
    sciguard_root = ROOT.parent / "02_SciGuard"
    fixture = sciguard_root / "fixtures" / "invalid" / "labels_t1w_to_dwi_no_transform.yaml"
    if not fixture.is_file():
        pytest.skip("SciGuard fixture not present")
    if str(sciguard_root) not in sys.path:
        sys.path.insert(0, str(sciguard_root))
    try:
        check_mod = importlib.import_module("validation.check")
    except ImportError:
        pytest.skip("SciGuard not importable")
    report = check_mod.check_workflow(fixture)
    assert isinstance(report, dict)
    assert report.get("certificate_of_scientific_correctness") is False
