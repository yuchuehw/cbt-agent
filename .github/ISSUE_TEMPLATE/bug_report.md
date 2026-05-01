name: Bug Report
description: Report a bug or unexpected behavior
title: "[BUG] "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thank you for reporting a bug! Please provide as much detail as possible to help us understand and fix the issue.
  
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Clear and concise description of the bug
      placeholder: "The agent incorrectly handled..."
    validations:
      required: true
  
  - type: textarea
    id: reproduce
    attributes:
      label: Steps to Reproduce
      description: Detailed steps to reproduce the bug
      placeholder: |
        1. Run `python main.py`
        2. Input: "..."
        3. Expected: "..."
        4. Actual: "..."
    validations:
      required: true
  
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What should have happened
      placeholder: "The agent should have..."
    validations:
      required: true
  
  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: What actually happened
      placeholder: "The agent instead..."
    validations:
      required: true
  
  - type: input
    id: python-version
    attributes:
      label: Python Version
      description: Output of `python --version`
      placeholder: "Python 3.10.5"
    validations:
      required: true
  
  - type: input
    id: os
    attributes:
      label: Operating System
      description: Your operating system
      placeholder: "Windows 10, macOS 13, Ubuntu 22.04"
    validations:
      required: true
  
  - type: input
    id: openai-status
    attributes:
      label: OpenAI API Key Status
      description: Do you have OPENAI_API_KEY set?
      placeholder: "Yes / No"
    validations:
      required: false
  
  - type: textarea
    id: additional
    attributes:
      label: Additional Context
      description: Any other context or error messages
      placeholder: "Error stack trace, logs, etc."
    validations:
      required: false

