---
name: sweep
description: Audit a codebase, write a findings document, and convert grouped issues into AgentBoard workspace cards. Use when the user wants a structured cleanup backlog before implementation begins.
---

# Sweep

Use this skill to turn codebase problems into an AgentBoard board.

## Workflow

1. Load `codebase-sweep` and `agentboard`.
2. Select or create the target app and board.
3. Confirm the target codebase path.
4. Map the codebase structure and supporting configs.
5. Read the codebase systematically using the `codebase-sweep` methodology.
6. Write findings to `docs/sweep/YYYY-MM-DD-findings.md` inside the target project.
7. Group findings into actionable issue clusters.
8. Create one workspace card per group, with priority and dependencies.
9. Summarize the findings document and the resulting board.

## Rules

- Discovery only. Do not fix code during the sweep.
- Findings must include concrete file references.
- Group cards by problem pattern, not by arbitrary directory.
