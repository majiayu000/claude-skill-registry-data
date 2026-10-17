---
name: parallel-search
description: Use for current web search, URL extraction, or asynchronous deep-research task creation through Parallel.
compatibility: Node.js 20+, `PARALLEL_API_KEY`, and the `parallel-web` package.
---

# Parallel Search

Exports `parallel_search`, `parallel_extract`, `parallel_task`, and `parallel_task_result` from `src/index.ts`.

All operations validate inputs before network access and return `{ ok: true, data }` or `{ ok: false, error }`. Task creation is nonblocking and returns the queued Task Run identifiers. `parallel_task_result` retrieves a run: `wait: false` polls its current status, `wait: true` blocks for the completed `{ status, output }` and returns `error.run_id` on timeout so the run is never orphaned.

See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md) for Toolforge conventions.
