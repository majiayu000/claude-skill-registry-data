---
name: fix
description: Run git-test precommit checks and fix failures without committing, or fix the errors described in a provided build log. Use when asked to fix build, test, lint, typecheck, or precommit failures.
---

# Fix

Run precommit and fix failures. Leave the fixes uncommitted.

## Existing error context

If the user provides error context (a build log path, a pasted error, or a description), don't run precommit at all. For a log file, read the last 200 lines with ANSI codes stripped. Fix the errors and stop; the caller handles verification.

## Run precommit

Otherwise run, with a timeout of at least 10 minutes:

```bash
git test run HEAD --retest --verbose --verbose
```

This runs even on battery power. The `build:precommit` battery gate doesn't apply because invoking this skill is an explicit request to fix the build.

If `git test` is not configured for this repository, say so and suggest the `build:test-setup` skill.

## Fix failures

Fix the failures and rerun. With fixes in the working tree, `git test run HEAD` refuses the dirty tree, so rerun without a commit argument: `git test run --retest --verbose --verbose` tests the working copy (uncached). Repeat until it exits 0.

Don't commit the fixes or create fixup commits. Callers such as `build:test-branch` run the plugin's `scripts/test-fix`, which stages the working tree and runs `git commit --fixup HEAD` itself.

## Report

Start the final message with one of:

- "✅ Precommit checks passed"
- "✅ Precommit checks passed (after fixing [brief description])"
- "✅ Fixed errors from provided context ([brief description])"
