---
name: understanding-data
description: Component skill for systematic data profiling and exploration in DataPeeker analysis sessions
---

# Understanding Data

## Purpose

This component skill guides systematic data profiling before analysis begins. Use it when:
- Starting a new analysis session with unfamiliar data
- Encountering unexpected query results
- Need to understand data structure, quality, or relationships
- Referenced by process skills requiring data familiarity

## Prerequisites

- Data loaded into a relational database (SQLite, PostgreSQL, MySQL, SQL Server, etc.)
- SQL query tool available (database CLI, IDE, or query interface)
- Analysis workspace created (if using DataPeeker conventions)

## Data Understanding Process

Create a TodoWrite checklist for the 4-phase data profiling process:

```
Phase 1: Schema Discovery
Phase 2: Data Quality Assessment
Phase 3: Distribution Analysis
Phase 4: Relationship Identification
```

Mark each phase as you complete it. Document all findings in a numbered markdown file.

---

## Phase 1: Schema Discovery

**Goal:** Understand tables, columns, types, and cardinalities.

### List All Tables

```sql
-- Get all tables in database (database-specific methods):
-- SQLite: SELECT name FROM sqlite_master WHERE type='table';
-- PostgreSQL: SELECT tablename FROM pg_tables WHERE schemaname = 'public';
-- MySQL: SHOW TABLES;
-- SQL Server: SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';

-- Standard SQL approach (PostgreSQL, MySQL, SQL Server):
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'your_schema'
ORDER BY table_name;
```

**Document:** Table names and their likely business meaning.

**Note:** Use database-specific CLI commands or syntax as appropriate for your database engine.

### Examine Table Schemas

For each table of interest:

```sql
-- Get column information (database-specific):
-- SQLite: PRAGMA table_info(table_name);
-- PostgreSQL: \d table_name (CLI) or SELECT * FROM information_schema.columns WHERE table_name = 'table_name';
-- MySQL: DESCRIBE table_name; or SHOW COLUMNS FROM table_name;
-- SQL Server: EXEC sp_columns table_name; or SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'table_name';

-- Standard SQL approach:
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'your_table'
ORDER BY ordinal_position;
```

**Document:**
- Column names and types
- Which columns are likely keys/identifiers
- Which columns are measures vs dimensions
- Missing columns you'd expect to see

### Check Row Counts

```sql
-- Count rows in each table
SELECT 'table_name' as table_name, COUNT(*) as row_count
FROM table_name;
```

**Document:**
- Relative sizes of tables
- Whether counts match expectations
- Any suspiciously small/large tables

### Identify Unique Identifiers

```sql
-- Check column uniqueness
SELECT COUNT(*) as total_rows,
       COUNT(DISTINCT column_name) as unique_values,
       COUNT(*) - COUNT(DISTINCT column_name) as duplicate_count
FROM table_name;
```

**Test for each candidate key column.**

**Document:**
- Which columns are unique (potential primary keys)
- Which columns have high cardinality (useful for grouping)
- Which columns have low cardinality (categories/flags)

---

## Phase 2: Data Quality Assessment

**Goal:** Identify missing data, invalid values, and data quality issues.

### Check for NULL Values

```sql
-- Count NULLs for each important column
SELECT
  COUNT(*) as total_rows,
  COUNT(column1) as column1_non_null,
  COUNT(*) - COUNT(column1) as column1_null_count,
  ROUND(100.0 * (COUNT(*) - COUNT(column1)) / COUNT(*), 2) as column1_null_pct
FROM table_name;
```

**Document:**
- Which columns have missing data
- Percentage of missingness
- Whether missingness is random or systematic

### Check for Empty Strings

```sql
-- Find empty or whitespace-only strings
SELECT COUNT(*) as empty_string_count
FROM table_name
WHERE TRIM(text_column) = ''
   OR text_column IS NULL;
```

**Document:** Columns with empty string issues.

### Examine Value Ranges

For numeric columns:

```sql
-- Get min, max, and outlier candidates
SELECT
  MIN(numeric_column) as min_value,
  MAX(numeric_column) as max_value,
  AVG(numeric_column) as avg_value,
  COUNT(*) as total_count,
  COUNT(CASE WHEN numeric_column < 0 THEN 1 END) as negative_count,
  COUNT(CASE WHEN numeric_column = 0 THEN 1 END) as zero_count
FROM table_name;
```

**Document:**
- Impossible values (negative prices, future dates, etc.)
- Extreme outliers
- Suspicious patterns (many zeros, rounded numbers)

### Check Date/Time Validity

```sql
-- Examine date ranges and formats
SELECT
  MIN(date_column) as earliest_date,
  MAX(date_column) as latest_date,
  COUNT(DISTINCT date_column) as unique_dates,
  COUNT(*) as total_rows
FROM table_name;
```

**Document:**
- Date ranges (do they make sense for the business context?)
- Gaps in date coverage
- Future dates where inappropriate

### Examine Categorical Values

```sql
-- Get frequency distribution for categorical column
SELECT
  category_column,
  COUNT(*) as frequency,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM table_name), 2) as percentage
FROM table_name
GROUP BY category_column
ORDER BY frequency DESC;
```

**Document:**
- Valid categories and their distributions
- Unexpected categories
- Misspellings or data entry variations
- Extremely rare categories

---

## Phase 3: Distribution Analysis

**Goal:** Understand how data is distributed across key dimensions.

### Time Distribution

For any table with dates/timestamps:

```sql
-- Group by time period to see distribution
-- Extract year-month (database-specific function):
-- SQLite: STRFTIME('%Y-%m', date_column)
-- PostgreSQL: TO_CHAR(date_column, 'YYYY-MM')
-- MySQL: DATE_FORMAT(date_column, '%Y-%m')
-- SQL Server: FORMAT(date_column, 'yyyy-MM')

-- Example using SQLite syntax:
SELECT
  STRFTIME('%Y-%m', date_column) as year_month,
  COUNT(*) as row_count
FROM table_name
GROUP BY year_month
ORDER BY year_month;
```

