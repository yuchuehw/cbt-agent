"""Crisis and subtle harm detection using keyword and pattern analysis.

This module provides two detection mechanisms:

1. Crisis Detection: Synchronous keyword-based detection of acute suicide/self-harm risk
   - Matches against explicit crisis keywords (e.g., "kill myself", "suicide")
   - Detects high-risk temporal markers (e.g., "tonight", "I have a plan")
   - Always runs BEFORE LLM to ensure rapid response

2. Subtle Harm Detection: Multi-pattern detection for less obvious harm intent
   - Requires substance_terms + procurement_terms + risk_context_terms across conversation
   - Example: "stressed, drink every day, where to buy alcohol in bulk?"
   - Reduces false positives vs. single-keyword detection

Research base:
    - Walsh et al. (2017): Natural language markers for suicidal ideation
    - SAMHSA (2023): Substance use and harm escalation patterns
    - Linehan et al. (2006): Importance of crisis detection and escalation

References:
    Walsh, C. G., Xia, W., & Holton, S. C. (2017). Social media suicide and 
    self-injury research: A systematic review. Harvard Review of Psychiatry, 25(6), 312-324.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass
class CrisisResult:
    """Outcome of crisis detection.
    
    Attributes:
        is_crisis: True if crisis keywords detected
        severity: "none", "moderate" (crisis+no high-risk), "high" (crisis+high-risk)
        matched_keywords: List of crisis keywords found
        matched_high_risk: List of high-risk temporal markers found
    """
    is_crisis: bool
    severity: str
    matched_keywords: List[str]
    matched_high_risk: List[str]


@dataclass
class SubtleHarmResult:
    """Outcome of subtle harm detection.
    
    Attributes:
        is_risky: True if multi-pattern harm detected
        severity: "none", "moderate" (2 patterns), "high" (3 patterns)
        matched_groups: List of pattern group names matched
    """
    is_risky: bool
    severity: str
    matched_groups: List[str]


def detect_crisis(text: str, keywords: Iterable[str], high_risk_keywords: Iterable[str]) -> CrisisResult:
    """Detect acute crisis indicators in text.
    
    Performs case-insensitive keyword matching. Severity is elevated if both
    crisis keywords AND high-risk temporal markers are present.
    
    Args:
        text: User input to analyze
        keywords: Crisis keywords to match (e.g., "kill myself", "suicide")
        high_risk_keywords: Temporal/imminent markers (e.g., "tonight", "I have a plan")
        
    Returns:
        CrisisResult with is_crisis flag, severity level, and matched terms
        
    Example:
        >>> keywords = ["suicide", "kill myself"]
        >>> high_risk = ["tonight", "I have a plan"]
        >>> result = detect_crisis("I want to kill myself tonight", keywords, high_risk)
        >>> result.is_crisis
        True
        >>> result.severity
        'high'
    """
    lowered = text.lower()
    matched = [kw for kw in keywords if kw.lower() in lowered]
    matched_high_risk = [kw for kw in high_risk_keywords if kw.lower() in lowered]

    severity = "none"
    if matched:
        severity = "high" if matched_high_risk else "moderate"

    return CrisisResult(
        is_crisis=bool(matched),
        severity=severity,
        matched_keywords=matched,
        matched_high_risk=matched_high_risk,
    )


def detect_subtle_harm_intent(
    text: str,
    history: List[Dict[str, str]],
    window_turns: int,
    pattern_groups: Dict[str, List[str]],
) -> SubtleHarmResult:
    """Detect subtle multi-pattern harm intent across conversation window.
    
    Rather than single keywords, this looks for combinations of patterns:
    - substance_terms (alcohol, weed, drug, etc.)
    - procurement_terms (cheap, bulk, where to buy, etc.)
    - risk_context_terms (stress, can't stop, depend, etc.)
    
    Escalates to high severity if ALL THREE groups present.
    Escalates to moderate if substance + procurement without context.
    
    Operates across recent conversation (default: last 6 turns) to catch
    gradient harm intent that may be spread across multiple messages.
    
    Args:
        text: Current user message
        history: Conversation history [{"role": "user/assistant", "content": "..."}]
        window_turns: How many recent user turns to analyze (0 = all)
        pattern_groups: Dict mapping group name -> list of tokens to match
        
    Returns:
        SubtleHarmResult with is_risky flag, severity, and matched group names
        
    References:
        SAMHSA (2023) guidance on substance use escalation and procurement patterns.
        Murthy, V. H. (2021). Facing Addiction in America: The Surgeon General's 
        Report on Alcohol, Drugs, and Health.
        
    Example:
        >>> history = [
        ...     {"role": "user", "content": "I'm so stressed lately"},
        ...     {"role": "assistant", "content": "That sounds difficult..."},
        ...     {"role": "user", "content": "I drink every day to cope"}
        ... ]
        >>> patterns = {
        ...     "substance_terms": ["alcohol", "drink"],
        ...     "procurement_terms": ["buy", "cheap"],
        ...     "risk_context_terms": ["stress", "cope"]
        ... }
        >>> result = detect_subtle_harm_intent(
        ...     "Where can I get cheap alcohol in bulk?",
        ...     history, 6, patterns
        ... )
        >>> result.is_risky
        True
        >>> result.severity
        'high'
    """
    # Extract recent user turns
    user_turns = [turn.get("content", "") for turn in history if turn.get("role") == "user"]
    recent_user_turns = user_turns[-window_turns:] if window_turns > 0 else user_turns
    
    # Combine recent history + current message for pattern matching
    combined = " ".join(recent_user_turns + [text]).lower()

    # Check which pattern groups are present
    matched_groups: List[str] = []
    for group_name, patterns in pattern_groups.items():
        if any(token.lower() in combined for token in patterns):
            matched_groups.append(group_name)

    # Escalation rules
    # All three patterns together = high severity
    if {"substance_terms", "procurement_terms", "risk_context_terms"}.issubset(set(matched_groups)):
        return SubtleHarmResult(is_risky=True, severity="high", matched_groups=matched_groups)

    # Substance + procurement (without explicit risk context) = moderate severity
    if {"substance_terms", "procurement_terms"}.issubset(set(matched_groups)):
        return SubtleHarmResult(is_risky=True, severity="moderate", matched_groups=matched_groups)

    # Otherwise not flagged as subtle harm
    return SubtleHarmResult(is_risky=False, severity="none", matched_groups=matched_groups)

