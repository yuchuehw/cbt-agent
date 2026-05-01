"""CBT Agent: Research-Backed Conversational Safety Architecture

A policy-enforcing, 4-layer conversational system for CBT-style dialogue, built
on evidence-based guardrails and designed for educational, research, and
supervised clinical use.

Quick Start:
    from cbt_agent.agents.cbt_agent import CbtAgent
    agent = CbtAgent()
    response = agent.run_turn("I feel stuck.")
    print(response.text)

Key Modules:
    - agents: CbtAgent interface for conversation management
    - runtime: Agent loop, crisis detection, policy enforcement
    - guardrails: Validators, pattern detectors, response repair
    - tools: CBT exercises and safety responses
    - bridge: HTTP server for external UIs
    - evals: Adversarial test suite and evaluation harness
    - policies: Machine-readable policy constraints (JSON)
    - prompts: System prompt with behavioral rules

Documentation:
    - README.md: Overview and quick start
    - docs/ARCHITECTURE.md: Detailed system design and data flow
    - docs/RESEARCH.md: Research citations for each guardrail
    - CONTRIBUTING.md: Development guide and contribution process
    - CHANGELOG.md: Version history and release notes

Research Base:
    This project is grounded in peer-reviewed research on CBT delivery,
    crisis detection, digital mental health safety, and fairness in AI.
    See docs/RESEARCH.md for complete citations and references.

Author: Yu-Chueh Wang (yuchuehw@uci.edu)
License: MIT
"""

__version__ = "0.1.0"
__author__ = "Yu-Chueh Wang"
__email__ = "yuchuehw@uci.edu"
__all__ = ["CbtAgent"]

from cbt_agent.agents.cbt_agent import CbtAgent

__doc__

