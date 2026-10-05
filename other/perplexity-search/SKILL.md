---
name: perplexity-search
description: Search only mode for low-cost Perplexity lookup. Use when the user needs links, sources, snippets, or quick web lookup without answer synthesis or deep research.
---

# Perplexity Search

Use this skill for Search only mode. Prefer the MCP path, but fall back to the direct Search API script if the MCP tool is not exposed in the current runtime.

Rules:

- Use the `perplexity_search` MCP tool from the `perplexity` server first.
- If the MCP tool is not exposed in the current runtime, run `python3 ~/.codeium/windsurf/skills/perplexity-search/search_only.py "<query>" --json` for a global Windsurf install, or `python3 perplexity_search_only/scripts/search_only.py "<query>" --json` when working from the repository root.
- Do not use `perplexity_ask`, `perplexity_reason`, or `perplexity_research`.
- Return 3-5 best results unless the user asks for another count.
- Include titles, URLs, dates when available, and short notes.
- If the user needs synthesis or recommendations, say that this requires a heavier mode.
