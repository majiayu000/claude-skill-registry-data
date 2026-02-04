---
name: crawl4ai
description: "Web crawling and content extraction to clean markdown files. Use this skill when the user wants to: (1) Crawl a website or webpage, (2) Extract and clean content from URLs, (3) Create markdown documentation from websites, (4) Analyze website structure before crawling, (5) Download website content including subpages. Typical triggers include 'crawl this website', 'extract content from URL', 'download this site as markdown', 'analyze website structure'."
---

# Crawl4AI - Website Crawling & Content Extraction

## Overview

This skill enables crawling entire websites and extracting clean, structured content with proper metadata separation. It uses an efficient **2-phase approach** that separates bulk crawling from content processing.

### Two-Phase Architecture

**Phase 1: Bulk Crawling** (`bulk_crawl.py`)
- Recursively crawls entire website tree (configurable depth)
- Parallel loading of multiple pages simultaneously
- Excludes nav/header/footer elements during crawl
- Saves raw data: `raw.html`, `raw.md`, `metadata.json`
- Fast and efficient - no per-page processing overhead

**Phase 2: Post-Processing** (`postprocess.py`)
- Processes all crawled pages offline
- Cleans markdown content (removes pagination, duplicates, nav remnants)
- Enriches metadata with AI (description, keywords) or heuristic methods
- Saves final: `content.md` (clean, NO frontmatter!) + enriched `metadata.json`
- Metadata stays in JSON - markdown stays pure

**Key Benefits:**
- **Separation of Concerns:** Crawling ≠ Processing
- **Scalability:** Crawl entire sites in parallel, process later
- **Flexibility:** Re-process data without re-crawling
- **Clean Output:** Markdown without frontmatter, metadata in JSON
- **Cost Efficient:** Batch AI calls for metadata generation

## Workflow

**For Single Pages:**
Use `crawl_to_markdown.py` for quick single-page extraction with intelligent content filtering.

**For Entire Websites (Recommended):**

**Step 1: Bulk Crawl**
```bash
python scripts/bulk_crawl.py <url> --output-dir ./site --max-depth 3
```
- Crawls entire website recursively
- Parallel loading of pages
- Saves raw data for all pages

**Step 2: Post-Process**
```bash
python scripts/postprocess.py ./site
```
- Cleans all markdown files
- Generates metadata with AI
- Creates final `content.md` + enriched `metadata.json` for each page

**Result:**
```
site/
  index/
    raw.html          # Original HTML (for reference)
    raw.md            # Original markdown from crawl4ai
    content.md        # ✨ Clean markdown (NO frontmatter!)
    metadata.json     # ✨ All metadata here
  about/
    raw.html
    raw.md
    content.md
    metadata.json
  ...
```

## Crawling Process

### Phase 1: Bulk Crawl (`bulk_crawl.py`)

Crawls an entire website recursively and saves raw data:

```bash
python scripts/bulk_crawl.py <url> [options]
```

**Parameters:**
- `<url>`: Start URL to crawl (required)
- `--output-dir PATH`: Output directory (default: ./crawled_site)
- `--max-depth N`: Maximum crawl depth (default: 3)
- `--wait-time N`: JavaScript wait time in seconds (default: 5.0)
- `--allow-external`: Allow crawling external domains (default: same-domain only)

**What it does:**
1. Starts from given URL
2. Extracts all internal links
3. Crawls pages in parallel (depth-first)
4. Excludes nav/header/footer during crawl
5. Saves for each page:
   - `raw.html` - Original HTML
   - `raw.md` - Raw markdown from crawl4ai
   - `metadata.json` - Basic metadata (url, title, links, crawled_at)

**Examples:**

Crawl entire site with max depth 3:
```bash
python scripts/bulk_crawl.py https://example.com --max-depth 3
```

Shallow crawl (only start page + direct links):
```bash
python scripts/bulk_crawl.py https://example.com --max-depth 1
```

