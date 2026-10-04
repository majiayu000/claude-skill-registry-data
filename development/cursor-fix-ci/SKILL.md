---
name: cursor-fix-ci
description: Find failing PR checks, inspect logs or external check links, and apply focused fixes
---

## Codex publication boundary

Treat repository review, local edits, pushing a branch, opening or updating a PR, and merging as distinct effects. Verify the target repository and current user authorization for each external write. If push or PR publication is not yet authorized, complete the local branch, diff, checks, and draft PR text so approval is the final step. Do not merge unless separately requested. Preserve the upstream review and CI workflow within those boundaries.

# Fix CI

## Trigger

Branch or PR CI is failing and needs a fast, iterative path to green checks.

## Workflow

1. Resolve the active PR and inspect `gh pr checks --json name,bucket,state,workflow,link`.
2. Inspect failed jobs and extract the first actionable error. Use GitHub Actions logs when available; otherwise use the check link to identify the failing command or service.
3. Apply the smallest safe fix.
4. Push, re-check the PR check set, and repeat until green.

## Guardrails

- Fix one actionable failure at a time.
- Prefer minimal, low-risk changes before broader refactors.
- Keep `gh pr checks` as the source of truth for overall PR CI state.

## Output

- Primary failing job and root error
- Fixes applied in iteration order
- Current CI status and next action
