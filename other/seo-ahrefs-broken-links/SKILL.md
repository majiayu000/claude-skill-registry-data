---
name: seo-ahrefs-broken-links
description: >
  Find broken backlinks pointing to a domain using Ahrefs: links targeting 404
  pages that can be reclaimed. Prioritizes highest-DR lost links for maximum
  recovery impact. Use when user says "broken backlinks", "broken links",
  "link reclamation", "dead backlinks", or "404 backlinks".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# Ahrefs Broken Backlinks

Fetches broken backlinks pointing to a domain (links targeting 404/gone pages),
sorted by source Domain Rating to prioritize the highest-value reclamation
opportunities.

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

**Step 1 — Call Broken Backlinks**

Call `mcp__claude_ai_ahrefs__site-explorer-broken-backlinks` with:
- `target`: the bare domain (e.g., `example.com`)

Returns per broken backlink: `url_from`, `url_to` (the 404 target page),
`anchor`, `domain_rating_source`, `http_code`, `first_seen`

**Step 2 — Sort by Priority**

Sort by `domain_rating_source` descending — highest-authority broken links first,
as reclaiming them delivers the greatest SEO value.

**Step 3 — Generate Reclamation Recommendations**

For each broken backlink in the top results:
- Suggest the closest matching live page on the domain to redirect the 404 target
- If no obvious match exists, recommend contacting the linking site with an
  updated URL

## Output Format

```
## Ahrefs Broken Backlinks: example.com

### Broken Backlink Summary
| Metric | Value |
|--------|-------|
| Total Broken Backlinks | 87 |
| Unique Linking Domains | 34 |
| High-DR Sources (DR 50+) | 12 |

### Broken Backlinks (sorted by Source DR)

| Linking Page | Linking Page DR | Target Page (404) | Anchor Text | HTTP Code | First Seen |
|-------------|-----------------|-------------------|-------------|-----------|------------|
| news.com/article | 76 | example.com/old-guide | "seo guide" | 404 | 2023-03-12 |
| blog.io/post | 63 | example.com/resources/pdf | "download" | 404 | 2022-11-08 |

### Link Reclamation Opportunities

**1. example.com/old-guide (DR 76 source — news.com/article)**
- Source anchor: "seo guide"
- Action: Redirect `/old-guide` → `/blog/complete-seo-guide` (301 redirect)
- OR: Contact news.com and provide updated URL

**2. example.com/resources/pdf (DR 63 source — blog.io/post)**
- Source anchor: "download"
- Action: Redirect `/resources/pdf` → `/downloads/seo-checklist.pdf` (301 redirect)
- OR: Contact blog.io/post author with updated resource URL
```

### Error — Ahrefs MCP Not Available

If MCP check fails, display the Ahrefs error template from
`references/mcp-degradation.md`:

```
## Ahrefs MCP Not Available

The `/seo ahrefs broken-links` command requires the Ahrefs MCP, which is not
currently connected.

**What you can do:**
- Use `/seo audit <url>` for a full static SEO analysis without live Ahrefs data
- Use `/seo technical <url>` for technical SEO issues without backlink/keyword data

**To connect Ahrefs MCP:**
- Ensure the Ahrefs MCP is registered at user scope in ~/.claude/mcp.json
- Verify with: cat ~/.claude/mcp.json | grep -i ahrefs
- Ahrefs MCP must be registered at user scope (not project scope) to work in subagents
```
