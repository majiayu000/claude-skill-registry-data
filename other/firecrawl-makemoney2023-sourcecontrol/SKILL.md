---
name: firecrawl
description: >-
  Use when scraping or mapping web pages via Firecrawl MCP for research, SEO, competitive intel, or content audits.
---

# Firecrawl

Thin adapter for digital workers. See `skills/org/TOOL-REGISTRY.md`.

## Preferred access
Firecrawl MCP (`user-firecrawl-mcp`)

## Env / secrets
`FIRECRAWL_API_KEY`

Resolve via `skills/integrations/obsidian-secrets/` then `.env.local`.

## MCP
`user-firecrawl-mcp` — tools: scrape, map, crawl, search, extract

## Primary ops
1. GetMcpTools then scrape/map target URLs
2. Cite source URLs in handoffs
3. Respect robots / public pages only for legal-counsel secondary use

## Fallback
Playwright browser MCP for single pages; Parallel for research

## Common failures
Missing key → obsidian-secrets / .env.local; do not invent page content
