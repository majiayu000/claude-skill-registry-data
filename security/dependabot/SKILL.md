---
name: dependabot
description: Processes all open Dependabot PRs sequentially — rebases if needed, analyzes for breaking changes and security issues, then merges or requests changes. Use when you want to handle pending Dependabot dependency updates.
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, WebSearch, WebFetch, Task, AskUserQuestion
---

# Dependabot PR Processor

Processes all open Dependabot pull requests one at a time: analyze for risks first, then rebase and merge if safe, or request changes if not.

## Process Overview

```
For each open Dependabot PR:
  1. Analyze update for breaking changes and security issues
  2. If risky → request changes with explanation → move to next PR
  3. If safe → check if up-to-date with base branch
  4. If not up-to-date → comment "@dependabot rebase" → poll until done
  5. Merge
  6. Move to next PR
```

## Step 1: Discover Open Dependabot PRs

```bash
gh pr list --author "app/dependabot" --state open --json number,title,headRefName,baseRefName,url,labels,body --limit 100
```

Parse the JSON output. If no PRs found, report "No open Dependabot PRs" and stop.

Sort PRs by number (ascending) to process oldest first.

Print a summary table of all found PRs before starting processing.

## Step 2: Process Each PR Sequentially

For each PR, execute steps 2a through 2e before moving to the next.

### Step 2a: Analyze Dependency Update

Analyze the update **before** rebasing — no point wasting a rebase if the update is problematic.

Extract from the PR body and title:

- **Package name** and **ecosystem** (npm, cargo, pip, docker, github-actions, etc.)
- **Version change** (from → to)
- **Whether it's a major, minor, or patch update**

#### Determine Risk Level

**Major version bumps** (e.g., 6.x → 7.x): HIGH risk — likely contains breaking changes.

**Minor version bumps** (e.g., 6.1 → 6.2): MEDIUM risk — could contain new features or deprecations.

**Patch version bumps** (e.g., 6.1.1 → 6.1.2): LOW risk — typically bug fixes only.

#### Research the Update

Use web search to check for issues:

```
Search: "<package-name> <new-version> breaking changes"
Search: "<package-name> <new-version> changelog"
Search: "<package-name> <new-version> security vulnerability CVE"
```

Also check the PR body itself — Dependabot usually includes a changelog summary and release notes.

#### Analysis Checklist

Evaluate the following and document findings:

1. **Breaking changes**: Does the changelog mention breaking changes, removed APIs, or changed behavior?
2. **Security advisories**: Is this update fixing a known CVE? Are there new CVEs introduced?
3. **Compatibility**: Is the new version compatible with our other dependencies and our minimum supported versions?
4. **CI status**: Check if CI passes on the PR:
   ```bash
   gh pr checks <NUMBER>
   ```

#### Decision Matrix

| Condition | Action |
|-----------|--------|
| Patch update, CI passes, no known issues | **Proceed to rebase/merge** |
| Minor update, CI passes, no breaking changes found | **Proceed to rebase/merge** |
| Major update, CI passes, no breaking changes found | **Proceed to rebase/merge (with note)** |
| CI fails | **Request changes** |
| Breaking changes found | **Request changes** |
| Security vulnerability introduced | **Request changes** |
| Cannot determine safety | **Request changes** (err on the side of caution) |

If the analysis found problems → skip to **step 2e** (request changes).
If the analysis is positive → continue to **step 2b**.

### Step 2b: Check if PR is Up-to-Date

```bash
gh pr view <NUMBER> --json mergeable,mergeStateStatus
```

Also check if the PR branch is behind the base branch:

```bash
git fetch origin <baseRefName> <headRefName>
git rev-list --count origin/<headRefName>..origin/<baseRefName>
```

If the count is > 0, the PR needs a rebase (likely because a previous PR was just merged into the base branch). Proceed to step 2c.
If the count is 0, the PR is up-to-date. Skip to step 2d.

### Step 2c: Rebase via Dependabot Comment

Post a comment to trigger Dependabot's rebase:

```bash
gh pr comment <NUMBER> --body "@dependabot rebase"
```

Then poll until the rebase is complete. Check every **60 seconds**:

```bash
sleep 60
git fetch origin <headRefName>
git rev-list --count origin/<headRefName>..origin/<baseRefName>
```

- If count reaches 0 → rebase complete, proceed to step 2d
- If after **10 minutes** (10 checks) the rebase still hasn't completed → log a warning and skip this PR (move to next)
- If the PR is closed or the branch is gone → log and skip

### Step 2d: Merge the PR and Wait for Completion

`main` merges through a merge queue. Merge with the procedure in the
`merge-train` skill, which waits on the queue entry and not on the PR state: a
PR that drops out of the queue stays `OPEN`.

Do not merge a Dependabot security update unless **Security update approved**
is green on the commit being merged (`AGENTS.md`, "Security updates"). Report
it and move to the next PR.

Wait until the PR is merged before starting the next one, because each merge
changes `main` and makes the other Dependabot PRs outdated.

Log: `"Merged PR #<NUMBER>: <title>"`

### Step 2e: Request Changes

If the analysis in step 2a found problems:

```bash
gh pr review <NUMBER> --request-changes --body "$(cat <<'EOF'
## Dependabot Auto-Review: Changes Requested

This dependency update was flagged for manual review.

### Findings

<list specific findings here>

### Reason

<explain why this cannot be auto-merged>

### Recommended Action

<suggest what the maintainer should do>
EOF
)"
```

Log: `"Requested changes on PR #<NUMBER>: <title> — Reason: <brief reason>"`

## Step 3: Summary Report

After processing all PRs, print a summary:

```
## Dependabot Processing Complete

| PR | Package | Version | Action | Reason |
|----|---------|---------|--------|--------|
| #123 | vite | 6.0 → 7.0 | Merged | Patch update, CI green |
| #124 | serde | 1.0 → 2.0 | Changes requested | Major version, breaking API |
| #125 | node | 22 → 24 | Skipped | Rebase timed out |

**Merged:** N
**Changes requested:** N
**Skipped:** N
```

## Important Notes

- Process PRs **strictly one at a time** — do NOT start processing the next PR until the current one is confirmed `MERGED`. Each merge changes the base branch, making other PRs outdated
- Always wait for CI to be green before merging
- When in doubt, request changes — a human can always override
- The `@dependabot rebase` command is the standard way to trigger a rebase; Dependabot responds with a reaction emoji and rebases asynchronously
- After confirming a merge, do a brief `sleep 10` before starting the next PR to allow GitHub to process webhooks and update remaining PR branches
- Expect each subsequent PR to need a rebase after the previous one merges — this is normal and handled by step 2b/2c
