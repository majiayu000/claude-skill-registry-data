---
name: tdd
description: Apply the incremental red-green-refactor method when implementing behavior test-first. Use when building a behavior slice test-first or deciding how to make code testable. Check selection and failure diagnosis belong to verify-change.
---

# Test-Driven Development

Use this method inside the active implementation workflow. It does not redefine
scope, choose the project's verification gates or close acceptance. Python test
syntax and fixtures come from python-testing; frontend tests follow the existing
Vitest and Playwright conventions.

## Philosophy

**Core principle**: Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe _what_ the system does, not _how_ it does it. A good test reads like a specification - "tenant owner can invite a member" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Bad tests** are coupled to implementation. They mock internal collaborators, test private methods, or inspect unrelated private implementation state. The warning sign: your test breaks when you refactor, but behavior hasn't changed. If you rename an internal function and tests fail, those tests were testing implementation, not behavior.

Repository integration tests may query PostgreSQL directly to assert persistence, constraints and rollback. This exception does not justify private implementation assertions in use-case or UI tests.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Anti-Pattern: Horizontal Slices

Avoid writing all tests first and then all implementation. This "horizontal slicing" treats RED as "write all tests" and GREEN as "write all code", and it produces weak tests:

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

Match test names and interface vocabulary to the domain language already used by the affected module, and respect ADRs in `docs/content/docs/equipo/adr/` for the area you're touching.

Reuse the active OpenSpec change and already agreed interface/behaviors. Identify observable criteria, the first vertical test and any difficult testability seam (use codebase-design when useful). Ask only for critical missing decisions. Do not repeat approval, create another spec or impose TDD on mechanical/docs-only work. Prioritize the affected contract and important errors rather than every imagined edge case.

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

Refactor only from GREEN: a failing test hides whether the refactor preserved behavior.

## Checklist Per Cycle

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```
