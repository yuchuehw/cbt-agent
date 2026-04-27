# Contributing to CBT Agent

Thank you for your interest in contributing to this project! This document provides guidelines for development, testing, and submitting improvements.

**Maintained by:** Yu-Chueh Wang (yuchuehw@uci.edu)

## Code of Conduct

We are committed to providing a safe, inclusive environment. Be respectful, constructive, and collaborative.

## Getting Started

### Prerequisites

- Python 3.9+
- Git
- OpenAI API key (optional; project works without it)

### Local Setup

```powershell
# Clone the repository
git clone https://github.com/yuchuehw/cbt-agent.git
cd cbt-agent

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # macOS/Linux

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If you're developing
```

### Project Structure

```
cbt-agent/
├── src/cbt_agent/           # Main application code
│   ├── agents/              # CbtAgent class and API
│   ├── runtime/             # Agent loop and routing
│   ├── guardrails/          # Safety validators and detectors
│   ├── tools/               # CBT exercises and responses
│   ├── bridge/              # HTTP server
│   ├── evals/               # Test cases
│   ├── config/              # Configuration files
│   ├── prompts/             # System prompt
│   └── policies/            # Policy constraints
├── docs/                    # Documentation
├── README.md                # User-facing overview
├── QUICKSTART.md            # Quick start guide
├── main.py                  # CLI entry point
├── requirements.txt         # Dependencies
└── pyproject.toml           # Python packaging
```

---

## Development Workflow

### 1. Create a Feature Branch

```powershell
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

Use descriptive names: `feature/session-persistence`, `fix/crisis-keyword-detection`, etc.

### 2. Make Changes

Follow these conventions:

#### Code Style

- **Type hints:** All functions should have parameter and return type annotations
  ```python
  def validate(response_text: str, policy: Dict[str, Any], user_input: str = "") -> List[str]:
      pass
  ```

- **Docstrings:** Use Google-style docstrings for public functions:
  ```python
  def detect_crisis(text: str, keywords: Iterable[str]) -> CrisisResult:
      """Detect crisis indicators in user text.
      
      Args:
          text: User input to analyze
          keywords: Crisis keywords to match (case-insensitive)
          
      Returns:
          CrisisResult with is_crisis flag, severity, and matched terms
          
      References:
          Walsh et al. (2017) on natural language markers for suicidal ideation
      """
  ```

- **Imports:** Group as follows:
  ```python
  from __future__ import annotations
  
  import json
  from pathlib import Path
  from typing import Any, Dict, List
  
  from cbt_agent.guardrails.policy_engine import load_policy
  from cbt_agent.runtime.message_schemas import AgentResponse
  ```

- **Line length:** Max 120 characters (PEP 8 allows up to 79, but we're lenient for readability)

- **Naming:**
  - Functions/variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`
  - Private: Prefix with `_`

#### Logging

Replace `print()` statements with structured logging where possible:

```python
import logging

logger = logging.getLogger(__name__)

def my_function():
    logger.debug("Processing user input")
    logger.info("Crisis detected, escalating")
    logger.warning("Policy violation: missing collaborative check-in")
    logger.error("Failed to load policy: %s", str(e))
```

#### Error Handling

Use custom exceptions for domain-specific errors:

```python
class PolicyViolationError(Exception):
    """Raised when response violates policy constraints."""
    pass

class CrisisDetectionError(Exception):
    """Raised when crisis detection encounters an error."""
    pass
```

### 3. Test Your Changes

#### Running Existing Tests

```powershell
# Run adversarial evaluation suite
python evals\adversarial_tests.py

# Run unit tests (if you add them)
pytest tests/ -v
```

#### Adding Tests

If you modify a guardrail, validator, or policy function, add a test:

```python
# tests/test_validators.py

import pytest
from cbt_agent.guardrails.validators import contains_deceptive_empathy

def test_contains_deceptive_empathy_true():
    text = "Dear friend, I see you and I wholeheartedly empathize."
    assert contains_deceptive_empathy(text) is True

def test_contains_deceptive_empathy_false():
    text = "From what you shared, that sounds difficult."
    assert contains_deceptive_empathy(text) is False
```

### 4. Update Documentation

If you change behavior, add a feature, or modify the policy:

1. **Update relevant docstrings** in code
2. **Update `docs/ARCHITECTURE.md`** if it affects the flow
3. **Update `README.md`** if it's user-facing
4. **Add research citations** to `docs/RESEARCH.md` if you implement new safety features
5. **Update `docs/CHANGELOG.md`** (see format below)

