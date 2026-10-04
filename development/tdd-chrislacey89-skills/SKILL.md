---
name: tdd
description: "Invoked helper skill for strict red-green-refactor implementation, usually delegated from /execute or bug-fix work shaped by /triage-issue. Use when backend behavior or behavior-heavy frontend logic should be built test-first through public interfaces. Not for shaping, decomposition, vague implementation tasks, or primarily visual frontend work."
sources:
  primary:
    - "TDD By Example — Kent Beck"
  secondary:
    - "Unit Testing — Vladimir Khorikov"
    - "A Philosophy of Software Design — John Ousterhout"
    - "Refactoring — Martin Fowler"
    - "Extreme Programming Explained — Kent Beck"
    - "Growing Object-Oriented Software, Guided by Tests — Freeman & Pryce"
    - "Introduction to Software Testing — Ammann & Offutt"
    - "Domain Modeling Made Functional — Scott Wlaschin"
    - "A Survey and Classification of Controlled Natural Languages — Tobias Kuhn (Computational Linguistics 2014)"
---

# Test-Driven Development

## Invocation Position

This is an invoked helper skill, not the normal first stop in the feature pipeline.

Use `/tdd` when backend implementation, bug-fix work, or behavior-heavy frontend logic should proceed through strict red-green-refactor cycles, usually because `/execute` delegated to it or a bug workflow produced a TDD-oriented fix plan.

Frontend examples that fit well here include reducers, state machines, validation flows, accessibility-critical behavior, and reproducible regressions in a user flow. Frontend work that is primarily visual, layout-driven, styling-focused, or about interaction feel should usually stay on the direct implementation path with browser-based verification.

Do not use it to replace shaping or decomposition. If the task is still unclear at the product, contract, or slice level, return to `/write-a-prd`, `/prd-to-issues`, or `/execute` first.

## Philosophy

**Core principle**: Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. Test difficulty is a design signal, not an obstacle to work around — when a test requires complex mock setup to reach domain logic, the production code has fused decisions with infrastructure. Refactor the production code, not the test scaffolding.

False positives (tests that fail on safe refactors) trigger a destructive sequence: developers investigate, find no real bug, stop trusting the suite, start ignoring failures, and a real regression slips through unnoticed. Coupling tests to implementation details is not a minor style issue — it is a primary mechanism by which test suites lose their value.

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe _what_ the system does, not _how_ it does it. A good test reads like a specification - "user can checkout with valid cart" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Bad tests** are coupled to implementation. They mock internal collaborators, test private methods, or verify through external means (like querying a database directly instead of using the interface). The warning sign: your test breaks when you refactor, but behavior hasn't changed. If you rename an internal function and tests fail, those tests were testing implementation, not behavior.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Anti-Pattern: Horizontal Slices

**DO NOT write all tests first, then all implementation.** This is "horizontal slicing" - treating RED as "write all tests" and GREEN as "write all code."

This produces **crap tests**:

- Tests written in bulk test _imagined_ behavior, not _actual_ behavior
- You end up testing the _shape_ of things (data structures, function signatures) rather than user-facing behavior
- Tests become insensitive to real changes - they pass when behavior breaks, fail when behavior is fine
- You outrun your headlights, committing to test structure before understanding the implementation

**Correct approach**: Vertical slices via tracer bullets. One test → one implementation → repeat. Each test responds to what you learned from the previous cycle. Because you just wrote the code, you know exactly what behavior matters and how to verify it.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
  ...
