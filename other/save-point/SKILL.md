---
name: monggle-save-point
version: 1.0.0
description: |
  Save point - Save/restore working state across sessions (monggle)
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
triggers:
  - /save-point
  - monggle save-point
---

# save-point (monggle)

Save point - Save/restore working state across sessions (monggle)

**Usage:** `/save-point [list|resume|load <id>]`

**Examples:**
```bash
/save-point
```
