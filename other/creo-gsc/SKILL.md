---
name: creo-gsc
description: >
  Google Search Console analysis and comprehensive SEO auditing.
  Site crawling, PageSpeed Insights, indexing API, on-page analysis,
  schema validation, hreflang, security headers, content quality, mobile SEO.
  Uses the GSC API where it can and opens the Search Console web UI in the
  user's browser where the API cannot (drilldowns, Validate Fix, settings).
  Requires gsc-analyzer extension.
  Triggers on: /creo gsc, Google Search Console, GSC, site audit, open GSC.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - mcp__claude-in-chrome__tabs_context_mcp
  - mcp__claude-in-chrome__tabs_create_mcp
  - mcp__claude-in-chrome__navigate
  - mcp__claude-in-chrome__computer
  - mcp__claude-in-chrome__read_page
  - mcp__claude-in-chrome__find
  - mcp__claude-in-chrome__get_page_text
---

# Creo GSC - Google Search Console & SEO Analysis

## Commands

| Command | Description |
|---------|-------------|
| `/creo gsc list-sites` | List all Search Console properties |
| `/creo gsc inspect <url>` | Inspect a URL's indexation status |
| `/creo gsc analytics` | Get search analytics (clicks, impressions, CTR) |
| `/creo gsc security <url>` | Analyze HTTP security headers |
| `/creo gsc onpage <url>` | On-page SEO analysis (title, meta, headings, images) |
| `/creo gsc schema <url>` | Validate structured data (JSON-LD) |
| `/creo gsc hreflang <url>` | Validate hreflang implementation |
| `/creo gsc full-seo <url>` | Run all 9 page analyzers on a URL |
| `/creo gsc site-audit <url>` | Crawl and audit entire website |
| `/creo gsc ui-export` | Export Page Indexing drilldown CSVs via Playwright (UI-only data the API cannot enumerate) |
| `/creo gsc validate-fix` | Click GSC's "Validate Fix" button via Playwright (no API exists for it) |
| `/creo gsc open [<surface>]` | Open a Search Console report in the user's browser (overview, performance, indexing, sitemaps, settings, inspect <url>) and read/operate it together |

## Browser-first operation

The API is preferred for data it can serve, but this skill is NOT API-only.
With browser tools available, open Search Console directly in the user's
signed-in Chrome — navigate to the exact report via the deep-link map in the
agent doc, read it, click drilldowns, export CSVs, and perform configuration
(submit sitemaps, manage users) together with the user. The user must already
be signed in; never attempt a scripted Google login; confirm before any
destructive click. Use the UI as ground truth whenever API results look wrong.

## Running gsc_toolkit CLI Commands

The toolkit is a Python package. All commands are executed via:

```bash
# Find the installed toolkit
GSC_DIR="${HOME}/.claude/skills/creo-gsc"

# Activate the virtual environment (if installed with venv)
source "${GSC_DIR}/.venv/bin/activate" 2>/dev/null || true

# Run commands
python -m gsc_toolkit <command> [options]
```

If the venv is not available, ensure gsc_toolkit's parent directory is on PYTHONPATH:

```bash
PYTHONPATH="${GSC_DIR}:${PYTHONPATH}" python -m gsc_toolkit <command>
```

## Full Command Reference

### GSC API Commands (require service account)

```bash
python -m gsc_toolkit list-sites
python -m gsc_toolkit inspect <url>
python -m gsc_toolkit analytics [--days 28] [--dimension query|page|device|country]
python -m gsc_toolkit sitemaps
python -m gsc_toolkit batch-inspect <urls_file>
python -m gsc_toolkit coverage [--path <directory>]
python -m gsc_toolkit links [--path <directory>]
python -m gsc_toolkit cwv <url> [--strategy mobile|desktop]
python -m gsc_toolkit cwv-batch <urls_file>
python -m gsc_toolkit index-request <url>
python -m gsc_toolkit index-batch <sitemap_url> [--limit 200]
python -m gsc_toolkit full-report [--days 28]
python -m gsc_toolkit seo-audit [--days 28] [--urls-file <file>]
```

