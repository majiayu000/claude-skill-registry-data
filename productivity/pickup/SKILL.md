---
name: pickup
description: Resume an existing AgentBoard phase-based project, recover context, and claim the next task. Use when the user wants Codex to continue a prior AgentBoard session.
---

# Pickup

Use this skill to resume existing project work.

## Workflow

1. Load the `agentboard` skill first.
2. Verify connectivity to AgentBoard.
3. List projects and identify the target project.
4. Fetch project details.
5. Check for `in-progress` tasks first.
6. If there is no active task, claim the next task.
7. If the task is a milestone, fetch the linked document.
8. Read recent activity log entries to recover context.
9. Summarize the current project state and begin work.

## Rules

- Prefer resuming an already assigned `in-progress` task over claiming a new one.
- If there are multiple candidate projects, ask the user rather than guessing.
- Show recent blockers or rejection feedback before proceeding.
