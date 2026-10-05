---
name: db-analyzer
description: Database schema analysis, optimization, and health check for PostgreSQL databases in Spring Boot / JPA projects. Use when user says "analyze database", "check schema", "optimize DB", "db health", "missing indexes", "schema drift", "database review", or when investigating slow queries, data integrity issues, or planning schema migrations. This skill connects to the actual database via MCP postgres to perform live analysis — it does not just review code. Use it proactively when PRs touch JPA entities, repositories, or Flyway/Liquibase migrations.
user_invocable: true
---

# Database Analyzer Skill

Live database analysis and optimization for PostgreSQL schemas in Spring Boot / JPA applications. Connects to the real database via MCP `mcp__postgres__query` tool.

## Core Principle

> The database is the truth. JPA entities, Hibernate mappings, and application code are opinions about the truth. When they diverge, the database wins — and your application loses.

---

## Usage

```
/db-analyzer                    → Full health check on ONLINE schema
/db-analyzer indexes            → Index analysis only
/db-analyzer drift              → Entity-DB alignment check
/db-analyzer table <name>       → Deep dive on a specific table
/db-analyzer fk                 → Foreign key integrity analysis
/db-analyzer performance        → Query performance & bloat analysis
/db-analyzer security           → Sensitive data & permissions audit
/db-analyzer migration <desc>   → Pre-migration safety check
```

---

## Prerequisites

- MCP postgres server must be configured and connected (`.mcp.json`)
- The target schema is `ONLINE` (case-sensitive in this database)
- Reference analysis available at `docs/analisisBBDD.md` in the project root

---

## Phase 1: Schema Health Check

Quick snapshot of overall schema health. Run this first for any database review.

### 1.1 Basic Metrics

```sql
-- Table count by type
SELECT table_type, COUNT(*) FROM information_schema.tables
WHERE table_schema = 'ONLINE' GROUP BY table_type;

-- Total columns
SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = 'ONLINE';

-- Total constraints by type
SELECT constraint_type, COUNT(*) FROM information_schema.table_constraints
WHERE table_schema = 'ONLINE' GROUP BY constraint_type;

-- Total indexes
SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'ONLINE';

-- Total sequences
SELECT COUNT(*) FROM information_schema.sequences WHERE sequence_schema = 'ONLINE';
```

### 1.2 Tables Without Primary Key

```sql
SELECT t.table_name
FROM information_schema.tables t
WHERE t.table_schema = 'ONLINE' AND t.table_type = 'BASE TABLE'
  AND NOT EXISTS (
    SELECT 1 FROM information_schema.table_constraints tc
    WHERE tc.table_schema = t.table_schema AND tc.table_name = t.table_name
      AND tc.constraint_type = 'PRIMARY KEY'
  )
ORDER BY t.table_name;
```

**Assessment criteria:**
- Junction/relation tables (`r_*`, `aux_*`) without PK: **LOW risk** if small
- Domain tables (`d_*`) without PK: **HIGH risk** — may cause Hibernate issues
- Execution process tables without PK: **MEDIUM risk** — may accumulate without cleanup

### 1.3 Data Type Consistency

```sql
-- Find mixed boolean patterns (boolean vs numeric(1,0))
SELECT table_name, column_name, data_type, numeric_precision, numeric_scale
FROM information_schema.columns
WHERE table_schema = 'ONLINE'
  AND ((data_type = 'numeric' AND numeric_precision = 1 AND numeric_scale = 0)
       OR data_type = 'boolean')
ORDER BY table_name, column_name;
```

**Flag:** Tables mixing `boolean` and `numeric(1,0)` — indicates legacy evolution. New columns should use `boolean`.

```sql
-- Find json vs jsonb usage
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'ONLINE' AND data_type IN ('json', 'jsonb')
ORDER BY data_type, table_name;
```

**Flag:** `json` columns should be migrated to `jsonb` for better indexing and query performance.

---

## Phase 2: Index Analysis

### 2.1 Missing Indexes on Foreign Keys

The most common cause of slow DELETE cascades and JOIN performance issues.