### Phase 2: Post-Processing (`postprocess.py`)

Processes bulk-crawled data and generates final output:

```bash
python scripts/postprocess.py <crawled_dir> [options]
```

**Parameters:**
- `<crawled_dir>`: Directory with bulk-crawled data (required)
- `--no-ai`: Disable AI metadata generation (use heuristic methods)

**What it does:**
1. Finds all pages with `raw.md` files
2. For each page:
   - Cleans markdown (removes pagination, duplicates, nav remnants)
   - Generates description & keywords (AI or heuristic)
   - Detects language from HTML
   - Calculates content hash and token estimate
   - Saves `content.md` (clean, NO frontmatter!)
   - Enriches `metadata.json` with all metadata

**Examples:**

Post-process with AI (requires ANTHROPIC_API_KEY):
```bash
export ANTHROPIC_API_KEY=sk-ant-...
python scripts/postprocess.py ./crawled_site
```

Post-process without AI (heuristic methods):
```bash
python scripts/postprocess.py ./crawled_site --no-ai
```

### Legacy: Single-Page Crawl (`crawl_to_markdown.py`)

For quick single-page extraction (legacy mode):

```bash
python scripts/crawl_to_markdown.py <url> --output-dir ./output
```

**Note:** For multi-page sites, use the 2-phase approach (bulk_crawl.py + postprocess.py) instead.

## Metadata Structure

Metadata is stored separately in `metadata.json` (NO frontmatter in markdown!):

```json
{
  "url": "https://example.com/page",
  "crawled_at": "2025-11-04T15:18:23.075744",
  "title": "Page Title",
  "links": ["https://example.com/about", ...],
  "description": "AI-generated or heuristic description (1-2 sentences)",
  "keywords": ["keyword1", "keyword2", ...],
  "language": "en",
  "content_hash": "b2ddd73c87e2af...",
  "estimated_tokens": 1250,
  "processed_at": "2025-11-04T15:18:47.280333"
}
```

**Advantages:**
- **Clean Separation:** Content in `.md`, metadata in `.json`
- **Easy Processing:** Parse JSON without markdown parsing
- **Flexible:** Add metadata fields without touching content
- **Portable:** Markdown files work anywhere without frontmatter issues

## Content Cleaning

The script automatically removes:
- Navigation menus (main nav, submenu controls)
- Page headers and footers
- Pagination controls (1|2|3, Weiter, Zurück, etc.)
- Slider/carousel controls
- Duplicate sections
- Empty sections and excessive whitespace
- Menu/navigation links

It preserves:
- Main content text and headings
- Content links relevant to the topic
- Images within the main content
- Structured data (lists, tables where present)
- Proper markdown formatting

## Output Structure

### 2-Phase Approach Output

```
crawled_site/
├── crawl_summary.json    # Summary of crawl (total pages, urls, etc.)
├── index/
│   ├── raw.html          # Original HTML from crawl
│   ├── raw.md            # Original markdown from crawl4ai
│   ├── content.md        # ✨ Clean content (after post-processing)
│   └── metadata.json     # ✨ All metadata (enriched after post-processing)
├── about/
│   ├── raw.html
│   ├── raw.md
│   ├── content.md
│   └── metadata.json
└── contact/
    ├── raw.html
    ├── raw.md
    ├── content.md
    └── metadata.json
```

**File Roles:**
- `raw.html` - Reference/debugging, contains original HTML
- `raw.md` - Raw output from crawl4ai (before cleaning)
- `content.md` - **Final clean markdown** (NO frontmatter!)
- `metadata.json` - **All metadata** (title, description, keywords, etc.)

### Legacy Single-Page Output

```
crawled_site/
└── index.md              # Content + frontmatter (legacy mode)
```

## Usage Workflow

### Recommended: 2-Phase Workflow

**Step 1: Bulk Crawl**
```bash
# Crawl entire website
python scripts/bulk_crawl.py https://example.com --max-depth 3 --output-dir ./mysite
```

