"""Optional stdio MCP transport. Calls neuroagentbench.evaluate only.

Not a Coala/Nipoppy product. Does not start an agent. No model API.
"""

from __future__ import annotations

from neuroagentbench import __version__
from neuroagentbench.agent import TOOLS, call_tool
from neuroagentbench.mcp_stdio import handle_message as _handle
from neuroagentbench.mcp_stdio import serve

SERVER = "neuroagentbench"


def handle_message(message: dict) -> dict | None:
    return _handle(
        message,
        name=SERVER,
        version=__version__,
        tools=TOOLS,
        call_tool=call_tool,
    )


def main() -> None:
    serve(name=SERVER, version=__version__, tools=TOOLS, call_tool=call_tool)


if __name__ == "__main__":
    main()
