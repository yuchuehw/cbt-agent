# Quick Start Guide

Welcome to **CBT Agent**—a research-backed, policy-enforcing conversational system for CBT-style dialogue.

## ⚡ 5-Minute Setup

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

## 🎯 Next Steps

| Goal | Read This |
|------|-----------|
| **Understand the system** | `docs/ARCHITECTURE.md` |
| **See research foundation** | `docs/RESEARCH.md` |
| **Set up development** | `docs/DEV_GUIDE.md` |
| **Contribute** | `docs/CONTRIBUTING.md` |
| **Publish to GitHub** | `docs/GITHUB_PUBLISH_GUIDE.md` |

## 📝 Key Features

- ✅ **4-layer safety architecture** (Prompt → Policy → Runtime → Validators)
- ✅ **Crisis detection before LLM** (keyword + high-risk markers)
- ✅ **Subtle harm detection** (3-pattern matching)
- ✅ **Response validation & repair** (targeted fixes without regeneration)
- ✅ **Research-backed** (15+ papers cited)
- ✅ **GitHub-ready** (CI/CD, templates, guides)

## 🚀 Try It

```
User: I keep overthinking mistakes at work.

Agent: From what you described, overthinking mistakes can feel heavy.
One possibility is this pattern could shift with targeted attention.
Does this fit your experience?

Suggested: Thought log: write one worry, evidence for/against, balanced thought.
```

## ⚠️ Important

**This is NOT a therapist, medical device, or emergency service.**
- See `docs/SAFETY_NOTICE.md` for full disclaimers
- In crisis: Call 988 (US/Canada) or local emergency services

## 📚 Documentation

- `README.md` — Overview and features
- `docs/ARCHITECTURE.md` — System design
- `docs/RESEARCH.md` — Research citations
- `docs/DEV_GUIDE.md` — Development setup
- `docs/CONTRIBUTING.md` — How to contribute
- `docs/INDEX.md` — Documentation index

## 💬 Questions?

Check the relevant documentation above or open an issue on GitHub.

---

**Author:** Yu-Chueh Wang  
**Email:** yuchuehw@uci.edu  
**License:** MIT

