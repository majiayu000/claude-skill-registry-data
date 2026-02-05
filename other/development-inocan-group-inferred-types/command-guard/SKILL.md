---
name: command_guard
description: Enforce .agentpolicy rules before executing commands.
metadata:
  short-description: Command safety guard
---

## Purpose
Prevent destructive or risky commands without explicit approval.

## Steps
1. Read `.agentpolicy` before running commands.
2. Block denied commands and request confirmation for guarded ones.
3. Record the decision in the Action Log.

## Guardrails
- Always respect `.agentpolicy` and `.agentignore`.
