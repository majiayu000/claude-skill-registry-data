---
name: fetch-web-intel
description: Use when Codex must fetch web pages, scrape selectors, or crawl sitemaps through the remote Fetch/Web MCP server catalog entry.
---

# Fetch Web Intel

## Purpose
Plan and execute web data collection tasks via the hosted Fetch MCP server registered in `servers/fetch`. Ideal for capturing article summaries, metadata, or targeted DOM fragments.

## Setup Checklist
1. Verify `FETCH_MCP_ENDPOINT` / `FETCH_MCP_API_KEY` exist and the endpoint is listed in `mcp.json`.
2. Confirm the remote server’s allow list includes the target domains; update the provider portal if not.
3. Decide on user agent overrides when sites block generic bots.

## Workflow
1. **Scope** – list URLs plus extraction goals (full page HTML, CSS selector, sitemap traversal). Batch by domain to leverage connection reuse.
2. **Execute** – call the MCP `fetch`, `scrape`, or `search` tools. Supply timeout hints for heavier pages.
3. **Normalize** – clean the payload (strip scripts, collapse whitespace) before storing or handing to other skills.
4. **Log** – capture HTTP status and rate-limit headers so we can backoff or retry intelligently.

## Notes
- Respect robots: if the server returns `blockedByRobots`, inform the user instead of retrying.
- Cap parallel requests to 3 per domain to avoid provider throttling.
- Store extracted outputs under `docs/intel/` through the filesystem skill if they need persistence beyond the current run.
