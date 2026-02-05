---
name: website-crawler
description: Crawl and ingest websites into whorl. Use when scraping a personal site, blog, or extracting web content for the knowledge base.
allowed-tools: Bash, Read, Write
---

# Website Crawler for Whorl

Crawl websites and ingest content into your whorl knowledge base.

## Prerequisites

Install trafilatura if not already available:
```bash
pip install trafilatura
```

## Single Page

Extract a single page and save to whorl docs:

```bash
# Extract content as markdown
trafilatura -u "https://example.com/page" --markdown > ~/.whorl/docs/page-name.md
```

Or with metadata in frontmatter:
```bash
URL="https://example.com/page"
SLUG=$(echo "$URL" | sed 's|https\?://||; s|/|_|g; s|_$||')
OUTPUT=~/.whorl/docs/"$SLUG".md

# Fetch and extract
CONTENT=$(trafilatura -u "$URL" --markdown)
TITLE=$(trafilatura -u "$URL" --json | python3 -c "import sys,json; print(json.load(sys.stdin).get('title','Untitled'))" 2>/dev/null || echo "Untitled")

# Write with frontmatter
cat > "$OUTPUT" << EOF
---
title: "$TITLE"
source_url: $URL
fetched_at: $(date -u +%Y-%m-%dT%H:%M:%SZ)
---

$CONTENT
EOF

echo "Saved to $OUTPUT"
```

## Crawl Entire Site

Crawl up to 30 pages from a site:
```bash
trafilatura --crawl "https://example.com" --markdown -o ~/.whorl/docs/site-name/
```

Or with sitemap:
```bash
trafilatura --sitemap "https://example.com/sitemap.xml" --markdown -o ~/.whorl/docs/site-name/
```

## Crawl with Custom Limit

For more control, use Python:
```python
import os
from pathlib import Path
from datetime import datetime, timezone
import trafilatura
from trafilatura.spider import focused_crawler

WHORL_DOCS = Path.home() / ".whorl" / "docs"
site_dir = WHORL_DOCS / "my-site"
site_dir.mkdir(parents=True, exist_ok=True)

for url in focused_crawler("https://example.com", max_seen_urls=50):
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        continue

    content = trafilatura.extract(downloaded, output_format='markdown')
    metadata = trafilatura.extract_metadata(downloaded)

    if not content:
        continue

    # Generate filename from URL
    slug = url.split("//")[-1].replace("/", "_").rstrip("_")[:80]
    filepath = site_dir / f"{slug}.md"

    # Write with frontmatter
    title = metadata.title if metadata else "Untitled"
    frontmatter = f"""---
title: "{title}"
source_url: {url}
fetched_at: {datetime.now(timezone.utc).isoformat()}
---

"""
    filepath.write_text(frontmatter + content)
    print(f"+ {filepath.name}")
```

## After Crawling

Run whorl sync to process new documents with ingestion agents:
```bash
whorl sync
```

Or if running locally without auth:
```bash
curl -X POST http://localhost:8000/api/sync
```

## Tips

- **Rate limiting**: trafilatura respects robots.txt and has built-in politeness
- **Deduplication**: whorl's hash index will detect duplicate content
- **Binary files**: PDFs and images should be downloaded separately with `curl -O`
- **Large sites**: Use `max_seen_urls` to limit scope, or target specific sitemaps
