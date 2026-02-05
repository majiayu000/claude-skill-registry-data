---
name: content-ingestion
description: Ingest web content into Kurt. Map sitemaps to discover URLs, then fetch content selectively.
---

# Content Ingestion

## Overview

This skill enables efficient web content ingestion with a map-then-fetch workflow. Discover URLs from sitemaps first, review what was found, then selectively download only the content you need. Supports single document fetching and fast parallel batch downloads.

Content is extracted as markdown with metadata (title, author, date, categories) and stored in the `sources/` directory.

## Quick Start

```bash
# 1. Discover URLs from sitemap (fast, no downloads)
kurct content map https://www.anthropic.com

# 1a. OR discover with publish dates (slower, extracts dates from blogrolls)
kurct content map https://docs.getdbt.com/sitemap.xml --discover-dates

# 2. Review what was found
kurt content list --status NOT_FETCHED

# 3. Fetch content (parallel batch)
kurct content fetch --url-prefix https://www.anthropic.com/
```

## Map-Then-Fetch Workflow

**Why two steps?**
- Sitemaps often contain hundreds or thousands of URLs
- Map step is fast (no downloads) - lets you review before committing
- Fetch step is slow (downloads + extraction) - run selectively
- Saves time, bandwidth, and storage

**Three-step process:**
1. **Map**: Discover URLs and create `NOT_FETCHED` records
2. **Review**: Examine discovered URLs using document management commands
3. **Fetch**: Download content selectively (single or batch)

### Integration with Iterative Source Gathering

**When invoked from `/create-project` or `/resume-project`**, use map-then-fetch to provide preview:

1. **Map first** - Show user what URLs were discovered
   ```bash
   kurct content map https://docs.example.com
   echo "Discovered X URLs. Preview:"
   kurt content list --url-prefix https://docs.example.com --status NOT_FETCHED | head -10
   ```

2. **Get approval** - Ask if user wants to fetch all or selective
   ```
   Found 150 URLs from docs.example.com

   Preview (first 10):
   1. https://docs.example.com/quickstart
   2. https://docs.example.com/api/authentication
   ...

   Fetch all 150 pages? Or selective? (all/selective/cancel)
   ```

3. **Fetch approved content**
   ```bash
   # If all:
   kurct content fetch --url-prefix https://docs.example.com

   # If selective (user specifies path pattern):
   kurct content fetch --url-prefix https://docs.example.com/api/
   ```

This provides **Checkpoint 1** (preview) for the iterative source gathering pattern.

## Core Operations

### Map Sitemap URLs

Discover URLs from sitemaps without downloading content.

```bash
# Discover all URLs from sitemap
kurct content map https://www.anthropic.com

# Discover with publish dates from blogrolls (recommended for blogs/docs)
kurct content map https://docs.getdbt.com/sitemap.xml --discover-dates

# Limit discovery (useful for testing)
kurct content map https://example.com --limit 10

# Map and fetch immediately
kurct content map https://example.com --fetch

# Discover dates with custom blogroll limit
kurct content map https://example.com --discover-dates --max-blogrolls 5

# JSON output for scripts
kurct content map https://example.com --output json
```

**What happens:**
- Automatically finds sitemap URLs (checks `/sitemap.xml`, `robots.txt`, etc.)
- Creates database records with `NOT_FETCHED` status
- Skips duplicate URLs gracefully
- Returns list of discovered documents

**Example output:**
```
✓ Found 317 URLs from sitemap
  Created: 317 new documents

  ✓ https://www.anthropic.com
     ID: 6203468a | Status: NOT_FETCHED
  ✓ https://www.anthropic.com/news/claude-3-7-sonnet
     ID: bc2bcf48 | Status: NOT_FETCHED
```

### Discovering Publish Dates from Blogrolls

**When to use `--discover-dates`:**
- Content freshness is critical (tutorials, documentation, blog posts)
- You need to identify outdated content for updates
- Building a chronological content inventory
- Working with blogs, changelogs, or release notes

**How it works:**
1. Maps sitemap normally (all URLs)
2. Uses LLM to identify blog indexes, changelogs, release notes pages
3. Scrapes those pages to extract individual post URLs + dates
4. Creates/updates document records with `published_date` populated
5. Marks discovered posts with `is_chronological=True` and `discovery_method="blogroll"`

