---
name: "tdd"
description: "Test-driven development: what a good test is, where its seam goes, the anti-patterns, and the rules of the red-green loop. Also decides when a test is not worth writing. Use when building features or fixing bugs test-first, when the user mentions red-green-refactor or asks for a failing test or a regression test, or when deciding whether a bug has a cheap enough test path to be worth one."
---

# Test-Driven Development

TDD is the red → green loop. This skill is what makes that loop produce tests
worth keeping: what a good test is, where tests go, the anti-patterns, the
rules, and the cases where the right move is not to write one.

When exploring the codebase, read `CONTEXT.md` if it exists so test names and
interface vocabulary match the project's domain language, and respect ADRs in
the area you are touching.

## Decide whether a test earns its place

Do this first, before writing anything. Most of the time the answer is yes and
this takes one sentence. When it is no, saying so explicitly is the whole
point.

**Write the test** when there is a clear, cheap path to one: an existing test
file for that codepath, a pure function, a reachable seam, a reproduction you
can already state in a sentence.

**Skip it** when the available test would need broad harness setup, brittle
mocks, slow end-to-end infrastructure, production-only state, vague
reproduction steps, or large unrelated fixture churn.

**Prefer no test over a bad test.** A bad test is one that mostly tests mocks,
encodes current implementation details, depends on timing or unrelated global
state, needs expensive infrastructure for a small fix, or would be deleted
immediately after proving the fix.

Skipping is not silent. Say why a failing test is impractical, then name the
closest executable check you will use instead: a targeted script, a manual
reproduction command, browser automation, a snapshot comparison, a log
assertion, a focused integration check. The **diagnose** skill's Phase 1 is the
same discipline applied to bugs, and its ten ways to build a feedback loop are
worth reading when no obvious test path exists.

## What a good test is

Tests verify behavior through public interfaces, not implementation details.
Code can change entirely; tests shouldn't. A good test reads like a
specification: "user can checkout with valid cart" tells you exactly what
capability exists, and it survives refactors because it doesn't care about
internal structure.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking
guidelines.

## Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe
behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing any test, write down the
seams under test and confirm them with the user. No test is written at an
unconfirmed seam. You can't test everything, so agreeing the seams up front is
how testing effort lands on the critical paths and complex logic instead of
every edge case.

Ask: "What's the public interface, and which seams should we test?"

When the shape of that interface is itself in question (how deep the module is,
where the seam belongs, what the interface should expose), call the Skill tool
with "codebase-design" for the vocabulary. It is the shared source of the
module, interface, depth, seam, adapter, leverage and locality terms, and it is
a reference to consult, not a session to run.

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead: one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **Confirm it fails for the right reason.** A test that passes before the fix, or fails on an unrelated error, is testing something other than what you think. Correct the test or the reproduction before touching the implementation.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** It belongs to the review stage (see the **review** skill), not the red → green implementation cycle.

## Guardrails

- Do not change tests merely to match a wrong implementation.
- Do not weaken existing assertions unless the expected behavior has genuinely changed and the reason is clear.
- Keep a regression test focused on the bug; avoid broad fixture churn or unrelated coverage expansion.
- If the bug is flaky, make the test deterministic where possible and say which signal is being locked down.
- If the bug exposes a broader class of failures, land the focused regression path first, then consider sibling coverage.

## Report the evidence, not the outcome

"Added tests, they pass" is not a result. Name:

- The failing-before test or executable check, and the failure it actually produced.
- The passing-after run, and any nearby validation (adjacent tests, type check, lint).
- If failing-before evidence could not be demonstrated, why, and the closest regression check used instead.

This is the **prove-it-works** principle (`principles/prove-it-works.md`)
applied to tests: the claim is only as good as the run behind it.
