---
name: storage-delete
description: Delete a single stored page from Crawlbase Cloud Storage by rid.
---

Use the `storage_delete` tool from the Crawlbase MCP server to remove one stored page. For deleting many at once, use `storage_bulk_delete` instead.

## When to use

Use this skill when the user wants to remove a specific stored item identified by its `rid`.

## Usage

Call `storage_delete` with:

- `rid` (required): the request id of the stored item
- `use_js_token`: true if the item was crawled with the JS token (i.e. its crawl response had `token_type: "js"`). Storage is per-token — deleting from the wrong silo is a no-op.

## Example prompts

- "Delete rid abc123 from Crawlbase storage"
- "Remove the stored screenshot with rid xyz789"
