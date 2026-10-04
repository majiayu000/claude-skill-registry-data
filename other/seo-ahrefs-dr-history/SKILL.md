---
name: seo-ahrefs-dr-history
description: >
  Show a domain's Domain Rating trend over time from Ahrefs. Reveals DR growth,
  drops, and significant changes. Use when user says "DR history", "domain rating
  history", "DR trend", "domain rating over time", or "DR changes".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# Ahrefs Domain Rating History

Fetches the Domain Rating trend over time for a domain from Ahrefs, showing
historical data points in reverse chronological order with trend analysis.

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

**Step 1 — Call Domain Rating History**

Call `mcp__claude_ai_ahrefs__site-explorer-domain-rating-history` with:
- `target`: the bare domain (e.g., `example.com`)

Returns per data point: `date` (ISO 8601), `domain_rating` (0–100), `ahrefs_rank`

**Step 2 — Sort and Analyze**

- Sort data points by date descending (most recent first)
- Calculate overall trend: compare first (oldest) and last (most recent) DR values
  - "DR increased by X points over the last Y months"
  - "DR decreased by X points over the last Y months"
  - "DR stable (±2 points) over the last Y months"

**Step 3 — Flag Significant Changes**

Scan consecutive data points for swings >5 DR points in a single month:
- Mark these as noteworthy events: "Significant DR drop of X points in [month]"
  or "Significant DR gain of X points in [month]"
- These warrant investigation (algorithm update, major link acquisition/loss,
  toxic backlink removal, etc.)

## Output Format

```
## Ahrefs Domain Rating History: example.com

### DR History (Most Recent First)

| Date | Domain Rating | Ahrefs Rank |
|------|--------------|-------------|
| 2026-02-01 | 67 | #12,345 |
| 2026-01-01 | 65 | #13,100 |
| 2025-12-01 | 66 | #12,890 |
| 2025-11-01 | 58 | #18,200 |
| 2025-10-01 | 59 | #17,600 |
| 2025-09-01 | 60 | #17,100 |

### Trend Analysis
- **Overall trend:** DR increased by 7 points over the last 6 months (59 → 67)
- **Trajectory:** Upward — consistent growth with minor fluctuations

### Noteworthy Events
- **November 2025:** DR drop of 8 points (60 → 58) — investigate possible
  toxic link removal, algorithm update, or loss of high-DR backlinks
- **January 2026:** DR gain of 7 points (58 → 65) — significant link
  acquisition or algorithmic recovery

### Summary
Current DR 67 represents strong domain authority. The 7-point gain over 6 months
indicates active link building or growing editorial coverage.
```

### Error — Ahrefs MCP Not Available

If MCP check fails, display the Ahrefs error template from
`references/mcp-degradation.md`:

```
## Ahrefs MCP Not Available

The `/seo ahrefs dr-history` command requires the Ahrefs MCP, which is not
currently connected.

**What you can do:**
- Use `/seo audit <url>` for a full static SEO analysis without live Ahrefs data
- Use `/seo technical <url>` for technical SEO issues without backlink/keyword data

**To connect Ahrefs MCP:**
- Ensure the Ahrefs MCP is registered at user scope in ~/.claude/mcp.json
- Verify with: cat ~/.claude/mcp.json | grep -i ahrefs
- Ahrefs MCP must be registered at user scope (not project scope) to work in subagents
```
