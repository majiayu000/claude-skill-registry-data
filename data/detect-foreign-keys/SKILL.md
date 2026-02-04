---
name: detect-foreign-keys
description: Identify foreign key relationships between tables using heuristics, value overlap analysis, and referential integrity checks
---

# Detecting Foreign Keys

## Purpose

This component skill guides systematic foreign key relationship detection in relational databases. Use it when:
- Multiple tables exist in the database and relationships are undocumented
- Need to understand table relationships before joining data
- Validating referential integrity between tables
- Identifying orphaned records that reference non-existent parent records
- Referenced by importing-data or cleaning-data skills requiring relationship analysis

## Prerequisites

- Tables exist in database (relational database with SQL support)
- SQL query tool available (database CLI, IDE, or query interface)
- Table schemas have been examined (Phase 1 of understanding-data)
- Analysis workspace created

## Foreign Key Detection Process

Create a TodoWrite checklist for the 5-phase FK detection process:

```
Phase 1: Candidate Identification - pending
Phase 2: Value Overlap Analysis - pending
Phase 3: Cardinality Assessment - pending
Phase 4: Referential Integrity Validation - pending
Phase 5: Relationship Documentation - pending
```

Mark each phase as you complete it. Document all findings in structured format.

---

## Phase 1: Candidate Identification

**Goal:** Identify columns that are likely foreign keys based on naming patterns, data types, and uniqueness.

### Identify Candidate FK Columns by Naming Convention

**Common FK naming patterns:**
- Columns ending in `_id` (e.g., `customer_id`, `product_id`)
- Columns ending in `Id` (e.g., `customerId`, `productId`)
- Columns named exactly `id` (but only in child tables)
- Columns starting with `fk_` (e.g., `fk_customer`)
- Columns matching another table name (e.g., `customer` in orders table)

```sql
-- List all columns across all tables
SELECT
  m.name as table_name,
  p.name as column_name,
  p.type as column_type
FROM sqlite_master m
JOIN pragma_table_info(m.name) p
WHERE m.type = 'table'
  AND m.name NOT LIKE 'sqlite_%'
  AND (
    p.name LIKE '%_id'
    OR p.name LIKE '%Id'
    OR p.name LIKE 'fk_%'
    OR p.name = 'id'
  )
ORDER BY m.name, p.name;
```

**Document:**
- List of candidate FK columns per table
- Note naming patterns observed
- Flag columns that might be composite keys (multiple FK columns in same table)

### Identify Candidate PK Columns

**Primary key characteristics:**
- Named `id`, `[table]_id`, or similar
- INTEGER or TEXT type
- Likely to be unique
- Often the first column in the table

```sql
-- Find columns likely to be primary keys
SELECT
  m.name as table_name,
  p.name as column_name,
  p.type as column_type,
  p.pk as is_primary_key
FROM sqlite_master m
JOIN pragma_table_info(m.name) p
WHERE m.type = 'table'
  AND m.name NOT LIKE 'sqlite_%'
  AND (
    p.pk = 1  -- Explicitly defined PK
    OR p.name = 'id'
    OR p.name = m.name || '_id'
  )
ORDER BY m.name;
```

**Document:**
- Primary key columns per table
- Whether PKs are explicitly defined (pk=1) or inferred
- Tables without obvious primary keys

### Match FK Candidates to Potential Parent Tables

**Heuristic:** A column named `customer_id` likely references a table named `customers` or `customer`.

```sql
-- Cross-reference FK column names with table names
-- (Pseudo-query - implement with string matching logic)
-- For each FK candidate like 'customer_id':
--   1. Strip suffix (_id, Id)
--   2. Look for table named 'customers', 'customer', or similar
--   3. Record as potential relationship
```

