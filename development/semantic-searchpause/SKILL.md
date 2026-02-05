---
name: semantic-search:pause
description: Use when you want to pause the semantic search file watcher to stop automatic reindexing
---

# Semantic Search Pause Watcher

Pause the file watcher that automatically reindexes changed files.

## Action

1. Call `mcp__semantic-search__pause_watcher` tool
2. Confirm to the user that the watcher is paused
3. Remind them that file changes won't be indexed until they resume with `/semantic-search:resume`
