---
name: post-merge-cleanup
description: "Verify a merged PR and remove its clean, idle task worktree. Use for post-merge cleanup."
license: MIT
metadata:
  display-name: "Post Merge Cleanup"
  version: "1.0"
  platforms: "claude-code codex"
  tags: "git worktree cleanup merged-pr"
---

# Post merge cleanup

An explicit cleanup request or a standing user or repository rule to run the cleaner when a known PR is reported merged authorizes removing only its identified task worktree after proving the merge. A generic PR handoff or request to merge alone does not authorize removal. On Claude Code, dispatch the `cleaner` agent; on Codex, dispatch a cleaner subagent and tell it to read this `SKILL.md` completely. If no subagent is available, take this role in the current session. The cleaner never merges a PR.

1. Read repository rules. Identify the exact repository, PR, base branch, PR head branch and task worktree from the user's request or established handoff. If more than one candidate fits, stop and report ambiguity. Inspect `git status --short --branch`, `git worktree list --porcelain`, and the worktree path before mutation.
2. Resolve the selected local Git remote's canonical repository identity. Query the PR with explicit repository selection independent of `GH_REPO` or other ambient defaults, and require its returned repository identity to match that remote. Require the PR's actual `MERGED` state, base branch, head branch, full head commit ID, and full merge commit ID. Fetch only that base ref from the verified remote and require the merge commit reachable from it. Never infer a merge from a closed PR, branch deletion, or the user's statement. If identity, merge metadata, or the matching ref cannot be verified, stop.
3. Match one non-primary linked worktree's exact canonical path and branch from `git worktree list --porcelain` to that PR head. Require its `HEAD` to equal the PR's full head commit ID; detached, moved, duplicate, and branchless cases stop. Never select by directory-name resemblance or clean up the primary checkout.
4. In that exact worktree, require empty `git status --porcelain=v1 --untracked-files=all` and empty `git status --porcelain=v1 --ignored=matching --untracked-files=all`. Inspect its worktree lock and live processes' current directories, open files, command lines, executables, and mapped files (`lsof`, `ps`, or `/proc` as available). Resolve paths before comparing. If any process view is unavailable, fails, or leaves worktree use uncertain, skip removal. Recheck identity, status, lock, and use immediately before removal.
5. Run `git worktree remove <exact path>` from another checkout, without `--force`. Do not prune broadly or delete branches. Stop on any failure; never retry with a stronger command. Preserve dirty, ignored, locked, active, primary, and unrelated worktrees.
6. Report the PR URL, merge commit, fetched base ref and tip, removed path or precise skip reason, and primary checkout status. For a tracked task, use its tracker adapter under repository instructions and copy every reconciliation line; never hand-edit its ledger. Do not pull, merge, rebase, reset, stash, push, delete branches, or update protected branches as part of cleanup.
