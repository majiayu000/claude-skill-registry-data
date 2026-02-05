---
name: vault-find-sections
description: Find all sections across vault matching a heading pattern. Triggers on "find sections", "notes with heading", "all X sections", "which notes have".
auto_trigger: true
trigger_keywords:
  - "find sections"
  - "notes with heading"
  - "all X sections"
  - "which notes have"
  - "find headings"
  - "search headings"
  - "heading pattern"
  - "notes with section"
  - "heading search"
  - "find heading"
  - "search for heading"
  - "section across vault"
  - "heading in notes"
  - "locate sections"
allowed-tools: mcp__flywheel__find_sections
---

# Section Finder

Find all notes containing a specific heading pattern across your vault.

## When to Use

Invoke when you want to:
- Find all notes with "## References" sections
- Discover which notes have a specific heading
- Search for heading patterns (regex supported)
- Audit section usage across the vault

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `pattern` | Yes | - | Regex pattern to match heading text |
| `folder` | No | - | Limit search to specific folder |

## Process

### 1. Parse User Input

Identify the heading pattern:
- "find all notes with a References section"
- "which notes have a TODO heading?"
- "find sections matching 'Implementation.*'"
- "notes in projects/ with a Status section"

### 2. Call MCP Tool

```
mcp__flywheel__find_sections(
  pattern: "References",
  folder: null  // or "projects/" to limit scope
)
```

### 3. Format Results

**Sections Found:**
```
Section Search Results
=================================================

Pattern: "References"
Scope: Entire vault

Found 23 notes with matching sections:

-------------------------------------------------

Projects (12 notes):
  projects/Alpha.md
    └─ ## References (line 45)
  projects/Beta.md
    └─ ## References (line 32)
    └─ ### Code References (line 67)
  projects/Gamma.md
    └─ ## References (line 28)
  ... and 9 more

Tech Notes (8 notes):
  tech/frameworks/React.md
    └─ ## References (line 89)
  tech/frameworks/Vue.md
    └─ ## External References (line 102)
  tech/tools/Docker.md
    └─ ## References (line 56)
  ... and 5 more

Daily Notes (3 notes):
  daily-notes/2025-12-30.md
    └─ ## References (line 23)
  daily-notes/2025-12-29.md
    └─ ## References (line 31)
  daily-notes/2025-12-28.md
    └─ ## References (line 27)

-------------------------------------------------

Summary:
  Total matches: 25 headings in 23 notes
  Most common: "## References" (21 occurrences)
  Variations: "External References", "Code References"

=================================================
```

**With Regex Pattern:**
```
Section Search Results
=================================================

Pattern: "TODO|Tasks|Action Items"
Scope: projects/

Found 8 notes with matching sections:

-------------------------------------------------

  projects/Alpha.md
    └─ ## TODO (line 15)
  projects/Beta.md
    └─ ## Tasks (line 22)
    └─ ### Subtasks (line 34)
  projects/Gamma.md
    └─ ## Action Items (line 18)
  projects/Delta.md
    └─ ## TODO (line 12)
    └─ ## Completed Tasks (line 45)
  ... and 4 more

-------------------------------------------------

Pattern Tips:
  - Use ".*" for wildcards
  - Use "|" for alternatives
  - Case-insensitive matching

=================================================
```

**No Sections Found:**
```
Section Search Results
=================================================

Pattern: "Appendix"
Scope: Entire vault

No matching sections found.

Suggestions:
  - Try a different pattern
  - Check spelling
  - Use regex: "Append.*" for partial match

Similar headings that exist:
  - "## Appendices" (2 notes)
  - "## Additional Notes" (5 notes)

=================================================
```

## Common Patterns

| Pattern | Finds | Use Case |
|---------|-------|----------|
| `References` | All "References" sections | Link audit |
| `TODO\|Tasks` | TODO or Tasks headings | Task overview |
| `^Status$` | Exact "Status" heading | Project tracking |
| `Implementation.*` | Any Implementation heading | Code sections |
| `Notes?` | "Note" or "Notes" | Note sections |

## Use Cases

- **Vault auditing**: "How many notes have a References section?"
- **Template compliance**: "Which project notes are missing a Status section?"
- **Content discovery**: "Find all notes with Implementation details"
- **Section extraction**: "Find sections to extract for a report"

## Integration

Works well with other skills:
- **vault-section**: Extract content from found sections
- **vault-search**: Combine with metadata filtering
- **vault-health**: Include in vault structure audits

---

**Version:** 1.0.0
