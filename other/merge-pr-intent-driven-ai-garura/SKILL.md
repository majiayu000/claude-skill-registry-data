---
name: merge-pr
description: Merge a pull request on the configured platform, switch to main, pull latest, and delete the feature branch (local and remote)
user-invocable: false
---

# merge-pr

Model-invocable skill for merging pull requests and completing the branch lifecycle.

## Purpose

Merge a PR using the platform's default merge strategy, switch to the base branch, pull latest, and delete the feature branch (local and remote). This skill executes — it does not orchestrate.

## Input

Receive from caller (agent):

| Field | Required | Description |
|-------|----------|-------------|
| `pr_number` | No | PR number to merge (auto-detected from current branch if omitted) |
| `delete_branch` | No | Delete feature branch after merge (default: true) |
| `base_branch` | No | Base branch to switch to after merge (default: auto-detect from PR) |

## Platform Dispatch

This skill routes all platform operations through the `platform-adapter` skill. The adapter resolves the active platform from `.garura/core/config.yaml` and dispatches to the correct CLI.

Supported platforms: `github` (via `gh`), `gitlab` (via `glab`). Bitbucket is not supported in this version — the adapter will return a structured failure if `platform=bitbucket` is configured.

## Process

### 1. Identify PR

If `pr_number` is not provided, detect the PR for the current branch:

```bash
# Get current branch
branch=$(git branch --show-current)
```

Invoke the `platform-adapter` skill with `verb: view-pr` and `args: {pr_number: ""}` (omit pr_number to auto-detect from current branch, per adapter's platform CLI behaviour).

### 2. Verify PR is Mergeable

Invoke the `platform-adapter` skill with `verb: view-pr` and `args: {pr_number: {pr_number}}` to check PR state. Access `state` and `mergeable` (GitHub) or equivalent fields from the raw output. The PR must be open and not have merge conflicts.

If the PR has merge conflicts, halt with structured failure (do not attempt resolution).

### 3. Merge PR

Invoke the `platform-adapter` skill with `verb: merge-pr` and `args: {pr_number: {pr_number}}`. The adapter uses the repository's default merge strategy — do not override.

### 4. Switch to Base Branch

```bash
# Switch to base branch (detected from PR or provided)
git checkout {base_branch}
```

### 5. Pull Latest

```bash
# Ensure local base is up to date
git pull
```

### 6. Delete Feature Branch

If `delete_branch` is true (default):

```bash
# Delete local feature branch
git branch -d {branch}

# Delete remote feature branch (if not already deleted by platform)
git push origin --delete {branch} 2>/dev/null || true
```

The remote deletion is best-effort — some platforms auto-delete on merge.

## Output

Return structured result to caller:

| Field | Description |
|-------|-------------|
| `status` | `merged`, `conflict`, or `failed` |
| `pr_number` | PR that was merged |
| `merge_sha` | Merge commit SHA (if available) |
| `base_branch` | Branch switched to |
| `branch_deleted` | Whether feature branch was deleted |
| `error` | Error message (only on failure) |

**IMPORTANT**: This skill produces operation results. The calling agent receives this output and decides what to do next. Do NOT instruct the agent to return or stop.

## Constraints

- NEVER override merge strategy — always use repository default
- NEVER resolve merge conflicts — halt on conflict
- NEVER ask for user input — return result to caller
- NEVER hardcode platform-specific CLI commands — always route through platform-adapter
- ALWAYS read platform from project config (handled by platform-adapter)
- ALWAYS verify PR is mergeable before attempting merge
- ALWAYS switch to base branch and pull after merge

## Version

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Category | operations |
