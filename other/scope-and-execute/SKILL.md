---
name: scope-and-execute
description: Analyze a problem, plan the fix, execute with verification. Use when tackling a non-trivial bug, feature, or refactor that needs structured approach.
triggers:
  - fix this area
  - implement this feature
  - refactor this
  - scope this out
---

# Scope and Execute

Structured approach for bounded implementation work.

## Phase 1: Analyze (read-only)

1. Identify affected files and modules
2. Check existing tests for the area
3. Note dependencies and side effects
4. State assumptions explicitly

## Phase 2: Plan

Write a brief plan:

1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]

## Phase 3: Execute

- Work through plan steps sequentially
- Run verification after each step
- If a step fails, diagnose before continuing
- Commit after each functional unit

## Phase 4: Verify

Run the full verification sequence:

1. `pnpm lint` — no new warnings
2. `pnpm catalog:validate` — if catalog files changed
3. `pnpm test` — all tests pass
4. `pnpm workspace:validate` — full workspace check

## Rules

- Touch only what's needed (surgical changes)
- No speculative features
- Match existing code style
- Remove only your own orphaned code
