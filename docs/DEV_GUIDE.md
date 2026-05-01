# Development Guide

Welcome to CBT Agent development! This guide covers setup, architecture understanding, and contribution workflow.

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Project Structure](#project-structure)
3. [Understanding the Architecture](#understanding-the-architecture)
4. [Running Tests](#running-tests)
5. [Code Standards](#code-standards)
6. [Debugging Tips](#debugging-tips)
7. [Common Tasks](#common-tasks)

## Local Development Setup

### Prerequisites

- Python 3.9 or higher
- Git
- pip or conda
- Optional: OpenAI API key for testing with live models

### Windows PowerShell Setup

```powershell
# Clone repository
git clone https://github.com/yourusername/cbt-agent.git
cd cbt-agent

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install development dependencies
pip install -r requirements-dev.txt

# Verify installation
python -c "from agents.cbt_agent import CbtAgent; print('✓ Installation successful')"
```

### macOS / Linux Setup

```bash
git clone https://github.com/yourusername/cbt-agent.git
cd cbt-agent

python -m venv venv
source venv/bin/activate

pip install -r requirements-dev.txt

python -c "from agents.cbt_agent import CbtAgent; print('✓ Installation successful')"
```

### Optional: Set Up OpenAI API Key

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

or

```bash
export OPENAI_API_KEY="sk-..."
```

Without this, the agent uses deterministic fallback responses for testing.

## Project Structure

```
cbt-agent/
├── agents/                   # Agent interface and wrappers
│   ├── __init__.py
│   └── cbt_agent.py         # Main CbtAgent class
│
├── runtime/                  # Core agent loop and routing
│   ├── __init__.py
│   ├── agent_loop.py        # Main orchestration: crisis → policy → LLM → validate
│   ├── tool_router.py       # Tool whitelist and execution
│   ├── input_router.py      # CLI command parsing
│   └── message_schemas.py   # Data classes for messages
│
├── guardrails/              # Safety enforcement
│   ├── __init__.py
│   ├── crisis_detector.py   # Keyword + pattern-based detection
│   ├── validators.py        # Response validation functions
│   └── policy_engine.py     # Policy loading and tool gating
│
├── tools/                   # CBT exercises and responses
│   ├── __init__.py
│   ├── therapist_tools.py   # Suggest exercise, reflect, summarize
│   └── safety_tools.py      # Crisis and risk response templates
│
├── bridge/                  # HTTP server for external UIs
│   ├── __init__.py
│   └── http_server.py       # REST API with session management
│
├── prompts/                 # System prompts and instructions
│   └── system_prompt.md     # Main CBT behavioral prompt
│
├── policies/                # Machine-readable constraints
│   └── cbt_policy.json      # Policy file: all rules in one place
│
├── config/                  # Configuration files
│   └── config.yaml          # Model, runtime, safety settings
│
├── evals/                   # Evaluation and testing
│   ├── __init__.py
│   ├── adversarial_tests.py # Test harness
│   └── test_conversations.jsonl  # Test cases
│
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md      # System design and data flow
│   ├── RESEARCH.md          # Research citations
│   └── DEV_GUIDE.md         # This file
│
├── tests/                   # Unit and integration tests (future)
│   ├── unit/
│   ├── integration/
│   └── conftest.py          # Pytest fixtures
│
├── main.py                  # CLI entry point
├── README.md                # User-facing overview
├── CONTRIBUTING.md          # Contribution guidelines
├── CHANGELOG.md             # Version history
├── SAFETY_NOTICE.md         # Legal disclaimers
├── requirements.txt         # Core dependencies
├── requirements-dev.txt     # Dev dependencies
├── pyproject.toml           # Python packaging config
├── setup.cfg                # Setup configuration
└── .gitignore               # Git ignore rules
```

## Understanding the Architecture

### The 4 Layers

**Layer 1: System Prompt** (`prompts/system_prompt.md`)
- Human-readable behavioral rules
- Defines intent and conversational style
- Not enforceable by itself

**Layer 2: Policy** (`policies/cbt_policy.json`)
- Machine-readable constraints
- Version-controlled and auditable
- Used by validators at runtime

**Layer 3: Runtime** (`runtime/agent_loop.py`)
- Orchestrates the entire flow
- Detects crisis BEFORE LLM
- Calls LLM with system prompt + history
- Validates response against policy

**Layer 4: Validators** (`guardrails/validators.py`)
- Pattern-level detection functions
- Identify violations
- Repair responses without full regeneration

### Execution Flow

See `docs/ARCHITECTURE.md` for detailed flow diagrams. Quick version:

```
Input → Crisis Check → Subtle Harm Check → Policy Load → LLM Call 
→ Validate → Repair → Tool Suggest → MHealth-EVAL → Return Response
```

## Running Tests

### Adversarial Test Suite

```powershell
python evals\adversarial_tests.py
```

Expected output:
```
Eval result: 6/6 passed, 0 failed
```

### Unit Tests (Future)

When tests/ directory is populated:

```powershell
pytest tests/ -v
pytest tests/ --cov=agents,guardrails,runtime,tools
```

### Manual Testing

```powershell
# Test the CLI
python main.py
> /cbt I feel stuck.
> /help
> /reset
> /exit

# Test the HTTP bridge
python bridge\http_server.py
# In another terminal:
curl -X POST http://localhost:8080/chat -H "Content-Type: application/json" \
  -d '{"session_id":"test","message":"/cbt I feel overwhelmed."}'
```

## Code Standards

### Type Hints

All functions must have type annotations:

```python
from typing import Dict, List

def my_function(text: str, policy: Dict[str, Any]) -> List[str]:
    """Process text and return violations."""
    pass
```

Check with mypy:

```powershell
mypy agents/ guardrails/ runtime/ tools/
```

### Docstrings

Use Google-style docstrings with research citations:

```python
def detect_crisis(text: str, keywords: Iterable[str]) -> CrisisResult:
    """Detect crisis indicators in text.
    
    Uses keyword matching. Always runs before LLM to ensure rapid
    response in acute situations.
    
    Args:
        text: User input to analyze
        keywords: Crisis keywords to match
        
    Returns:
        CrisisResult with is_crisis flag and matched terms
        
    References:
        Walsh et al. (2017): Natural language markers for suicidal ideation.
        See docs/RESEARCH.md for full citations.
    """
```

### Code Formatting

Use black and isort:

```powershell
black agents/ guardrails/ runtime/ tools/
isort agents/ guardrails/ runtime/ tools/
```

Configure in `pyproject.toml`:
- Line length: 120 characters
- Python 3.9+

### Linting

```powershell
flake8 agents/ guardrails/ runtime/ tools/
```

## Debugging Tips

### Enable Logging

Add to your script:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

See debug output for:
- Policy loading
- Crisis detection
- Validation violations
- Tool execution

### Use the Fallback Mode

Without `OPENAI_API_KEY`, agent generates deterministic responses:

```powershell
# This will work without API key
python main.py
> I feel stuck.
```

Useful for testing infrastructure without costs.

### Inspect Policy

```python
from guardrails.policy_engine import load_policy

policy = load_policy()
print(policy["response_style"]["max_questions_per_turn"])
# Output: 2
```

### Test Validators

```python
from guardrails.validators import contains_deceptive_empathy

text = "Dear friend, I see you."
print(contains_deceptive_empathy(text))
# Output: True
```

### Trace Execution

Add print/log statements at key points:

```python
def run_agent(user_input, conversation_state):
    policy = load_policy()
    print(f"Policy loaded: {len(policy)} sections")
    
    crisis = detect_crisis(user_input, ...)
    print(f"Crisis check: {crisis.is_crisis}")
    
    # ... rest of function
```

## Common Tasks

### Add a New Validator

1. Create validator function in `guardrails/validators.py`:

```python
def contains_my_pattern(response_text: str) -> bool:
    """Check if response contains problematic pattern."""
    return "problematic" in response_text.lower()
```

2. Add to `validate()` function:

```python
if policy.get("my_section", {}).get("check_my_pattern"):
    if contains_my_pattern(response_text):
        violations.append("my_pattern_violation")
```

3. Add repair logic in `repair_response()`:

```python
if "my_pattern_violation" in violations:
    response_text = response_text.replace("problematic", "better")
```

4. Update policy in `cbt_policy.json`:

```json
{
  "my_section": {
    "check_my_pattern": true
  }
}
```

5. Test with adversarial suite

### Add a New Tool

1. Implement in `tools/therapist_tools.py`:

```python
def my_tool(context: str) -> str:
    """Return CBT exercise."""
    return "Try this exercise..."
```

2. Register in `runtime/tool_router.py`:

```python
TOOL_REGISTRY = {
    "my_tool": therapist_tools.my_tool,
    # ... existing tools
}
```

3. Add to policy allowlist:

```json
{
  "tools": {
    "allowed": ["my_tool", "suggest_cbt_exercise", ...]
  }
}
```

4. Test via CLI:

```
/tool my_tool Some context
```

### Change Model Provider

1. Edit `config/config.yaml`:

```yaml
model:
  provider: claude  # or openai, anthropic, local
  model_name: claude-3-sonnet
```

2. Update `runtime/agent_loop.py` `llm_call()` function to support new provider

3. Test with adversarial suite to ensure policy enforcement still works

### Release a New Version

1. Update `pyproject.toml` version
2. Update `__init__.py` `__version__`
3. Add entry to `CHANGELOG.md`
4. Commit with message: `Release v0.2.0`
5. Tag: `git tag v0.2.0`
6. Push: `git push origin main --tags`

## Getting Help

- **Architecture questions?** → Read `docs/ARCHITECTURE.md`
- **Why was X designed this way?** → Check `docs/RESEARCH.md`
- **How do I extend the system?** → See `CONTRIBUTING.md`
- **Is there a test for that?** → Look in `evals/` or `tests/`
- **Found a bug?** → Open an issue with reproducible steps
- **Want to contribute?** → See `CONTRIBUTING.md` first

---

Happy hacking! 🎉

