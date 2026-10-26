"""Public import, agent tool, optional MCP. No model API. No agent start."""

from __future__ import annotations

import os
from pathlib import Path

from neuroagentbench import evaluate
from neuroagentbench.agent import TOOLS, call_tool
from neuroagentbench.mcp import handle_message

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "tasks/connectome/nab-atlas-wrong.yaml"
RUN = ROOT / "examples/runs/atlas-wrong"


def test_public_evaluate_false_success() -> None:
    os.environ.pop("OPENAI_API_KEY", None)
    score = evaluate(TASK, RUN)
    assert score["false_success"] is True


def test_agent_tool_matches_evaluate() -> None:
    via = call_tool("evaluate", {"task": str(TASK), "run": str(RUN)})
    assert via["false_success"] is True
    assert {tool["name"] for tool in TOOLS} == {"evaluate"}
    assert "run" not in {tool["name"] for tool in TOOLS}


def test_mcp_tools_call_evaluate() -> None:
    listed = handle_message({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    assert [tool["name"] for tool in listed["result"]["tools"]] == ["evaluate"]
    called = handle_message(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "evaluate",
                "arguments": {"task": str(TASK), "run": str(RUN)},
            },
        }
    )
    assert called["result"]["isError"] is False
    assert "false_success" in called["result"]["content"][0]["text"]
