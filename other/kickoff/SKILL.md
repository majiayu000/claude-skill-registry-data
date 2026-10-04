---
name: kickoff
description: Start or select an AgentBoard phase-based project, verify connectivity, and claim the first actionable task. Use when the user wants to begin a structured AgentBoard project from Codex.
---

# Kickoff

Use this skill to start a fresh AgentBoard project session in Codex.

## Workflow

1. Load the `agentboard` skill first for setup, auth, and state-machine rules.
2. Verify the AgentBoard MCP is reachable.
3. List existing projects.
4. If a project already exists, ask the user which project to work on.
5. If no project exists, collect:
   - project name
   - project type: `new_feature`, `refactor`, `bug_fix`, `migration`, or `integration`
   - idea description
   - optional target project path
6. Create the project if needed.
7. Claim the first task with `agentboard_get_next_task`.
8. Summarize:
   - project name
   - current phase
   - current task
   - whether a linked milestone document is present
   - immediate next step

## Rules

- Stop if the cloud service is unhealthy.
- Do not guess the target project path if the user has multiple plausible repos open.
- If the claimed task is a milestone, read the linked document before starting work.
