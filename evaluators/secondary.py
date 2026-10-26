"""Optional SciCap/SciGuard flags. Not this paper's oracle.

When sibling packages import, record their decision or status on the score.
When they do not import, or no mapped fixture exists, record not_run.
Never fake PASS. Never overwrite L0–L5, scientific_valid, or false_success.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Callable

_ROOT = Path(__file__).resolve().parents[1]
_WORKSPACE = _ROOT.parent
_SCICAP_ROOT = _WORKSPACE / "01_SciCap"
_SCICAP_CORE = _SCICAP_ROOT / "packages" / "scicap-core"
_SCIGUARD_ROOT = _WORKSPACE / "02_SciGuard"

# Task-level sibling fixtures only. These are B7 secondary arms, not gold.
_SCICAP_BINDINGS = {
    "nab-valid-stub": (
        _SCICAP_ROOT
        / "packages"
        / "scicap-neuro"
        / "capabilities"
        / "neuro.t1.hippocampal_volumes.yaml",
        _SCICAP_ROOT / "examples" / "instances" / "complete_t1w.json",
    ),
}
_SCIGUARD_FIXTURES = {
    "nab-labels-on-dwi": (
        _SCIGUARD_ROOT / "fixtures" / "invalid" / "labels_t1w_to_dwi_no_transform.yaml"
    ),
}

_SCICAP_DECISIONS = frozenset({"ALLOW", "REJECT", "ABSTAIN"})


def secondary_flags(task: dict[str, Any]) -> dict[str, Any]:
    """Attach SciCap/SciGuard flags. oracle is always false."""
    scicap = _scicap_flag(task)
    sciguard = _sciguard_flag(task)
    return {
        "scicap_decision": scicap["decision"],
        "sciguard_status": sciguard["status"],
        "scicap_importable": scicap["importable"],
        "sciguard_importable": sciguard["importable"],
        "oracle": False,
    }


def _append_sys_path(path: Path) -> None:
    text = str(path)
    if text not in sys.path:
        sys.path.append(text)


def _scicap_flag(task: dict[str, Any]) -> dict[str, Any]:
    invoke_fn = _load_scicap_invoke()
    if invoke_fn is None:
        return {"decision": "not_run", "importable": False}
    binding = _SCICAP_BINDINGS.get(str(task.get("task_id") or ""))
    if binding is None or not binding[0].is_file() or not binding[1].is_file():
        return {"decision": "not_run", "importable": True}
    try:
        result = invoke_fn(binding[0], binding[1])
    except Exception:  # noqa: BLE001 — sibling may raise; never fake ALLOW/PASS
        return {"decision": "not_run", "importable": True}
    decision = str((result or {}).get("decision") or "not_run")
    if decision not in _SCICAP_DECISIONS:
        decision = "not_run"
    return {"decision": decision, "importable": True}


def _sciguard_flag(task: dict[str, Any]) -> dict[str, Any]:
    validate_fn = _load_sciguard_validate()
    if validate_fn is None:
        return {"status": "not_run", "importable": False}
    fixture = _SCIGUARD_FIXTURES.get(str(task.get("task_id") or ""))
    if fixture is None or not fixture.is_file():
        return {"status": "not_run", "importable": True}
    try:
        report = validate_fn(fixture)
    except Exception:  # noqa: BLE001 — sibling may raise; never fake PASS
        return {"status": "not_run", "importable": True}
    return {"status": _status_from_sciguard(report), "importable": True}


def _status_from_sciguard(report: dict[str, Any] | None) -> str:
    if not isinstance(report, dict):
        return "not_run"
    edges = report.get("edges") or []
    statuses = [str(item.get("status") or "") for item in edges if isinstance(item, dict)]
    if "FAIL" in statuses or report.get("graph_status") == "reject":
        return "FAIL"
    if "UNKNOWN" in statuses:
        return "UNKNOWN"
    if "NEEDS_REVIEW" in statuses:
        return "NEEDS_REVIEW"
    if statuses and all(status == "PASS" for status in statuses):
        return "PASS"
    return "not_run"


def _load_scicap_invoke() -> Callable[..., Any] | None:
    try:
        import scicap as pkg  # type: ignore

        fn = getattr(pkg, "invoke", None)
        if callable(fn):
            return fn
    except ImportError:
        pass
    _preload_scicap_core()
    _append_sys_path(_SCICAP_ROOT)
    try:
        import scicap as sibling  # type: ignore

        fn = getattr(sibling, "invoke", None)
        if callable(fn):
            return fn
    except ImportError:
        pass
    try:
        from scicap_core.invoke import invoke as core_invoke  # type: ignore

        return core_invoke
    except ImportError:
        return None


def _preload_scicap_core() -> None:
    init = _SCICAP_CORE / "__init__.py"
    if not init.is_file() or "scicap_core" in sys.modules:
        return
    spec = importlib.util.spec_from_file_location(
        "scicap_core",
        init,
        submodule_search_locations=[str(_SCICAP_CORE)],
    )
    if spec is None or spec.loader is None:
        return
    module = importlib.util.module_from_spec(spec)
    sys.modules["scicap_core"] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop("scicap_core", None)


def _load_sciguard_validate() -> Callable[..., Any] | None:
    try:
        import sciguard as pkg  # type: ignore

        fn = getattr(pkg, "validate", None) or getattr(pkg, "check_workflow", None)
        if callable(fn):
            return fn
    except ImportError:
        pass
    if _SCIGUARD_ROOT.is_dir():
        _append_sys_path(_SCIGUARD_ROOT)
        try:
            import sciguard as sibling  # type: ignore

            fn = getattr(sibling, "validate", None) or getattr(
                sibling, "check_workflow", None
            )
            if callable(fn):
                return fn
        except ImportError:
            pass
        try:
            from validation.check import check_workflow

            return check_workflow
        except ImportError:
            return None
    return None
