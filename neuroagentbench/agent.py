"""Agent call contract. Same function as `neuroagentbench evaluate`. No agent start."""

from __future__ import annotations

from typing import Any

from neuroagentbench import evaluate

TOOLS: list[dict[str, Any]] = [
    {
        "name": "evaluate",
        "description": (
            "Score a recorded run tree with L0–L5. "
            "A file can exist and still be a false_success. "
            "Does not start an agent or call a model."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "task": {"type": "string", "description": "Path to task YAML"},
                "run": {"type": "string", "description": "Path to recorded run directory"},
                "seed": {"type": "integer", "description": "Optional seed written onto the score"},
            },
            "required": ["task", "run"],
        },
    }
]


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name != "evaluate":
        raise ValueError(f"unknown tool: {name}")
    seed = arguments.get("seed")
    return evaluate(arguments["task"], arguments["run"], seed=None if seed is None else int(seed))
