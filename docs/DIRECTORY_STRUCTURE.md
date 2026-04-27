# Directory Organization Guide

**Last Updated:** April 26, 2026

This document explains the project structure after reorganization.

## Root Directory (Minimal)

Only essential files at root level:

```
cbt-agent/
├── README.md                 # Main overview (entry point)
├── QUICKSTART.md             # 5-minute setup guide
├── LICENSE                   # MIT license
├── main.py                   # CLI entry point
├── pyproject.toml            # Python packaging config
├── requirements.txt          # Core dependencies
├── requirements-dev.txt      # Development dependencies
├── .gitignore                # Git ignores
├── .editorconfig             # Editor consistency
└── ...
```

**Rationale:** Keeps root clean and focused on entry points and essential config.

## Code Structure (src/ folder)

All application code lives in `src/cbt_agent/`:

```
src/
└── cbt_agent/
    ├── __init__.py           # Package exports
    ├── agents/               # Main agent interface
    │   └── cbt_agent.py
    ├── runtime/              # Core execution
    │   ├── agent_loop.py
    │   ├── tool_router.py
    │   ├── input_router.py
    │   └── message_schemas.py
    ├── guardrails/           # Safety enforcement
    │   ├── crisis_detector.py
    │   ├── validators.py
    │   └── policy_engine.py
    ├── tools/                # CBT tools
    │   ├── therapist_tools.py
    │   └── safety_tools.py
    ├── prompts/              # System prompts
    │   └── system_prompt.md
    ├── policies/             # Policy constraints
    │   └── cbt_policy.json
    ├── config/               # Configuration
    │   └── config.yaml
    ├── bridge/               # HTTP server
    │   └── http_server.py
    └── evals/                # Evaluation harness
        ├── adversarial_tests.py
        └── test_conversations.jsonl
```

**Rationale:** Modern Python best practice (PEP 420). Makes imports cleaner: `from cbt_agent import CbtAgent`.

## Documentation Structure (docs/ folder)

All documentation lives in `docs/`:

```
docs/
├── INDEX.md                  # Documentation index
├── ARCHITECTURE.md           # System design (400+ lines)
├── RESEARCH.md               # Research citations (450+ lines)
├── DEV_GUIDE.md              # Development setup (350+ lines)
├── CONTRIBUTING.md           # Contribution guide (300+ lines)
├── CHANGELOG.md              # Version history
├── GITHUB_PUBLISH_GUIDE.md   # Publishing steps
├── SAFETY_NOTICE.md          # Safety disclaimers
├── TERMS.md                  # Terms of service
├── PRIVACY.md                # Privacy policy
└── plan.md                   # Original architecture doc
```

**Rationale:** Keeps documentation organized and separate from code. Easy to publish with GitHub Pages.

## Consolidated/Removed Files

### Consolidated Into QUICKSTART.md
- ~~00_START_HERE.md~~ — Now in QUICKSTART.md
- ~~READY_TO_PUBLISH.md~~ — Now in QUICKSTART.md + docs/
- ~~TO_THE_PROJECT_OWNER.md~~ — Now in QUICKSTART.md

### Reference/Archive (Can Be Removed)
- ~~FILES_CREATED.md~~ — Development reference
- ~~PROJECT_STRUCTURE.md~~ — This document (use DEV_GUIDE.md instead)
- ~~IMPROVEMENT_SUMMARY.md~~ — Development reference
- ~~COMPLETION_SUMMARY.txt~~ — Development reference

### Moved to Docs
- ~~CONTRIBUTING.md~~ → docs/CONTRIBUTING.md
- ~~CHANGELOG.md~~ → docs/CHANGELOG.md
- ~~SAFETY_NOTICE.md~~ → docs/SAFETY_NOTICE.md
- ~~TERMS.md~~ → docs/TERMS.md
- ~~PRIVACY.md~~ → docs/PRIVACY.md
- ~~GITHUB_PUBLISH_GUIDE.md~~ → docs/GITHUB_PUBLISH_GUIDE.md
- ~~plan.md~~ → docs/plan.md

## File Count Before & After

| Location | Before | After | Change |
|----------|--------|-------|--------|
| Root | 25+ | 8 | -17 (68% reduction) |
| docs/ | 8 | 11 | +3 (consolidated docs) |
| src/cbt_agent/ | scattered | consolidated | Organized |
| Total | 25+ | 19 | Cleaner structure |

## How to Use the New Structure

### For Users
1. Read `README.md` first
2. Use `QUICKSTART.md` for setup
3. Check `docs/INDEX.md` for all documentation

### For Developers
1. Follow `docs/DEV_GUIDE.md` for setup
2. Read `docs/ARCHITECTURE.md` to understand system
3. Check `docs/CONTRIBUTING.md` before contributing

### For Researchers
1. Review `docs/RESEARCH.md` for citations
2. Check `docs/ARCHITECTURE.md` for design decisions
3. See code in `src/cbt_agent/` for implementation

### For Publishing
1. Follow `docs/GITHUB_PUBLISH_GUIDE.md` step-by-step
2. Everything is already organized for GitHub

## Import Changes

### Before (with code scattered in root)
```python
from agents.cbt_agent import CbtAgent
from runtime.agent_loop import run_agent
from guardrails.validators import validate
```

### After (with src/cbt_agent/)
```python
from cbt_agent import CbtAgent
from cbt_agent.runtime.agent_loop import run_agent
from cbt_agent.guardrails.validators import validate
```

**Note:** Update `pyproject.toml` to include: `packages = [{include = "cbt_agent", from = "src"}]`

## Configuration Changes

### pyproject.toml Update
```toml
[tool.setuptools]
packages = [{include = "cbt_agent", from = "src"}]
```

### Python Path
If running directly (not installed):
```python
import sys
sys.path.insert(0, 'src')
from cbt_agent import CbtAgent
```

## Benefits of This Structure

✅ **Cleaner Root:** Only 8 root files (was 25+)  
✅ **Professional:** Follows Python best practices (PEP 420, src/ layout)  
✅ **Scalable:** Easy to add new modules to `src/cbt_agent/`  
✅ **Organized Docs:** All documentation in one place  
✅ **GitHub Ready:** Clear structure for publishing  
✅ **Maintainable:** Easy to find things  
✅ **Portable:** Code can be packaged and installed independently  

## Next Steps

1. **Update imports** in `main.py` and `bridge/http_server.py`
2. **Update pyproject.toml** with package configuration
3. **Move files** to their new locations
4. **Test** that everything still works
5. **Commit** reorganization as one clean commit

---

**Author:** Yu-Chueh Wang (yuchuehw@uci.edu)  
**Date:** April 26, 2026

