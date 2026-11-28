---
name: test-design
description: What to test and how — regression test fails first, boundary tables, behavior over implementation, boundary-only mocks, the mock-echo trap, proving new tests can fail. Use when writing or reviewing tests, adding regression coverage for a fix, asked "is this tested?", raising coverage, or judging whether a green suite protects anything. Not for deciding whether the code itself is correct — that is debugging.
---

# Test Design

Weak test design looks like: mirror the happy path, assert the code did what it does, mock everything so it runs fast, call it covered. Strong test design asks of every test: "what realistic mistake would make this fail?" A test no plausible mistake can fail is ballast.

## What to test (priority order)

1. **The bug you just fixed** — a regression test that fails on the pre-fix code. Write it FIRST, run it, paste the failing assertion, then fix. If you fixed first, revert the fix (`git stash` or comment it out), run the test, confirm red, restore. A "regression test" that was never seen red proves nothing.
2. **The contract, at its boundaries** — for each input: empty/zero/null, one, many, max, just-past-max, wrong type/shape, duplicate, unicode/whitespace where strings. Write it as a table: input → expected. Boundaries are where implementations disagree with intentions.
3. **The failure paths** — what the code does when its dependency errors, times out, returns malformed data. Untested error handling is usually broken error handling.
4. **The invariant** — a property that must hold across all inputs (sorted output stays sorted, money sums preserved, scrubbed text contains no digits). One property test or loop-over-cases beats five example tests.

## Test behavior, not implementation

Assert on observable outcomes (return values, emitted events, state visible to callers, rendered output) — not on internals (which private method was called, call order, intermediate structure). Implementation-coupled tests break on every refactor while catching no bugs, training everyone to update tests reflexively — which is how real regressions slip through.

Heuristic: could someone rewrite the function body correctly and keep your test green? They should be able to.

## Mock discipline

- Mock at the boundary you don't own (network, clock, randomness, filesystem) — not your own logic. Mocking your own modules tests the mocks.
- **The mock-echo trap**: a test that stubs `getX` to return `42` and then asserts the result contains `42` tests nothing but the stub. Every mocked test needs real logic under test between stub and assertion.
- Fix time and randomness explicitly (injected clock/seed) — tests that pass "most of the time" are worse than no tests.
- Keep mock shapes honest: when the real dependency's response shape changes, grep for its mocks — a green suite against a stale mock is a false green.

## Structural rules

- One behavior per test; the name states the expectation ("rejects expired proposal") not the method ("test handleProposal 2").
- Arrange–act–assert, visible in the test body. Shared setup helpers are fine; shared *assertions* hidden in helpers obscure what's protected.
- Assert a specific value. `not.toThrow()`, `toBeDefined()`, `is not None`, or a snapshot nobody read are near-zero-information assertions.
- Tests must not depend on each other or on execution order; each builds its own state and cleans up (or uses fresh fixtures).
- Deterministic first: no real network, no real sleeps (use fake timers), no shared global state across files.

## Before reporting

1. **Confirm the runner collected them**: the reported test count rose by the number you added. A misnamed file or unregistered module produces a green run that ran nothing.
2. **Prove one can fail**: for each new group, break the code under test deliberately (flip a comparison, return a constant), rerun, see red, revert — even when no bug is being fixed.
3. **Report the gap**: name each test and the mistake it catches, and list the paths you consciously left untested. "Added tests" without this is not a coverage claim.

## Calibrate quantity

A tiny pure function needs 1–3 boundary cases, not twelve. A gnarly state machine or money-handling path deserves the full table, failure paths, and an invariant. Match the project's existing test idioms and runner conventions — a beautifully designed test in the wrong framework style is a maintenance burden.
