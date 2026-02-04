---
name: bear-notes
description: Search, read, and manage Bear notes. Use when user asks about their notes, wants to find information in Bear, create notes, or manage tags.
---

# Bear Notes Skill

This skill provides access to Bear notes through a bash CLI that reads directly from Bear's SQLite database and uses x-callback-url for write operations.

## Script Location

`~/.claude/skills/bear-notes/scripts/bear`

## Available Commands

### Search and Read

**search** - Search notes by term, optionally filter by tag
```bash
bear search "meeting notes"
bear search "project" "work"
```

**open** - Get note content by ID
```bash
bear open "ABC123-456DEF-789"
```

**open-title** - Get note by exact title
```bash
bear open-title "My Note Title"
```

### Create and Modify

**create** - Create new note
```bash
bear create "Note content" "Note Title" "tag1,tag2"
bear create "Quick note"  # Without title or tags
```

**add-text** - Add text to existing note
```bash
bear add-text "ABC123-456DEF-789" "Additional content" append
bear add-text "ABC123-456DEF-789" "Header text" prepend
bear add-text "ABC123-456DEF-789" "Replace everything" replace_all
```

### Tags

**tags** - List all tags with note counts
```bash
bear tags
```

**tag** - List notes with specific tag
```bash
bear tag "work"
```

**rename-tag** - Rename tag
```bash
bear rename-tag "old-name" "new-name"
```

**delete-tag** - Delete tag
```bash
bear delete-tag "unused-tag"
```

### Special Queries

**untagged** - List untagged notes
```bash
bear untagged
bear untagged "search term"
```

**todos** - List notes containing unchecked todos (`- [ ]`)
```bash
bear todos
bear todos "project"
```

**today** - List notes created today
```bash
bear today
bear today "meeting"
```

### Other Operations

**grab-url** - Create note from URL
```bash
bear grab-url "https://example.com" "research,reading"
```

**trash** - Move note to trash
```bash
bear trash "ABC123-456DEF-789"
```

## Output Format

All commands output JSON:
- Single objects: One JSON object
- Lists: One JSON object per line (JSON Lines format)

Example list output:
```json
{"id":"ABC-123","title":"Note 1","content_preview":"First note...","created":"2025-11-25T10:00:00","modified":"2025-11-25T10:00:00"}
{"id":"DEF-456","title":"Note 2","content_preview":"Second note...","created":"2025-11-25T11:00:00","modified":"2025-11-25T11:00:00"}
```

Example single note:
```json
{
  "id": "ABC-123",
  "title": "My Note",
  "content": "Full note content here...",
  "created": "2025-11-25T10:00:00",
  "modified": "2025-11-25T10:00:00",
  "tags": ["work", "project"]
}
```

## Implementation Details

**Read Operations:**
- Queries Bear's SQLite database directly at:
  `~/Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data/database.sqlite`
- Uses `sqlite3 -json` for JSON output
- Filters out trashed notes (`ZTRASHED = 0`)

**Write Operations:**
- Uses Bear's x-callback-url API
- Opens URLs via `open bear://x-callback-url/...`
- URL parameters are properly encoded

**Timestamps:**
- Bear uses Core Data format (seconds since 2001-01-01)
- Converted to ISO 8601 format in output

## Use Cases

- Search notes: "Find my notes about project planning"
- Read content: "Show me the content of my meeting notes"
- Create notes: "Create a note with my todo list"
- Manage tags: "List all my work-related notes"
- Find todos: "Show me all my incomplete tasks"
- Quick capture: "Save this URL to Bear"

## Limitations

- Read operations are synchronous and fast
- Write operations trigger Bear app (x-callback-url)
- Database path is macOS-specific
- Requires Bear app to be installed
