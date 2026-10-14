---
name: crawl-markdown
description: Crawl a URL and extract clean, readable Markdown content. Strips ads, navigation, and boilerplate — returns only the main content.
---

Use the `crawl_markdown` tool from the Crawlbase MCP server to fetch clean Markdown from a URL.

## When to use

Use this skill when the user wants to read or summarize a webpage's content without dealing with HTML noise. Ideal for articles, documentation, blog posts, and product pages.

## Usage

Call the `crawl_markdown` tool with the `url` parameter. Optionally pass:

- `device`: "desktop" (default), "mobile", or "tablet"
- `user_agent`: custom user agent string
- `store`: true to push the result to Crawlbase Cloud Storage instead of returning the Markdown. Response then contains `rid`, `stored_at`, `storage_url`, and `token_type`. Retrieve later with `storage_get` (use `as: "markdown"` to convert).

## Example prompts

- "Get the markdown content of https://example.com"
- "Summarize the article at https://example.com/article"
- "Extract the main content from https://example.com as markdown"
- "Crawl https://example.com as markdown and store it in Crawlbase Cloud Storage"
