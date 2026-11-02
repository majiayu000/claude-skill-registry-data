---
name: writing-tests
description: |-
  Use when writing or reviewing tests in any language, or diagnosing a suite that is slow, brittle, or hard to read. Triggers: "write tests", "how should I test this", "what kind of test", "test is flaky/fragile", "should I mock this", "test is hard to read". Python-specific practices (mocking, pytest, async) are included in `references/python-testing.md`.
---

# Writing Tests

## When to Use

- Writing or reviewing tests in any language or framework.
- Choosing what kind of test to write (unit, integration, E2E).
- Diagnosing a suite that is slow, brittle, flaky, or hard to maintain.
- Reviewing test structure, naming, or test double usage.
- Unsure what test coverage a change needs.

## When NOT to use

- Auditing Python code for house-style violations outside tests: see the `python` skill.

## Invocation Notice

- Tell the user when this skill is running: `writing-tests`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## Quick Reference

- Test observable behavior — outputs, state transitions, emitted effects — not implementation internals.
- One behavior per test.
  Split when you can't write a single coherent name covering all assertions.
- Write the regression test before the fix; a test you never saw fail proves nothing.
- Keep tests order-independent and deterministic.
  Inject clocks and randomness; never sleep.
- Prefer DAMP over DRY in test code: readable duplication beats abstraction that hides the story.
- Mock and stub at collaboration boundaries only.
  Prefer real collaborators for domain logic.

## Test Structure (AAA)

Every test follows the same three-phase structure — called Arrange/Act/Assert, Given/When/Then, or Setup/Exercise/Verify depending on tradition.
All three describe identical phases:

| Phase | AAA     | Given/When/Then | Meszaros |
| ----- | ------- | --------------- | -------- |
| 1     | Arrange | Given           | Setup    |
| 2     | Act     | When            | Exercise |
| 3     | Assert  | Then            | Verify   |
| 4     | —       | —               | Teardown |

Separate phases with a blank line — that is the minimum required structure.
Section-label comments (`# Arrange` / `# Act` / `# Assert`, or `# Given` / `# When` / `# Then`) are acceptable when the team finds them helpful; they are not required.
The examples in this document include labels as a teaching aid.

```text
// Arrange
cart = new_cart()
cart.add(item("widget", price=9.99), quantity=3)

// Act
total = cart.total()

// Assert
assert total == 29.97
```

**Teardown** is required when a test acquires real resources (files, connections).
Prefer automatic cleanup via framework hooks over manual teardown in the test body.

**Test organization** (file layout, grouping by class vs. flat functions, `describe` blocks) follows your testing framework's conventions.
The AAA structure applies at the individual test function level, regardless of how tests are grouped.

**Violations that signal a structural problem:**

- Interleaved Act/Assert cycles — the test covers multiple behaviors; split it.
- No Assert — "testing that nothing crashes" is not testing.
- Giant Arrange that buries the Act — extract a named Creation Method.

See `references/test-structure.md` for AAA in depth, DAMP vs. DRY, and GWT vs. AAA.

## Naming

Test names are the first thing a reader sees on a failure.
They must communicate the scenario and the expected outcome without entering the test body.
The name is the test's specification.

Three-part form: `<Behavior>_<Condition>_<ExpectedOutcome>`

Casing and separators follow your language convention — the goal (communicating scenario and expected outcome) is universal; the style is not.

```text
// snake_case (Python, Ruby)
withdraw_money__insufficient_funds__raises_error
cart_with_no_items__total_is_zero

// camelCase segments (Java, C#, JS)
withdrawMoney_insufficientFunds_raisesError
cartWithNoItems_totalIsZero
```

Alternative — full behavioral statement (readable as documentation):

```text
should_reject_transfer_when_balance_is_negative
returns_empty_list_for_unknown_category
```

Note: some frameworks require a specific prefix for test discovery (e.g., `test_` in pytest, `Test` in Go).
That prefix is a framework requirement, not a naming-quality choice — it does not substitute for a descriptive name.
A function named `test_withdraw` is as opaque as `testWithdraw`; `test_withdraw__insufficient_funds__raises_error` communicates what the test verifies.

Avoid: numbered suffixes (`test_2`, `test_order_2`), names that state only the entry point without a condition or expected outcome, names that describe input type rather than scenario.

See `references/test-structure.md` for naming conventions in depth.

## Comments

Don't write comments that explain what the test does — the name and structure should.
Write a comment only when:

- A non-obvious business rule drives the assertion and the test name cannot carry the full context.
- A deliberate deviation from convention would otherwise look like a mistake.

A test that requires comments to be understandable has a naming or structure problem.
Fix the test.

## Test Portfolio

Shape the suite toward many fast unit tests, fewer integration tests, and a minimal set of end-to-end tests — the testing pyramid.
Treat the ratios as a sanity check against a slow, expensive, inverted pyramid, not a quota.
Let contract risk and the natural behavioral unit drive the actual mix.

**Match test scope to the natural behavioral unit of the code:**

- Pure function with no collaborators → unit test.
- Component coordinating several well-tested sub-components → integration test at the component boundary.
- Service or module with a defined API → integration test treating the service as the unit, using real or in-process infrastructure.
- User-facing workflow spanning multiple services → E2E test (keep to a minimum; critical paths only).

**Coverage expectations for each change:**

