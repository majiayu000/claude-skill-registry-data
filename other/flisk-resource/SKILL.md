---
name: flisk-resource
description: Add one service to an existing Flisk project with `flisk resource <name> --type frontend|backend|worker|agent|mcp --stack <stack>`, or wrap an existing Dockerfile or image with `--type bring-your-own`. Use when the user asks to add a service, website, agent, MCP tools server, worker or backend. For a whole new app from a plain request, use flisk-build; to start it, use flisk-up.
license: MIT
compatibility: Requires the flisk CLI. Does not deploy.
metadata:
  author: flisk-sh
  version: "1.0"
---

# Flisk resource

Create services with the CLI so each one gets a valid `service.json` and the right runtime contract. Do not hand-write container manifests.

## Workflow

1. Choose the type: `frontend` (website), `backend` (HTTP API), `worker` (background jobs), `agent` (its own `/health`, `/ready`, and `x-session-id` routing), `mcp` (tools server), `database` (the project's Postgres: a `service.json` only, which services name in `dependsOn`), or `bring-your-own` (an existing Dockerfile with `--dockerfile`, or an image with `--image`).
2. Create it: `flisk resource <name> --type <type> --stack <stack>`. Use `--language <id>` only when the user names a language (`bun` is the default).
3. For an existing service, use `--register-existing` instead of generating templates.
4. Check the result with `flisk doctor` and read the new `service.json`.
5. Start it with `flisk up <stack>` (see the flisk-up skill).

## Guardrails

- Use kebab-case names.
- A database migration belongs in its own `migrator` resource, not in an API start script.
- Ask before creating resources in a stack the user did not name.