**Document:**
- FK candidate → Parent table mapping (e.g., `orders.customer_id` → `customers.id`)
- Confidence level:
  - **High:** Exact name match (e.g., `customer_id` → `customer` table)
  - **Medium:** Plural/singular variation (e.g., `customer_id` → `customers` table)
  - **Low:** Partial name match or ambiguous

---

## Phase 2: Value Overlap Analysis

**Goal:** Validate FK candidates by checking if their values actually exist in the proposed parent table.

### Check Value Overlap Percentage

For each candidate FK relationship identified in Phase 1:

```sql
-- Calculate what percentage of FK values exist in parent table
WITH fk_values AS (
  SELECT DISTINCT child_fk_column as value
  FROM child_table
  WHERE child_fk_column IS NOT NULL
),
pk_values AS (
  SELECT DISTINCT parent_pk_column as value
  FROM parent_table
  WHERE parent_pk_column IS NOT NULL
),
overlap AS (
  SELECT COUNT(*) as matching_count
  FROM fk_values fk
  WHERE fk.value IN (SELECT value FROM pk_values)
)
SELECT
  (SELECT COUNT(*) FROM fk_values) as total_fk_values,
  (SELECT COUNT(*) FROM pk_values) as total_pk_values,
  overlap.matching_count,
  ROUND(100.0 * overlap.matching_count / (SELECT COUNT(*) FROM fk_values), 2) as match_percentage
FROM overlap;
```

**Interpret match percentage:**
- **100% match:** Strong FK relationship (perfect referential integrity)
- **95-99% match:** Likely FK with some orphaned records
- **80-94% match:** Possible FK with significant orphans (investigate)
- **<80% match:** Unlikely to be true FK (name coincidence or wrong parent table)

**Document:**
- Match percentage for each candidate relationship
- Count of orphaned FK values (values not in parent)
- Count of unused PK values (values not referenced by any FK)

### Identify Orphaned Records

For relationships with <100% match:

```sql
-- Find child records with FK values that don't exist in parent
SELECT
  child_table.rowid,
  child_table.child_fk_column as orphaned_value,
  COUNT(*) OVER (PARTITION BY child_table.child_fk_column) as occurrences
FROM child_table
LEFT JOIN parent_table ON child_table.child_fk_column = parent_table.parent_pk_column
WHERE parent_table.parent_pk_column IS NULL
  AND child_table.child_fk_column IS NOT NULL
LIMIT 20;
```

**Document:**
- Sample orphaned values
- How many child records affected
- Whether orphaned values follow a pattern (all recent, specific category, etc.)

### Check Reverse Overlap (Unused Parent Records)

```sql
-- Find parent records not referenced by any child
SELECT
  parent_table.parent_pk_column as unused_pk_value,
  COUNT(*) as occurrence_count
FROM parent_table
LEFT JOIN child_table ON parent_table.parent_pk_column = child_table.child_fk_column
WHERE child_table.child_fk_column IS NULL
  AND parent_table.parent_pk_column IS NOT NULL
LIMIT 20;
```

**Document:**
- Count of unused parent records
- Whether this is expected (e.g., new customers with no orders yet)

---

## Phase 3: Cardinality Assessment

**Goal:** Determine the relationship type (one-to-one, one-to-many, many-to-many).

### Calculate FK → PK Cardinality

**How many child records per parent record?**

```sql
-- Average number of child records per parent
SELECT
  COUNT(*) as total_child_records,
  COUNT(DISTINCT child_fk_column) as distinct_fk_values,
  ROUND(1.0 * COUNT(*) / NULLIF(COUNT(DISTINCT child_fk_column), 0), 2) as avg_children_per_parent,
  MIN(child_count) as min_children,
  MAX(child_count) as max_children
FROM child_table
CROSS JOIN (
  SELECT
    child_fk_column as fk,
    COUNT(*) as child_count
  FROM child_table
  WHERE child_fk_column IS NOT NULL
  GROUP BY child_fk_column
);
```

