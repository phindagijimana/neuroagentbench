"""SWE-bench-style public baseline (B0).

Pass iff the task's expected artifact files exist on the recorded tree.
Does not inspect space, atlas, QC, units, modality, transforms, or gold
action. Not a scientific-validity oracle. Atlas-wrong is expected to pass.

When a recorded tree declares input paths (inputs.json / run_manifest.json),
B0 also reports whether those files exist on disk. That lets B0 see a real
S0 T1w without copying NIfTI into this folder. Missing inputs are reported
but do not change artifact status (bytes may be absent on a clean machine).

No MRI bytes. No model API.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from evaluators.run_tree import load_task

_NAB_ROOT = Path(__file__).resolve().parents[1]
_WORKSPACE = _NAB_ROOT.parent


def _is_real_gzip(path: Path) -> bool:
    try:
        if not path.is_file() or path.stat().st_size < 1024:
            return False
        return path.read_bytes()[:2] == b"\x1f\x8b"
    except OSError:
        return False


def _resolve_declared_path(raw: str) -> Path:
    text = str(raw or "").strip()
    if not text:
        return Path()
    candidate = Path(text)
    if candidate.is_file():
        return candidate.resolve()
    for base in (_WORKSPACE, _NAB_ROOT, Path.cwd()):
        joined = (base / text).resolve()
        if joined.is_file():
            return joined
    return _WORKSPACE / text


def _sha256(path: Path) -> str | None:
    try:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return None


def _iter_declared_inputs(run: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for name in ("inputs.json", "run_manifest.json"):
        path = run / name
        if not path.is_file():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict):
            continue
        if isinstance(payload.get("inputs"), dict):
            inputs = payload["inputs"]
        elif name == "inputs.json":
            inputs = {
                key: value
                for key, value in payload.items()
                if isinstance(value, (str, dict))
            }
        else:
            continue
        if not inputs:
            continue
        for key, value in inputs.items():
            if key in seen:
                continue
            extra: dict[str, Any] = {}
            if isinstance(value, str):
                raw_path = value
            elif isinstance(value, dict):
                raw_path = str(value.get("path") or "")
                extra = dict(value)
            else:
                continue
            if not raw_path:
                continue
            seen.add(key)
            extra.pop("path", None)
            rows.append({"name": key, "declared": raw_path, **extra})
    return rows


def _grade_inputs(run: Path) -> tuple[list[dict[str, Any]], list[str], list[str], list[str]]:
    rows: list[dict[str, Any]] = []
    present: list[str] = []
    missing: list[str] = []
    real_files: list[str] = []
    for item in _iter_declared_inputs(run):
        resolved = _resolve_declared_path(str(item.get("declared") or ""))
        exists = resolved.is_file()
        real_gzip = _is_real_gzip(resolved)
        sha_expected = item.get("sha256")
        sha_actual = _sha256(resolved) if exists and real_gzip else None
        row = {
            "name": item["name"],
            "declared": item["declared"],
            "resolved": str(resolved) if exists else None,
            "exists": exists,
            "real_gzip": real_gzip,
            "sha256_match": (sha_actual == sha_expected) if (sha_expected and sha_actual) else None,
        }
        rows.append(row)
        if exists:
            present.append(str(item["name"]))
        else:
            missing.append(str(item["name"]))
        if real_gzip:
            real_files.append(str(resolved))
    return rows, present, missing, real_files


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

    input_rows, inputs_present, inputs_missing, real_files = _grade_inputs(run)

    return {
        "grader": "file_exists",
        "layer": "B0",
        "status": status,
        "passed": status == "pass",
        "expected": expected,
        "present": present,
        "missing": missing,
        "inputs": input_rows,
        "inputs_present": inputs_present,
        "inputs_missing": inputs_missing,
        "real_files_seen": real_files,
        "task_id": task.get("task_id"),
        "run_dir": str(run),
    }


def grade_paths(task_path: Path | str, run_dir: Path | str) -> dict[str, Any]:
    return grade_file_exists(load_task(Path(task_path)), run_dir)
