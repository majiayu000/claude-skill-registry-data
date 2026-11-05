---
name: subagent-review
description: Runs swarm_search, swarm_run, or run_judge_panel via the synthet-agent-swarm MCP server. Use for a read-only external review, a judge panel, harness selection, or /swarm.
capability: "Run swarm_search, swarm_run, or run_judge_panel through the synthet-agent-swarm MCP server."
side_effect_level: external_export
approval_required: true
requires_tools: "MCP server synthet-agent-swarm: swarm_search, swarm_run, run_judge_panel"
output_schema: "Markdown summary of harness results and agreement."
risk_class: high
---

# Subagent review (MCP)

Run external judges **through the synthet-agent-swarm MCP server**. Do not spawn `codex`, `agy`, `claude`, or `agent` in the terminal.

Writes stay off. Never set `allowWrites: true`.

## Prerequisites

- The `synthet-agent-swarm` package is built: `npm run build` in `agent-orchestrator/` of that checkout. The launch file is `agent-orchestrator/dist/index.js`.
- The user MCP server named `synthet-agent-swarm` is enabled and the client has been reloaded.

## Steps

1. Resolve the MCP server whose `serverName` is `synthet-agent-swarm`. Read the schemas for `swarm_search`, `swarm_run`, and `run_judge_panel`. The field contract is `docs/api.md` in the synthet-agent-swarm checkout. This skill's [references/mcp-tools.md](references/mcp-tools.md) is the short form.
2. Call `swarm_search`. Show id, command, available, and transports. A query of `gemini` also returns `agy`. `agent` is the cursor row.
3. Call `swarm_run` for a review or one judgement. Omit `harnesses` for every available harness. Pass `model` only when the user names one. Set `dryRun: true` when the user says dry run or you are checking setup.
4. Call `run_judge_panel` for a frozen manifest. Blind panels reject `extraContext`. The tool does not call Jev.
5. Read `.agent-runs/` and summarize. Code-review findings use severity blocker, high, medium, low, or nit. Agreement is not a human label. Do not apply patches unless the user asks.

Old names `detect_subagents`, `run_subagent`, and `run_judge_swarm` still work and return the previous JSON shape. New calls use `swarm_search` and `swarm_run`.

## Errors

| Situation | Action |
|---|---|
| `unknown_harness` | Show `next_steps` from `swarm_search` |
| `model_unsupported` | Retry with the harness ids in `next_steps`, or omit `model` |
| `harness_unavailable` | Report the search row. Do not install adapters with `npx` |
| MCP server missing | Build `agent-orchestrator` and reload the user MCP entry |

## Related

- Command: `/swarm`
- Subagent: `external-swarm`
- Reference: [references/mcp-tools.md](references/mcp-tools.md)
