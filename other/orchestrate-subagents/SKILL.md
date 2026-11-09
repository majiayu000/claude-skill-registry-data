---
name: orchestrate-subagents
description: Plan and coordinate parallel subagent lanes using Hephaera roles, durable task artifacts, and tool-specific execution guidance.
engines: [AGNOSTIC]
---

## When to use
Use when a user specifies an agent, developer, worker, or parallel execution count, or when `computer-science/project-manager` identifies work that can safely run in parallel.

Use before spawning subagents or delegating work so each lane has a resolved role, explicit ownership, dependencies, expected output, and verification evidence.

Do not use this task-backed lane workflow for active Brainstorm mode. `brainstorm-flow` owns its fixed main project-manager plus two read-only researcher team and keeps researcher reports ephemeral without `SUBAGENTS.md`.

## Output
- `../.hephaera/.cache/tasks/<task_name>/SUBAGENTS.md` lane plan
- requested and effective capacity
- lane IDs, role IDs, agent types, scopes, write sets, dependencies, outputs, and verification paths
- integration order and conflict risks
- subagent prompt text for each lane
- recorded lane result summaries after agents finish

## Notes
- The project-manager role owns lane decomposition and effective parallelism decisions.
- Resolve every lane role with `../commands/resolve-role.sh` before assigning work.
- Use `explorer` for read-only investigation lanes and `worker` for implementation lanes when Codex subagents are available.
- Worker lanes must have disjoint write sets. If safe disjoint ownership cannot be declared, keep the work local or sequential.
- Never delegate the immediate critical-path blocker when the main agent needs that result before it can continue.
- Keep Hephaera portable: if a tool has no subagent runtime, use the same lane plan as delegation guidance or sequential execution order.
- Brainstorm is the exception to portable fallback: if two researcher subagents are unavailable, preserve its active state and block idea processing instead of reducing or serializing the team.

## Subagent prompt template

```markdown
You are working as `<role-id>` on lane `<lane-id>`.

You are not alone in the codebase. Other agents or the main agent may be working in parallel. Do not revert edits made by others. Keep your work inside your assigned scope and adjust to compatible changes if you encounter them.

Scope:
- <files, module, or responsibility>

Write set:
- <paths this lane may edit, or none for read-only lanes>

Dependencies:
- <none or named blockers>

Expected output:
- <deliverable>

Verification:
- <commands, checks, artifacts, or review evidence>

Final response requirements:
- summarize what you did
- list files changed
- provide verification evidence
- call out blockers, conflicts, or residual risks
```

## Commands
../commands/create-subagent-plan.sh "<task_name>" ["agent_count"] [--dry-run]

../commands/validate-subagent-plan.sh "<task_name|path>"

../commands/record-subagent-result.sh "<task_name>" "<lane_id>" "<status>" "<summary_file>" [--dry-run]
