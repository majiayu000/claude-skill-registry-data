---
name: catchup
description: Rebuilds session context after a clear by reading git history, plans, and beads state. Triggers on 'catch up'.
---

# Context Recovery Skill

You are resuming work after a session clear. Your job is to rebuild full working context from git history, the latest plan, and beads issue state, then produce a visible briefing and internalize everything needed to continue.

## Step 1: Branch Check

If not on main, store the merge-base SHA and continue. 

Run these commands:
```bash
git branch --show-current
git merge-base HEAD main 2>/dev/null
```

## Step 2: Git History

If on main (no merge-base range), use the last ~20 commits:
```bash
git log --oneline -20
git diff --stat HEAD~20..HEAD
git diff --stat          # uncommitted changes
git diff --cached --stat # staged changes
```

If on a feature branch, use the merge-base range:
```bash
git log --oneline <merge-base>..HEAD
git diff --stat <merge-base>..HEAD
git diff --stat          # uncommitted changes
git diff --cached --stat # staged changes
```

Then **read every file** that appears in the diff stats (both committed and uncommitted). Build a mental model of what changed and why.

## Step 3: Latest Plan

Find the most recently modified file in `~/.claude/plans/`:
```bash
ls -t ~/.claude/plans/ | head -1
```

Read that file in full. Only include the Active Plan section in the briefing if the plan is relevant to the current repository (e.g., references the same project, codebase, or directory). Skip it if the plan is for a different project.

## Step 4: Beads State

Run these commands (skip if `bd` is not available):
```bash
bd list --status=in_progress
bd ready
```

Note which issues are actively being worked and which are unblocked and available.

## Step 5: Produce Briefing

Output a concise visible briefing in this format:

```
## Catchup Briefing

**Branch:** <branch-name> (<N> commits ahead of main)

### Recent Changes
- <1-line summary per commit, grouped by theme>

### Uncommitted Work
- <files with uncommitted/staged changes, or "Clean working tree">

### Active Plan
- <plan title + key status from the plan file>

### Beads Status
- **In Progress:** <issue titles>
- **Ready:** <issue titles>

### Suggested Next Step
> <concrete next action based on plan state + beads + uncommitted work>
```

After outputting the briefing, you now have full context. Continue working as if you never lost the session.