- Happy path and the primary alternative paths.
- Validation failures and error paths.
- Boundary inputs and edge cases.
- A regression test for every bug fixed — write it before the fix.
- Cleanup, cancellation, and resource-release paths when the code touches I/O or long-running work.

**Multiple write-sites:** when the same contract outcome can be produced by more than one code path (canonical path, dedup shortcut, cache hit, idempotency early-return), each path needs its own test.
A test of the canonical path does not prove the shortcut is correct.

```text
// Test the canonical path
result = repo.save(record, mode=CANONICAL)
assert result.id != null

// Also test the shortcut — it may skip validation or use a different write order
result = repo.save(record, mode=DEDUP)
assert result.id != null
assert result.normalized_url == normalize(record.url)
```

**Derived-pair invariants:** when a spec asserts `field_a == f(field_b)` and the two fields are written by different producers, neither field-local tests nor per-producer tests prove the invariant holds after composition.
Write a post-composition test.

```text
// Each producer may be correct in isolation but the pair must be verified together
manifest = merge(resolver_output, fetcher_output)
assert manifest.normalized_url == normalize(manifest.source_url)
```

See `references/test-portfolio.md` for the pyramid vs. trophy vs. honeycomb debate, scope decision questions, property-based testing, and mutation testing.

## Test Doubles

"Mock" is not a synonym for "test double."
Use Meszaros's taxonomy:

| Type      | Definition                     | Use when                                                           |
| --------- | ------------------------------ | ------------------------------------------------------------------ |
| **Dummy** | Passed but never used          | A parameter is required but irrelevant to this test                |
| **Fake**  | Simplified real implementation | In-memory database, fake queue, in-process event bus               |
| **Stub**  | Returns canned values          | Providing indirect inputs: HTTP responses, clocks, config          |
| **Spy**   | Stub that records calls        | Verifying a side-effect occurred; assert post-hoc on the recording |
| **Mock**  | Pre-programmed expectations    | The interaction itself is the behavior under test                  |

**Prefer state verification** (assert on observable outcomes) over behavior verification (assert on call sequences).
Tests that assert call sequences are structure-sensitive: they break when implementation is refactored without changing behavior.

**When to use doubles:** external I/O (network, filesystem, email), non-determinism (clocks, randomness), operations that must not execute in tests (charge a card, send a real notification).
Prefer real collaborators for domain logic — test domain objects with their actual peers rather than stubbing business logic.
A Fake (in-memory implementation) is a test double and is appropriate for external infrastructure; using a `FakeRepo` does not violate this principle.

**Stub at the boundary, not deep inside.**
Replace the dependency at the seam where your module uses it.
Deep mock chains that mirror the internal call graph are a design smell — they indicate I/O has not been properly decoupled from logic.

Common mistake: asserting that a mock was called without asserting on observable output.
Call-count assertions prove the mock was invoked, not that the behavior was correct.

See `references/test-doubles.md` for the full taxonomy with examples, the classical vs. mockist distinction, and common misuse patterns.

## TDD

Red-green-refactor is an ordering discipline: write a failing test, write minimum code to pass, then refactor.
The principles in this skill apply regardless of whether tests are written before or after code.

One rule from TDD that applies universally: when fixing a bug, write the failing test that reproduces it before touching production code.
A test you never saw fail doesn't prove the bug is gone.
For failures that can't be reproduced locally (race conditions, load-dependent), write a characterization test capturing the known behavior and confirm the failure reproduces in CI before patching.

## Intent and Scope

- Infer intended behavior from names, docstrings, type signatures, usage patterns, and existing tests before writing new ones.
  If intent is ambiguous, state assumptions explicitly and ask before encoding behavior in a test — a test locks in whatever it asserts, wrong or right.
- When the task is test-only, do not modify production code.
  If code changes would improve clarity or testability, record them as recommendations and keep implementation out of the test change.

## Common Mistakes

- **Fragile Test** — breaks when unrelated code changes; caused by asserting on internals (call sequences, private state, string representations of objects).
- **Assertion Roulette** — multiple assertions with no identifying messages; when one fails the reader can't tell which.
- **Eager Test** — verifies multiple behaviors in one test; split when the name can't coherently cover all assertions.
- **Mystery Guest** — fixture set up outside the test body (external file, shared database, implicit setup); the reader can't understand cause and effect without finding the external resource.
- **Erratic Test** — non-deterministic; primary causes: shared mutable state that bleeds between tests, ordering dependencies (test B silently relies on test A having run first), timing assertions using `sleep` instead of condition-based waits, unordered collections in equality checks, unseeded randomness, and resource leaks from missing teardown.
  Diagnose ordering issues by running with a randomized seed.
  Fix with per-test setup/teardown hooks, condition-based waits, sorted comparisons, and seeded randomness.
- **Slow Tests** — unit tests touching real databases, networks, or filesystems; replace with fakes or in-process substitutes.
- **Testing the mock** — asserting call counts without asserting on observable output; proves the mock was invoked, not that the behavior was correct.
- **Missing regression test** — fixing a bug without first writing a failing test that reproduces it.

## References

- `references/test-structure.md` — AAA in depth, naming conventions, DAMP vs. DRY, GWT vs. AAA
- `references/test-portfolio.md` — pyramid, trophy, honeycomb, scope decision guide, property-based testing, mutation testing
- `references/test-doubles.md` — full taxonomy with pseudocode, classical vs. mockist school, when to use each type
- `references/python-testing.md` — Python-specific practices: `unittest.mock` discipline, pytest structure, async testing, dependency audits