```

## Workflow

!`mkdir -p .claude && touch .claude/.tdd-active && echo "TDD marker created — enforcement hook active"`

### 1. Planning

Before writing any code:

- [ ] Confirm with user what interface changes are needed
- [ ] Confirm with user which behaviors to test (prioritize)
- [ ] Identify opportunities for [deep modules](deep-modules.md) (small interface, deep implementation)
- [ ] Classify code under test using the [code classification quadrant](code-classification.md): domain model → unit test, controller → integration test, trivial → skip, overcomplicated → refactor first
- [ ] Design interfaces for [testability](interface-design.md), including which preconditions belong in the *type* rather than in a runtime check — [interface-design.md](interface-design.md) § *Make an illegal input unconstructable, not merely detectable*
- [ ] List the behaviors to test (not implementation steps)
- [ ] Partition the input domain into characteristics and blocks (see below)
- [ ] Get user approval on the plan

Ask: "What should the public interface look like? Which behaviors are most important to test?"

**You can't test everything.** Confirm with the user exactly which behaviors matter most. Focus testing effort on critical paths and complex logic, not every possible edge case.

**Partitioning the input domain.** Name the input's **characteristics** — its independent properties — and split each into **blocks** that are complete (every value lands in one) and disjoint (no value lands in two). Plan one test per block. Prefer many characteristics with few blocks over few with many, and when categories overlap, decompose them into independent booleans plus an explicit constraint rather than patching the categories.

An acceptance criterion already written in EARS form (`When`/`While`/`If … then`, from `/prd-to-issues`) arrives pre-partitioned: each keyword clause names a characteristic — a compound criterion names several, not one — and the `shall` clause is the behavior the oracle checks, a worked example lifted from the spec ([tests.md § The Oracle](tests.md)). Mirror the clause in the test name so the criterion and the test that proves it stay findable from each other.

This produces the list, not the order. Step 3 still writes one test at a time, one block per cycle — enumerating blocks up front is not the horizontal slicing forbidden above; writing them all as tests up front is. [tests.md § Cover Both Failure Directions](tests.md) is this applied to a classifier; an `If … then` criterion is that guard stated at requirement time.

### 2. Tracer Bullet

Write ONE test that confirms ONE thing about the system:

```
RED:   Write test for first behavior → test fails
GREEN: Write minimal code to pass → test passes
```

This is your tracer bullet - proves the path works end-to-end.

Choose a first test that exercises the full vertical path. Prefer one that forces you to create the module, wire the interface, and return a result — even if the result is trivial. The purpose is to resolve _where does this belong?_ before confronting correctness.

### 3. Incremental Loop

For each remaining behavior:

```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

Rules:

- One test at a time
- Only enough code to pass current test
- Don't anticipate future tests
- Keep tests focused on observable behavior
- If getting to green requires more than one conceptual change, back out. Write a simpler test that isolates the prerequisite behavior. Get that green first, then return to the original test. A red bar lasting more than a few minutes is the signal to decompose.

### 4. Refactor

After all tests pass, look for [refactor candidates](refactoring.md):

- [ ] Extract duplication
- [ ] Deepen modules (move complexity behind simple interfaces)
- [ ] Apply SOLID principles where natural
- [ ] Consider what new code reveals about existing code
- [ ] Run tests after each refactor step
- [ ] **Comment the code, not the incident.** Reread the comments this cycle added and move any sentence that explains history rather than the code in front of you. `/execute` Step 3 carries the rule and names where that content lands.
- [ ] **Consolidate a restated claim.** A *prose contract* often states one claim at several *operative sites* at once. That is information leakage with nothing to break when a site is missed, so an additive edit leaves the superseded statement live beside the new one. Census the artifact, then extract the claim to one interpolated constant. [references/restated-claims.md](references/restated-claims.md) defines both terms and carries the census move, the limit of the literal-count assertion, and the fallback when interpolation is unavailable.
- [ ] **[TypeScript projects, when implementing a library-provided callback]** If the refactor produced a local wrapper type for the callback's return (e.g. `AdjacentStepOverrides` for a Mastra `prepareStep` return), anchor the return to the library's declared shape using `satisfies LibraryReturnType` on the object expression, or return a fresh object literal, or derive the local type via `ReturnType<typeof libraryCallback>` / `Parameters<…>`. Do **not** return a typed local variable. TypeScript's excess-property check does not run on returns of typed values, so any field not declared by the library's signature is silently dropped at runtime — build passes, tests pass, the library never sees the field. This is the failure mode `/research` Phase 1.25 and `/pre-merge`'s Runtime Initialization & Production-Runtime Parity dimension backstop, but `satisfies` at refactor time closes the gap at compile time. Cite: ts-essentials Rule 31, "Use `satisfies` for type validation without losing inference precision."

**Never refactor while RED.** Get to GREEN first. One exception, and it is a narrow one: a type-first migration deliberately breaks the *build*, which is not a red bar — see [refactoring.md](refactoring.md) § *A broken build is not a red bar*.

