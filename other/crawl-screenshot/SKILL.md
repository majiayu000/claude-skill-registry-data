---
name: crawl-screenshot
description: Take a full-page or viewport screenshot of any URL. Supports desktop and mobile viewports, custom dimensions, and configurable page-load wait times.
---

Use the `crawl_screenshot` tool from the Crawlbase MCP server to capture a screenshot of a webpage.

## When to use

Use this skill when the user wants a visual snapshot of a webpage, needs to verify a page's appearance, or wants to share a visual preview of content.

## Usage

Call the `crawl_screenshot` tool with the `url` parameter. Optionally pass:

- `device`: "desktop" (default), "mobile", or "tablet"
- `mode`: "fullpage" (default) or "viewport"
- `width`: max width in pixels (viewport mode only)
- `height`: max height in pixels (viewport mode only)
- `page_wait`: milliseconds to wait before taking the screenshot
- `store`: true to push the underlying HTML page to Crawlbase Cloud Storage. The screenshot itself is NOT stored — the response still includes an ephemeral `screenshot_url`, plus `rid`, `stored_at`, `storage_url`, and `token_type: "js"`. Screenshots always land in the JS-token silo, so subsequent `storage_get` / `storage_delete` calls must pass `use_js_token: true`.

## Example prompts

- "Take a screenshot of https://example.com"
- "Capture a mobile screenshot of https://example.com"
- "Take a viewport screenshot of https://example.com at 1280x800"
- "Take a screenshot of https://example.com and store the page in Crawlbase Cloud Storage"
