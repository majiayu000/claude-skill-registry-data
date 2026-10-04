---
name: wrap-up
description: Save progress and leave a clean AgentBoard handoff for the next Codex session. Use when the user wants to end a session without losing context.
---

# Wrap-Up

Use this skill at the end of a working session.

## Workflow

1. Find the active project and any `in-progress` tasks.
2. For each active task, append a useful progress note covering:
   - what changed
   - what remains
   - blockers or decisions
   - files touched when code changed
3. If work is actually complete:
   - implementation tasks go to review with notes and acceptance criteria
   - milestone work is submitted through the linked document flow
4. Add a project log entry summarizing the session.
5. Fetch final project state.
6. Present a handoff summary for the next agent.

## Rules

- Do not mark incomplete work as complete.
- Notes should capture decisions and handoff context, not empty status filler.
