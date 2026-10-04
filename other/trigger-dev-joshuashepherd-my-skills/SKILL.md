---
name: trigger-dev
description: >-
  Work with Trigger.dev (v4) — the open-source background jobs framework for
  durable TypeScript tasks, scheduled/cron jobs, waits, Realtime, React hooks,
  the Management API, and chat.agent AI agents. Use when the user mentions
  Trigger.dev, writes/triggers tasks, edits trigger.config.ts, uses
  @trigger.dev/sdk or the trigger.dev CLI. ALWAYS fetch current docs first.
---

# Trigger.dev (Cursor)

Trigger.dev is an open-source background-jobs framework: reliable, long-running async TypeScript workflows with built-in queues, retries, waits, and real-time monitoring. **Current version is v4** — model training data is usually stale (v2/v3), so never write Trigger.dev code from memory.

## Canonical source

Full patterns, invariants, and the curated doc map live in the Claude bundle:
**`.claude/skills/trigger-dev/SKILL.md`** and **`.claude/skills/trigger-dev/reference.md`**.

## Rule 0: fetch live docs before writing code

1. **`trigger` MCP server** — if configured, use its `search_docs` tool (no auth needed). Best source.
2. **`llms.txt` index** — `https://trigger.dev/docs/llms.txt` to find the exact page.
3. **Raw markdown** — append `.md` to any docs URL, e.g. `https://trigger.dev/docs/tasks/overview.md`.
4. **Full dump** — `https://trigger.dev/docs/llms-full.txt` (large; broad context only).
5. **Context7** fallback if the above are unreachable.

## Recommended tooling

```bash
npx trigger.dev@latest init                                  # add to a project
npx trigger.dev@latest install-mcp --client cursor           # live docs/deploy/monitor in Cursor
npx trigger.dev@latest skills                                # offline pattern skills
npx trigger.dev@latest dev                                   # local dev server
```

The MCP server config for Cursor goes in `~/.cursor/mcp.json` (user) or `.cursor/mcp.json` (project):

```json
{ "mcpServers": { "trigger": { "command": "npx", "args": ["trigger.dev@latest", "mcp"] } } }
```

## v4 invariants

- Import from `@trigger.dev/sdk` — NEVER `@trigger.dev/sdk/v3`; NEVER `client.defineJob()` (v2).
- Every task is a named `export`; define with `task()` / `schemaTask()`.
- Backend: `tasks.trigger<typeof myTask>("task-id", payload)` with a **type-only** import of the task.
- `triggerAndWait()` returns a `Result` — check `.ok` / `.output`, or `.unwrap()`.
- Never `Promise.all` around waits or `*AndWait`. Tasks have no timeouts (use `maxDuration`).

```ts
import { task } from "@trigger.dev/sdk";

export const myTask = task({
  id: "my-task",
  retry: { maxAttempts: 3 },
  run: async (payload: { url: string }) => ({ success: true }),
});
```
