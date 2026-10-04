---
name: seo-ahrefs-anchor-analysis
description: >
  Analyze a domain's anchor text distribution from Ahrefs: see the breakdown of
  anchor text used across all backlinks and assess link profile health. Use when
  user says "anchor text", "anchor analysis", "anchor distribution", "link anchors",
  or "anchor text profile".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# Ahrefs Anchor Text Analysis

Fetches the anchor text distribution for a domain's backlink profile from Ahrefs,
sorted by referring domains count, and assesses the health of the anchor profile.

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

**Step 1 — Call Anchors**

Call `mcp__claude_ai_ahrefs__site-explorer-anchors` with:
- `target`: the bare domain (e.g., `example.com`)

Returns per anchor: `anchor` (text), `referring_domains` count, `backlinks` count

**Step 2 — Calculate Percentages**

- Sum all `referring_domains` across all anchors to get the total
- Calculate each anchor's `% of Total` = (`referring_domains` / total) * 100
- Sort by `referring_domains` descending

**Step 3 — Health Assessment**

Classify the anchor text distribution using these thresholds:

- **Branded anchors** (domain name, brand name, company name):
  - >40% of referring domains = healthy
  - <10% = may indicate over-reliance on keyword anchors
- **Exact-match keyword anchors** (exact target keyword with no brand):
  - >10% = over-optimized risk (potential Google penalty signal)
  - 3–10% = acceptable range
- **Generic anchors** ("click here", "here", "this link", "read more", naked URLs):
  - >30% = may indicate low-quality link profile
  - 10–30% = normal range
- **Diverse distribution** (no single non-branded anchor >5%) = natural profile signal

## Output Format

```
## Ahrefs Anchor Text Analysis: example.com

### Anchor Text Distribution

| Anchor Text | Referring Domains | Backlinks | % of Total |
|-------------|------------------|-----------|------------|
| example.com | 1,420 | 3,100 | 44.2% |
| brand name | 580 | 890 | 18.1% |
| seo tools | 210 | 340 | 6.5% |
| click here | 180 | 210 | 5.6% |
| best seo software | 95 | 112 | 3.0% |

**Total referring domains across all anchors:** 3,210

### Profile Health Assessment

| Signal | Value | Status |
|--------|-------|--------|
| Branded anchors (example.com + brand name) | 62.3% | HEALTHY (>40%) |
| Exact-match keyword anchors (seo tools, best seo software) | 9.5% | ACCEPTABLE (<10%) |
| Generic anchors (click here, etc.) | 5.6% | HEALTHY (<30%) |
| Anchor diversity | 45+ unique anchors | NATURAL |

**Overall:** Healthy anchor profile. Branded anchors dominate at 62.3%, with
acceptable exact-match at 9.5%. No over-optimization signals detected.

### Recommendations
- Maintain branded anchor dominance — continue building brand mentions
- Monitor exact-match anchors — approaching 10% threshold; avoid actively
  building more exact-match links
```

### Error — Ahrefs MCP Not Available

If MCP check fails, display the Ahrefs error template from
`references/mcp-degradation.md`:

```
## Ahrefs MCP Not Available

The `/seo ahrefs anchor-analysis` command requires the Ahrefs MCP, which is not
currently connected.

**What you can do:**
- Use `/seo audit <url>` for a full static SEO analysis without live Ahrefs data
- Use `/seo technical <url>` for technical SEO issues without backlink/keyword data

**To connect Ahrefs MCP:**
- Ensure the Ahrefs MCP is registered at user scope in ~/.claude/mcp.json
- Verify with: cat ~/.claude/mcp.json | grep -i ahrefs
- Ahrefs MCP must be registered at user scope (not project scope) to work in subagents
```
