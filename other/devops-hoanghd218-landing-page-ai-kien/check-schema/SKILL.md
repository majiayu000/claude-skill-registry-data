---
name: vault-schema-check
description: Find fields that have multiple different types across notes (schema violations). Triggers on "schema check", "frontmatter inconsistencies", "metadata violations", "type mismatches".
auto_trigger: true
trigger_keywords:
  - "schema check"
  - "frontmatter inconsistencies"
  - "metadata violations"
  - "type mismatches"
  - "schema violations"
  - "inconsistent fields"
  - "field type errors"
  - "check frontmatter"
  - "metadata issues"
  - "frontmatter problems"
  - "type errors"
  - "yaml issues"
  - "inconsistent metadata"
  - "property mismatches"
  - "schema problems"
  - "fix metadata"
allowed-tools: mcp__flywheel__find_frontmatter_inconsistencies
---

# Frontmatter Schema Checker

Detect fields with inconsistent types across your vault (schema violations).

## When to Use

Invoke when you want to:
- Find frontmatter fields with mixed types (string vs array)
- Detect data quality issues
- Prepare for vault migrations
- Ensure metadata consistency

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| None | - | This skill requires no arguments |

## Process

### 1. Parse User Input

Recognize schema check requests:
- "check my frontmatter for inconsistencies"
- "find schema violations"
- "are there type mismatches in my metadata?"
- "frontmatter health check"

### 2. Call MCP Tool

```
mcp__flywheel__find_frontmatter_inconsistencies()
```

### 3. Format Results

**Inconsistencies Found:**
```
Frontmatter Schema Check
=================================================

⚠️ Found 3 fields with type inconsistencies

-------------------------------------------------

Field: tags
  Expected: array (majority usage)
  Inconsistencies: 12 notes

  Type Distribution:
    array:   89 notes (88%)  ✓ Expected
    string:  12 notes (12%)  ⚠️ Should be array

  Example violations:
    - daily-notes/2025-12-15.md: tags: "work" (string)
    - projects/alpha.md: tags: "project, active" (string)

  Fix suggestion:
    Convert string values to arrays:
    tags: "work" → tags: ["work"]
    tags: "project, active" → tags: ["project", "active"]

-------------------------------------------------

Field: priority
  Expected: number (majority usage)
  Inconsistencies: 5 notes

  Type Distribution:
    number:  23 notes (82%)  ✓ Expected
    string:   5 notes (18%)  ⚠️ Should be number

  Example violations:
    - tasks/review.md: priority: "high" (string)
    - tasks/urgent.md: priority: "1" (quoted number)

  Fix suggestion:
    Convert to numeric values:
    priority: "high" → priority: 1
    priority: "1" → priority: 1

-------------------------------------------------

Field: date
  Expected: string (YYYY-MM-DD format)
  Inconsistencies: 2 notes

  Type Distribution:
    string:  340 notes (99%)  ✓ Expected
    number:    2 notes (1%)   ⚠️ Numeric dates

  Example violations:
    - archive/old-note.md: date: 20231215 (number)

  Fix suggestion:
    Convert to string format:
    date: 20231215 → date: "2023-12-15"

-------------------------------------------------

Summary:
  Total fields checked: 15
  Fields with issues: 3
  Notes affected: 19

Recommended actions:
  1. Fix 'tags' field in 12 notes (string → array)
  2. Fix 'priority' field in 5 notes (string → number)
  3. Fix 'date' field in 2 notes (number → string)

=================================================
```

**No Inconsistencies:**
```
Frontmatter Schema Check
=================================================

✓ No type inconsistencies found!

All 15 frontmatter fields have consistent types
across all notes in your vault.

Fields verified:
  - type: string (234 notes)
  - status: string (156 notes)
  - tags: array (101 notes)
  - priority: number (28 notes)
  - date: string (342 notes)
  ... and 10 more fields

Your vault schema is healthy! ✓

=================================================
```

## Understanding Schema Violations

| Issue | Description | Impact |
|-------|-------------|--------|
| String vs Array | `tags: "work"` vs `tags: ["work"]` | Dataview queries may fail |
| String vs Number | `priority: "1"` vs `priority: 1` | Sort/filter issues |
| Inconsistent Nulls | `field: null` vs missing field | Query edge cases |

## Use Cases

- **Data quality**: "Is my frontmatter consistent?"
- **Migration prep**: "What needs fixing before export?"
- **Dataview debugging**: "Why is my query not working?"
- **Bulk cleanup**: "What fields have type issues?"

## Integration

Works well with other skills:
- **vault-schema**: Understand field overview first
- **vault-field-values**: See specific value distributions
- **vault-search**: Find notes to fix by field criteria

## Vault Rules Observed

This skill (and the Schema Enforcer agent) follow vault rules:
- Never add wikilinks to YAML frontmatter
- Keys must be lowercase without special characters
- Values should be plain text (except author `[[@username]]`)
- Protected folders must use subfolders

---

**Version:** 1.0.0
