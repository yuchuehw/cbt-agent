from __future__ import annotations

from typing import Dict, List


def reflect_user_text(user_text: str) -> str:
    snippet = user_text.strip()
    if len(snippet) > 160:
        snippet = snippet[:157] + "..."
    return f"You are describing: {snippet}"


def summarize_thoughts(turns: List[Dict[str, str]]) -> str:
    user_turns = [t["content"] for t in turns if t.get("role") == "user"]
    if not user_turns:
        return "No user thoughts recorded yet."
    return " | ".join(user_turns[-3:])


def suggest_cbt_exercise(context: str) -> str:
    lowered = context.lower()
    if "avoid" in lowered or "procrast" in lowered:
        return "Behavioral experiment: choose one 5-minute starter task and rate anxiety before/after."
    if "worry" in lowered or "ruminat" in lowered:
        return "Thought log: write one worry, evidence for/against it, and a balanced alternative thought."
    return "Micro-reframe: identify one automatic thought and rewrite it in a more balanced way."

