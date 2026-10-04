---
name: seo-ahrefs-new-links
description: >
  See recently acquired and lost backlinks for a domain using Ahrefs. Shows new
  referring domains in the last 30 days and any lost referring domains. Use when
  user says "new backlinks", "new links", "recently acquired links", "lost links",
  or "new referring domains".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# Ahrefs New and Lost Links

Fetches referring domain history from Ahrefs, filtered to show recently acquired
domains (last 30 days) and any lost referring domains.

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

**Step 1 — Call Referring Domains**

Call `mcp__claude_ai_ahrefs__site-explorer-referring-domains` with:
- `target`: the bare domain (e.g., `example.com`)

Returns per referring domain: `domain`, `domain_rating`, `backlinks` count,
`first_seen` date (ISO 8601), and optionally `lost_date` for domains no longer linking.

**Step 2 — Filter by Date (Client-Side)**

The tool may not support native date filtering. If no native date filter exists:
- Compute the cutoff date: current date minus 30 days
- Filter entries where `first_seen >= cutoff_date` → these are new referring domains
- Separate entries where `lost_date` is present → these are lost referring domains

**Step 3 — Sort and Summarize**

- New referring domains: sort by `domain_rating` descending (highest DR new links first)
- Lost referring domains: sort by `domain_rating` descending (highest DR losses first)
- Calculate net change: new count minus lost count

## Output Format

```
## Ahrefs New & Lost Links: example.com (Last 30 Days)

### Net Change Summary
| Metric | Value |
|--------|-------|
| New Referring Domains | +12 |
| Lost Referring Domains | -3 |
| Net Change | +9 |

### New Referring Domains (Last 30 Days)

| Domain | DR | Backlinks from Domain | First Seen |
|--------|----|-----------------------|------------|
| highdr-news.com | 71 | 1 | 2026-02-18 |
| industry-blog.io | 58 | 3 | 2026-02-10 |
| partner-site.com | 44 | 2 | 2026-02-05 |

### Lost Referring Domains

| Domain | DR | Lost Date |
|--------|----|-----------|
| old-partner.com | 52 | 2026-01-28 |

### Observations
- Gained 12 new referring domains this month — healthy link velocity
- Lost 3 domains — investigate whether content was removed or sites changed focus
- Highest-DR gain: highdr-news.com (DR 71) — strong editorial link
```

### No New Links

If no referring domains have `first_seen` within the last 30 days:

```
## Ahrefs New & Lost Links: example.com

No new referring domains detected in the last 30 days.

**Suggestions:**
- Run `/seo ahrefs backlinks example.com` to review the full backlink profile
- Consider outreach or PR campaigns to build new referring domains
```

### Error — Ahrefs MCP Not Available

If MCP check fails, display the Ahrefs error template from
`references/mcp-degradation.md`:

```
## Ahrefs MCP Not Available

The `/seo ahrefs new-links` command requires the Ahrefs MCP, which is not
currently connected.

**What you can do:**
- Use `/seo audit <url>` for a full static SEO analysis without live Ahrefs data
- Use `/seo technical <url>` for technical SEO issues without backlink/keyword data

**To connect Ahrefs MCP:**
- Ensure the Ahrefs MCP is registered at user scope in ~/.claude/mcp.json
- Verify with: cat ~/.claude/mcp.json | grep -i ahrefs
- Ahrefs MCP must be registered at user scope (not project scope) to work in subagents
```
