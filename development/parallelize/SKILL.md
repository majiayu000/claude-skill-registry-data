---
name: parallelize
description: Create isolated git worktree, open new iTerm2 window with Claude Code, and spawn a task agent there for parallel work. Use when the user says "parallelize" followed by a task description, or asks to work on something in parallel.
allowed-tools: Bash, Task
---

# Parallelize Work in Git Worktree

This Skill sets up parallel work sessions using git worktrees and new terminal windows.

## Instructions

When the user says "parallelize: {task}" or asks to work on something in parallel:

### Step 1: Extract Task Description
Parse the task description from the user's message.

### Step 2: Suggest Branch Name
Based on the task description, suggest a branch name using conventional commit format:
- `chore/` - maintenance, cleanup, dependencies
- `feature/` - new functionality
- `fix/` - bug fixes
- `refactor/` - code restructuring

Keep branch name concise (under 50 characters).

### Step 3: Create Git Worktree
Execute these commands:

```bash
REPO_NAME=$(basename $(git rev-parse --show-toplevel))
BRANCH_NAME="suggested-branch-name"
WORKTREE_PATH="$HOME/Development/git-worktrees/${REPO_NAME}_${BRANCH_NAME}"

mkdir -p "$HOME/Development/git-worktrees"
git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"
```

### Step 4: Open iTerm2 with Claude Code and Send Task
Launch a new iTerm2 window with Claude Code in the worktree and automatically send the task:

```bash
osascript -e "tell application \"iTerm\"
    create window with default profile
    tell current session of current window
        write text \"cd $WORKTREE_PATH\"
        write text \"claude --dangerously-skip-permissions\"
        delay 5
        write text \"$TASK_DESCRIPTION\"
    end tell
end tell"
```

This will:
1. Open new iTerm2 window
2. Navigate to the worktree
3. Start Claude with permissions bypassed
4. Wait 5 seconds for Claude to fully load
5. Automatically send the task description to Claude

### Step 5: Inform User
Tell the user what happened:

```
✅ Parallel work session created
📍 Worktree: {WORKTREE_PATH}
🌿 Branch: {BRANCH_NAME}
🪟 New iTerm2 window opened with Claude Code
📋 Task automatically sent: {TASK}

The new Claude session is now working on the task independently.
You can continue working here while it runs in parallel.

When the parallel work is complete, you can:
1. Review changes: cd {WORKTREE_PATH} && git diff
2. Merge branch: git merge {BRANCH_NAME}
3. Clean up: git worktree remove {WORKTREE_PATH}
```

## Cleanup After Parallel Work

When the parallel work is done, clean up the worktree:

```bash
# Make sure you're not in the worktree directory
cd /Users/ericpardee/Development/bitbucket.org/americor/crm

# Remove the worktree
git worktree remove ~/Development/git-worktrees/{repo}_{branch}
```

## Examples

### Example 1: Simple parallel task
User: "parallelize: reduce repo size"

Actions:
1. Create branch: chore/reduce-repo-size
2. Worktree: ~/Development/git-worktrees/crm_chore/reduce-repo-size
3. Open new iTerm2 with Claude
4. Wait 5 seconds for Claude to load
5. Automatically send task: "reduce repo size"
6. Inform user that parallel session is working

### Example 2: Feature work
User: "Can you parallelize adding dark mode?"

Actions:
1. Create branch: feature/add-dark-mode
2. Worktree: ~/Development/git-worktrees/crm_feature/add-dark-mode
3. Open new iTerm2 with Claude
4. Wait 5 seconds for Claude to load
5. Automatically send task: "adding dark mode"
6. Inform user that parallel session is working

## Troubleshooting

### iTerm2 doesn't open
- Check if iTerm2 is installed
- Verify iTerm2 is in /Applications/
- Try manually: `open -a iTerm`

### Worktree creation fails
- Check if branch already exists: `git branch -a | grep branch-name`
- Check if worktree path already exists: `ls ~/Development/git-worktrees/`
- Remove existing worktree first: `git worktree remove path`

### Claude doesn't start in new window
- Verify claude is in PATH: `which claude`
- Try starting Claude manually in the worktree directory
- Check Claude Code installation

### Task doesn't get sent automatically
- The delay might be too short for Claude to fully load
- Increase the delay in Step 4 from 5 to 7-10 seconds
- Check if Claude is fully loaded before the task is sent
- Manually paste the task if auto-send fails
