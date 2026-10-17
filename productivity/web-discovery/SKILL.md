---
name: web-discovery
description: Browser-first web discovery workflow for AI agents. Use when web_search APIs are unavailable or undesired, and you need human-like search results from engines like Google or Brave using browser automation, then pass selected URLs into the web-scraping skill for extraction and synthesis.
---

# Web Discovery (Browser-first)

Use this when you want real SERP behavior instead of search APIs.

## Workflow

1. Open browser and run searches on `google.com` and/or `search.brave.com`.
2. Collect top result URLs (skip ads, dedupe by normalized URL/domain).
3. Save URLs to a temp file.
4. Run `scripts/batch_scrape.py` to extract concise content via `skills/web-scraping/scripts/auto_scrape.py`.
5. Summarize findings with source links.

## Browser guidance

- Use browser snapshots to capture result links quickly.
- Prefer top 5-10 strong results per query.
- Skip obvious low-value pages (tag pages, doorway pages, duplicate mirrors).

## Batch extraction

```bash
python3 skills/web-discovery/scripts/batch_scrape.py \
  --input /tmp/urls.txt \
  --output /tmp/scrape-results.jsonl \
  --limit 12
```

Input format (`/tmp/urls.txt`): one URL per line.

## Defaults

- Keep context small: extract targeted text, not raw HTML, unless requested.
- Fail soft: continue scraping remaining URLs if one fails.
- Reuse method memory from `skills/web-scraping/data/site_profiles.csv` automatically via `auto_scrape.py`.
