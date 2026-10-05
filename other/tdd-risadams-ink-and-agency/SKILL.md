---
name: tdd
category: codebase-build
description: Test-driven development — the red → green loop and the rules that make its tests worth keeping. Use when the user wants to build a feature or fix a bug test-first, mentions "red-green-refactor", TDD, or integration tests.
codex-short-description: "The red → green loop, done so tests are worth keeping"
compatibility: claude-code codex opencode
---

# Test-Driven Development

TDD is the **red → green** loop. This skill is the reference that makes the loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle — consult them before and during the loop, not after.

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

## What a good test is

Tests verify **behaviour through public interfaces**, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists — and survives refactors because it doesn't care about internal structure.

See [tests.md](tests.md) for good/bad examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams — where tests go

A **seam** is the public boundary you test at: the interface where you observe behaviour without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam. You can't test everything — agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

**Present candidate seams with their trade-offs, never as a bare list of names.** A prompt that offers "the component seam, the route handler, or the integration seam" asks the user to choose between labels. For each candidate give:

- **What it catches** — the class of bug a test here would fail on.
- **What it misses** — what passes straight through it.
- **What it costs** — rough speed and setup, and whether it survives a refactor of the code beneath it.

Then recommend one and say why. Where the shape of the interface is itself the open question rather than where to test it, that's the [codebase-design](../codebase-design/) vocabulary — seam, depth, adapter — and worth settling first.

**Not every change earns the loop.** Config, wiring, glue, type-only changes, and straight CRUD delegation have no independent source of truth to assert against, so a test written for them restates the implementation and lands you in the tautological anti-pattern below from the other direction. When a change looks like that, say so and propose the seam one level up — the behaviour the glue serves — or no test at all. That judgement is part of agreeing the seams, not a step to skip past.

## Anti-patterns

- **Implementation-coupled** — mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behaviour hasn't changed.
- **Tautological** — the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a hand-derived snapshot, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth — a known-good literal, a worked example, the spec.
- **Horizontal slicing** — writing all tests first, then all implementation. Bulk tests verify *imagined* behaviour: you test the *shape* of things rather than user-facing behaviour, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** — one test → one implementation → repeat, each test a **tracer bullet** responding to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** It belongs to the review stage (see the `code-review` skill), not the red → green implementation cycle.

> **Host portability:** tool names follow Claude Code conventions; on other hosts map by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/tdd.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
