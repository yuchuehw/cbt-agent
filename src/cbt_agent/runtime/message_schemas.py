from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ToolCall:
    name: str
    args: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResponse:
    text: str
    violations: List[str] = field(default_factory=list)
    tool_call: Optional[ToolCall] = None
    meta: Dict[str, Any] = field(default_factory=dict)

