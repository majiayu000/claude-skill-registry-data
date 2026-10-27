---
name: resume
description: Resume a previous session from claude/tasks/todo.md. Use at the start of a new session to restore context and continue where you left off.
---

# Resume Skill

Restore session context and continue previous work.

## Protocol

### 1. Read session state
Read `claude/tasks/todo.md` — the source of truth for current task state.

### 2. Read accumulated wisdom
Read `claude/tasks/lessons.md` — relevant past lessons (tail -40 for recent ones).

### 3. Read error history (if touching code)
Read `claude/tasks/CLAUDE_ERRORS.md` — known bugs in affected areas.

### 4. Reconstruct context
From todo.md, identify:
- Task title and goal
- Completed steps (checked items)
- Next action (first unchecked item)
- Branch name (if noted)
- Which claude/*.md files were loaded

### 5. Re-read domain docs
If the task involves specific areas, re-read the relevant `claude/*.md` from the lookup table in CLAUDE.md.

### 6. Check git state
```bash
git branch --show-current 2>/dev/null
git status --short 2>/dev/null | head -20
```
Verify you're on the right branch and no unexpected changes are staged.

### 7. Report to user
Brief summary:
- "Resuming task: [title]"
- "Completed: [N] steps"
- "Next action: [first unchecked step]"
- "Branch: [branch name]"

### 8. Proceed with next action
Do NOT re-do completed steps. Start from the first unchecked item.

## Rules
- NEVER re-implement something already marked complete in todo.md
- If todo.md is empty or missing: ask the user what to work on
- If branch is different from what's noted in todo.md: flag the discrepancy before proceeding
