# CBT Agent: Research-Backed Conversational Safety Architecture

> **A policy-enforcing, 4-layer conversational system for CBT-style dialogue, built on evidence-based guardrails and designed for educational, research, and supervised clinical use.**

![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)
[![Safety First](https://img.shields.io/badge/safety-first-critical.svg)]()

## ⚠️ Safety and Legal Notice (Read First)

**This is NOT a licensed therapist, medical device, or emergency service.**

- Does not provide medical advice or substitute for professional mental health care
- Not approved for unsupervised use with minors or in clinical settings without human oversight
- **In a crisis:** Contact local emergency services immediately
- **In the US/Canada:** Call or text **988** (Suicide and Crisis Lifeline)

By using this repository, you agree to: [`SAFETY_NOTICE.md`](SAFETY_NOTICE.md) • [`TERMS.md`](TERMS.md) • [`PRIVACY.md`](PRIVACY.md) • [`LICENSE`](LICENSE)


## What is included

The project is organized in **4 safety layers**:

1. **System Prompt** (`prompts/system_prompt.md`): Behavioral intent with epistemic humility
2. **Policy** (`policies/cbt_policy.json`): Machine-readable constraints and rules
3. **Runtime** (`runtime/`): Enforcement, crisis detection, policy validation
4. **Guardrails** (`guardrails/`): Pattern detection, response repair, crisis escalation

Key components:
- Policy enforcement with response validation and repair
- Crisis detection (keyword + high-risk markers) — immediate escalation
- Subtle harm detection (3-part pattern: substance + procurement + context)
- CBT validators: tentative language, context citation, collaborative check-in, cultural humility
- Tool router with whitelist-based access control
- MHealth-EVAL scoring for appropriateness, trustworthiness, and safety
- Comprehensive evaluation harness with adversarial test scenarios

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for detailed data flow and design decisions.
See [`docs/RESEARCH.md`](docs/RESEARCH.md) for the research papers supporting each guardrail.

## Quick Start

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Commands

```
/cbt <message>                              # Send CBT message
/tool <name> <input>                        # Call a specific tool
  Example: /tool suggest_cbt_exercise I avoid difficult tasks.
/help                                       # Show available commands
/reset                                      # Clear session history
/exit, /quit                                # Exit
```

### Example Session

```
User: I keep overthinking mistakes at work.

Agent: From what you described, overthinking mistakes can feel like they weigh a lot. 
One possibility is this pattern could shift with targeted attention. 
Does this fit your experience?

Suggested next step: Thought log: write one worry, evidence for/against it, 
and a balanced alternative thought.
```

## HTTP Bridge (for External UIs)

Run the bridge server:

```powershell
python bridge\http_server.py
```

Server listens at `http://127.0.0.1:8080`

### Example Request

```json
POST /chat
{
  "session_id": "user-123",
  "message": "/cbt I feel overwhelmed by my workload."
}
```

### Example Response

```json
{
  "response": "From what you shared, workload pressure can feel heavy...",
  "violations": [],
  "meta": {
    "mode": "cbt",
    "mhealth_eval": {
      "appropriateness_score": 2,
      "trustworthiness_flags": [],
      "safety_flags": []
    }
  }
}
```

## Evaluation & Testing

Run the adversarial test suite:

```powershell
python evals\adversarial_tests.py
```

Tests include:
- Safe CBT scenarios (should stay in CBT mode)
- Context scenarios (should acknowledge cultural/religious/family context)
- Deceptive empathy scenarios (should avoid anthropomorphic language)
- Crisis scenarios (should detect and escalate, not provide CBT)
- Subtle harm scenarios (should detect multi-pattern harm intent)

See `evals/test_conversations.jsonl` for test cases and metrics.

## Research & Safety

This project is grounded in research on:

- **CBT delivery:** Clark (2011), Cuijpers et al. (2019)
- **Crisis detection:** Walsh et al. (2017) on natural language markers
- **Evaluation:** Fitzpatrick et al. (2017) MHealth-EVAL framework
- **Fairness:** Tervalon & Murray-García (1998) cultural humility
- **AI safety:** Christiano et al. (2016) on safety-critical design

See [`docs/RESEARCH.md`](docs/RESEARCH.md) for full citations and mapping of each guardrail to its research foundation.

## Key Design Principles

1. **Prompts define intent. Code enforces behavior. Policies define constraints.**
   - Prompt: What the agent *should* do
   - Policy: What the agent *must* do (machine-readable)
   - Code: How violations are detected and repaired

2. **Crisis detection happens BEFORE the LLM,** not relying on the model's judgment alone

3. **Subtle harm detection uses multi-pattern matching**, not single keywords

4. **Response validation catches violations after generation** and repairs them without full regeneration

5. **Tool access is explicitly whitelisted,** preventing prompt injection from expanding capabilities

6. **All decisions are logged** for audit and improvement

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for detailed examples.

## Configuration

Edit `config/config.yaml` to customize:

```yaml
model:
  provider: openai              # or future: claude, anthropic, local
  model_name: gpt-4.1-mini
  temperature: 0.4              # Lower = more deterministic

runtime:
  max_history_turns: 10
  auto_repair_on_violation: true

safety:
  crisis_mode_enabled: true
```

## Environment Variables

```powershell
$env:OPENAI_API_KEY="sk-..."          # OpenAI API key
$env:OPENAI_MODEL="gpt-4"             # Specific model override
```

Without `OPENAI_API_KEY`, the agent uses a deterministic fallback response so you can test the scaffold locally.

## Extending the System

### Add a New Policy Constraint

1. Update `policies/cbt_policy.json`
2. Create a validator function in `guardrails/validators.py`
3. Add it to the `validate()` function
4. Add repair logic in `repair_response()` if needed
5. Test with `evals/adversarial_tests.py`

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for full guidelines.

### Add a New Tool

1. Implement in `tools/therapist_tools.py` or `tools/safety_tools.py`
2. Register in `TOOL_REGISTRY` in `runtime/tool_router.py`
3. Add to allowed list in `policies/cbt_policy.json`
4. Test via `/tool <name> <input>` command

## Architecture Overview

```
┌─────────────────┐
│   User Input    │
└────────┬────────┘
         │
    ┌────▼──────────────┐
    │ Crisis Detection  │──► If crisis: escalate, skip CBT
    │ (keywords + HRK)  │
    └────┬──────────────┘
         │ (not crisis)
    ┌────▼──────────────────────┐
    │ Subtle Harm Detection      │──► If risky: escalate
    │ (3-pattern: substance+     │
    │  procurement+context)      │
    └────┬──────────────────────┘
         │ (not risky)
    ┌────▼─────────────┐
    │ Load Policy       │
    │ Load Prompt       │
    └────┬─────────────┘
         │
    ┌────▼─────────────┐
    │ Call LLM          │
    └────┬─────────────┘
         │
    ┌────▼────────────────┐
    │ Validate Response    │
    │ vs. Policy           │
    └────┬────────────────┘
         │ (violations?)
    ┌────▼───────────┐
    │ Repair Response │
    └────┬───────────┘
         │
    ┌────▼──────────────┐
    │ Optional Tool      │
    │ Suggestion         │
    └────┬──────────────┘
         │
    ┌────▼──────────────┐
    │ Evaluate           │
    │ MHealth-EVAL       │
    └────┬──────────────┘
         │
    ┌────▼──────────────┐
    │  Return Response   │
    │  + Violations      │
    │  + Meta (eval)     │
    └────────────────────┘
```

## Limitations & Guarantees

### ✓ This Architecture Provides

- Transparent system prompt and policy
- Deterministic crisis detection before LLM
- Response validation and targeted repair
- Comprehensive logging and decision tracking
- Multi-layer safety approach

### ✗ This Does NOT Guarantee

- **Perfect safety:** Edge cases and adversarial inputs can bypass guardrails
- **Keyword-resistant detection:** Sophisticated harm-seeking may avoid keywords
- **100% violation catching:** Some violations may slip through LLM generation
- **Real-time monitoring:** Deployed systems need monitoring infrastructure
- **Therapy substitution:** No automated system replaces human oversight

**Always assume human review is needed for high-stakes decisions.**

## Deployment Considerations

- **Local/research:** Run directly with Python
- **API server:** Use HTTP bridge for external UIs or orchestrators
- **Clinical:** Requires human oversight, audit logging, incident response plan
- **Docker:** Community contributions welcome (see [CONTRIBUTING.md](CONTRIBUTING.md))

## Contributing

We welcome contributions! See [`CONTRIBUTING.md`](CONTRIBUTING.md) for:

- Code style and type hints
- Testing requirements
- Documentation standards
- Pull request process
- Areas where help is needed (testing, docs, research, deployment)

## License

MIT License. See [`LICENSE`](LICENSE).

## Citation

If you use this project in research, please cite:

```bibtex
@software{cbt_agent_2026,
  title={CBT Agent: Research-Backed Conversational Safety Architecture},
  author={Wang, Yu-Chueh},
  year={2026},
  url={https://github.com/yuchuehw/cbt-agent}
}
```

## Acknowledgments

Built on research from:
- Clark (2011), Cuijpers et al. (2019): CBT delivery
- Fitzpatrick et al. (2017): MHealth-EVAL framework
- Walsh et al. (2017): Crisis detection via NLP
- Tervalon & Murray-García (1998): Cultural humility
- Christiano et al. (2016): Safety-critical AI design

See [`docs/RESEARCH.md`](docs/RESEARCH.md) for complete references.

---

**Questions?** Open an issue or start a discussion. **Found a security issue?** Please email instead of opening an issue.