```sql
-- Find FK columns that lack a dedicated index on the referencing side
SELECT
    tc.table_name,
    kcu.column_name AS fk_column,
    ccu.table_name AS referenced_table
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage ccu
    ON tc.constraint_name = ccu.constraint_name AND tc.table_schema = ccu.constraint_schema
WHERE tc.table_schema = 'ONLINE' AND tc.constraint_type = 'FOREIGN KEY'
  AND NOT EXISTS (
    SELECT 1 FROM pg_indexes pi
    WHERE pi.schemaname = 'ONLINE'
      AND pi.tablename = tc.table_name
      AND pi.indexdef LIKE '%' || kcu.column_name || '%'
  )
ORDER BY tc.table_name;
```

**Severity:** HIGH for FK columns in high-volume tables (`d_forecast`, `d_movement`, `d_spot`), MEDIUM for configuration tables.

### 2.2 Unused Indexes

```sql
-- Indexes with zero scans (potential candidates for removal)
SELECT
    schemaname, relname AS table_name, indexrelname AS index_name,
    idx_scan, idx_tup_read, idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE schemaname = 'ONLINE' AND idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

**Caution:** Zero-scan indexes might be used by:
- Unique constraints (enforcement, not scanning)
- Rarely-executed reports or batch jobs
- Code paths not yet exercised in dev

**Recommendation:** Flag but do NOT recommend removal without verifying against production stats.

### 2.3 Duplicate/Redundant Indexes

```sql
-- Find indexes where one is a prefix of another (the shorter one may be redundant)
SELECT
    a.tablename,
    a.indexname AS index_1,
    a.indexdef AS def_1,
    b.indexname AS index_2,
    b.indexdef AS def_2
FROM pg_indexes a
JOIN pg_indexes b ON a.schemaname = b.schemaname AND a.tablename = b.tablename
    AND a.indexname != b.indexname
WHERE a.schemaname = 'ONLINE'
    AND b.indexdef LIKE '%' || substring(a.indexdef FROM '\(.*\)') || '%'
    AND length(a.indexdef) < length(b.indexdef)
ORDER BY a.tablename;
```

### 2.4 Over-Indexed Tables

```sql
-- Tables with more indexes than columns (potential write performance issue)
SELECT
    t.table_name,
    (SELECT COUNT(*) FROM information_schema.columns c
     WHERE c.table_schema = t.table_schema AND c.table_name = t.table_name) AS column_count,
    (SELECT COUNT(*) FROM pg_indexes pi
     WHERE pi.schemaname = 'ONLINE' AND pi.tablename = t.table_name) AS index_count
FROM information_schema.tables t
WHERE t.table_schema = 'ONLINE' AND t.table_type = 'BASE TABLE'
HAVING (SELECT COUNT(*) FROM pg_indexes pi WHERE pi.schemaname = 'ONLINE' AND pi.tablename = t.table_name)
     > (SELECT COUNT(*) FROM information_schema.columns c WHERE c.table_schema = t.table_schema AND c.table_name = t.table_name) * 0.5
