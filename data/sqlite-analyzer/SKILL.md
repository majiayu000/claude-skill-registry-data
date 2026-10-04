---
name: sqlite-analyzer
description: Analyzes SQLite databases to identify schema issues, data inconsistencies, and relationship problems. Use when investigating database bugs, validating data integrity, debugging ORM mapping issues, or understanding database structure. Particularly useful for diagnosing ID mismatches, foreign key violations, and entity relationship errors.
---

# SQLite Database Analyzer

## Overview

This skill enables systematic analysis of SQLite databases to identify structural issues, data inconsistencies, and relationship problems. It provides workflows for investigating database bugs, validating schemas, and understanding entity relationships.

## When to Use This Skill

- **Debugging ORM Issues**: ID fields mapped incorrectly (e.g., using `name` instead of actual `id`)
- **Data Integrity Checks**: Finding orphaned references or foreign key violations
- **Schema Investigation**: Understanding table structure and relationships
- **Bug Investigation**: Identifying root causes of data-related bugs
- **Migration Validation**: Verifying database migrations completed successfully

## Quick Start Workflow

1. **Locate Database**: Find the SQLite `.db` file path
2. **Inspect Schema**: Use `.schema` or `.tables` to understand structure
3. **Query Data**: Run targeted SELECT queries to investigate issues
4. **Cross-Reference**: Compare data between related tables
5. **Report Findings**: Document issues with specific examples

## Analysis Tasks

### 1. Schema Inspection

**Discover all tables:**

```sql
.tables
```

**View specific table schema:**

```sql
.schema table_name
```

**Get detailed table info:**

```sql
PRAGMA table_info(table_name);
```

**Example output interpretation:**

```
cid  name       type     notnull  dflt_value  pk
---  ---------  -------  -------  ----------  --
0    id         TEXT     1        NULL        1
1    name       TEXT     1        NULL        0
2    config     TEXT     0        NULL        0
```

### 2. Data Sampling

**Quick row count:**

```sql
SELECT COUNT(*) FROM table_name;
```

**Sample data with column details:**

```sql
SELECT * FROM table_name LIMIT 5;
```

**Check for NULL values:**

```sql
SELECT
  COUNT(*) as total,
  COUNT(column_name) as non_null,
  COUNT(*) - COUNT(column_name) as null_count
FROM table_name;
```

### 3. Relationship Validation

**Find orphaned references:**

```sql
SELECT child.id, child.foreign_key_column
FROM child_table child
LEFT JOIN parent_table parent ON child.foreign_key_column = parent.id
WHERE parent.id IS NULL;
```

**Count references per parent:**

```sql
SELECT
  parent.id,
  parent.name,
  COUNT(child.id) as child_count
FROM parent_table parent
LEFT JOIN child_table child ON parent.id = child.parent_id
GROUP BY parent.id, parent.name
ORDER BY child_count DESC;
```

**Verify bidirectional relationships:**

```sql
-- Check if all referenced IDs exist
SELECT DISTINCT foreign_key_column
FROM child_table
WHERE foreign_key_column NOT IN (SELECT id FROM parent_table);
```

### 4. ID Mismatch Detection

**Common bug pattern**: ORM returns `name` as `id`

**Diagnostic query:**

```sql
-- Compare actual ID with name field
SELECT
  id,
  name,
  CASE
    WHEN id = name THEN '⚠️ ID equals name (potential bug)'
    ELSE '✅ ID distinct from name'
  END as status
FROM table_name;
```

**Check for CUID/UUID patterns:**

```sql
SELECT
  id,
  name,
  LENGTH(id) as id_length,
  CASE
    WHEN LENGTH(id) = 25 THEN 'CUID2'
    WHEN LENGTH(id) = 36 THEN 'UUID'
    WHEN LENGTH(id) < 20 THEN 'Short ID (possibly name)'
    ELSE 'Unknown format'
  END as id_format
FROM table_name
LIMIT 10;
```

### 5. Debugging Workflow for ID Mismatches

When you suspect IDs are being mapped incorrectly (like the MCP server bug):

**Step 1: Verify actual database content**

```sql
SELECT id, name FROM mcp_servers;
```

