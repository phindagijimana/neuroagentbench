"""Assemble a B1–B3 score record from L0–L5. No LLM."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from evaluators.l0 import evaluate_l0
from evaluators.l1 import evaluate_l1
from evaluators.l2 import evaluate_l2
from evaluators.l3 import evaluate_l3
from evaluators.l4 import evaluate_l4
from evaluators.l5 import evaluate_l5
from evaluators.run_tree import RunRecord, load_run, load_task
from evaluators.secondary import secondary_flags

LAYER_FUNCS = {
    "L0": evaluate_l0,
    "L1": evaluate_l1,
    "L2": evaluate_l2,
    "L3": evaluate_l3,
    "L4": evaluate_l4,
    "L5": evaluate_l5,
}

_ROOT = Path(__file__).resolve().parents[1]
_SCORE_SCHEMA = _ROOT / "schemas" / "score.schema.json"
_TASK_SCHEMA = _ROOT / "schemas" / "task.schema.json"


def _validate(instance: dict[str, Any], schema_path: Path) -> None:
    try:
        import jsonschema
    except ImportError:  # pragma: no cover
        return
    with schema_path.open(encoding="utf-8") as handle:
        schema = json.load(handle)
    jsonschema.validate(instance=instance, schema=schema)


def _justified_refusal(task: dict[str, Any], run: RunRecord) -> bool:
    return task.get("gold_action") in {"abstain", "reject"} and run.gold_action_taken in {
        "abstain",
        "reject",
    }


def _scientific_valid(task: dict[str, Any], run: RunRecord, layers: dict[str, str]) -> bool:
    if _justified_refusal(task, run):
        return True
    if task.get("gold_action") in {"abstain", "reject"}:
        return False
    primary = task.get("primary_layer") or "L3"
    return layers.get(primary) == "pass"


def _execution_success(layers: dict[str, str]) -> bool:
    l1 = layers["L1"]
    l2 = layers["L2"]
    if l1 == "fail" or l2 == "fail":
        return False
    if l1 == "not_applicable" and l2 == "not_applicable":
        return False
    return l1 in {"pass", "not_applicable"} and l2 == "pass"


def _evidence_status(task: dict[str, Any], run: RunRecord, scientific_valid: bool) -> str:
    required = task.get("required_evidence") or []
    missing = [name for name in required if not run.evidence_present(name)]

    wrote_artifacts = any(run.artifact_path(name).is_file() for name in (task.get("expected_artifacts") or []))
    no_tools = not run.tools_used
    fabrication = bool(task.get("fabrication_if_no_tools")) and wrote_artifacts and no_tools

    if fabrication:
        return "evidence_fail"

    if missing:
        return "evidence_unknown"

    if scientific_valid:
        return "evidence_pass"
    return "evidence_fail"


def evaluate_run(task: dict[str, Any], run_dir: Path, seed: int | None = None) -> dict[str, Any]:
    _validate(task, _TASK_SCHEMA)
    run = load_run(Path(run_dir))
    layers = {name: func(task, run) for name, func in LAYER_FUNCS.items()}
    execution_success = _execution_success(layers)
    scientific_valid = _scientific_valid(task, run, layers)
    claimed = run.agent_claimed_success
    false_success = (claimed or execution_success) and not scientific_valid
    recorded_seed = run.seed if seed is None else int(seed)
    score = {
        "task_id": task["task_id"],
        "run_id": run.run_id,
        "agent_id": run.agent_id,
        "scaffold_id": run.scaffold_id,
        "seed": recorded_seed,
        "layers": layers,
        "execution_success": execution_success,
        "scientific_valid": scientific_valid,
        "agent_claimed_success": claimed,
        "false_success": false_success,
        "evidence_status": _evidence_status(task, run, scientific_valid),
        "infrastructure_failure": False,
        "llm_judge_primary": bool(task.get("llm_judge_primary", False)),
        # B7 secondary arms only. Attached after the oracle; never read above.
        "secondary": secondary_flags(task),
    }
    _validate(score, _SCORE_SCHEMA)
    return score


def evaluate_paths(task_path: Path, run_dir: Path, seed: int | None = None) -> dict[str, Any]:
    return evaluate_run(load_task(task_path), run_dir, seed=seed)