### 5. Harden with Assertions

After refactoring, consider where production assertions would catch future infections closer to their source. Assertions shorten the distance between a defect and the failure it causes — without them, corrupted state propagates silently until it surfaces in unrelated code.

- [ ] **Preconditions** on functions receiving external or untrusted input — fail fast on invalid state rather than propagating it
- [ ] **Postconditions** on functions with complex transformations — verify output invariants hold
- [ ] **Invariant checkers** for non-trivial data structures — a `isValid()` or `sane()` method that checks structural properties through the public interface
- [ ] **Keep debugging assertions** — if you added assertions during debugging to narrow the problem, keep them as permanent production guards. Removing them after the fix discards the detector along with the defect.

Not every cycle needs this step. Apply it when the code handles complex state, crosses trust boundaries, or was the site of a bug fix.

## Timing-coupled primitives are test couplings

Any test that could reach code calling `sleep`, `delay`, `retry`, `timeout`, `interval`, or any other scheduled/debounced/throttled primitive has a hidden coupling to real wall-clock time. This is how tests that pass in milliseconds suddenly jump to multi-second runtime — or worse, start timing out — the moment a retry or backoff is added.

Two rules:

1. **Every time-based primitive is a first-class configurable policy.** Pass the delay, schedule, or timeout as a parameter or config value; never hardcode it. Tests pass zero-duration or no-retry policies; production passes real ones. This applies to `Effect.sleep` / `Schedule` / `Effect.retry` in Effect projects, `setTimeout` / `setInterval` in vanilla Node, RxJS `delay` / `timer` operators, any retry-wrapped fetch client, and any worker queue with a polling interval.

2. **If a test jumps from sub-second to multi-second runtime after adding a retry or sleep, the fix is never "bump `testTimeout`."** The fix is "inject the primitive so tests can disable it." `testTimeout` bumps mask the coupling; injection removes it. Only bump if you have an affirmative reason — e.g. the test is genuinely exercising real-time behavior and cannot use a virtual clock.

**Audit signal:** before you decide a slow test is legitimate, grep the touched code for `Effect\.sleep|Effect\.delay|Schedule\.|setTimeout|setInterval` (or the equivalent in your stack). If any match is in a code path the test can reach and the primitive isn't injected, the coupling is the bug — not the timeout.

## Mocked external seams hide production-runtime behavior

Mocking a type you don't own — a platform API (workerd crypto, edge-runtime globals), the filesystem, a deploy/copy step — makes the test pass in a runtime more permissive than production, or against an artifact layout production won't have. The test is green and blind at the same time. Per GOOS's "only mock types you own," wrap the external type in a thin adapter you *do* own and integration-test that adapter against the real dependency; don't mock the boundary itself. The parity gap a mocked owned-seam leaves is caught downstream at `/execute` Step 4 **Tier 2.7 (Production-Runtime Parity)** — but the root fix is the owned adapter here, not the gate there.

## Checklist Per Cycle

```
[ ] Test describes behavior, not implementation
[ ] Test name claims no constraint the assertion cannot falsify
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Expected values come from an independent source, not the code's own formula
[ ] Code is minimal for this test
[ ] No speculative features added
```

The first two rows are two different name failures, deliberately adjacent. *Describes behavior, not implementation* is the WHAT-vs-HOW axis: a name describing the implementation. *Claims no constraint the assertion cannot falsify* is the name-vs-assertion axis, and it fires only on names that assert a **relationship** — a bound, an ordering, a rejection, a deadline. `"user can checkout with valid cart"` names an outcome and is out of scope for it. A name can pass either row and fail the other. That second row's method is not restated here — see [tests.md](tests.md) § *A test name is a claim the assertion must be able to falsify*.

## Handoff

- **Expected input:** a concrete backend behavior, frontend interaction behavior, or fix path that is already scoped well enough to implement
- **Produces:** tested code increments built through red-green-refactor
- **Usually invoked by:** `/execute`, or by bug-fix work prepared through `/triage-issue`
- **Returns control to:** the calling implementation flow, usually `/execute`, for final verification and handoff to `/pre-merge`
- **On exit:** `/execute` Step 6 removes `.claude/.tdd-active` after commit
