---
name: seo-ahrefs-competitors
description: >
  Discover a domain's top organic competitors from Ahrefs: competing domains,
  keyword overlap count, shared keywords, and unique competitor keywords. Use when
  user says "Ahrefs competitors", "organic competitors", "competing domains",
  "keyword overlap", or "who competes with".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# Ahrefs Organic Competitors

Identifies the top organic search competitors for a domain based on keyword
overlap, sorted by common keywords descending.

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

**Step 1 — Call Organic Competitors**

Call `mcp__claude_ai_ahrefs__site-explorer-organic-competitors` with:
- `target`: the bare domain (e.g., `example.com`)

Returns per competitor: domain, keyword overlap count, shared keywords,
unique keywords (keywords competitor ranks for that target doesn't)

**Step 2 — Sort and Analyze**

- Sort by common keywords descending (most overlap = closest competitor)
- Identify top 3 competitors
- For each top competitor, note the unique keywords they rank for that the
  target domain does not — these represent content gap opportunities

## Output Format

```
## Ahrefs Organic Competitors: example.com

### Competitor Landscape

| Domain | Common Keywords | Domain's Keywords | Competitor's Keywords | Traffic |
|--------|----------------|-------------------|----------------------|---------|
| competitor1.com | 4,230 | 12,450 | 18,900 | 145,000 |
| competitor2.com | 3,810 | 12,450 | 22,100 | 210,000 |
| competitor3.com | 2,950 | 12,450 | 9,800 | 67,000 |

### Top 3 Competitor Insights

**1. competitor1.com** (4,230 shared keywords)
- Unique strengths: ranks for 14,670 keywords you don't
- Opportunity: "product comparison" queries, "pricing" pages, "vs" content

**2. competitor2.com** (3,810 shared keywords)
- Unique strengths: ranks for 18,290 keywords you don't
- Opportunity: tutorial content, how-to guides, beginner-focused articles

**3. competitor3.com** (2,950 shared keywords)
- Unique strengths: ranks for 6,850 keywords you don't
- Opportunity: local/regional queries, case studies, integration pages
```

### Error — Ahrefs MCP Not Available

If MCP check fails, display the Ahrefs error template from
`references/mcp-degradation.md`:

```
## Ahrefs MCP Not Available

The `/seo ahrefs competitors` command requires the Ahrefs MCP, which is not
currently connected.

**What you can do:**
- Use `/seo audit <url>` for a full static SEO analysis without live Ahrefs data
- Use `/seo technical <url>` for technical SEO issues without backlink/keyword data

**To connect Ahrefs MCP:**
- Ensure the Ahrefs MCP is registered at user scope in ~/.claude/mcp.json
- Verify with: cat ~/.claude/mcp.json | grep -i ahrefs
- Ahrefs MCP must be registered at user scope (not project scope) to work in subagents
```
