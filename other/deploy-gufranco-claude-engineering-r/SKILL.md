---
name: deploy
description: Merge a shipped PR, verify the deployment, and monitor post-deploy health, with land and canary subcommands.
disable-model-invocation: true
argument-hint: "/deploy [land|canary] [pr-number]"
allowed-tools: "Read, Bash, Grep, AskUserQuestion"
sensitive: true
---

## Overview

Post-merge deployment and monitoring skill. Picks up where `/ship` leaves off: merging the PR, verifying the deployment succeeds, and monitoring production health afterward.

## When to Use

Run `land` once `/ship pr` produced a green, approved PR, and `canary` right after a deploy lands, whether this session merged it or not.

### Subcommand Routing

| Invocation | Action |
|-----------|--------|
| `/deploy` or `/deploy land` | Merge PR and verify deployment (default) |
| `/deploy canary` | Post-deploy monitoring for errors and regressions |

If no subcommand is given, default to `land`.

## Process

1. Route the invocation per Subcommand Routing.
2. For `land`, run its Steps in order: identify, pre-merge checks, merge, wait for the deploy, health check, switch to local main.
3. For `canary`, run its Steps: baseline, monitor loop, per-interval report, final report, rollback suggestion on issues.
4. End with the Output block for `land` or the Canary Report for `canary`.

---

## land

Merge a PR, wait for the deployment pipeline, and verify production health.

### When to use

- After `/ship pr` created a PR and CI is green.
- When a PR is approved and ready to merge.

### Arguments

- No arguments: detect the PR for the current branch.
- PR number or URL: target a specific PR.
- `--squash`: squash merge (default).
- `--merge`: create a merge commit instead.
- `--no-delete`: keep the branch after merge.

### Steps

1. **Identify the PR.** If no argument, find the PR for the current branch:
   ```
   GH_TOKEN=$(gh auth token --user <account>) gh pr view --json number,state,reviewDecision,statusCheckRollup
   ```
   If no `gh` is available, try `glab`. Prefix with the appropriate token per [`standards/github-accounts.md`](../../standards/github-accounts.md) or [`standards/gitlab-accounts.md`](../../standards/gitlab-accounts.md).

2. **Pre-merge checks.** Verify all conditions are met:

   | Condition | How to check | Blocker? |
   |-----------|-------------|----------|
   | CI is green | `statusCheckRollup` all passing | Yes |
   | PR is approved | `reviewDecision` is APPROVED | Yes |
   | No merge conflicts | `mergeable` is true | Yes |
   | Branch is up to date | Compare with base branch HEAD | Warning only |

   If any blocker condition fails, stop and report the issue. Do not merge.

3. **Merge the PR.** Default to squash merge:
   ```
   GH_TOKEN=$(gh auth token --user <account>) gh pr merge <number> --squash --delete-branch
   ```
   If `--no-delete` is passed, omit `--delete-branch`.
   If this is a dual-base PR, same change targeting two branches, omit `--delete-branch` per [`../../rules/git-workflow.md`](../../rules/git-workflow.md).

4. **Wait for deployment.** Detect the deployment mechanism:

   | Signal | Platform | How to monitor |
   |--------|---------|---------------|
   | [`.github/workflows/`](../../.github/workflows) with deploy job | GitHub Actions | `GH_TOKEN=$(gh auth token --user <account>) gh run list --branch main --limit 1 --json databaseId,status`, then poll a one-shot `GH_TOKEN=$(gh auth token --user <account>) gh run view <id> --json status,conclusion` every 60 seconds, at most 20 times, and every 3 minutes while the run is `queued`; GitLab: `glab ci status -F json` on the same schedule |
   | Vercel project | Vercel | Check Vercel MCP or `vercel ls --limit 1` |
   | Railway, Render, Fly | PaaS | Suggest user check the dashboard |
   | Manual deploy | Any | Ask user to trigger and confirm |

   If no deployment mechanism is detected, ask the user how deployments work.

5. **Verify production health.** After deployment completes:
   - If a health endpoint is known, from project docs or user input, `curl` it and verify 200.
   - If the project has a public URL, verify it loads.
   - Check for new error reports if monitoring is configured, such as through the Sentry MCP.
   - Report the deployment result.

6. **Switch to local main.** After successful deployment:
   ```
   git checkout main && git pull origin main
   ```

### Output

```
## Deployment Summary

**PR:** #<number> - <title>
**Merged:** <timestamp GMT>
**Method:** squash / merge commit
**Branch deleted:** yes / no

### Deployment
**Platform:** <detected platform>
**Status:** success / pending / failed
**URL:** <production URL if known>

### Health Check
**Endpoint:** <URL checked>
**Status:** <HTTP status code>
**Errors:** none / <error details>
```

