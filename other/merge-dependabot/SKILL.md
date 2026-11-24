---
name: merge-dependabot
description: Explicitly invoke to review and merge this repository's open Dependabot PRs one at a time.
---

# Merge Dependabot PRs

Invocation: `$merge-dependabot`. Invoking this skill authorizes sequential merges of the selected Dependabot PRs.

1. List open Dependabot PRs, for example: `mise exec -- gh pr list --repo ahstn/oceans-llm --state open --app dependabot --limit 100`. Inspect diffs, actual resolved versions, review feedback, mergeability, and CI; do not trust titles alone.
2. Order by dependency relationships first. Otherwise group by ecosystem and shared lockfile, handle smaller independent updates before broader runtime/authentication changes, and leave blocked PRs until repaired. Explain the chosen order briefly.
3. Process one PR at a time. Refresh its head SHA and checks after each preceding merge. Resolve conflicts or dependency failures in an isolated worktree; preserve unrelated local changes and keep lockfiles consistent with manifests. Run applicable mise checks and the verification planner; follow `verify-oceans-admin` for runtime surfaces and include its report in any created PR.
4. Wait for applicable CI to pass on the latest head. Inspect failures before retrying; stop work on a PR when a substantive failure cannot be resolved within the dependency update, report the blocker, and continue independent PRs. Never bypass checks, branch protections, or reviews.
5. Read the repository's allowed merge methods. Merge with `gh pr merge <number> --repo ahstn/oceans-llm --merge --match-head-commit <verified-sha>` when merge commits are allowed. Confirm `state: MERGED` before advancing; never queue all PRs for auto-merge.
6. Re-list open Dependabot PRs and report merged PRs in order, fixes, verification, and anything remaining. Do not silently expand the batch to newly created PRs.