**Interpret cardinality:**
- **avg = 1.0, max = 1:** One-to-one relationship
- **avg > 1.0:** One-to-many relationship (most common)
- **Multiple FK columns referencing same parent:** Potential many-to-many via junction table

**Document:**
- Relationship type (one-to-one, one-to-many)
- Average, min, max child records per parent
- Whether distribution is balanced or skewed

### Identify Many-to-Many Relationships

**Junction table characteristics:**
- Table has 2+ foreign keys
- Few or no other columns besides FKs
- Composite primary key (both FKs together)

```sql
-- Find tables with multiple FK candidates (potential junction tables)
SELECT
  table_name,
  COUNT(*) as fk_column_count,
  GROUP_CONCAT(column_name, ', ') as fk_columns
FROM (
  SELECT
    m.name as table_name,
    p.name as column_name
  FROM sqlite_master m
  JOIN pragma_table_info(m.name) p
  WHERE m.type = 'table'
    AND m.name NOT LIKE 'sqlite_%'
    AND (p.name LIKE '%_id' OR p.name LIKE 'fk_%')
)
GROUP BY table_name
HAVING COUNT(*) >= 2
ORDER BY fk_column_count DESC;
```

**Document:**
- Junction tables identified
- Which two (or more) tables they connect
- Cardinality of the many-to-many relationship

### Check for Self-Referencing FKs

**Hierarchical data pattern:**
- Table has FK pointing to its own PK (e.g., `employee.manager_id` → `employee.id`)

```sql
-- Find columns that might reference the same table
SELECT
  table_name,
  column_name,
  type
FROM (
  SELECT
    m.name as table_name,
    p.name as column_name,
    p.type as type
  FROM sqlite_master m
  JOIN pragma_table_info(m.name) p
  WHERE m.type = 'table'
    AND m.name NOT LIKE 'sqlite_%'
    AND (
      p.name LIKE 'parent_%'
      OR p.name LIKE 'manager_%'
      OR p.name LIKE '%_parent_id'
    )
);
```

**Document:**
- Self-referencing relationships
- Depth of hierarchy (max levels)
- Orphaned roots or cycles

---

## Phase 4: Referential Integrity Validation

**Goal:** Quantify integrity violations and assess data quality impact.

### Calculate Integrity Violation Rate

For each confirmed FK relationship:

```sql
-- Comprehensive referential integrity check
WITH integrity_check AS (
  SELECT
    COUNT(*) as total_child_records,
    COUNT(child_fk_column) as non_null_fk_count,
    COUNT(*) - COUNT(child_fk_column) as null_fk_count,
    SUM(CASE WHEN p.parent_pk_column IS NULL AND c.child_fk_column IS NOT NULL THEN 1 ELSE 0 END) as orphaned_count
  FROM child_table c
  LEFT JOIN parent_table p ON c.child_fk_column = p.parent_pk_column
)
SELECT
  total_child_records,
  non_null_fk_count,
  null_fk_count,
  ROUND(100.0 * null_fk_count / total_child_records, 2) as null_fk_pct,
  orphaned_count,
  ROUND(100.0 * orphaned_count / non_null_fk_count, 2) as orphaned_pct,
  non_null_fk_count - orphaned_count as valid_fk_count,
  ROUND(100.0 * (non_null_fk_count - orphaned_count) / non_null_fk_count, 2) as integrity_pct
FROM integrity_check;
```

**Document:**
- Total child records
- NULL FK percentage (records with no parent reference)
- Orphaned FK percentage (records referencing non-existent parent)
- Valid FK percentage (clean referential integrity)

### Assess Impact of Integrity Violations

**Business impact depends on:**
- How joins will be used (INNER vs LEFT)
- Whether orphaned records are recent (data entry lag) or old (data quality issue)
- Whether NULL FKs are expected (optional relationships)

