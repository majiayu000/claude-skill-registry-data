---
name: context_compactor
description: Compress long-run context into handoff, backlog, and action logs.
metadata:
  short-description: Compact long-run context
---

## Purpose
Keep context small and recoverable across long sessions.

## Steps
1. Summarize current state into `HANDOFF.md`.
2. Rotate or trim `AUTO_CONTEXT.md`.
3. Update `BACKLOG.md` with open items.
4. Respect `LINE_BUDGETS.yaml` limits.
5. Record a compact Action Log entry.

## Guardrails
- Do not remove evidence or required references.