### Page Analysis Commands (no API required)

```bash
python -m gsc_toolkit security <url>
python -m gsc_toolkit onpage <url>
python -m gsc_toolkit schema <url>
python -m gsc_toolkit hreflang <url> [--no-return-check]
python -m gsc_toolkit robots <base_url>
python -m gsc_toolkit sitemap-check <sitemap_url>
python -m gsc_toolkit full-seo <url>
```

### Content & Quality Analysis (no API required)

```bash
python -m gsc_toolkit content <url>
python -m gsc_toolkit mobile <url>
python -m gsc_toolkit performance <url>
python -m gsc_toolkit url-analysis <url>
```

### Site-wide Analysis (no API required)

```bash
python -m gsc_toolkit site-audit <url> [--max-pages 500] [--max-depth 10] [--delay 0.2] [--output file.json]
```

## Available Analyzers

1. **SecurityAnalyzer** - HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy
2. **OnPageAnalyzer** - Title, meta description, canonical, headings, content length, images, Open Graph, Twitter Cards
3. **SchemaAnalyzer** - JSON-LD validation, required/recommended fields, schema.org compliance
4. **HreflangAnalyzer** - Tag syntax, self-referential links, return link validation, x-default, language codes
5. **RobotsAnalyzer** - robots.txt syntax, directives, sitemap declarations, Googlebot blocking detection
6. **ContentAnalyzer** - Readability (Flesch-Kincaid, Gunning Fog), freshness, language detection, keyword analysis
7. **MobileAnalyzer** - Viewport, touch targets, font sizes, responsive design, PWA features
8. **PerformanceAnalyzer** - Render-blocking CSS/JS, image optimization, caching headers, compression
9. **LinksAnalyzer** - Anchor text quality, URL structure, pagination, nofollow detection
10. **SiteCrawler** + **SiteAuditor** - Full site crawl with duplicate detection, thin content, orphan pages, broken links
11. **PageSpeedAnalyzer** - Core Web Vitals via PageSpeed Insights API
12. **IndexingAPI** - Request indexing via Google Indexing API
13. **CoverageAnalyzer** - Parse GSC Coverage CSV exports
14. **GSCAnalyzer** - Main Search Console API client (analytics, inspection, sitemaps)

## Configuration

For GSC API access, set environment variables or create `.env` in the working directory:

```
GSC_KEY_FILE=./service-account-key.json
GSC_SITE_URL=sc-domain:your-domain.com
GSC_DEFAULT_DAYS=28
PAGESPEED_API_KEY=your_api_key
GSC_OUTPUT_DIR=./output
```

Page analysis commands (security, onpage, schema, hreflang, robots, content, mobile, performance, url-analysis, full-seo, site-audit) do not require any API credentials.

## UI-only Surfaces (no API exists)

The Search Console API cannot enumerate Page Indexing drilldown example URLs,
and there is no API for the "Validate Fix" button. Two Playwright scripts in
the extension's `scripts/` directory cover these:

```bash
# One-time headed login (shared persistent profile), then recurring exports:
GSC_SITE_URL="sc-domain:example.com" node scripts/gsc_ui_export.mjs --setup
GSC_SITE_URL="sc-domain:example.com" node scripts/gsc_ui_export.mjs --out=./gsc-exports

# Click "Validate Fix" for issue classes whose fix is live:
GSC_SITE_URL="sc-domain:example.com" node scripts/gsc_validate_fix.mjs --dry-run
GSC_SITE_URL="sc-domain:example.com" node scripts/gsc_validate_fix.mjs --issues="Not found (404),Server error (5xx)"
```

Requires Playwright in the working project (`npm i -D playwright && npx
playwright install chromium`). Exit code 2 means the saved Google session
expired - re-run `--setup`. Full workflow details, the stable drilldown
item_key table, and export-handling gotchas are in the agent doc
(`agents/creo-gsc.md`, "GSC UI-only surfaces").