#### CHANGELOG Format

```markdown
## [Version] - YYYY-MM-DD

### Added
- New feature description

### Changed
- Behavior change description with migration notes

### Fixed
- Bug fix description

### Deprecated
- Deprecation notice with replacement

### Research
- Citation to papers supporting the change
```

### 5. Commit Your Changes

Write clear, atomic commits:

```powershell
git add <files>
git commit -m "Short description (50 chars max)

Longer explanation if needed. Include:
- What changed
- Why it changed
- Any breaking changes or migration notes
"
```

Example:
```
Improve crisis detection with natural language context

- Add NLP-based severity scoring (complementary to keywords)
- Detect temporal urgency markers (tonight, right now, etc.)
- Reduce false positives by requiring context alignment

References Walsh et al. (2017) on NLP markers for suicidal ideation.
```

### 6. Submit a Pull Request

Push your branch:

```powershell
git push origin feature/your-feature-name
```

Then open a pull request on GitHub with:

- **Title:** Short description (same as first commit line)
- **Description:**
  ```markdown
  ## What
  Brief summary of changes
  
  ## Why
  Motivation and context
  
  ## How to Test
  Steps to verify the change works
  
  ## Checklist
  - [ ] Tests added/updated
  - [ ] Documentation updated
  - [ ] No breaking changes (or migration documented)
  - [ ] Evaluated with `evals/adversarial_tests.py`
  ```

- **Reference issues:** "Closes #123" if this PR fixes an issue

## Review Process

1. **Automated checks:** GitHub Actions will run tests and linting
2. **Code review:** At least one maintainer will review
3. **Feedback:** We may ask for changes or clarification
4. **Approval:** Once approved, a maintainer will merge

### What We Look For

- ✓ Code follows style guidelines
- ✓ All tests pass (existing + new)
- ✓ Documentation is clear and complete
- ✓ Commit messages are descriptive
- ✓ Changes are focused (not 10 unrelated fixes in one PR)
- ✓ No reduction in safety/security
- ✓ Research citations included for new safety features

---

## Types of Contributions

### Bug Reports

Found a bug? Please file an issue with:

- Clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Environment (OS, Python version, API key status)

Example:
```
**Description:** Crisis detection doesn't recognize "i wanna end it all"

**Steps:** 
1. Run python main.py
2. Input: "i wanna end it all"
3. Expected: Crisis escalation response
4. Actual: Normal CBT response

**Environment:** Windows 10, Python 3.10, no OPENAI_API_KEY set
```

### Feature Requests

Have an idea? File an issue with:

- Clear use case
- Expected behavior
- Possible implementation approaches (optional)

Example:
```
**Request:** Add session persistence to memory files

**Use case:** Users want conversations to resume after disconnect

**Possible approach:** Serialize history to JSON files in a sessions/ directory
```

### Documentation Improvements

Found unclear docs? Consider submitting:

- Clarified explanations
- Additional examples
- Links to helpful resources
- Corrections to inaccuracies

### Research Contributions

If you're familiar with digital mental health research:

- Suggest new papers for `docs/RESEARCH.md`
- Point out research-practice gaps
- Propose new safety features backed by evidence

---

## Areas for Contribution

High-priority areas where we welcome contributions:

1. **Testing:** Unit tests, integration tests, adversarial scenarios
2. **Documentation:** Docstrings, tutorials, deployment guides
3. **Type Hints:** Complete type annotations across all modules
4. **Logging:** Structured logging and observability
5. **Performance:** Optimize LLM calls, cache policy loads
6. **Deployment:** Docker support, configuration management, monitoring
7. **Accessibility:** Support for different LLM providers (Claude, etc.)
8. **Safety:** New validators, subtle harm detection patterns, evaluation metrics

---

## Release Process

Maintainers use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR:** Breaking changes (e.g., policy schema change)
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes

Releases are tagged as `v1.2.3` and published to PyPI (future).

---

## Questions?

- **How do I...?** → Check `docs/DEV_GUIDE.md` and `docs/ARCHITECTURE.md`
- **What should I work on?** → Look for issues marked `good-first-issue` or `help-wanted`
- **I found a security issue** → **Don't open an issue.** Email yuchuehw@uci.edu instead
- **General question?** → Open a discussion or start an issue with `[Question]` in the title

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE).

---

Thank you for contributing to making digital mental health safer! 🎉

**Maintained by:** Yu-Chueh Wang (yuchuehw@uci.edu)