**Step 2: Post-Process**
```bash
# Process all pages
export ANTHROPIC_API_KEY=sk-ant-...  # Optional, for AI metadata
python scripts/postprocess.py ./mysite
```

**Result:** Clean `content.md` + enriched `metadata.json` for each page!

### Quick Single-Page Extraction (Legacy)

```bash
# For single pages only
python scripts/crawl_to_markdown.py https://example.com
```

### Advanced Options

**Control crawl depth:**
```bash
python scripts/bulk_crawl.py https://example.com --max-depth 2  # Shallow crawl
```

**JavaScript-heavy sites:**
```bash
python scripts/bulk_crawl.py https://example.com --wait-time 10.0
```

**Skip AI metadata generation:**
```bash
python scripts/postprocess.py ./mysite --no-ai  # Use heuristic methods
```

## KI-gestützte Metadaten (Optional)

Der Skill kann **Claude Haiku** nutzen, um intelligente Descriptions und Keywords zu generieren.

### Mit KI (Empfohlen):
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

**Vorteile:**
- Intelligente, kontextbezogene Descriptions
- Semantisch sinnvolle Keywords mit korrekter Großschreibung
- Versteht den Inhalt und fasst ihn zusammen

**Kosten:** ~0.2 Cent pro Seite (Claude Haiku)

### Ohne KI (Fallback):
Wenn kein API-Key gesetzt ist, nutzt der Skill automatisch heuristische Methoden:
- Extrahiert erste substantielle Textzeile als Description
- Ermittelt Keywords nach Häufigkeit
- Funktioniert gut, aber weniger präzise

**Der Skill zeigt beim Start an, welcher Modus verwendet wird:**
- `✨ KI-Metadaten-Generierung aktiviert (Claude Haiku)` - KI wird genutzt
- `ℹ️  KI-Metadaten-Generierung nicht verfügbar` - Fallback-Methoden werden genutzt

## Installation Requirements

The crawl4ai library must be installed in a virtual environment. If the venv doesn't exist yet, create and install:

```bash
# Navigate to skill directory
cd /Users/tobiasbrummer/.claude/skills/crawl4ai

# Create virtual environment (if not exists)
python3 -m venv venv

# Activate and install crawl4ai
source venv/bin/activate
pip install crawl4ai

# Install anthropic for KI-based metadata generation (optional but recommended)
pip install anthropic

# Install playwright browsers (one-time setup)
playwright install chromium
```

**Important:** All scripts must be run using the venv's Python interpreter:
```bash
/Users/tobiasbrummer/.claude/skills/crawl4ai/venv/bin/python3 scripts/crawl_to_markdown.py <url>
```

See `references/crawl4ai_reference.md` for detailed API documentation.

## Common Issues and Solutions

**Issue: Pages taking too long**
- Reduce `--wait-time` if site doesn't need much JavaScript
- Increase `--wait-time` if content is missing (up to 10s for heavy JS sites)

**Issue: Wrong content extracted**
- The script uses intelligent heuristics to find main content
- If it picks the wrong element, the site may have unusual structure
- Check the console output to see what selector was used

**Issue: Missing content**
- Some sites may need longer `--wait-time` for JavaScript
- Try increasing from 5s to 8-10s for dynamic content
- Check if site requires authentication (not supported)

**Issue: Still seeing some navigation**
- The 3-stage cleaning is aggressive but may miss some edge cases
- The script will continuously improve pattern matching
- Most navigation is successfully removed (85-95% reduction typical)

## Tips for Best Results

1. **Default settings work well** for most sites
2. **Check token estimate** in output to verify content size
3. **Content hash in frontmatter** allows easy change detection for re-crawls
4. **Review the extracted content** to ensure quality
5. **Adjust wait-time** for JavaScript-heavy sites
6. **Use descriptive output directories** when crawling multiple pages
