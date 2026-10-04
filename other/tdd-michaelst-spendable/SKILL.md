---
name: tdd
description: Test-driven development with a red-green-clean loop, running mix credo on the whole project at the end of every vertical slice so standards violations are fixed in the slice that introduced them instead of piling into a refactor at the end. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests, or asks for test-first development.
---

# Test-Driven Development

## Philosophy

**Core principle**: Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe _what_ the system does, not _how_ it does it. A good test reads like a specification - "a transaction's unallocated remainder lands in Spendable" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Bad tests** are coupled to implementation. They mock internal collaborators, test private functions, or verify through external means (like calling an action module directly instead of the context facade). The warning sign: your test breaks when you refactor, but behavior hasn't changed.

Two rules this codebase enforces that are easy to get wrong:

- **Test through the facade**, never the action module. `Budgets.create_budget/2`, not `Spendable.Budgets.Actions.CreateBudget.create_budget/2`.
- **There are no factories.** Every record a test needs is created through the context function that owns it.

See [tests.md](../../../docs/tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

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

## Test Economy: Extend Before You Add

Vertical slicing means one behavior per cycle — it does **not** mean one new `test` block per behavior. Before writing a new test, check whether an existing test already establishes the exact setup you need.

**Extend an existing test when** the new behavior shares the same arrange/act and differs only by one assertion or one input value. Add the assertion, or add a case to the existing parametrized list, instead of cloning a whole setup that does mostly the same thing.

**Write a new test when** the behavior needs its own arrange/act, or when folding it into an existing test would obscure which behavior broke on failure.

The goal is to **avoid duplicate scaffolding, not to minimize test count.** A distinct behavior crammed into an unrelated test to save a line is worse than a focused new test — it hurts failure diagnosis and readability. But five near-identical tests that differ by one value should be one test over a list of cases.

## Workflow

### 1. Planning

When exploring the codebase, use the vocabulary the context owns — [CONTEXT-MAP.md](../../../CONTEXT-MAP.md) and the `CONTEXT.md` in the context you are touching — so test names and interface vocabulary match the project's language.

Before writing any code:

- [ ] Confirm with user what interface changes are needed
- [ ] Confirm with user which behaviors to test (prioritize)
- [ ] Identify opportunities for [deep modules](deep-modules.md) (small interface, deep implementation)
- [ ] List the behaviors to test (not implementation steps)

Ask: "What should the public interface look like? Which behaviors are most important to test?"

**Test everything.** Focus testing effort on critical paths and complex logic, then add smaller tests to make sure edge cases are covered. Every action gets the same three at minimum: happy path, domain error, and a scope belonging to another user returning `{:error, :not_authorized}` against the *real* record id.

### 2. Tracer Bullet

Write ONE test that confirms ONE thing about the system:

```
RED:   Write test for first behavior → test fails
GREEN: Write minimal code to pass → test passes
CLEAN: mise exec -- mix credo → passes
```

This is your tracer bullet - proves the path works end-to-end.

### 3. Incremental Loop

For each remaining behavior:

```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
CLEAN: mise exec -- mix credo → passes
```

Rules:

- One behavior at a time
- Before adding a new test, prefer extending an existing test with matching setup (see [Test Economy](#test-economy-extend-before-you-add))
- Only enough code to pass current test
- Don't anticipate future tests
- Keep tests focused on observable behavior

**Build the setup to exercise the branch, not to pass.** Setup whose defaults make the happy path automatic proves nothing about the path you care about, and the test still goes green — so the bug ships. Before you accept a GREEN, ask what your setup made *impossible*: a transaction whose allocations already sum to its full amount never exercises the Spendable remainder; a budget with no allocations never reaches the balance arithmetic; a Plaid fixture with no pending transactions never reaches `replace_pending`; a scope that owns everything never proves the ownership pin does anything.

When a test passes on the first run, treat it as suspect until you have seen it fail for the right reason.

### 3a. Credo on every slice

**Run `mise exec -- mix credo` at the end of every cycle, once the slice is GREEN.** Not at the end of the feature.

Credo is cheap, and the whole point of running it per slice is that a standards violation caught in the slice that introduced it is a two-line fix. The same violation found after twelve slices is a refactor across everything built on top of it, done at the exact moment you least want to be restructuring code. The custom `SpendableCredo` checks in [credo/](../../../credo) police this codebase's own conventions, so they fire on exactly the things a generic linter would miss.

- **Run it on the whole project**, never with a file filter or path argument. It is fast, and a slice that cleans up its own file while breaking another has not passed.
- **Only fix while GREEN.** Credo runs after the test passes, never while RED — the same rule as refactoring.
- **Fix the underlying issue.** Never edit `credo/.credo.exs` to disable a rule, never add `# credo:disable-for-next-line` or `# credo:disable-for-this-file`, and never delete flagged code purely to silence it.
- **Re-run the test after a credo fix.** A cleanup that breaks the slice you just proved is not done.

This is the same gate [complete-issue](../complete-issue/SKILL.md) runs before commit. Running it per slice means that gate should be green the first time rather than opening a refactor.

### 4. Refactor

After all tests pass, look for [refactor candidates](refactoring.md). Credo has already been satisfied on every slice, so this pass is about the design judgment credo can't see:

- [ ] Extract duplication
- [ ] Ensure code follows the [standards](../../../docs/standards.md)
- [ ] Deepen modules (move complexity behind simple interfaces)
- [ ] Apply SOLID principles where natural
- [ ] Consider what new code reveals about existing code
- [ ] Run tests after each refactor step

**Never refactor while RED.** Get to GREEN first.

## Checklist Per Cycle

```
[ ] Test describes behavior, not implementation
[ ] Test goes through the context facade
[ ] Test creates its data through context functions, not a factory
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
[ ] mix credo passes on the whole project
```
