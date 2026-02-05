---
name: tk-find
description: Search across Tasuku tasks, notes, learnings, and decisions. Use when user says /tk:find or asks to search, find, or look for something in tasks.
---

# Search Tasuku

Search across all Tasuku content including tasks, notes, learnings, and decisions.

## Instructions

1. Ask user for search query if not provided
2. Use the `tk_find` MCP tool with the query
3. Display results grouped by type (tasks, notes, learnings, decisions)
4. Show the matching content with context

## Output Format

```
## Search Results for "query"

### Tasks (X matches)
- [task-id] Description

### Notes (X matches)
- [task-id/note-id] Note text

### Learnings (X matches)
- [learning-id] Learning text

### Decisions (X matches)
- [decision-id] Chose X because Y
```

## Notes

- Search is case-insensitive
- Matches on task IDs, descriptions, note text, learning text, decision IDs/choices/reasoning
- If no results, suggest broadening the search or checking spelling
