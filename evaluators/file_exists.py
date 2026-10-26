"""SWE-bench-style public baseline (B0).

Pass iff the task's expected artifact files exist on the recorded tree.
Does not inspect space, atlas, QC, units, modality, transforms, or gold
action. Not a scientific-validity oracle. Atlas-wrong is expected to pass.

No MRI bytes. No model API.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from evaluators.run_tree import load_task


def grade_file_exists(task: dict[str, Any], run_dir: Path | str) -> dict[str, Any]:
    """Return a B0 file-exists grade for one recorded run directory."""
    run = Path(run_dir)
    expected = [str(name) for name in (task.get("expected_artifacts") or [])]
    present: list[str] = []
    missing: list[str] = []
    for name in expected:
        path = run / "artifacts" / name
        if path.is_file():
            present.append(name)
        else:
            missing.append(name)

    if not expected:
        status = "empty"
    elif missing:
        status = "fail"
    else:
        status = "pass"

    return {
        "grader": "file_exists",
        "layer": "B0",
        "status": status,
        "passed": status == "pass",
        "expected": expected,
        "present": present,
        "missing": missing,
        "task_id": task.get("task_id"),
        "run_dir": str(run),
    }


def grade_paths(task_path: Path | str, run_dir: Path | str) -> dict[str, Any]:
    return grade_file_exists(load_task(Path(task_path)), run_dir)
