---
name: storage-bulk-get
description: Retrieve up to 100 stored pages from Crawlbase Cloud Storage in one call, optionally auto-deleting each item after retrieval.
---

Use the `storage_bulk_get` tool from the Crawlbase MCP server to fetch many stored pages at once.

## When to use

Use this skill when the user has a list of rids (typically from `storage_list`) and wants their bodies in a single round-trip, or wants a fetch-and-drain pattern.

## Usage

Call `storage_bulk_get` with:

- `rids` (required): array of up to 100 request ids
- `auto_delete`: true to delete each item after successful retrieval
- `as`: "metadata_only" (default — rid/url/timestamps only, no body), "json" (full records), "html" (raw bodies), or "markdown" (converted)
- `use_js_token`: true if these rids live in the JS-token silo. All rids in one call must be in the same silo. Storage is per-token — mixed-silo calls will silently miss results.

Default is `metadata_only` to keep the response lean — explicitly request `html` or `markdown` when bodies are needed.

## Example prompts

- "Bulk-retrieve these 50 rids as markdown"
- "Fetch rids from storage and delete them after"
- "Get metadata for these 100 stored items"
