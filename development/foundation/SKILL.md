---
name: foundation
description: Build a spec and seed AgentBoard workspace cards from it. Use when the user wants a structured plan before implementation or wants to turn a problem statement into an orchestrated board.
---

# Foundation

Use this skill to turn a goal into a spec plus workspace cards.

## Workflow

1. Load the `agentboard` skill first.
2. Select or create the target app.
3. Select or create the target board.
4. Ask clarifying questions one at a time until the scope is concrete.
5. Research the codebase with companion tools when needed.
6. Write a spec to `docs/specs/YYYY-MM-DD-<topic>.md`.
7. Show the spec to the user for approval before creating cards.
8. Create one backlog card per major chunk of work.
9. Summarize the created app, board, spec path, and cards.

## Rules

- The spec defines what needs to happen, not detailed implementation steps.
- Each card should be a focused unit of work that one agent can plan and execute.
- Do not start orchestration in the same session unless the user explicitly asks.
