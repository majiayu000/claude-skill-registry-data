---
name: test-driven-development
description: Test-driven development. Use before writing implementation code for any feature or bugfix, when the user mentions "TDD" or "red-green-refactor", or wants integration-style tests.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Test-Driven Development

Read `learnings.md` beside this file before starting; append an entry when a "should be a seam" boundary turns out not to be.

TDD is the **red → green loop**. This skill makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Consult every section before and during the loop, not after.

See [test.md](test.md) for good/bad examples and [mocking.md](mocking.md) for what to mock in this stack.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. A good test reads like a spec — "createComment rejects an empty body" tells you exactly what capability exists — and survives refactors because it doesn't care about internal structure.

## Seams — where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. In this repo the seams are:

- **Validation schemas** (`src/verification/*.validation.ts`) — `safeParse` against valid/invalid shapes.
- **Service functions** (`src/server/actions/Database/services/`) — the exported function's input → `ok:true/false` result contract (invariant #4 in `CLAUDE.md`).
- **Authorization functions** (invariant #5) — pure functions taking a session, returning a decision.

**Test only at pre-agreed seams.** Before writing any test, state which seam you're testing and confirm it with the user — don't silently pick your own scope. You can't test everything; agreeing the seam up front is how effort lands on the critical paths instead of every edge case.

Don't test through the Cloudflare Workers runtime itself — that's a separate, explicit decision (e.g. `@cloudflare/vitest-pool-workers`), not a default.

## Anti-patterns

- **Implementation-coupled** — mocks internal collaborators, tests private helpers, or verifies through a side channel (querying Neon directly instead of going through the service's own read function). Tell: the test breaks on refactor even though behavior didn't change.
- **Tautological** — the expected value is recomputed the way the code computes it, so it passes by construction. Expected values must come from an independent source — a known-good literal, a worked example.
- **Horizontal slicing** — writing all tests first, then all implementation. Tests the imagined *shape* of things instead of real behavior. Work in **vertical slices**: one seam → one test → one minimal implementation → repeat.

## Rules of the loop

- **Red before green.** Write the failing test first (`npm test`), confirm it fails for the right reason, then write only enough code to pass it. Don't anticipate future tests.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** Cleanup belongs to the review stage, not the red → green cycle — hand off to `/refactor` or `/full-review` once the slice is green, don't interleave it.

## Handoffs

- Slice is green, structure needs cleanup → `/refactor` (separate step, not part of this cycle).
- Feature's TDD cycles are done → `/full-review` to validate.
