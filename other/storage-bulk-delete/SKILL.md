---
name: storage-bulk-delete
description: Delete up to 100 stored pages from Crawlbase Cloud Storage in one call. Irreversible.
---

Use the `storage_bulk_delete` tool from the Crawlbase MCP server to remove many stored pages at once. For fetch-and-delete in one step, use `storage_bulk_get` with `auto_delete: true` instead.

## When to use

Use this skill when the user wants to clean up a batch of stored items by rid.

## Usage

Call `storage_bulk_delete` with:

- `rids` (required): array of up to 100 request ids
- `use_js_token`: true if these rids live in the JS-token silo. All rids in one call must be in the same silo. Storage is per-token — deleting from the wrong silo is a no-op.

## Example prompts

- "Delete these 100 rids from Crawlbase storage"
- "Clear out my JS-token storage silo" (combine with `storage-list` to enumerate first)
