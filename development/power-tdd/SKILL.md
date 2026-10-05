---
name: power-tdd
description: Use when implementing any feature or fixing any bug, before writing implementation code
---

# Test First

## The iron law

**No production code without a failing test first.**

Not "usually". Not "unless it's small". The rule has no exception clause, because every
exception anyone has proposed was a case where the test was skipped and the bug shipped.

## The cycle

### RED — write one failing test

One test, for one behavior, with a name that says what the behavior is. Use real code, not
mocks of the thing you are testing. A mock of your own function tests that you can configure a
mock.

Before you write it, name the production change that would make this test fail. If you cannot
name it, you do not yet know what you are testing.

### Verify RED — mandatory

Run it. Watch it fail. Then check **why** it failed:

- It must fail, not error. An import error is not a red test.
- It must fail because the behavior is missing, not because of a typo, a missing fixture, or a
  wrong path.
- If it **passes**, you are testing behavior that already exists. Stop and find the real gap.

Skipping this step is where the whole cycle stops working, because a test that never failed
proves nothing when it passes.

### GREEN — the minimum

Write the least code that makes it pass. No speculative parameters, no "we'll need this
later", no configuration for a case nobody asked for.

### Verify GREEN

Run it and watch it pass. Then run the surrounding suite: your change must not have broken
anything. Read the output — not the exit code alone.

### REFACTOR — only on green

Improve names and structure with the tests passing. Run them again after.

## If you wrote code first

Delete it. Do not keep it in a scratch file, do not adapt it, do not look at it while writing
the test. Code you can see is code the test will be shaped to fit, which produces a test that
passes for the wrong reason.

## Rationalizations

| Thought | Reality |
|---|---|
| "It's a one-line change" | One-line changes ship bugs. That is why they are worth a test. |
| "I'll add the test after" | The test after is shaped by the code. It tests what you built, not what was needed. |
| "It's just a config value" | If a wrong value breaks things, a test can catch a wrong value. |
| "There's no framework here" | Then the first task is the framework, and it is a real task. |
| "I already know it works" | Then the test passes immediately and costs a minute. Write it. |
| "The test would be trivial" | Trivial tests catch typos, which are the most common defect. |
| "This is exploratory" | Exploration is a spike, and its code is throwaway. Label it and delete it. |

## Regression tests

A bugfix needs a test that fails before the fix and passes after. Prove it both ways: write the
test, watch it fail, apply the fix, watch it pass, **revert the fix and watch it fail again**,
restore. A regression test you never saw fail is a regression test you cannot trust.
