from __future__ import annotations

import os
import importlib
from pathlib import Path
from typing import Any, Dict, List, Optional

from cbt_agent.guardrails.crisis_detector import detect_crisis, detect_subtle_harm_intent
from cbt_agent.guardrails.policy_engine import load_policy
from cbt_agent.guardrails.validators import evaluate_mhealth_eval, repair_response, validate
from cbt_agent.runtime.message_schemas import AgentResponse
from cbt_agent.runtime.tool_router import route_tool_call
from cbt_agent.tools.safety_tools import build_crisis_response, build_subtle_risk_response
from cbt_agent.memory import MemoryManager

BASE_DIR = Path(__file__).resolve().parents[1]
PROMPT_PATH = BASE_DIR / "prompts" / "system_prompt.md"


def load_system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def build_messages(system_prompt: str, conversation_state: Dict[str, Any], user_input: str, memory_context: Optional[Dict[str, str]] = None) -> List[Dict[str, str]]:
    """Build message list for LLM, optionally including memory context."""
    messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]

    # Add memory context if available
    if memory_context:
        memory_summary = "\n".join([f"{k}: {v}" for k, v in memory_context.items()])
        messages.append({
            "role": "system",
            "content": f"User context:\n{memory_summary}"
        })

    history = conversation_state.get("history", [])
    messages.extend(history)
    messages.append({"role": "user", "content": user_input})
    return messages


def llm_call(messages: List[Dict[str, str]]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        # Optional live path when API credentials are present.
        openai_module = importlib.import_module("openai")
        OpenAI = getattr(openai_module, "OpenAI")
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            input=messages,
            temperature=0.4,
        )
        return response.output_text.strip()

    user_text = messages[-1]["content"]
    return (
        f"You mentioned '{user_text}'. One possibility is this thought is carrying a lot of pressure. "
        "Would you like to test one small experiment this week?"
    )


def run_agent(user_input: str, conversation_state: Dict[str, Any], memory_manager: Optional[MemoryManager] = None) -> AgentResponse:
    """Run agent with integrated memory system.

    Args:
        user_input: User's message
        conversation_state: Current state including history
        memory_manager: Optional memory manager for persistent context

    Returns:
        AgentResponse with violations, metadata, and memory updates
    """
    policy = load_policy()
    history = conversation_state.get("history", [])

    # Detect crisis
    crisis = detect_crisis(
        user_input,
        policy["safety"].get("crisis_keywords", []),
        policy["safety"].get("high_risk_keywords", []),
    )

    # Update memory with user input (if available)
    if memory_manager:
        memory_manager.update_for_message("user", user_input, is_crisis=crisis.is_crisis)

    if crisis.is_crisis and policy["safety"].get("override_cbt_mode_on_crisis", True):
        crisis_text = build_crisis_response()

        if memory_manager:
            memory_manager.update_for_message("assistant", crisis_text, is_crisis=True)

        mhealth_eval = evaluate_mhealth_eval(
            response_text=crisis_text,
            user_input=user_input,
            policy=policy,
            violations=[],
            mode="crisis",
            subtle_harm_detected=False,
        )
        return AgentResponse(
            text=crisis_text,
            meta={
                "mode": "crisis",
                "severity": crisis.severity,
                "matched_keywords": crisis.matched_keywords,
                "matched_high_risk": crisis.matched_high_risk,
                "mhealth_eval": mhealth_eval,
                "memory": memory_manager.get_memory_stats() if memory_manager else None,
            },
        )

    # Detect subtle harm
    subtle_harm = detect_subtle_harm_intent(
        text=user_input,
        history=history,
        window_turns=policy.get("safety", {}).get("subtle_harm_window_turns", 6),
        pattern_groups=policy.get("safety", {}).get("subtle_harm_patterns", {}),
    )
    if subtle_harm.is_risky and policy.get("safety", {}).get("escalate_on_subtle_harm_intent", True):
        subtle_text = build_subtle_risk_response()

        if memory_manager:
            memory_manager.update_for_message("assistant", subtle_text, is_crisis=True)

        mhealth_eval = evaluate_mhealth_eval(
            response_text=subtle_text,
            user_input=user_input,
            policy=policy,
            violations=[],
            mode="crisis",
            subtle_harm_detected=True,
        )
        return AgentResponse(
            text=subtle_text,
            meta={
                "mode": "crisis",
                "severity": subtle_harm.severity,
                "subtle_harm": True,
                "matched_subtle_groups": subtle_harm.matched_groups,
                "mhealth_eval": mhealth_eval,
                "memory": memory_manager.get_memory_stats() if memory_manager else None,
            },
        )

    # Get memory context for LLM
    memory_context = memory_manager.get_context_for_llm() if memory_manager else None

    # Build messages with memory context
    messages = build_messages(load_system_prompt(), conversation_state, user_input, memory_context)
    response_text = llm_call(messages)

    # Validate and repair response
    violations = validate(response_text, policy, user_input=user_input)
    if violations:
        response_text = repair_response(response_text, violations, user_input=user_input)

    # Update memory with assistant response
    if memory_manager:
        memory_manager.update_for_message("assistant", response_text)

    # Evaluate response
    mhealth_eval = evaluate_mhealth_eval(
        response_text=response_text,
        user_input=user_input,
        policy=policy,
        violations=violations,
        mode="cbt",
        subtle_harm_detected=subtle_harm.is_risky,
    )

    # Optional tool suggestion
    if any(token in user_input.lower() for token in ["exercise", "try", "plan"]):
        suggestion = route_tool_call(policy, "suggest_cbt_exercise", {"context": user_input})
        response_text = f"{response_text}\n\nSuggested next step: {suggestion}"

    return AgentResponse(
        text=response_text,
        violations=violations,
        meta={
            "mode": "cbt",
            "risk_flags": violations,
            "mhealth_eval": mhealth_eval,
            "memory": memory_manager.get_memory_stats() if memory_manager else None,
        },
    )