```sql
-- Analyze orphaned records by recency
SELECT
  CASE
    WHEN date_column >= date('now', '-7 days') THEN 'Last 7 days'
    WHEN date_column >= date('now', '-30 days') THEN 'Last 30 days'
    WHEN date_column >= date('now', '-90 days') THEN 'Last 90 days'
    ELSE 'Older than 90 days'
  END as recency,
  COUNT(*) as orphaned_count
FROM child_table c
LEFT JOIN parent_table p ON c.child_fk_column = p.parent_pk_column
WHERE p.parent_pk_column IS NULL
  AND c.child_fk_column IS NOT NULL
  AND c.date_column IS NOT NULL
GROUP BY recency
ORDER BY MIN(c.date_column);
```

**Document:**
- Whether orphans are recent (may resolve soon) or old (permanent issue)
- Impact on analytical queries (e.g., "10% of orders will be excluded in INNER JOIN to customers")

### Validate Composite Keys

If multiple columns together form a FK:

```sql
-- Check integrity for composite FK
WITH composite_fk_values AS (
  SELECT DISTINCT
    child_table.fk_column1,
    child_table.fk_column2
  FROM child_table
  WHERE child_table.fk_column1 IS NOT NULL
    AND child_table.fk_column2 IS NOT NULL
),
composite_pk_values AS (
  SELECT DISTINCT
    parent_table.pk_column1,
    parent_table.pk_column2
  FROM parent_table
)
SELECT
  COUNT(*) as total_composite_fk_values,
  SUM(CASE WHEN pk.pk_column1 IS NULL THEN 1 ELSE 0 END) as orphaned_count
FROM composite_fk_values fk
LEFT JOIN composite_pk_values pk
  ON fk.fk_column1 = pk.pk_column1
  AND fk.fk_column2 = pk.pk_column2;
```

**Document:**
- Composite key relationships identified
- Integrity percentage for composite keys

---

## Phase 5: Relationship Documentation

**Goal:** Create structured documentation of all discovered relationships for use in cleaning and analysis.

### Create Relationship Catalog

Document each confirmed relationship:

```markdown
## Foreign Key Relationships

### High Confidence Relationships (>95% integrity)

#### orders.customer_id → customers.id
- **Relationship Type:** Many-to-one
- **Child Table:** orders (1,523 rows)
- **Parent Table:** customers (342 rows)
- **Match Percentage:** 98.2%
- **Cardinality:** Avg 4.5 orders per customer (min: 1, max: 47)
- **NULL FKs:** 12 rows (0.8%)
- **Orphaned FKs:** 15 rows (1.0%)
- **Recommended Join:** LEFT JOIN (to preserve orphaned orders)
- **Cleaning Action:** Investigate 15 orphaned orders, flag for review

### Medium Confidence Relationships (80-95% integrity)

#### products.category_id → categories.id
- **Relationship Type:** Many-to-one
- **Child Table:** products (856 rows)
- **Parent Table:** categories (24 rows)
- **Match Percentage:** 87.3%
- **Cardinality:** Avg 35.7 products per category (min: 2, max: 142)
- **NULL FKs:** 89 rows (10.4%)
- **Orphaned FKs:** 20 rows (2.4%)
- **Recommended Join:** INNER JOIN (if categorized products only needed)
- **Cleaning Action:** Exclude or recategorize 20 orphaned products

### Low Confidence / Unconfirmed (<80% integrity)

#### transactions.merchant_id → merchants.id
- **Relationship Type:** Uncertain
- **Match Percentage:** 67.8%
- **Issue:** Large number of orphaned merchant_id values
- **Recommendation:** Verify with data owner - may be wrong parent table
```

### Create Join Recommendations

For each relationship:

```markdown
## Join Recommendations

### orders ⟶ customers

**Recommended SQL:**
```sql
-- Use LEFT JOIN to preserve all orders (including orphans)
SELECT
  o.*,
  c.customer_name,
  c.customer_segment
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.id;

