"""L5: pinned digest / hashes if present."""

from __future__ import annotations

from typing import Any

from evaluators.run_tree import RunRecord


def evaluate_l5(task: dict[str, Any], run: RunRecord) -> str:
    declared = (task.get("oracles") or {}).get("layers") or []
    pins = task.get("l5_pins") or []
    if "L5" not in declared or not pins:
        return "not_applicable"

    gold_action = task.get("gold_action")
    if gold_action in {"abstain", "reject"} and run.gold_action_taken in {"abstain", "reject"}:
        return "not_applicable"

    provenance = run.provenance
    for pin in pins:
        name = pin.get("name")
        if provenance.get(name) != pin.get("digest"):
            return "fail"
    return "pass"
