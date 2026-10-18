---
name: tdd
description: Test-drive behavior changes with a red-green-refactor loop through public interfaces. Use when the user explicitly requests TDD, test-first development, RED/GREEN evidence, or behavior design remains unresolved.
---

# Test-Driven Development

## Hard Law

**No production code before RED.** For behavior-changing work, write a failing test through a public interface before editing production code.

This applies to features, bugfixes, risky refactors, and any production-code edit that changes observable behavior.

Allowed escapes:

- docs-only changes
- formatting-only changes
- generated-code-only changes
- config-only changes where no runtime behavior is asserted
- scaffold/bookkeeping-only changes
- truly non-testable work with an explicit `reason_not_testable`

`reason_not_testable` cannot cover forgotten RED.

If production code was written first:

1. Stop advancing the slice.
2. Write the RED test that proves the actual intended public result.
3. Run it and record real failure evidence.
4. Patch production code only enough to make that test pass.
5. Record the task as `tdd_status: recovered`.

If the current code already passes the new test, do not fake RED. Isolate the pre-fix state or revert enough of the slice to observe the failure. If true RED cannot be reconstructed, record the deviation explicitly; do not call the task normally RED/GREEN compliant.

**Core principle**: Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

For test selection and assertions, use [high-signal-tests.md](high-signal-tests.md): keep tests only when they prove durable product or capability behavior through an owned public seam.

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe _what_ the system does, not _how_ it does it. A good test reads like a specification - "user can checkout with valid cart" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Low-signal tests** spend maintenance without protecting owned behavior. Cull existence and registration checks, assertions already satisfied by typechecking, simulated third-party behavior or provider-shape assumptions, shape/contract checks standing in for a feature, low-value UI wiring, and regressions whose only value is blocking reversion. Keep the owned behavior and culling rules co-located in [high-signal-tests.md](high-signal-tests.md).

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

### 1. Planning

Before writing any code:

- [ ] Decide whether the work is behavior-changing and therefore `tdd_status: required`
- [ ] Confirm with user what interface changes are needed
- [ ] Confirm with user which behaviors to test (prioritize)
- [ ] Use `$codebase-design` to identify deep modules, seams, adapters, and test surfaces
- [ ] Design interfaces for testability through the public seam
- [ ] List the behaviors to test (not implementation steps)
- [ ] Get user approval on the plan
- [ ] Record `red_command`, `expected_red_failure`, and `green_command` in the plan before implementation starts

Ask: "What should the public interface look like? Which behaviors are most important to test?"

**You can't test everything.** Confirm with the user exactly which behaviors matter most. Focus testing effort on critical paths and complex logic, not every possible edge case.

### 2. Tracer Bullet

Write ONE test that confirms ONE thing about the system:

```
RED:   Write test for first behavior → test fails
GREEN: Write minimal code to pass → test passes
```

This is your tracer bullet - proves the path works end-to-end.

### 3. Incremental Loop

For each remaining behavior:

```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

Rules:

- One test at a time
- Run and read RED before production code
- Only enough code to pass current test
- Don't anticipate future tests
- Keep tests focused on observable behavior
- Record `red_evidence` and `green_evidence` before claiming completion

### 4. Refactor

After all tests pass, look for [refactor candidates](refactoring.md):

- [ ] Extract duplication
- [ ] Deepen modules (move complexity behind simple interfaces)
- [ ] Apply SOLID principles where natural
- [ ] Consider what new code reveals about existing code
- [ ] Run tests after each refactor step

**Never refactor while RED.** Get to GREEN first.

## Checklist Per Cycle

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Assertions preserve the product/capability invariant
[ ] Test proves behavior owned by this system; typechecking or a third party's suite cannot provide the same evidence
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```
