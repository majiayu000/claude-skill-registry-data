---
name: seo-ahrefs-content-gap
description: >
  Find keywords that competitors rank for but the target domain does not, using
  Ahrefs data. Reveals content opportunities and topic gaps. Use when user says
  "content gap", "keywords competitors rank for", "missing keywords",
  "competitor keywords", or "content gap analysis".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# Ahrefs Content Gap Analysis

Discovers keywords competitors rank for that the target domain does not, revealing
content opportunities. Uses runtime schema discovery to choose the best available
Ahrefs tool.

## References

@skills/seo/references/mcp-degradation.md
@skills/seo/references/ahrefs-api-reference.md

## Inputs

- `domain`: The bare target domain to analyze (e.g., `example.com`). Strip
  `https://`, `http://`, and trailing slashes.
- `competitors` (optional): Up to 3 competitor domains, space-separated
  (e.g., `competitor1.com competitor2.com`). If not provided, auto-detect using
  Ahrefs organic competitors tool.

## MCP Check

Before proceeding, verify Ahrefs MCP is available:

1. Use ToolSearch with query `+ahrefs`
2. If tools are returned → Ahrefs MCP is available, proceed to Execution
3. If no tools returned → display the Ahrefs MCP error template from
   `references/mcp-degradation.md` and stop

## Execution

**Step 1 — Identify Competitors**

If `competitors` parameter provided: use those domains directly.

If no competitors specified:
- Call `mcp__claude_ai_ahrefs__site-explorer-organic-competitors` with
  `target`: the bare domain
- Select top 3 competitors by common keyword overlap from the response

**Step 2 — Runtime Schema Discovery for Content Gap Tool**

IMPORTANT: The filter parameter for `keywords-explorer-matching-terms` that
enables competitor-domain filtering is UNVERIFIED. Discover the schema at runtime:

1. Use ToolSearch to load `mcp__claude_ai_ahrefs__keywords-explorer-matching-terms`
2. Inspect the tool's parameter schema carefully
3. Decision:
   - If the tool has a competitor/domain filter parameter → proceed with
     **Approach A** (direct filter)
   - If the tool has no such filter → fall back to **Approach B** (cross-reference)

Document which approach was used in the output.

**Step 3A — Direct Filter Approach (if schema supports it)**

For each competitor domain identified:
- Call `mcp__claude_ai_ahrefs__keywords-explorer-matching-terms` with:
  - `target`: the competitor domain keyword or filter parameter (per discovered schema)
  - Apply any discovered competitor/domain filter to find keywords competitor ranks for
- Cross-reference against target domain's keywords to identify gaps

**Step 3B — Cross-Reference Approach (fallback)**

1. Call `mcp__claude_ai_ahrefs__site-explorer-organic-keywords` with
   `target`: the target domain → collect target's keyword set

2. For each of the 3 competitor domains:
   - Call `mcp__claude_ai_ahrefs__site-explorer-organic-keywords` with
     `target`: the competitor domain
   - Collect their keyword set

3. Find keywords in competitor sets NOT in target's keyword set → these are gaps

**Step 4 — CRITICAL: Monetary Conversion**

`cpc` is returned in CENTS. Divide by 100 before display.
Format as USD per click: `$X.XX`.

Example: API returns `cpc = 350` → display as `$3.50/click`

**Step 5 — Prioritize Gaps**

Sort content gap keywords by:
1. Volume descending (highest search demand first)
2. Filter out keywords with position >50 for the target domain (focus on true gaps)

## Output Format

```
## Ahrefs Content Gap Analysis: example.com

**Method used:** [Approach A — direct filter] or [Approach B — cross-reference]
**Competitors analyzed:** competitor1.com, competitor2.com, competitor3.com

### Content Gap Opportunities

| Keyword | Volume | Difficulty | CPC | Competitor Ranking | Your Position |
|---------|--------|-----------|-----|-------------------|---------------|
| seo checklist | 8,100 | 42 | $3.20/click | competitor1.com #3 | Not ranking |
| on-page seo guide | 5,400 | 38 | $2.80/click | competitor2.com #5 | Not ranking |
| technical seo audit | 3,600 | 55 | $5.10/click | competitor1.com #2 | Not ranking |

### Summary
- **Total gap keywords found:** 340
- **High-opportunity gaps** (volume >1,000, difficulty <50): 45 keywords
- **Top content opportunity:** Create comprehensive "seo checklist" guide targeting
  the cluster around "seo checklist", "seo audit checklist", "on-page seo checklist"
```

### Error — Ahrefs MCP Not Available

If MCP check fails, display the Ahrefs error template from
`references/mcp-degradation.md`:

```
## Ahrefs MCP Not Available

The `/seo ahrefs content-gap` command requires the Ahrefs MCP, which is not
currently connected.

**What you can do:**
- Use `/seo audit <url>` for a full static SEO analysis without live Ahrefs data
- Use `/seo technical <url>` for technical SEO issues without backlink/keyword data

**To connect Ahrefs MCP:**
- Ensure the Ahrefs MCP is registered at user scope in ~/.claude/mcp.json
- Verify with: cat ~/.claude/mcp.json | grep -i ahrefs
- Ahrefs MCP must be registered at user scope (not project scope) to work in subagents
```
