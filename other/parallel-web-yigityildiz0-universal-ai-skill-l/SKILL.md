---
name: parallel-web
description: "Parallel web research and retrieval. Paralel web araştır, çoklu kaynak tara. Requires documented Parallel tools/credentials; report unavailable integrations."
license: MIT
---

# Parallel Web (gated)

Upstream [parallel-web/parallel-agent-skills](https://github.com/parallel-web/parallel-agent-skills) (MIT), all skills unchanged as modules.

**Gate:** Parallel's CLI and APIs need an installed, authenticated and funded `parallel-cli`, or a configured Parallel Search MCP. Use this skill only when the user explicitly asks for Parallel or it is already configured. Otherwise ordinary research belongs to `research-analyst`. Never create accounts or keys; `parallel-cli-setup` explains setup when the user asks for it.

## Modules

- [`choose-your-parallel-api`](modules/choose-your-parallel-api/MODULE.md) — Choose the right Parallel API and configuration for cost, latency, and answer quality.
- [`migrate-to-parallel`](modules/migrate-to-parallel/MODULE.md) — Migrate Exa, Tavily, Perplexity, or Firecrawl web-data integrations completely to the appropriate Parallel products while preserving applic…
- [`parallel-cli-setup`](modules/parallel-cli-setup/MODULE.md) — Set up and maintain the Parallel CLI (install, auth, balance, skills install)
- [`parallel-data-enrichment`](modules/parallel-data-enrichment/MODULE.md) — Bulk data enrichment.
- [`parallel-deep-research`](modules/parallel-deep-research/MODULE.md) — ONLY use when user explicitly says 'deep research', 'exhaustive', 'comprehensive report', or 'thorough investigation'.
- [`parallel-findall`](modules/parallel-findall/MODULE.md) — Discover entities (companies, people, products, etc.) matching a natural-language description.
- [`parallel-mcp-setup`](modules/parallel-mcp-setup/MODULE.md) — Use when installing, configuring, or troubleshooting an authenticated Parallel Search MCP connection in Bifrost, including gateway-level se…
- [`parallel-memory`](modules/parallel-memory/MODULE.md) — Recall past Parallel Task, Monitor, and FindAll runs when they may help; evict runs or clear memory when asked.
- [`parallel-monitor`](modules/parallel-monitor/MODULE.md) — Continuously track the web for changes on a recurring cadence.
- [`parallel-search-setup`](modules/parallel-search-setup/MODULE.md) — Use when verifying, using, or troubleshooting the anonymous Parallel Search MCP server bundled with this plugin — when the user installs th…
- [`parallel-web-extract`](modules/parallel-web-extract/MODULE.md) — CLI-backed URL extraction.
- [`parallel-web-search`](modules/parallel-web-search/MODULE.md) — CLI-backed web search.
- [`result`](modules/result/MODULE.md) — Get completed research task result by run ID
- [`status`](modules/status/MODULE.md) — Check running research task status by run ID
