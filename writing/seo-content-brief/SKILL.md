---
name: seo-content-brief
description: >
  Generate a structured SEO content brief for a keyword using live Ahrefs SERP
  data and optional GSC overlay. Use when user says "content brief", "write a
  brief for", "content plan for keyword", "what should I write about", "brief
  for article", "content strategy for keyword", "help me write content for",
  or "create a brief for".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# SEO Content Brief Generator

Produces a structured, copy-pasteable content brief for writers by analyzing
live SERP data from Ahrefs. When a site parameter is provided and GSC MCP is
available, overlays current ranking position and click data for targeted
improvement guidance.

Note: SERP analysis is inlined here — skills cannot call each other as
sub-routines in Claude Code.

## References

@skills/seo/references/mcp-degradation.md
@skills/seo/references/ahrefs-api-reference.md
@skills/seo/references/gsc-api-reference.md

## Inputs

- `keyword`: The target keyword for the content brief (required). Example: `"best crm for startups"`
- `site` (optional): GSC property URL to overlay existing ranking data.
  Accepts both formats:
  - Domain property: `sc-domain:example.com`
  - URL prefix: `https://example.com/` or `https://www.example.com/`

## MCP Check

**Primary check (required):**
1. Use ToolSearch with query `+ahrefs`
2. If tools returned → Ahrefs MCP is available, proceed to Execution
3. If no tools returned → display the Ahrefs MCP error template from
   `references/mcp-degradation.md` and stop

**Optional GSC check (only if `site` parameter was provided):**
1. Use ToolSearch with query `+google-search-console`
2. If tools returned → GSC MCP is available, will overlay ranking data in Step 3
3. If no tools returned → note "GSC data unavailable — brief generated from SERP data only" and proceed

## Execution

**Step 1 — SERP Analysis (INLINE)**

Note: SERP analysis is inlined here because Claude Code skills cannot call
each other as sub-routines. The following replicates the seo-serp logic directly.

1a. Use ToolSearch with query `serp-overview` to inspect the tool definition
    and discover its parameter names. The keyword parameter may be named
    `keyword`, `query`, or `term` — do not assume. Use the exact parameter name
    found in the schema for the call.

1b. Call `mcp__claude_ai_ahrefs__serp-overview` using the discovered parameter
    name with the user's keyword as the value.

Returns: list of ranking pages with fields that may include `url`,
`domain_rating`, `traffic`, `traffic_cost`, `position`, `title`.

From the results, extract:
- Top 10 URLs, DR scores, and traffic estimates for the SERP table
- Content type pattern (guides, tool pages, listicles, comparisons, etc.)
- Average DR of top 10 for SERP difficulty assessment

**Step 2 — Keyword Volume Data**

Call `mcp__claude_ai_ahrefs__keywords-explorer-overview` with the keyword to
get search volume and keyword difficulty score.

If this tool is unavailable or returns an error, note "Volume data unavailable"
and proceed — the brief can still be generated from SERP data.

Key fields to extract: `volume` (monthly searches), `difficulty` (KD 0–100).

**Step 3 — GSC Overlay (only if `site` parameter provided AND GSC MCP available)**

Use ToolSearch to discover the exact GSC tool name prefix at runtime (it varies
by MCP registration alias). Look for a tool matching `query_search_analytics`.

Call the GSC `query_search_analytics` tool with:
- `siteUrl`: the value of the `site` parameter (e.g., `sc-domain:example.com`)
- `startDate`: 28 days ago (YYYY-MM-DD)
- `endDate`: today (YYYY-MM-DD)
- `dimensions`: `["query"]`
- Filter or search for the specific keyword in results

Extract for the keyword: `clicks`, `impressions`, `ctr`, `position`.

If the keyword is not found in GSC data → note "Keyword not yet ranking in GSC
for this property — brief targets a new ranking opportunity."

If GSC is unavailable → skip this step and note in output.

**Step 4 — Generate Brief**

Synthesize findings into a structured content brief:

