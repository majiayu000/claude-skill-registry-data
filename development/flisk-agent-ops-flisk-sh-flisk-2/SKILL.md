---
name: flisk-agent-ops
description: Ground rules and the CLI-to-MCP command map for a coding agent (Claude Code, Cursor, Codex) working in a Flisk project - create services with `flisk resource` instead of hand-writing Dockerfiles, Compose files or manifests, keep the agent resource contract, and drive the stack with `--json` commands or the `flisk mcp` tools (`doctor`, `up`, `status`, `logs`, `resource_restart`, `agent_list`, `agent_sessions`, `down`). Use when about to write container config by hand or when you need the MCP tool for a CLI command. For building a whole app from a request, use flisk-build.
license: MIT
compatibility: Requires the flisk CLI, Docker, and Tilt.
metadata:
  author: flisk-sh
  version: "1.0"
---

# Flisk Agent Operations Guide

When building, adding, or modifying services in this workspace, **do not hand-write Dockerfiles, Docker Compose files, or container manifests**. Flisk automatically manages containerization, networking (Traefik), dependencies, and hot reload.

## Core Rules for AI Coding Agents

1. **Always use Flisk to scaffold new services:**
   - Scaffold an AI agent: `flisk resource <name> --type agent [--durability files|postgres]`
   - Scaffold an MCP tool server: `flisk resource <name> --type mcp`
   - Scaffold a backend API: `flisk resource <name> --type backend [--framework hono|express|fastify]`
   - Scaffold a worker: `flisk resource <name> --type worker`
   - Scaffold a frontend: `flisk resource <name> --type frontend [--framework react|vue|next]`
   - Wrap an existing Dockerfile or image: `flisk resource <name> --type bring-your-own --dockerfile ./Dockerfile` (or `--image <name>`)

2. **The `agent` Process Contract:**
   - `/health`: Liveness only. Responds 200 when the process is alive.
   - `/ready`: Readiness check. Responds 200 when the checkpoint store (named volume or Postgres) is reachable.
   - `/turn` (POST): Accepts a JSON body `{"input": "..."}` with header `x-session-id: <session-id>`.
   - `/session` (GET): Returns checkpointed messages and turns for the session specified in `x-session-id`.
   - `/sessions` (GET): Lists the stored sessions, newest first.
   - Checkpoints persist across container restarts and `flisk down`/`flisk up`.

3. **Operate via MCP or CLI:**
   - Preflight & diagnostics: `flisk doctor --json` (or tool `doctor`)
   - Start the stack: `flisk up --json` (or tool `up`)
   - Inspect status: `flisk status --json` (or tool `status`)
   - Check logs: `flisk logs --tail 200 --json` (or tool `logs`)
   - Restart a service: `flisk restart <resource> --json` (or tool `resource_restart`)
   - List agents: `flisk resources --type agent --json` (or tool `agent_list`)
   - List agent sessions: `flisk agent sessions <resource> --json` (or tool `agent_sessions` with `resource`); add `--session-id <id>` (tool: `sessionId`) to read one session's checkpoint
   - Stop services: `flisk down --json` (or tool `down`)
