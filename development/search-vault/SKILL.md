---
name: vault-search
description: Advanced vault search with filters (folder, tags, frontmatter). Triggers on "search vault", "find notes", "query notes", "search for".
auto_trigger: true
trigger_keywords:
  - "search vault"
  - "search"
  - "find notes"
  - "find"
  - "query notes"
  - "search for"
  - "look for"
  - "where are"
  - "show me notes"
  - "notes about"
  - "notes with"
  - "notes in"
  - "locate notes"
  - "where is"
  - "filter notes"
  - "query"
  - "lookup"
  - "find by"
allowed-tools: mcp__flywheel__search_notes
---

# Search Skill

Advanced vault search with powerful filtering using Flywheel MCP.

## Purpose

Comprehensive search interface to your vault with support for:
- Folder filtering (search within specific folders)
- Tag filtering (has_tag, has_all_tags, has_any_tag)
- Frontmatter filtering (where: {key: value})
- Title search (title_contains)
- Sorting (modified, created, title)
- Pagination (limit, order)

Goes far beyond basic text search - this is semantic, metadata-aware search.

## When to Use

Invoke when you want to:
- **Find notes**: "search for X" or "find notes about Y"
- **Filter by folder**: "notes in work/" or "search tech folder"
- **Filter by tags**: "notes with #project" or "tagged work and azure"
- **Filter by metadata**: "notes with status active" or "type project"
- **Recent notes**: "notes modified this week" or "recent changes"

## Process

### 1. Parse User Query

Extract search parameters from natural language:

**Examples:**
```
"search for databricks"
  → title_contains: "databricks"

"notes in work/ tagged project"
  → folder: "work/", has_tag: "project"

"recent notes with status active"
  → sort_by: "modified", where: {status: "active"}
```

### 2. Call MCP Tool

```
Call: mcp__flywheel__search_notes
Parameters: {
  folder: "work/",
  has_tag: "project",
  title_contains: "databricks",
  sort_by: "modified",
  order: "desc",
  limit: 50
}
```

### 3. Display Results

```
Search Results
═══════════════════════════════════════════════

Query: databricks in work/ tagged #project
Found: 12 notes (sorted by modified, desc)

1. [[Databricks Migration Project]]
   📂 work/projects/databricks-migration.md
   📅 Modified: 2025-12-30 | Created: 2024-05-15
   🏷️ Tags: #work #project #databricks
   📋 type: project | status: active

2. [[Databricks ETL Pipeline]]
   📂 work/projects/databricks-etl.md
   📅 Modified: 2025-12-28 | Created: 2024-09-20
   🏷️ Tags: #work #project #databricks
   📋 type: project | status: completed

═══════════════════════════════════════════════

Options:
- Refine search (add/change filters)
- Show note content (preview specific note)
- Export results (CSV/markdown)
```

## Search Parameters

### Folder Filter
```
folder: "work/"          → Only work folder
folder: "tech/tools"     → Specific subfolder
(no folder parameter)    → All folders
```

### Tag Filters
```
has_tag: "project"              → Has #project tag
has_all_tags: ["work", "azure"] → Has BOTH tags
has_any_tag: ["work", "tech"]   → Has EITHER tag
```

### Title Filter
```
title_contains: "databricks"    → Title includes "databricks" (case-insensitive)
title_contains: "meeting 2024"  → Multiple words
```

### Frontmatter Filter
```
where: {type: "project"}                → type == "project"
where: {status: "active", owner: "X"}   → status AND owner
where: {priority: "high"}               → priority == "high"
```

### Sorting
```
sort_by: "modified"  → Most recently modified first (default)
sort_by: "created"   → Most recently created first
sort_by: "title"     → Alphabetical by title
```

### Order
```
order: "desc"  → Descending (default for modified/created)
order: "asc"   → Ascending
```

### Limit
```
limit: 10   → Return max 10 results
limit: 50   → Return max 50 results (default)
limit: 100  → Return max 100 results
```

## Natural Language Examples

### Simple Title Search
```
User: "search for databricks"
Params: {title_contains: "databricks"}
Result: All notes with "databricks" in title
```

### Folder + Tag
```
User: "notes in work/ tagged project"
Params: {folder: "work/", has_tag: "project"}
Result: Project notes in work folder
```

### Multiple Tags (AND)
```
User: "notes tagged work and azure"
Params: {has_all_tags: ["work", "azure"]}
Result: Notes with BOTH work AND azure tags
```

### Recent Notes
```
User: "recent notes in work/"
Params: {folder: "work/", sort_by: "modified", order: "desc", limit: 20}
Result: 20 most recently modified work notes
```

## Related Skills

- **related**: Find similar notes (uses tags + links)
- **orphans**: Find disconnected notes
- **hubs**: Find highly connected notes
- **gaps**: Find missing notes (inverse of search)

## Performance

- **MCP call**: ~200-500ms depending on filters
- **Result formatting**: ~50ms for 50 results
- **Total**: Usually under 1 second
