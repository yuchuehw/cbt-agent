"""CBT Agent CLI - Interactive conversation interface with persistent memory.

Usage:
    python main.py

Commands:
    /cbt <message>              Send CBT message
    /tool <name> <input>        Call a specific tool
    /reset                      Clear session (saves to persistent memory)
    /help                       Show available commands
    /exit, /quit                Exit the program

Features:
    - Persistent cross-session memory (themes, breakthroughs, patterns)
    - Time-aware conversations (duration tracking, turn counts)
    - Smart context management (adaptive conversation window)
    - Multi-user support (each user has separate memory)
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from cbt_agent.agents.cbt_agent import CbtAgent
from cbt_agent.guardrails.policy_engine import load_policy
from cbt_agent.runtime.input_router import parse_input
from cbt_agent.runtime.tool_router import route_tool_call

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the CBT Agent CLI with memory persistence."""
    print("\n" + "="*60)
    print("CBT Agent - With Persistent Memory")
    print("="*60)
    print("Type '/help' for commands. Your conversations are saved.")
    print("="*60 + "\n")

    # Initialize agent with persistent memory (default user)
    agent = CbtAgent(user_id="cli_user")
    policy = load_policy()

    logger.info("CBT Agent CLI started")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Parse user input (commands vs. messages)
            routed = parse_input(user_input)

            # Handle commands
            if routed.route == "command":
                if routed.command in {"exit", "quit"}:
                    # Save session before exiting
                    agent.reset()
                    print("\nAgent: Thank you for our conversation. Take care. Goodbye.")
                    logger.info("User exited program")
                    break

                if routed.command == "help":
                    print("\nAgent: Available commands:")
                    print("  /cbt <message>          - Send a CBT conversation message")
                    print("  /tool <name> <input>    - Use a specific tool")
                    print("  /reset                  - End session (saves memory)")
                    print("  /exit, /quit            - Exit the program")
                    print("  /memory                 - Show memory summary")
                    print("  /help                   - Show this help message")
                    print()
                    continue

                if routed.command == "reset":
                    agent.reset()
                    print("\nAgent: Session ended and saved to persistent memory.")
                    print("Starting fresh session (your themes & breakthroughs are remembered)\n")
                    logger.info("Session reset - memory saved")
                    continue

                if routed.command == "memory":
                    summary = agent.get_memory_summary()
                    print("\nAgent: Memory Summary:")
                    print(f"  Themes: {summary.get('semantic', {}).get('themes', [])}")
                    print(f"  Breakthroughs: {len(summary.get('semantic', {}).get('breakthroughs', []))}")
                    print(f"  Past sessions: {summary.get('episodic', {}).get('past_sessions', 0)}")
                    print(f"  Current session: {summary.get('time', {}).get('session_duration_minutes', 0):.1f} minutes")
                    print()
                    continue

                if routed.command == "tool":
                    tool_name = routed.args.get("name", "") if routed.args else ""
                    tool_input = routed.args.get("input", "") if routed.args else ""

                    if not tool_name:
                        print("Agent: Tool not specified. Use: /tool <name> <input>\n")
                        continue

                    try:
                        if tool_name == "suggest_cbt_exercise":
                            result = route_tool_call(policy, tool_name, {"context": tool_input})
                        elif tool_name == "reflect_user_text":
                            result = route_tool_call(policy, tool_name, {"user_text": tool_input})
                        else:
                            result = f"Tool '{tool_name}' not found. Available: suggest_cbt_exercise, reflect_user_text"

                        print(f"\nAgent: {result}\n")
                    except Exception as e:
                        print(f"\nAgent: Error calling tool: {e}\n")
                        logger.error(f"Tool error: {e}")
                    continue

            # Handle CBT conversation messages
            try:
                response = agent.run_turn(routed.payload)
                print(f"\nAgent: {response.text}")

                # Optionally show memory stats
                if response.meta.get("memory"):
                    mem = response.meta["memory"]
                    print(f"\n[Memory: {mem['semantic_themes']} themes, "
                          f"{mem['breakthroughs']} breakthroughs, "
                          f"{mem['past_sessions']} past sessions]\n")
                else:
                    print()

            except Exception as e:
                print(f"\nAgent: I encountered an error: {e}")
                print("Please try again.\n")
                logger.error(f"Error processing message: {e}", exc_info=True)

        except KeyboardInterrupt:
            print("\n\nAgent: Interrupted. Saving your session...")
            agent.reset()
            print("Goodbye!")
            logger.info("User interrupted - memory saved")
            break
        except EOFError:
            # Handle end of input (e.g., piped input)
            print("\nAgent: End of input. Saving session. Goodbye.")
            agent.reset()
            logger.info("EOF reached - memory saved")
            break


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()

