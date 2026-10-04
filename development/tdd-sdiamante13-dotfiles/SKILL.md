---
name: tdd
description: Use when implementing a new function, adding a feature, fixing a bug, refactoring with test coverage, or writing a new test. Enforces strict outside-in red-green-refactor TDD with one-failure-per-turn discipline, predict-the-failure-before-every-run checks, hardcode-first minimum changes, triangulation, and property-based testing for large input spaces. Triggers on explicit TDD requests and on any task phrased as "implement", "add", "write a function", "build a feature", or "fix a bug" in a test-capable codebase. Reports red/green validation evidence.
---

# TDD Cycle

Strict outside-in test-driven development. The main session owns the cycle; sub-agents handle individual steps.

STARTER_CHARACTER = 🔴 for a red test, 🌱 for green, 🌀 for refactor, always followed by a space.

## When This Skill Applies

- Writing a new function, method, or module
- Adding a new feature
- Fixing a bug (write the reproducing test first)
- Refactoring code that has test coverage
- Backfilling tests on an existing implementation (also see `/retroactive-test-check`)

## Core Principle

The TDD cycle drives design via a sequence of small, auditable state changes. Every production code change *that carries behavior* traces to a specific failing test. Tests describe behavior (inputs, outputs, side effects), not implementation (method calls, internal state). Behavior-free code is exempt — see "Don't Test Behavior-Free Code" below.

**Predict every run.** Before you run any test, state the exact failure you expect — the message *and* the reason it should fail. Running without a prediction is a code smell: if you can't say what should happen, you don't yet understand the behavior you're driving. A run that fails for a reason other than the one you predicted (a "wrong-reason red" — unrelated compile/import/syntax/setup error) does not count as a valid red; fix the cause and re-predict.

## Don't Test Behavior-Free Code

TDD drives *behavior*. Code that holds no behavior has nothing for a test to drive, and a test against it asserts the language's own semantics, not your design. Do NOT write tests for:

- Trivial getters and setters (plain field reads/writes, no transformation, validation, or side effect)
- Plain data carriers — DTOs, POJOs, records, structs, value objects whose only members are accessors
- Builders, constructors, and factories that only assign fields
- Generated or boilerplate accessors (Lombok, `@Data`, framework-generated code)
- Pass-through delegations that add no logic

These need no failing test and no test backfill. Adding one is the getter/setter anti-pattern: it inflates the suite, couples tests to structure, and breaks on harmless refactors without catching real defects.

**The test arrives when behavior arrives.** The moment an accessor gains logic — a computed value, a conditional, validation, a transformation, a side effect — it is behavior, and the new behavior is driven by a failing test like anything else. Test the behavior, not the field.

If you reach for a test only because "every change needs a test" or to satisfy the TDD gate, and the code under test has no behavior, that is the wrong reason — skip the test and make the edit.

## The Cycle — Main Session Owns It

1. **RED** — Write ONE failing test. **Predict the exact failure (message + reason).** Run it. Confirm it fails for the reason you predicted.
2. **GREEN** — Write the minimum code that addresses the current failure message. **Predict that it now passes.** Run it. Confirm it passes.
3. **REFACTOR** — Clean up while tests stay green. Run tests. Confirm still green.
4. **REPEAT** with the next failing test.

Do NOT delegate an entire RGR loop to a single sub-agent. Individual steps may use task agents ("write the failing test", "write minimum code to pass", "refactor X") — but the main session runs the tests and verifies state between steps.

### Two-step red for new public API

When the surface under test does not exist yet, take the red in two predicted steps:

1. **First red** — the test fails to compile/import because the class, function, method, or route does not exist. Predict that exact failure, run, confirm.
2. **Second red** — add only the missing surface returning an intentionally wrong result, so the test now fails on the *assertion*. Predict the assertion failure (expected vs. got), run, confirm.

Only then move to green. This separates "the thing isn't there" from "the thing is wrong", and each transition is predicted and observed.

## Red-Phase Discipline — One Test Per Turn

