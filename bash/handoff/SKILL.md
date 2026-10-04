---
name: handoff
description: Prepare a portable context-rich handoff prompt for another coding agent.
category: utilities
aliases: []
triggers:
- use handoff
- run handoff
keywords:
- handoff
- utilities
- prepare
- portable
- context
- rich
- handoff
dependencies:
- optional:clipboard-tool
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- handoff
- utilities
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- handoff
- portable
- prepare
- utilities
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Handoff

## Purpose
Prepare a portable context-rich handoff prompt for another coding agent.

## When to Use
Use when you need to prepare a portable context-rich handoff prompt for another coding agent. or trigger commands matching use handoff, run handoff.

## When NOT to Use
Do not use outside permitted scope or when authorization is missing.

## Capabilities
- Prepare a portable context-rich handoff prompt for another coding agent.
- Deterministic step-by-step execution
- Structured artifact validation

## Inputs
Natural-language request, execution context, and configuration parameters.

## Workflow
1. Identify the task from the user text. If the user gives only a short label,
   infer from the current repo, recent discussion, branch name, linked issue/PR,
   docs, and obvious nearby context.
2. Gather enough context to write a useful handoff: repo/product identity,
   relevant issue/PR/branch names, likely modules, constraints, and known
   symptoms. Do not perform the receiving agent's full independent review or
   decide the final technical direction for them.
3. Write a standalone prompt for a fresh agent.
4. Copy the full prompt to the clipboard.
5. Final reply: terse confirmation with the task title. Do not paste the full
   prompt unless the user asks.

## Tools
optional:clipboard-tool

## Examples
Example usage:
```bash
# Invoke via skills CLI
python scripts/skills/skills.py route "use handoff"
```

## Safety
Never perform destructive unconfirmed modifications. Adhere to zero-trust boundaries.

## Source
Imported from openclawskills.net.

## Notes
Maintained as part of canonical utilities category.
