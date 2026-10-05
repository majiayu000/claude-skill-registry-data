---
name: perplexity-pro
description: Pro Search mode through the local Sonar Pro script. Use when the user needs a concise sourced answer, step log, or usage cost.
---

# Perplexity Pro Search

Use this skill for Pro Search mode through a local script path that works both in a global Windsurf install and from the repository root.

Rules:

- Run `python3 ~/.codeium/windsurf/skills/perplexity-pro/pro_search.py "<query>" --context-size medium --json` for a global Windsurf install, or `python3 perplexity-pro-search/scripts/pro_search.py "<query>" --context-size medium --json` from the repository root.
- Use `--context-size low` for small factual checks and `--context-size high` only when needed.
- Do not replace this with `perplexity_search`, `perplexity_ask`, `perplexity_reason`, or `perplexity_research` unless the user asks.
- Report `usage.cost.total_cost` when present.
- Return the answer, key sources, and cost if available.
