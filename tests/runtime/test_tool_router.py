from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from cbt_agent.runtime.tool_router import route_tool_call


def test_route_tool_call_uses_package_imports_and_routes_allowed_tool() -> None:
    policy = {"tools": {"allowed": ["suggest_cbt_exercise"]}}

    result = route_tool_call(
        policy,
        "suggest_cbt_exercise",
        {"context": "I keep worrying and ruminating about work."},
    )

    assert "Thought log" in result
