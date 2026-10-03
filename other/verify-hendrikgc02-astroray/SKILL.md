---
name: verify
description: Spawn the hardware-verifier agent for a named package's most recent PR.
invocation: /verify <pkg>
---

# /verify \<pkg\>

Spawn the `hardware-verifier` agent for the named package.

## Before spawning

1. Find the package's most recent PR:
   ```
   gh pr list --search "<pkg>" --state open
   gh pr list --search "<pkg>" --state closed --limit 5
   ```
2. Read the package spec at `.astroray_plan/packages/<pkg>*.md` to extract:
   - The most recent binding introduced (for the smoke-check step)
   - The acceptance gate list

3. Resolve the PR's worktree and head SHA:
   ```
   gh pr view <number> --json headRefName,headRefOid
   ```
   The worktree path is `.claude/worktrees/<pkg>` (the branch's registered
   worktree). Verify it exists via `git worktree list`.

4. Pass to hardware-verifier:
   - `worktree_path`: absolute path to the PR's branch worktree
   - `expected_sha`: the PR's `headRefOid`
   - `pr_number`: PR number
   - `spec_path`: package spec path
   - `recent_binding`: the most recent binding name (for Step 2 smoke-check)

## Reactive mode

If a PR has the `needs-verifier` label, `/verify` can also be triggered
reactively. In that case, extract the package name from the PR title.
