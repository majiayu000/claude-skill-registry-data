---
name: delete-memory
description: Delete memories from the index. Supports deletion by IDs, project, timestamp, or all.
allowed-tools: mcp__cc-forever-mcp__delete_memory, mcp__cc-forever-mcp__get_stats
user-invocable: false
---

# Delete Memories

Delete memories from the persistent index.

## Arguments

- `all` - Delete all memories
- `project:<name>` - Delete all memories for a specific project
- `before:<timestamp>` - Delete memories before an ISO timestamp (e.g., `before:2025-01-01`)
- `<id1> <id2> ...` - Delete specific memory IDs

**Arguments:** $ARGUMENTS

## Steps

### 1. Parse Arguments

Determine the deletion mode:

- If `$ARGUMENTS` contains "all": delete all memories (confirm first)
- If `$ARGUMENTS` starts with "project:": extract project name
- If `$ARGUMENTS` starts with "before:": extract timestamp
- Otherwise: treat as space-separated IDs

### 2. Confirmation for Destructive Operations

For `all` or `project:` deletions, warn the user about the scope of deletion.

### 3. Execute Deletion

Call `mcp__cc-forever-mcp__delete_memory` with appropriate parameters:

**For all:**
```json
{
  "all": true
}
```

**For project:**
```json
{
  "project": "<project-name>"
}
```

**For before timestamp:**
```json
{
  "before": "<ISO-timestamp>"
}
```

**For specific IDs:**
```json
{
  "ids": ["<id1>", "<id2>", ...]
}
```

### 4. Report Results

Display the deletion result:

```
Deletion completed:
- Deleted: {deleted_count} memories
- Criteria: {criteria used}
```

### 5. Show Updated Stats

Optionally call `get_stats` to show the remaining memory count.

## Examples

- `/cc-forever:delete all` - Delete all memories
- `/cc-forever:delete project:my-app` - Delete all memories for "my-app" project
- `/cc-forever:delete before:2025-01-01T00:00:00Z` - Delete memories before 2025
- `/cc-forever:delete 2025-01-15T10:30:00.000Z-0 2025-01-15T10:30:00.000Z-1` - Delete specific IDs