ORDER BY index_count DESC;
```

---

## Phase 3: Entity-Database Drift Detection

Compare JPA entity definitions against the actual database schema.

### 3.1 Methodology

```
For each JPA @Entity in the project:
1. Read the entity class — extract table name, column names, types, nullable, length
2. Query information_schema.columns for the actual table
3. Compare: column-by-column alignment
4. Report drift
```

### 3.2 Common Drift Patterns

| Drift Type | JPA Side | DB Side | Risk |
|------------|----------|---------|------|
| **Nullable mismatch** | `@Column(nullable=false)` | Column allows NULL | Data corruption: DB accepts nulls that entity says shouldn't exist |
| **Length mismatch** | `@Column(length=100)` | `varchar(255)` | Silent truncation or wasted space |
| **Missing column** | Entity has field | Column doesn't exist in DB | Application crash on query |
| **Extra column** | No field in entity | Column exists in DB | Invisible data — may contain important legacy values |
| **Type mismatch** | `Boolean` field | `numeric(1,0)` column | Works via Hibernate type conversion but fragile |
| **Missing FK** | `@ManyToOne` | No FK constraint in DB | Orphan records possible |
| **Index mismatch** | `@Table(indexes=...)` | Different indexes in DB | Hibernate DDL not applied; DB has its own indexes |

### 3.3 Detecting Orphan Records

For tables with `@ManyToOne` but no DB-level FK:

```sql
-- Template: find orphan records
SELECT child.id, child.<fk_column>
FROM "ONLINE".<child_table> child
LEFT JOIN "ONLINE".<parent_table> parent ON child.<fk_column> = parent.<pk_column>
WHERE parent.<pk_column> IS NULL AND child.<fk_column> IS NOT NULL;
```

---

## Phase 4: Query Performance Analysis

### 4.1 Table Bloat & Vacuum Stats

```sql
SELECT
    relname AS table_name,
    n_live_tup AS live_rows,
    n_dead_tup AS dead_rows,
    CASE WHEN n_live_tup > 0
         THEN round(100.0 * n_dead_tup / (n_live_tup + n_dead_tup), 2)
         ELSE 0
    END AS dead_pct,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
WHERE schemaname = 'ONLINE'
ORDER BY n_dead_tup DESC
LIMIT 20;
```

**Flag:** Tables with >20% dead rows need VACUUM. Tables never analyzed have stale statistics.

### 4.2 Table Sizes

```sql
SELECT
    tablename AS table_name,
    pg_size_pretty(pg_total_relation_size('"ONLINE"."' || tablename || '"')) AS total_size,
    pg_size_pretty(pg_relation_size('"ONLINE"."' || tablename || '"')) AS table_size,
    pg_size_pretty(pg_total_relation_size('"ONLINE"."' || tablename || '"') - pg_relation_size('"ONLINE"."' || tablename || '"')) AS index_size
FROM pg_tables
WHERE schemaname = 'ONLINE'
ORDER BY pg_total_relation_size('"ONLINE"."' || tablename || '"') DESC
LIMIT 20;
```

### 4.3 Sequential Scans vs Index Scans

```sql
SELECT
    relname AS table_name,
    seq_scan,
    idx_scan,
    CASE WHEN (seq_scan + idx_scan) > 0
         THEN round(100.0 * seq_scan / (seq_scan + idx_scan), 2)
         ELSE 0
    END AS seq_scan_pct,
    seq_tup_read,
    idx_tup_fetch
FROM pg_stat_user_tables
WHERE schemaname = 'ONLINE' AND (seq_scan + idx_scan) > 100
ORDER BY seq_scan_pct DESC
LIMIT 20;
```

**Flag:** Tables with >80% sequential scans and >1000 rows are candidates for missing indexes.

### 4.4 Slow Query Candidates (Lock Contention)

```sql
-- Tables with high lock waits (if pg_stat_statements available)
SELECT
    relname,
    n_tup_ins AS inserts,
    n_tup_upd AS updates,
    n_tup_del AS deletes,
    n_tup_hot_upd AS hot_updates
FROM pg_stat_user_tables
WHERE schemaname = 'ONLINE'
ORDER BY (n_tup_upd + n_tup_del) DESC
LIMIT 15;
```

---

## Phase 5: Foreign Key Integrity

### 5.1 Circular Dependencies

```sql
-- Find bidirectional FK relationships (A->B AND B->A)
WITH fk_pairs AS (
    SELECT
        kcu.table_name AS source_table,
        ccu.table_name AS target_table
    FROM information_schema.key_column_usage kcu
    JOIN information_schema.referential_constraints rc
        ON kcu.constraint_name = rc.constraint_name AND kcu.table_schema = rc.constraint_schema
    JOIN information_schema.constraint_column_usage ccu
        ON rc.unique_constraint_name = ccu.constraint_name
    WHERE kcu.table_schema = 'ONLINE'
)
SELECT a.source_table, a.target_table
FROM fk_pairs a
JOIN fk_pairs b ON a.source_table = b.target_table AND a.target_table = b.source_table
WHERE a.source_table < a.target_table;
```

**Known circular dependency in this schema:** `d_ftp_model_details_level1 <-> d_ftp_model_details_level2`

### 5.2 Self-Referencing Tables

```sql
SELECT
    kcu.table_name,
    kcu.column_name AS fk_column,
    ccu.column_name AS references_column
