---
name: testing-conventions
description: "Generic rules for when a test gets written, what earns one, and that the environment is part of the contract. Use before writing or changing a test, fixing a bug, or reviewing coverage."
---

# Testing conventions

When a test is written, what earns one, and the environment as part of the contract.

## When to use

- Writing a new test or changing an existing one.
- Fixing a bug, before writing the fix.
- Reviewing test coverage in a pull request.

## Rules

### When a test is written

- New code gets tests.
- A bug fix starts with the test that reproduces the bug.
- The test commit comes first and fails on the current code.
- The fix commit follows. Two commits, never one.
- Test first for new features is a recommendation, not a rule.
- Apply it to logic with a clear contract. Infrastructure code and skill scripts are left out.

### What gets a test

- Every branch with a decision.
- Every failure path.
- Every boundary: empty, zero, one, maximum, duplicate, out of order.
- Every value read from the environment.
- Not a getter, glue code or generated code.

### A refusal names the mechanism

- A test asserting a write was refused names the mechanism that refused it: an error code, a
  constraint name, or a message that carries one of those, not a generic phrase.
- A non nil error alone keeps passing when the check under test is removed and an unrelated one
  refuses in its place.
- Database: name the SQLSTATE or the constraint name carried on the error, not only that a query
  failed.

### Revert proof per mechanism

- A fix that adds more than one mechanism able to catch the same case gets each one reverted
  alone, with the test watched failing.
- A test that passes with its own mechanism removed does not cover that mechanism.

### An invisible row still needs proof it exists

- A test that an unprivileged caller cannot see a row also asserts, through a privileged path,
  that the row is actually there.
- An empty result is otherwise indistinguishable from nothing having been written.

### A policy test carries no predicate of its own

- A test of a database row level policy issues a query with no predicate repeating the policy's
  own condition.
- A query that repeats the policy's condition in its own filter still passes once the policy is
  removed.

### The environment is part of the contract

- Code that reads identity, home directory, configuration files, tokens, PATH or locale gets a
  test with those empty.
- Or pointed at an empty directory.
- Run once is enough. The point is that the empty case exists, not repeated variants.

### Form

- Table driven where the stack supports it.
- The test name states the behaviour, not the expectation.
- Fixtures look like real data.
- No network.
- Deterministic: no wall clock, no shared state, fixed seeds where randomness is involved.
- Independent of execution order.
- No sleep to wait for timing. Wait on the condition instead.

### A failing test

- Never deleted, skipped or weakened to make a run pass.
- The cause gets fixed, or the failure gets reported.
- A flaky test gets fixed or reported, never retried until it passes.

### Rewriting a check, a matcher or a gate

- Collect the inputs the old version rejected before writing the new one.
- Run both versions over every one of them. Keep every rejection the old version made.
- A deliberate change of decision on one of them is named with its reason, in the pull request.
- The comparison goes into the pull request as a table: input, old decision, new decision.
- Every probe input becomes a test, so the next rewrite starts from them instead of from a blank
  slate.

## Guardrails

- A bug fix has two commits: the failing test, then the fix.
- New behaviour covered: branches, failure paths, boundaries, environment values.
- No test added to a getter, glue code or generated code only to raise a count.
- A refusal assertion names the error code, the constraint name, or a message carrying one of
  those, never a non nil check or a generic message alone.
- An invisibility test proves the row exists through a privileged path.
- A database policy test's query carries no predicate repeating the policy's own condition.
- An environment input has an empty or redirected case.
- Tests stay deterministic, independent, network free, sleep free.
- No failing test removed, skipped or weakened. A flaky test fixed or reported.
- A rewritten check, matcher or gate carries its before/after comparison table in the pull
  request, with every input the old version rejected still rejected or its change named.

## References

- `test` for detecting the runner and running the suite.
- `go-tests` and `python-conventions` for the stack's test form.
- `fix-ci` for a failure caused by an environment difference.
