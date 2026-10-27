---
name: checkpoint
description: Save session state before context gets full or before ending. Writes current task state, branch, and loaded docs to claude/tasks/todo.md so the next session can resume cleanly.
---

# Checkpoint Skill

Save session state for clean handoff to the next session.

## When to use
- Context window is getting full (preemptively)
- Before ending a session with work in progress
- Before a long-running operation that might reset context

## Protocol

### 1. Record current state in claude/tasks/todo.md

```markdown
# Task: <current task title>
_Checkpointed: {{DATE}}_

**Goal:** <what done looks like>
**Branch:** <output of: git branch --show-current>
**Loaded docs:** claude/architecture.md, claude/rules.md, [others read this session]

## Completed Steps
- [x] 1. <step>
- [x] 2. <step>

## Remaining Steps
- [ ] 3. <next action — be specific>
- [ ] 4. <step>

## Next Action
> <Single most important thing to do when resuming>

## Uncommitted Files
<output of: git status --short | head -20>

## Notes
<Any constraints, blockers, or decisions made this session>
```

### 2. Update claude/tasks/lessons.md
If any corrections or new patterns were discovered this session, add them NOW.

### 3. Confirm to user
"Session state saved to claude/tasks/todo.md. To resume: use `/resume`."

## Rules
- NEVER checkpoint without writing the Next Action explicitly
- NEVER skip lessons.md update if corrections were made
- Checkpoint early — better to checkpoint too often than to lose context
