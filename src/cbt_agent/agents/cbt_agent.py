"""CBT Agent: Main agent interface for conversational interactions.

This module provides the CbtAgent class, a stateful wrapper around the runtime
that maintains conversation history and enforces policy constraints through
the multi-layer architecture.

Research base:
    - Clark (2011) on evidence-based CBT delivery
    - Cuijpers et al. (2019) on collaborative therapeutic stance
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List

from runtime.agent_loop import run_agent
from runtime.message_schemas import AgentResponse

logger = logging.getLogger(__name__)


@dataclass
class CbtAgent:
    """Stateful CBT conversational agent.
    
    Maintains conversation history and orchestrates the runtime enforcement
    of policy constraints. Each turn:
    1. Loads relevant policy
    2. Detects crisis (synchronous, before LLM)
    3. Detects subtle harm (pattern-based)
    4. Calls LLM with system prompt + history
    5. Validates response against policy
    6. Repairs violations if needed
    7. Optionally suggests tools
    8. Returns annotated response with violations and metadata
    
    Attributes:
        history: List of conversation turns [{"role": "user/assistant", "content": "..."}]
    
    References:
        See docs/ARCHITECTURE.md for detailed flow diagram.
        See docs/RESEARCH.md for citations.
    """

    history: List[Dict[str, str]] = field(default_factory=list)

    def run_turn(self, user_input: str) -> AgentResponse:
        """Process one user turn and return agent response.
        
        Args:
            user_input: User's message text
            
        Returns:
            AgentResponse with:
            - text: The agent's response (after validation/repair)
            - violations: List of policy violations found
            - tool_call: Optional tool invocation (not used in CLI)
            - meta: Metadata including mode (cbt/crisis), risk flags, mhealth_eval
            
        Raises:
            No explicit exceptions; graceful degradation on errors
        """
        # Provide recent history to avoid token limits
        state = {"history": self.history[-20:]}
        
        logger.debug(f"Processing user input: {user_input[:80]}...")
        response = run_agent(user_input=user_input, conversation_state=state)
        
        # Update history with both user and agent messages
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": response.text})
        
        logger.info(f"Turn complete. Mode: {response.meta.get('mode')}, Violations: {len(response.violations)}")
        return response

    def reset(self) -> None:
        """Clear conversation history.
        
        Use this to start a new session without creating a new agent.
        """
        logger.info("Session history cleared")
        self.history.clear()

