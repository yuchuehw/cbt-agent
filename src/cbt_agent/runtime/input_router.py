from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class RoutedInput:
    route: str
    payload: str = ""
    command: str = ""
    args: Dict[str, str] | None = None


def parse_input(raw_text: str) -> RoutedInput:
    text = raw_text.strip()
    if not text.startswith("/"):
        return RoutedInput(route="direct", payload=text)

    command_parts = text.split(maxsplit=1)
    command = command_parts[0].lower()

    if command == "/cbt":
        payload = command_parts[1] if len(command_parts) > 1 else ""
        return RoutedInput(route="direct", payload=payload)

    if command == "/tool":
        parts = text.split(maxsplit=2)
        tool_name = parts[1] if len(parts) > 1 else ""
        tool_input = parts[2] if len(parts) > 2 else ""
        return RoutedInput(route="command", command="tool", args={"name": tool_name, "input": tool_input})

    if command in {"/help", "/reset", "/exit", "/quit", "/memory"}:
        return RoutedInput(route="command", command=command.lstrip("/"), args={})

    # Unknown slash text falls back to direct mode so content is not lost.
    return RoutedInput(route="direct", payload=text)


