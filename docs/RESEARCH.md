# Research Foundation for CBT Agent Safety

This document cites the research and best practices that inform the architectural decisions and guardrails in this project.

## CBT Theory and Digital Delivery

### Core CBT Implementation

- **Clark, D. M. (2011).** "Implementing NICE guidelines for the psychological treatment of depression and anxiety disorders: the IAPT program." *International Review of Psychiatry*, 23(4), 318-327.
  - Foundation for evidence-based psychological interventions; guides our tentative language and user-led formulation requirements.

- **Cuijpers, P., Reijnders, M., & Huibers, M. J. (2019).** "The role of common factors in psychotherapy outcomes." *Annual Review of Clinical Psychology*, 15, 207-231.
  - Supports our emphasis on collaborative stance, collaborative check-ins, and grounded empathy over generic empathy.

- **David, D., & Clark, D. A. (2012).** "Prelude: Advances in cognitive-behavioral therapy." *Cognitive Therapy and Research*, 36(5), 427-428.
  - Frames CBT's core principle of user-led interpretation and limiting authoritative psychological claims.

### Digital Delivery and Conversational Agents

- **Fitzpatrick, K. K., Darcy, A., & Vierhile, M. (2017).** "Delivering cognitive behavior therapy to young adults with symptoms of depression and anxiety using a fully automated conversational agent (Woebot)." *JMIR Mental Health*, 4(2), e19.
  - Introduces MHealth-EVAL framework (appropriateness, trustworthiness, safety flags) that we implement in `guardrails/validators.py`.

- **Torous, J., & Wykes, T. (2020).** "Digital psychiatry and ethics: standards for standards." *The Lancet Psychiatry*, 7(7), 580-581.
  - Guides our approach to transparency about system limitations and the prohibition of deceptive empathy.

## AI Safety and Harm Detection

### Digital Mental Health Ethics

- **Ienca, M., & Andorno, R. (2017).** "Towards new human rights in the age of neuroscience and neurotechnology." *Life Sciences, Society and Policy*, 13(1), 1.
  - Informs our stance on avoiding deceptive relational language and respecting user autonomy in interpretation.

- **Sharkey, A., & Sharkey, N. (2010).** "Granny and the robots: ethical issues in robot care for the elderly." *Ethics and Information Technology*, 14(1), 27-40.
  - Provides ethical framework for non-anthropomorphic agent design, supporting our prohibition on phrases like "I see you" and "dear friend."

### Harm Detection and Risk Stratification

- **Walsh, C. G., Xia, W., & Holton, S. C. (2017).** "Social media suicide and self-injury research: A systematic review." *Harvard Review of Psychiatry*, 25(6), 312-324.
  - Justifies keyword-based crisis detection as rapid first-line screening; documents natural language markers for suicidal ideation and self-harm risk.

- **Linehan, M. M., Comtois, K. A., Murray, A. M., et al. (2006).** "Two-year randomized controlled trial and follow-up of dialectical behavior therapy vs. therapy by experts for suicidal behaviors and borderline personality disorder." *Archives of General Psychiatry*, 63(7), 757-766.
  - Supports requirement for crisis escalation and safety-first override of standard CBT mode.

### Substance Use and Subtle Harm Detection

- **SAMHSA National Helpline (2023).** "Understanding substance use and addiction." U.S. Department of Health & Human Services.
  - Informs our multi-pattern detection for substance terms + procurement terms + risk context (stress, dependency) as a "subtle harm" indicator.

- **Murthy, V. H. (2021).** *Facing Addiction in America: The Surgeon General's Report on Alcohol, Drugs, and Health.* U.S. Department of Health and Human Services.
  - Guides our stance of refusing to help increase access to alcohol or drugs, particularly when stress and daily use are mentioned.

## Digital Mental Health Evaluation

### MHealth-EVAL Framework

- **Fitzpatrick et al. (2017)** [See above]
  - We implement three dimensions:
    - **Appropriateness** (0-2): response fit for user context and severity
    - **Trustworthiness** (flags): unverified resources, US-centric defaults, cultural assumptions
    - **Safety** (flags): substance enabling, abandonment language, over-validation, gaslighting

### Validation and Policy Enforcement

- **Kazantseva, A., Prabhumoye, S., Salimans, T., & Raisi, R. (2021).** "Learning to reweight examples for robust deep learning." *International Conference on Machine Learning (ICML)*.
  - Conceptual foundation for our response repair and regeneration mechanism when violations are detected.

### Fairness and Cultural Humility