FROM information_schema.key_column_usage kcu
JOIN information_schema.referential_constraints rc
    ON kcu.constraint_name = rc.constraint_name AND kcu.table_schema = rc.constraint_schema
JOIN information_schema.constraint_column_usage ccu
    ON rc.unique_constraint_name = ccu.constraint_name
WHERE kcu.table_schema = 'ONLINE' AND kcu.table_name = ccu.table_name
ORDER BY kcu.table_name;
```

### 5.3 FK Cascade Behavior

```sql
SELECT
    tc.table_name,
    tc.constraint_name,
    rc.update_rule,
    rc.delete_rule
FROM information_schema.table_constraints tc
JOIN information_schema.referential_constraints rc
    ON tc.constraint_name = rc.constraint_name AND tc.table_schema = rc.constraint_schema
WHERE tc.table_schema = 'ONLINE' AND tc.constraint_type = 'FOREIGN KEY'
    AND (rc.delete_rule != 'NO ACTION' OR rc.update_rule != 'NO ACTION')
ORDER BY tc.table_name;
```

**Flag:** CASCADE DELETE on hub tables (`d_scenario`, `d_curve`, `d_business_unit`) is extremely dangerous — deleting one row could cascade across dozens of tables.

---

## Phase 6: Security & Sensitive Data

### 6.1 Potential Sensitive Data

```sql
-- Find columns that might contain sensitive data by name pattern
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'ONLINE'
    AND (column_name ILIKE '%password%'
         OR column_name ILIKE '%secret%'
         OR column_name ILIKE '%token%'
         OR column_name ILIKE '%cert%'
         OR column_name ILIKE '%key%'
         OR column_name ILIKE '%credential%'
         OR column_name ILIKE '%ssn%'
         OR column_name ILIKE '%email%')
ORDER BY table_name, column_name;
```

### 6.2 Database Roles & Permissions

```sql
-- Check current user permissions on the schema
SELECT grantee, privilege_type, table_name
FROM information_schema.role_table_grants
WHERE table_schema = 'ONLINE' AND grantee = current_user
ORDER BY table_name
LIMIT 30;
```

---

## Phase 7: Pre-Migration Safety Check

Use this when planning schema changes (new columns, index additions, FK changes).

### Checklist before any migration:

| Check | Query/Action | Why |
|-------|-------------|-----|
| Table size | `SELECT pg_size_pretty(pg_total_relation_size(...))` | Large tables need online DDL or downtime |
| Active connections | `SELECT count(*) FROM pg_stat_activity WHERE datname = current_database()` | Migrations may lock tables |
| Dependent FKs | Query `information_schema.referential_constraints` | Adding NOT NULL or changing types affects referencing tables |
| Index impact | Count existing indexes | Adding more indexes to over-indexed tables degrades writes |
| Backup tables | Check if `*_backup` table exists | Some tables have backup copies that need parallel migration |
| Entity alignment | Compare JPA entity with DB column | Migration should match what JPA expects |

### Lock-safe DDL patterns for PostgreSQL:

```sql
-- ✅ Safe: ADD COLUMN with default (PostgreSQL 11+, no table rewrite)
ALTER TABLE "ONLINE".d_example ADD COLUMN new_col boolean DEFAULT false;

-- ⚠️ Risky: ADD COLUMN NOT NULL without default (requires table rewrite)
ALTER TABLE "ONLINE".d_example ADD COLUMN new_col boolean NOT NULL;

-- ✅ Safe: CREATE INDEX CONCURRENTLY (no lock)
CREATE INDEX CONCURRENTLY idx_example ON "ONLINE".d_example (column_name);

-- ⚠️ Risky: CREATE INDEX (locks table for writes)
CREATE INDEX idx_example ON "ONLINE".d_example (column_name);

