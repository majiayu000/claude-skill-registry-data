---
name: maintain
description: Detect and fix stale claude/*.md knowledge docs. Use when claude/architecture.md or build.md references missing files, wrong commands, or outdated patterns. Keeps the knowledge base accurate.
---

# Maintain Skill

Keep the brain knowledge base accurate and current.

## When to use
- After a major refactor that changed file structure
- When a command in claude/build.md produces "command not found"
- When claude/architecture.md references a directory that no longer exists
- Periodically as part of session end

## Protocol

### 1. Scan claude/*.md files for staleness signals
Read each claude/*.md file and flag:
- Directory paths that no longer exist
- Commands that fail when run
- Service names that no longer exist in the codebase
- `{{PLACEHOLDER}}` tokens that were never filled in
- References to files that have been deleted or moved

### 2. Verify each flagged item
```bash
# Check if a directory exists
ls claude/path/to/check 2>&1

# Check if a command is available
which command_name 2>&1
```

### 3. Fix verified stale content
- Update paths to reflect current structure
- Update commands based on current package.json/Makefile
- Remove references to deleted services/modules
- Fill in any remaining `{{PLACEHOLDER}}` tokens

### 4. Add new knowledge (opportunistic)
If you discover new facts about the codebase during maintenance, add them to the appropriate claude/*.md file.

### 5. Report changes
List every file updated with a one-line description of what changed.

## Rules
- NEVER remove knowledge without verifying it's actually stale
- NEVER add speculative content — only add what you've verified
- Document the maintenance run in claude/tasks/lessons.md
- Stale docs are bugs — treat them with the same urgency as code bugs
