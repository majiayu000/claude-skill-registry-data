---
name: memloom-setup
description: Install and configure memloom end to end. Daemon, config, MCP registration, Claude Code capture and recall hooks, first import. Use when asked to set up memloom.
---

# memloom setup

Install memloom, a local-first memory engine, on this machine. The full runbook with
expected output per step lives at https://docs.memloom.dev/guides/agent-setup; it is the
source of truth if anything here is unclear.

## Human gates

Do everything yourself except two things:

1. Ask the human for `OPENROUTER_API_KEY` when step 3 comes. Never print the key anywhere.
   If they decline, continue in offline mode and say recall quality is degraded.
2. Never run `memloom connect claude-code` or a non-dry-run `memloom import` without the
   human naming the scope or approving the run.

## Steps

1. Check `node --version` is 20 or later. If not, stop and ask the human to upgrade.
2. `npm install -g memloom`, then `memloom init`. This creates `~/.memloom` and starts the
   daemon on `http://127.0.0.1:4319`.
3. Ask for the API key. Add `OPENROUTER_API_KEY=...` to `~/.memloom/config.env`, then
   `memloom stop` and `memloom init` to restart. If anything was saved before the key was
   set, the daemon refuses to start: run `memloom stop`, `memloom reembed`, `memloom init`.
4. Register MCP. Claude Code: `claude mcp add memloom -- npx -y @memloom/mcp`. Other
   clients run the same command as a stdio server; configs are at
   https://docs.memloom.dev/mcp/setup.
5. Ask which projects to capture, then `memloom connect claude-code --project <name>`
   (repeatable) or `--all` with explicit approval. This installs session-end capture and
   prompt-time recall hooks; edits merge with existing hooks and a backup is written first.
6. `memloom import agent-memory --dry-run`, show the human, run for real. Then
   `memloom import sessions --dry-run`, get approval (this one spends LLM calls), run.
7. Verify: `memloom save "memloom setup verified"`, `memloom recall "setup verified"`
   expecting the hit, one `recall_memory` call through MCP, then `memloom status`
   expecting daemon running, both hooks installed, and the chosen scope.

## Common failures

- `command not found` after install: Node older than 20, npm skipped the package.
- 503 "store is locked": a psql/Drizzle client holds the single-connection lock; close it.
- Embedding mismatch on start: `memloom stop && memloom reembed`, then `memloom init`.
- `import sessions` refuses offline: distillation needs the LLM; set the key first.
