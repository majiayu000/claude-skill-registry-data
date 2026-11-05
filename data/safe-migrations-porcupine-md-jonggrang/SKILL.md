---
name: safe-migrations
description: Run database migrations safely in production. Zero-downtime strategies, rollback procedures, backward compatibility.
type: pattern
tier: library
domains: [database]
trigger: "migration, schema change, alter table, column, add index, rename, production database"
---

## The Golden Rule: Backward Compatible First

**Never break the running application.** Migrations must be compatible with the code running before AND after the migration.

## Safe Migration Patterns

### Adding a Column (Safe)

```sql
-- SAFE: new nullable column, app ignores it until code deploys
ALTER TABLE users ADD COLUMN display_name VARCHAR(255);

-- THEN: deploy code that reads/writes display_name
-- THEN: if needed, backfill values
UPDATE users SET display_name = username WHERE display_name IS NULL;
-- THEN: add NOT NULL constraint (separate migration)
ALTER TABLE users ALTER COLUMN display_name SET NOT NULL;
```

### Renaming a Column (Dangerous → Use This Instead)

```sql
-- STEP 1: add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);

-- STEP 2: copy data
UPDATE users SET full_name = first_name || ' ' || last_name;

-- STEP 3: deploy code that reads BOTH columns (backward compat)
-- STEP 4: verify new column has all data
-- STEP 5: drop old columns (in a later migration after old code is gone)
ALTER TABLE users DROP COLUMN first_name;
ALTER TABLE users DROP COLUMN last_name;
```

### Adding an Index (Use CONCURRENTLY)

```sql
-- WRONG: locks the table
CREATE INDEX idx_users_email ON users(email);

-- RIGHT: doesn't lock (PostgreSQL)
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

### Dropping a Column (Multi-Step)

```sql
-- STEP 1: deploy code that no longer reads/writes the column
-- STEP 2: mark column ignored (shadow drop)
ALTER TABLE users ALTER COLUMN old_col DROP NOT NULL;
-- STEP 3: wait for all app instances to deploy
-- STEP 4: drop the column
ALTER TABLE users DROP COLUMN old_col;
```

## Migration File Structure (Prisma example)

```
prisma/migrations/
  20240101000000_add_user_display_name/
    migration.sql
  20240102000000_backfill_display_name/
    migration.sql
```

## Rollback Strategy

```sql
-- Always write a down migration
-- migration_20240101_up.sql
ALTER TABLE users ADD COLUMN score INTEGER DEFAULT 0;

-- migration_20240101_down.sql
ALTER TABLE users DROP COLUMN score;
```

## Production Checklist

Before running migration in production:
- [ ] Tested on staging with production data volume
- [ ] Estimated execution time (slow on large tables?)
- [ ] Index additions use CONCURRENTLY
- [ ] NOT NULL columns have a DEFAULT value
- [ ] Down migration written and tested
- [ ] Deployment window scheduled (if table lock required)
- [ ] Database backup taken
- [ ] Monitoring in place to detect query slowdowns post-migration
