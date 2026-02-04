---
name: wikilinkify-frontmatter
description: Convert plain text frontmatter values to wikilinks when they match existing notes. Triggers on "wikilinkify frontmatter", "link frontmatter", "convert to wikilinks".
auto_trigger: true
trigger_keywords:
  - "wikilinkify frontmatter"
  - "link frontmatter"
  - "convert to wikilinks"
  - "frontmatter to wikilinks"
  - "add wikilinks to frontmatter"
  - "link frontmatter values"
  - "make frontmatter linkable"
  - "frontmatter links"
  - "wikify frontmatter"
  - "link metadata values"
allowed-tools: mcp__flywheel__suggest_wikilinks_in_frontmatter
---

# Wikilinkify Frontmatter

Convert plain text frontmatter values to wikilinks when they match existing note titles or aliases.

## When to Use

Invoke when you want to:
- Make frontmatter values traversable in the graph
- Convert string values like `client: "Acme Corp"` to `client: [[Acme Corp]]`
- Enable backlink tracking from frontmatter references
- Bridge schema-based (frontmatter) and graph-based (wikilink) paradigms

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| path | Yes | Path to the note (e.g., "projects/phoenix.md") |

## Process

### 1. Parse User Input

Recognize wikilinkify requests:
- "add wikilinks to the frontmatter in this note"
- "convert frontmatter values to links"
- "link the metadata in projects/phoenix.md"

### 2. Call MCP Tool

```
mcp__flywheel__suggest_wikilinks_in_frontmatter(path)
```

### 3. Format Results

```
Wikilinkify Frontmatter: projects/phoenix.md
=================================================

Current Frontmatter:
-------------------------------------------------
---
title: Phoenix Project
client: Acme Corp
team:
  - Ben Carter
  - Sarah Johnson
  - Mike Williams
status: active
---

Wikilink Suggestions (3):
-------------------------------------------------
  Field: client = "Acme Corp"
    -> client: [[Acme Corp]]
    Target note: companies/Acme Corp.md

  Field: team[0] = "Ben Carter"
    -> team: [[[Ben Carter]], "Sarah Johnson", "Mike Williams"]
    Target note: people/Ben Carter.md

  Field: team[1] = "Sarah Johnson"
    -> team: [[[Ben Carter]], [[Sarah Johnson]], "Mike Williams"]
    Target note: people/Sarah Johnson.md

No match found for:
  - team[2]: "Mike Williams" (no matching note)

Updated Frontmatter:
-------------------------------------------------
---
title: Phoenix Project
client: [[Acme Corp]]
team:
  - [[Ben Carter]]
  - [[Sarah Johnson]]
  - Mike Williams
status: active
---

Would you like me to apply these changes?

=================================================
```

### 4. Apply Changes (with confirmation)

If user confirms:
1. Read current file content
2. Update frontmatter values with wikilinks
3. Preserve values that don't match any notes
4. Write updated file

## Matching Logic

The tool matches values against:
- Note titles (case-insensitive)
- Note aliases defined in frontmatter
- Both relative and absolute paths

Already-linked values (`[[Note]]`) are skipped.

## Benefits

**For Graph Navigation:**
- Frontmatter values appear in backlinks
- Graph view shows frontmatter relationships
- Queries can traverse frontmatter links

**For Data Integrity:**
- Broken links are detectable
- Renamed notes update automatically (in some editors)
- Clear visual indication of relationships

## Use Cases

- **CRM-style vaults**: Link client, contact, project fields
- **Research notes**: Link author, source, related-work fields
- **Project management**: Link team, stakeholder, dependency fields
- **Meeting notes**: Link attendee, facilitator, client fields

## Integration

Part of the Bidirectional Bridge:
- **normalize-note**: Full analysis including prose detection
- **promote-frontmatter**: Extract patterns before linking

---

**Version:** 1.0.0
