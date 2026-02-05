---
name: hack-cli
description: >
  Use the hack CLI for local dev environments (docker compose, logs, run commands) and agent integration setup.
  Trigger when asked to start/stop services, open project URLs, inspect logs, run commands in services, manage
  branch instances, or configure agent integrations (Cursor/Claude/Codex/MCP). Prefer CLI over MCP when shell
  access is available.
---

# hack CLI

Use hack CLI as the primary interface for local dev.

## Quick Start

- Start services: `hack up --detach`
- Open app: `hack open --json`
- Tail logs: `hack logs --pretty`
- Snapshot logs: `hack logs --json --no-follow`
- Run commands: `hack run <service> <cmd...>`
- Stop services: `hack down`

## Branch Instances

Use branch instances to run parallel environments:

- `hack up --branch <name> --detach`
- `hack open --branch <name>`
- `hack logs --branch <name>`
- `hack down --branch <name>`

## Logs

- Loki history: `hack logs --loki --since 2h --pretty`
- Filter services: `hack logs --loki --services api,web`
- Force compose logs: `hack logs --compose`

## Project Targeting

- Run from repo root when possible.
- Otherwise use `--project <name>` or `--path <repo-root>`.
- List projects: `hack projects --json`.

## Daemon (optional)

- Start for faster JSON status/ps: `hack daemon start`
- Check status: `hack daemon status`

## Agent Setup

- Cursor rules: `hack setup cursor`
- Claude hooks: `hack setup claude`
- Codex skill: `hack setup codex`
- Init prompt: `hack agent init` (use --client cursor|claude|codex to open)
- Init patterns: `hack agent patterns`
- MCP (no shell only): `hack setup mcp`
