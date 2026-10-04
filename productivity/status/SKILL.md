---
name: status
description: Show read-only status for an AgentBoard phase-based project. Use when the user wants phase, task, blocker, or next-step visibility without mutating anything.
---

# Status

Use this skill for project situational awareness.

## Workflow

1. Load the `agentboard` skill first.
2. Verify connectivity.
3. List projects.
4. Fetch the selected project's details and tasks.
5. Present:
   - phase number and phase name
   - task counts by status
   - blocked or review-pending work
   - next likely action

## Rules

- Do not claim a task.
- Do not mutate project state.
- If there are no projects, tell the user to start with `kickoff`.
