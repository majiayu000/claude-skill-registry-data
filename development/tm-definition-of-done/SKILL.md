---
name: tm-definition-of-done
description: Enforce Tavern Master definition of done (lint + tests + formatting + plan updates).
---

## When to use
Use for any change that modifies code, UI, data, sync, or build configuration.

## Operating rules
- Follow `AGENTS.md` (ask clarifying questions when required; don’t guess).
- Keep changes reviewable: small, focused commits; avoid sweeping refactors unless explicitly requested.

## Definition of done checklist
After making changes (or before presenting a final patch):
1. Run:
   - `npm run lint`
   - `npm run test`
   - `npm run format:check`
2. If scope or sequencing changed, update `IMPLEMENTATION_PLAN.md` (keep it a living checklist).
3. If UI changed, ensure:
   - labels match the screen’s intent
   - keyboard focus order is reasonable
   - no obvious contrast regressions (per existing theme)
4. Summarize:
   - what changed
   - commands run + results
   - any follow-up items and where they’re tracked