### What a good red test looks like

- Asserts on outputs, side effects, return values, emitted events, or externally-observable state — never on internal method calls or private collaborators.
- Fails because the production behavior is absent or wrong. A "cannot find module", "wrong arity", or "not implemented" from a stub is a valid red — that is the compiler/runtime asking you to build the next stub.
- Has a name (or Gherkin phrasing) a non-developer could read and understand as a statement about behavior.
- Has the minimum setup required to force the one behavior under test.

### Forbidden in one red-phase turn

- Writing multiple test cases at once, even if "they go together".
- Writing tests for code that no outer failing test has demanded (speculative coverage).
- Asserting on internal calls, private state, or implementation details.
- Mocking internal collaborators — mock at system boundaries only (external APIs, DB, network).
- Stacking many assertions into one test covering multiple behaviors.

### Triangulation: examples vs. properties

After a green where you hardcoded a literal, you often need a second red to force generalization. Pick deliberately:

**Use example-based tests when…**
- Input space is small, enumerable, bounded (e.g., days of week, fixed enum)
- The examples carry documentary value — each names a meaningfully-distinct case
- Two or three well-chosen inputs pin down the behavior

**Use property-based tests when…**
- Input space is large or unbounded (integers, strings, arbitrary lists/records)
- Behavior is governed by an invariant or algebraic relation
- You catch yourself wanting "a few more" examples "to be thorough" — that urge is the signal
- Roundtrip, idempotence, identity, commutativity, reference-implementation, invariant preservation

### Third-example rule of thumb

If you're about to write a THIRD example-based test against the same function to force the same generalization — STOP and convert to a property test. Beyond three, each example adds cost without confidence; a property covers the whole space.

### Property patterns to reach for

- **Roundtrip** — `decode(encode(x)) == x`
- **Invariant preservation** — operation preserves size/order/membership
- **Idempotence** — `f(f(x)) == f(x)`
- **Algebraic identity** — `f(x, identity) == x`
- **Commutativity / associativity**
- **Reference implementation** — new impl matches known-correct naive impl
- **Metamorphic relation** — known input change produces known output change

For TypeScript projects, prefer `fast-check` for property-based testing.

## Green-Phase Discipline — Minimum Change Per Turn

Each turn addresses ONE failure. Change only what the current failure message requires, then re-run. Let the next failure tell you what to do next.

### Allowed changes by failure category

| Failure | Allowed change this turn |
|---|---|
| Syntax / missing import | Add the import or fix the syntax. Nothing else. |
| Unknown symbol / "not defined" | Declare as empty stub (throws "not implemented" or returns trivially invalid value). Match arity to call site. |
| Wrong arity | Adjust signature to match caller. Do not wire new parameter through body. |
| "Must implement method Y" | Add Y as stub that throws "not implemented". |
| "Not implemented" thrown by stub | Replace throw with simplest expression that could satisfy next check the test makes (usually a literal). |
| `expected X, got <trivial>` | Return the literal X. **Fake it.** Do not write general logic. |
| `expected X, got Y` from real logic | Inspect the logic, make narrowest correction to yield X for this input. Do not re-architect. |
| Unexpected exception | Fix only the line in your own code on the first frame of the stack trace. |
| Expected exception NOT thrown | Add the throw in exactly the single branch the test exercises. |
| External dependency unreachable in unit test | STOP — return to red. Wrong boundary under test, or missing mock at system edge. |
| Fixture / before-hook failure | STOP — return to red. Test-side changes are not a green-phase activity. |

### Forbidden in one green-phase turn

While driving the current failure to green, do NOT:

- Add error handling, logging, or validation the failure did not demand
- Implement branches the failing assertion does not exercise
- Generalize beyond what the current assertion requires
- Add speculative null/empty/boundary handling
- Refactor ("while I'm here" cleanup belongs in refactor phase)
- Fix multiple failing tests in one change — address the first, re-run, then the next
- Touch files unrelated to the current failure
- **Write new tests, edit existing tests, modify fixtures, or change mocks** — green is for production code only

