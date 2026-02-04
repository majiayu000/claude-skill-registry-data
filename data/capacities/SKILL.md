---
name: capacities
description: Interact with Capacities PKM app. Use when user wants to search their knowledge base, create notes/objects, save weblinks, or append to daily notes. Triggers on keywords like "capacities", "PKM", "knowledge base", "daily note", "save to capacities".
---

# Capacities Skill

## Understanding Capacities

Capacities is a **graph-based PKM** (Personal Knowledge Management) app — the user's "second brain".

**Key concepts:**
- **Space** = A workspace (most users have one)
- **Structure** = Object type (e.g. "Book", "Note", "Task", "Person"). Defines what properties objects of this type can have.
- **Object** = User-created content. Has a type (structureId) and a title. Each object can fill in the properties defined by its structure.
- **Property** = A field in a structure (e.g. "Author", "Rating", "Created at"). Every object of that type can have this property filled in.
- **Collection** = User-created grouping within a structure type.

**Example:** Structure "Book" has properties [title, Author, Rating, Notes]. When user creates a Book object called "Erta Ale", they can fill in Author="Atticus", Rating=5, etc.

## Commands

Run via: `python .claude/skills/capacities/capacities.py <command>`

### space-info — Understand the space
Returns all Structures (types) with their properties and collections. **Run this first** to understand what types exist.
```bash
space-info
```
Output format:
```
Book (id: uuid)
  Properties: title, Author, Rating, Notes, ...
  Collections: To Read, Favorites
```

### search — Find Objects (user content)
Find actual content the user created.
```bash
search "query"                   # Search by title
search "query" --mode fullText   # Search in content too
```

### daily-note — Save to today's journal
Quick capture. Good for insights, reminders, quick thoughts.
```bash
daily-note << 'EOF'
## Insight
Long content with "quotes" and special chars...
EOF
```

### weblink — Save a URL
```bash
weblink "https://url" [--title ""] [--tags "a,b"] [--notes "markdown"]
```

### create — Create new Object ⚠️ LOCAL ONLY
Requires Capacities desktop app installed. (Won't work in sandboxes, use MCP instead.)
```bash
create --title "Title" --content - [--type Book|Note|Task|...] << 'EOF'
Long markdown content with "quotes"...
EOF
```

### current — Get what user is looking at ⚠️ LOCAL ONLY
Requires Capacities desktop app installed. (Won't work in sandboxes, use MCP instead.)
```bash
current
```
Returns title, URL, type, and content snippets of the active object — all in one call.

## Tips

1. **Run `space-info` first** to understand what types the user has
2. **Search before creating** to avoid duplicates
3. "save this" / "remember this" → `daily-note`
4. User shares a link → `weblink`
5. User wants structured content → `create` with appropriate `--type`
