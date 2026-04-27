# Documentation Index

Quick reference for all project documentation and how to use it.

## Getting Started

**New to the project?** Start here:

1. **[README.md](../README.md)** — Project overview, quick start, and key concepts
   - What is CBT Agent?
   - How to set up and run
   - Example usage
   - Key design principles

2. **[docs/DEV_GUIDE.md](DEV_GUIDE.md)** — Development setup and common tasks
   - How to set up your development environment
   - Project structure explanation
   - Running tests
   - Debugging tips

3. **[CONTRIBUTING.md](../CONTRIBUTING.md)** — How to contribute
   - Code style guidelines
   - Testing requirements
   - PR process
   - Contribution areas

## Understanding the System

**Want to understand how it works?**

1. **[docs/ARCHITECTURE.md](ARCHITECTURE.md)** — System design and data flow
   - The 4-layer architecture (Prompt → Policy → Runtime → Validators)
   - Complete execution flow with examples
   - How each component works
   - Extension points for customization
   - Safety guarantees and limitations

2. **[docs/RESEARCH.md](RESEARCH.md)** — Research foundation and citations
   - Why each guardrail exists
   - Peer-reviewed papers supporting the design
   - How CBT theory informs the system
   - Crisis detection based on NLP research
   - Fairness and cultural humility foundations

3. **[plan.md](../plan.md)** — Original architectural vision
   - The philosophical motivation
   - Why 4 layers are needed
   - Conceptual foundation

## Quick Reference

### Code Organization

```
agents/              → Main agent interface (CbtAgent)
runtime/             → Core agent loop and enforcement
guardrails/          → Validators, crisis detection, policy
tools/               → CBT exercises and safety responses
bridge/              → HTTP server for external UIs
prompts/             → System prompt with behavioral rules
policies/            → Machine-readable policy constraints (JSON)
evals/               → Test cases and evaluation harness
docs/                → Documentation (you're here!)
```

### Key Files

| File | Purpose | Read When |
|------|---------|-----------|
| `prompts/system_prompt.md` | CBT behavioral rules (human-readable) | Modifying agent behavior |
| `policies/cbt_policy.json` | Safety constraints (machine-readable) | Adding new guardrails |
| `runtime/agent_loop.py` | Main execution orchestration | Understanding flow |
| `guardrails/validators.py` | Pattern detectors for violations | Checking policy enforcement |
| `guardrails/crisis_detector.py` | Crisis/subtle harm detection | Understanding safety |
| `tools/therapist_tools.py` | CBT exercises | Adding new tools |
| `evals/adversarial_tests.py` | Test harness | Running evaluations |

### Making Changes

| I Want To... | See This Guide | Then This File |
|---|---|---|
| Set up development | [DEV_GUIDE.md](DEV_GUIDE.md) | `requirements-dev.txt` |
| Add a validator | [CONTRIBUTING.md](../CONTRIBUTING.md) | `guardrails/validators.py` |
| Add a tool | [CONTRIBUTING.md](../CONTRIBUTING.md) | `tools/therapist_tools.py` |
| Change a policy rule | [ARCHITECTURE.md](ARCHITECTURE.md) | `policies/cbt_policy.json` |
| Add a new guardrail | [RESEARCH.md](RESEARCH.md) then [ARCHITECTURE.md](ARCHITECTURE.md) | Find research foundation first |
| Understand a decision | [RESEARCH.md](RESEARCH.md) | Citations + references |
| Deploy to production | [DEV_GUIDE.md](DEV_GUIDE.md) | "Deployment Considerations" |

## Documentation by Audience

### For Users

- **[README.md](../README.md)** — How to use the agent
- **[SAFETY_NOTICE.md](../SAFETY_NOTICE.md)** — Important disclaimers
- **[TERMS.md](../TERMS.md)** — Terms of service

### For Developers

