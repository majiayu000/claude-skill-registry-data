---
name: hotfix
description: Emergency production fix that branches from the latest release tag, applies a minimal fix, ships with expedited review, and backports to main.
disable-model-invocation: true
argument-hint: "/hotfix | /hotfix <description>"
allowed-tools: "Read, Grep, Glob, Edit, Write, Bash, AskUserQuestion"
sensitive: true
---

## Overview

Expedited workflow for production emergencies. Prioritizes speed and minimal change over thoroughness. Every step is designed to get a safe fix deployed as fast as possible.

## When to Use

- A released version is broken in production and the fix cannot wait for the next release from main.
- The root cause is known, or the failing code path is narrow enough to find within 30 minutes.
- For an unclear root cause, run `/investigate` first and return here with the hypothesis it confirmed.
- For a fix that can ride the next regular release, use the normal branch and `/ship` flow.

## Arguments

- No arguments: interactive mode. Ask what is broken in production.
- `<description>`: start the hotfix for the described issue.

## Process

### Step 1: Find the release baseline

Identify the latest release tag:

```
git describe --tags --abbrev=0
```

If no tags exist, use the current state of the main branch as the baseline.

### Step 2: Create the hotfix branch

```
git checkout -b hotfix/<description> <tag>
```

Use a short, descriptive branch name: `hotfix/null-pointer-checkout`, `hotfix/rate-limit-bypass`.

### Step 3: Identify the minimal fix

Read only the files directly related to the bug. Do not read surrounding code for context unless strictly necessary. Do not refactor anything.

The fix must be the smallest possible change that resolves the production issue. If two approaches exist and one touches fewer lines, choose that one.

### Step 4: Reproduce the bug

Write a test that demonstrates the failure. This test must:

- Fail on the current hotfix branch before the fix
- Pass after the fix is applied
- Be fast to run in isolation

If reproduction requires infrastructure that is not available locally, document the reproduction steps and skip to the fix.

### Step 5: Apply the fix

Implement the minimal change. Rules for hotfix code:

- No refactoring
- No renaming
- No style changes
- No dependency updates unless the dependency is the root cause
- No "while I'm here" improvements

### Step 6: Run critical tests

Run the test files that cover the affected code first, for the fastest signal:

```
<test-runner> <affected-test-files>
```

Then run the full local gate per [`../../rules/git-workflow.md`](../../rules/git-workflow.md) before committing, in order: format check, lint, type check, full test suite, build. Urgency shortens the review, never the gate; CI runs the same gate again after the push.

### Step 7: Commit

```
fix(scope): <description>

Hotfix for v<version>. <Brief explanation of the root cause>.
```

### Step 8: Push and create PR

Push the hotfix branch. Create a PR targeting the release branch. If no release branch exists, target main.

Mark the PR as urgent in the title: `[HOTFIX] fix(scope): <description>`.

### Step 9: Backport to main

After the hotfix is merged to the release branch:

```
git checkout main
git pull origin main
git cherry-pick <hotfix-commit-hash>
```

Run tests on main to verify the cherry-pick applies cleanly. If conflicts exist, resolve them and verify.

### Step 10: Tag the patch release

Tag the merged fix on the release branch, never `HEAD`. After Step 9 the checkout is `main`, whose tip is the cherry-pick and carries none of the release branch's history.

```
git fetch origin <release-branch>
git tag -a v<major>.<minor>.<patch+1> -m "v<major>.<minor>.<patch+1>" origin/<release-branch>
git push origin v<major>.<minor>.<patch+1>
```

When no release branch exists and the PR targeted `main`, tag that PR's merge commit by its SHA instead of `origin/<release-branch>`.

## Rules

- Minimal change only. The hotfix branch exists to fix one thing and nothing else.
- No scope creep on the hotfix branch. Another issue noticed while fixing gets its own change on main, in the same session.
- Speed is the priority. Skip steps that do not contribute to getting the fix deployed safely.
- Backport must happen the same day. A fix that lives only on the release branch will be lost on the next release from main.
- Never skip the reproduction test. A hotfix without a test is a hotfix that can regress silently.
- If the fix is not obvious within 30 minutes, escalate. Call in another engineer. A wrong hotfix is worse than a slow hotfix.

## Common Rationalizations

- "The fix is obvious, the reproduction test only slows us down": a hotfix without a failing test can regress silently. Write the test from Step 4 first, or document the reproduction steps when the infrastructure is not available locally.
- "A cleaner refactor would remove the whole class of bug": the hotfix branch carries the smallest change that resolves the production issue. Pick the approach that touches fewer lines.
- "The full suite takes too long, so skip tests": run the affected test files first for speed, then the full local gate of format, lint, type check, full suite, and build before the commit.
- "The backport can happen with the next release": the next release is cut from main, so a fix that lives only on the release branch ships the bug again. Cherry-pick to main the same day.
- "One more hour and I will have it": past 30 minutes without an obvious fix, bring in another engineer. A wrong hotfix costs more than a slow one.

## Red Flags

- Stop and bring in another engineer when 30 minutes have passed and the fix is still not obvious.
- Stop and trim the diff when it contains a rename, a style change, or a dependency bump that is not the root cause.
- Stop and write the reproduction test when the fix is applied and no test has failed on the unfixed branch.
- Stop and rebranch from the tag when the hotfix branch was cut from main while a release tag exists.
- Stop and resolve before tagging when the cherry-pick onto main conflicts or the tests on main fail.

## Verification

- The hotfix branch starts at the tag `git describe --tags --abbrev=0` returned, or at main when the repository has no tags.
- A test fails on the branch without the fix and passes with it, or the reproduction steps are written down because the infrastructure was not available locally.
- The diff holds only the fix and its test.
- Format check, lint, type check, the full test suite, and the build each exit 0 locally before the commit, and the PR title starts with `[HOTFIX]` and targets the release branch, or main when no release branch exists.
- The fix commit is cherry-picked onto main and the tests on main pass.
- The patch tag `v<major>.<minor>.<patch+1>` exists on the remote.

## Related skills

- `/investigate` -- When the root cause is unclear and structured debugging is needed before the fix.
- `/ship commit` -- Commit the hotfix.
- `/incident` -- Document the incident after the fix is deployed.
- `/review` -- Expedited review of the hotfix PR.
