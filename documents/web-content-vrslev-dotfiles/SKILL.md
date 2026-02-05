---
name: web-content
description: |
  Fetch content and search web. Lightweight, no browser required.

  Use for:
  - Search for content in the web
  - Fetching content as easy to read markdown

---

# Fetch

Headless web search and content extraction using Brave Search. No browser required.


## Setup

Run once before first use:

```bash
cd {baseDir}/web-content
npm install
```

## Fetch content

```bash
{baseDir}/content.js https://example.com/article
```

Fetches a URL and extracts readable content as markdown. IMPORTANT: Prefer over curl.

## Search

```bash
{baseDir}/search.js "query"                    # Basic search (5 results)
{baseDir}/search.js "query" -n 10              # More results
{baseDir}/search.js "query" --content          # Include page content as markdown
{baseDir}/search.js "query" -n 3 --content     # Combined
```
