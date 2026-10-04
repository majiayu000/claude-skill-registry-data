---
name: agent-retrospective
description: "Analyzes repeated agent failures or noisy routing and proposes evidence-backed changes to instructions, skills, gates, or runbooks."
---

# Agent Retrospective

Turn repeated agent failure into a small process fix.

## Workflow

1. Identify the failure pattern from actual evidence.
2. Separate one-off mistakes from durable routing or instruction problems.
3. Propose the smallest instruction, skill, or validation update.
4. If editing instructions, use `agents-md-retrospective`.
5. Record validation or explain why only a documentation change was possible.

## Output

- failure pattern
- root cause category
- proposed fix
- files to edit
- validation plan
- residual risk

## Rule

Do not add broad personality prompts. Improve routing, evidence requirements,
or validation gates instead.
