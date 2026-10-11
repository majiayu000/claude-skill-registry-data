---
name: fix-ci
description: Diagnose a failing CI run from the log — reproduce locally, minimal fix, verify.
trigger: when the user pastes a CI failure or says the build/pipeline is red
---
## When to use
The user shows a failing CI log or says the pipeline/build broke.

## How
1. Read the log bottom-up — the first *error* matters; everything after is
   usually cascade. Quote the exact failing line back.
2. Classify: test failure / lint-format / type error / dependency or install /
   flaky-infra (timeout, network, runner died).
3. Reproduce locally with the same command CI ran (from the workflow file —
   `read_file .github/workflows/*.yml`); same Python/node version if pinned.
4. Fix the cause, not the symptom: a failing assertion means the code or the
   test is wrong — decide which from the requirement, then change that one.
5. Re-run the exact failing command locally until green; mention any check
   you could NOT run locally.
6. Flaky-infra failures: say so explicitly, suggest retry + a guard (timeout
   bump, retry-on-503), don't "fix" unrelated code.

## Avoid
- Deleting/skipping a test to make CI green — that's a last resort the user
  must explicitly approve.
- Pinning random versions until it passes, with no explanation.
- Fixing three unrelated things in one go.

## Done well
The failing line is named, the cause is explained in one sentence, the fix is
minimal, and the previously-failing command passes locally.
