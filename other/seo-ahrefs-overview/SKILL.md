---
name: seo-ahrefs-overview
description: >
  Get Ahrefs domain overview: Domain Rating, total backlinks, referring domains,
  organic keywords, estimated monthly traffic, and traffic value. Use when user
  says "Ahrefs overview", "domain rating", "DR score", "check backlinks",
  "how strong is this domain", "domain authority", or "check domain in Ahrefs".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# Ahrefs Domain Overview

Fetches domain authority, backlink summary, and organic traffic metrics from
Ahrefs for a given domain.

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

**Step 1 — Call Site Explorer Metrics**

Call `mcp__claude_ai_ahrefs__site-explorer-metrics` with:
- `target`: the bare domain (e.g., `example.com`)

Returns: `organic_traffic`, `traffic_cost` (CENTS), `organic_keywords`,
`backlinks`, `referring_domains`

**Step 2 — Call Domain Rating**

Call `mcp__claude_ai_ahrefs__site-explorer-domain-rating` with:
- `target`: the bare domain

Returns: `domain_rating` (0–100), `ahrefs_rank`

**Step 3 — CRITICAL: Monetary Conversion**

`traffic_cost` is returned in CENTS. Divide by 100 before display.
Format as USD with comma thousands separators: `$X,XXX`.

Example: API returns `traffic_cost = 125000` → display as `$1,250`

## Output Format

```
## Ahrefs Overview: example.com

| Metric | Value |
|--------|-------|
| Domain Rating | 67/100 |
| Ahrefs Rank | #12,345 |
| Total Backlinks | 45,230 |
| Referring Domains | 3,210 |
| Organic Keywords | 12,450 |
| Est. Monthly Traffic | 89,000 visits |
| Traffic Value | $4,200/mo |

### Interpretation

- **DR 67/100** — Strong domain with solid authority
- **3,210 referring domains** — Healthy and diverse link profile
- **$4,200/mo traffic value** — Equivalent Ahrefs estimate of organic traffic cost via paid ads
```

### Error — Ahrefs MCP Not Available

If MCP check fails, display the Ahrefs error template from
`references/mcp-degradation.md`:

```
## Ahrefs MCP Not Available

The `/seo ahrefs overview` command requires the Ahrefs MCP, which is not
currently connected.

**What you can do:**
- Use `/seo audit <url>` for a full static SEO analysis without live Ahrefs data
- Use `/seo technical <url>` for technical SEO issues without backlink/keyword data

**To connect Ahrefs MCP:**
- Ensure the Ahrefs MCP is registered at user scope in ~/.claude/mcp.json
- Verify with: cat ~/.claude/mcp.json | grep -i ahrefs
- Ahrefs MCP must be registered at user scope (not project scope) to work in subagents
```
