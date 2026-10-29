---
name: speckit-worktree-list
description: Show all active worktrees with feature status and spec artifact summary
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: worktree:commands/speckit.worktree.list.md
---

# List Worktrees

Show all active git worktrees with their feature branch status, spec artifact availability, and task completion progress — a dashboard for parallel feature development.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). The user may request a specific format (e.g., "compact") or filter (e.g., "stale only").

## Prerequisites

1. Verify a spec-kit project exists by checking for `.specify/` directory
2. Verify git is available and the project is a git repository

## Outline

1. **List all worktrees**: Run `git worktree list` to get all active worktrees:
   - Parse the output to extract path, branch, and HEAD commit for each worktree
   - Identify the main working directory vs. feature worktrees
   - Check which worktrees are in `.worktrees/` directory

2. **Gather feature status**: For each worktree, check its spec-kit state:
   - **Branch name**: The feature branch checked out in this worktree
   - **Spec artifacts**: Which files exist (spec.md, plan.md, tasks.md, research.md)
   - **Task progress**: If tasks.md exists, count `[x]` vs `[ ]` items
   - **Last activity**: Most recent commit date on the branch
   - **Merge status**: Whether the branch has been merged into main/master
   - **Staleness**: Whether any artifacts have `⚠️ **STALE**` markers

3. **Classify worktree status**:

   | Status | Condition |
   |--------|-----------|
   | ✅ Active | Recent commits (within 7 days), unmerged |
   | 🟡 Idle | No recent commits (7-30 days), unmerged |
   | ⚠️ Stale | No commits for 30+ days, unmerged |
   | ✅ Merged | Branch merged into main/master |
   | ❌ Orphaned | Branch deleted but worktree still exists |

4. **Output dashboard**:

   ```markdown
   # Active Worktrees

   | # | Branch | Path | Status | Artifacts | Tasks | Last Activity |
   |---|--------|------|--------|-----------|-------|---------------|
   | 1 | 003-user-auth | .worktrees/003-user-auth/ | ✅ Active | spec ✅ plan ✅ tasks ✅ | 12/18 (67%) | 2 hours ago |
   | 2 | 004-chat-system | .worktrees/004-chat-system/ | 🟡 Idle | spec ✅ plan ✅ tasks ❌ | — | 12 days ago |
   | 3 | 005-api-gateway | .worktrees/005-api-gateway/ | ✅ Merged | spec ✅ plan ✅ tasks ✅ | 8/8 (100%) | 3 days ago |

   ## Summary
   - **Total worktrees**: 3 (+ main working directory)
   - **Active**: 1
   - **Idle**: 1
   - **Ready to clean**: 1 (merged)

   ## Recommended Actions
   - Run `/speckit.worktree.clean` to remove the merged worktree (005-api-gateway)
   - Resume work on 004-chat-system or run `/speckit.tasks` to generate tasks
   ```

5. **Report**: Output the dashboard. Do not modify any files — this command is read-only.

## Rules

- **Read-only** — this command never modifies any files or worktrees
- **Always include main** — show the main working directory as the first entry for context
- **Show all worktrees** — include active, idle, stale, merged, and orphaned
- **Accurate progress** — task counts must reflect actual `[x]` and `[ ]` in tasks.md
- **Recommend cleanup** — always suggest cleaning merged or orphaned worktrees