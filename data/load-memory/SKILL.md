---
name: load-memory
description: Reload memory context from files
---

## Script Path Resolution

**IMPORTANT:** The `scripts/` folder is in the plugin directory, NOT the current project.

From "Base directory for this skill:" above, derive the scripts path:
- Remove `/skills/load-memory` from the end
- Add `/scripts/` to get the scripts directory

Example:
- Base: `~/.claude/plugins/cache/memory-keeper-marketplace/memory-keeper/13.8.3/skills/load-memory`
- Scripts: `~/.claude/plugins/cache/memory-keeper-marketplace/memory-keeper/13.8.3/scripts/`

Use this full path when running node commands below.

# Load Memory

Reload memory context into current session.

## Usage

```
/memory-keeper:load-memory
```

## Actions

Run the load-memory script (use full path from above):
```bash
node "{SCRIPTS_PATH}/load-memory.js"
```

This will output the current memory state to context:

1. **Hierarchical Memory** (if exists):
   - `project.md` - Project overview
   - `architecture.md` - Architecture decisions
   - `conventions.md` - Coding conventions

2. **L3 Summaries**:
   - JSON summaries of rotated memory archives

3. **Rolling Memory**:
   - Last 50 lines of `memory.md`

## When to Use

- After manually editing memory files
- To refresh context if it seems stale
- To verify what memory is currently loaded

## Notes

- Memory is automatically loaded on session start
- This command reloads without restarting session
