---
name: seo-internal-links
description: >
  Analyze internal link structure by crawling a domain. Identifies orphan pages,
  underlinked pages (configurable heuristic, default fewer than 3 inbound links),
  and broken internal links.
  Suggests anchor text for top 5 underlinked pages. Reuses existing fetch/parse
  scripts. Optional Ahrefs enrichment. Use when user says "internal links",
  "link structure", "orphan pages", "internal linking", "link graph", "anchor text audit".
allowed-tools:
  - Read
  - Bash
  - Glob
  - WebFetch
  - ToolSearch
---

# Internal Link Audit

<!-- Updated: 2026-06-10 -->

Crawls a domain to build an internal link graph. Identifies orphan pages, underlinked pages,
and broken internal links. Suggests anchor text improvements.

## Inputs

- `domain`: Target domain URL (e.g., `https://example.com`). Include protocol.
- `max_pages` (optional): Max pages to crawl. Default: 100. Maximum: 200.

## Execution

**Step 1: Crawl Site**

Use `scripts/fetch_page.py` and `scripts/parse_html.py` to crawl the site:

```bash
# Fetch homepage
python3 scripts/fetch_page.py <domain>
# Parse HTML to extract links
python3 scripts/parse_html.py <html_content>
```

Follow internal links only (same domain hostname). Normalize URLs:
- Remove trailing slashes (treat `/about` and `/about/` as same)
- Remove URL fragments (`#section`)
- Preserve query strings only if they appear to be content (not tracking: strip `utm_*`, `ref=`, `source=`)

Respect robots.txt: fetch `<domain>/robots.txt` first, skip disallowed paths.
Cap crawl at `max_pages`. Track crawl queue (BFS order from homepage).

**Step 2: Build Link Graph**

For each crawled page, record:
- Source URL
- Target URL (all internal links found)
- Anchor text for each link

Build adjacency structure:
- `outbound[url]` = list of (target, anchor_text)
- `inbound[url]` = list of (source, anchor_text)

**Step 3: Calculate Per-Page Metrics**

For each crawled page:
- Inbound internal links count (links from other crawled pages pointing here)
- Outbound internal links count (links from this page to other pages)
- Link depth from homepage (BFS level at which this page was first discovered)

**Step 4: Identify Issues**

- **Orphan pages** (hard finding): Pages discovered via sitemap (`<domain>/sitemap.xml`) or linked from other pages but with **zero** inbound internal links. Fetch sitemap first to identify all known URLs.
- **Underlinked pages** (heuristic flag): Pages with fewer inbound internal links than a configurable threshold (default: 3). This threshold is a heuristic for prioritizing internal-linking work — Google defines no numeric minimum, so it is not a Google requirement.
- **Excessive outbound**: Pages with > 100 outbound internal links (PageRank dilution).
- **Broken internal links**: For top 20 most-linked pages, verify HTTP status. Flag 4xx/5xx.

**Step 5: Anchor Text Suggestions for Top 5 Underlinked Pages**

For each of the 5 most underlinked pages (fewest inbound links, excluding orphans):
1. Fetch the page and extract H1 and `<title>` tag
2. Identify top 3 relevant anchor text options based on: H1 noun phrases, title keywords, page URL slug
3. Find pages in crawl that mention related terms and could link to this page
4. Output: target URL, suggested anchors (ranked), recommended source pages

Anchor text guidance (per Google's crawlable-links doc,
https://developers.google.com/search/docs/crawling-indexing/links-crawlable):
- Write descriptive, reasonably concise link text relevant to the target page
- Avoid generic anchors like "click here", "read more", or "website"
- Links must be `<a>` elements with an `href` attribute resolving to a crawlable URL — Google can't reliably extract script-driven pseudo-links

**Step 6: Optional Ahrefs Enrichment**

If Ahrefs available (ToolSearch '+ahrefs'):
- Fetch `site-explorer-pages-by-internal-links` for the domain
- Cross-reference crawl findings with Ahrefs data
- Add `### Ahrefs Internal Link Data` section showing discrepancies

## Output Format

```
## Internal Link Audit: [domain]

### Summary Stats

| Metric | Value |
|--------|-------|
| Pages crawled | N / max_pages |
| Total internal links | N |
| Avg inbound links per page | N.N |
| Orphan pages found | N |
| Underlinked pages (below threshold, default <3 inbound) | N |
| Pages with broken internal links | N |

### Orphan Pages

Pages with 0 inbound internal links:

| URL | Depth | Found via |
|-----|-------|-----------|
| /page | — | sitemap |

### Top 5 Underlinked Pages — Suggested Anchors

**1. [URL]** — N inbound links
- H1: "[heading]"
- Suggested anchors: "[anchor 1]", "[anchor 2]", "[anchor 3]"
- Recommended source pages: [list pages that mention related terms]

### Broken Internal Links

| Source Page | Broken Link | Status Code |
|---|---|---|

### Link Depth Distribution

| Depth | Pages | % of Total |
|-------|-------|------------|
| 1 (homepage) | 1 | X% |
| 2 | N | X% |
| 3+ | N | X% |

### Pages with Excessive Outbound Links (>100)

| Page | Outbound Links |
|------|----------------|

## Data Sources

- Internal crawl via fetch_page.py + parse_html.py ([N] pages, [date])
- [Ahrefs MCP — if used]
```