**Example:**
```bash
# Discover docs.getdbt.com with date extraction
kurct content map https://docs.getdbt.com/sitemap.xml --discover-dates

# Output shows date discovery:
# ✓ Found 500 URLs from sitemap
# --- Discovering blogroll/changelog pages ---
# Found 8 potential blogroll/changelog pages
#
# Scraping https://docs.getdbt.com/blog...
#   Found 45 posts with dates
# Scraping https://docs.getdbt.com/docs/dbt-versions/...
#   Found 23 posts with dates
#
# ✓ Total documents discovered from blogrolls: 68
#   New: 12 (not in sitemap)
#   Existing: 56 (enriched with dates)
```

**Performance:**
- Regular mapping: ~2-5 seconds (just sitemap parsing)
- With `--discover-dates`: ~5-15 minutes (includes LLM analysis + page scraping)
- Controlled with `--max-blogrolls` (default: 10 pages)

**Benefits:**
- Dates captured upfront (before fetch)
- Discovers additional posts not in sitemap
- Enriches existing records with publish dates
- Enables date-based filtering and relevance tracking

### Troubleshooting: Sitemap Discovery Failures

If automatic discovery fails with "No sitemap found," use this fallback workflow:

#### Tier 1: Try Common Sitemap Paths Directly

Most sites use standard paths. Try these **directly** (not base URL):

```bash
# Standard path (most common)
kurct content map https://docs.getdbt.com/sitemap.xml

# Alternative paths
kurct content map https://docs.getdbt.com/sitemap_index.xml
kurct content map https://docs.getdbt.com/sitemap/sitemap.xml
kurct content map https://docs.getdbt.com/sitemaps/sitemap.xml
```

**Success if:** Kurt finds and processes the sitemap
**Next if fails:** Try Tier 2

#### Tier 2: Check robots.txt

Use WebFetch to find sitemap URL in robots.txt:

```
WebFetch URL: https://docs.getdbt.com/robots.txt
Prompt: "Extract all Sitemap URLs from this robots.txt file"
```

Then try the discovered sitemap URLs:
```bash
kurct content map <sitemap-url-from-robots>
```

**Success if:** Sitemap URL found in robots.txt works
**Next if fails:** Try Tier 3

#### Tier 3: Search for Sitemap

Use WebSearch to discover sitemap location:

```
WebSearch: "site:docs.getdbt.com sitemap"
WebSearch: "docs.getdbt.com sitemap.xml"
```

Or check common documentation pages for sitemap links.

Then try discovered URLs with `kurct content map`

**Success if:** Sitemap found via search
**Next if fails:** Try Tier 4

#### Tier 4: Manual URL Collection

If no sitemap exists or is inaccessible, manually collect URLs:

**Option A: Use WebSearch to find pages**
```
WebSearch: "site:docs.getdbt.com tutorial"
WebSearch: "site:docs.getdbt.com guide"
```

**Option B: Crawl from homepage**
- Use WebFetch on homepage
- Extract navigation links
- Add each URL manually

**Option C: User provides URL list**
- Ask user for key URLs to ingest
- Import from CSV or list

Then add URLs manually:
```bash
kurct content add https://docs.getdbt.com/page1
kurct content add https://docs.getdbt.com/page2
kurct content add https://docs.getdbt.com/page3
```

#### Real Example: docs.getdbt.com

```bash
# ❌ Automatic discovery fails
kurct content map https://docs.getdbt.com
# Error: No sitemap found

# ✅ Direct sitemap URL works!
kurct content map https://docs.getdbt.com/sitemap.xml --limit 100
# Success: Found 100 URLs from sitemap
```

#### Quick Diagnostic Commands

**Test if sitemap exists:**
```bash
# Use WebFetch to check
WebFetch URL: https://example.com/sitemap.xml
Prompt: "Does this sitemap exist? If yes, describe its structure."
```

**Why automatic discovery fails:**
- Anti-bot protection (site blocks trafilatura but not WebFetch)
- Sitemap not in robots.txt
- Non-standard sitemap location
- Dynamic/JavaScript-rendered sitemaps

**When to use each tier:**
- **Tier 1**: Always try first (5 seconds to test)
- **Tier 2**: Standard sites with robots.txt (1 minute)
- **Tier 3**: Unusual configurations (2-3 minutes)
- **Tier 4**: No sitemap or heavily protected sites (ongoing)

