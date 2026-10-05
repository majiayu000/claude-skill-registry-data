---
name: perplexity-search-only
description: Low-cost Perplexity search for links, snippets, and source discovery without answer synthesis. Use when the task needs fresh links or primary sources, not a synthesized answer.
---

# Perplexity Search Only

Use this skill for the Search only mode.

1. Prefer the MCP path `perplexity_search`.
2. If the MCP tool is not exposed in the current runtime, run:
   `python3 perplexity_search_only/scripts/search_only.py "<query>" --json`
3. Return links, dates when available, and short notes.
4. Do not switch into Pro Search or Deep Research unless the user asks.
