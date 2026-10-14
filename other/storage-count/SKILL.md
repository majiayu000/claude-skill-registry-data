---
name: storage-count
description: Return the total number of documents in Crawlbase Cloud Storage for a token.
---

Use the `storage_count` tool from the Crawlbase MCP server to count stored documents.

## When to use

Use this skill when the user asks "how many" pages are stored, or wants to verify storage usage before bulk operations.

## Usage

Call `storage_count` with:

- `use_js_token`: true to count the JS-token silo; omit or false for the normal silo. Storage is per-token — call twice (once for each silo) to get a grand total.

## Example prompts

- "How many pages do I have in Crawlbase storage?"
- "Count the items in my JS storage silo"
