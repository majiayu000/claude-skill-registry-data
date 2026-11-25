---
name: obscura
description: Web scraping and automation using the Obscura headless browser.
---

# Obscura Headless Browser

Obscura is a lightweight headless browser engine built in Rust for web scraping and AI agent automation. It bypasses bot protections, runs real JavaScript, and uses minimal resources.

It is available in the system PATH as `obscura`.

## Fetch a page

Use `obscura fetch` to render a single page.

```bash
# Get the page title
obscura fetch https://example.com --eval "document.title"

# Extract all links
obscura fetch https://example.com --dump links

# Render JavaScript and dump HTML
obscura fetch https://news.ycombinator.com --dump html

# Dump plain text (good for LLM context)
obscura fetch https://example.com --dump text

# Wait for dynamic content
obscura fetch https://example.com --wait-until networkidle0

# Wait for a specific element
obscura fetch https://example.com --selector ".my-dynamic-element"

# Stealth mode (anti-detection for Cloudflare/Datadome)
obscura fetch https://example.com --stealth --dump text

# Quiet mode (suppresses the banner output)
obscura fetch https://example.com --quiet --dump text
```

## Scrape in parallel

Use `obscura scrape` to extract data from multiple URLs simultaneously.

```bash
obscura scrape url1 url2 url3 \
  --concurrency 5 \
  --eval "document.querySelector('h1').textContent" \
  --format json
```

## Tips for AI Agents

1. When you need to read an article or the content of a web page, use `obscura fetch <url> --quiet --dump text` to get clean, readable text.
2. If the page is heavily protected, add the `--stealth` flag to randomize fingerprints and bypass anti-bot challenges.
3. Use `--eval` to extract specific DOM elements, states, or variables instead of dumping the whole page.
