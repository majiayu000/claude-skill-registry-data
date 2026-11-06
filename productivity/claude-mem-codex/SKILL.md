---
name: claude-mem-codex
description: Use claude-mem from Codex via a Codex-specific wrapper, MCP registration, and ~/.codex-backed data paths.
metadata:
  author: codex
  version: "1.0.0"
---

# Claude-Mem For Codex

Use this skill when you want to use `claude-mem` from Codex.

## Goal

Provide Codex-friendly persistent memory by using the upstream `claude-mem` worker and MCP search server, without requiring Claude Code plugin commands.

## What This Installs

- Upstream repo under `~/.codex/claude-mem`
- Worker runtime backed by Bun
- Codex MCP server entry pointing to `plugin/scripts/mcp-server.cjs`
- Codex-specific data/config directories:
  - `~/.codex/memories/claude-mem`
  - `~/.codex/claude-mem-config`

## Usage

Use the MCP tools with the same 3-layer workflow recommended upstream:

1. `search`
2. `timeline`
3. `get_observations`

Fetch full observations only after filtering with `search`/`timeline`.

## Local Conventions

- Do not use Claude Code `/plugin` commands.
- Start the worker with Bun and the Codex-specific env vars.
- Point Codex MCP config at the installed repo path, not a temporary clone.

## Verification

Verify these before relying on the memory layer:

- Worker health endpoint responds on `127.0.0.1:37777`
- `codex mcp list` shows the configured server
- `codex mcp get claude-mem` shows the expected command/env
