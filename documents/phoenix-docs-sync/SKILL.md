---
name: phoenix-docs-sync
description:
  'Syncs calculations documentation and JSDoc with actual behavior. Use after
  non-trivial changes to calculation modules.'
---

# Phoenix Docs Sync

You keep docs and comments aligned with reality for all calculation modules.

## When to Use

- After modifying:
  - XIRR, waterfall, fees, capital allocation, exit recycling, or reserve logic
- When:
  - Truth-case semantics change
  - Clawback behavior is clarified or corrected
  - Precision / Decimal.js logic changes

## Targets

- `docs/calculations.md`
- Relevant sections in `README.md`
- JSDoc in:
  - `server/analytics/*.ts`
  - Shared types for waterfalls, fees, etc.
- Phase reports:
  - `docs/phase0-validation-report.md`
  - `docs/phase1a-completion-report.md`

## Workflow

1. Read the updated code and any relevant truth-case JSONs.
2. Update documentation to:
   - Describe what the module computes in plain English.
   - Highlight key assumptions and invariants.
   - Reference example truth-case IDs where helpful.
3. Update JSDoc:
   - Parameters
   - Returns
   - Semantics (especially around clawback and precision)
4. Ensure no documentation mentions outdated semantics (e.g., "hard floor" for
   clawback when implementation is shortfall-based partial).

## Invariants

- Docs must never contradict the actual implementation or truth cases.
- Any semantic change to a calculation should be reflected in docs and JSDoc in
  the same PR or change set.
