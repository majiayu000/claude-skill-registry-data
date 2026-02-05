---
name: vrau
description: Use when starting or resuming a vrau workflow - routes to correct phase
model: haiku
---

# Vrau Workflow

## ⚠️ CRITICAL SAFETY RULE ⚠️

**NEVER COMMIT TO MAIN BRANCH**

Before doing ANYTHING, check current branch:
```bash
git branch --show-current
```

**If on main/master:**
1. STOP immediately
2. Create a new branch OR use worktree
3. NEVER proceed with commits on main

**This is non-negotiable. No exceptions. Ever.**

## On Start
1. Scan `docs/designs/` for folders matching `YYYY-MM-DD-*`
2. If none: start new workflow (see below)
3. If one: auto-select, detect state, ask about worktree/branch (see Resuming Workflow below), invoke correct phase
4. If multiple: ask user which to resume (or start new, or delete old), then ask about worktree/branch (see Resuming Workflow below), invoke correct phase

## New Workflow Setup
1. Ask user for task description
2. Ask: Start from GitHub issue?
   - Yes → get issue number, set Doc Approach B
   - No → set Doc Approach A
3. (Optional) Ask: Local-only mode? → set Doc Approach C, create .no-commit.local
4. **Ask: Worktree or new branch?**
   - Worktree → use superpowers:using-git-worktrees
   - New branch → `git checkout -b <workflow-name>` and `git push -u origin <workflow-name>`
5. Update main first: `git checkout main && git pull`
6. Create worktree OR branch based on choice
7. Create folder `docs/designs/YYYY-MM-DD-<slug>/`
8. Create README.md with Doc Approach and issue number (if any)
9. Create execution-log.md (see format below)
10. Commit, push (skip if Doc Approach C)
11. Invoke vrau:brainstorm

## Resuming Workflow
When resuming an existing workflow:
1. Update main first: `git checkout main && git pull`
2. **Ask: Worktree or new branch?**
   - Worktree → use superpowers:using-git-worktrees
   - New branch → `git checkout -b <workflow-name>-<phase>` and `git push -u origin <workflow-name>-<phase>`
3. Create worktree OR branch based on choice
4. Proceed to invoke correct phase

**Why:** User must choose worktree/branch preference every time they resume work. Never assume.

## State Detection
Read `docs/designs/<workflow>/execution-log.md`:
- Phase: brainstorm | plan | execute
- Status of current phase

Fallback if no execution log - check files:
- Only README.md → brainstorm
- Has design/*.md, no plan/*.md → plan
- Has plan/*.md → execute
- If unclear → ASK USER

## Execution Log Format
```
# Execution Log: <workflow>

## Workflow Context
- **Task:** <description>
- **Phase:** brainstorm | plan | execute
- **Branch:** <branch name>
- **Issue:** #<number> or (none)

## Status
- **Current Step:** <step number and name>
- **Last Updated:** <timestamp>
```

## Routing
- Brainstorm needed → invoke vrau:brainstorm
- Plan needed → invoke vrau:plan
- Execute needed → invoke vrau:execute
