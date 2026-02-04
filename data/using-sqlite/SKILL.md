---
name: using-sqlite
description: Use when working with SQLite databases in DataPeeker analysis sessions - querying data, importing CSVs, exploring schemas, formatting output, or optimizing performance. Provides task-oriented guidance for effective SQLite CLI usage in data analysis workflows.
---

# Using SQLite

## Overview

SQLite is the primary database for DataPeeker analysis sessions. This skill provides task-oriented guidance for common SQLite operations during data analysis.

**Core principle:** Explore schema first, format output for readability, write efficient queries, verify all operations.

## When to Use

Use this skill when you need to:
- Explore an unfamiliar database schema
- Query data for analysis or hypothesis testing
- Import CSV files into SQLite tables
- Format query output for readability
- Diagnose slow queries or optimize performance
- Understand which CLI invocation pattern to use

**When NOT to use:**
- Database-agnostic data profiling (see `understanding-data` skill for patterns that work across all SQL databases)
- Complex data cleaning logic (delegate to `cleaning-data` skill + sub-agents)
- Statistical analysis (use Python/pandas for advanced statistics)
- Large-scale transformations (use Python sqlite3 module)

## DataPeeker Conventions

```
Database Path:    data/analytics.db (relative from project root)
Table Naming:     raw_* for imported data, clean_* for cleaned data
Single Database:  All tables in one file per analysis session
```

**Example workflow:**
```
CSV file → raw_sales → clean_sales → Analysis queries
```

## Quick Reference

| Task | Guidance File |
|------|---------------|
| Understand what tables/columns exist | @./exploring-schema.md |
| Make query results readable | @./formatting-output.md |
| Write analytical queries | @./writing-queries.md |
| Load CSV files | @./importing-data.md |
| Fix slow queries | @./optimizing-performance.md |
| Choose CLI invocation method | @./invoking-cli.md |

## Task-Oriented Guidance

### Exploring Schema

**Before writing queries, understand the database structure.**

See @./exploring-schema.md for:
- Listing all tables (.tables)
- Viewing table structure (.schema, PRAGMA table_info)
- Understanding column types and constraints
- Checking for indexes

**When:** Starting analysis, unfamiliar database, before writing joins

---

### Formatting Output

**Make query results readable for analysis.**

See @./formatting-output.md for:
- Output modes (column, csv, json, markdown)
- Showing/hiding headers (.headers on/off)
- Setting column widths for readability
- Redirecting output to files

**When:** Query results hard to read, need specific format for export, preparing reports

---

### Writing Queries

**SQLite-specific query patterns and conventions.**

See @./writing-queries.md for:
- SQLite idioms used in DataPeeker (COUNT(*) - COUNT(col) for NULLs)
- Date handling with STRFTIME
- DataPeeker percentage calculation conventions
- Common verification queries

**See also:** `writing-queries` and `understanding-data` skills for database-agnostic SQL patterns and data profiling approaches. This guidance focuses on SQLite-specific syntax, CLI usage, and optimizations.

**When:** Need SQLite-specific syntax, DataPeeker query conventions, date formatting with STRFTIME

---

### Importing Data

**Load CSV files and verify import success.**

See @./importing-data.md for:
- Using .import command
- Verification queries (row counts, sample data)
- When to use CLI vs Python sqlite3
- Transaction handling

**When:** Loading new data, Phase 4 of importing-data skill, verifying data loaded correctly

---

### Optimizing Performance

**Diagnose and fix slow queries.**

See @./optimizing-performance.md for:
- EXPLAIN QUERY PLAN analysis
- Creating indexes for common queries
- Using transactions for bulk operations
- PRAGMA optimization

**When:** Query takes >1 second, loading large datasets, repeated similar queries

---

### Invoking CLI

**Choose the right method to run sqlite3 commands.**

See @./invoking-cli.md for:
- Interactive mode (for exploration)
- Heredoc pattern (for multi-command scripts)
- File redirect (for SQL files)
- One-liner mode (for quick checks)

**When:** Starting any SQLite operation, unsure which invocation to use

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing queries without exploring schema | Always run .tables and .schema first |
| Poor output formatting (hard to read results) | Use .mode column and .headers on for readability |
| Ignoring NULL values in calculations | Use COUNT(*) - COUNT(col) for NULL counting |
| Integer division losing decimals | Use 100.0 (not 100) for percentage calculations |
| Slow queries without diagnosis | Run EXPLAIN QUERY PLAN before optimizing |
| Assuming import succeeded | Always verify with SELECT COUNT(*) after import |
| Using wrong CLI invocation pattern | Interactive for exploration, heredoc for scripts |

## Verification Before Proceeding

**After any import operation:**
```sql
-- 1. Verify row count matches expectation
SELECT COUNT(*) FROM raw_table;

-- 2. Check sample data looks correct
SELECT * FROM raw_table LIMIT 5;

-- 3. Verify no unexpected NULLs
SELECT COUNT(*) - COUNT(critical_column) FROM raw_table;
```

**After writing a complex query:**
```sql
-- 1. Check query plan
EXPLAIN QUERY PLAN SELECT ...;

-- 2. Time the query
.timer on
SELECT ...;
```

## Real-World Impact

**Systematic approach prevents:**
- Writing queries against wrong tables (explore schema first)
- Unreadable output (format before analyzing)
- Slow queries (diagnose with EXPLAIN QUERY PLAN)
- Silent data loss (verify imports)
- Incorrect percentages (use float division)

**Following this skill:**
- Reduces query debugging time by 50%+
- Catches import issues immediately
- Produces readable analysis artifacts
- Ensures reproducible workflows
