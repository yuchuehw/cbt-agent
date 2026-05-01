"""CBT Agent: Main agent interface for conversational interactions.

This module provides the CbtAgent class, a stateful wrapper around the runtime
that maintains conversation history and enforces policy constraints through
the multi-layer architecture. Now includes persistent memory management.

Research base:
    - Clark (2011) on evidence-based CBT delivery
    - Cuijpers et al. (2019) on collaborative therapeutic stance
    - LangChain memory architecture (modular approach)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from cbt_agent.runtime.agent_loop import run_agent
from cbt_agent.runtime.message_schemas import AgentResponse
from cbt_agent.memory import MemoryManager

logger = logging.getLogger(__name__)


@dataclass
class CbtAgent:
    """Stateful CBT conversational agent with persistent memory.

    Maintains conversation history and orchestrates the runtime enforcement
    of policy constraints through the multi-layer architecture. Now includes:
    - Persistent memory (semantic, episodic)
    - Time awareness (session duration, message frequency)
    - Smart conversation window (adaptive vs. fixed)
    - Cross-session context retrieval

    Each turn:
    1. Loads relevant policy
    2. Updates memory system with user input
    3. Detects crisis (synchronous, before LLM)
    4. Detects subtle harm (pattern-based)
    5. Enriches LLM context with memory
    6. Calls LLM with system prompt + history + memory context
    7. Updates memory with response
    8. Validates response against policy
    9. Repairs violations if needed
    10. Optionally suggests tools
    11. Returns annotated response with violations, metadata, and memory stats

    Attributes:
        user_id: Unique identifier for persistent memory
        history: List of conversation turns [{"role": "user/assistant", "content": "..."}]
        memory_manager: Manages semantic, episodic, and working memory
        memory_dir: Directory for persistent memory storage

    References:
        See docs/ARCHITECTURE.md for detailed flow diagram.
        See docs/RESEARCH.md for citations.
    """

    user_id: str = field(default="default")
    history: List[Dict[str, str]] = field(default_factory=list)
    memory_manager: Optional[MemoryManager] = field(default=None, init=False)
    memory_dir: Path = field(default_factory=lambda: Path("memory_storage"))

    def __post_init__(self) -> None:
        """Initialize memory manager after dataclass initialization."""
        self.memory_manager = MemoryManager(
            user_id=self.user_id,
            storage_dir=self.memory_dir
        )
        logger.info(f"CbtAgent initialized with persistent memory for user {self.user_id}")

    def run_turn(self, user_input: str) -> AgentResponse:
        """Process one user turn and return agent response.

        Args:
            user_input: User's message text

        Returns:
            AgentResponse with:
            - text: The agent's response (after validation/repair)
            - violations: List of policy violations found
            - tool_call: Optional tool invocation (not used in CLI)
            - meta: Metadata including:
              - mode: cbt or crisis
              - risk_flags: Policy violations
              - mhealth_eval: Evaluation metrics
              - memory: Memory statistics (themes, breakthroughs, sessions)

        Raises:
            No explicit exceptions; graceful degradation on errors
        """
        # Provide recent history (used as fallback if memory unavailable)
        state = {"history": self.history[-20:]}

        logger.debug(f"Processing user input: {user_input[:80]}...")

        # Run agent with memory manager
        response = run_agent(
            user_input=user_input,
            conversation_state=state,
            memory_manager=self.memory_manager
        )

        # Update local history
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": response.text})

        # Log turn completion with memory stats
        memory_stats = self.memory_manager.get_memory_stats()
        logger.info(
            f"Turn complete. Mode: {response.meta.get('mode')}, "
            f"Violations: {len(response.violations)}, "
            f"Memory: {memory_stats['current_working_memory_size']} messages, "
            f"Themes: {memory_stats['semantic_themes']}, "
            f"Sessions: {memory_stats['past_sessions']}"
        )

        return response

    def reset(self) -> None:
        """Clear session history but preserve persistent memory.

        Ends current session in memory manager and starts a new one.
        Persistent semantic and episodic memory are preserved.
        """
        # End current session
        if self.memory_manager:
            session_summary = f"Session with {len(self.history)} messages"
            self.memory_manager.end_session(summary=session_summary)
            self.memory_manager.start_new_session()

        # Clear local history
        self.history.clear()

        logger.info(f"Session reset for user {self.user_id}. Persistent memory preserved.")

    def get_memory_summary(self) -> Dict[str, any]:
        """Get comprehensive memory summary for debugging/monitoring.

        Returns:
            Dictionary with:
            - semantic: Themes, breakthroughs, patterns
            - episodic: Past sessions and cross-session patterns
            - working: Current conversation context
            - time: Session duration and turn count
        """
        if not self.memory_manager:
            return {}

        return {
            "semantic": {
                "themes": self.memory_manager.semantic.get_top_themes(5),
                "breakthroughs": self.memory_manager.semantic.breakthroughs[:5],
            },
            "episodic": {
                "past_sessions": len(self.memory_manager.episodic.sessions),
                "recent_sessions": self.memory_manager.episodic.get_recent_sessions(2),
                "cross_session_patterns": self.memory_manager.episodic.get_cross_session_patterns(),
            },
            "working": {
                "current_messages": len(self.memory_manager.working.current_session),
                "summary": self.memory_manager.working.to_summary(),
            },
            "time": {
                "session_start": self.memory_manager.time_metadata.session_start,
                "total_turns": self.memory_manager.time_metadata.total_turns,
                "session_duration_minutes": self.memory_manager.time_metadata.session_duration_minutes,
            },
        }


