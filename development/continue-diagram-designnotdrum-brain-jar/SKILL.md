---
name: continue-diagram
description: "Continue working on an existing diagram. Load, review, and modify persistent diagrams across sessions."
allowed-tools:
  - mcp__visual-thinking__list_diagrams
  - mcp__visual-thinking__get_diagram
  - mcp__visual-thinking__update_diagram
  - mcp__visual-thinking__search_diagrams
  - mcp__visual-thinking__delete_diagram
  - mcp__visual-thinking__export_diagram
---

# Continue a Diagram

Continue working on diagrams from previous sessions.

## Finding Diagrams

**List recent diagrams:**
```
list_diagrams()
```

**Filter by scope:**
```
list_diagrams(scope: "project:my-app")
```

**Search by content:**
```
search_diagrams(query: "notification architecture")
```

## Loading a Diagram

**By ID (exact):**
```
get_diagram(id: "abc-123")
```

**By title (fuzzy match):**
```
get_diagram(title: "notification flow")
```

**With version history:**
```
get_diagram(id: "abc-123", include_history: true)
```

## Updating Diagrams

When you modify a diagram, the previous version is automatically saved to history.

**Update content:**
```
update_diagram(
  id: "abc-123",
  mermaid: "flowchart TD\n  A --> B --> C",
  note: "Simplified the flow"
)
```

**Update metadata:**
```
update_diagram(
  id: "abc-123",
  title: "New Title",
  context: "Updated context explaining changes",
  tags: ["architecture", "v2"]
)
```

## Version History

Diagrams track their evolution. Each update creates a version snapshot.

To see history:
```
get_diagram(id: "abc-123", include_history: true)
```

History shows:
- Previous Mermaid content
- Timestamp of each version
- Notes explaining what changed

## Exporting

**As Mermaid file:**
```
export_diagram(id: "abc-123", format: "mermaid")
```

**As SVG (via Mermaid CLI):**
```
export_diagram(id: "abc-123", format: "svg")
```

**For draw.io:**
```
export_diagram(id: "abc-123", format: "drawio")
```

## Cleanup

**Delete a diagram:**
```
delete_diagram(id: "abc-123")
```

## Workflow Tips

1. **Start each session** by checking for relevant existing diagrams
2. **Update, don't recreate** — build on existing work
3. **Use notes** — explain what changed when updating
4. **Export for sharing** — generate files others can view

## Related Skills

- **capture** — Create new diagrams during brainstorming