### When the fix is in the test, return to red

If the minimum fix would be in a test file, fixture, or mock — STOP. Green is for production code only. Discard the in-progress production edit, update the test in a red-phase turn, re-run to see the real red, then re-enter green.

### Worked pattern: hardcode first

Test: `expect(sum_of_squares([2, 3])).toBe(13)`

- Turn 1. Failure: "sum_of_squares is not defined" → add empty stub throwing "not implemented"
- Turn 2. Failure: "not implemented" → replace with `return 13` (literal)
- Stop. The general algorithm is NOT written yet — no failing test has demanded it. Generalization comes later, driven by a new red test.

### When in doubt

If you're tempted to write code beyond what the current failure demands — stop, delete it, re-run, let the next failure speak.

## Refactor Phase

- Only with tests green.
- Clean up duplication, improve naming, extract helpers — behavior-preserving only.
- Run full test suite after each refactor. If any test fails, the refactor wasn't behavior-preserving.
- Refactor phase can be delegated to a task agent with a specific, narrow instruction ("extract the validation block into a helper without changing behavior").

## Blocked Test Harness

If a failing test cannot be written because the harness is missing, flaky, unsafe, or blocked by unrelated infrastructure, state why. Create the closest executable characterization or documented verification command instead, then keep the production change as small as possible.

## Plan Structure — TDD Cycles, Not Waterfall

Implementation plans must be iterative RGR cycles, not layer-by-layer construction.

### Wrong

```
Step 1: Define all domain types
Step 2: Define all events
Step 3: Implement all command logic
Step 4: Write unit tests
Step 5: Write acceptance tests
```

This batches implementation before tests and does not drive design from failing tests.

### Right

```
Step 1: Write failing acceptance scenario → run → see fail
Step 2: Identify first compilation/runtime failure
Step 3: Write failing unit test for that specific need
Step 4: Write minimum code to pass the unit test
Step 5: Refactor
Step 6: Repeat 3-5 until acceptance scenario passes
```

Plans describe acceptance scenarios + design decisions + module structure for context. They do NOT prescribe "build X, then Y, then test." The implementation sequence emerges from the TDD cycle itself.

## Retroactive Test Coverage

If you're writing a test that passes on the first run (the behavior is already implemented), you MUST mutation-verify it before trusting it. See the `/retroactive-test-check` skill.

## Common Anti-Patterns

- **One-shot TDD** — writing all tests + full implementation in one step. Not TDD; just "tests exist before commit".
- **Speculative tests** — writing tests for code no failing outer test has demanded.
- **Batched failures** — seeing 3 reds and making one combined change to fix them all. Address the first, re-run, then the next.
- **Running without a prediction** — if you can't say what should fail and why, you don't understand the behavior yet.
- **Wrong-reason red** — accepting a red that failed on an unrelated compile/import/setup error instead of the asserted behavior.
- **Mocking internal collaborators** — if you need to, the design is wrong, not the test.
- **Refactor during green** — moves the goalposts. Refactor is a separate phase with its own run-tests gate.
- **Generalization without a failing test** — the code only exists because triangulation demanded it.
- **Testing behavior-free code** — tests for trivial getters/setters, plain DTOs/POJOs/records, or field-only builders. They assert language semantics, not your design. See "Don't Test Behavior-Free Code".

## Final Report

When the cycle (or batch of cycles) is done, report the validation evidence:

- RED command and the intended failure result (what you predicted and saw).
- Files changed.
- GREEN command and passing result.
- Broader validation command and result, or skipped broader validation with the reason.

## Why

- Prevents speculative code that no failure ever demanded
- Keeps each turn's state change observable, reviewable, revertable
- Preserves the test suite as the design driver instead of agent guesswork
- Surfaces missing tests: code that would only exist by speculation is instead exposed as an untested path the next failing test must ask for
- Makes the red→green transition auditable — every diff traces to a specific predicted failure message
