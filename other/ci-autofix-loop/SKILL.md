---
name: ci-autofix-loop
description: >
  End-to-end CI fixer loop for the current git branch/PR (GitHub Actions + Buildkite).
  Use when asked to “fix CI”, “make checks green”, or “address failing checks”, and
  the workflow should: (1) discover failing checks via `gh pr checks`, (2) diagnose
  failures via provider logs (Buildkite log tooling/API or `gh run view --log-failed`),
  (3) apply minimal code fixes, (4) run `code-simplifier` + `code-review`, (5) commit
  + push, and (6) iterate until remaining failures are unfixable via code change.
---

# CI Autofix Loop

Use this workflow to diagnose and fix CI failures on the current PR or pushed
branch. Work one failure at a time, validate the smallest relevant change, and
repeat until checks pass or the remaining failures need action outside the code.

## Before you start

- Work in a git repository with a PR, or a branch pushed to a remote.
- Confirm `gh` is authenticated for this repository.
- If the PR has Buildkite checks, confirm Buildkite access through
  `BUILDKITE_TOKEN`.

Identify the PR and base branch with:

```sh
gh pr view --json number,baseRefName,headRefName,url
```

If there is no PR, use the current branch and its upstream tracking ref:

```sh
git status -sb
git rev-parse --abbrev-ref --symbolic-full-name @{u}
```

The upstream command may have no result when tracking is not configured.

## Find and classify failing checks

Get the check list:

```sh
gh pr checks --json name,state,link,description
```

If a check has no URL, inspect the rollup:

```sh
gh pr view --json statusCheckRollup
```

Classify each failure by its link or purpose:

- **Buildkite:** the link uses `buildkite.com`, often with a `buildkite/<pipeline>`
  context.
- **GitHub Actions:** the link uses `github.com/actions`.
- **Manual or external gate:** review requirements, organization policy, or another
  check that code changes cannot satisfy.

Resolve actionable failures individually. For each one, inspect its logs, identify
the failing command and relevant code, then make the smallest useful fix.

## Diagnose Buildkite failures

Normalize the check link to the base build URL:

```text
https://buildkite.com/<org>/<pipeline>/builds/<num>
```

Use the local log helper when available. First check for
`.codex/skills/buildkite-fetch-logs/scripts/get_buildkite_logs.py` in the repo. If
it is absent, search the workspace or `CODEX_HOME`. Use the helper to download
failed logs to a temporary directory and inspect the failing jobs. If the helper
is unavailable, inspect job state and logs through the Buildkite API with
`BUILDKITE_TOKEN`.

Treat a stale-branch message such as “Your PR is too stale” or “must include commit
<sha>” as a base-branch sync issue. Fetch and rebase onto the PR base, resolve any
conflicts, then update the branch with lease protection:

```sh
git fetch <remote> <baseBranch>
git rebase <remote>/<baseBranch>
git push --force-with-lease
```

For other failures, map the log error to the relevant code, apply the smallest fix,
and run the exact test command named in the log when feasible.

## Diagnose GitHub Actions failures

Read the run or job ID from the check URL. Run URLs contain
`/actions/runs/<run_id>`; job URLs also contain `/job/<job_id>`. Fetch failed logs
for the narrowest available scope:

```sh
gh run view <run_id> --log-failed
gh run view <run_id> --job <job_id> --log-failed
```

Use the job-level command when the URL provides a job ID. Find the referenced files
or commands, then run the smallest local equivalent, such as the formatter,
typecheck, or unit test. Make the minimal fix and let the push-triggered workflow
rerun validate it.

If a failure is flaky or infrastructure-only, has no deterministic local
reproduction, or has no actionable logs, classify it as unfixable by code. Stop
with a summary and links to the relevant checks.

## Review, commit, and push

Before committing, run `code-simplifier` on the current diff. Keep behavior
unchanged and remove unrelated refactoring. Then run `code-review` against the PR
base or upstream branch, and address any blockers.

Create one focused commit per logical CI fix; squash related changes when they form
one coherent fix. Push the PR branch. If history was rebased or rewritten, use
`git push --force-with-lease`, never plain `--force`.

## Repeat and stop

After each push, check the PR again with:

```sh
gh pr checks
```

Continue while a failure provides actionable code-level evidence. Stop when all CI
checks are green, or when every remaining item requires a review, external policy,
or infrastructure action that code cannot address. If two or three iterations
produce no new signal, stop and report the blocker with concrete links.

## Guardrails

- Keep Buildkite and GitHub credentials secret: never print or persist tokens.
- Remove temporary log directories after inspecting them.
- Keep every fix minimal and reviewable; avoid unrelated refactoring.
