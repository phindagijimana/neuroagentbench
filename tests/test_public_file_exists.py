"""Public B0: SWE-bench-style file-exists grader. No space/atlas/QC/oracle."""

from __future__ import annotations

import os
from pathlib import Path

from evaluators.file_exists import grade_paths
from evaluators.run_tree import load_task

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "examples" / "runs"
TASKS = ROOT / "tasks"

for _key in (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "GOOGLE_API_KEY",
):
    os.environ.pop(_key, None)


def _grade(task_rel: str, run_name: str) -> dict:
    return grade_paths(TASKS / task_rel, RUNS / run_name)


def test_valid_stub_file_exists_pass() -> None:
    result = _grade("anat/nab-valid-stub.yaml", "valid-stub")
    assert result["status"] == "pass"
    assert result["passed"] is True
    assert result["missing"] == []
    assert "hippocampal_volumes.json" in result["present"]


def test_atlas_wrong_file_exists_pass() -> None:
    """Residual: the matrix file exists, so B0 passes; L3 is not this grader."""
    result = _grade("connectome/nab-atlas-wrong.yaml", "atlas-wrong")
    assert result["status"] == "pass"
    assert result["passed"] is True
    assert "connectome_matrix.json" in result["present"]
    assert result["missing"] == []


def test_no_tools_matrix_file_exists_pass() -> None:
    result = _grade("connectome/nab-no-tools-matrix.yaml", "no-tools-matrix")
    assert result["status"] == "pass"
    assert result["passed"] is True
    assert "connectome_matrix.json" in result["present"]


def test_labels_on_dwi_file_exists_may_pass_if_matrix_written() -> None:
    task = load_task(TASKS / "connectome" / "nab-labels-on-dwi.yaml")
    run = RUNS / "labels-on-dwi"
    result = grade_paths(TASKS / "connectome" / "nab-labels-on-dwi.yaml", run)
    matrix = run / "artifacts" / "connectome_matrix.json"
    if matrix.is_file():
        assert result["passed"] is True
        assert result["status"] == "pass"
        assert "connectome_matrix.json" in result["present"]
    else:
        assert result["status"] in {"fail", "empty"}
    assert task["expected_artifacts"] == ["connectome_matrix.json"]
