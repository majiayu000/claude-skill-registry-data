---
name: handoff_writer
description: Write a compact HANDOFF.md snapshot to restore context after session resets.
metadata:
  short-description: Write handoff snapshot
---

## Purpose
Create a short, high-signal state snapshot that survives long runs and chat
resets.

## Steps
1. Summarize the active task, current status, and next actions.
2. Link to `PLANS.md`, `AUTO_CONTEXT.md`, relevant files, and ADRs.
3. Record last verification commands and outcomes.
4. Keep it concise and update it at major milestones.

## Output
- Update `.agent-docs/memory/HANDOFF.md`.

## Guardrails
- Do not include secrets or sensitive data.
- Prefer links and file paths over large pasted content.
