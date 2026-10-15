---
name: GitHub
description: Read pull requests, issues and CI checks via GitHub REST API.
requires:
  bins: []
  env:
    - GITHUB_TOKEN
---

# GitHub

Use this skill for repository operations: pull requests, issues, CI checks.
Backed by the `github` extension which calls the GitHub REST API directly with
a Personal Access Token. No `gh` CLI dependency.

## Use when

- "List open PRs in <repo>"
- "Show details of PR 123"
- "Check CI status of PR 7"
- "List open issues"

## Do not use when

- Cloning, committing, or pushing code → use `git` directly
- Creating PRs / issues (write operations) → not exposed in this version
- Searching across many repos → REST search is not exposed; ask the user to use the GitHub UI

## Tools

### `status`
No arguments. Returns whether `GITHUB_TOKEN` is set and, if so, the
authenticated user.

### `pr_list`
- `repo` (string) — `owner/repo`. Falls back to `GITHUB_DEFAULT_REPO`.
- `state` (string, optional) — `open`|`closed`|`all`. Default `open`.
- `limit` (integer, optional) — 1–100, default 20.

Returns `{repo, state, limit, count, pulls: [{number, title, state, draft, user, head_sha, base_ref, html_url, created_at, updated_at}]}`.

### `pr_view`
- `repo` (string, optional)
- `number` (integer, required)

Returns the raw GitHub PR object.

### `pr_checks`
- `repo` (string, optional)
- `number` (integer, required)

Two-step: fetches the PR to get the head SHA, then fetches check-runs.
Returns `{repo, number, head_sha, checks: {total_count, check_runs: [...]}}`.

### `issue_list`
- `repo` (string, optional)
- `state` (string, optional)
- `limit` (integer, optional, 1–100)

Returns issues with PRs filtered out (`pull_request` field absent).

## Execution guidance

- Start with `status` if uncertain about auth (verifies token + lists default repo).
- If error code is `-32011` (unauthorized) → `GITHUB_TOKEN` is missing or invalid; ask the operator.
- If `-32013` (rate limited) → wait until the `reset_at` epoch in the message.
- Pass explicit `repo` only when different from `GITHUB_DEFAULT_REPO`.
- Prefer `pr_checks` over `pr_view` when the user asks "what is failing in PR X".
