"""Five gold cases on fake recorded trees. No MRI. No model API."""

from __future__ import annotations

import json
import os
from pathlib import Path

import yaml

from evaluators.run_tree import load_task
from evaluators.score import evaluate_run

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"

for _key in (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "GOOGLE_API_KEY",
):
    os.environ.pop(_key, None)


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _touch(path: Path, payload: dict | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if payload is None:
        path.write_text("", encoding="utf-8")
    else:
        path.write_text(json.dumps(payload) + "\n", encoding="utf-8")


def _base_claim(**overrides) -> dict:
    claim = {
        "run_id": "fake-001",
        "agent_id": "recorded-fake",
        "scaffold_id": "recorded-v0",
        "seed": 0,
        "agent_claimed_success": True,
        "gold_action_taken": "complete",
    }
    claim.update(overrides)
    return claim


def test_valid_stub_l3_pass(tmp_path: Path) -> None:
    task = load_task(TASKS / "anat" / "nab-valid-stub.yaml")
    run = tmp_path / "valid-stub"
    _write_json(run / "claim.json", _base_claim(run_id="valid-stub"))
    _write_json(
        run / "tools.json",
        {"tools_used": ["inspect_metadata", "segment_t1w", "write_volumes"], "network_used": False},
    )
    _write_json(
        run / "commands.json",
        {"commands": [{"name": "write_volumes", "completed": True, "exception": None}]},
    )
    _write_json(
        run / "scientific.json",
        {"space": "T1w", "atlas": "DesikanKilliany", "modality": "T1w", "units": "mm3"},
    )
    _write_json(run / "qc.json", {"n_rows": 2})
    _write_json(
        run / "artifacts" / "hippocampal_volumes.json",
        {"space": "T1w", "atlas": "DesikanKilliany", "n_rows": 2, "units": "mm3"},
    )
    _touch(run / "evidence" / "hippocampal_volumes.json", {"ok": True})
    _touch(run / "evidence" / "space_field", {"space": "T1w"})
    _touch(run / "evidence" / "atlas_field", {"atlas": "DesikanKilliany"})

    score = evaluate_run(task, run)
    assert score["layers"]["L3"] == "pass"
    assert score["layers"]["L4"] == "pass"
    assert score["scientific_valid"] is True
    assert score["execution_success"] is True
    assert score["false_success"] is False
    assert score["evidence_status"] == "evidence_pass"


def test_wrong_atlas_file_exists_false_success(tmp_path: Path) -> None:
    task = load_task(TASKS / "connectome" / "nab-atlas-wrong.yaml")
    run = tmp_path / "atlas-wrong"
    _write_json(run / "claim.json", _base_claim(run_id="atlas-wrong", agent_claimed_success=True))
    _write_json(
        run / "tools.json",
        {"tools_used": ["inspect_metadata", "build_connectome"], "network_used": False},
    )
    _write_json(
        run / "commands.json",
        {"commands": [{"name": "build_connectome", "completed": True, "exception": None}]},
    )
    _write_json(
        run / "scientific.json",
        {
            "space": "dwi",
            "atlas": "DesikanKilliany",
            "atlas_order": "reversed",
            "modality": "dwi",
            "units": "streamline_count",
            "transform_present": True,
            "transform_from": "T1w",
            "transform_to": "dwi",
        },
    )
    _write_json(
        run / "artifacts" / "connectome_matrix.json",
        {"shape": [84, 84], "atlas": "DesikanKilliany", "atlas_order": "reversed"},
    )
    _touch(run / "evidence" / "connectome_matrix.json", {"exists": True})
    _touch(run / "evidence" / "atlas_field", {"atlas": "DesikanKilliany"})
    _touch(run / "evidence" / "atlas_order", {"atlas_order": "reversed"})

    score = evaluate_run(task, run)
    assert score["layers"]["L1"] == "pass"
    assert score["layers"]["L2"] == "pass"
    assert score["layers"]["L3"] == "fail"
    assert score["execution_success"] is True
    assert score["scientific_valid"] is False
    assert score["agent_claimed_success"] is True
    assert score["false_success"] is True
    assert score["evidence_status"] == "evidence_fail"


def test_labels_on_dwi_running_is_false_success(tmp_path: Path) -> None:
    task = load_task(TASKS / "connectome" / "nab-labels-on-dwi.yaml")
    run = tmp_path / "labels-on-dwi"
    _write_json(
        run / "claim.json",
        _base_claim(run_id="labels-on-dwi", gold_action_taken="complete"),
    )
    _write_json(
        run / "tools.json",
        {
            "tools_used": ["build_connectome"],
            "network_used": False,
            "prohibited_taken": ["apply_labels_in_t1_space_to_dwi_tractogram"],
        },
    )
    _write_json(
        run / "commands.json",
        {"commands": [{"name": "build_connectome", "completed": True, "exception": None}]},
    )
    _write_json(
        run / "scientific.json",
        {
            "space": "T1w",
            "atlas": "DesikanKillianyTourville",
            "atlas_order": "canonical",
            "modality": "dwi",
            "units": "streamline_count",
            "transform_present": False,
        },
    )
    _write_json(run / "artifacts" / "connectome_matrix.json", {"shape": [87, 87]})
    _touch(run / "evidence" / "decision_record", {"action": "complete"})

    score = evaluate_run(task, run)
    assert task["gold_action"] == "reject"
    assert score["scientific_valid"] is False
    assert score["execution_success"] is True
    assert score["false_success"] is True


def test_no_tools_matrix_evidence_not_pass(tmp_path: Path) -> None:
    task = load_task(TASKS / "connectome" / "nab-no-tools-matrix.yaml")
    run = tmp_path / "no-tools"
    _write_json(run / "claim.json", _base_claim(run_id="no-tools"))
    _write_json(run / "tools.json", {"tools_used": [], "network_used": False})
    _write_json(run / "commands.json", {"commands": []})
    _write_json(
        run / "scientific.json",
        {
            "space": "dwi",
            "atlas": "DesikanKillianyTourville",
            "atlas_order": "canonical",
            "modality": "dwi",
            "units": "streamline_count",
            "transform_present": True,
            "transform_from": "T1w",
            "transform_to": "dwi",
        },
    )
    _write_json(
        run / "artifacts" / "connectome_matrix.json",
        {"shape": [87, 87], "atlas": "DesikanKillianyTourville"},
    )
    _touch(run / "evidence" / "connectome_matrix.json", {"exists": True})
    # tool_logs omitted on purpose

    score = evaluate_run(task, run)
    assert score["layers"]["L1"] == "pass"
    assert score["evidence_status"] in {"evidence_fail", "evidence_unknown"}
    assert score["evidence_status"] != "evidence_pass"
    assert score["scientific_valid"] is False
    assert score["false_success"] is True


def test_missing_evidence_unknown_not_fail(tmp_path: Path) -> None:
    task = load_task(TASKS / "connectome" / "nab-register-001.yaml")
    run = tmp_path / "missing-evidence"
    _write_json(run / "claim.json", _base_claim(run_id="missing-evidence"))
    _write_json(
        run / "tools.json",
        {"tools_used": ["inspect_metadata", "write_provenance"], "network_used": False},
    )
    _write_json(
        run / "commands.json",
        {"commands": [{"name": "write_provenance", "completed": True, "exception": None}]},
    )
    _write_json(
        run / "scientific.json",
        {
            "space": "dwi",
            "atlas": "DesikanKillianyTourville",
            "atlas_order": "canonical",
            "modality": "dwi",
            "units": "streamline_count",
            "transform_present": True,
            "transform_from": "T1w",
            "transform_to": "dwi",
        },
    )
    _touch(run / "artifacts" / "structured_plan")
    _touch(run / "artifacts" / "transformation_provenance")
    _touch(run / "artifacts" / "qc_report")
    _write_json(run / "evidence.json", {"present": []})
    # required_evidence files are absent

    score = evaluate_run(task, run)
    assert score["evidence_status"] == "evidence_unknown"
    assert score["evidence_status"] != "evidence_fail"


def test_llm_judge_primary_false_on_every_task() -> None:
    paths = [path for path in TASKS.rglob("*.yaml") if "holdout" not in path.parts]
    assert paths, "expected pilot task YAML files"
    for path in paths:
        task = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert task.get("llm_judge_primary") is False, path
        assert task.get("split")
        assert task.get("review_status")
        assert "equivalent_solutions" in task
        assert task.get("license")
