---
name: seo-ahrefs-backlinks
description: >
  Analyze a domain's backlink profile using Ahrefs: see who links to the domain,
  source Domain Rating, anchor text, link type, and when each link was first seen.
  Use when user says "Ahrefs backlinks", "backlink profile", "who links to",
  "link analysis", or "referring pages".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# Ahrefs Backlink Profile

Fetches top backlinks for a domain from Ahrefs, sorted by source Domain Rating
(highest authority links first).

## References

@skills/seo/references/mcp-degradation.md
@skills/seo/references/ahrefs-api-reference.md

## Inputs

- `domain`: The bare domain to analyze (e.g., `example.com`). Strip `https://`,
  `http://`, and trailing slashes before passing to Ahrefs tools.

## MCP Check

Before proceeding, verify Ahrefs MCP is available:

1. Use ToolSearch with query `+ahrefs`
2. If tools are returned → Ahrefs MCP is available, proceed to Execution
3. If no tools returned → display the Ahrefs MCP error template from
   `references/mcp-degradation.md` and stop

## Execution

**Step 1 — Call All Backlinks**

Call `mcp__claude_ai_ahrefs__site-explorer-all-backlinks` with:
- `target`: the bare domain (e.g., `example.com`)

Returns per backlink: `url_from`, `url_to`, `anchor`, `domain_rating_source`,
`first_seen`, `lost_date`

**Step 2 — Sort and Summarize**

- Sort results by `domain_rating_source` descending (highest DR first)
- Count total backlinks
- Count unique referring domains (deduplicate by root domain of `url_from`)
- Count dofollow vs nofollow links (use `lost_date` absence to identify active links)

## Output Format

```
## Ahrefs Backlinks: example.com

### Summary
| Metric | Value |
|--------|-------|
| Total Backlinks | 45,230 |
| Unique Referring Domains | 3,210 |
| Dofollow Links | 38,400 (85%) |
| Nofollow Links | 6,830 (15%) |

### Top Backlinks (by Source DR)

| Linking Page | Target Page | Anchor Text | Source DR | Type | First Seen |
|-------------|-------------|-------------|-----------|------|------------|
| domain.com/page | example.com/blog | brand name | 82 | dofollow | 2024-01-15 |
| news.com/article | example.com/ | keyword phrase | 74 | dofollow | 2023-11-03 |
```

### Error — Ahrefs MCP Not Available

If MCP check fails, display the Ahrefs error template from
`references/mcp-degradation.md`:

```
## Ahrefs MCP Not Available

The `/seo ahrefs backlinks` command requires the Ahrefs MCP, which is not
currently connected.

**What you can do:**
- Use `/seo audit <url>` for a full static SEO analysis without live Ahrefs data
- Use `/seo technical <url>` for technical SEO issues without backlink/keyword data

**To connect Ahrefs MCP:**
- Ensure the Ahrefs MCP is registered at user scope in ~/.claude/mcp.json
- Verify with: cat ~/.claude/mcp.json | grep -i ahrefs
- Ahrefs MCP must be registered at user scope (not project scope) to work in subagents
```
