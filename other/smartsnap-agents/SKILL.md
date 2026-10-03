---
name: smartsnap-agents
title: "SmartSnap: Proactive Evidence Seeking for Self-Verifying Agents"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.22322
keywords: [agents, verification, self-improvement, evidence-gathering]
description: "Shift agent verification from post-hoc external judgment to proactive in-situ self-evidence curation. Agents generate atomic evidence tuples during execution, guided by 3C principles (Completeness, Conciseness, Creativity), with structured verifier feedback across four dimensions—reducing verification costs and enabling dense learning signals."
---

## Overview

SmartSnap enables agents to prove their success rather than waiting for external verification.

## Core Technique

**3C Evidence Principles:**

```python
evidence = agent.gather_evidence(
    completeness=include_all_pivotal_actions,
    conciseness=minimize_redundancy,
    creativity=generate_additional_proof_actions
)
```

**Evidence Definition:**
Atomic (action, observation) tuples—objective facts.

## When to Use

Use when: Agent verification critical, reducing cognitive load, dense learning signals.

## References

- Proactive evidence gathering
- Atomic evidence definition
- Structured verifier feedback
