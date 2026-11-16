---
name: test-first
description: Use when implementing a feature, fixing a bug or changing behaviour, before writing the implementation. Write one failing test, watch it fail for the right reason, write the least code that passes, then tidy up with the tests green.
license: MIT
metadata:
  bundled-by: Shodh
  sources: obra/superpowers (test-driven-development), affaan-m/ECC (tdd-workflow)
---

# Test first

A test you never saw fail proves nothing: it may pass whatever the code does.
Writing the test first is how you know it can catch the bug.

Second of Shodh's six building skills (plan-before-building → **test-first**
→ debug-systematically → design-polish for UI work → verify-before-done →
fresh-eyes-review). Each step
of an agreed plan names the test that proves it; this skill is how that test
gets written.

## When to use it

Always for new behaviour, bug fixes and refactors that must not change
behaviour. Ask the user before skipping it for throwaway prototypes, generated
code or configuration files. In a Creator session nobody is asked: decide
yourself, and list the choice in `finish_creation`.

## The cycle

### 1. Red: one failing test

- Find the project's test runner first: read the build files (`Cargo.toml`,
  `package.json`, `pyproject.toml`, `go.mod`) and the existing tests, and
  follow their style and location.
- Write **one** test for **one** behaviour, named for what should happen
  ("rejects an empty email", not "test1").
- Test real code. Use a fake only where the real thing is slow, external or
  random, and never assert on the fake itself.
- Before writing it, say which change in the code would make it fail. If you
  cannot, the test is too vague.

### 2. Watch it fail

Run the test with `run_command`. It must **fail**, and fail because the
behaviour is missing, not because of a typo, a missing import or a crash in
the test. A test that passes at once tests something that already works: fix
the test.

Commands ask the user for approval unless the conversation allows them. That
is expected; wait for the answer and never look for a way around it.

### 3. Green: the least code that passes

Write the simplest code that makes the test pass. No options nobody asked for,
no refactor of the code around it, no "while I am here".

Run the test again and see it pass. Then run the **whole** test suite of the
project (or the package you changed), not only your test. Fix anything you
broke now, in the code, at its root cause. A failure you did not cause still goes in
your report, by name.

### Never make a test pass by weakening it

Never weaken an assertion, widen a tolerance, raise a threshold or a timeout,
add a retry, skip, ignore or delete a test (`#[ignore]`, `@pytest.mark.skip`,
`.skip`, `t.Skip`), or update a snapshot or golden file to get green. A failing
existing test means your change or that test is wrong: find out which. If you
believe the test is wrong, show the user the failure and why, and change it
only when they agree.

### 4. Refactor with the tests green

Only after green: remove duplication, improve names, extract a helper. Run the
tests after each change. Behaviour stays the same.

### 5. Repeat

Next behaviour, next failing test.

## If code came before the test

It happens. Write the test, then prove it can fail: undo your change (or comment
out the line that makes it pass), run the test and see it fail, then restore the
change and see it pass. Only code you wrote in this conversation is undone this
way; never discard the user's own work.

## What a good test looks like

| Quality | Good | Bad |
|---|---|---|
| One thing | "rounds totals to cents" | "validates email and domain and spaces" |
| Clear name | Says the behaviour | `test_1`, `it works` |
| Real code | Calls the function under test | Asserts that a mock was called |
| Edge cases | Empty, one, many, too large, wrong type, failure path | Only the happy path |

There is no coverage percentage to hit. Cover the behaviour the change adds or
fixes, its edge cases and its failure paths.

## Signs you are off track

- Code before a test, and no proof the test can fail.
- A test that passed the first time it ran.
- You cannot say why the test failed.
- "I'll add tests later." Later does not come.

## Bug fixes

Every bug fix starts with a test that reproduces the bug and fails. The fix
makes it pass. The test stays, so the bug cannot come back unseen. For finding
the cause, use debug-systematically.

## Sources and credit

Merged and rewritten for Shodh from:
- **obra/superpowers**, skill `test-driven-development`
  (https://github.com/obra/superpowers, commit
  22f0b463e7a5e579904dd6211a520321035526f7), MIT License, Copyright (c) 2025
  Jesse Vincent. See `LICENSE-superpowers.txt`.
- **affaan-m/ECC**, skill `tdd-workflow` (https://github.com/affaan-m/ECC,
  commit d2ef2680594f9a17526a6e1a2e18b3d242c5d17b), MIT License, Copyright (c)
  2026 Affaan Mustafa. See `LICENSE-ECC.txt`.

Where the two disagreed, Shodh chose: no fixed coverage target (ECC's 80%
minimum is dropped; cover the behaviour instead); code written before its test
is proven by undoing it and watching the test fail, rather than deleted
(superpowers' "delete means delete"); no git checkpoint commits. The test
runner detection step and the plan-to-test mapping come from ECC.
