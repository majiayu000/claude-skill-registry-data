---
name: seo-brand-radar
description: >
  Monitor brand visibility in AI search and traditional search. Use when user says
  "brand radar", "brand monitoring", "AI search visibility", "brand mentions",
  "share of voice", "who mentions my brand in AI", "brand in ChatGPT",
  "brand in Perplexity", "how visible is my brand", "brand awareness tracking",
  "AI brand presence", "is my brand cited in AI responses".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# Brand Radar — AI Search Brand Monitoring

Monitors brand visibility in AI-generated search responses, brand mention trends,
share of voice, and which domains cite the brand in AI responses. Powered by
Ahrefs Brand Radar — no fallback exists for this data.

## References

@skills/seo/references/mcp-degradation.md
@skills/seo/references/ahrefs-api-reference.md

## Inputs

- `brand`: The brand name or domain to monitor (required). Can be a company name
  (`Notion`) or a domain (`notion.so`). Use whatever format the user provides —
  do NOT normalize unless the API explicitly requires it.

## MCP Check

Before proceeding, verify Ahrefs MCP is available:

1. Use ToolSearch with query `+ahrefs`
2. If tools are returned → Ahrefs MCP is available, proceed to Execution
3. If no tools returned → display the Brand Radar error template below and stop

**CRITICAL — No Fallback:** Brand Radar is an Ahrefs-exclusive feature. If Ahrefs
MCP is not connected, this command cannot provide any data. Do NOT estimate or
fabricate brand monitoring data. Do NOT attempt to infer brand visibility from
other sources. Stop and show the error.

## Execution

### Step 1 — Schema Discovery (CRITICAL)

Use ToolSearch with query `brand-radar` to discover all available Brand Radar tools
and their exact parameter schemas.

From the returned tool definitions, inspect and document:
a) What parameter name is used for the brand/target input — may be `target`,
   `brand`, `query`, `brandTarget`, or another name. Do NOT assume it is `target`.
b) What response fields each tool returns — field names vary and are NOT documented
   statically in this skill.
c) Which Brand Radar tools are available in the connected Ahrefs MCP version.

Record the discovered parameter name as `{brand_param}` before making any API calls.
All subsequent calls in Steps 2–5 use `{brand_param}: {brand_input}`.

**If ToolSearch returns no brand-radar tools:** Display error "Brand Radar tools
not found in connected Ahrefs MCP. This feature may not be available in your
Ahrefs account tier." and stop.

### Step 2 — Brand Mentions Overview

Call `mcp__claude_ai_ahrefs__brand-radar-mentions-overview` with:
- `{brand_param}`: the brand input

This is the primary data call. If this call fails (any error), stop entirely and
display: "Brand Radar primary data unavailable: {error}. Cannot generate report."

Document the actual response fields returned for use in Output Format.

### Step 3 — Share of Voice

Call `mcp__claude_ai_ahrefs__brand-radar-sov-overview` with:
- `{brand_param}`: the brand input

If this call fails, log `SKIPPED: brand-radar-sov-overview — {error}` and continue
with remaining steps.

### Step 4 — AI Search Visibility (Primary Differentiator)

Call `mcp__claude_ai_ahrefs__brand-radar-ai-responses` with:
- `{brand_param}`: the brand input

This is the most differentiated data — shows how the brand appears in AI-generated
search responses (ChatGPT, Perplexity, etc.). If this call fails, log
`SKIPPED: brand-radar-ai-responses — {error}` and continue.

### Step 5 — Cited Domains in AI Responses

Call `mcp__claude_ai_ahrefs__brand-radar-cited-domains` with:
- `{brand_param}`: the brand input

Shows which domains are cited alongside the brand in AI responses — critical for
understanding who the brand is associated with in AI-generated content.
If this call fails, log `SKIPPED: brand-radar-cited-domains — {error}` and continue.

### Step 6 — Monetary Conversion (CRITICAL)

If any response field contains cost, value, or traffic_value data:
- All monetary values from Ahrefs are returned in CENTS
- Divide by 100 before display
- Format as USD with comma separators: `$X,XXX`

Example: `traffic_cost = 125000` → display as `$1,250`

## Output Format

Output tables are adapted at runtime based on discovered API response fields.
The exact columns depend on what the Brand Radar API returns — do NOT hardcode
column names. Build tables from actual response fields.

```
## Brand Radar: {brand}
**Generated:** {date}
**Data Source:** Ahrefs Brand Radar

### AI Search Visibility
{Table built from brand-radar-ai-responses data}
{Adapt columns to actual response fields — e.g., AI platform, mention count,
sentiment, response type, or whatever fields the API returns}

### Brand Mentions Overview
{Table/summary built from brand-radar-mentions-overview}
{Adapt columns to actual response fields — e.g., total mentions, trend,
sources, time period}

### Share of Voice
{Data from brand-radar-sov-overview}
{Adapt to actual response fields — e.g., SOV percentage, competitor comparison}

### Top Cited Sources in AI Responses
{Table from brand-radar-cited-domains}
{Columns adapted to actual response — e.g., domain, citation count, context}

### Key Insights
{AI interpretation of brand visibility trends and competitive position.
Identify: (1) Is the brand well-represented in AI responses? (2) What are the
strongest / weakest visibility signals? (3) What action would improve AI brand
visibility? Write 3-5 sentences of analytical interpretation, not raw data.}

### Skipped Data
{If any steps were skipped due to errors, list them here with reasons}
```

## Error — Ahrefs MCP Not Available

```
## Ahrefs Brand Radar Not Available

The `/seo brand-radar` command requires the Ahrefs MCP, which is not currently
connected.

**Important:** Brand Radar is an Ahrefs-exclusive feature with no alternative
data source. Connect Ahrefs MCP to use this command. No fallback exists —
brand monitoring data cannot be estimated or approximated from other sources.

**What you can do while Ahrefs is unavailable:**
- Use `/seo audit <url>` for a full static SEO analysis
- Use `/seo geo <url>` for AI Overviews optimization analysis (static, no live data)

**To connect Ahrefs MCP:**
- Ensure the Ahrefs MCP is registered at user scope in ~/.claude/mcp.json
- Verify with: cat ~/.claude/mcp.json | grep -i ahrefs
- Ahrefs MCP must be registered at user scope (not project scope) to work in subagents
```
