---
name: sql-development
description: >
  Write, format, review, and optimize relational SQL queries following standard
  conventions. Use when composing complex SELECT queries with JOINs and CTEs,
  designing normalized schemas with primary/foreign key constraints, writing
  ACID transaction blocks, preventing SQL injection via parameterization, or
  reviewing query execution bottlenecks.
compatibility: >
  Agent Skills-compatible coding agents reading, writing, or optimizing SQL across
  relational databases (PostgreSQL, MySQL, SQLite).
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "sql, databases, rdbms, joins, ctes, transactions, query-optimization, acid"
  topics: "databases, software-development"
---

# Relational SQL Development and Query Design

Structured Query Language (SQL) is the foundational language of relational database management systems. Writing robust SQL requires clear formatting, precise JOIN semantics, proper use of Common Table Expressions (CTEs), strict referential integrity constraints, and disciplined transaction management.

## Core Rules

1. **Always parameterize queries**: Never concatenate user input into SQL strings. Use prepared statements and bind parameters (`$1`, `?`, or `:param`).
2. **Capitalize SQL keywords**: Write `SELECT`, `FROM`, `WHERE`, `JOIN`, `GROUP BY`, `ORDER BY` in uppercase for visual clarity and scanning speed.
3. **Always use explicit table aliases in multi-table queries**: Qualify every column with its table name or alias (e.g. `u.email`, `o.total_amount`) to prevent ambiguous column errors.
4. **Prefer CTEs (`WITH` clauses) over deeply nested subqueries**: CTEs break complex queries into readable, linear data-transformation steps.
5. **Always specify explicit `JOIN` types**: Never use implicit comma joins (`FROM users, orders WHERE ...`). Use explicit `INNER JOIN`, `LEFT JOIN`, etc.
6. **Enforce data integrity at the database layer**: Use `NOT NULL`, `CHECK`, `UNIQUE`, and `FOREIGN KEY` constraints rather than relying solely on application-level validation.

---

## 1. Clean Query Structure & Formatting

```sql
WITH active_customers AS (
    SELECT
        u.id AS user_id,
        u.email,
        u.created_at
    FROM users AS u
    WHERE u.status = 'ACTIVE'
      AND u.deleted_at IS NULL
),
customer_order_aggregates AS (
    SELECT
        o.user_id,
        COUNT(o.id) AS total_orders,
        SUM(o.amount_cents) AS total_spend_cents,
        MAX(o.ordered_at) AS latest_order_date
    FROM orders AS o
    WHERE o.status = 'COMPLETED'
    GROUP BY o.user_id
)
SELECT
    c.user_id,
    c.email,
    COALESCE(a.total_orders, 0) AS total_orders,
    COALESCE(a.total_spend_cents, 0) AS total_spend_cents,
    a.latest_order_date
FROM active_customers AS c
LEFT JOIN customer_order_aggregates AS a
    ON c.user_id = a.user_id
ORDER BY total_spend_cents DESC, c.user_id ASC
LIMIT 50;
```

---

## 2. Choosing the Correct JOIN Type

| Join Type | Behavior | When to Use |
| :--- | :--- | :--- |
| `INNER JOIN` | Returns rows only when keys match in **both** tables | Filtering results where related entity must exist (e.g. Orders with Customers) |
| `LEFT JOIN` | Returns **all** rows from left table, with NULLs for unmatched right rows | Preserving parent entities even if they have zero children (e.g. Users without orders) |
| `FULL OUTER JOIN` | Returns rows when there is a match in **either** table | Reconciling and identifying discrepancies across two data sets |
| `CROSS JOIN` | Cartesian product (every row combined with every row) | Generating grids, permutations, or date dimension series |

---

## 3. Schema Design and Constraints

Enforce business rules directly in table definitions:

```sql
CREATE TABLE accounts (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE RESTRICT,
    account_number VARCHAR(32) NOT NULL,
    currency CHAR(3) NOT NULL DEFAULT 'EUR',
    balance_cents BIGINT NOT NULL DEFAULT 0,
    status VARCHAR(16) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Business constraints
    CONSTRAINT chk_valid_status CHECK (status IN ('ACTIVE', 'SUSPENDED', 'CLOSED')),
    CONSTRAINT chk_positive_balance CHECK (balance_cents >= 0),
    CONSTRAINT uq_org_account_num UNIQUE (organization_id, account_number)
);

-- Indexing foreign keys (RDBMS does not automatically index FK columns!)
CREATE INDEX idx_accounts_organization_id ON accounts (organization_id);
```

---

## 4. ACID Transactions and Isolation

Transactions guarantee that multiple statements execute atomically:

```sql
BEGIN;

-- Deduct from source account
UPDATE accounts
SET balance_cents = balance_cents - 5000
WHERE id = 101 AND balance_cents >= 5000;

-- Ensure deduction occurred (check rows affected in application)
-- Add to target account
UPDATE accounts
SET balance_cents = balance_cents + 5000
WHERE id = 202;

-- Record audit ledger entry
INSERT INTO transfer_ledger (from_account_id, to_account_id, amount_cents)
VALUES (101, 202, 5000);

COMMIT;
```

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Performance / Bug Risk | Correct Practice |
| :--- | :--- | :--- |
| `SELECT *` in application queries | Unnecessary I/O, breaks when column order changes, blocks index-only scans | Explicitly select required columns: `SELECT u.id, u.email` |
| Missing `WHERE` in `UPDATE`/`DELETE` | Accidental catastrophic loss of all table data | Always double-check `WHERE` clause before execution |
| Comma joins: `FROM a, b WHERE a.id = b.a_id` | Accidental Cartesian products when WHERE conditions are omitted | Always use explicit `JOIN ... ON ...` |
| Functions on indexed columns in `WHERE` | Prevents index usage: `WHERE YEAR(created_at) = 2026` | Use range: `WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01'` |
| Storing financial amounts as `FLOAT` | Floating-point rounding inaccuracies | Use `BIGINT` (in cents) or `NUMERIC(12, 2)` |

---

## 6. Verification Checklist

- [ ] All dynamic variables are bound via parameters, not string concatenation.
- [ ] Columns are qualified with table names/aliases.
- [ ] No `SELECT *` in production queries.
- [ ] Foreign keys have matching B-tree indexes.
- [ ] Multi-step updates wrapped in explicit `BEGIN ... COMMIT` blocks.
