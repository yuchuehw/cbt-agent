"""Memory management system for CBT-Agent.

Provides multi-layer memory system with persistent storage:
- Semantic Memory: Extracts and stores key themes, breakthroughs, patterns
- Episodic Memory: Session summaries and cross-session context
- Working Memory: Smart conversation window (optimized vs. fixed 20-turn)
- Time Awareness: Tracks conversation timing and patterns
- Persistent Storage: JSON-based storage for transparency

Research base:
    - LangChain memory architecture (modular approach)
    - Cognitive science on memory types (Tulving, 1972)
    - Session-based memory patterns from Claude/OpenAI Assistants
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class TimeMetadata:
    """Track conversation timing information."""

    session_start: str  # ISO format datetime
    session_end: Optional[str] = None
    total_turns: int = 0
    total_duration_seconds: int = 0
    last_message_time: Optional[str] = None

    @property
    def session_duration_minutes(self) -> float:
        """Calculate session duration in minutes."""
        if self.session_end:
            start = datetime.fromisoformat(self.session_start)
            end = datetime.fromisoformat(self.session_end)
            return (end - start).total_seconds() / 60
        return 0.0

    @property
    def time_since_last_message(self) -> Optional[float]:
        """Minutes since last message (if session is ongoing)."""
        if self.last_message_time and not self.session_end:
            last = datetime.fromisoformat(self.last_message_time)
            now = datetime.now()
            return (now - last).total_seconds() / 60
        return None

    def to_summary(self) -> str:
        """Generate human-readable summary of session timing."""
        duration = self.session_duration_minutes
        hours = int(duration // 60)
        minutes = int(duration % 60)

        if hours > 0:
            return f"Session: {hours}h {minutes}m, {self.total_turns} messages"
        return f"Session: {minutes}m, {self.total_turns} messages"


@dataclass
class SemanticMemory:
    """Extract and store key themes, patterns, and breakthroughs."""

    themes: Dict[str, int] = field(default_factory=dict)  # Theme -> frequency
    breakthroughs: List[str] = field(default_factory=list)  # Key insights
    patterns: Dict[str, Any] = field(default_factory=dict)  # User patterns
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())

    def add_theme(self, theme: str) -> None:
        """Register a theme and increment frequency."""
        self.themes[theme] = self.themes.get(theme, 0) + 1
        self.last_updated = datetime.now().isoformat()

    def add_breakthrough(self, insight: str) -> None:
        """Record a breakthrough or key insight."""
        if insight not in self.breakthroughs:
            self.breakthroughs.append(insight)
            self.last_updated = datetime.now().isoformat()

    def get_top_themes(self, n: int = 5) -> List[tuple]:
        """Get top N themes by frequency."""
        return sorted(self.themes.items(), key=lambda x: x[1], reverse=True)[:n]

    def to_summary(self) -> str:
        """Generate summary of semantic memory."""
        top_themes = self.get_top_themes(3)
        theme_str = ", ".join([f"{t[0]} ({t[1]})" for t in top_themes])
        return f"Themes: {theme_str}. Breakthroughs: {len(self.breakthroughs)}"


@dataclass
class EpisodicMemory:
    """Store session summaries for cross-session retrieval."""

    sessions: List[Dict[str, Any]] = field(default_factory=list)  # Session records
    max_sessions: int = 10  # Keep last 10 sessions

    def add_session(self, session_data: Dict[str, Any]) -> None:
        """Record a completed session."""
        self.sessions.append({
            "timestamp": datetime.now().isoformat(),
            "duration_minutes": session_data.get("duration_minutes", 0),
            "turn_count": session_data.get("turn_count", 0),
            "summary": session_data.get("summary", ""),
            "key_topics": session_data.get("key_topics", []),
        })

        # Keep only last N sessions
        if len(self.sessions) > self.max_sessions:
            self.sessions = self.sessions[-self.max_sessions:]

    def get_recent_sessions(self, n: int = 3) -> List[Dict[str, Any]]:
        """Get last N session summaries."""
        return self.sessions[-n:]

    def get_cross_session_patterns(self) -> str:
        """Identify patterns across sessions."""
        if not self.sessions:
            return ""

        all_topics = []
        for session in self.sessions:
            all_topics.extend(session.get("key_topics", []))

        # Count topic frequency
        topic_freq = {}
        for topic in all_topics:
            topic_freq[topic] = topic_freq.get(topic, 0) + 1

        # Get recurring topics
        recurring = [t for t, freq in topic_freq.items() if freq > 1]
        if recurring:
            return f"Recurring topics: {', '.join(recurring)}"
        return ""


@dataclass
class WorkingMemory:
    """Smart conversation window - adaptive vs. fixed."""

    current_session: List[Dict[str, str]] = field(default_factory=list)
    max_turns: int = 20  # Fallback to fixed window
    crisis_turns: int = 10  # Keep extra context around crises

    def add_message(self, role: str, content: str, is_crisis: bool = False) -> None:
        """Add message to working memory."""
        self.current_session.append({
            "role": role,
            "content": content,
            "is_crisis": is_crisis,
            "timestamp": datetime.now().isoformat()
        })
        self._prune_history()

    def _prune_history(self) -> None:
        """Intelligently prune history, keeping crisis context."""
        if len(self.current_session) <= self.max_turns:
            return

        # Find crisis messages
        crisis_indices = [
            i for i, msg in enumerate(self.current_session)
            if msg.get("is_crisis", False)
        ]

        if crisis_indices:
            # Keep crisis context: 5 messages before & after last crisis
            last_crisis = crisis_indices[-1]
            start = max(0, last_crisis - 5)
            end = min(len(self.current_session), last_crisis + self.crisis_turns)

            # Keep oldest + crisis context + most recent
            keep = (
                self.current_session[:2] +
                self.current_session[start:end] +
                self.current_session[-2:]
            )
            self.current_session = keep
        else:
            # No crisis, just keep most recent
            self.current_session = self.current_session[-self.max_turns:]

    def get_messages_for_llm(self) -> List[Dict[str, str]]:
        """Get clean messages for LLM (without internal metadata)."""
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.current_session
        ]

    def to_summary(self) -> str:
        """Summarize working memory."""
        return f"Working memory: {len(self.current_session)} recent messages"


class MemoryStore:
    """Persistent storage layer - JSON-based for transparency."""

    def __init__(self, storage_dir: Path = Path("memory_storage")):
        """Initialize memory storage."""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        logger.info(f"Memory store initialized at {self.storage_dir}")

    def _get_user_dir(self, user_id: str) -> Path:
        """Get or create user-specific directory."""
        user_dir = self.storage_dir / user_id
        user_dir.mkdir(exist_ok=True)
        return user_dir

    def save_semantic_memory(self, user_id: str, memory: SemanticMemory) -> None:
        """Persist semantic memory."""
        try:
            user_dir = self._get_user_dir(user_id)
            path = user_dir / "semantic_memory.json"
            data = {
                "themes": memory.themes,
                "breakthroughs": memory.breakthroughs,
                "patterns": memory.patterns,
                "last_updated": memory.last_updated,
            }
            path.write_text(json.dumps(data, indent=2))
            logger.debug(f"Saved semantic memory for {user_id}")
        except Exception as e:
            logger.error(f"Error saving semantic memory: {e}")

    def load_semantic_memory(self, user_id: str) -> SemanticMemory:
        """Load semantic memory from storage."""
        try:
            user_dir = self._get_user_dir(user_id)
            path = user_dir / "semantic_memory.json"

            if path.exists():
                data = json.loads(path.read_text())
                memory = SemanticMemory(
                    themes=data.get("themes", {}),
                    breakthroughs=data.get("breakthroughs", []),
                    patterns=data.get("patterns", {}),
                    last_updated=data.get("last_updated", datetime.now().isoformat()),
                )
                logger.debug(f"Loaded semantic memory for {user_id}")
                return memory
        except Exception as e:
            logger.error(f"Error loading semantic memory: {e}")

        return SemanticMemory()

    def save_episodic_memory(self, user_id: str, memory: EpisodicMemory) -> None:
        """Persist episodic memory (session history)."""
        try:
            user_dir = self._get_user_dir(user_id)
            path = user_dir / "episodic_memory.json"
            data = {"sessions": memory.sessions}
            path.write_text(json.dumps(data, indent=2))
            logger.debug(f"Saved episodic memory for {user_id}")
        except Exception as e:
            logger.error(f"Error saving episodic memory: {e}")

    def load_episodic_memory(self, user_id: str) -> EpisodicMemory:
        """Load episodic memory from storage."""
        try:
            user_dir = self._get_user_dir(user_id)
            path = user_dir / "episodic_memory.json"

            if path.exists():
                data = json.loads(path.read_text())
                memory = EpisodicMemory(sessions=data.get("sessions", []))
                logger.debug(f"Loaded episodic memory for {user_id}")
                return memory
        except Exception as e:
            logger.error(f"Error loading episodic memory: {e}")

        return EpisodicMemory()

    def save_session(self, user_id: str, session_id: str, messages: List[Dict[str, str]]) -> None:
        """Archive a completed session."""
        try:
            user_dir = self._get_user_dir(user_id)
            session_dir = user_dir / "sessions"
            session_dir.mkdir(exist_ok=True)

            path = session_dir / f"{session_id}.json"
            data = {
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "messages": messages,
            }
            path.write_text(json.dumps(data, indent=2))
            logger.debug(f"Archived session {session_id}")
        except Exception as e:
            logger.error(f"Error archiving session: {e}")


class MemoryManager:
    """Orchestrate all memory types and persistence."""

    def __init__(self, user_id: str = "default", storage_dir: Path = Path("memory_storage")):
        """Initialize memory manager."""
        self.user_id = user_id
        self.store = MemoryStore(storage_dir)

        # Load persistent memory
        self.semantic = self.store.load_semantic_memory(user_id)
        self.episodic = self.store.load_episodic_memory(user_id)

        # Initialize working memory
        self.working = WorkingMemory()

        # Time tracking
        self.time_metadata = TimeMetadata(session_start=datetime.now().isoformat())

        logger.info(f"Memory manager initialized for user {user_id}")

    def update_for_message(self, role: str, content: str, is_crisis: bool = False) -> None:
        """Update all memory layers for a new message."""
        # Update working memory
        self.working.add_message(role, content, is_crisis)

        # Update time tracking
        self.time_metadata.last_message_time = datetime.now().isoformat()
        self.time_metadata.total_turns += 1

        # Extract themes from user messages
        if role == "user":
            self._extract_themes(content)

        # Detect breakthroughs in assistant responses
        if role == "assistant":
            self._detect_breakthroughs(content)

    def _extract_themes(self, text: str) -> None:
        """Extract themes from user text (simple keyword-based)."""
        theme_keywords = {
            "anxiety": ["anxious", "anxiety", "worried", "panic", "nervous"],
            "sleep": ["sleep", "insomnia", "tired", "fatigue"],
            "relationships": ["relationship", "friend", "family", "partner"],
            "work": ["work", "job", "boss", "colleague", "project"],
            "mood": ["sad", "depressed", "happy", "mood", "emotion"],
        }

        text_lower = text.lower()
        for theme, keywords in theme_keywords.items():
            if any(kw in text_lower for kw in keywords):
                self.semantic.add_theme(theme)

    def _detect_breakthroughs(self, text: str) -> None:
        """Detect breakthroughs in assistant responses."""
        breakthrough_markers = [
            "you've overcome",
            "you can",
            "one possibility",
            "strength",
            "progress",
            "learned",
        ]

        text_lower = text.lower()
        if any(marker in text_lower for marker in breakthrough_markers):
            # Extract first sentence as breakthrough
            sentences = text.split(".")
            if sentences:
                insight = sentences[0].strip()[:100]
                if len(insight) > 20:
                    self.semantic.add_breakthrough(insight)

    def get_context_for_llm(self) -> Dict[str, str]:
        """Get consolidated context for LLM call."""
        context = {
            "working_memory": self._format_working_memory(),
            "semantic_summary": self.semantic.to_summary(),
            "episodic_summary": self.episodic.get_cross_session_patterns(),
            "time_summary": self.time_metadata.to_summary(),
        }

        # Filter out empty fields
        return {k: v for k, v in context.items() if v}

    def _format_working_memory(self) -> str:
        """Format working memory for LLM context."""
        messages = self.working.get_messages_for_llm()
        if not messages:
            return ""
        return f"Recent conversation: {len(messages)} messages"

    def end_session(self, summary: str = "") -> None:
        """End current session and archive to episodic memory."""
        self.time_metadata.session_end = datetime.now().isoformat()

        # Calculate duration
        start = datetime.fromisoformat(self.time_metadata.session_start)
        end = datetime.fromisoformat(self.time_metadata.session_end)
        duration_seconds = (end - start).total_seconds()
        self.time_metadata.total_duration_seconds = int(duration_seconds)

        # Create session record for episodic memory
        session_data = {
            "duration_minutes": duration_seconds / 60,
            "turn_count": self.time_metadata.total_turns,
            "summary": summary,
            "key_topics": list(self.semantic.get_top_themes(5)),
        }

        self.episodic.add_session(session_data)

        # Persist memory
        self.store.save_semantic_memory(self.user_id, self.semantic)
        self.store.save_episodic_memory(self.user_id, self.episodic)

        # Archive session
        messages = self.working.get_messages_for_llm()
        self.store.save_session(
            self.user_id,
            f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            messages
        )

        logger.info(f"Session ended: {self.time_metadata.to_summary()}")

    def start_new_session(self) -> None:
        """Start a new session (resets working memory, keeps semantic/episodic)."""
        self.working = WorkingMemory()
        self.time_metadata = TimeMetadata(session_start=datetime.now().isoformat())
        logger.info(f"New session started for {self.user_id}")

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about memory usage."""
        return {
            "user_id": self.user_id,
            "semantic_themes": len(self.semantic.themes),
            "breakthroughs": len(self.semantic.breakthroughs),
            "past_sessions": len(self.episodic.sessions),
            "current_working_memory_size": len(self.working.current_session),
            "session_duration_minutes": self.time_metadata.session_duration_minutes,
            "total_turns": self.time_metadata.total_turns,
        }

