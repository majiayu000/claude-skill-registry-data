---
name: tk-ready
description: Show ready-to-work tasks with no blockers. Use when user says /tk:ready or asks what to work on, what's next, available tasks, or unblocked tasks.
---

# Show Ready Tasks

Display tasks that are ready to work on (not blocked, not in progress, not done).

## Instructions

1. Use the `tk_list` MCP tool with `status: "ready"` filter
2. Sort by priority (critical first, then high, normal, low, backlog)
3. Highlight the top task as the suggested next action
4. Show task ID, description, and priority level

## Output Format

```
## Ready to Work (X tasks)

**Suggested next:** [highest-priority-task-id] - Description

Other ready tasks:
- [task-id] Description (priority)
- [task-id] Description (priority)
```

## Priority Levels

- 0 = critical (urgent)
- 1 = high (important)
- 2 = normal (default)
- 3 = low (when time permits)
- 4 = backlog (future consideration)

## Notes

- If no ready tasks exist, check for blocked tasks and explain what's blocking progress
- Suggest using `tk task start <id>` to begin working on a task
