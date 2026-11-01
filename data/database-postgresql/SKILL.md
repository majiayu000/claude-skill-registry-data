---
name: database-postgresql
description: Database Engineer — PostgreSQL / TimescaleDB — Institutional capability and runbook for database-postgresql.
---

# SKILL: Database Engineer — PostgreSQL / TimescaleDB
## Domain: Schema Design, Migrations, Query Optimization

**Activation triggers:** new table, schema change, migration, index design,
query optimization, TimescaleDB hypertable, pgvector, RBAC DB functions.

---

## Schema Design Rules

```sql
-- Every table MUST have:
--   id UUID PRIMARY KEY DEFAULT gen_random_uuid()
--   created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
--   updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- Soft deletes: deleted_at TIMESTAMPTZ (never hard delete users/accounts)

CREATE TABLE journal.trades (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES iam.users(id) ON DELETE CASCADE,
    journal_id      UUID NOT NULL REFERENCES journal.journals(id) ON DELETE CASCADE,
    symbol          TEXT NOT NULL,
    direction       TEXT NOT NULL CHECK (direction IN ('long', 'short')),
    open_price      NUMERIC(20,8) NOT NULL,
    close_price     NUMERIC(20,8),
    lot_size        NUMERIC(10,4) NOT NULL,
    pnl             NUMERIC(20,8),
    status          TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'closed', 'cancelled')),
    opened_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    closed_at       TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index ALL FK columns
CREATE INDEX idx_trades_user_id ON journal.trades(user_id);
CREATE INDEX idx_trades_journal_id ON journal.trades(journal_id);
-- Index query predicates
CREATE INDEX idx_trades_status ON journal.trades(status) WHERE status = 'open';
-- Composite indexes for common query patterns
CREATE INDEX idx_trades_user_opened ON journal.trades(user_id, opened_at DESC);
```

---

## Migration Protocol

```bash
# 1. Write the SQL migration
cat > schema_files/12_new_feature.sql << 'EOF'
-- Up migration
ALTER TABLE journal.trades ADD COLUMN tags TEXT[] DEFAULT '{}';
CREATE INDEX idx_trades_tags ON journal.trades USING GIN(tags);

-- Down migration (rollback)
-- ALTER TABLE journal.trades DROP COLUMN tags;
EOF

# 2. Generate Alembic version
cd integral-expert-backend
alembic revision --autogenerate -m "add tags to trades"

# 3. Review the generated migration
# 4. Test on dev
alembic upgrade head

# 5. Never auto-apply on production without review
```

---

## Query Optimization Checklist

```sql
-- ALWAYS: EXPLAIN ANALYZE before declaring a query done
EXPLAIN ANALYZE
SELECT t.id, t.symbol, t.pnl
FROM journal.trades t
WHERE t.user_id = $1
  AND t.status = 'closed'
  AND t.closed_at > NOW() - INTERVAL '30 days'
ORDER BY t.closed_at DESC
LIMIT 50;

-- Look for:
-- ✓ Index Scan (good)
-- ✗ Seq Scan on large table (add index)
-- ✗ Hash Join with large row estimate (check indexes)
-- ✗ Nested Loop with > 100 rows (may need index or query rewrite)
```

---

## TimescaleDB Hypertables

```sql
-- Convert time-series tables to hypertables
SELECT create_hypertable('copy_trading.execution_logs', 'executed_at',
    chunk_time_interval => INTERVAL '1 week',
    if_not_exists => TRUE
);

-- IMPORTANT: TimescaleDB removes FK constraints on hypertables
-- SQLAlchemy models MUST still declare ForeignKey() for ORM relationships
-- The FK won't be enforced at DB level but ORM needs it for join resolution

-- Continuous aggregates for analytics
CREATE MATERIALIZED VIEW copy_trading.daily_pnl
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 day', executed_at) AS day,
    subscription_id,
    SUM(pnl_amount) AS total_pnl,
    COUNT(*) AS trade_count
FROM copy_trading.execution_logs
GROUP BY 1, 2;
```

---

## RBAC Database Functions

```sql
-- Always use parameterized functions, never inline SQL in application
CREATE OR REPLACE FUNCTION iam.get_user_permissions(p_user_id UUID)
RETURNS TABLE(resource TEXT, action TEXT) AS $$
    SELECT DISTINCT p.resource, p.action
    FROM iam.user_roles ur
    JOIN iam.role_permissions rp ON rp.role_id = ur.role_id
    JOIN iam.permissions p ON p.id = rp.permission_id
    WHERE ur.user_id = p_user_id
      AND ur.is_active = TRUE
      AND (ur.expires_at IS NULL OR ur.expires_at > NOW())
      AND rp.is_active = TRUE
      AND p.is_active = TRUE;
$$ LANGUAGE SQL STABLE SECURITY DEFINER;
```

---

## Anti-Patterns

```
✗ Missing index on FK columns (causes seq scan on joins)
✗ Storing JSON blobs instead of normalized tables for queryable data
✗ Using TEXT for monetary values (use NUMERIC(20,8))
✗ Missing ON DELETE behavior on FK (choose CASCADE, SET NULL, or RESTRICT explicitly)
✗ Auto-applying Alembic migrations without review
✗ Dropping columns directly (soft delete first, drop after 2 releases)
✗ SELECT * in production queries (always specify columns)
✗ Non-parameterized queries (SQL injection risk)
```
