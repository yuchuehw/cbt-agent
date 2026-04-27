from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))


from cbt_agent.agents.cbt_agent import CbtAgent
from cbt_agent.guardrails.policy_engine import load_policy
from cbt_agent.runtime.input_router import parse_input
from cbt_agent.runtime.tool_router import route_tool_call


def main() -> None:
    print("CBT agent is running. Type '/help' for commands.")
    agent = CbtAgent()
    policy = load_policy()

    while True:
        user_input = input("User: ").strip()
        routed = parse_input(user_input)

        if routed.route == "command":
            if routed.command in {"exit", "quit"}:
                print("Agent: Take care. Goodbye.")
                break

            if routed.command == "help":
                print("Agent: Commands: /cbt <text>, /tool <name> <input>, /reset, /exit")
                continue

            if routed.command == "reset":
                agent.reset()
                print("Agent: Session history cleared.")
                continue

            if routed.command == "tool":
                tool_name = routed.args.get("name", "") if routed.args else ""
                tool_input = routed.args.get("input", "") if routed.args else ""

                if tool_name == "suggest_cbt_exercise":
                    result = route_tool_call(policy, tool_name, {"context": tool_input})
                elif tool_name == "reflect_user_text":
                    result = route_tool_call(policy, tool_name, {"user_text": tool_input})
                else:
                    result = "Unsupported tool for CLI command."

                print(f"Agent: {result}")
                continue

        response = agent.run_turn(routed.payload)
        print(f"Agent: {response.text}")


if __name__ == "__main__":
    main()

