# CBT Agent Architecture

## Overview

This is a **policy-enforcing, research-backed CBT-style conversational agent** structured in 4 distinct layers, each with specific responsibility:

1. **System Prompt Layer** — Behavioral intent
2. **Policy Layer** — Machine-readable constraints  
3. **Runtime Layer** — Enforcement and tool gating
4. **Sandbox Layer** — Validation and repair

The key architectural principle: **Prompts define intent. Code enforces behavior. Policies define constraints.**

## Layer 1: System Prompt

**File:** `prompts/system_prompt.md`

The system prompt shapes conversational behavior by defining:
- Epistemic humility: treat all interpretations as tentative
- User-led formulation: ask before interpreting
- Minimal interventions: at most 1 CBT exercise per turn
- Grounded empathy: reflect concrete details, avoid generic phrases
- Safety priority: crisis detection triggers immediate escalation

**Why separate from code?** Prompts are human-readable and easier to iterate. But they alone cannot enforce constraints.

**Research basis:** Clark (2011), Cuijpers et al. (2019) on collaborative CBT delivery.

---

## Layer 2: Policy File

**File:** `policies/cbt_policy.json`

The policy is a **machine-readable contract** specifying:

### `interpretation_limits`
- `max_hypotheses_per_response`: Limit speculative statements
- `require_user_input_before_interpretation`: Don't interpret without context

### `response_style`
- `no_generic_empathy`: Block "I understand"
- `no_deceptive_empathy`: Block "I see you", "dear friend"
- `max_questions_per_turn`: Limit cognitive load
- `require_tentative_language`: Enforce "one possibility", "might"
- `max_response_paragraphs`: Keep responses concise

### `cbt_constraints`
- `max_interventions_per_turn`: One exercise per turn
- `require_user_context_citation`: Echo user's own language
- `challenge_distortions_gently`: Avoid harsh contradiction
- `require_guided_self_discovery`: Don't give answers

### `risk_controls`
- `block_over_validation`: Don't over-affirm distorted thinking
- `block_gaslighting_language`: Never imply user is at fault
- `block_abandonment_language`: Commit to support
- `require_collaborative_check_in`: Always check understanding
- `require_non_authoritative_language`: Avoid certainty claims

### `fairness`
- `avoid_identity_assumptions`: No default demographics
- `require_cultural_humility_when_context_signaled`: Acknowledge cultural/religious/family context
- `sensitive_identity_terms`: List of keywords that trigger humility checks

### `safety`
- **Crisis keywords:** Explicit list of high-risk phrases (e.g., "kill myself", "end my life")
- **High-risk keywords:** Temporal/imminent markers ("tonight", "right now", "I have a plan")
- **Subtle harm patterns:** Three-part detection (substance + procurement + risk context)
- **Escalation flags:** Rules for when to override CBT mode

### `trustworthiness`
- `block_unverified_numbers`: Only cite verified crisis lines
- `verified_numbers`: Hardcoded list (e.g., 988 US/Canada)
- `discourage_us_centric_default`: Flag 988 for non-US users

### `tools`
- `allowed`: Whitelist of permitted tool names (prevents prompt injection)

**Why JSON, not Python code?** 
- Non-technical stakeholders can read and audit it
- Can be versioned and rolled back independently
- Can be loaded at runtime without code changes
- Enables A/B testing different policies

**Research basis:** Fitzpatrick et al. (2017) on MHealth-EVAL; Christiano et al. (2016) on safety-critical design.

---

## Layer 3: Runtime (Agent Loop + Enforcement)

**Files:**
- `runtime/agent_loop.py` — Main orchestration
- `runtime/tool_router.py` — Tool gating
- `runtime/input_router.py` — Command parsing
- `guardrails/validators.py` — Violation detection
- `guardrails/policy_engine.py` — Policy loading

### Execution Flow

```
User Input
    ↓
Crisis Detection (synchronous keyword + semantic check)
    ↓ (crisis? → Crisis Response)
    ↓ (not crisis)
Subtle Harm Detection (substance + procurement + context)
    ↓ (subtle? → Risk Response)
    ↓ (not subtle)
Load Policy & System Prompt
    ↓
Call LLM
    ↓
Validate Response Against Policy
    ↓ (violations? → Repair/Regenerate)
    ↓ (no violations)
Optional Tool Suggestion (if user mentions "exercise", "try", "plan")
    ↓
Evaluate MHealth-EVAL Score
    ↓
Return AgentResponse(text, violations, meta)
```

### Key Design Decisions

1. **Crisis detection BEFORE LLM call:** Don't let the model decide if something is a crisis. Use keyword detection + semantic context as the first line of defense.

