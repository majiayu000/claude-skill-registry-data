---
name: semantic-search:clear
description: Use when you want to wipe all indexed data and start fresh
---

# Clear Index

Wipe all indexed data from the database.

## Action

1. Warn the user this will delete all indexed data
2. Call `mcp__semantic-search__clear_index` tool
3. Confirm the index has been cleared
4. Remind them to run `/semantic-search:reindex` to rebuild
