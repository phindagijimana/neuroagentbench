"""L4: QC / numeric invariants if the task lists them."""

from __future__ import annotations

from typing import Any

from evaluators.run_tree import RunRecord


def _compare(actual: Any, op: str, expected: Any) -> bool:
    if op == "==":
        return actual == expected
    if op == ">=":
        return actual >= expected
    if op == "<=":
        return actual <= expected
    if op == ">":
        return actual > expected
    if op == "<":
        return actual < expected
    if op == "!=":
        return actual != expected
    return False


def evaluate_l4(task: dict[str, Any], run: RunRecord) -> str:
    declared = (task.get("oracles") or {}).get("layers") or []
    invariants = task.get("l4_invariants") or []
    if "L4" not in declared or not invariants:
        return "not_applicable"

    gold_action = task.get("gold_action")
    if gold_action in {"abstain", "reject"} and run.gold_action_taken in {"abstain", "reject"}:
        return "not_applicable"

    qc = run.qc
    for invariant in invariants:
        name = invariant.get("name")
        if name not in qc:
            return "fail"
        op = invariant.get("op", "==")
        if not _compare(qc[name], op, invariant.get("value")):
            return "fail"
    return "pass"
