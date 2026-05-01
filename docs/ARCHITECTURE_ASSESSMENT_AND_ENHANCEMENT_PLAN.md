# CBT-Agent Architecture Assessment & Enhancement Plan

**Author:** Yu-Chueh Wang (yuchuehw@uci.edu)  
**Date:** April 27, 2026  
**Status:** Analysis & Strategic Plan

---

## Executive Summary

CBT-Agent currently has a **focused, specialized architecture** optimized for safety-critical mental health conversations. Analysis shows:

- ✅ **Has:** Orchestrator (basic), Tool routing (deterministic)
- ❌ **Missing:** Memory layers, Context compressor, Multi-agent coordination
- 📊 **Assessment:** These additions would enhance utility for broader conversational AI use cases, but require careful evaluation of trade-offs with safety-first design

**Recommendation:** Implement **staged enhancements** prioritizing memory layers and context compression while maintaining safety guarantees. Hold multi-agent coordination for future phases.

---

## Current Architecture Analysis

### 1. Orchestrator - ✅ HAS (Basic)

**Current Implementation:**
- `runtime/agent_loop.py` - Sequential orchestrator
- Flow: Crisis detection → Subtle harm → Policy load → LLM call → Validation → Repair → Tool assist

**Capabilities:**
- Linear execution flow
- Crisis detection BEFORE LLM (safety-first)
- Policy-based decision branches
- Simple tool routing
- Response validation and repair

