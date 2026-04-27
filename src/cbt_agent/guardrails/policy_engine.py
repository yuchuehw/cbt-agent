"""Policy loading and tool access control.

This module manages the machine-readable policy file (`cbt_policy.json`), which
serves as the executable contract for agent behavior. The policy defines:

- Interpretation limits: max hypotheses, require user context before interpreting
- Response style: no generic/deceptive empathy, max questions, tentative language
- CBT constraints: max interventions, require context citation
- Risk controls: block gaslighting, abandonment, over-validation; require check-ins
- Fairness: cultural humility signals, identity-aware responses
- Safety: crisis keywords, subtle harm patterns, escalation rules
- Trustworthiness: verified resources, region-aware defaults
- Tools: whitelist of allowed tool names (prevents prompt injection)

The policy is loaded once at startup and used by all runtime components to
enforce constraints. See docs/ARCHITECTURE.md for detailed explanation.

Research base:
    - Christiano et al. (2016): Tool whitelisting as safety mechanism
    - Fitzpatrick et al. (2017): MHealth-EVAL framework for evaluation
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_POLICY_PATH = BASE_DIR / "policies" / "cbt_policy.json"


def load_policy(path: Path = DEFAULT_POLICY_PATH) -> Dict[str, Any]:
    """Load and return the policy JSON file.
    
    The policy file is machine-readable YAML that enforces guardrails at runtime.
    It is loaded once per session and used by validators, crisis detection, and
    tool routing to ensure consistent behavior.
    
    Args:
        path: Path to policy JSON file (defaults to policies/cbt_policy.json)
        
    Returns:
        Dict containing all policy constraints and rules
        
    Raises:
        FileNotFoundError: If policy file does not exist
        json.JSONDecodeError: If policy JSON is malformed
        
    Example:
        >>> policy = load_policy()
        >>> max_questions = policy["response_style"]["max_questions_per_turn"]
        >>> crisis_keywords = policy["safety"]["crisis_keywords"]
    """
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def policy_allows_tool_call(policy: Dict[str, Any], tool_name: str) -> bool:
    """Check if a specific tool is allowed by policy.
    
    This implements a whitelist approach: tools must be explicitly listed
    in policy["tools"]["allowed"]. This prevents prompt injection attacks
    that might try to invoke unauthorized tools.
    
    Args:
        policy: Loaded policy dict
        tool_name: Name of tool to check (e.g., "suggest_cbt_exercise")
        
    Returns:
        True if tool is in allowed list, False otherwise
        
    References:
        Christiano et al. (2016). The case for aligning artificial intelligence
        with human values. arXiv preprint arXiv:1606.06565.
        
    Example:
        >>> policy = load_policy()
        >>> policy_allows_tool_call(policy, "suggest_cbt_exercise")
        True
        >>> policy_allows_tool_call(policy, "send_email")  # not whitelisted
        False
    """
    allowed = policy.get("tools", {}).get("allowed", [])
    return tool_name in allowed
