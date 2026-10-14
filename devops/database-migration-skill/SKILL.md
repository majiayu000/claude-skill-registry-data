---
name: database-migration-skill
description: >-
  Database schema evolution with Prisma, Alembic, Django — workflows, rollback,
  zero-downtime, seed data, migration testing.
license: Apache-2.0
compatibility: opencode
category: DevOps
---

## What I do

I help you manage database schema changes safely and repeatably:

1. **Schema Evolution**: Design schemas that change safely over time
2. **Prisma Migrations**: TypeScript/Node.js migration workflow
3. **Alembic Migrations**: Python/SQLAlchemy migration workflow
4. **Django Migrations**: Django ORM migration workflow
5. **Rollback Strategies**: Safe rollback planning and execution
6. **Zero-Downtime Migrations**: Techniques for production-safe schema changes
7. **Seed Data**: Manage test and development seed data
8. **Migration Testing**: Verify migrations work correctly before production

## When to use me

Use this skill when:
- Creating or modifying database schema
- Setting up a migration system for a new project
- Writing reversible migrations
- Planning zero-downtime production migrations
- Managing seed data for development/testing
- Debugging failed migrations
- Setting up migration CI checks
- Converting between migration tools

## Related Skills

- **performance-optimization-skill**: Handles runtime query profiling and optimization. This skill handles schema lifecycle. Index optimization can overlap — this skill handles index creation in migrations, performance skill handles query analysis.
- **civiltekk-python-backend-skill**: FastAPI/Django/Flask project patterns that use these migration tools (`scaffold` and `patterns` routes).
- **docker-containerization-skill**: Database containers in compose configurations.

---

## Step 1: Migration Principles

### Rules for Safe Migrations

1. **Never modify an existing migration** that has been applied
2. **Always make migrations reversible** (with rare exceptions)
3. **Test migrations against production-like data** before deploying
4. **Use separate migrations** for additive and destructive changes
5. **Prefer additive changes** — add new columns/tables before removing old ones

### Migration Categories

| Type | Risk | Reversibility | Example |
|------|------|---------------|---------|
| Additive (create table, add column) | Low | Easy | Add `phone` column to `users` |
| Add constraint | Medium | Moderate | Add NOT NULL, foreign key |
| Add index | Low | Easy | Add index on `users.email` |
| Rename column/table | Medium | Hard | Rename `name` to `full_name` |
| Remove column/table | High | Hard (data loss) | Drop `legacy_field` |
| Change column type | High | Hard | Change `int` to `bigint` |
| Data migration | Medium | Moderate | Backfill new column from old data |

---

## Step 2: Prisma (TypeScript/Node.js)

### Setup

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  posts     Post[]
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

### Workflow

```bash
npx prisma migrate dev --name init          # Create and apply migration
npx prisma migrate dev --name add-phone     # New migration
npx prisma migrate deploy                   # Apply pending migrations (production)
npx prisma migrate status                   # Check migration state
npx prisma migrate reset                    # Reset database (development only)
npx prisma db push                          # Push schema without migration (prototyping)
```

### Custom Migration SQL

```sql
-- prisma/migrations/20240115_add_user_role/migration.sql
ALTER TABLE "User" ADD COLUMN "role" TEXT NOT NULL DEFAULT 'user';

UPDATE "User" SET "role" = 'admin' WHERE email IN ('admin@example.com');

CREATE INDEX "User_role_idx" ON "User"("role");
```

### Seed Data

```typescript
import { PrismaClient } from '@prisma/client'
const prisma = new PrismaClient()

async function main() {
  await prisma.user.upsert({
    where: { email: 'admin@example.com' },
    update: {},
    create: { email: 'admin@example.com', name: 'Admin', role: 'admin' },
  })
}

main()
  .then(() => prisma.$disconnect())
  .catch((e) => { console.error(e); process.exit(1) })
```

---

## Step 3: Alembic (Python/SQLAlchemy)

### Setup

```bash
pip install alembic
alembic init alembic
```

### Configuration

```python
from alembic.config import Config
from sqlalchemy import create_engine
import os

config = Config("alembic.ini")
config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])
```

### Create Migration

```bash
alembic revision --autogenerate -m "add user phone column"
alembic upgrade head
alembic downgrade -1
alembic history --verbose
alembic current
```