2. **Subtle harm detection BEFORE LLM:** Three-part pattern (substance + procurement + context) catches sophisticated harm-seeking that single keywords would miss. Draws on SAMHSA guidance.

3. **Validation AFTER LLM call:** After the model generates a response, check it against the policy. If violations found, either repair (strip/rewrite offending phrases) or regenerate (ask model to comply).

4. **Tool gating:** The tool router checks policy *before* execution. Unknown tools raise PermissionError. This prevents prompt injection from expanding agent capabilities.

5. **Logging all decisions:** Every crisis/subtle harm detection, validation violation, and policy decision is logged for audit.

**Research basis:** Walsh et al. (2017) on crisis keyword detection; SAMHSA (2023) on substance harm.

---

## Layer 4: Sandbox (Validators + Tools)

**Files:**
- `guardrails/validators.py` — Pattern detection and response repair
- `guardrails/crisis_detector.py` — Crisis/subtle harm classification
- `tools/therapist_tools.py` — Deterministic CBT suggestions
- `tools/safety_tools.py` — Crisis response templates

### Validators

Each validator is a **phrase-level pattern detector:**

- `contains_generic_empathy()` — Blocks "I understand", "I know how you feel"
- `contains_deceptive_empathy()` — Blocks "I see you", "dear friend", "I wholeheartedly empathize"
- `contains_over_validation()` — Blocks "you are absolutely right", "exactly, everyone"
- `contains_gaslighting_language()` — Blocks "you are causing your own", "it is your fault"
- `contains_abandonment_language()` — Blocks "I can't help you"
- `count_hypotheses()` — Enforces max speculative statements
- `count_questions()` — Enforces max questions per turn
- `has_user_context_citation()` — Checks if response echoes user language
- `has_collaborative_check_in()` — Requires "Does this fit your experience?"
- `has_cultural_humility_signal()` — Requires acknowledgment of cultural/religious/family context if signaled

### Response Repair

If violations are found, `repair_response()` applies targeted fixes:

- Generic empathy → "From what you described"
- Too many questions → Keep first 2, discard rest
- Missing context citation → Prepend "From what you shared"
- Missing cultural humility → Prepend "I want to respect your values and context"
- Missing collaborative check-in → Append "Does this fit your experience?"

This allows imperfect LLM outputs to be salvaged without requiring regeneration.

### Crisis & Subtle Harm Detection

**Crisis Detection:**
- Keyword match against `crisis_keywords` (e.g., "kill myself", "suicide")
- If high-risk keywords also present ("tonight", "I have a plan"), severity = "high"
- Else severity = "moderate"
- Override: when crisis detected, skip CBT mode entirely

**Subtle Harm Detection:**
- Three-part pattern matching across conversation window (default: 6 turns)
- Groups: `substance_terms`, `procurement_terms`, `risk_context_terms`
- If all three groups present → severity = "high"
- If substance + procurement → severity = "moderate"
- Otherwise → no escalation

Example: "I'm stressed and drink every day. Where can I buy alcohol in bulk for cheap?" matches substance (drink) + procurement (bulk, cheap) + context (stressed) → escalated.

### Tools

**Deterministic CBT tools** (no LLM required):
- `reflect_user_text(context)` → Paraphrase user statement
- `summarize_thoughts(turns)` → List last 3 user thoughts
- `suggest_cbt_exercise(context)` → Based on keywords, suggest avoidance/worry/rumination exercise

Tools are only called if in the allowed list and user input triggers them. They don't require policy validation (they're deterministic).

---

## Data Flow: A Complete Example

**User input:** "I keep procrastinating and feel stuck."

1. **Input Router** → Parse as direct message (not a slash command)

2. **Crisis Detection** → Check "procrastinating" and "stuck" against crisis keywords → No match → continue

3. **Subtle Harm Detection** → No substance/procurement terms → continue

4. **LLM Call:**
   - System prompt: "You are a CBT-style agent..."
   - History: []
   - User: "I keep procrastinating and feel stuck."
   - Model response: "I understand how frustrating procrastination is. Have you considered breaking tasks into smaller steps? Maybe try a 5-minute starter task and see how it goes?"

5. **Validation** against policy:
   - ❌ Contains "I understand" (generic empathy) → violation
   - ✓ Mentions tentative ("maybe") → OK
   - ✓ One question (within max 2) → OK
   - ❌ No collaborative check-in → violation
   - ✓ Includes user context (procrastination) → OK

6. **Repair:**
   - Replace "I understand" with "From what you described"
   - Append "Does this fit your experience?"
   - Result: "From what you described, procrastination can feel frustrating. Have you considered breaking tasks into smaller steps? Maybe try a 5-minute starter task and see how it goes? Does this fit your experience?"

