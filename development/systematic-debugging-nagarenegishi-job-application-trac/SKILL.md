---
name: systematic-debugging
description: >
  Apply whenever the task is diagnosing a bug, a failing test, or unexpected
  behavior — even if the user only says "fix it". Core rule: never fix what
  has not been reproduced. Not required for feature work, or when the user
  has already stated the cause and only wants the change made.
---

# Systematic Debugging

Never "fix" something that has not been reproduced. Work the steps below in order; do not skip ahead to a fix, however obvious the cause looks.

## 1. Reproduce first

State the reproduction:

- The exact action that triggers the bug (command, request, input, click path).
- What happens, versus what should happen.

Then run the reproduction and confirm the failure yourself. If the environment does not allow running it, say so and ask the user for the failing output — never proceed on an assumed failure mode.

If the bug cannot be reproduced, stop. Report what was tried and what extra information would make it reproducible.

## 2. Isolate

Narrow down where the failure lives before deciding why it happens:

- Change one variable at a time: one input, one config value, one commit, one layer.
- Cut the search space in half where possible: does the bad value already exist at the API boundary? In the database? In the request? Use `git bisect` for regressions; shrink a failing input to the smallest that still fails.
- State what has been ruled out as you go, so nothing gets re-tested.

## 3. Hypothesize with evidence

Every hypothesis needs an observation that could falsify it, gathered before the fix:

- State the hypothesis: "X fails because Y."
- Name the check that would disprove it: a log line, a debugger value, a targeted test, a smaller reproduction.
- Run the check. If the observation contradicts the hypothesis, discard it and say so; do not stretch the hypothesis to fit.

Reading code and concluding "this must be it" is not evidence — the check must observe the running system.

## 4. Fix and confirm

- Make the smallest change that addresses the confirmed cause. Do not refactor, clean up, or fix unrelated issues in the same pass; note them for later.
- Confirm the fix against the original reproduction from step 1, not only by passing tests.
- Run the project's test suite to check for regressions, and add a test that captures the reproduction.

## Reporting

At each step, state which one you are on and what was observed. If a fix attempt fails, report the failure and return to step 3 with the new observation; do not stack a second guess on top of the first.