-- Alternative: INNER JOIN if orphans should be excluded
SELECT
  o.*,
  c.customer_name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id;
-- Note: Excludes 15 orders (1.0%) with invalid customer_id
```

**Join Impact:**
- LEFT JOIN: Preserves all 1,523 orders (15 will have NULL customer fields)
- INNER JOIN: Returns 1,508 orders (99.0% of total)
- Recommendation: Use LEFT JOIN, filter nulls in WHERE clause if needed
```

### Document Data Quality Implications

```markdown
## Data Quality Implications

### Orphaned Records Summary

Total orphaned records across all relationships: 35 (2.1% of all child records)

| Child Table | FK Column | Orphan Count | % of Child Table | Impact |
|-------------|-----------|--------------|------------------|--------|
| orders | customer_id | 15 | 1.0% | Low - recent orders, may resolve |
| products | category_id | 20 | 2.4% | Medium - affects category analysis |

### Recommended Cleaning Actions

**High Priority:**
1. products.category_id orphans (20 rows) - CREATE placeholder category "Uncategorized" or exclude from analysis
2. orders.customer_id orphans (15 rows) - FLAG for customer service review

**Medium Priority:**
3. NULL customer_id in orders (12 rows) - Investigate if legitimate (guest checkout?) or data entry error

### Analysis Limitations

Due to referential integrity issues:
- Customer-level aggregations will exclude 1.0% of orders (if using INNER JOIN)
- Category-level product analysis may be incomplete (2.4% of products uncategorized)
- Time-series trends should use LEFT JOIN to preserve all records
```

---

## Integration with Other Skills

### With `importing-data` (Phase 5: Quality Assessment)

After importing tables, run FK detection to include in quality report:

```markdown
## Foreign Key Relationships (from detect-foreign-keys skill)

High Confidence:
- orders.customer_id → customers.id (98% integrity, 15 orphans)
- ...

Medium Confidence:
- products.category_id → categories.id (87% integrity, 20 orphans)
```

### With `cleaning-data` (Phase 1: Scope Definition)

Use FK findings to inform cleaning scope:

```markdown
## Referential Integrity Issues

From detect-foreign-keys analysis:
- **orders.customer_id:** 15 orphaned records (1.0%) - Priority: HIGH
  - Recommended action: Flag for review, preserve with LEFT JOIN
```

### With `understanding-data` (Phase 4: Relationship Identification)

This skill provides the systematic process for Phase 4:

```markdown
## Phase 4: Relationship Identification

Use the `detect-foreign-keys` component skill to systematically identify and validate all foreign key relationships.
```

---

## Common Pitfalls

**DON'T:**
- Assume naming conventions are always correct (validate with value overlap)
- Skip Phase 4 integrity validation - orphaned records break analyses
- Use INNER JOIN without understanding orphan impact
- Ignore NULL FKs - they may be legitimate or data quality issues

**DO:**
- Validate every candidate FK with value overlap analysis (Phase 2)
- Quantify integrity violations with exact counts and percentages
- Document both high-confidence and uncertain relationships
- Provide join recommendations based on integrity findings
- Feed FK findings back into cleaning-data scope

---

## When to Re-Run

Re-run this skill when:
- New tables are added to the database
- Referential integrity violations are suspected
- Planning complex multi-table analyses
- Cleaning activities might have affected FK relationships
- Data loads introduce new orphaned records

---

## Success Criteria

After completing this skill, you should have:
- ✅ Complete catalog of FK relationships with confidence levels
- ✅ Integrity percentages for each relationship
- ✅ Count and examples of orphaned records
- ✅ Cardinality assessment (one-to-one, one-to-many, many-to-many)
- ✅ Join recommendations (LEFT vs INNER, filters needed)
- ✅ Data quality implications documented
- ✅ Cleaning actions prioritized

This documentation feeds into importing-data quality reports and cleaning-data scope definitions, ensuring relationship-aware data quality management.