7. **Tool Suggestion** (user said "try" → trigger exercise suggestion):
   - `suggest_cbt_exercise("I keep procrastinating")` → "Behavioral experiment: choose one 5-minute starter task and rate anxiety before/after."
   - Append to response

8. **MHealth-EVAL:**
   - Appropriateness: 2 (no safety flags, all policy constraints met after repair)
   - Trustworthiness: [] (no unverified numbers or US-centric defaults)
   - Safety: [] (no gaslighting, abandonment, substance enabling)

9. **Return:**
   ```json
   {
     "text": "From what you described, procrastination can feel frustrating...",
     "violations": ["generic_empathy", "missing_collaborative_check_in"],
     "meta": {
       "mode": "cbt",
       "risk_flags": ["generic_empathy", "missing_collaborative_check_in"],
       "mhealth_eval": {
         "appropriateness_score": 2,
         "trustworthiness_flags": [],
         "safety_flags": []
       }
     }
   }
   ```

---

## Deployment Modes

### 1. CLI (main.py)
Direct command line interaction with slash command support:
```
/cbt I feel stuck.
/tool suggest_cbt_exercise I avoid difficult tasks.
/reset
/help
```

### 2. HTTP Bridge (bridge/http_server.py)
RESTful endpoint for external UIs:
```
POST /chat
{
  "session_id": "user-123",
  "message": "/cbt I feel overwhelmed."
}
```

Returns:
```json
{
  "response": "From what you shared...",
  "violations": [],
  "meta": {...}
}
```

### 3. Direct Python Import
Use `CbtAgent` class directly in other Python code:
```python
from agents.cbt_agent import CbtAgent

agent = CbtAgent()
response = agent.run_turn("I feel stuck.")
print(response.text)
agent.reset()
```

---

## Extension Points

### Adding a New Policy Constraint

1. **Update `policies/cbt_policy.json`:** Add new policy field
2. **Create validator function** in `guardrails/validators.py`
3. **Add to `validate()` function:** Check policy and call validator
4. **Add repair logic** in `repair_response()` if needed
5. **Test** with `evals/adversarial_tests.py`

### Adding a New Tool

1. **Implement function** in `tools/therapist_tools.py` or `tools/safety_tools.py`
2. **Register in TOOL_REGISTRY** in `runtime/tool_router.py`
3. **Add to allowed list** in `policies/cbt_policy.json`
4. **Optional: Add trigger logic** in `runtime/agent_loop.py` (e.g., if user says "exercise")

### Swapping LLM Provider

1. **Modify `llm_call()`** in `runtime/agent_loop.py`
2. **Update config** in `config/config.yaml`
3. **Ensure message format matches** (system + user messages)
4. **Test with adversarial suite** to confirm policy enforcement still works

---

## Safety Guarantees and Limitations

### What This Architecture Provides

✓ **Layer 1:** Intent clarity via explicit system prompt
✓ **Layer 2:** Auditable, version-control-friendly policy file
✓ **Layer 3:** Deterministic crisis detection before LLM
✓ **Layer 4:** Response validation and repair without full regeneration
✓ **All layers:** Extensive logging and decision tracking

### What It Does NOT Guarantee

✗ **No system is 100% safe:** Edge cases and adversarial prompts can bypass guardrails
✗ **Keyword detection has limits:** Sophisticated harm-seeking may avoid keywords
✗ **Repair is imperfect:** Some violations may not be caught after LLM generation
✗ **No real-time monitoring:** Deployed systems need monitoring and incident response
✗ **Validation is not substitution:** This tool is not therapy and requires human oversight

---

## Testing Strategy

See `evals/adversarial_tests.py` for the evaluation harness:

- **Safe CBT scenarios:** Agent should stay in CBT mode with appropriate responses
- **Context scenarios:** Agent should acknowledge cultural/religious/family context
- **Deceptive empathy scenarios:** Agent should avoid anthropomorphic language
- **Crisis scenarios:** Agent should detect and escalate, not provide CBT
- **Subtle harm scenarios:** Agent should detect multi-pattern harm intent

Each test case specifies:
- User input
- Expected mode (cbt or crisis)
- Required phrases (must_contain_any)
- Banned phrases (must_not_contain)
- Minimum appropriateness score
- Maximum trustworthiness/safety flags

---

## References

- **Fitzpatrick et al. (2017):** MHealth-EVAL framework foundation
- **Clark (2011):** CBT delivery in digital contexts
- **Walsh et al. (2017):** Crisis keyword detection
- **Tervalon & Murray-García (1998):** Cultural humility
- **Christiano et al. (2016):** Safety-critical AI design

See `docs/RESEARCH.md` for full citations.

---

*Last updated: April 2026*

