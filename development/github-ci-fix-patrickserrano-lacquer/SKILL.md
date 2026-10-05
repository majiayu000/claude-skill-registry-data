---
name: github-ci-fix
description: Fix failing PR checks, debug GitHub Actions, or account for CI follow-up rounds and wait for verification.
---

# GitHub CI Fix

## Overview

Systematic workflow for debugging failing PR checks using `gh` CLI. Identifies GitHub Actions failures with logs, scopes external checks (Buildkite, etc.) as out-of-scope, then uses existing plan workflow for fixes.

## Prerequisites

```bash
gh auth status  # Required scopes: repo, workflow
```

**STOP if unauthenticated:** `gh auth login --scopes repo,workflow`

## Quick Reference

| Task | Command |
|------|---------|
| Find current PR | `gh pr view --json number,url` |
| Inspect PR status (snapshot only) | `gh pr checks <pr>` |
| Wait for CI | `lacquer wait pr <N>` |
| View run details | `gh run view <run-id>` |
| Get failed logs | `gh run view <run-id> --log-failed` |
| Full run log | `gh run view <run-id> --log` |
| Recent runs for this check | `gh run list --workflow <name> --branch <branch> --json conclusion,headSha,createdAt -L 20` |
| Rerun without code changes (flakiness probe) | `gh run rerun <run-id> --failed` |

## Workflow

### 1. Verify Auth → 2. Find PR → 3. Inspect

```bash
gh auth status  # If fails: ask user to authenticate
gh pr view --json number,url  # Or use user-provided PR number
gh pr checks <pr>  # Shows check name, status, details URL
```

### 4. Scope: GitHub Actions vs External

**GitHub Actions** (`detailsUrl` has `/actions/runs/`): Pull logs, extract snippets, fix
**External CI** (Buildkite, CircleCI): Report URL only, request user to share logs

**STOP:** Do not attempt external CI log access.

### 4.5. Flaky or Real? Scope the Breaking Commit

Before treating a failure as a bug to fix, rule out flakiness — a fix for a
flaky test is a wasted diagnosis, and a "fix" that just happens to make a
flaky test pass on the next run isn't actually verified.

**Flakiness probe:**
```bash
gh run rerun <run-id> --failed   # same commit, no code change
lacquer wait pr <N>  # Wait for the rerun, then inspect its outcome
```
If it now passes with nothing changed, it's flaky — report that (test name,
run URL, "passed on rerun with no changes") rather than diagnosing a bug that
isn't there. Don't silently move on either: a flaky check is still worth
flagging to the user, since it can mask a real failure next time.

**Corroborate with history**, especially if a rerun isn't practical (slow or
expensive job):
```bash
gh run list --workflow <name> --branch <branch> --json conclusion,headSha,createdAt -L 20
```
A mixed pass/fail pattern across unchanged code on recent commits is the same
flakiness signal without needing a live rerun.

**If it's consistently failing (not flaky), scope the breaking commit** so
the fix targets the actual regression instead of the whole diff since last
green:
```bash
# Find the last passing SHA and first failing SHA from the run history above,
# then list the suspect commits between them:
git log --oneline <last-good-sha>..<first-failing-sha>
```
For a failure that's expensive to reproduce per-commit, `git bisect` against
the specific failing check (run it locally, or trigger the same CI job per
bisect step) narrows this further than reading the commit list alone.

### 5. Pull GitHub Actions Logs

```bash
# Extract run ID from detailsUrl: .../runs/<run-id>
gh run view <run-id> --log-failed  # Preferred: failed jobs only
gh run view <run-id> --log         # Alternative: full log
```

Extract 20-50 lines before failure with error messages and stack traces.

### 6. Report → 7. Plan → 8. Implement → 9. Verify

**Report:** GitHub Actions (name, URL, log snippet, diagnosis, flaky-or-real verdict, breaking commit if scoped) + External (name, URL, "share logs")

**Plan:** **REQUIRED** - Use `EnterPlanMode`. Never skip for "simple fixes".

**Implement:** After approval: code changes → tests → commit → `lacquer ci-round begin <N> --reason "<failed check and what changed>"` → push the granted SHA.
For review-requested changes use `--review "<what was asked, and by whom>"`
instead of `--reason`, even on green CI. Review rounds spend the same budget.
A push without `begin` spends an `unrecorded` round when next observed by
`begin` or `status`, except a GitHub-created update-branch merge: commit API
committer email `noreply@github.com`, exactly two parents, and one parent equal to
the previous known head. It is recorded as a neutral `update` (known on later
observations), spending no round and never resetting the budget. Local merges
and other unknown heads are still charged. Only a human-authorized
`lacquer ci-round reset <N> --reason "<why>"` refills the budget.
Exit 10 means stop and surface the ACTION, never reset yourself to bypass it.

**Verify:** `lacquer wait pr <N>` then `gh run view <run-id> --log-failed` if a check failed.
Run the wait in the background and read its exit code when it finishes; it sleeps
between polls. Use `--repo owner/name` when outside the PR's checkout.

| Exit | Outcome | Action |
|------|---------|--------|
| `0` | passed | Every check is terminal and none failed; read the skipped-check warnings, since skipped checks did not run. |
| `1` | failed | Inspect the named failures and pull their logs. |
| `2` | timed out | Checks are still running; the result is unknown, not a pass. |
| `3` | no checks | Never green: nothing tested this PR. Investigate missing checks. |
| `4` | wait failed | The wait itself failed; fix the reported error before claiming a CI result. |

`gh pr checks --watch` exits 0 even when checks fail; do not use its exit code
as proof of green CI. A `gh pr checks` snapshot is for inspection only.

Older binaries without `lacquer wait`: inspect `gh pr view <N> --json statusCheckRollup` until a nonempty list is terminal, explicitly checking each result; empty conclusions (`""`), pending statuses, and an empty list are never green.

## Common Patterns

```bash
# Multiple failing jobs
gh run view <run-id> --json jobs --jq '.jobs[] | select(.conclusion=="failure")'

# Log too large: use --log-failed (skips successful steps)
gh run view <run-id> --log-failed

# Re-run after fix (avoids rebuilding successful jobs)
gh run rerun <run-id> --failed
```

## Boundaries

**In scope:** GitHub Actions failures, log extraction, flaky-vs-real triage, breaking-commit scoping, scoping external checks, plan creation
**Out of scope:** External CI log access, fixes without plan approval, bypassing auth

## Red Flags - STOP

- Trying to access external CI logs via workarounds
- Creating fixes without viewing actual logs
- Proceeding without `gh` authentication
- Skipping plan creation for "quick fixes"
- Making assumptions about failures without reading logs

**If you see these, STOP and follow the workflow.**

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "I'll fix it without seeing logs" | STOP. Pull logs first. |
| "It failed, so it must be a real bug" | STOP. Rerun first — rule out flakiness before diagnosing. |
| "Buildkite is just like GitHub Actions" | STOP. External checks are out of scope. |
| "Simple fix, no need for plan" | STOP. Use plan workflow. |
| "I'll parse the web UI" | STOP. Use `gh` CLI. |
| "Auth is optional" | STOP. Required for all operations. |

## Impact

**Before:** Changes without seeing errors, confusion on check scope, inline plans, fixes chasing flaky tests
**After:** Auth verification, systematic logs, flaky-vs-real triage, breaking-commit scoping, proper boundaries, plan workflow integration

## Project conventions

Read [references/project-rules.md](references/project-rules.md) for the relevant
section when handling this task. Read only what applies; examples do not
authorize releases, deployments or changes outside the user's scope.
Always-loaded safety rules still apply.

- CI Hygiene
- CI round budget
