"""L3: space, transform, atlas, units, modality versus task gold."""

from __future__ import annotations

from typing import Any

from evaluators.run_tree import RunRecord

_COMPARE_KEYS = ("space", "atlas", "atlas_order", "units", "modality")


def evaluate_l3(task: dict[str, Any], run: RunRecord) -> str:
    gold_action = task.get("gold_action")
    if gold_action in {"abstain", "reject"}:
        if run.gold_action_taken in {"abstain", "reject"}:
            return "pass"
        return "fail"

    gold = task.get("scientific_gold") or {}
    if not gold:
        return "not_applicable"

    sci = run.scientific
    if not sci:
        return "fail"

    for key in _COMPARE_KEYS:
        if key in gold and gold[key] is not None and sci.get(key) != gold[key]:
            return "fail"

    if gold.get("transform_required"):
        if not sci.get("transform_present"):
            return "fail"
        for key in ("transform_from", "transform_to"):
            if key in gold and sci.get(key) != gold[key]:
                return "fail"

    if gold.get("tools_must_have_run") and not run.tools_used:
        return "fail"

    return "pass"
