---
name: speckit-worktree-create
description: Spawn an isolated git worktree for a new or existing feature branch
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: extension:worktree
---

# Worktree Create Skill

# Create Worktree

Spawn an isolated git worktree for a feature branch so you can work on multiple features in parallel without switching branches. Each worktree gets its own directory with a full working copy.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). The user may specify a branch name (e.g., "003-user-auth") or "current" to create a worktree for the current branch.

## Prerequisites

1. Verify a spec-kit project exists by checking for `.specify/` directory
2. Verify git is available and the project is a git repository
3. Check that the target branch exists (local or remote)

## Outline

1. **Determine target branch**: Identify which feature branch to create a worktree for:
   - If user specifies a branch name, use that
   - If user says "current", use the current branch
   - If no input, check for the most recently created feature branch
   - Validate the branch exists in git

2. **Choose worktree location**: Determine the worktree directory path:
   - Default location: `.worktrees/{branch-name}/` relative to the repository root
   - If `.worktrees/` directory does not exist, create it
   - Add `.worktrees/` to `.gitignore` if not already present
   - Verify the worktree does not already exist for this branch

3. **Create the worktree**: Execute the git worktree command:
   - Run `git worktree add .worktrees/{branch-name} {branch-name}`
   - If the branch is remote-only, track it: `git worktree add .worktrees/{branch-name} -b {branch-name} origin/{branch-name}`
   - Verify the worktree was created successfully

4. **Verify spec artifacts**: Check that the worktree has access to spec artifacts:
   - Confirm `specs/{branch-name}/` directory exists in the worktree
   - List available artifacts (spec.md, plan.md, tasks.md)
   - Note any missing artifacts

5. **Report**: Output a summary:

   ```markdown
   # Worktree Created

   | Field | Value |
   |-------|-------|
   | **Branch** | {branch-name} |
   | **Worktree path** | .worktrees/{branch-name}/ |
   | **Spec artifacts** | spec.md ✅, plan.md ✅, tasks.md ❌ |

   ## Next Steps
   - `cd .worktrees/{branch-name}/` to work in the isolated worktree
   - Run `/speckit.implement` inside the worktree to build the feature
   - Run `/speckit.worktree.list` to see all active worktrees
   - When done, run `/speckit.worktree.clean` to remove the worktree
   ```

## Rules

- **Never modify the main working directory** — worktrees are created in `.worktrees/` only
- **Always update .gitignore** — ensure `.worktrees/` is ignored to prevent accidental commits
- **One worktree per branch** — refuse to create a duplicate worktree for the same branch
- **Validate branch exists** — do not create worktrees for non-existent branches
- **Preserve existing worktrees** — never overwrite or remove an existing worktree
