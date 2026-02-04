---
name: search-memory
description: Search past sessions and memory
---

## Script Path Resolution

**IMPORTANT:** The `scripts/` folder is in the plugin directory, NOT the current project.

From "Base directory for this skill:" above, derive the scripts path:
- Remove `/skills/search-memory` from the end
- Add `/scripts/` to get the scripts directory

Example:
- Base: `~/.claude/plugins/cache/memory-keeper-marketplace/memory-keeper/13.8.3/skills/search-memory`
- Scripts: `~/.claude/plugins/cache/memory-keeper-marketplace/memory-keeper/13.8.3/scripts/`

Use this full path when running node commands below.

# Search Memory

Search through session history and memory archives.

## Usage

```
/memory-keeper:search-memory [query]
```

## Actions

Use full path from above:
```bash
# Search across all memory layers
node "{SCRIPTS_PATH}/counter.js" search-memory "query"

# Include L1 raw sessions (slower but thorough)
node "{SCRIPTS_PATH}/counter.js" search-memory "query" --deep

# Filter by type
node "{SCRIPTS_PATH}/counter.js" search-memory --type=decision
node "{SCRIPTS_PATH}/counter.js" search-memory --type=theme
node "{SCRIPTS_PATH}/counter.js" search-memory --type=issue
```

## Examples

```bash
# Search all memory layers for "auth"
node "{SCRIPTS_PATH}/counter.js" search-memory "auth"

# Deep search including L1 sessions
node "{SCRIPTS_PATH}/counter.js" search-memory "auth" --deep
```

## Notes

- Searches L1, L2, and L3 memory layers
- Use `--deep` flag for thorough L1 session search
