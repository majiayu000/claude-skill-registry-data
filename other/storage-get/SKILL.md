---
name: storage-get
description: Retrieve a single previously-stored page from Crawlbase Cloud Storage by rid or url. Returns the stored body as JSON, HTML, or Markdown.
---

Use the `storage_get` tool from the Crawlbase MCP server to fetch one stored page.

## When to use

Use this skill when the user has a `rid` (or a previously-stored URL) and wants the stored body back without re-crawling.

## Usage

Call `storage_get` with `rid` and/or `url` (at least one is required — `rid` is the exact identifier and is preferred when known). Optionally pass:

- `as`: "json" (default — full record), "html" (just the body), or "markdown" (converted from html)
- `use_js_token`: true if the original crawl response had `token_type: "js"` (JS-rendered pages or screenshots). Storage is per-token — querying the wrong silo returns "Not found".

## Example prompts

- "Fetch rid abc123 from Crawlbase storage"
- "Get https://example.com from storage as markdown"
- "Retrieve the stored JS-rendered page with rid xyz789"
