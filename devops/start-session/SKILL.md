---
name: start-session
description: Start a Nativly work session - recap where we left off, propose today's goal, and start building.
disable-model-invocation: true
argument-hint: "[minutes available, e.g. 45]"
---

Start a work session. Time available: $ARGUMENTS (assume 45 minutes if empty).

1. Read docs/progress/PROGRESS.md. Run `git status`, `git log --oneline -5`,
   `gh run list --limit 3`, and check Docker is up (`docker info`; if not, `colima start`).
2. In 2–3 lines: current phase, last thing finished, anything uncommitted, red CI.
3. Propose ONE goal that fits the time and the current phase: what gets built and how it
   will be verified. Then start building it.