**Step 2: Check what backend returns**

- Add debug logging in DTO/serialization layer
- Compare logged IDs with database IDs

**Step 3: Identify the mapping bug**

```rust
// ❌ WRONG: Using name as ID
id: model.name.clone(),

// ✅ CORRECT: Using actual ID field
id: model.id.clone(),
```

**Step 4: Verify the fix**

```sql
-- After fix, verify IDs are preserved
SELECT id, name FROM table_name
WHERE id IN ('expected-cuid-1', 'expected-cuid-2');
```

### 6. Data Consistency Checks

**Find duplicate keys:**

```sql
SELECT column_name, COUNT(*) as count
FROM table_name
GROUP BY column_name
HAVING COUNT(*) > 1;
```

**Check for invalid JSON:**

```sql
SELECT id, json_column
FROM table_name
WHERE json_valid(json_column) = 0;
```

**Timestamp validation:**

```sql
SELECT
  id,
  created_at,
  updated_at,
  CASE
    WHEN updated_at < created_at THEN '⚠️ Updated before created'
    WHEN created_at > strftime('%s', 'now') * 1000 THEN '⚠️ Future timestamp'
    ELSE '✅ Valid'
  END as status
FROM table_name
WHERE updated_at < created_at OR created_at > strftime('%s', 'now') * 1000;
```

## Investigation Templates

### Template 1: Entity Relationship Bug

````markdown
## Issue

[Description of the bug, e.g., "Assistant shows MCP server IDs instead of names"]

## Database Inspection

```sql
-- Step 1: Check parent table
SELECT id, name FROM parent_table LIMIT 5;

-- Step 2: Check child table references
SELECT id, name, foreign_key_column FROM child_table LIMIT 5;

-- Step 3: Join to verify relationships
SELECT
  child.id as child_id,
  child.foreign_key_column as ref_id,
  parent.name as parent_name
FROM child_table child
LEFT JOIN parent_table parent ON child.foreign_key_column = parent.id;
```
````

## Findings

- Actual database IDs: [list actual IDs]
- Backend returned IDs: [list returned IDs]
- Mismatch: [describe the discrepancy]

## Root Cause

[Identify the code causing incorrect mapping]

## Fix

[Show the correction needed]

````

### Template 2: Migration Validation

```markdown
## Migration Goal
[What the migration was supposed to achieve]

## Validation Queries
```sql
-- Check schema changes
PRAGMA table_info(table_name);

-- Verify data migration
SELECT COUNT(*) FROM table_name WHERE new_column IS NOT NULL;

-- Check constraints
PRAGMA foreign_key_list(table_name);
````

## Results

- Schema: [✅ correct / ❌ issues found]
- Data: [✅ migrated / ❌ missing data]
- Constraints: [✅ valid / ❌ violations found]

```

## Best Practices

1. **Always use absolute paths** when locating database files
2. **Sample before bulk operations** - check a few rows first
3. **Use transactions for analysis** - wrap in BEGIN/ROLLBACK if testing updates
4. **Document ID formats** - note whether using CUID, UUID, or other formats
5. **Cross-reference logs** - compare database state with application logs
6. **Check multiple timestamps** - initial app start vs. current state
7. **Consider data lifecycle** - some inconsistencies may be from migration periods

## Common Pitfalls

- **Assuming ID == name**: Many bugs come from treating name as primary key
- **Ignoring case sensitivity**: SQLite is case-insensitive by default
- **Not checking NULL values**: Can cause unexpected JOIN results
- **Forgetting LIMIT**: Large tables can overflow terminal output
- **Using old schema assumptions**: Schema may have changed between app versions

## Resources

### scripts/
Contains executable utilities for common database analysis tasks:

- `analyze_schema.py` - Generate comprehensive schema report
- `find_orphans.py` - Detect orphaned references across all tables
- `compare_ids.py` - Compare ID formats and detect mismatches
- `export_sample.py` - Export sample data for debugging

### references/
Additional documentation for advanced analysis:

- `sqlite-optimization.md` - Performance tuning and query optimization
- `common-patterns.md` - Frequently encountered database patterns
- `debugging-checklist.md` - Systematic debugging approach
```
