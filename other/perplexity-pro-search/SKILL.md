---
name: perplexity-pro-search
description: Perplexity Pro Search for concise sourced answers with explicit search_type=pro. Use when the task needs a synthesized answer with sources, not just links.
---

# Perplexity Pro Search

Use this skill for the Pro Search mode.

1. Run `python3 perplexity-pro-search/scripts/pro_search.py "<query>" --context-size medium --json`.
2. Keep the question narrow unless the user explicitly wants broader coverage.
3. Return the answer, strongest sources, and usage/cost when helpful.
4. Do not silently replace this with Search only or Deep Research.
