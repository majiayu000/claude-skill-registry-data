---
name: push-and-pull
description: Katara's push and pull for test discipline. Use for tdd, /tdd, "red green", "write a failing test", "add a regression test", when a bug has an obvious cheap local test target, and when writing, changing, or reviewing tests. Skip a new test when the test path is unclear, expensive, integration-heavy, or not requested. Tests assert observable behavior so they fail when behavior breaks and survive refactors.
---

# Katara's push and pull

Waterbending is a rhythm. Push, then pull. Test-first work is the same rhythm. Push a failing test that names the behavior. Pull the code until it passes. Then let the water settle and clean up.

## When to push a new test

Write the test first when the user asks for TDD, a failing test, or a regression test, or when the bug has a clear, cheap test path. Make the broken behavior executable before you change production code. The goal is a focused regression test that fails before the fix and passes after it.

Do not force a test when it would be impractical. If the available test would need broad harness setup, brittle mocks, slow end-to-end infrastructure, production-only state, vague reproduction steps, or large unrelated fixture churn, skip the new test and use the closest useful check instead (see below).

## The rhythm

1. **Understand the behavior.** Name the intended behavior, the current behavior, the affected path, and the smallest observable reproduction.
2. **Choose the narrowest executable check.** Prefer the closest unit, component, integration, or regression test the codepath already uses. If no practical test path is obvious, do not build one from scratch just to satisfy the rhythm.
3. **Push (red).** Write the smallest test for one behavior a caller can observe, the one that would have caught the bug. It encodes intended behavior, not the current implementation.
4. **Run it before the fix.** Confirm it fails for the intended reason. Quote the failure content, not the assertion line. An exception, an empty result against a literal, and the predicted mismatch all print red, and only the predicted mismatch proves the test measures the bug. An import error or a crash is not red. It is a broken instrument. If the test passes, or fails for an unrelated reason, correct the test or the reproduction before you touch the implementation.
5. **Pull (green).** Make the smallest production change that satisfies the intended behavior and keeps nearby contracts. Rerun the new test, then the whole nearby suite.
6. **Settle (refactor).** Clean the code with the tests green. Run them again after each change.
7. Repeat for the next behavior. Commit at each green when the work spans several behaviors, and land the failing test in a commit before its fix.

## When a failing test is impractical

Use the closest executable regression check instead: a targeted script, a manual reproduction command, browser automation, a snapshot comparison, a log assertion, or a focused integration check.

Prefer no new test over a bad test. A bad test mostly tests mocks, encodes implementation details, depends on timing or unrelated global state, needs expensive infrastructure for a small fix, or would be deleted right after it proved the fix.

## What to test

- **Behavior at the public surface.** Inputs and outputs, side effects a caller sees, errors a caller handles. Not private helpers, call counts, or internal state.
- **The bug's exact trigger.** A regression test reproduces the reported input, not a cleaned-up approximation.
- **The edges that matter.** Empty, one, many, the boundary value, the error path. Skip edges no caller can reach.
- **The real thing when cheap.** Prefer a real database, filesystem, or process in a test container over a mock. Mock only what is slow, flaky, or external.

## Check a test is worth keeping

- Revert the code change. Does the test fail? If not, it tests nothing.
- Rename an internal function. Does the test still pass? If not, it tests the implementation.
- Read the test name alone. Does it say what behavior is promised?

## Rules

- Never change a test merely to match a wrong implementation.
- Never delete or weaken a failing test, or an existing assertion, to get green. Weaken an assertion only when the expected behavior has truly changed and the reason is clear.
- Keep a regression test focused on the bug. Avoid broad fixture churn or unrelated coverage.
- Never assert on log text, timing, or ordering the caller does not depend on.
- A flaky test is a bug. Make it deterministic where you can (shared state, real time, network) and name the signal it locks down, or quarantine it with an issue.
- When the bug exposes a broader class of failures, land the focused regression test first. Consider sibling coverage after.

## Reply

Report the evidence, not only the outcome.

- Name the failing-before test or check and quote the failure it produced, trimmed to the diff.
- Name the passing-after run and any nearby checks you ran.
- If you could not show failing-before evidence, say why and name the closest regression check you used instead.
