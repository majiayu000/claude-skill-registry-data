---
name: tdd
description: Test-driven development with vertical red-green-refactor cycles and behavior-preserving green-to-green refactor loops. Use when the user requests TDD, test-first feature or bug work, integration tests that drive implementation, or an internal restructure that must preserve observable behavior. Infer the contract from the request and repository evidence; ask only when unresolved material choices would change public or business behavior, data or security meaning, or scope.
---

# Test-Driven Development

## Philosophy

**Core principle**: Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe _what_ the system does, not _how_ it does it. A good test reads like a specification - "user can checkout with valid cart" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Bad tests** are coupled to implementation. They mock internal collaborators, test private methods, or verify through external means (like querying a database directly instead of using the interface). The warning sign: your test breaks when you refactor, but behavior hasn't changed. If you rename an internal function and tests fail, those tests were testing implementation, not behavior.

See [tests.md](tests.md) for examples, [mocking.md](mocking.md) for mocking guidelines, and [saved filter tracer bullet](examples/saved-filter-tracer-bullet.md) for a concise workflow example.

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

### 1. Planning

When exploring the codebase, use the project's domain glossary so that test names and interface vocabulary match the project's language, and respect ADRs in the area you're touching.

Before writing any code:

- [ ] Infer the intended interface and prioritized behavior from the user
      request, existing tests, code, repository rules, and documented contracts
- [ ] Identify opportunities for [deep modules](deep-modules.md) (small interface, deep implementation)
- [ ] Design interfaces for [testability](interface-design.md)
- [ ] List the behaviors to test (not implementation steps)

Proceed with the strongest evidence-backed interpretation. Ask the user only
when an unresolved material choice would change public or business behavior,
data or security meaning, or the authorized scope. State the competing options
and their effects; do not use routine implementation details as approval gates.

**You can't test everything.** Infer priorities from risk and repository
contracts. Focus testing effort on critical paths and complex logic, not every
possible edge case.

### 2. Tracer Bullet

Write ONE test that confirms ONE thing about the system:

```
RED:   Write test for first behavior → test fails
GREEN: Write minimal code to pass → test passes
```

This is your tracer bullet - proves the path works end-to-end.

Use the smallest testable seam that exercises the behavior. A small contract
fixture is appropriate when it is the shortest path to test an API envelope,
configuration interpretation, or display-value versus runtime-value mapping.
Do not build heavyweight scaffolding for a narrow contract, and do not let
boundary cataloguing turn the TDD cycle into an architecture review.

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

### 4. Refactor

After all tests pass, look for [refactor candidates](refactoring.md):

- [ ] Extract duplication
- [ ] Deepen modules (move complexity behind simple interfaces)
- [ ] Apply SOLID principles where natural
- [ ] Consider what new code reveals about existing code
- [ ] Run tests after each refactor step

**Never refactor while RED.** Get to GREEN first.

## Validation Evidence

Use `RED`, `GREEN`, and `REFACTOR` as observed execution states, not intentions:

- report the exact command actually run and the result observed
- call a test RED only after it ran and failed for the expected missing behavior
- call a test GREEN only after it ran and passed
- label checks that were not run as **planned**, **unavailable**, or **inferred**
  and explain why
- never claim GREEN from a plan, code trace, static inspection, or expected
  outcome alone

## Behavior-Preserving Refactor Mode

Use this mode when the requested outcome is a new internal structure with the
same externally observable behavior. Unlike feature work, a safe refactor may
start and remain GREEN; do not manufacture a failing test merely to satisfy the
RED step.

### 1. Freeze The Current Contract

Before moving code:

- run the relevant existing tests and record the baseline
- identify public APIs, return values, exceptions, side effects, persistence,
  events, serialization, and ordering guarantees that must remain stable
- distinguish public import paths from incidental internal imports
- add a characterization test only when material current behavior lacks a
  reliable public test anchor
- if the baseline already fails, record the pre-existing failure and do not
  attribute it to the refactor

### 2. Move One Responsibility Green-To-Green

For each slice:

1. Select one coherent responsibility and its real consumers.
2. Move or extract that responsibility without changing its public behavior.
3. Update callers and imports.
4. Run the narrowest relevant tests.
5. Remove the old implementation or delegation once callers have cut over.
6. Run the same tests again before selecting the next responsibility.

Keep the slice vertical by capability or concept. Do not split all declarations
first and reconnect behavior later.

### 3. Preserve Behavior, Not The Old Shape

- Test through public behavior rather than new module names or private helpers.
- Preserve an old import path only when it is a real public contract or a
  verified consumer requires a transition.
- Do not keep dual implementations, permanent compatibility wrappers, or empty
  facades merely to make the move look safer.
- Do not turn characterization tests into approval of accidental behavior
  without checking whether the repository treats that behavior as a contract.

### 4. Complete The Cutover

The refactor is not complete until:

- one concept has one clear owner
- obsolete code and dead imports are removed
- focused tests remain GREEN
- the full relevant test suite and project quality checks pass
- skipped or unavailable checks are reported

See [refactoring.md](refactoring.md) for the refactor-mode checklist.

## Checklist Per Cycle

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
[ ] Validation is labeled executed or planned; GREEN reflects an observed pass
```
