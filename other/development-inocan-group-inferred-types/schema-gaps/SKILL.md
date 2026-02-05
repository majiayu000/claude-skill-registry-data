---
name: schema-gaps
description: Find notes missing expected fields based on inferred conventions. Triggers on "incomplete notes", "missing fields", "find gaps", "schema gaps".
auto_trigger: true
trigger_keywords:
  - "incomplete notes"
  - "missing fields"
  - "find gaps"
  - "schema gaps"
  - "notes missing"
  - "incomplete metadata"
  - "missing frontmatter"
  - "fix incomplete"
  - "fields missing"
  - "find incomplete"
allowed-tools: mcp__flywheel__find_incomplete_notes, mcp__flywheel__infer_folder_conventions
---

# Schema Gaps Finder

Find notes that are missing expected fields based on what other notes in the same folder have.

## When to Use

Invoke when you want to:
- Find notes with incomplete metadata
- Identify gaps in your note consistency
- Get suggestions for what fields to add
- See completeness scores for your notes

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| folder | No | Folder to analyze. Omit for entire vault. |

## Process

### 1. Parse User Input

Recognize gap-finding requests:
- "find notes with missing fields"
- "which notes are incomplete?"
- "show me schema gaps in meetings/"

### 2. Call MCP Tool

```
mcp__flywheel__find_incomplete_notes({
  folder: "meetings/",
  min_frequency: 0.7,
  limit: 50
})
```

### 3. Format Results

```
## Incomplete Notes Report

### meetings/ (3 incomplete of 47)

#### meetings/2025-12-20 Client Call.md
**Completeness:** 50%

Missing fields:
| Field | Expected Type | Frequency | Suggested Value |
|-------|---------------|-----------|-----------------|
| attendees | array | 87% | (detect from prose) |
| tags | array | 91% | ["meeting"] |

#### meetings/2025-12-22 Quick Sync.md
**Completeness:** 67%

Missing fields:
| Field | Expected Type | Frequency | Suggested Value |
|-------|---------------|-----------|-----------------|
| tags | array | 91% | ["meeting", "standup"] |

---

**Summary:**
- 3 notes need attention
- Most common missing field: `tags` (3 notes)
- Run `/schema-apply` to add suggested fields
```

## Use Cases

- **Quality audit**: "How consistent is my metadata?"
- **Batch fixing**: "What notes need fields added?"
- **Pre-migration**: "Find gaps before changing schema"
- **Review workflow**: "Check notes before archiving"

## Integration

Works well with other skills:
- **schema-infer**: Understand what fields are expected
- **schema-apply**: Apply suggested fixes
- **vault-search**: Find specific incomplete notes

---

**Version:** 1.0.0