- From SERP data: identify dominant content type, derive H2 structure from
  top-ranking titles, extract semantic keyword signals from titles/descriptions,
  identify differentiation gaps (what's missing or underserved)
- From keyword data: set word count target (correlate with SERP average; without
  data, use content type defaults: guide 2000–3500w, comparison 1500–2500w,
  tool page 1000–2000w, listicle 1500–2500w)
- From GSC data (if available): frame as position improvement rather than new ranking

**Step 5 — CRITICAL: Monetary conversion**

Any fields ending in `_cost`, `_value`, or `cpc` from Ahrefs are in CENTS.
Divide by 100 before display. Format as USD with comma thousands separators.

Also: GSC `ctr` is a decimal (0.0523 = 5.23%). Multiply by 100 for display.

## Output Format

The output must be copy-pasteable for content writers with no further editing needed:

```
## Content Brief: "{keyword}"
**Generated:** {YYYY-MM-DD}
**Keyword Volume:** {volume} searches/month (from Ahrefs){| — volume data unavailable}
**Keyword Difficulty:** {KD score}/100{| — KD data unavailable}
**SERP Difficulty:** {Low|Moderate|High|Very high} (avg DR of top 10: {avg_dr})

---

### Current Position (GSC data)
{If GSC data available and keyword found:}
You currently rank #{position} for this keyword with {clicks} clicks/month
({impressions} impressions, {ctr}% CTR).
Target: Move from #{position} to top 3.

{If GSC data available but keyword not found:}
This keyword is not yet ranking in GSC for {site}. Brief targets a new ranking
opportunity.

{If no site parameter provided or GSC unavailable:}
No GSC data — provide `site` parameter to overlay your current ranking position.

---

### What's Ranking Now

| # | URL | DR | Est. Traffic | Content Type |
|---|-----|----|-------------|--------------|
| 1 | example.com/page... | 72 | 8,200 | {type} |
| 2 | competitor.com/article... | 65 | 5,100 | {type} |
| 3 | site.com/guide... | 58 | 3,400 | {type} |
| 4 | domain.com/resource... | 71 | 2,900 | {type} |
| 5 | blog.com/post... | 44 | 1,800 | {type} |

---

### Recommended Structure
**Target word count:** {X,XXX–X,XXX words} (based on {SERP content type pattern|content type default})
**Content type:** {article|guide|comparison|tool page|listicle} — {why, based on SERP}
**Target URL slug:** `/{keyword-slug}`

**Suggested H2 structure:**
1. {H2 derived from top-ranking content patterns — what they all cover}
2. {H2}
3. {H2}
4. {H2}
5. {H2 — consider this for differentiation}

---

### Semantic Keywords to Include
Based on top-ranking title and description analysis:
- {keyword or phrase seen repeatedly in top results}
- {keyword or phrase}
- {keyword or phrase}
- {keyword or phrase}
- {keyword or phrase}

---

### Differentiation Angle
{2–3 sentences: What are the top-ranking pages doing? What's missing, underserved,
or poorly covered? What unique angle would stand out in this SERP — a specific
audience, use case, data depth, format, or perspective not yet covered?}

---

*Brief generated from Ahrefs SERP data{+ GSC data for {site}| — no GSC data (provide site= for ranking overlay)}.*
*Data reflects SERP as of {YYYY-MM-DD}.*
```

## Error — Ahrefs MCP Not Available

If the primary Ahrefs MCP check fails, display this message and stop:

```
## Ahrefs MCP Not Available

The `/seo content-brief` command requires the Ahrefs MCP, which is not
currently connected. SERP data is required to generate a content brief.

**What you can do:**
- Use `/seo audit <url>` for a full static SEO analysis without live SERP data
- Use `/seo technical <url>` for technical SEO issues without keyword data
- Manually provide target URLs to analyze for content patterns

**To connect Ahrefs MCP:**
- Ensure the Ahrefs MCP is registered at user scope in ~/.claude/mcp.json
- Verify with: cat ~/.claude/mcp.json | grep -i ahrefs
- Ahrefs MCP must be registered at user scope (not project scope) to work in subagents
```

## Error — GSC MCP Not Available (non-blocking)

If the optional GSC check fails (only relevant when `site` parameter was provided):

```
## Google Search Console MCP Not Available

GSC data for {site} is unavailable — the GSC MCP is not currently connected.
Proceeding with SERP-only brief. No current ranking position data will be included.

**To connect GSC MCP:**
- Install and configure a Google Search Console MCP server (see README for setup)
- Add it to ~/.claude/mcp.json at user scope (NOT project scope)
- Re-run `/seo content-brief {keyword} site={site}` to get the full brief with ranking overlay
```

## Error — Both Ahrefs and GSC Unavailable

If both MCPs fail (Ahrefs is required — stop):

Display the Ahrefs MCP Not Available error above. The brief cannot be generated
without Ahrefs SERP data regardless of GSC availability.