### Fetch Single Document

Download content for a specific document.

```bash
# Fetch by document ID
kurct content fetch 6203468a-e3dc-48f2-8e1f-6e1da34dab05

# Fetch by URL (creates document if needed)
kurct content fetch https://www.anthropic.com/company
```

**What happens:**
- Downloads HTML content
- Extracts markdown with trafilatura
- Saves to `sources/{domain}/{path}/page.md`
- Updates database: `FETCHED` status, content metadata
- Returns document details

### Batch Fetch Documents

Download multiple documents in parallel (5-10x faster than sequential).

```bash
# Fetch all from domain
kurct content fetch --url-prefix https://www.anthropic.com/

# Fetch all blog posts
kurct content fetch --url-contains /blog/

# Fetch everything NOT_FETCHED
kurct content fetch --all

# Increase parallelism (default: 5)
kurct content fetch --url-prefix https://example.com/ --max-concurrent 10

# Retry failed documents
kurct content fetch --status ERROR --url-prefix https://example.com/
```

**What happens:**
- Fetches documents concurrently (default: 5 parallel)
- Uses async httpx for fast downloads
- Extracts metadata: title, author, date, categories, language
- Stores content fingerprint for deduplication
- Updates all document records in batch

**Performance:**
- Sequential: ~2-3 seconds per document
- Parallel (5 concurrent): ~0.4-0.6 seconds per document
- Example: 82 documents in ~10 seconds vs ~3 minutes

**File structure after fetch:**
```
sources/
└── www.anthropic.com/
    ├── news/
    │   └── claude-3-7-sonnet.md
    └── company.md
```

## Alternative: Manual URL Addition

When sitemap discovery fails or you want to add specific URLs.

### Add Single URLs

```bash
# Add URL without fetching
kurct content add https://example.com/page1
kurct content add https://example.com/page2

# Then fetch when ready
kurct content fetch https://example.com/page1
```

### Direct Fetch (Add + Fetch)

Create document record and fetch content in one step.

```bash
# Creates document if doesn't exist, then fetches
kurct content fetch https://example.com/specific-page
```

## WebFetch Fallback (When Kurt Fetch Fails)

If `kurct content fetch` fails due to anti-bot protection or other issues, use WebFetch as a fallback with automatic import.

### Workflow

1. **Attempt Kurt fetch first** (creates ERROR record if it fails)
2. **Use WebFetch to retrieve content with metadata**
3. **Save with YAML frontmatter**
4. **Auto-import hook handles the rest**

### WebFetch with Metadata Extraction

When using WebFetch, extract FULL metadata to preserve in the file:

```
Use WebFetch with this prompt:
"Extract ALL metadata from this page including:
- Full page title
- Description / meta description
- Author(s)
- Published date or last modified date
- Any structured data or meta tags
- The complete page content as markdown

Format the response to clearly show:
1. All metadata fields found
2. The markdown content"
```

### Save Content with Frontmatter

Save the fetched content with YAML frontmatter:

```markdown
---
title: "Full Page Title from WebFetch"
url: https://example.com/page
description: "Meta description or summary"
author: "Author Name or Organization"
published_date: "2025-10-22"
last_modified: "2025-10-22"
fetched_via: WebFetch
fetched_at: "2025-10-23"
---

# Page Content

[Markdown content from WebFetch...]
```

### Auto-Import Process

Once the file is saved to `/sources/`, the PostToolUse hook automatically:

1. Detects the new .md file
2. Finds the ERROR record in Kurt DB
3. Updates status to FETCHED
4. **Parses frontmatter and populates metadata fields**
5. Links the file to the database record
6. Runs metadata extraction (kurt index)
7. Shows confirmation message

**Result:** File is fully indexed in Kurt with proper title, author, dates, and description!

### Example: Complete WebFetch Fallback

```bash
# 1. Kurt fetch fails
kurct content fetch https://docs.example.com/guide
# → Creates ERROR record

# 2. Use WebFetch (Claude does this automatically)
# Extracts metadata + content

# 3. Save with frontmatter to sources/
# File: sources/docs.example.com/guide.md

# 4. Auto-import hook triggers
# → Updates ERROR record to FETCHED
# → Populates title, author, date from frontmatter
# → Links file to database

# 5. Verify
kurt content get-metadata <doc-id>
# Shows proper title, metadata, FETCHED status
```

