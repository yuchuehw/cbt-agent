# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Reorganized project structure: code moved to `src/cbt_agent/`, docs consolidated in `docs/`
- Added `QUICKSTART.md` for quick setup guide
- Added `docs/DIRECTORY_STRUCTURE.md` explaining new organization
- Updated author information: Yu-Chueh Wang (yuchuehw@uci.edu)

### Changed
- Consolidated multiple root-level documentation files into `QUICKSTART.md`
- Moved documentation files to `docs/` folder
- Updated all author and contact information
- Improved file organization for better maintainability

### Fixed
- None yet in this unreleased version

## [0.1.0] - 2026-04-26

### Added
- Initial scaffold: 4-layer architecture (prompt + policy + runtime + sandbox)
- Policy enforcement framework with machine-readable `cbt_policy.json`
- Crisis detection with keyword matching and high-risk temporal markers
- Subtle harm detection: three-pattern matching (substance + procurement + context)
- Response validators: generic empathy, deceptive empathy, over-validation, gaslighting, abandonment
- CBT-specific validators: tentative language, context citation, collaborative check-in, cultural humility
- Response repair mechanism: targeted fixes without requiring full regeneration
- Tool router with whitelist-based access control
- MHealth-EVAL scoring (appropriateness, trustworthiness, safety)
- CLI interface with slash command support (`/cbt`, `/tool`, `/help`, `/reset`, `/exit`)
- HTTP bridge for external UIs with session management
- Adversarial test suite with 6 scenario types
- System prompt with explicit behavioral rules aligned with evidence-based CBT
- Configuration file for model selection, runtime settings, and safety toggles
- Fallback response generation when OPENAI_API_KEY not set
- Comprehensive documentation (2,400+ lines across 8 guides)
- Research foundation with 15+ peer-reviewed paper citations
- GitHub integration (CI/CD, templates, workflows)
- Type hints and docstrings throughout codebase

### Guardrails & Safety Features
- Epistemic humility: Enforce tentative language and limit hypotheses (max 2 per response)
- Grounded empathy: Block generic and deceptive empathy phrases
- Collaborative stance: Require check-in ("Does this fit your experience?")
- User-led interpretation: Require context citation from user input
- Minimal interventions: Max 1 CBT exercise per turn
- Non-authoritative language: Avoid claiming psychological certainty
- Crisis override: Switch to safety mode immediately, skip CBT interventions
- Cultural humility: Signal respect for cultural/religious/family context when mentioned
- Trustworthiness: Block unverified numbers, flag US-centric defaults for non-US users
- Substance harm prevention: Refuse to help with accessing alcohol/drugs
- Abandonment prevention: Maintain commitment language in all responses

### Research Foundation
- Architecture informed by IAPT integration (Clark, 2011) and collaborative CBT (Cuijpers et al., 2019)
- Crisis detection grounded in natural language markers research (Walsh et al., 2017)
- MHealth-EVAL framework adopted from Fitzpatrick et al. (2017)
- Policy-as-code approach supports reproducible, auditable safety enforcement
- Tool router whitelist prevents prompt injection (Christiano et al., 2016)

### Documentation
- Comprehensive README with quick-start and examples
- docs/ARCHITECTURE.md: Complete system design (400+ lines)
- docs/RESEARCH.md: Research citations (450+ lines)
- docs/DEV_GUIDE.md: Development setup (350+ lines)
- docs/CONTRIBUTING.md: Contributor guide (300+ lines)
- docs/INDEX.md: Documentation index (250+ lines)
- SAFETY_NOTICE.md: Legal disclaimers and limitations
- TERMS.md: User terms of service
- PRIVACY.md: Privacy and data handling
- LICENSE: MIT license

---

## Version Guidelines

- **MAJOR version** (e.g., 1.0.0): Breaking changes (e.g., policy schema change, API signature change)
- **MINOR version** (e.g., 0.1.0): New features added in backward-compatible manner
- **PATCH version** (e.g., 0.0.1): Bug fixes and minor improvements

---

## How to Contribute

See [docs/CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Code style and type hints
- Testing requirements
- Documentation standards
- Pull request process
- Research citation best practices

---

## Future Roadmap (Potential)

Possible future enhancements (not yet committed):

- **Session persistence:** JSON/SQLite-backed conversation history
- **Async support:** Non-blocking LLM calls and tool execution
- **Multi-provider support:** Claude, Anthropic, open-source models
- **Advanced NLP:** Sentiment analysis, topic modeling, semantic similarity for harm detection
- **Memory system:** Long-term user profile, custom preferences
- **A/B testing:** Policy variation experimentation
- **Monitoring:** Metrics, alerting, incident response
- **Deployment:** Docker containerization, cloud-ready setup
- **Localization:** Multi-language support and region-specific resources
- **Advanced evaluation:** Automated scorer for helpfulness, cultural appropriateness, safety

---

**Maintained by:** Yu-Chueh Wang (yuchuehw@uci.edu)  
*Last updated: 2026-04-26*

