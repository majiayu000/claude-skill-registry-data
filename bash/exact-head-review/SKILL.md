---
name: exact-head-review
description: "Resolve the live PR head and verify an isolated checkout before reviewing or recording an exact-revision verdict."
---
# Review the actual pull-request head

A supplied SHA is a claim. Resolve the current head independently through the repository API or `gh pr view --json headRefOid,baseRefOid,state`. Confirm repository identity and open state. Compare full object IDs, never short prefixes.

1. Record the resolved head and base, repository, PR number and retrieval time.
2. Fetch the PR's ref through the verified repository remote. Check command success, then verify the fetched object equals the API head. Stop on mismatch or unavailable evidence; do not use stale `FETCH_HEAD`.
3. Create a new detached worktree at that exact commit in an operator-chosen review directory. Do not reuse, reset or clean another worktree. Confirm both HEAD and clean tracked/untracked state before testing.
4. Read the actual diff and consumers. A nonempty diff does not prove the behavior is wanted; a test count does not prove a guard can fail. Use `mutation-check` for important negative paths.
5. Re-read live head/base before issuing the verdict. If either changed, identify affected evidence and review the new candidate. Do not transfer approval by branch name.
6. Report full revision, findings, executed checks, limits and whether the verdict is current. Remove only your clean disposable worktree with `git worktree remove`; preserve dirty evidence for inspection.

No script is bundled for this workflow. Use the available repository connector or installed Git/GitHub CLI, and report unavailable dependencies explicitly.
