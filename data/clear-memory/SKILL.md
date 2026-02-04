---
name: clear-memory
description: Clean up old memory files
---

## Script Path Resolution

**IMPORTANT:** The `scripts/` folder is in the plugin directory, NOT the current project.

From "Base directory for this skill:" above, derive the scripts path:
- Remove `/skills/clear-memory` from the end
- Add `/scripts/` to get the scripts directory

Example:
- Base: `~/.claude/plugins/cache/memory-keeper-marketplace/memory-keeper/13.8.3/skills/clear-memory`
- Scripts: `~/.claude/plugins/cache/memory-keeper-marketplace/memory-keeper/13.8.3/scripts/`

Use this full path when running node commands below.

# Clear Memory

Clean up old session files.

## Usage

```
/memory-keeper:clear-memory [all|old]
```

## Actions

### Archive old files (recommended):
Use full path from above:
```bash
node "{SCRIPTS_PATH}/counter.js" compress
```

This archives session files older than 30 days into monthly archives:
```
sessions/2025-10-15_0300.md -> sessions/archive/2025-10.md
```

### Clear everything (manual):

**WARNING: Destructive operation**

```bash
# Remove all session files
rm -rf .claude/memory/sessions/*.md
rm -rf .claude/memory/sessions/*.jsonl

# Optionally clear memory.md
rm .claude/memory/memory.md
```

## Recommendations

1. **Regular maintenance**: Run `compress` monthly
2. **Before major changes**: Create backup first

## Notes

- `compress` is non-destructive (archives, doesn't delete)
- Archived files can be manually reviewed in `sessions/archive/`
