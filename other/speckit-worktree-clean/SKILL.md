---
name: speckit-worktree-clean
description: Remove stale or merged worktrees and reclaim disk space
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: worktree:commands/speckit.worktree.clean.md
---

# Clean Worktrees

Remove worktrees for branches that have been merged or are no longer needed. Safely cleans up `.worktrees/` directory entries and reclaims disk space.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). The user may specify a branch name to clean (e.g., "005-api-gateway"), "merged" to clean all merged worktrees, or "all" to clean everything.

## Prerequisites

1. Verify a spec-kit project exists by checking for `.specify/` directory
2. Verify git is available and the project is a git repository
3. Verify `.worktrees/` directory exists and contains worktrees

## Outline

1. **Scan worktrees**: List all worktrees and classify them:
   - **Merged**: Branch has been merged into main/master — safe to remove
   - **Orphaned**: Branch has been deleted but worktree still exists — safe to remove
   - **Stale**: No commits for 30+ days, not merged — warn before removing
   - **Active**: Recent activity, not merged — refuse to remove unless forced

2. **Build cleanup plan**: Based on user input, determine what to remove:

   | User Input | Action |
   |-----------|--------|
   | Specific branch name | Remove that worktree only (with confirmation) |
   | `merged` | Remove all merged worktrees |
   | `stale` | Remove all stale worktrees (30+ days inactive) |
   | `all` | Remove all worktrees except main (with strong warning) |
   | No input | Remove merged and orphaned only (safest default) |

3. **Present cleanup plan**: Show a preview before making any changes:

   ```markdown
   # Worktree Cleanup Plan

   | # | Branch | Status | Action | Disk Size |
   |---|--------|--------|--------|-----------|
   | 1 | 005-api-gateway | ✅ Merged | Remove | ~45 MB |
   | 2 | 002-old-feature | ❌ Orphaned | Remove | ~32 MB |
   | 3 | 004-chat-system | 🟡 Idle | Keep (not merged) | ~41 MB |

   **Will remove**: 2 worktrees (~77 MB)
   **Will keep**: 1 worktree
   ```

4. **Confirm with user**: Ask for explicit confirmation before proceeding. Removing worktrees with uncommitted changes is destructive.

5. **Check for uncommitted changes**: Before removing each worktree:
   - Run `git -C .worktrees/{branch}/ status --porcelain` to check for uncommitted work
   - If uncommitted changes exist, **warn the user** and skip unless they confirm
   - List the uncommitted files so the user knows what would be lost

6. **Execute cleanup**: For each worktree to remove:
   - Run `git worktree remove .worktrees/{branch-name}` to safely remove
   - If the worktree is locked, run `git worktree unlock .worktrees/{branch-name}` first
   - Remove the entry from `.worktrees/` directory
   - Run `git worktree prune` after all removals to clean up stale references

7. **Report**: Output a summary:
   - How many worktrees were removed
   - How much disk space was reclaimed (approximate)
   - How many worktrees remain
   - Any worktrees that were skipped (with reason)

## Rules

- **Never remove without confirmation** — always show the plan first and wait for approval
- **Never remove the main working directory** — only clean feature worktrees in `.worktrees/`
- **Warn about uncommitted changes** — refuse to remove worktrees with uncommitted work unless user explicitly confirms
- **Safe defaults** — with no input, only remove merged and orphaned worktrees
- **Prune after cleanup** — always run `git worktree prune` to clean up stale administrative files
- **Never delete branches** — removing a worktree does not delete the git branch, only the working directory