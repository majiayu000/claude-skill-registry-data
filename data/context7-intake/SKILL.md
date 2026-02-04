---
name: context7-intake
description: Use when Codex needs curated documentation context or outlines from the Context7 MCP server.
---

# Context7 Intake

## Purpose
Route documentation and background research tasks to the Context7 hosted MCP server so Codex can retrieve multi-level summaries without overloading the context window.

## Setup Checklist
1. Confirm `CONTEXT7_ENDPOINT` and `CONTEXT7_API_KEY` are available plus optional `CONTEXT7_COLLECTIONS`.
2. Update `servers/context7/config.json` when you add or remove collections so the metadata stays accurate.
3. For large collections, request an outline first before pulling full passages.

## Workflow
1. **Define the brief** – specify what context is needed (e.g., “architecture overview for Scheduler service between 2022-2023”).
2. **Search** – call the Context7 `search` tool with filters (collection, tags). If no hit, broaden keywords or switch collections.
3. **Summarize** – use the server’s outline/summary tools, then refine by requesting the exact sections.
4. **Cite** – capture the provided citation metadata when transferring insight into other skills or docs.

## Notes
- Context7 enforces concurrency quotas—queue multiple queries sequentially.
- When multiple results are returned, prefer outlines first, then fetch full passages for the top 2 hits.
- Store curated snippets in `docs/context/` if they should be re-used later.
