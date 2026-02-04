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

## Troubleshooting

### Crawl succeeds but output is blank

Some sites don't match the default `--selector` and can return empty/whitespace Markdown.
The script will retry without CSS selection automatically, but you can also force it explicitly:

```bash
uv run scripts/crawl_to_markdown.py --selector '' https://example.com
```

### uv cache permission errors

If `uv` fails accessing its cache directory (e.g. `~/.cache/uv`), either point it at a
writable cache directory:

```bash
uv --cache-dir .uv-cache run scripts/crawl_to_markdown.py https://example.com
```

Or avoid the cache entirely:

```bash
uv --no-cache run scripts/crawl_to_markdown.py https://example.com
```

## Output format

For each URL, the script prints a header and raw Markdown content:

```
URL: https://example.com
<raw markdown>
---
```

If a crawl fails, the output includes an error block for that URL.
