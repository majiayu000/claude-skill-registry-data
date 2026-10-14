---
name: storage-list
description: List rids currently in Crawlbase Cloud Storage, with scroll-based pagination (up to 1000 rids per call). Useful for enumerating everything stored under a token.
---

Use the `storage_list` tool from the Crawlbase MCP server to enumerate stored rids.

## When to use

Use this skill when the user wants to see what's in their storage, iterate over every stored item, or find rids they don't remember.

## Usage

Call `storage_list` with:

- `limit`: max rids to return (≤1000)
- `scroll`: true on follow-up calls to continue an open scroll session
- `scroll_id`: opaque continuation token from the previous response — pass it back with `scroll: true`
- `scroll_order`: "asc" or "desc" (default desc)
- `use_js_token`: true to list the JS-token silo instead of the normal one. Storage is per-token; each silo is enumerated separately.

Scroll sessions expire after ~15s of inactivity — loop tightly, don't pause between pages.

## Example prompts

- "List all stored pages in Crawlbase"
- "Show me the 500 most recent rids in storage"
- "Enumerate everything in my JS-token storage"
