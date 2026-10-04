---
name: forge-roles
description: Reference definitions for the Agent Forge orchestration roles (lead, worker, planner, evaluator). Use when coordinating multi-agent Forge work or when you need one role's responsibilities and constraints.
---

# Forge Roles

The Agent Forge harness splits multi-agent work into distinct roles. These persona
definitions come verbatim from the Claude Code harness (`.claude/agents/`) and are
bundled here so Codex can read them as reference.

- [evaluator](references/evaluator.md)
- [lead](references/lead.md)
- [planner](references/planner.md)
- [worker](references/worker.md)

Read the relevant role file before acting in that capacity. The Lead never writes
production code; Workers implement in scope; the Planner expands specs; the Evaluator
judges output at a model tier >= the tier that produced it.