### Benefits of WebFetch with Frontmatter

- ✅ Preserves all page metadata (title, author, dates)
- ✅ Automatic import via hook
- ✅ No manual database updates needed
- ✅ Content is queryable and searchable
- ✅ Metadata extraction works same as native fetch
- ✅ Transparent fallback - just works!

## Advanced Usage

For custom extraction behavior beyond the CLI, use trafilatura Python library directly.

### Custom Crawling

Control crawl depth, URL patterns, language filters, and more.

```python
# See scripts/advanced_crawl_and_import.py
from trafilatura.spider import focused_crawler

todo = focused_crawler(
    homepage,
    max_seen_urls=100,
    max_known_urls=50
)
```

[Trafilatura Crawls Documentation](https://trafilatura.readthedocs.io/en/latest/crawls.html)

### Custom Extraction Settings

Fine-tune extraction: precision vs recall, include comments, handle tables.

```python
# See scripts/advanced_fetch_custom_extraction.py
from trafilatura import extract

content = extract(
    html,
    include_comments=False,
    include_tables=True,
    favor_precision=True
)
```

[Trafilatura Core Functions](https://trafilatura.readthedocs.io/en/latest/corefunctions.html)

### Custom Extraction Config

Configure timeouts, minimum text size, date extraction.

```python
# See scripts/custom_extraction_config.py
from trafilatura.settings import use_config

config = use_config()
config.set('DEFAULT', 'MIN_EXTRACTED_SIZE', '500')
```

[Trafilatura Settings](https://trafilatura.readthedocs.io/en/latest/corefunctions.html#extraction-settings)

## Quick Reference

| Task | Command | Performance |
|------|---------|-------------|
| Map sitemap | `kurct content map <url>` | Fast (no downloads) |
| Map with dates | `kurct content map <url> --discover-dates` | ~5-15 min (LLM scraping) |
| Fetch single | `kurct content fetch <id\|url>` | ~2-3s per doc |
| Batch fetch | `kurct content fetch --url-prefix <url>` | ~0.4-0.6s per doc |
| Add URL | `kurct content add <url>` | Instant |
| Review discovered | `kurt content list --status NOT_FETCHED` | Instant |
| Retry failures | `kurct content fetch --status ERROR` | Varies |

## Python API

```python
# URL Discovery
from kurt.ingest_map import (
    map_sitemap,              # Discover URLs from sitemap
    map_blogrolls,            # Discover from blogroll/changelog pages
    identify_blogroll_candidates,  # Find potential blogroll pages
    extract_chronological_content,  # Extract posts with dates
)

# Content Fetching
from kurt.ingest_fetch import (
    add_document,             # Add single URL
    fetch_document,           # Fetch single document
    fetch_documents_batch,    # Batch fetch (async parallel)
)

# Map sitemap
docs = map_sitemap("https://example.com", limit=100)

# Add document
doc = add_document("https://example.com/page")

# Fetch single
result = fetch_document(document_id="abc-123")

# Batch fetch
results = fetch_documents_batch(
    document_ids=["abc-123", "def-456"],
    max_concurrent=10
)
```

See:
- [ingest_map.py](https://github.com/boringdata/kurt-core/blob/main/src/kurt/ingest_map.py) - URL discovery
- [ingest_fetch.py](https://github.com/boringdata/kurt-core/blob/main/src/kurt/ingest_fetch.py) - Content fetching

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No sitemap found" | **See detailed guide above**: Try direct sitemap URLs (`.../sitemap.xml`), check robots.txt, or use WebSearch. Full 4-tier fallback documented in "Troubleshooting: Sitemap Discovery Failures" section. |
| Slow batch fetch | Increase `--max-concurrent` (default: 5, try 10) |
| Extraction quality low | See advanced extraction scripts for custom settings |
| Duplicate content | Kurt automatically deduplicates using content hashes |
| Rate limiting | Reduce `--max-concurrent` or add delays |
| Content fetch fails | Use WebFetch fallback with frontmatter (see "WebFetch Fallback" section) |

## Next Steps

- For document management, see **document-management-skill**
- For custom extraction, see [scripts/](scripts/) directory
- For trafilatura details, see [Trafilatura Documentation](https://trafilatura.readthedocs.io/)
