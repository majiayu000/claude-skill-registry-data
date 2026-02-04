---
name: vault-related
description: Find notes related to current note (by tags, folder, keywords). Triggers on "related notes", "similar notes", "find related", "what's related".
auto_trigger: true
trigger_keywords:
  - "related notes"
  - "similar notes"
  - "find related"
  - "what's related"
  - "related to"
  - "similar to"
  - "show related"
  - "notes like this"
  - "like this note"
  - "notes like"
  - "find similar"
  - "comparable notes"
  - "akin to"
  - "matching notes"
  - "same topic"
allowed-tools: mcp__flywheel__search_notes, mcp__flywheel__get_note_metadata
---

# Related Notes

Find notes similar to a given note based on tags, folder, and metadata.

## Purpose

Discover notes related to the current context:
- Same tags
- Same folder
- Similar frontmatter
- Common keywords

Useful for:
- Finding relevant context
- Discovering connections
- Research exploration
- Knowledge consolidation

## Process

### 1. Get Current Note Metadata

```javascript
current = get_note_metadata(note_path)
  → Extract: tags, folder, frontmatter
```

### 2. Search by Tag Similarity

```javascript
tag_matches = search_notes({
  has_any_tag: current.tags,
  limit: 20
})
```

### 3. Search by Folder

```javascript
folder_matches = search_notes({
  folder: current.folder,
  limit: 20
})
```

### 4. Rank by Similarity

Score each note:
- **+3 points**: Same primary tag
- **+2 points**: Same folder
- **+1 point**: Shared secondary tag
- **+1 point**: Same frontmatter type

### 5. Report Results

```
Related Notes
═══════════════════════════════════════════════
Finding notes related to: [[MyProject]]

📊 Most Related (by score):
   1. [[Related Project]] - Score: 7
      • Tags: #project, #data-platform, #azure
      • Folder: work/projects/

   2. [[Similar Work]] - Score: 6
      • Tags: #project, #methodology
      • Folder: work/projects/

   3. [[Connected Topic]] - Score: 5
      • Tags: #methodology
      • Folder: work/projects/

🏷️ Tag Matches (15):
   • #project: 8 notes
   • #azure: 4 notes
   • #data-platform: 3 notes

📁 Folder Matches: 12 notes in work/projects/

💡 Suggestions:
   • Consider linking [[MyProject]] to top 3 related notes
   • Review folder matches for additional context

═══════════════════════════════════════════════
```

## Use Cases

**Research:**
- "What else have I written about X?"
- "Find all project notes like this one"

**Context:**
- "What notes are in same topic area?"
- "Show similar work from last quarter"

**Consolidation:**
- "Find duplicate or overlapping content"
- "Discover notes to merge"

---

**Version:** 1.0.0