### Manual Migration

```python
def upgrade() -> None:
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))
    op.create_index('ix_users_phone', 'users', ['phone'])

def downgrade() -> None:
    op.drop_index('ix_users_phone', table_name='users')
    op.drop_column('users', 'phone')
```

### Safe Column Type Change (Two-Phase)

```python
def upgrade() -> None:
    op.add_column('orders', sa.Column('amount_new', sa.BigInteger(), nullable=True))

    op.execute("""
        UPDATE orders SET amount_new = amount::bigint
    """)

    op.alter_column('orders', 'amount_new', nullable=False)
    op.drop_column('orders', 'amount')
    op.alter_column('orders', 'amount_new', new_column_name='amount')
```

---

## Step 4: Django Migrations

### Workflow

```bash
python manage.py makemigrations              # Detect model changes
python manage.py migrate                     # Apply all pending migrations
python manage.py migrate app_name 0003       # Migrate to specific version
python manage.py migrate app_name zero       # Rollback all migrations for app
python manage.py showmigrations              # Show migration status
python manage.py sqlmigrate app_name 0003    # Show SQL for migration
```

### Empty Migration (for data migrations)

```bash
python manage.py makemigrations --empty users --name populate_roles
```

```python
from django.db import migrations

def populate_roles(apps, schema_editor):
    User = apps.get_model('users', 'User')
    for user in User.objects.filter(is_superuser=True):
        user.role = 'admin'
        user.save(update_fields=['role'])

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0004_add_role_field'),
    ]

    operations = [
        migrations.RunPython(populate_roles, migrations.RunPython.noop),
    ]
```

---

## Step 5: Zero-Downtime Migration Strategy

### Two-Phase Migration Pattern

**Phase 1: Add new structure (non-breaking)**

```sql
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);
CREATE INDEX CONCURRENTLY users_full_name_idx ON users(full_name);
```

- Application reads old column, writes to both
- Deploy application code that populates `full_name` from `name`

**Phase 2: Remove old structure (after full rollout)**

```sql
-- Only after ALL instances are reading from full_name
ALTER TABLE users DROP COLUMN name;
```

### Checklist for Production Migrations

- [ ] Migration tested against production-like data volume
- [ ] Rollback migration prepared and tested
- [ ] Data backup verified
- [ ] Index creation uses `CONCURRENTLY` (PostgreSQL) or equivalent
- [ ] Long-running migrations run during low-traffic period
- [ ] Application code deployed that handles both old and new schema
- [ ] Migration run in a transaction where possible (DDL permitting)

### PostgreSQL-Specific

```sql
CREATE INDEX CONCURRENTLY users_email_idx ON users(email);
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
ALTER TABLE users ADD CONSTRAINT users_phone_check CHECK (phone ~ '^\+?[0-9]{10,15}$');
```

---

## Step 6: Migration Testing

### CI Integration

```yaml
name: Migration Check
on: [push]
jobs:
  migrate:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - name: Test migrations
        run: |
          alembic upgrade head
          alembic downgrade base
          alembic upgrade head
```

### Test Checklist

| Test | Purpose |
|------|---------|
| Forward migration | Verify migration applies cleanly |
| Rollback migration | Verify downgrade works |
| Forward-rollback-forward | Verify idempotency |
| With seed data | Verify data integrity |
| With production-like volume | Verify performance |
| Concurrent access | Verify no deadlocks |

---

## Step 7: Migration Pitfalls

### `bulk_insert` JSONB with asyncpg

**Learning**: `migration-jsonb-dicts`

When using Alembic `bulk_insert` with asyncpg, JSONB columns require Python dicts — not JSON strings. asyncpg does not auto-serialize `json.dumps()` output; it expects native Python types.

```python
import json

# WRONG — JSON string passed to asyncpg JSONB column
op.bulk_insert(
    sa.table("nodes"),
    [{"id": "n1", "config": json.dumps({"key": "val"})}],
)
# asyncpg error: expected dict, got str

# CORRECT — native Python dict
op.bulk_insert(
    sa.table("nodes"),
    [{"id": "n1", "config": {"key": "val"}}],
)
```

> **Cross-reference**: This pitfall is also documented in **civiltekk-python-backend-skill** (`scaffold` route).
