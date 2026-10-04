---
name: codex-orchestrate
description: Coordinate independent work with Codex subagents. Use for requests to orchestrate a task, run a team, or delegate parallel work in Codex, with personal model defaults for scouts and workers.
---

# Codex Orchestrate

Call the Skill tool with `orchestrate`. If the tool cannot resolve it, read the [shared coordination policy](../orchestrate/SKILL.md). It owns role preferences, assignment ownership, and completion criteria; this adapter owns Codex execution.

Before dispatching, read [Codex tool mechanics](references/codex-tools.md). Use the current task's Codex subagent tools. Check supported model settings and live capacity. If subagent tools are unavailable, continue directly and disclose the limitation.

When a child's model differs from its parent's, start it with fresh context; do not fork conversation history. For the same model, default to fresh context and fork only when prior reasoning materially helps. Fresh-context briefs must carry the decisions the child cannot see. See the tool reference for exact fork settings and inheritance constraints.

Persistence means continuing the child's own conversation, not repeatedly forking the coordinator. Reuse the Astra advisor's returned ID for related follow-ups.

Allow nested delegation only when the live contract permits it and a concrete subtask has an explicit scope and capacity budget.

Let agents send useful discoveries directly to named teammates, copying scope or dependency changes back to you. Resolve conflicting decisions and ownership centrally.

Mechanics checked against the live Codex contract and [official subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) on 2026-09-07.
