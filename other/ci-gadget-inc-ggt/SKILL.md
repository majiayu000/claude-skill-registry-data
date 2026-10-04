---
name: ci
description: Diagnoses and fixes CI failures and re-runs GitHub Actions jobs. Use when CI is failing, tests break in CI, lint errors block merging, a build fails, or jobs need re-running.
---

# CI

Inspect, fix, and re-run GitHub Actions CI on the current branch.

## Operations

### Fix CI Failures

Identify failed jobs in the latest CI run, analyze logs, categorize failures, and fix each one.
See [fix.md](fix.md) for detailed instructions.

### Re-run CI Jobs

Re-run failed or all jobs in the latest CI run.
See [rerun.md](rerun.md) for detailed instructions.

## Routing

- "fix ci" / "ci is broken" / "tests failing in CI" / "lint failing" / "build broken" → **Fix**
- "rerun ci" / "retry ci" / "re-run the build" / "run ci again" → **Re-run**
- "fix and push" → **Fix**, then use git skill to commit and push
