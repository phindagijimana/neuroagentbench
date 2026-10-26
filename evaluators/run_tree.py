"""Load a recorded run tree (JSON + placeholder files). No MRI bytes."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _exists(path: Path) -> bool:
    return path.is_file()


@dataclass
class RunRecord:
    path: Path
    claim: dict[str, Any] = field(default_factory=dict)
    tools: dict[str, Any] = field(default_factory=dict)
    commands: dict[str, Any] = field(default_factory=dict)
    scientific: dict[str, Any] = field(default_factory=dict)
    qc: dict[str, Any] = field(default_factory=dict)
    provenance: dict[str, Any] = field(default_factory=dict)
    evidence_manifest: dict[str, Any] = field(default_factory=dict)

    @property
    def run_id(self) -> str:
        return str(self.claim.get("run_id") or self.path.name)

    @property
    def agent_id(self) -> str:
        return str(self.claim.get("agent_id") or "recorded-fake")

    @property
    def scaffold_id(self) -> str:
        return str(self.claim.get("scaffold_id") or "recorded-v0")

    @property
    def seed(self) -> int:
        return int(self.claim.get("seed", 0))

    @property
    def agent_claimed_success(self) -> bool:
        return bool(self.claim.get("agent_claimed_success", False))

    @property
    def gold_action_taken(self) -> str:
        return str(self.claim.get("gold_action_taken") or "complete")

    @property
    def tools_used(self) -> list[str]:
        used = self.tools.get("tools_used") or []
        return [str(item) for item in used]

    @property
    def network_used(self) -> bool:
        return bool(self.tools.get("network_used", False))

    @property
    def prohibited_taken(self) -> list[str]:
        taken = self.tools.get("prohibited_taken") or []
        return [str(item) for item in taken]

    def artifact_path(self, name: str) -> Path:
        return self.path / "artifacts" / name

    def evidence_candidates(self, name: str) -> list[Path]:
        return [
            self.path / "evidence" / name,
            self.path / "evidence" / f"{name}.json",
            self.path / "artifacts" / name,
            self.path / "artifacts" / f"{name}.json",
        ]

    def has_file(self, name: str) -> bool:
        return any(_exists(candidate) for candidate in self.evidence_candidates(name))

    def evidence_present(self, name: str) -> bool:
        listed = self.evidence_manifest.get("present") or []
        if listed and name in listed and self.has_file(name):
            return True
        return self.has_file(name)


def load_run(run_dir: Path) -> RunRecord:
    root = Path(run_dir)
    if not root.is_dir():
        raise FileNotFoundError(f"run directory not found: {root}")
    return RunRecord(
        path=root,
        claim=_read_json(root / "claim.json"),
        tools=_read_json(root / "tools.json"),
        commands=_read_json(root / "commands.json"),
        scientific=_read_json(root / "scientific.json"),
        qc=_read_json(root / "qc.json"),
        provenance=_read_json(root / "provenance.json"),
        evidence_manifest=_read_json(root / "evidence.json"),
    )


def load_task(task_path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("PyYAML is required to load task manifests") from exc
    with Path(task_path).open(encoding="utf-8") as handle:
        task = yaml.safe_load(handle)
    if not isinstance(task, dict):
        raise ValueError(f"{task_path} must contain a mapping")
    return task
