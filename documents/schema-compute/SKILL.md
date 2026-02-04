---
name: schema-compute
description: Auto-generate computed frontmatter fields like word_count, link_count, reading_time. Triggers on "compute fields", "calculate metadata", "derived fields".
auto_trigger: true
trigger_keywords:
  - "compute fields"
  - "calculate metadata"
  - "derived fields"
  - "auto-generate fields"
  - "word count"
  - "link count"
  - "reading time"
  - "computed frontmatter"
  - "generate metadata"
  - "add computed"
allowed-tools: mcp__flywheel__compute_frontmatter, Read, Edit
---

# Computed Frontmatter

Auto-compute derived fields from note content. Generates metadata like word count, link count, and reading time.

## When to Use

Invoke when you want to:
- Add analytics fields to notes
- Track note length and complexity
- Generate reading time estimates
- Add last_updated timestamps

## Available Computed Fields

| Field | Description | Example |
|-------|-------------|---------|
| word_count | Words in note body | 1523 |
| link_count | Outgoing wikilinks | 24 |
| backlink_count | Incoming links | 15 |
| tag_count | Number of tags | 5 |
| reading_time | Estimated read time | "8 min" |
| created | File creation date | "2025-01-03" |
| last_updated | File modification date | "2025-01-03" |

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| path | Yes | Note to compute fields for |
| fields | No | Specific fields to compute (default: all) |

## Process

### 1. Parse User Input

Recognize computation requests:
- "add computed fields to projects/Phoenix.md"
- "calculate word count for this note"
- "add reading time to my meeting notes"

### 2. Call MCP Tool

```
mcp__flywheel__compute_frontmatter({
  path: "projects/Phoenix.md",
  fields: ["word_count", "link_count", "reading_time"]
})
```

### 3. Format Results

```
## Computed Frontmatter

For: projects/Phoenix.md

| Field | Value | Method |
|-------|-------|--------|
| word_count | 1523 | Prose word count |
| link_count | 24 | Outgoing wikilinks |
| backlink_count | 15 | Incoming links |
| reading_time | "8 min" | word_count / 200 |

### Suggested YAML
```yaml
word_count: 1523
link_count: 24
backlink_count: 15
reading_time: "8 min"
```

**Add these to frontmatter?** (y/n)
```

## Six Gates Compliance

| Gate | Implementation |
|------|----------------|
| 1. Read Before Write | compute_frontmatter reads file first |
| 2. File Exists | Validates path before computation |
| 3. Chain Validation | N/A (single step) |
| 4. Mutation Confirmation | Shows preview, requires confirmation |
| 5. Health Check | Uses MCP health infrastructure |
| 6. Post Validation | Confirms changes after applying |

## Use Cases

- **Content analytics**: "How long are my notes?"
- **Complexity tracking**: "Which notes have many links?"
- **Reading estimates**: "Add reading time to blog posts"
- **Timestamp management**: "Update last_updated field"

## Integration

Works well with other skills:
- **schema-infer**: See if computed fields are common
- **vault-search**: Query by computed values
- **schema-apply**: Add to batch operations

---

**Version:** 1.0.0
