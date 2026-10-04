---
name: seo-ahrefs-keywords
description: >
  Get a domain's top organic keyword rankings from Ahrefs: keyword, position,
  search volume, CPC, estimated traffic, and traffic share. Use when user says
  "Ahrefs keywords", "organic keywords", "keyword rankings", "what keywords rank",
  or "ranking keywords".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# Ahrefs Organic Keywords

Fetches top organic keywords a domain ranks for, sorted by estimated traffic
(highest-value keywords first).

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

**Step 1 — Call Organic Keywords**

Call `mcp__claude_ai_ahrefs__site-explorer-organic-keywords` with:
- `target`: the bare domain (e.g., `example.com`)

Returns per keyword: `keyword`, `position`, `volume`, `cpc` (CENTS), `traffic`,
`traffic_percent`

**Step 2 — CRITICAL: Monetary Conversion**

`cpc` is returned in CENTS. Divide by 100 before display.
Format as USD per click: `$X.XX`.

Example: API returns `cpc = 250` → display as `$2.50/click`

**Step 3 — Sort and Cluster**

- Sort by `traffic` descending (highest-value keywords first)
- Identify top 3 keyword clusters by topic (group keywords sharing root terms
  or intent — e.g., "seo tools", "seo software", "best seo tool" form one cluster)

## Output Format

```
## Ahrefs Organic Keywords: example.com

### Top Keywords (by Traffic)

| Keyword | Position | Search Volume | CPC | Est. Traffic | Traffic % |
|---------|----------|--------------|-----|-------------|-----------|
| seo tools | #3 | 22,000 | $4.50/click | 3,200 | 12.4% |
| best seo software | #5 | 8,100 | $6.20/click | 890 | 3.5% |
| keyword research tool | #8 | 5,400 | $3.10/click | 410 | 1.6% |

### Summary
- **Total organic keywords:** 12,450
- **Total estimated traffic:** 25,700 visits/mo

### Top Keyword Clusters
1. **SEO tools** — "seo tools", "best seo software", "seo tool comparison" (combined traffic: 4,500)
2. **Keyword research** — "keyword research tool", "find keywords", "keyword tracker" (combined traffic: 1,800)
3. **Backlink analysis** — "backlink checker", "check backlinks", "link analysis tool" (combined traffic: 1,200)
```

### Error — Ahrefs MCP Not Available

If MCP check fails, display the Ahrefs error template from
`references/mcp-degradation.md`:

```
## Ahrefs MCP Not Available

The `/seo ahrefs keywords` command requires the Ahrefs MCP, which is not
currently connected.

**What you can do:**
- Use `/seo audit <url>` for a full static SEO analysis without live Ahrefs data
- Use `/seo technical <url>` for technical SEO issues without backlink/keyword data

**To connect Ahrefs MCP:**
- Ensure the Ahrefs MCP is registered at user scope in ~/.claude/mcp.json
- Verify with: cat ~/.claude/mcp.json | grep -i ahrefs
- Ahrefs MCP must be registered at user scope (not project scope) to work in subagents
```
