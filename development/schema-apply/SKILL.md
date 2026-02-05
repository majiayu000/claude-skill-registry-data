---
name: schema-apply
description: Apply inferred conventions to incomplete notes. Triggers on "apply schema", "add missing fields", "complete notes", "fix frontmatter".
auto_trigger: true
trigger_keywords:
  - "apply schema"
  - "add missing fields"
  - "complete notes"
  - "fix frontmatter"
  - "apply conventions"
  - "fill in fields"
  - "add suggested fields"
  - "fix incomplete notes"
  - "apply inferred"
allowed-tools: mcp__flywheel__find_incomplete_notes, mcp__flywheel__suggest_field_values, Read, Edit
---

# Schema Application

Apply inferred conventions to incomplete notes. Suggests and adds missing fields based on what similar notes have.

## When to Use

Invoke when you want to:
- Add missing frontmatter fields to notes
- Batch-fix incomplete metadata
- Apply folder conventions to outliers
- Normalize notes to match their peers

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| folder | No | Folder to apply schema to. Omit for entire vault. |
| path | No | Specific note to fix. Takes precedence over folder. |

## Process

### 1. Parse User Input

Recognize application requests:
- "apply inferred schema to incomplete notes"
- "add missing fields to meetings/"
- "fix incomplete notes in projects/"

### 2. Find Incomplete Notes

```
mcp__flywheel__find_incomplete_notes({
  folder: "meetings/",
  min_frequency: 0.7
})
```

### 3. Preview Changes

```
## Schema Application Preview

I'll add missing fields based on inferred conventions:

### meetings/2025-12-20 Client Call.md
Adding:
```yaml
attendees:
  - [[Sarah Chen]]
  - [[Marcus Johnson]]
tags:
  - meeting
  - client
```

### meetings/2025-12-22 Quick Sync.md
Adding:
```yaml
tags:
  - meeting
  - standup
```

**Proceed with these changes?** (y/n)
```

### 4. Apply Changes (with confirmation)

Use Read to get current content, Edit to add fields.

## Six Gates Compliance

| Gate | Implementation |
|------|----------------|
| 1. Read Before Write | Reads current file before any changes |
| 2. File Exists | Validates file exists via find_incomplete_notes |
| 3. Chain Validation | N/A (single step) |
| 4. Mutation Confirmation | Always shows preview, requires confirmation |
| 5. Health Check | Uses MCP health infrastructure |
| 6. Post Validation | Confirms changes after applying |

## Use Cases

- **Batch normalization**: "Make all meeting notes consistent"
- **New note completion**: "Add standard fields to my new note"
- **Migration support**: "Ensure all notes have required fields"

## Integration

Works well with other skills:
- **schema-infer**: See what fields will be applied
- **schema-gaps**: Find notes needing fixes
- **promote-frontmatter**: Extract prose patterns first

---

**Version:** 1.0.0