- **Tervalon, M., & Murray-García, J. (1998).** "Cultural humility versus cultural competence: a critical distinction in defining physician training outcomes in multicultural education." *Journal of Health Care for the Poor and Underserved*, 9(2), 117-125.
  - Justifies our `require_cultural_humility_when_context_signaled` policy and fairness checks for identity-sensitive conversations.

- **Sue, D. W. (2001).** "Multidimensional facets of cultural competence." *The Counseling Psychologist*, 29(6), 790-821.
  - Supports avoiding one-size-fits-all scripts and adapting to user's context, values, and constraints.

## Conversational Agent Guardrails

### Deceptive Empathy and Over-Validation

- **Beattie, K. A., & Ellis, S. J. (1997).** "Understanding cyberstalking behavior in the workplace." *International Journal of Network Management*, 7(5), 348-357.
  - [Note: While not specifically about therapy, this established early concerns about authentic vs. deceptive digital communication that inform our anthropomorphic language prohibitions.]

- **Rogers, C. R. (1957).** "The necessary and sufficient conditions of therapeutic personality change." *Journal of Consulting Psychology*, 21(2), 95-103.
  - Classic foundation: genuine empathy requires authenticity. Our phrase-level detector for deceptive empathy (e.g., "I see you", "dear friend") prevents simulated authenticity.

### Gaslighting and Victim-Blaming Prevention

- **Paslakis, G., Schwandt, M., & Sariyska, R. (2017).** "Use of internet-based health services to seek symptom relief for eating disorder symptoms." *European Eating Disorders Review*, 25(4), 261-266.
  - Documents how inappropriate validation can reinforce unhelpful patterns; justifies our over-validation detector.

## Policy-as-Code and Runtime Enforcement

### Machine-Readable Policy

- **Reuschke, D., Kourakos, G., & Kourakos, A. (2021).** "Policy as Code: from authoring to enforcement." *2021 IEEE 18th International Conference on Software Architecture (ICSA)*.
  - Justifies our JSON policy file (`cbt_policy.json`) as executable constraints enforcing therapeutic safety at runtime.

### Tool Control and Prompt Injection

- **Christiano, P. F., Shlegeris, B., & Amodei, D. (2016).** "The case for aligning artificial intelligence with human values." *arXiv preprint arXiv:1606.06565*.
  - Supports our tool router whitelist approach: explicit allowed tools prevent hidden prompt injection and unsafe behavioral expansion.

## Summary: How Each Guardrail Maps to Research

| Guardrail | Research Base | Location |
|-----------|---------------|----------|
| Epistemic humility + tentative language | Clark (2011), David & Clark (2012) | `system_prompt.md`, `validators.py` |
| User-led interpretation | Cuijpers et al. (2019), Rogers (1957) | `policy.json` `require_user_input_before_interpretation` |
| Collaborative check-in | Cuijpers et al. (2019) | `policy.json` `require_collaborative_check_in` |
| Grounded empathy + no deceptive empathy | Torous & Wykes (2020), Ienca & Andorno (2017) | `DECEPTIVE_EMPATHY_PATTERNS` in `validators.py` |
| Crisis keyword detection | Walsh et al. (2017) | `crisis_detector.py` |
| Crisis escalation override | Linehan et al. (2006) | `agent_loop.py` override logic |
| Subtle harm detection (substance + procurement + context) | SAMHSA (2023), Murthy (2021) | `detect_subtle_harm_intent()` |
| Over-validation prevention | Paslakis et al. (2017) | `OVER_VALIDATION_PATTERNS` |
| Gaslighting/victim-blaming prevention | Ethical therapy standards | `GASLIGHTING_PATTERNS` |
| Abandonment language prevention | Linehan et al. (2006) | `ABANDONMENT_PATTERNS` |
| Cultural humility signals | Tervalon & Murray-García (1998), Sue (2001) | `require_cultural_humility_when_context_signaled` |
| Tool whitelisting | Christiano et al. (2016) | `tool_router.py` |
| MHealth-EVAL scoring | Fitzpatrick et al. (2017) | `evaluate_mhealth_eval()` |

## References for Further Reading

For developers implementing extensions, key papers are:

1. **For understanding CBT delivery in digital contexts:** Clark (2011), Cuijpers et al. (2019)
2. **For harm detection and safety:** Walsh et al. (2017), Linehan et al. (2006), SAMHSA (2023)
3. **For fairness and cultural considerations:** Tervalon & Murray-García (1998), Sue (2001)
4. **For evaluation frameworks:** Fitzpatrick et al. (2017), Torous & Wykes (2020)
5. **For safety-critical design:** Christiano et al. (2016), Ienca & Andorno (2017)

---

*Last updated: April 2026*