---

## canary

Monitor a recently deployed change for errors, performance regressions, and unexpected behavior.

### When to use

- Immediately after `/deploy land` succeeds.
- When a deploy happened outside this session and the user wants a health check.
- When monitoring a risky change in the first minutes after deployment.

### Arguments

- No arguments: monitor for 5 minutes with checks every 60 seconds.
- `--duration <minutes>`: monitor for a custom duration.
- `--url <url>`: target a specific URL for health checks.
- `--baseline`: capture current metrics as the baseline before a deploy, run this first.

### Steps

1. **Establish baseline.** If `--baseline` was passed or no prior baseline exists:
   - Record current error rate from monitoring tools, if accessible.
   - Record response time for key endpoints.
   - Save as the comparison point.

2. **Monitor loop.** For each check interval:
   - Verify the health endpoint returns 200.
   - Check for new errors in monitoring tools, Sentry MCP if available.
   - Compare current response time against baseline.
   - Check browser console for JavaScript errors, if Playwright MCP is available and a frontend URL is known.

3. **Report per interval:**

   | Check | Status |
   |-------|--------|
   | Health endpoint | 200 OK / <error> |
   | New errors | 0 / <count and summary> |
   | Response time | <current> vs <baseline> |
   | Console errors | 0 / <count> |

4. **Final report after monitoring completes:**

   ```
   ## Canary Report

   **Duration:** <N> minutes
   **Intervals:** <count>
   **URL:** <monitored URL>

   ### Health
   **Uptime:** <percentage>
   **Errors detected:** <count>

   ### Performance
   **Response time (baseline):** <value>
   **Response time (current):** <value>
   **Delta:** <percentage change>

   ### Verdict
   <CLEAN: no issues detected / WARNING: <issues found>>
   ```

5. **If issues detected:** suggest rollback steps:
   - `git revert <merge-commit> && git push`
   - Or revert via the platform's rollback mechanism.

## Rules

- Never merge a PR with failing CI checks. No exceptions.
- Never merge without approval unless the user explicitly requests it.
- Prefix every `gh` or `glab` command with the appropriate token per [`standards/github-accounts.md`](../../standards/github-accounts.md) or [`standards/gitlab-accounts.md`](../../standards/gitlab-accounts.md).
- All timestamps in GMT.
- Canary monitoring is non-blocking: report findings, do not auto-rollback without user confirmation.
- If rate limits are a concern for monitoring, use one-shot checks instead of continuous polling per [`../../rules/git-workflow.md`](../../rules/git-workflow.md).
- Never access production databases or infrastructure directly. Use health endpoints and monitoring tool APIs only.

## Common Rationalizations

- "`statusCheckRollup` is green, so CI passed": the rollup reads success when only an unrelated check ran. Confirm the CI workflows ran on the head commit with `GH_TOKEN=$(gh auth token --user <account>) gh run list --commit <full-sha>`.
- "The reviewer is away and the change is small": merging without approval needs the user's explicit request. Ask.
- "The canary showed errors, revert now to be safe": canary is non-blocking. Report the findings and the rollback steps, then wait for confirmation.
- "The dashboard is faster than the health endpoint": production databases and infrastructure stay off limits. Use health endpoints and monitoring APIs.
- "Delete the branch, it merged": a dual-base PR still needs its branch for the second merge. Omit `--delete-branch`.

## Red Flags

- Stop and report when any pre-merge blocker row fails, and leave the PR unmerged.
- Stop and ask how deployments work when no row of the deployment detection table matches.
- Stop and present the rollback steps when the health endpoint returns anything other than 200 after the deploy.
- Stop and switch to one-shot `GH_TOKEN=$(gh auth token --user <account>) gh run view` checks when `GH_TOKEN=$(gh auth token --user <account>) gh api rate_limit` shows fewer than 500 remaining.

## Verification

- `GH_TOKEN=$(gh auth token --user <account>) gh pr view <number> --json state` returns `MERGED` after `land`.
- The deploy run for the merge commit shows `completed` with conclusion `success`, or the user confirmed a manual deploy.
- The health endpoint returned 200, with the URL and status in the Deployment Summary.
- `git branch --show-current` prints `main` and `git status` reports the branch up to date with `origin/main`.
- After `canary`, the Canary Report carries a CLEAN or WARNING verdict with the interval count.

## Related skills

- `/ship pr` -- Create the PR that this skill merges.
- `/ship checks` -- Diagnose CI failures before merging.
- `/incident` -- Document the incident if the deploy causes problems.
- `/investigate` -- Debug issues found during canary monitoring.
