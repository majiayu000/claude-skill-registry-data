---
name: automerge
allowed-tools: Bash, Read, Grep, Glob, ToolSearch
description: 'Merge open PRs in bulk or enable GitHub auto-merge. Use for "automerge", "merge everything", "merge all PRs", "clear the PR queue", "enable auto-merge".'
---

# Automerge — Bulk & Automatic PR Merging

Merge every open pull request that is safe to merge, and/or enable GitHub's native
**auto-merge** so future-ready PRs land on their own when checks go green.

Two distinct capabilities — pick based on what the user wants:

| User intent | Capability | Effect |
|-------------|-----------|--------|
| "Merge everything right now" | **Bulk merge** | Merge each mergeable open PR immediately |
| "Auto-merge from now on" / "enable auto-merge" | **Enable auto-merge** | GitHub merges each PR the instant its required checks pass |

All GitHub actions use the `mcp__github__*` tools. Load them with
`ToolSearch("select:mcp__github__list_pull_requests,mcp__github__pull_request_read,mcp__github__merge_pull_request,mcp__github__enable_pr_auto_merge,mcp__github__update_pull_request,mcp__github__get_me")`.

## Guardrails (read first)

"Everything" does **not** mean "recklessly". A merge is hard to reverse and
outward-facing. Apply these unless the user *explicitly* overrides each one:

1. **Never force-merge a PR with failing required checks.** Prefer `enable_pr_auto_merge`
   so GitHub gates on the checks itself. Only bypass when the user names the PR and
   says to merge despite red.
2. **Skip drafts.** A draft PR is not ready by definition. List them, don't merge them.
3. **Skip PRs with requested changes / unresolved review threads** unless told otherwise.
4. **Confirm scope before a destructive bulk run.** If there are more than a handful of
   open PRs, list them and get a go-ahead before merging in bulk — one wrong merge is
   easier to prevent than to revert.
5. **Distinguish unrelated red checks from real failures.** A red check on an unrelated
   project (e.g. a monorepo Vercel deploy pointing at a different app) is not a reason to
   block a docs-only PR — but say so explicitly rather than silently overriding.

## Workflow: bulk-merge all open PRs

1. **Identify the repo and user.**
   ```
   mcp__github__get_me                     # confirm identity/permissions
   ```
   Determine `owner`/`repo` from the session's repo scope (or ask).

2. **List open PRs.**
   ```
   mcp__github__list_pull_requests({ owner, repo, state: "open", per_page: 30 })
   ```
   Page through if there are more. Note draft status on each.

3. **For each non-draft PR, check mergeability.**
   ```
   mcp__github__pull_request_read({ method: "get", owner, repo, pullNumber })       # mergeable, mergeable_state
   mcp__github__pull_request_read({ method: "get_status", owner, repo, pullNumber }) # required checks
   ```
   - `mergeable_state: "clean"` → safe to merge now.
   - `"blocked"` / `"unstable"` → checks pending or failing; prefer auto-merge instead.
   - `"dirty"` → merge conflict; skip and report (needs a rebase, not a merge).

4. **Merge the clean ones.**
   ```
   mcp__github__merge_pull_request({ owner, repo, pullNumber, merge_method: "squash" })
   ```
   Default to `squash` unless the repo convention says otherwise. Continue on error —
   collect failures and report them rather than aborting the whole batch.

5. **Report** a compact table: PR #, title, outcome (merged / auto-merge enabled /
   skipped-draft / skipped-conflict / skipped-failing), and next step for each skip.

## Workflow: enable auto-merge (the "set and forget" path)

For PRs that are ready-but-waiting-on-CI, don't sit and poll — hand it to GitHub:

```
mcp__github__enable_pr_auto_merge({ owner, repo, pullNumber, merge_method: "squash" })
```

GitHub then merges automatically the moment all required checks pass and approvals are
met. Requires auto-merge to be enabled in repo settings and at least one required check
or branch-protection rule — if the call errors with that reason, tell the user to enable
"Allow auto-merge" in **Settings → General → Pull Requests**.

To disable later: `mcp__github__disable_pr_auto_merge({ owner, repo, pullNumber })`.

## Merge method selection

| Method | When |
|--------|------|
| `squash` | Default. Keeps `main` history linear and clean. |
| `merge` | When the repo wants full commit history / merge commits preserved. |
| `rebase` | When the repo enforces a linear history without merge commits. |

Check the repo's existing merged PRs or branch-protection settings to infer the
convention before overriding the `squash` default.

## Handling a red check that isn't the PR's fault

Monorepos often attach many CI checks; some fail for reasons unrelated to a given diff
(a deploy project pointed at a stale/removed directory, a flaky job). Before treating a
PR as unmergeable:

- Read *which* check failed and whether the diff could plausibly cause it.
- If a docs/config-only change trips an app-build check for a different package, that's
  infra noise — surface the diagnosis to the user and recommend merging or marking the
  check non-required, rather than blocking silently.
- Never edit unrelated app code or Vercel/CI settings to "fix" a check unless the user
  asks.

## Turning this into a standing automation (optional)

If the user wants *every future PR* auto-merged without being asked each time, that's a
repo-level or harness-level automation, not a one-off skill run:

- **Repo-level**: a GitHub Actions workflow that calls `gh pr merge --auto --squash` on
  `pull_request` events (respecting branch protection). Offer to draft it if asked.
- **Harness-level**: subscribe to PR activity (`subscribe_pr_activity`) and enable
  auto-merge on each new PR as it appears.

Don't set either up implicitly — auto-merging all future PRs is a policy decision.
Confirm with the user first.

## Quick reference

```
# Bulk merge everything mergeable (after listing + confirming)
list_pull_requests(state:"open") → for each non-draft clean PR → merge_pull_request(squash)

# Enable auto-merge on the ready-but-pending ones
enable_pr_auto_merge(pullNumber, merge_method:"squash")

# Undo
disable_pr_auto_merge(pullNumber)
```

## Checklist

1. Confirm `owner`/`repo` and permissions (`get_me`).
2. List open PRs; separate drafts, conflicts, clean, and pending-CI.
3. For a large batch, show the list and get explicit go-ahead.
4. Merge the clean ones (`squash` by default); enable auto-merge on pending-CI ones.
5. Skip drafts and conflicts; report each skip with its reason and next step.
6. Report a final table of outcomes. Never force-merge failing required checks without
   an explicit per-PR instruction.
