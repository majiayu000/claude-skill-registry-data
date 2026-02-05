---
name: exa-search-ops
description: Use when Codex needs semantic web search, news reconnaissance, or citation gathering through the Exa MCP server.
---

# Exa Search Ops

## Purpose
Coordinate Exa-based semantic searches for discovery tasks, including link gathering, trend monitoring, and citation harvesting, using the remote configuration defined in `servers/exa`.

## Setup Checklist
1. Set `EXA_ENDPOINT`, `EXA_API_KEY`, and (optionally) `EXA_DEFAULT_REGION`.
2. Verify the `exa` entry exists in `mcp.json` with `maxResults` metadata tuned to the task.
3. Track the current request quota under the Exa dashboard before kicking off large searches.

## Workflow
1. **Frame the question** – clarify keywords, negative keywords, date windows, and desired number of results.
2. **Search** – call the `search` tool with structured parameters (topic, start/end date, numResults). Use follow-up expansion judiciously.
3. **Digest** – parse the returned snippets, grouping them by theme and ranking by score.
4. **Cite+Store** – log the `title`, `url`, and `score` for each item you surface downstream. Consider persisting curated lists under `docs/exa/`.

## Notes
- Enforce deduplication by comparing normalized URLs before presenting results.
- Use chronological filters instead of multi calls when researching within a known time range.
- If Exa responds with `rate_limited`, wait 10 seconds and retry once before escalating.
