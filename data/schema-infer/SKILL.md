---
name: schema-infer
description: Auto-detect metadata conventions for a folder. Triggers on "infer schema", "what conventions", "learn schema", "folder conventions".
auto_trigger: true
trigger_keywords:
  - "infer schema"
  - "what conventions"
  - "learn schema"
  - "folder conventions"
  - "detect schema"
  - "schema patterns"
  - "metadata conventions"
  - "frontmatter patterns"
  - "what fields should"
  - "expected fields"
  - "folder schema"
  - "infer conventions"
allowed-tools: mcp__flywheel__infer_folder_conventions
---

# Schema Inference

Auto-detect metadata conventions from your existing notes. Zero configuration - the system learns from what you've already written.

## When to Use

Invoke when you want to:
- Understand what frontmatter fields are standard in a folder
- Discover implicit schemas from existing notes
- Find required vs optional fields
- See naming patterns for files

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| folder | No | Folder to analyze (e.g., "meetings/"). Omit for entire vault. |

## Process

### 1. Parse User Input

Recognize schema inference requests:
- "what conventions does my meetings folder use?"
- "infer schema for projects/"
- "what fields should be in daily notes?"

### 2. Call MCP Tool

```
mcp__flywheel__infer_folder_conventions({
  folder: "meetings/",
  min_confidence: 0.5
})
```

### 3. Format Results

```
## Inferred Schema: meetings/

Based on 47 notes in this folder:

### Required Fields (>90% presence)
| Field | Type | Common Values |
|-------|------|---------------|
| type | string | "meeting" (100%) |
| date | date | - |
| attendees | array[wikilink] | - |

### Optional Fields (50-90% presence)
| Field | Type | Common Values |
|-------|------|---------------|
| status | string | scheduled (40%), completed (50%), cancelled (10%) |
| tags | array | meeting, standup, review |

### Suggested Computed Fields
- word_count (not currently tracked)
- link_count (not currently tracked)

### Naming Convention
Files follow pattern: `YYYY-MM-DD *.md`

### Coverage
- 94% of notes have frontmatter
- 3 notes may be incomplete (see /schema-gaps)
```

## Use Cases

- **New folder setup**: "What schema should my new project folder follow?"
- **Documentation**: "Document the metadata conventions for this vault"
- **Consistency check**: "Are my meeting notes following a pattern?"
- **Onboarding**: "What fields does this team use?"

## Integration

Works well with other skills:
- **schema-gaps**: Find notes missing expected fields
- **schema-apply**: Apply inferred conventions to incomplete notes
- **vault-schema**: See vault-wide field overview

---

**Version:** 1.0.0
