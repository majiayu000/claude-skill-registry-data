---
name: crawl-html
description: Crawl a URL and return its full raw HTML content. Supports JS rendering, custom user agents, device emulation, geo-targeting, and optional screenshot capture.
---

Use the `crawl` tool from the Crawlbase MCP server to fetch the raw HTML of a given URL.

## When to use

Use this skill when the user wants the full HTML source of a webpage, needs to inspect page structure, or wants to extract specific elements.

## Usage

Call the `crawl` tool with the `url` parameter. Optionally pass:

- `device`: "desktop" (default), "mobile", or "tablet"
- `country`: ISO country code for geo-targeting (e.g. "US", "DE")
- `ajax_wait`: milliseconds to wait for AJAX requests
- `page_wait`: milliseconds to wait for page load
- `screenshot`: true to also capture a screenshot
- `store`: true to push the result to Crawlbase Cloud Storage instead of returning the body. Response then contains `rid`, `stored_at`, `storage_url`, and `token_type` (`"normal"` or `"js"`). Use `storage_get` later to retrieve.

## Example prompts

- "Crawl https://example.com and return the HTML"
- "Fetch the HTML of https://example.com from a mobile browser"
- "Get the HTML source of https://example.com and take a screenshot"
- "Crawl https://example.com and store it in Crawlbase Cloud Storage"
