from __future__ import annotations

from typing import Any, Dict

from guardrails.policy_engine import policy_allows_tool_call
from tools import therapist_tools

TOOL_REGISTRY = {
    "reflect_user_text": therapist_tools.reflect_user_text,
    "summarize_thoughts": therapist_tools.summarize_thoughts,
    "suggest_cbt_exercise": therapist_tools.suggest_cbt_exercise,
}


def route_tool_call(policy: Dict[str, Any], tool_name: str, args: Dict[str, Any]) -> Any:
    if not policy_allows_tool_call(policy, tool_name):
        raise PermissionError(f"Blocked tool call: {tool_name}")

    tool_fn = TOOL_REGISTRY.get(tool_name)
    if tool_fn is None:
        raise ValueError(f"Unknown tool: {tool_name}")

    return tool_fn(**args)

