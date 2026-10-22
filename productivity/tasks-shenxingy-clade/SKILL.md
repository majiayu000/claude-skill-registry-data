---
name: tasks
description: Coordinate dependency-aware project tasks across independent Codex, Claude Code, Kimi and human sessions using Beads. Use for shared plans, claiming work, task handoffs, acceptance and agent monitoring snapshots.
---

# Shared tasks

Run the workflow in `prompt.md` using this skill's `scripts/tasks.py`.
Beads holds task state; Git holds code; Markdown explains decisions and context.
The helper does not launch agents or models. Each runtime uses it directly.

- For first setup or moving to a server, read [service setup](references/service.md).
- For planning, use [the plan example](references/plan.json).
- For Web monitoring integration, read [the observation contract](references/monitoring.md).

Use one live backend per project. Give each independent execution a fresh
session ID. Readiness and claims come from Beads; a Markdown checkbox, local
Git branch or old handoff is not a current ownership grant.

Task acceptance and Git publication are separate. Preserve existing repository
verification, review and delivery authority. Only record checks actually run.
