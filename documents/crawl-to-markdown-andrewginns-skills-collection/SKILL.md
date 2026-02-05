---
name: crawl-to-markdown
description: Use when web.run fails to parse a webpage and you need raw Markdown via Crawl4AI.
---

Use this skill only after the built-in `web.run` tool fails to return usable content for a page.

## What this skill does

- Crawls one or more URLs with Crawl4AI.
- Returns raw Markdown for each URL.

## How to run

This script uses uv inline metadata. If `uv` is available just run:

```bash
uv run scripts/crawl_to_markdown.py https://example.com
```

Multiple URLs:

```bash
uv run scripts/crawl_to_markdown.py https://example.com https://example.org
```

Or pipe a newline-delimited list:

```bash
printf "https://example.com\nhttps://example.org\n" | uv run scripts/crawl_to_markdown.py
```

## Output format

For each URL, the script prints a header and raw Markdown content:

```
URL: https://example.com
<raw markdown>
---
```

If a crawl fails, the output includes an error block for that URL.
