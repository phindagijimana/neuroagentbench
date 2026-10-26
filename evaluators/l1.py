"""L1: required files exist and parse. No MRI bytes."""

from __future__ import annotations

import json
from typing import Any

from evaluators.run_tree import RunRecord


def _justified_refusal(task: dict[str, Any], run: RunRecord) -> bool:
    gold = task.get("gold_action")
    return gold in {"abstain", "reject"} and run.gold_action_taken in {"abstain", "reject"}


def evaluate_l1(task: dict[str, Any], run: RunRecord) -> str:
    if _justified_refusal(task, run):
        return "not_applicable"

    expected = task.get("expected_artifacts") or []
    if not expected:
        return "not_applicable"

    for name in expected:
        path = run.artifact_path(name)
        if not path.is_file():
            return "fail"
        if path.suffix == ".json":
            try:
                with path.open(encoding="utf-8") as handle:
                    json.load(handle)
            except (OSError, json.JSONDecodeError):
                return "fail"
    return "pass"
