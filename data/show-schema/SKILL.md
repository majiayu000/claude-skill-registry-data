---
name: vault-schema
description: Analyze all frontmatter fields used across the vault. Triggers on "frontmatter schema", "metadata fields", "what fields exist", "vault schema".
auto_trigger: true
trigger_keywords:
  - "frontmatter schema"
  - "metadata fields"
  - "what fields exist"
  - "vault schema"
  - "field types"
  - "metadata structure"
  - "frontmatter overview"
  - "what metadata"
  - "yaml fields"
  - "property names"
  - "metadata overview"
  - "field list"
  - "what properties"
  - "note attributes"
allowed-tools: mcp__flywheel__get_frontmatter_schema
---

# Frontmatter Schema Analyzer

Understand all metadata fields used across your vault.

## When to Use

Invoke when you want to:
- Discover what frontmatter fields exist in your vault
- Understand field usage patterns (types, counts)
- Plan metadata standardization
- Get an overview of your vault's schema

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| None | - | This skill requires no arguments |

## Process

### 1. Parse User Input

Recognize schema requests:
- "what frontmatter fields exist in my vault?"
- "show me the vault schema"
- "what metadata fields do I use?"

### 2. Call MCP Tool

```
mcp__flywheel__get_frontmatter_schema()
```

### 3. Format Results

```
Frontmatter Schema Analysis
=================================================

Total Fields: 15 unique fields across vault

Field Overview:
-------------------------------------------------

  Field         Type(s)        Usage    Notes
  ──────────────────────────────────────────────
  type          string         234      Most common: "project", "note"
  status        string         156      Most common: "active", "done"
  date          string         342      Date format: YYYY-MM-DD
  tags          array          89       Avg 3 tags per note
  author        string         45       Usually "@username" format
  created       string         412      Timestamp or date
  modified      string         412      Timestamp or date
  aliases       array          67       For note title variations
  priority      number         23       Range: 1-5
  project       string         78       Links to project notes

-------------------------------------------------

Type Distribution:
  string:  10 fields (67%)
  array:   3 fields (20%)
  number:  1 field (7%)
  boolean: 1 field (7%)

Top 5 Most Used Fields:
  1. created (412 notes)
  2. modified (412 notes)
  3. date (342 notes)
  4. type (234 notes)
  5. status (156 notes)

=================================================
```

## Use Cases

- **Schema discovery**: "What metadata am I actually using?"
- **Standardization planning**: "Which fields should I consolidate?"
- **Migration prep**: "What fields need to be converted?"
- **Documentation**: "What's the schema of my knowledge base?"

## Integration

Works well with other skills:
- **vault-field-values**: See all unique values for a specific field
- **vault-schema-check**: Find inconsistencies in field types
- **vault-search**: Query notes by frontmatter fields

---

**Version:** 1.0.0
