---
name: semantic-search:reindex
description: Use when you want to rebuild or refresh the semantic search index for the codebase
---

# Semantic Search Reindex

Trigger a full reindex of the codebase for semantic search.

## Action

1. Call `mcp__semantic-search__reindex` tool with `force: true`
2. Immediately call `mcp__semantic-search__get_status` to show initial progress
3. Inform the user that indexing is running in the background
4. Tell them they can check progress with `/semantic-search:status`

## Options

If the user says "clean" or "fresh", use `clear_first: true` to wipe the index before rebuilding.