**Limitations:**
- Single-path execution (no parallel processes)
- No state machine for complex conversations
- Limited error recovery paths
- No graceful degradation for LLM failures
- Fixed sequence (can't reorder steps)

**Score:** 6/10 (Functional but rigid)

---

### 2. Memory Layers - ❌ MISSING

**Current Implementation:**
- Simple list history in `CbtAgent.history` (last 20 turns)
- No semantic memory
- No retrieval-augmented generation (RAG)
- No long-term context storage

**What We're Missing:**

| Layer | Status | Impact |
|-------|--------|--------|
| **Short-term Memory** | Partial | Only recent turns kept (20 turn window) |
| **Semantic Memory** | None | Can't extract/remember key themes |
| **Episodic Memory** | None | Can't recall important past events |
| **Procedural Memory** | None | Can't learn user-specific strategies |
| **Working Memory** | Partial | Context passed but not optimized |

**Consequence:**
- Long conversations lose context (only last 20 turns visible)
- Can't reference earlier breakthroughs
- Repeats same advice
- Missing longitudinal patterns (e.g., "you've overcome similar challenges before")

---

### 3. Context Compressor - ❌ MISSING

**Current Implementation:**
- Raw conversation history passed to LLM
- Token count unlimited (no optimization)
- Full message history = full token cost

**What We're Missing:**

```
Current:  20 turns × ~200 tokens/turn = ~4,000 tokens per call
Optimized: Compressed summary = ~800 tokens + recent context = ~1,200 tokens

Potential Savings: 70% token reduction
```

**Specific Gaps:**
- No summarization of resolved topics
- No extraction of key facts
- No semantic compression
- No topic clustering
- No salience-based filtering

**Impact on Safety:**
- More expensive LLM calls (higher cost, higher latency)
- More context drift (less precision in safety detection)
- Harder to maintain conversation continuity

---

### 4. Tool Routing - ✅ HAS (Deterministic)

**Current Implementation:**
- `runtime/tool_router.py` - Simple registry lookup
- `TOOL_REGISTRY` with 3 tools (whitelist-based)
- Policy-gated access control
- Deterministic execution (no LLM-driven tool selection)

**Capabilities:**
- ✅ Safe tool selection (whitelist prevents injection)
- ✅ Policy-enforced gating
- ✅ No LLM decision-making for tools
- ✅ Predictable, auditable behavior

**Limitations:**
- ❌ No adaptive tool selection (same 3 tools always)
- ❌ Simple keyword trigger (`"exercise"`, `"try"`, `"plan"`)
- ❌ No tool chaining/composition
- ❌ No tool output handling
- ❌ Can't learn which tools work best for user

**Score:** 7/10 (Safe but limited)

---

### 5. Multi-Agent - ❌ MISSING

**Current Implementation:**
- Single monolithic agent
- No agent specialization
- No delegation or coordination
- All functions in one call path

**What We're Missing:**
- Sub-agents for specific domains (crisis specialist, CBT coach, validator)
- Agent communication/coordination
- Load balancing
- Fallback chains
- Hierarchical reasoning

---

## Comparative Analysis: How Leading Agentic Tools Maximize AI Utility

### Claude/Anthropic Model
- **Tool Use:** Flexible, LLM-driven with safety filtering
- **Memory:** Context window management + optional memory files
- **Architecture:** Single powerful model with guided planning
- **Strength:** Flexibility + Safety balance
- **Trade-off:** More expensive, less deterministic

### OpenAI Assistants API
- **Tool Use:** Code interpreter + retrieval + function calls
- **Memory:** Vector store for retrieval-augmented context
- **Architecture:** Single assistant with tool registry
- **Strength:** Integration + standardized tooling
- **Trade-off:** Less control, vendor lock-in

### LangChain Agent Framework
- **Tool Use:** Dynamic routing with LLM selection
- **Memory:** Multiple memory types (long-term, short-term, entity)
- **Architecture:** Modular agents + chains + memory systems
- **Strength:** Composability + flexibility
- **Trade-off:** Complexity, safety requires explicit guardrails

### CBT-Agent Current Approach
- **Tool Use:** Policy-gated deterministic routing
- **Memory:** Simple turn-based history
- **Architecture:** Sequential orchestrator with safety layers
- **Strength:** Predictability + Safety + Auditability
- **Trade-off:** Limited flexibility, context constraints

---

## Enhancement Recommendations

### Phase 1: Memory Layers (HIGH PRIORITY)

**Why:** Enables longitudinal learning and pattern recognition while maintaining safety

**Implementation (3-6 weeks):**

```
1. Semantic Memory Layer
   - Extract key themes/breakthroughs per session
   - Store in compressed format
   - Retrieve relevant context for new conversations
   
2. Improved Working Memory
   - Replace fixed 20-turn window with smart window
   - Prioritize crisis/breakthrough moments
   - Compress routine exchanges
   
3. Session Episodic Memory
   - Store session summaries
   - Retrieve cross-session context
   - Enable "you've mentioned this before" references
```

**Safety Considerations:**
- ✅ Memory retrieval subject to policy validation
- ✅ No sensitive data storage
- ✅ User control over what's remembered
- ✅ Clear privacy boundaries

---

### Phase 2: Context Compressor (HIGH PRIORITY)

**Why:** Reduces costs, improves speed, maintains context precision

**Implementation (2-4 weeks):**

```
1. Smart Summarization
   - Identify resolved vs. ongoing topics
   - Extract key facts and patterns
   - Compress background context
   
2. Salient Content Filter
   - Prioritize crisis/breakthrough mentions
   - Keep recent exchanges intact
   - Compress repetitive exchanges
   
3. Token Optimization
   - Measure token efficiency
   - A/B test compression strategies
   - Monitor safety impact
```

**Safety Considerations:**
- ✅ Compression validates against policy
- ✅ Crisis keywords never compressed
- ✅ Full history stored, compressed version used for LLM only
- ✅ Audit trail of what was compressed

---

### Phase 3: Adaptive Tool Routing (MEDIUM PRIORITY)

**Why:** Current tool selection is too rigid; needs context awareness

**Implementation (4-8 weeks):**

```
1. Context-Aware Tool Selection
   - Analyze user input for tool fit
   - Select most relevant tool(s)
   - Maintain policy-based gating
   
2. Tool Effectiveness Learning
   - Track which tools help users
   - Personalize tool selection
   - Explain tool recommendations
   
3. Tool Chaining
   - Sequence multiple tools
   - Handle tool output
   - Maintain safety through chain
```

**Safety Considerations:**
- ✅ Tool whitelist maintained
- ✅ No LLM-driven execution (policy validates)
- ✅ Each tool call auditable
- ✅ Explicit safety checks per tool

---

### Phase 4: Enhanced Orchestrator (MEDIUM PRIORITY)

**Why:** Support more complex conversation flows

**Implementation (6-12 weeks):**

```
1. State Machine Orchestrator
   - Define conversation states
   - Enable non-linear flows
   - Support recovery paths
   
2. Error Recovery
   - Graceful fallback for LLM failures
   - Alternative response paths
   - User-directed escalation
   
3. Parallel Processing
   - Simultaneous safety checks
   - Asynchronous context retrieval
   - Speed up response generation
```

**Safety Considerations:**
- ✅ Crisis detection always runs first
- ✅ Policy validation before any action
- ✅ Safety checks never skipped
- ✅ State transitions validated

---

### Phase 5: Multi-Agent (LOW PRIORITY - Future)

**Why:** Specialize agents for different concerns

**Not recommended yet because:**
- ❌ Adds complexity without clear safety advantage
- ❌ Coordination overhead
- ❌ Harder to audit and validate
- ❌ CBT delivery benefits from unified agent voice

**Only pursue if:**
- Real-world data shows need for specialization
- Safety impact is well-understood
- Clear user benefit is demonstrated

---

## Implementation Priority Matrix

| Component | Effort | Impact | Safety Risk | Priority |
|-----------|--------|--------|-------------|----------|
| Memory Layers | Medium | High | Low | ⭐⭐⭐ HIGH |
| Context Compressor | Medium | High | Low | ⭐⭐⭐ HIGH |
| Adaptive Tool Routing | Medium | Medium | Low | ⭐⭐ MEDIUM |
| Enhanced Orchestrator | High | Medium | Low | ⭐⭐ MEDIUM |
| Multi-Agent | High | Low | Medium | ❌ DEFER |

---

## Detailed Implementation Plan

### Phase 1: Memory Layers

**Timeline:** Weeks 1-6  
**Team:** 1-2 developers

**Week 1-2: Design & Architecture**
```python
# New modules to create
cbt_agent/
├── memory/
│   ├── __init__.py
│   ├── memory_manager.py      # Orchestrates all memory types
│   ├── semantic_memory.py     # Theme/breakthrough extraction
│   ├── episodic_memory.py     # Session summaries
│   ├── working_memory.py      # Smart conversation window
│   └── memory_store.py        # Persistence layer (JSON/SQLite)
```

**Week 3-4: Core Implementation**
- Semantic memory: Extract themes using keyword clustering
- Episodic memory: Session summarization via extraction
- Storage: JSON format for transparency
- Safety: Policy-based memory validation

**Week 5-6: Integration & Testing**
- Integrate with agent_loop.py
- Test with adversarial test suite
- Measure token reduction
- Verify safety impact

---

### Phase 2: Context Compressor

**Timeline:** Weeks 3-6  
**Team:** 1 developer (can overlap with Phase 1)

**Week 1-2: Compression Strategies**
```python
# New module
cbt_agent/
├── compression/
│   ├── __init__.py
│   ├── compressor.py          # Main compression orchestrator
│   ├── summarizer.py          # Conversation summarization
│   ├── filter.py              # Salient content selection
│   └── evaluator.py           # Measure compression quality
```

**Week 3-4: Implementation**
- Identify resolved vs. ongoing topics
- Summarize using extractive + abstractive methods
- Maintain salient content (crisis keywords, breakthroughs)
- Test compression without losing safety information

**Week 5-6: Validation & Optimization**
- Measure token efficiency
- A/B test compression strategies
- Verify safety keywords aren't lost
- Benchmark with/without compression

---

### Phase 3: Adaptive Tool Routing

**Timeline:** Weeks 7-14  
**Team:** 1-2 developers

**Key Changes:**
```python
# Enhanced tool_router.py
- Add tool selection logic (context-aware)
- Add tool ranking (relevance scoring)
- Add effectiveness tracking
- Maintain policy gating throughout
```

**Implementation:**
- Context analysis: Extract user intent
- Tool scoring: Match intent to tools
- Selection: Pick best tool(s)
- Execution: Route through policy
- Tracking: Record tool usage/outcomes

---

### Phase 4: Enhanced Orchestrator

**Timeline:** Weeks 15-26  
**Team:** 2 developers

**Architecture:**
```python
# New orchestration system
cbt_agent/
├── orchestration/
│   ├── __init__.py
│   ├── state_machine.py       # Conversation states
│   ├── executor.py            # Execute state transitions
│   ├── error_handler.py       # Recovery paths
│   └── validator.py           # Safety validation per state
```

**State Flow:**
```
START → SAFETY_CHECK → CONTEXT_LOAD → TOOL_SELECTION → 
LLM_CALL → VALIDATION → REPAIR → RESPONSE → END
```

---

## Research & Inspiration from Leading Frameworks

### What Works from Claude
- ✅ Flexible tool use with safety guardrails
- ✅ Guided planning (instructions → actions)
- ✅ Clear thinking/reasoning in responses
- **Apply to CBT-Agent:** Add reasoning layer showing thought process

### What Works from LangChain
- ✅ Modular memory systems (short/long/entity)
- ✅ Composable chains and agents
- ✅ Tool chaining and sequencing
- **Apply to CBT-Agent:** Adopt modular memory approach

### What Works from Anthropic
- ✅ Constitutional AI (explicit values)
- ✅ Safety as first-class concern
- ✅ Clear agent roles and boundaries
- **Apply to CBT-Agent:** Already strong here, extend to specialized sub-agents

### What CBT-Agent Does Better
- ✅ Safety-first (not bolted on)
- ✅ Policy-as-code (auditable)
- ✅ Deterministic (reproducible)
- ✅ Specialized for domain (mental health)
- **Maintain these** while adding utility

---

## Risk Assessment & Mitigation

### Risk 1: Memory Leakage
**Risk:** Sensitive mental health data stored unencrypted  
**Mitigation:**
- Encryption at rest
- Clear retention policies
- User control over memory
- Regular audits

### Risk 2: Context Compression Loss
**Risk:** Important safety signals compressed away  
**Mitigation:**
- Never compress crisis keywords
- Maintain full audit trail
- A/B test compression impact
- Conservative compression initially

### Risk 3: Increased Complexity
**Risk:** More code = more bugs = safety issues  
**Mitigation:**
- Modular implementation
- Extensive testing
- Backward compatibility
- Gradual rollout

### Risk 4: Performance Degradation
**Risk:** Memory/compression adds latency  
**Mitigation:**
- Async operations where possible
- Caching strategies
- Performance monitoring
- Fallback to simple mode

---

## Success Metrics

### Phase 1: Memory Layers
- ✅ Cross-session context retention
- ✅ Breakthrough pattern recognition
- ✅ Zero loss of crisis keywords
- ✅ User satisfaction +15%

### Phase 2: Context Compressor
- ✅ 50-70% token reduction
- ✅ <100ms compression overhead
- ✅ Zero safety signal loss
- ✅ Cost reduction 40%+

### Phase 3: Adaptive Tool Routing
- ✅ Tool relevance score >0.8
- ✅ User satisfaction with suggestions +20%
- ✅ Tool usage increase 30%+
- ✅ Policy violations 0

### Phase 4: Enhanced Orchestrator
- ✅ Non-linear conversation support
- ✅ Error recovery success 95%+
- ✅ State transition success 99%+
- ✅ Safety maintained throughout

---

## Resource Requirements

| Phase | Duration | Team | Effort (person-weeks) | Budget |
|-------|----------|------|----------------------|--------|
| Phase 1: Memory | 6 weeks | 1-2 | 8-12 | $20k-30k |
| Phase 2: Compressor | 4 weeks | 1 | 4-6 | $10k-15k |
| Phase 3: Tool Routing | 8 weeks | 1-2 | 8-12 | $20k-30k |
| Phase 4: Orchestrator | 12 weeks | 2 | 18-24 | $45k-60k |
| **Total** | **30 weeks** | **2-3** | **38-54** | **$95k-135k** |

---

## Rollout Strategy

### Phase A: Internal Testing (Weeks 1-4)
- Develop on feature branches
- Test with adversarial suite
- Validate safety impact
- Get team approval

### Phase B: Beta Testing (Weeks 5-8)
- Deploy to limited users
- Collect feedback
- Monitor safety metrics
- Gather performance data

### Phase C: General Release (Weeks 9+)
- Gradual rollout
- Monitor metrics
- Support users
- Plan next phase

---

## Conclusion

**CBT-Agent is architecturally sound for its current purpose** (safety-critical conversational AI for mental health), but can be significantly enhanced without compromising safety.

**Recommended approach:**
1. **Implement memory layers** (High value, manageable complexity)
2. **Add context compression** (High ROI, safety-friendly)
3. **Enhance tool routing** (Incremental, well-proven)
4. **Consider orchestrator upgrade** (Longer term, higher complexity)
5. **Defer multi-agent** (Not needed, adds risk without proportional benefit)

This balanced approach maximizes utility (more like Claude/LangChain) while maintaining CBT-Agent's core strengths (safety, auditability, specialization).

---

**Author:** Yu-Chueh Wang (yuchuehw@uci.edu)  
**Status:** Strategic Plan Ready for Review  
**Next Step:** Team discussion on priority and resource allocation

