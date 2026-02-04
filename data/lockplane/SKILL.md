---
name: lockplane
description: Use Lockplane for safe database schema management - define schemas in .lp.sql files, validate, and apply with shadow DB testing
---

# Lockplane Expert

Help users manage database schemas safely using Lockplane.

## What is Lockplane?

Lockplane tests migrations on a shadow database before applying to production, validates SQL for dangerous patterns, and works with PostgreSQL, SQLite, and Turso.

## Core Workflow

1. **Create schema** - Write `.lp.sql` files with CREATE TABLE statements
2. **Validate** - `lockplane plan --validate schema/`
3. **Apply** - `lockplane apply --auto-approve --target-environment local --schema schema/`

## Commands

### Validate schema
```bash
lockplane plan --validate schema/users.lp.sql
lockplane plan --validate schema/  # validate entire directory
```

### Apply changes
```bash
# Environments are defined in lockplane.toml and .env.<name>
lockplane apply --auto-approve --target-environment local --schema schema/
```

## Configuration

Define environments in lockplane.toml and keep credentials in `.env.<name>` files:

```toml
default_environment = "local"

[environments.local]
description = "Local development"
```

```bash
# .env.local - PostgreSQL
POSTGRES_URL=postgresql://user:password@localhost:5432/myapp?sslmode=disable
POSTGRES_SHADOW_URL=postgresql://user:password@localhost:5433/myapp_shadow?sslmode=disable

# Or for SQLite:
# SQLITE_DB_PATH=./schema/myapp.db
# SQLITE_SHADOW_DB_PATH=./schema/myapp_shadow.db

# Or for Turso/libSQL:
# LIBSQL_URL=libsql://mydb-user.turso.io
# LIBSQL_AUTH_TOKEN=eyJhbGc...
# LIBSQL_SHADOW_DB_PATH=./schema/turso_shadow.db
```

**Supported databases:** PostgreSQL, SQLite, Turso/libSQL

Override with CLI flags (`--target`, `--shadow-db`) when needed.

Tip: `npx lockplane init` is the easiest way to set this up—it now pauses on a shadow DB preview screen (per database type), lets you customize the shadow port/path if needed, and shows a summary of primary + shadow connections before writing any files.

## Schema Format

Standard PostgreSQL DDL in `.lp.sql` files:

```sql
-- schema/users.lp.sql
CREATE TABLE users (
  id BIGINT PRIMARY KEY,
  email TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE UNIQUE INDEX users_email_idx ON users(email);
```

**Requirements:**
- Standard SQL DDL only (CREATE TABLE, CREATE INDEX, ALTER TABLE)
- No destructive operations (DROP TABLE, DROP COLUMN, TRUNCATE)
- No IF NOT EXISTS or CREATE OR REPLACE
- No transaction control (BEGIN/COMMIT/ROLLBACK)

## Safety Validations

**Data loss operations (ERROR):**
- DROP TABLE, DROP COLUMN, TRUNCATE TABLE

**Non-declarative patterns (ERROR):**
- IF NOT EXISTS clauses
- Transaction control (BEGIN, COMMIT, ROLLBACK)
- CREATE OR REPLACE

**Blocking operations (WARNING):**
- CREATE INDEX without CONCURRENTLY

## Example Interaction

**User: "I need to add an email column to my users table"**

Response:
```
I'll help you add an email column. Update your schema file:

```sql
-- schema/users.lp.sql
CREATE TABLE users (
  id BIGINT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT,  -- Add this
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

Then validate and apply:
```bash
lockplane plan --validate schema/users.lp.sql
lockplane apply --auto-approve --target-environment local --schema schema/
```

Note: I made email nullable because adding a NOT NULL column to an existing table with data would fail. To make it NOT NULL:
1. Add as nullable first
2. Backfill data in your application
3. Add NOT NULL constraint in a second migration
```

## Best Practices

1. Always validate before applying
2. Use shadow DB validation (lockplane apply does this by default)
3. Keep schema files in version control
4. Use CREATE INDEX CONCURRENTLY for production databases
5. Test locally before production
