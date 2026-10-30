---
name: heal-ci
description: Katara heals a sick pipeline one wound at a time. Use for fix-ci, /fix-ci, "CI is red", "fix the failing checks", "get CI green", or a branch or PR whose checks fail. Finds the failing checks, reads the logs or external check links for the first actionable error, applies the smallest safe fix, and repeats until the checks are green.
---

# Katara heals CI

A healer facing many wounds treats the one that bleeds first, checks the patient, and only then moves on. A red pipeline is the same. Find the first real error, close it with the least force, and look again.

## Trigger

A branch or PR has failing CI and needs a fast, iterative path to green checks.

## Steps

1. **Resolve the PR and read the checks.** Find the active PR for the branch, then run `gh pr checks --json name,bucket,state,workflow,link`.
2. **Find the first actionable error.** Inspect each failed job. Read the GitHub Actions logs when they exist (`gh run view <run-id> --log-failed`). Otherwise follow the check's link to find the failing command or service. Read until you reach the first error that names a cause, not the cascade after it.
3. **Reproduce it locally when you can.** Run the failing command on your machine. A fix you watched pass beats one you pushed and hoped for.
4. **Apply the smallest safe fix.** Fix the cause the log names. When the cause is a real defect in the code, switch to `healing-water` for it.
5. **Push and check again.** Push, rerun `gh pr checks`, and repeat from step 2 until every check is green.

## Rules

- Fix one actionable failure at a time.
- Prefer minimal, low-risk changes before broader refactors.
- Keep `gh pr checks` as the source of truth for the PR's overall CI state.
- Never skip, disable, or weaken a check or a test to turn it green. Never retry a flaky job and call it fixed. A flaky check is a bug with a cause.
- A failure the branch did not cause (a broken base branch, an outage in an external service) is reported, not patched over in this branch.

## Reply

- The primary failing job and its root error, quoted from the log.
- The fixes applied, in iteration order.
- The current CI status and the next action.
