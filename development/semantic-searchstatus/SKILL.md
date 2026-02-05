---
name: semantic-search:status
description: Use when you want to check semantic search server status, indexing progress, or watcher state
---

# Semantic Search Status

Check the status of the semantic search MCP server.

## Action

Call the `mcp__semantic-search__get_status` tool and report:

1. **Server status** - ready/initializing/error
2. **Watcher status** - running/stopped
3. **Indexing progress** - if in progress, show current file and progress
4. **Index stats** - number of files and chunks indexed
5. **Any errors** - if present
