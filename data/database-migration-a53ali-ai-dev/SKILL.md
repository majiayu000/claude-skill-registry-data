---
name: database-migration
description: Plan and execute safe database schema migrations with zero downtime. Apply expand/contract pattern, backward-compatible changes, and rollback strategies. Covers PostgreSQL, MySQL, and NoSQL schema evolution patterns grounded in Martin Fowler's evolutionary database design.
triggers:
  - "database migration"
  - "schema change"
  - "rename column"
  - "add column"
  - "migrate database"
  - "zero downtime migration"
  - "alter table"
audience:
  - engineer
---

# Database Migration

Evolve your database schema safely without downtime or data loss.

---

## The Expand/Contract Pattern (Fowler)

The safest approach for zero-downtime migrations. Never make a breaking schema change in a single deployment.

### Phase 1: Expand
- Add the new column/table/index alongside the old
- Both old and new schema coexist
- New code writes to both old and new; reads from old
- Deploy this version first

### Phase 2: Migrate
- Backfill existing rows to populate new column/table
- Run as a background job with batching — never one giant UPDATE
- Verify data integrity before proceeding

### Phase 3: Switch
- Update application to read from new column/table
- Keep writing to both during transition window
- Deploy and monitor

### Phase 4: Contract
- Remove writes to old column/table
- Deploy
- After a safe stabilization window, drop the old column/table

```
Old column present:  ████████████████████░░░░░░░░░░░░░░░░░░░░
New column present:  ░░░░░████████████████████████████████████
App reads new:       ░░░░░░░░░░░████████████████████████████████
Old column dropped:  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████
                     Deploy 1  Deploy 2  Deploy 3        Deploy 4
```

---

## Migration Safety Checklist

Before writing any migration:

### Risk Assessment
- [ ] How many rows affected? (< 1M = low risk, > 10M = high risk)
- [ ] Is this table actively written during migration? (hot table = higher risk)
- [ ] Will this lock the table? (ALTER TABLE on MySQL < 8 = full table lock)
- [ ] Is there a rollback plan?
- [ ] Is there a tested rollback migration?

### Backward Compatibility
- [ ] Old code can still run against new schema (expand phase must be compatible)
- [ ] New code can still run against old schema (rollback scenario)
- [ ] No NOT NULL columns added without defaults on existing tables
- [ ] No columns renamed in a single step (add + copy + drop separately)

---

## Safe Migration Patterns

### Adding a Column
```sql
-- Safe: backward compatible, nullable or with default
ALTER TABLE orders ADD COLUMN shipped_at TIMESTAMP NULL;
-- Then backfill:
UPDATE orders SET shipped_at = updated_at WHERE status = 'shipped';
```

### Renaming a Column (3-step)
```sql
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN email_address VARCHAR(255);

-- Step 2: Copy data + write to both in app code
UPDATE users SET email_address = email;

-- Step 3: (after stabilization) Drop old column
ALTER TABLE users DROP COLUMN email;
```

### Adding a NOT NULL Column
```sql
-- NEVER: ALTER TABLE foo ADD COLUMN bar NOT NULL; (breaks existing rows)

-- Safe: Add nullable, backfill, then add constraint
ALTER TABLE foo ADD COLUMN bar VARCHAR(100) NULL;
UPDATE foo SET bar = 'default_value' WHERE bar IS NULL;
ALTER TABLE foo ALTER COLUMN bar SET NOT NULL;
```

### Large Table Backfill
```sql
-- Never: UPDATE large_table SET new_col = compute(old_col);
-- Safe: Batch with a loop

DO $$
DECLARE
  batch_size INT := 1000;
  last_id BIGINT := 0;
  max_id BIGINT;
BEGIN
  SELECT MAX(id) INTO max_id FROM large_table;
  WHILE last_id < max_id LOOP
    UPDATE large_table
    SET new_col = compute(old_col)
    WHERE id > last_id AND id <= last_id + batch_size
      AND new_col IS NULL;
    last_id := last_id + batch_size;
    PERFORM pg_sleep(0.1); -- rate limit
  END LOOP;
END $$;
```

### Adding an Index Without Locking (PostgreSQL)
```sql
-- Locks table:
CREATE INDEX idx_users_email ON users(email);

-- Non-blocking:
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

---

## Rollback Strategy

Every migration must have a tested rollback:

```markdown
## Migration: add-shipped-at-to-orders

**Forward**:
```sql
ALTER TABLE orders ADD COLUMN shipped_at TIMESTAMP NULL;
```

**Rollback**:
```sql
ALTER TABLE orders DROP COLUMN IF EXISTS shipped_at;
```

**Rollback safe?**: Yes — column drop is instant if no data dependencies
**Rollback window**: Any time before Phase 4 (contract)
**Data loss on rollback?**: No — column was nullable, backfill was additive
```

---

## Migration Tooling

| Tool | Stack | Notes |
|---|---|---|
| Flyway | Java / any | SQL-first, versioned, team-friendly |
| Liquibase | Java / any | XML/YAML/SQL, supports rollback |
| Alembic | Python | SQLAlchemy-based, autogenerate support |
| ActiveRecord Migrations | Ruby/Rails | Convention-driven |
| golang-migrate | Go | SQL files, multiple drivers |
| Prisma Migrate | Node.js | Schema-first, shadow database |

**Shared practices regardless of tool:**
- Migrations in version control alongside application code
- Each migration in its own file; never edit a committed migration
- Run migrations in CI before deploy; never apply manually in prod
- Store migration history in the database itself

---

## Database-Specific Gotchas

### PostgreSQL
- `ALTER TABLE ... ADD COLUMN` with a volatile default rewrites the whole table (< PG 11)
- `CREATE INDEX` without `CONCURRENTLY` locks the table
- Long transactions can block `ALTER TABLE` indefinitely

### MySQL / MariaDB
- `ALTER TABLE` in MySQL < 8 takes a full table lock on most operations
- Use `pt-online-schema-change` or `gh-ost` for large tables
- InnoDB online DDL has limitations; check MySQL docs per operation

### MongoDB / NoSQL
- No schema enforcement — document shape drift is the risk
- Use schema validation (`$jsonSchema`) on collections
- Version your documents: `{ "_schemaVersion": 2, ... }`
- Migrate lazily (read-time upgrade) or eagerly (background job) — decide explicitly

---

## Pre-Deploy Checklist

- [ ] Migration reviewed by another engineer
- [ ] Tested against a prod-sized dataset in staging
- [ ] Execution time estimated (row count × expected ms/row)
- [ ] Rollback tested in staging
- [ ] Feature flag gates the code change (deploy migration separately from code)
- [ ] Monitoring/alerts on DB latency and error rate during migration window
- [ ] On-call aware of migration timing

---

## References
- Martin Fowler: [Evolutionary Database Design](https://martinfowler.com/articles/evodb.html)
- Martin Fowler: [Expand/Contract](https://martinfowler.com/bliki/ParallelChange.html)
- Pramod Sadalage & Martin Fowler: *Refactoring Databases*
- [gh-ost: GitHub Online Schema Tool](https://github.com/github/gh-ost)
