---
name: seo-gsc-indexing
description: >
  Identify indexing problems and coverage issues using Google Search Console URL
  inspection data. Checks up to 20 pages for indexing status, coverage state,
  robots.txt state, and last crawl date. Use when user says "index issues",
  "indexing problems", "not indexed", "indexing coverage",
  or "why is my page not indexed".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# GSC Index Issues — Indexing Coverage Report

@skills/seo/references/mcp-degradation.md
@skills/seo/references/gsc-api-reference.md

Checks indexing status for up to 20 pages using the GSC URL Inspection API.
IMPORTANT: `inspect_url` is rate-limited — this skill caps all calls at 20 to avoid
rate-limit hangs. Prioritizes pages most likely to have indexing issues.

## MCP Check

Before calling any GSC tool, verify the MCP is connected:

1. Use ToolSearch with query `+google-search-console`
2. If tools returned — note the actual tool name prefix, proceed to Inputs
3. If no tools returned — display the GSC MCP error template from
   `references/mcp-degradation.md` and stop:

```
## Google Search Console MCP Not Available

The `/seo gsc index-issues` command requires the GSC MCP, which is not currently connected.

**What you can do:**
- Use `/seo technical <url>` for crawlability and indexability analysis (no live data)
- Use `/seo audit <url>` for a full static SEO audit

**To connect GSC MCP:**
- Install and configure a Google Search Console MCP server (see README for setup)
- Add it to ~/.claude/mcp.json at user scope (NOT project scope)
- Verify GSC property access before running commands (domain vs URL prefix format)
- See references/gsc-api-reference.md for property format details
```

## Inputs

- `site`: The GSC property URL. Accept both formats:
  - Domain property: `sc-domain:example.com`
  - URL prefix: `https://example.com` or `https://www.example.com`
  - If user provides a bare domain (no prefix), call `list_sites` to identify
    the correct property format registered in GSC.
- `urls` (optional): Specific URLs the user wants to inspect. If provided, inspect
  these directly (still capped at 20 total calls).

## Date Calculation

Use Bash to calculate dates for the initial search analytics query:

```bash
endDate=$(date -v-3d +%Y-%m-%d)
startDate=$(date -v-31d +%Y-%m-%d)
echo "endDate: $endDate | startDate: $startDate"
```

## Execution

**RATE LIMIT RULE: Never call `inspect_url` more than 20 times in a single run.**

### Path A — User provided specific URLs

If the user provides specific URLs to inspect:
1. Accept up to 20 URLs (if user provides more, inspect first 20, note the cap)
2. For each URL, call `inspect_url`:
   - `siteUrl`: the site property
   - `inspectionUrl`: the specific URL
3. Collect all results, proceed to Output

### Path B — No specific URLs (general scan)

1. **Get pages GSC knows about:**
   Call `query_search_analytics` with:
   - `siteUrl`: the site property
   - `startDate`: calculated startDate
   - `endDate`: calculated endDate
   - `dimensions`: `["page"]`
   - `rowLimit`: 100

2. **Select pages to inspect (cap at 20):**
   Strategy — prioritize pages most likely to have indexing issues:
   - Sort pages by impressions ascending (low impressions = potential indexing issues)
   - Take the bottom 20 pages by impressions
   - These are the pages GSC sees but that get little visibility

3. **Inspect each selected page:**
   For each of the up to 20 selected pages, call `inspect_url`:
   - `siteUrl`: the site property
   - `inspectionUrl`: the page URL

   Stop after 20 calls regardless of remaining pages.

**Post-processing:**
Group results by coverage state:
- Indexed (coverageState contains "Indexed" or indexingState = "INDEXED")
- Excluded (coverageState contains "Excluded", "Blocked", "Noindex", "Redirect")
- Error (coverageState contains "Error", "Not found")

## Output Format

```
## GSC Index Issues: [site property]
**Pages inspected:** [count] of [total pages in GSC]
**Rate limit cap:** 20 inspect_url calls maximum per run

### Indexing Status Summary
| Coverage State | Count |
|----------------|-------|
| Indexed | [n] |
| Excluded | [n] |
| Error | [n] |

### Indexed Pages
| URL | Indexing State | Last Crawl Date |
|-----|----------------|-----------------|
| [url] | [state] | [date] |

### Excluded Pages
| URL | Coverage State | Robots.txt State | Last Crawl Date |
|-----|----------------|------------------|-----------------|
| [url] | [state] | [state] | [date] |

### Error Pages
| URL | Coverage State | Page Fetch State | Last Crawl Date |
|-----|----------------|------------------|-----------------|
| [url] | [state] | [state] | [date] |

### Recommendations
- [For each excluded/error page: specific action based on coverage state]
```

**Recommendation logic by coverage state:**
- "Blocked by robots.txt": Check robots.txt is not accidentally blocking this URL
- "Excluded by 'noindex' tag": Remove noindex meta tag if page should be indexed
- "Redirect": Verify the redirect target is indexed
- "Crawl anomaly" or fetch error: Check server response codes, page may be returning 5xx
- "Duplicate without user-selected canonical": Add canonical tag pointing to preferred URL
- "Not found (404)": Fix broken URL or add redirect from old URL

**Note if cap reached:** "Showing [20] of [total] pages. Run again with specific URLs
to inspect additional pages."
