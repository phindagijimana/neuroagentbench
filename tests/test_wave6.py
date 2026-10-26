"""Wave 6: recorded tree that points at fetched S0 T1w. No NIfTI in git.

B0 may see the real gzip when it is already on disk. Pytest does not
download. Holdout stays empty. No run --agent. No GPT judge.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import yaml

from evaluators.file_exists import grade_file_exists
from evaluators.score import evaluate_paths
from neuroagentbench.cli import main

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
TASK = TASKS / "anat" / "nab-valid-stub.yaml"
RUN = ROOT / "examples" / "runs" / "s0-public-t1w"
S0_REL = Path("shared") / "data" / "external" / "ds000003" / "sub-01" / "anat" / "sub-01_T1w.nii.gz"
S0_SHA256 = "9cb6dc66d4e845a40f2317027aa60d0035cb95634b303f6c0efce961e1e2a4d6"
S0_BYTES = 5712417

for _key in (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "GOOGLE_API_KEY",
):
    os.environ.pop(_key, None)


def _pilot_tasks() -> list[Path]:
    return [path for path in TASKS.rglob("*.yaml") if "holdout" not in path.parts]


def test_s0_tree_has_no_nifti() -> None:
    assert RUN.is_dir()
    manifest = json.loads((RUN / "run_manifest.json").read_text(encoding="utf-8"))
    assert manifest["bytes_in_git"] is False
    assert manifest["nifti_in_tree"] is False
    t1w = manifest["inputs"]["t1w"]
    assert t1w["path"] == S0_REL.as_posix()
    assert t1w["sha256"] == S0_SHA256
    assert t1w["bytes"] == S0_BYTES
    assert t1w["gzip_magic"] == "1f8b"
    assert not list(RUN.rglob("*.nii"))
    assert not list(RUN.rglob("*.nii.gz"))
    assert not (RUN / "sub-01_T1w.nii.gz").exists()
    assert not (ROOT / "shared" / "data" / "external").exists()
    for path in RUN.rglob("*"):
        if path.is_file():
            assert path.suffix.lower() not in {".nii", ".gz", ".trk", ".tck"}


def test_s0_tree_scores_valid_stub() -> None:
    score = evaluate_paths(TASK, RUN)
    assert score["run_id"] == "s0-public-t1w"
    assert score["llm_judge_primary"] is False
    assert score["scientific_valid"] is True
    assert score["false_success"] is False
    assert score["layers"]["L3"] == "pass"
    assert score["secondary"]["oracle"] is False
    score_src = (ROOT / "evaluators" / "score.py").read_text(encoding="utf-8")
    assert "openai" not in score_src.lower()
    assert "gpt" not in score_src.lower()


def test_b0_sees_fetched_t1w_when_present() -> None:
    task = {
        "task_id": "nab-valid-stub",
        "expected_artifacts": ["hippocampal_volumes.json"],
    }
    grade = grade_file_exists(task, RUN)
    assert grade["status"] == "pass"
    rows = {row["name"]: row for row in grade["inputs"]}
    assert "t1w" in rows
    if rows["t1w"]["exists"]:
        assert rows["t1w"]["real_gzip"] is True
        assert "ds000003" in (rows["t1w"]["resolved"] or "")
        assert rows["t1w"]["sha256_match"] is True
        assert any(Path(item).name == "sub-01_T1w.nii.gz" for item in grade["real_files_seen"])


def test_llm_judge_primary_five_tasks_holdout_empty_no_agent() -> None:
    paths = _pilot_tasks()
    assert len(paths) == 5
    for path in paths:
        task = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert task.get("llm_judge_primary") is False, path
        assert task.get("split") != "holdout"
    assert not list((TASKS / "holdout").rglob("*.yaml"))
    rc = main(["run", "--task", str(TASK)])
    assert rc != 0
    cli_src = (ROOT / "neuroagentbench" / "cli.py").read_text(encoding="utf-8")
    assert "--agent" not in cli_src
    workflow = ROOT / ".github" / "workflows" / "pytest.yml"
    assert workflow.is_file()
    text = workflow.read_text(encoding="utf-8")
    assert "OPENAI_API_KEY" in text
    assert "NIfTI" in text
