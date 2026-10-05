---
name: merge-and-monitor
description: |
  Merge a pull request, watch the deployment pipeline it triggers through to completion, and
  verify the result is healthy. Use when the user says "merge and monitor", "merge and watch
  the deploy", "merge it and make sure everything is working fine", "merge and verify", "land
  it", or any variation of merging a PR followed by watching/verifying its deployment. Also
  runs automatically as `ship --merge`'s end-state stage. Works in any repo with a gh-accessible
  remote.
license: MIT
metadata:
  author: Nicholas Sollazzo
  version: "3.0.0"
compatibility: Requires git and an authenticated gh CLI
argument-hint: "[<PR number>] [--from-ship] [--base <branch>]"
---

# Merge and Monitor

Take a PR through merge → deployment → health verification, reporting evidence at each stage. Never declare success without observed proof (run conclusion, health output).

## Entry contract

**Standalone** (the user asked directly): run every step from Step 1.

**From `ship --merge`** (`--from-ship`): ship passes the PR number, the base branch (`--base`),
and `--squash`, and has already proved readiness via `babysit` (fresh APPROVED + CI green +
mergeable). **Skip Step 1 entirely** — re-querying would be a slower, staler signal than what ship
just observed. Start at Step 2.

**Target branch.** Throughout, "the target branch" means `--base` when ship passed one, otherwise
the repo default (`git remote show origin` / `origin/HEAD`). A PR stacked on a non-default base
deploys from *that* branch — using the default would watch the wrong runs.

## Invoking sibling skills (portability)

Step 5 uses this kit's `verify` skill. Run it by whatever mechanism your agent provides — a
skill-invocation tool if your harness has one, otherwise load `verify/SKILL.md` from this kit and
follow its procedure directly.

## Step 1: Identify the PR and gate on readiness

Find the PR: the one for the current branch (`gh pr view`) unless the user named one.

Check readiness before merging:

```bash
gh pr view <n> --json state,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup
```

If anything is blocking (red CI, missing approval, conflicts), STOP and report exactly what's blocking — do not force-merge or bypass checks. `statusCheckRollup` entries come in two shapes (CheckRun uses `conclusion`, StatusContext uses `state`) — handle both when summarizing.

## Step 2: Merge

Merge with the repo's preferred method (infer from recently merged PRs if unsure; default `--squash`):

```bash
gh pr merge <n> --squash --delete-branch
```

If `gh pr merge` fails with 401/403 despite the PR being mergeable, fall back to REST — some org token setups reject the GraphQL path but accept REST:

```bash
gh api -X PUT repos/{owner}/{repo}/pulls/<n>/merge -f merge_method=squash
```

Capture the merge commit SHA (`gh pr view <n> --json mergeCommit`) — it identifies the deploy run in Step 4.

## Step 3: Locate the deployment

Determine what the merge triggers:

1. Check `.github/workflows/` for workflows firing `on: push` to **the target branch** whose name/jobs indicate deploy/release/CD.
2. If none, check for external CD the repo documents (Vercel/Flux/ArgoCD/etc. — README, CLAUDE.md, docs).
3. If no deployment pipeline exists, say so plainly, confirm the merge landed, and stop — do not invent a monitoring step.

## Step 4: Monitor to completion

For GitHub Actions, find the run for the merge commit and watch it:

```bash
gh run list --workflow=<deploy>.yml --branch <target> --limit 5 --json databaseId,headSha,status,conclusion,url
```

**Trap**: match the run by `headSha` == the merge commit SHA — the newest run may belong to someone else's merge. If the run hasn't appeared yet, poll every ~15s; once found:

```bash
gh run watch <run-id> --exit-status
```

Deploy runs can take minutes — poll in the background rather than blocking, at a frequency matched to the pipeline's typical duration. If the run fails, fetch the failing log (`gh run view <run-id> --log-failed`), report it verbatim, and STOP — do not retry the deploy or attempt fixes without asking.

## Step 5: Verify health

After the pipeline succeeds, verify the deployment actually works:

1. If the deploy workflow itself contains verification/smoke-test steps, read their output as evidence — that beats re-running anything.
2. Otherwise invoke the `verify` skill, telling it explicitly to exercise the **deployed** surface (the live URL, the deployed CLI, the endpoint the change touches) rather than the local tree — name that target in the invocation, since `verify` defaults to the working copy. It reports concrete commands + output, which is exactly the evidence Step 6 needs.
3. If neither is possible, state that verification is limited to the pipeline's own success — do not fabricate a health check.

## Guardrails

- **Never merge without an explicit merge instruction.** This skill merges because merging is what it was asked to do. `babysit` still never merges; `ship` still stops at green without `--merge`.
- **Never mutate external state to make a deploy go green.** Diagnose read-only. A red deploy gate caused by shared infrastructure is someone else's live workload — report the cause and the owner, don't clear it.
- **A failed deploy is an incident, not a stage to retry.** The merge already landed. Report the failing log verbatim and STOP. Rolling back or re-running is the user's decision.

## Step 6: Report

Summarize with evidence: merged PR + merge commit SHA, deploy run URL + conclusion, health-check output. If anything was skipped or unverifiable, state it explicitly — "deployed and verified" must be literally true.