**Look for:**
- Seasonal patterns
- Growth/decline trends
- Gaps or spikes
- Incomplete periods (partial months)

**Document:** Time coverage and patterns.

### Segmentation Distribution

For key categorical dimensions:

```sql
-- Distribution by segment
SELECT
  segment_column,
  COUNT(*) as count,
  COUNT(DISTINCT id_column) as unique_entities,
  ROUND(AVG(numeric_measure), 2) as avg_measure
FROM table_name
GROUP BY segment_column
ORDER BY count DESC;
```

**Document:**
- How data is distributed across segments
- Whether segments are balanced or skewed
- Segments with insufficient data for analysis

### Value Distribution Buckets

For continuous numeric measures:

```sql
-- Create distribution buckets
SELECT
  CASE
    WHEN value < 10 THEN '0-9'
    WHEN value < 50 THEN '10-49'
    WHEN value < 100 THEN '50-99'
    WHEN value < 500 THEN '100-499'
    ELSE '500+'
  END as value_bucket,
  COUNT(*) as frequency
FROM table_name
GROUP BY value_bucket
ORDER BY value_bucket;
```

**Adjust buckets to your data range.**

**Document:**
- Shape of distribution (normal, skewed, bimodal?)
- Presence of outliers
- Whether transformations might be needed

### Correlation Exploration

For related numeric columns:

```sql
-- Check if two measures move together
SELECT
  segment,
  COUNT(*) as n,
  ROUND(AVG(measure1), 2) as avg_measure1,
  ROUND(AVG(measure2), 2) as avg_measure2
FROM table_name
GROUP BY segment
ORDER BY avg_measure1;
```

**Look for:** Whether segments with high measure1 also have high measure2.

**Document:** Observed correlations or anti-correlations.

---

## Phase 4: Relationship Identification

**Goal:** Understand how tables relate to each other.

### Foreign Key Discovery

```sql
-- Find potential foreign keys by checking if column values exist in another table
SELECT
  'table_a.fk_column references table_b.id_column' as relationship,
  COUNT(*) as rows_in_table_a,
  COUNT(DISTINCT a.fk_column) as unique_fk_values,
  (SELECT COUNT(DISTINCT id_column) FROM table_b) as unique_ids_in_table_b
FROM table_a a;
```

**Test:** Do all fk_column values exist in table_b? (Referential integrity)

**Document:**
- Confirmed foreign key relationships
- Orphaned records (FKs with no matching primary key)
- Unused primary keys (keys with no foreign key references)

### Join Cardinality

```sql
-- Understand join behavior before using it
SELECT
  'table_a to table_b' as join_direction,
  COUNT(*) as rows_before_join,
  COUNT(b.id) as matches_found,
  COUNT(*) - COUNT(b.id) as rows_without_match
FROM table_a a
LEFT JOIN table_b b ON a.fk_column = b.id_column;
```

**Document:**
- One-to-one, one-to-many, or many-to-many?
- Percentage of successful joins
- Whether LEFT/INNER/OUTER JOIN is appropriate

### Cross-Table Consistency

```sql
-- Check if aggregates match between tables
SELECT 'table_a' as source, SUM(amount) as total FROM table_a
UNION ALL
SELECT 'table_b' as source, SUM(amount) as total FROM table_b;
```

**For fact tables that should reconcile.**

**Document:**
- Whether totals match expectations
- Discrepancies that need explanation

### Hierarchical Relationships

```sql
-- Find parent-child relationships
SELECT
  parent_id,
  COUNT(*) as child_count,
  COUNT(DISTINCT child_category) as distinct_child_types
FROM table_name
GROUP BY parent_id
ORDER BY child_count DESC;
```

**Document:**
- Hierarchical structures (customers > orders > line items)
- Depth of hierarchy
- Orphaned children or childless parents

---

## Documentation Requirements

After completing all 4 phases, create a summary document:

### Data Profile Summary

```markdown
## Data Profile Summary

### Tables
- `table_name` (X rows): Description and purpose

### Key Findings
- Data Quality: [Major issues or "clean"]
- Coverage: [Date ranges, completeness]
- Relationships: [How tables connect]

### Analysis Implications
- [What this data can/cannot answer]
- [Segments available for analysis]
- [Known limitations]

### Recommended Filters
- [Filters to apply for clean data]
- [Time periods to focus on]
```

---

## Common Pitfalls

**DON'T:**
- Assume column names accurately describe contents
- Skip Phase 2 (data quality) - dirty data leads to wrong conclusions
- Ignore NULL values - they often have business meaning
- Forget to check join cardinality before complex queries

**DO:**
- Verify assumptions with queries
- Document surprises and anomalies
- Note data quality issues for later interpretation
- Keep a running list of questions for data owners

---

## When to Re-Profile

Re-run portions of this skill when:
- Query results don't match expectations
- You discover a new table mid-analysis
- You suspect data quality issues
- Time period changes significantly (new data loaded)

---

## Integration with Process Skills

Process skills reference this component skill with:

```markdown
If unfamiliar with the data, use the `understanding-data` component skill to profile tables before proceeding.
```

This ensures analysts don't make assumptions about data structure or quality.

## Database Engine Specifics

This skill provides database-agnostic guidance with examples in multiple SQL dialects.

**Related skills for database-specific implementation:**
- `using-sqlite` - SQLite CLI usage, syntax, and optimizations
- `using-postgresql` - PostgreSQL-specific features (if available)
- Other database-specific skills for CLI commands, performance tuning, and engine-specific features
