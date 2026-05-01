What you’re really asking for is **“how do I turn a prompt into an actually enforceable agent system”**—and the key shift is this:

> A good CBT prompt is not the agent.
> The agent is: **prompt + runtime + tool boundaries + policy enforcement code + eval loop**

So I’ll give you a **real project structure you can actually build with Codex / Claude-style tool calling agents**, not just prompt theory.

---

# 1) The mental model (important)

You want 4 layers:

### Layer 1 — System prompt (behavior shaping)

Your CBT prompt goes here.

### Layer 2 — Policy file (machine-readable rules)

This is your “guardrail contract”.

### Layer 3 — Agent runtime (the brain wrapper)

This is where tools are allowed/blocked.

### Layer 4 — Execution sandbox (real safety)

Nothing important happens without passing checks here.

---

# 2) Recommended project structure

Here is a clean, production-style layout:

```
cbt-agent/
│
├── agents/
│   └── cbt_agent.py
│
├── prompts/
│   └── system_prompt.md
│
├── policies/
│   └── cbt_policy.json
│
├── tools/
│   ├── therapist_tools.py
│   └── safety_tools.py
│
├── guardrails/
│   ├── policy_engine.py
│   ├── validators.py
│   └── crisis_detector.py
│
├── runtime/
│   ├── agent_loop.py
│   ├── tool_router.py
│   └── message_schemas.py
│
├── config/
│   └── config.yaml
│
├── evals/
│   ├── test_conversations.jsonl
│   └── adversarial_tests.py
│
├── main.py
└── requirements.txt
```

This separation is what makes it *actually controllable*.

---

# 3) The system prompt file

📄 `prompts/system_prompt.md`

Put your CBT prompt here exactly as you wrote it.

But slightly tighten it:

* remove redundancy
* remove contradictions
* keep it “behavioral”, not philosophical

Example header:

```text
You are a CBT-style conversational agent.

You must follow:
- epistemic humility
- user-led interpretation
- crisis detection priority
- no authoritative psychological claims
```

This file alone does NOTHING unless enforced by runtime.

---

# 4) Policy file (THIS is your real guardrail)

📄 `policies/cbt_policy.json`

This is what makes your agent “respect rules”.

Example:

```json id="cbt_policy"
{
  "interpretation_limits": {
    "max_hypotheses_per_response": 2,
    "require_user_input_before_interpretation": true
  },

  "response_style": {
    "no_generic_empathy": true,
    "max_questions_per_turn": 2,
    "require_tentative_language": true
  },

  "cbt_constraints": {
    "max_interventions_per_turn": 1,
    "require_user_context_citation": true
  },

  "safety": {
    "crisis_keywords_enabled": true,
    "escalate_on_self_harm_risk": true,
    "override_cbt_mode_on_crisis": true
  }
}
```

This is what your runtime enforces.

---

# 5) The agent loop (core system)

📄 `runtime/agent_loop.py`

This is where Codex/Claude actually becomes an “agent”.

Pseudo-structure:

```python
def run_agent(user_input, conversation_state):
    # 1. load policy
    policy = load_policy()

    # 2. detect safety risk FIRST (before LLM)
    risk = crisis_detector(user_input)
    if risk:
        return handle_crisis(user_input)

    # 3. build prompt
    messages = build_messages(system_prompt, conversation_state, user_input)

    # 4. call model
    response = llm_call(messages)

    # 5. validate response against policy
    violations = validate(response, policy)
    if violations:
        response = repair_or_regenerate(response, violations)

    # 6. tool execution gate (if tools used)
    if response.requests_tool:
        if not policy_allows(response.tool_call):
            block_tool_call()
        else:
            execute_tool()

    return response
```

This is the *real guardrail layer*.

---

# 6) Tool control (very important)

📄 `runtime/tool_router.py`

Never let the model directly execute tools.

Instead:

```python
ALLOWED_TOOLS = [
    "reflect_user_text",
    "summarize_thoughts",
    "suggest_cbt_exercise"
]

def route_tool_call(tool_name, args):
    if tool_name not in ALLOWED_TOOLS:
        raise Exception("Blocked tool")

    return execute(tool_name, args)
```

This prevents:

* hidden prompt injection → system compromise
* unsafe expansions of behavior

---

# 7) Validation layer (your real “guardrail brain”)

📄 `guardrails/validators.py`

Example checks:

```python
def validate(response, policy):

    violations = []

    if count_hypotheses(response) > policy["interpretation_limits"]["max_hypotheses_per_response"]:
        violations.append("too_many_hypotheses")

    if contains_generic_empathy(response):
        violations.append("generic_empathy")

    if not uses_tentative_language(response):
        violations.append("too_directive")

    return violations
```

Then:

```python
def repair_or_regenerate(response, violations):
    # either:
    # 1. strip violating sections
    # 2. or re-prompt model with correction instruction

    return regenerate_with_constraints(response, violations)
```

---

# 8) Crisis detection (must be BEFORE the LLM)

📄 `guardrails/crisis_detector.py`

Do NOT rely on LLM alone.

Use hybrid:

```python
CRISIS_KEYWORDS = [
    "kill myself",
    "end my life",
    "self harm",
    "suicide"
]

def crisis_detector(text):
    return any(k in text.lower() for k in CRISIS_KEYWORDS)
```

Optionally:

* add classifier model
* or second LLM pass

But keyword + rules is your first line.

---

# 9) Main entry point

📄 `main.py`

```python
from runtime.agent_loop import run_agent

while True:
    user_input = input("User: ")
    response = run_agent(user_input, state={})
    print("Agent:", response)
```

---

# 10) How to initialize the project

There is no special “Codex init command”.

You just:

### Step 1

```bash
mkdir cbt-agent
cd cbt-agent
python -m venv venv
source venv/bin/activate
```

### Step 2

```bash
pip install openai pyyaml jsonschema
```

(or Anthropic SDK if Claude)

### Step 3

Create folders:

```bash
mkdir agents prompts policies tools guardrails runtime config evals
```

### Step 4

Run:

```bash
python main.py
```

---

# 11) How Codex / Claude fits in

You do NOT “configure Codex”.

You:

* call model inside `llm_call()`
* pass system prompt
* enforce rules externally

Example:

```python
client.responses.create(
    model="gpt-4.1",
    input=messages
)
```

Claude equivalent:

```python
client.messages.create(
    model="claude-3",
    system=system_prompt,
    messages=messages
)
```

---

# 12) The most important insight (people miss this)

If you only remember one thing:

> **Prompts define intent.
> Code enforces behavior.
> Policies define constraints.**

If you rely on prompt alone, your CBT agent will eventually:

* over-interpret users
* become directive
* hallucinate psychological certainty
* ignore safety edge cases

---

# If you want next step

I can help you upgrade this into:

### advanced version:

* multi-agent CBT system (reflector + challenger + safety monitor)
* memory system (session + long-term cognitive patterns)
* prompt injection resistance layer
* evaluation harness (test if it *actually follows CBT rules*)

Just tell me 👍
