---
name: backlog-update
description: Reminder to update backlog.org before commits or when finishing significant work. Use before committing changes, after completing implementation from plan mode, or when wrapping up a work session. This skill ensures the project's task tracking in backlog.org stays current with actual progress. Trigger when about to commit, exiting plan mode, or when user says "done", "let's commit", "wrap up", or similar.
---

# Backlog Update Reminder

This skill reminds you to update backlog.org before commits or when finishing significant work. The backlog should reflect reality BEFORE the commit is made.

## When to Offer This Workflow

**Trigger conditions:**
- About to run `git commit` or create a commit
- Exiting plan mode after completing implementation
- User says "done", "finished", "let's commit", "wrap up"
- Completing a significant piece of work

**Initial check:**
Before proceeding with the commit, read backlog.org's Current WIP section to see what's in Active.

## Workflow

### 1. Check Active Tasks

Read the `* Current WIP` > `** Active` section in backlog.org.

Look for tasks related to the work just completed.

### 2. Update Progress Notes

If work relates to an Active task, add progress notes under that task:

```org
*** TODO [PROJECT-NNN-XX] Task title
:PROPERTIES:
:SOURCE: [[file:...][...]]
:END:

Previous notes...

[YYYY-MM-DD] What was done, what remains.
```

### 3. Assess Task Status

After adding notes, consider:

- **Still in progress?** Leave as TODO/WIP, notes are sufficient
- **Blocked?** Suggest running `/task-hold <id> <reason>`
- **Complete?** Suggest running `/task-complete <id> [version]`

Do NOT mark complete automatically - that's an explicit user action via `/task-complete`.

### 4. Check CHANGELOG.md

If significant user-facing changes were made:

- Read `CHANGELOG.md` if it exists
- Check if the change is already documented under `## [Unreleased]`
- If not, suggest adding an entry:
  - **Added** - New features
  - **Changed** - Changes to existing functionality
  - **Fixed** - Bug fixes
  - **Removed** - Removed features

### 5. Update Handoff Notes

If stopping work mid-task:

- Update `:HANDOFF:` property with context for next session
- Include: what was tried, where stuck, what to try next

### 6. Then Commit

Only after backlog.org and CHANGELOG.md are updated, proceed with the commit.

## Related Commands

| Command | When to suggest |
|---------|-----------------|
| `/task-complete <id>` | Task is fully done |
| `/task-hold <id> <reason>` | Task is blocked |
| `/task-queue <id>` | Need to add a task to Active |

## Example

```
User: "Let's commit these changes"

Claude: "Before committing, let me check backlog.org...

I see [DAB-001-01] is in Active. We just implemented the directory
structure. Should I:
1. Add progress notes (still more to do)
2. Mark complete with /task-complete DAB-001-01
3. Proceed without updating (unrelated work)"
```
