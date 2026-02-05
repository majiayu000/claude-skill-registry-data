---
name: normalize-note
description: Harmonize frontmatter and wikilinks in a note. Detects prose patterns, suggests frontmatter additions, and suggests wikilinks for frontmatter values. Triggers on "normalize note", "harmonize note", "sync frontmatter".
auto_trigger: true
trigger_keywords:
  - "normalize note"
  - "harmonize note"
  - "sync frontmatter"
  - "bridge frontmatter"
  - "bidirectional sync"
  - "frontmatter from prose"
  - "prose to frontmatter"
  - "wikilinks in frontmatter"
  - "normalize this note"
  - "harmonize frontmatter"
allowed-tools: mcp__flywheel__detect_prose_patterns, mcp__flywheel__suggest_frontmatter_from_prose, mcp__flywheel__suggest_wikilinks_in_frontmatter, mcp__flywheel__validate_cross_layer
---

# Normalize Note

Harmonize the relationship between frontmatter (Schema-Native) and wikilinks (Graph-Native) in a note.

## When to Use

Invoke when you want to:
- Detect "Key: [[Value]]" patterns in prose and suggest frontmatter fields
- Find frontmatter values that could be converted to wikilinks
- Check consistency between frontmatter references and prose wikilinks
- Get a unified view of how to improve note structure

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| path | Yes | Path to the note to normalize (e.g., "projects/my-project.md") |

## Process

### 1. Parse User Input

Recognize normalization requests:
- "normalize this note"
- "harmonize frontmatter and wikilinks in projects/foo.md"
- "sync the frontmatter with the prose"

### 2. Call MCP Tools (in sequence)

```
# Step 1: Detect prose patterns
mcp__flywheel__detect_prose_patterns(path)

# Step 2: Suggest frontmatter from patterns
mcp__flywheel__suggest_frontmatter_from_prose(path)

# Step 3: Suggest wikilinks for frontmatter
mcp__flywheel__suggest_wikilinks_in_frontmatter(path)

# Step 4: Validate cross-layer consistency
mcp__flywheel__validate_cross_layer(path)
```

### 3. Format Results

```
Note Normalization Report: projects/my-project.md
=================================================

Prose Patterns Detected (5):
-------------------------------------------------
  Line 12: Client: [[Acme Corp]]       -> client: [[Acme Corp]]
  Line 14: Status: Active              -> status: Active
  Line 15: Owner: [[Ben Carter]]       -> owner: [[Ben Carter]]
  Line 18: Priority: High              -> priority: High
  Line 22: Due Date: 2024-01-15        -> due_date: 2024-01-15

Frontmatter -> Wikilink Suggestions (2):
-------------------------------------------------
  Field: attendees[0] = "Ben Carter"
    -> attendees: [[[Ben Carter]], "Sarah Johnson"]
    Target: people/Ben Carter.md

  Field: project = "Phoenix"
    -> project: [[Phoenix]]
    Target: projects/Phoenix.md

Cross-Layer Consistency:
-------------------------------------------------
  ✓ Consistent (in both): [[Acme Corp]], [[Ben Carter]]
  ⚠ Frontmatter only: Sarah Johnson (not linked in prose)
  ⚠ Prose only: [[Another Note]] (not in frontmatter)

Recommended Actions:
-------------------------------------------------
1. Add detected patterns to frontmatter
2. Convert matching frontmatter values to wikilinks
3. Review prose-only links for frontmatter inclusion

=================================================
```

## Use Cases

- **New note cleanup**: After writing, normalize to add proper structure
- **Schema migration**: Convert prose-heavy notes to structured frontmatter
- **Graph enhancement**: Make frontmatter values traversable via wikilinks
- **Consistency audit**: Ensure frontmatter and prose references align

## Integration

Works with other bidirectional skills:
- **promote-frontmatter**: Apply frontmatter suggestions
- **wikilinkify-frontmatter**: Convert frontmatter values to wikilinks

---

**Version:** 1.0.0
