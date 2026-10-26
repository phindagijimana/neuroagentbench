"""CLI: evaluate recorded trees and list the pilot suite. Dry-run run refuses without a tree."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from evaluators.run_tree import load_task
from evaluators.score import evaluate_paths

_ROOT = Path(__file__).resolve().parents[1]
_TASKS = _ROOT / "tasks"


def _iter_tasks() -> list[Path]:
    return sorted(path for path in _TASKS.rglob("*.yaml") if "holdout" not in path.parts)


def cmd_evaluate(args: argparse.Namespace) -> int:
    score = evaluate_paths(Path(args.task), Path(args.run), seed=args.seed)
    json.dump(score, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    """Refuse to start an agent. Optional --from-recorded aliases evaluate."""
    if args.from_recorded:
        score = evaluate_paths(Path(args.task), Path(args.from_recorded), seed=args.seed)
        json.dump(score, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0
    payload = {
        "ok": False,
        "reason": "evaluate_first_no_agent",
        "message": "neuroagentbench run refuses without a recorded tree; evaluate first. No model or agent is started.",
    }
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 1


def cmd_list(args: argparse.Namespace) -> int:
    rows = []
    for path in _iter_tasks():
        task = load_task(path)
        if args.suite and task.get("suite") != args.suite:
            continue
        rows.append(
            {
                "task_id": task.get("task_id"),
                "split": task.get("split"),
                "gold_action": task.get("gold_action"),
                "llm_judge_primary": task.get("llm_judge_primary"),
                "path": str(path.relative_to(_ROOT)),
            }
        )
    json.dump(rows, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="neuroagentbench")
    sub = parser.add_subparsers(dest="command", required=True)

    evaluate = sub.add_parser("evaluate", help="score a recorded run tree")
    evaluate.add_argument("--task", required=True, help="path to task YAML")
    evaluate.add_argument("--run", required=True, help="path to recorded run directory")
    evaluate.add_argument("--seed", type=int, default=None, help="write seed onto the score record (B6)")
    evaluate.set_defaults(func=cmd_evaluate)

    run = sub.add_parser("run", help="dry-run: refuse unless a recorded tree is supplied")
    run.add_argument("--task", required=True, help="path to task YAML")
    run.add_argument(
        "--from-recorded",
        dest="from_recorded",
        default=None,
        help="alias evaluate on this recorded tree; do not start an agent",
    )
    run.add_argument("--seed", type=int, default=None, help="write seed when --from-recorded is used")
    run.set_defaults(func=cmd_run)

    listing = sub.add_parser("list", help="list tasks in a suite")
    listing.add_argument("--suite", default="pilot-v0")
    listing.set_defaults(func=cmd_list)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
