name: Feature Request
description: Suggest a new feature or improvement
title: "[FEATURE] "
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Thank you for suggesting an enhancement! Help us understand your use case and proposal.
  
  - type: textarea
    id: problem
    attributes:
      label: Problem Statement
      description: Describe the problem this feature would solve
      placeholder: "Currently there is no way to... which makes it difficult to..."
    validations:
      required: true
  
  - type: textarea
    id: proposed-solution
    attributes:
      label: Proposed Solution
      description: Describe the feature you'd like
      placeholder: "I propose adding..."
    validations:
      required: true
  
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: Describe any alternative solutions or features
      placeholder: "Alternative 1: ... (pros/cons)"
    validations:
      required: false
  
  - type: textarea
    id: use-case
    attributes:
      label: Use Case
      description: Describe the use case (clinical, research, educational, etc.)
      placeholder: "This would enable..."
    validations:
      required: false
  
  - type: textarea
    id: references
    attributes:
      label: Research or Reference Links
      description: Any papers, discussions, or external references
      placeholder: "See [paper]: ..."
    validations:
      required: false
  
  - type: checkboxes
    id: contribution
    attributes:
      label: Contribution
      description: Are you interested in contributing this feature?
      options:
        - label: "I'm willing to help implement this feature"
        - label: "I'm willing to help test/evaluate this feature"

