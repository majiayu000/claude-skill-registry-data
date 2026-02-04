---
name: grey-haven-database-conventions
description: "Apply Grey Haven database conventions - snake_case fields, multi-tenant with tenant_id and RLS, proper indexing, migrations for Drizzle (TypeScript) and SQLModel (Python). Use when designing schemas, writing database code, creating migrations, setting up RLS policies, or when user mentions 'database', 'schema', 'Drizzle', 'SQLModel', 'migration', 'RLS', 'tenant_id', 'snake_case', 'indexes', or 'foreign keys'."
# v2.0.43: Skills to auto-load for database work
skills:
  - grey-haven-code-style
  - grey-haven-data-validation
# v2.0.74: Tools for database schema work
allowed-tools:
  - Read
  - Write
  - MultiEdit
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# Grey Haven Database Conventions

**Database schema standards for Drizzle ORM (TypeScript) and SQLModel (Python).**

Follow these conventions for all Grey Haven multi-tenant database schemas.

## Supporting Documentation

- **[examples/](examples/)** - Complete schema examples (all files <500 lines)
  - [drizzle-schemas.md](examples/drizzle-schemas.md) - TypeScript/Drizzle examples
  - [sqlmodel-schemas.md](examples/sqlmodel-schemas.md) - Python/SQLModel examples
  - [migrations.md](examples/migrations.md) - Migration patterns
  - [rls-policies.md](examples/rls-policies.md) - Row Level Security
- **[reference/](reference/)** - Detailed references (all files <500 lines)
  - [field-naming.md](reference/field-naming.md) - Naming conventions
  - [indexing.md](reference/indexing.md) - Index patterns
  - [relationships.md](reference/relationships.md) - Foreign keys and relations
- **[templates/](templates/)** - Copy-paste schema templates
- **[checklists/](checklists/)** - Schema validation checklists

## Critical Rules

### 1. snake_case Fields (ALWAYS)

**Database columns MUST use snake_case, never camelCase.**

```typescript
// ✅ CORRECT
export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  created_at: timestamp("created_at").defaultNow().notNull(),
  tenant_id: uuid("tenant_id").notNull(),
  email_address: text("email_address").notNull(),
});

// ❌ WRONG - Don't use camelCase
export const users = pgTable("users", {
  createdAt: timestamp("createdAt"),  // WRONG!
  tenantId: uuid("tenantId"),        // WRONG!
});
```

### 2. tenant_id Required (Multi-Tenant)

**Every table MUST include tenant_id for data isolation.**

```typescript
// TypeScript - Drizzle
export const organizations = pgTable("organizations", {
  id: uuid("id").primaryKey().defaultRandom(),
  tenant_id: uuid("tenant_id").notNull(),  // REQUIRED
  name: text("name").notNull(),
});
```

```python
# Python - SQLModel
class Organization(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True)  # REQUIRED
    name: str = Field(max_length=255)
```

**See [examples/drizzle-schemas.md](examples/drizzle-schemas.md) and [examples/sqlmodel-schemas.md](examples/sqlmodel-schemas.md) for complete examples.**

### 3. Standard Timestamps

**All tables must have created_at and updated_at.**

```typescript
// TypeScript - Reusable timestamps
export const baseTimestamps = {
  created_at: timestamp("created_at").defaultNow().notNull(),
  updated_at: timestamp("updated_at").defaultNow().notNull().$onUpdate(() => new Date()),
};

export const teams = pgTable("teams", {
  id: uuid("id").primaryKey().defaultRandom(),
  ...baseTimestamps,  // Spread operator
  tenant_id: uuid("tenant_id").notNull(),
  name: text("name").notNull(),
});
```

```python
# Python - Mixin pattern
class TimestampMixin:
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

class Team(TimestampMixin, SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(index=True)
    name: str = Field(max_length=255)
```

### 4. Row Level Security (RLS)

**Enable RLS on all tables with tenant_id.**

```sql
-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Tenant isolation policy
CREATE POLICY "tenant_isolation" ON users
  FOR ALL TO authenticated
  USING (tenant_id = (current_setting('request.jwt.claims')::json->>'tenant_id')::uuid);
```

**See [examples/rls-policies.md](examples/rls-policies.md) for complete RLS patterns.**

## Quick Reference

