---
name: liku-orchestrator
description: Path-grounded multi-agent orchestration using the Liku directory hierarchy (skills.xml inheritance, todo.md + LikuErrors.md audit trail, SQLite memory). Use when you need to initialize Liku, generate an agent bundle for a specific Liku/* residence path, or expose Liku as an MCP server for Gemini-CLI, Claude Code, Copilot-CLI, or ChatGPT Codex.
---

# Liku Orchestrator

## What to do

- Treat `Liku/` as the canonical source of truth for agent identity, scope, and state.
- Load skills by inheriting `skills.xml` from the agent residence directory up to `Liku/`.
- Mirror progress to `todo.md`; mirror failures to `LikuErrors.md`.

## Quick start (repo-local)

- Initialize: run `liku init`
- Start MCP server (stdio): run `liku-mcp`
- Generate a bundle for a residence path:
  - Call MCP tool `liku.invoke` with `agentResidence` like `Liku/specialist/ts` and a JSON `task`.

## Notes

- If an action would require root-only privilege, return an escalation request as structured output; do not assume interactive consent unless the client supports it.