- **[DEV_GUIDE.md](DEV_GUIDE.md)** — Setup and development
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** — Code standards and PR process
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — System design deep dive
- **[RESEARCH.md](RESEARCH.md)** — Why decisions were made

### For Researchers

- **[RESEARCH.md](RESEARCH.md)** — Full academic citations
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — Design rationale
- **[docs/policy.json](../policies/cbt_policy.json)** — Exact constraints being enforced
- **[evals/adversarial_tests.py](../evals/adversarial_tests.py)** — Evaluation methodology

### For Clinical/Healthcare Professionals

- **[README.md](../README.md)** — What the system does
- **[SAFETY_NOTICE.md](../SAFETY_NOTICE.md)** — Limitations and disclaimers
- **[ARCHITECTURE.md](ARCHITECTURE.md)** → "Safety Guarantees and Limitations" section
- **[RESEARCH.md](RESEARCH.md)** → CBT and digital mental health papers

## FAQ by Topic

### "How does crisis detection work?"
→ [ARCHITECTURE.md](ARCHITECTURE.md) → "Layer 4: Sandbox" → "Crisis & Subtle Harm Detection"

### "What papers support the guardrails?"
→ [RESEARCH.md](RESEARCH.md) → Read the whole document, or [ARCHITECTURE.md](ARCHITECTURE.md) → "References"

### "How can I add a new safety feature?"
→ [CONTRIBUTING.md](../CONTRIBUTING.md) → "Add a New Policy Constraint"

### "Is the agent safe to deploy?"
→ [SAFETY_NOTICE.md](../SAFETY_NOTICE.md) and [ARCHITECTURE.md](ARCHITECTURE.md) → "Limitations & Guarantees"

### "How do I customize the agent's behavior?"
→ [ARCHITECTURE.md](ARCHITECTURE.md) → "Extension Points"

### "What's the difference between policy and prompt?"
→ [ARCHITECTURE.md](ARCHITECTURE.md) → "Layer 1: System Prompt" and "Layer 2: Policy File"

### "How do I run tests?"
→ [DEV_GUIDE.md](DEV_GUIDE.md) → "Running Tests"

### "What's the development workflow?"
→ [CONTRIBUTING.md](../CONTRIBUTING.md) → "Development Workflow"

## Document Statistics

| Document | Lines | Purpose |
|----------|-------|---------|
| README.md | 250+ | User overview and quick start |
| CONTRIBUTING.md | 300+ | Developer guide and PR process |
| ARCHITECTURE.md | 400+ | System design and data flow |
| RESEARCH.md | 450+ | Academic citations and foundations |
| DEV_GUIDE.md | 350+ | Development setup and tasks |
| IMPROVEMENT_SUMMARY.md | 400+ | Summary of all changes made |
| docs/INDEX.md | 250+ | You are here! |

**Total: 2,400+ lines of documentation**

## Getting Help

- **"How do I...?"** → Check [DEV_GUIDE.md](DEV_GUIDE.md) "Common Tasks"
- **"Why was X designed this way?"** → [RESEARCH.md](RESEARCH.md) + [ARCHITECTURE.md](ARCHITECTURE.md)
- **"Found a bug?"** → Open an issue with steps to reproduce
- **"Have a feature idea?"** → Open a feature request issue
- **"Want to contribute?"** → Read [CONTRIBUTING.md](../CONTRIBUTING.md) first
- **"Security concern?"** → Email instead of opening an issue

## Next Steps

1. If you're using the agent: Read [README.md](../README.md)
2. If you're developing: Read [DEV_GUIDE.md](DEV_GUIDE.md)
3. If you're contributing: Read [CONTRIBUTING.md](../CONTRIBUTING.md)
4. If you want to understand the system: Read [ARCHITECTURE.md](ARCHITECTURE.md)
5. If you want to know the research: Read [RESEARCH.md](RESEARCH.md)

---

**Last Updated:** April 26, 2026