### Field Naming Patterns

**Boolean fields:** Prefix with `is_`, `has_`, `can_`
```typescript
is_active: boolean("is_active")
has_access: boolean("has_access")
can_edit: boolean("can_edit")
```

**Timestamp fields:** Suffix with `_at`
```typescript
created_at: timestamp("created_at")
updated_at: timestamp("updated_at")
deleted_at: timestamp("deleted_at")
last_login_at: timestamp("last_login_at")
```

**Foreign keys:** Suffix with `_id`
```typescript
tenant_id: uuid("tenant_id")
user_id: uuid("user_id")
organization_id: uuid("organization_id")
```

**See [reference/field-naming.md](reference/field-naming.md) for complete naming guide.**

### Indexing Patterns

**Always index:**
- `tenant_id` (for multi-tenant queries)
- Foreign keys (for joins)
- Unique constraints (email, slug)
- Frequently queried fields

```typescript
// Composite index for tenant + lookup
export const usersIndex = index("users_tenant_email_idx").on(
  users.tenant_id,
  users.email_address
);
```

**See [reference/indexing.md](reference/indexing.md) for index strategies.**

### Relationships

**One-to-many:**
```typescript
export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),  // User has many posts
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, { fields: [posts.user_id], references: [users.id] }),
}));
```

**See [reference/relationships.md](reference/relationships.md) for all relationship patterns.**

## Drizzle ORM (TypeScript)

**Installation:**
```bash
bun add drizzle-orm postgres
bun add -d drizzle-kit
```

**Basic schema:**
```typescript
// db/schema.ts
import { pgTable, uuid, text, timestamp, boolean } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  created_at: timestamp("created_at").defaultNow().notNull(),
  updated_at: timestamp("updated_at").defaultNow().notNull(),
  tenant_id: uuid("tenant_id").notNull(),
  email_address: text("email_address").notNull().unique(),
  is_active: boolean("is_active").default(true).notNull(),
});
```

**Generate migration:**
```bash
bun run drizzle-kit generate:pg
bun run drizzle-kit push:pg
```

**See [examples/migrations.md](examples/migrations.md) for migration workflow.**

## SQLModel (Python)

**Installation:**
```bash
pip install sqlmodel psycopg2-binary
```

**Basic model:**
```python
# app/models/user.py
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True)
    email_address: str = Field(unique=True, index=True, max_length=255)
    is_active: bool = Field(default=True)
```

**Generate migration:**
```bash
alembic revision --autogenerate -m "Add users table"
alembic upgrade head
```

**See [examples/migrations.md](examples/migrations.md) for Alembic setup.**

## When to Apply This Skill

Use this skill when:
- ✅ Designing new database schemas
- ✅ Creating Drizzle or SQLModel models
- ✅ Writing database migrations
- ✅ Setting up RLS policies
- ✅ Adding indexes for performance
- ✅ Defining table relationships
- ✅ Reviewing database code in PRs
- ✅ User mentions: "database", "schema", "Drizzle", "SQLModel", "migration", "RLS", "tenant_id", "snake_case"

## Template References

- **TypeScript**: `cvi-template` (Drizzle ORM + PlanetScale)
- **Python**: `cvi-backend-template` (SQLModel + PostgreSQL)

## Critical Reminders

1. **snake_case** - ALL database fields use snake_case (never camelCase)
2. **tenant_id** - Required on all tables for multi-tenant isolation
3. **Timestamps** - created_at and updated_at on all tables
4. **RLS policies** - Enable on all tables with tenant_id
5. **Indexing** - Index tenant_id, foreign keys, and unique fields
6. **Migrations** - Always use migrations (Drizzle Kit or Alembic)
7. **Field naming** - Booleans use is_/has_/can_ prefix, timestamps use _at suffix
8. **No raw SQL** - Use ORM for queries (prevents SQL injection)
9. **Soft deletes** - Use deleted_at timestamp, not hard deletes
10. **Foreign keys** - Always define relationships explicitly

## Next Steps

- **Need examples?** See [examples/](examples/) for Drizzle and SQLModel schemas
- **Need references?** See [reference/](reference/) for naming, indexing, relationships
- **Need templates?** See [templates/](templates/) for copy-paste schema starters
- **Need checklists?** Use [checklists/](checklists/) for schema validation
