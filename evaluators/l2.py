"""L2: commands completed; no hidden exception in logs."""

from __future__ import annotations

from typing import Any

from evaluators.run_tree import RunRecord


def _justified_refusal(task: dict[str, Any], run: RunRecord) -> bool:
    gold = task.get("gold_action")
    return gold in {"abstain", "reject"} and run.gold_action_taken in {"abstain", "reject"}


def evaluate_l2(task: dict[str, Any], run: RunRecord) -> str:
    if _justified_refusal(task, run):
        return "not_applicable"

    hidden = run.commands.get("hidden_exceptions") or []
    if hidden:
        return "fail"

    for command in run.commands.get("commands") or []:
        if command.get("completed") is False:
            return "fail"
        if command.get("exception"):
            return "fail"

    log_path = run.path / "logs" / "run.log"
    if log_path.is_file():
        text = log_path.read_text(encoding="utf-8", errors="replace")
        if "Traceback" in text or "HIDDEN_EXCEPTION" in text:
            return "fail"

    return "pass"