-- ✅ Safe: Adding FK with NOT VALID + separate VALIDATE
ALTER TABLE "ONLINE".d_example ADD CONSTRAINT fk_example
    FOREIGN KEY (col) REFERENCES "ONLINE".d_parent(id) NOT VALID;
ALTER TABLE "ONLINE".d_example VALIDATE CONSTRAINT fk_example;
```

---

## Phase 8: Deep Dive on Specific Table

When invoked with `/db-analyzer table <name>`, perform a comprehensive analysis of a single table:

```
1. Full column listing with types, nullability, defaults
2. All constraints (PK, FK, UNIQUE, CHECK)
3. All indexes with definitions
4. Row count and table size
5. Dead rows / vacuum stats
6. FK references TO this table (what depends on it)
7. FK references FROM this table (what it depends on)
8. Corresponding JPA entity (search in src/main/java)
9. Entity-DB drift analysis
10. Recent DML stats (inserts, updates, deletes)
```

---

## Output Format

```markdown
## Database Analysis Report: [Schema / Table / Area]

### Health Score: [HEALTHY / NEEDS ATTENTION / CRITICAL]

### Summary
| Metric | Value | Status |
|--------|-------|--------|
| Tables without PK | N | ⚠️/✅ |
| Missing FK indexes | N | ⚠️/✅ |
| Entity-DB drift | N mismatches | ⚠️/✅ |
| Dead row ratio | N% | ⚠️/✅ |
| json columns (should be jsonb) | N | ⚠️/✅ |

### Critical Issues
| Location | Issue | Impact | Recommendation |
|----------|-------|--------|----------------|
| d_user_authorities | No PK, no indexes | Auth query performance | Add composite PK |
| d_bullet.id_nat_elasticity | FK without index | Slow DELETE on d_elasticity | CREATE INDEX CONCURRENTLY |

### Optimization Opportunities
| Table | Current | Recommended | Expected Impact |
|-------|---------|-------------|-----------------|
| d_behaviour_formula.formula | json | jsonb | Enables GIN indexing, faster queries |
| d_bullet.ind_balloon_* | numeric(1,0) | boolean | Cleaner types, smaller storage |

### Entity-DB Drift
| Entity | Field | JPA Definition | DB Reality | Action |
|--------|-------|---------------|------------|--------|
| Curve.java | descCurve | @Column(length=255) | varchar(500) | Update entity annotation |

### Index Recommendations
| Table | Column(s) | Type | Reason |
|-------|-----------|------|--------|
| d_bullet | id_nat_elasticity | btree | FK column, no index |
| d_forecast | id_nat_data_date_curve, forecast_date | btree | Composite for range queries |

### Migration Safety Notes
- [Any warnings about specific tables that need special handling]
- [Estimated lock duration for recommended changes]
- [Order of operations for dependent changes]
```

---

## Quick Reference: Known Schema Characteristics

These are documented characteristics of the ONLINE schema (see `docs/analisisBBDD.md`):

| Characteristic | Details |
|---------------|---------|
| Hub tables | `d_scenario` (23 refs), `d_curve` (23), `d_business_unit` (20) |
| Versioning | `version` varchar(14) in 80 tables, format `V.XXXXXXXX` |
| Base/Override pattern | 16 self-referencing tables (`id_nat_base_*`) |
| Circular FK | `d_ftp_model_details_level1 <-> d_ftp_model_details_level2` |
| Wide table | `d_manual_contract` (173 columns, all varchar(250)) |
| Mixed booleans | `boolean` coexists with `numeric(1,0)` for `ind_*` columns |
| json vs jsonb | 6 formula columns use `json`, 15 others use `jsonb` |
| Tables without PK | 16 tables |
| Tables without indexes | 12 tables |

---

## Integration with Other Skills

| When you find... | Also run... |
|-----------------|-------------|
| Entity-DB drift | `/check-legacy` on the entity class |
| N+1 query patterns | `/jpa-patterns` for fetch strategy review |
| Transaction boundary issues | `/check-architecture` Phase 4 |
| Slow queries from JPA | `/code-quality` Performance section |
| Schema changes in PR | `/deep-review` for impact analysis |
