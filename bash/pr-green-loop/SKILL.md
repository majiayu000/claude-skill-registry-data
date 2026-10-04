---
name: pr-green-loop
description: >-
  After pushing code or creating a PR, automatically wait for CI checks to
  complete, fix failures, address Bugbot findings, and re-push in a loop
  until the PR is green. Use when the user pushes to a PR, creates a PR,
  or asks to get a PR to green.
---

# PR Green Loop

Drive a PR to green by iterating: push → wait for checks → fix failures → address Bugbot → re-push → repeat.

## When to activate

- User creates a PR (after `pr-create` finishes)
- User pushes new commits to an existing PR
- User asks to "get the PR green", "fix CI", or "fix all PR issues"

## Prerequisites

- `gh` CLI installed and authenticated
- Current branch has a remote-tracking PR (or one was just created)

## Workflow

### Step 1: Ensure code is pushed and PR exists

1. Run `git status` to check for uncommitted changes.
2. Push the branch: `git push -u origin HEAD`.
3. If no PR exists yet, delegate to the `pr-create` skill and wait for user approval before continuing.
4. Capture the PR number:

```bash
gh pr view --json number -q .number
```

### Step 2: Wait for CI checks to complete

Poll until all check suites finish (no `pending` / `queued` / `in_progress` remaining):

```bash
gh pr checks <PR_NUMBER> --watch --fail-fast
```

If `--watch` is unavailable or hangs, fall back to a manual polling loop:

```bash
while true; do
  STATUS=$(gh pr checks <PR_NUMBER> --json name,state --jq '[.[].state] | unique | join(",")')
  echo "Check states: $STATUS"
  # Break when no "PENDING", "QUEUED", or "IN_PROGRESS" remain
  echo "$STATUS" | grep -qiE 'pending|queued|in_progress' || break
  sleep 30
done
```

Report the final status summary before proceeding.

### Step 3: Fix CI failures

If any check failed:

1. Delegate to the `ci-fix` skill (fetch logs, classify, auto-fix or diagnose).
2. For auto-fixable issues (lint, format, lock file, pre-commit): apply fixes, stage, and commit.
3. For test failures: read the failing test, understand the root cause, fix the code (not just the test), and commit.
4. Use conventional commits: `fix(<scope>): <description>`.

### Step 4: Address Bugbot findings

Bugbot posts review comments on the PR. Fetch and fix them:

1. Fetch unresolved review conversations (delegate to `github-pull-request-handling` skill's script):

```bash
SKILL_BASE_DIR/scripts/pr-conversations.sh <PR_NUMBER>
```

2. For each unresolved Bugbot comment:
   - Read the full thread to understand the finding.
   - Fix the issue in the codebase.
   - Commit with a conventional message: `fix(<scope>): address bugbot — <short description>`.
   - Reply to the comment with the commit hash (see `github-pull-request-handling` for reply format).

3. For non-Bugbot review comments: skip them — those are for the author to triage manually.

### Step 5: Push and loop

1. Push all new fix commits: `git push`.
2. Go back to **Step 2** and wait for the new CI run.
3. Repeat until:
   - All checks pass **and** no new unresolved Bugbot comments exist.
   - Or a **maximum of 3 iterations** is reached (to avoid infinite loops).

If the loop limit is hit, report the remaining failures and stop.

### Step 6: Report final status

When the PR is green (or the loop limit is reached), output a summary:

```
## PR Green Loop — Result

**PR**: #<number>
**Status**: ✅ All green / ⚠ Issues remain after 3 iterations
**Iterations**: <count>

**Fixes applied**:
- <commit hash>: <description>
- <commit hash>: <description>

**Remaining issues** (if any):
- <description of unresolved failure or comment>
```

## Delegation to other skills

| Concern | Delegate to |
|---------|-------------|
| Creating the PR | `pr-create` |
| Diagnosing CI failures | `ci-fix` |
| Fetching/replying to review comments | `github-pull-request-handling` |
| Commit message format | `git-conventional-commits` |
| Python lint/format fixes | `ruff` |
| Lock file sync | `uv` |

## Rules

- Never force-push; always use regular `git push`.
- Never `git add .` — stage only files related to the fix.
- Stop and ask the user if a test failure root cause is ambiguous.
- Only auto-fix Bugbot comments; leave human reviewer comments for the author.
- Cap iterations at 3 to prevent runaway loops.
