---
name: schema-migrate
description: Rename frontmatter fields or transform values in bulk. Triggers on "rename field", "migrate values", "transform field", "bulk update".
auto_trigger: true
trigger_keywords:
  - "rename field"
  - "migrate values"
  - "transform field"
  - "bulk update field"
  - "change field name"
  - "convert values"
  - "field migration"
  - "update frontmatter"
  - "refactor field"
  - "bulk rename"
allowed-tools: mcp__flywheel__rename_field, mcp__flywheel__migrate_field_values
---

# Schema Migration

Rename frontmatter fields or transform values across multiple notes. All operations preview changes first (dry-run by default).

## When to Use

Invoke when you want to:
- Rename a field across all notes (e.g., `author` -> `owner`)
- Transform field values (e.g., "high" -> 1)
- Standardize inconsistent values
- Migrate to a new schema

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| operation | Yes | "rename" or "migrate" |
| field | Yes | Field to operate on |
| new_name | For rename | New field name |
| mapping | For migrate | Value transformations (e.g., {"high": 1, "low": 3}) |
| folder | No | Limit to specific folder |

## Process

### 1. Parse User Input

**Rename requests:**
- "rename 'author' to 'owner' in projects folder"
- "change field name from status to state"

**Migration requests:**
- "convert priority values: high=1, medium=2, low=3"
- "transform status from strings to numbers"

### 2. Call MCP Tool

For rename:
```
mcp__flywheel__rename_field({
  old_name: "author",
  new_name: "owner",
  folder: "projects/",
  dry_run: true
})
```

For value migration:
```
mcp__flywheel__migrate_field_values({
  field: "priority",
  mapping: {"high": 1, "medium": 2, "low": 3},
  dry_run: true
})
```

### 3. Format Preview

```
## Field Migration Preview

### Renaming: author -> owner
Scope: projects/
Affected: 12 notes

| Note | Current Value | Action |
|------|---------------|--------|
| projects/Phoenix.md | [[Sarah Chen]] | Rename |
| projects/Beta.md | Marcus | CONFLICT |
| projects/Alpha.md | [[John Smith]] | Rename |
| ... | ... | ... |

### Conflicts (1)
- **projects/Beta.md** has both 'author' and 'owner' fields

### Options
1. Apply renames, skip conflicts
2. Apply renames, merge conflicts (combine values)
3. Cancel

**Choose option:**
```

### 4. Apply Changes (with confirmation)

After user confirms, run with `dry_run: false`.

## Six Gates Compliance

| Gate | Implementation |
|------|----------------|
| 1. Read Before Write | dry_run=true by default |
| 2. File Exists | Validates all affected files |
| 3. Chain Validation | Preview -> Confirm -> Apply |
| 4. Mutation Confirmation | Always shows preview first |
| 5. Health Check | Uses MCP health infrastructure |
| 6. Post Validation | Reports success/failure counts |

## Use Cases

- **Schema evolution**: "We decided to rename 'author' to 'owner'"
- **Value standardization**: "Convert string priorities to numbers"
- **Cleanup**: "Rename misspelled field 'stauts' to 'status'"
- **Migrations**: "Prepare for new tool that expects different field names"

## Integration

Works well with other skills:
- **vault-schema**: See all field names before migrating
- **vault-schema-check**: Find type inconsistencies to fix
- **schema-infer**: Understand current conventions

---

**Version:** 1.0.0
