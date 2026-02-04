---
name: grey-haven-data-modeling
description: Design database schemas for Grey Haven multi-tenant SaaS - SQLModel models, Drizzle schema, multi-tenant isolation with tenant_id and RLS, timestamp fields, foreign keys, indexes, migrations, and relationships. Use when creating database tables.
# v2.0.43: Skills to auto-load for data modeling
skills:
  - grey-haven-code-style
  - grey-haven-database-conventions
# v2.0.74: Tools for data modeling
allowed-tools:
  - Read
  - Write
  - MultiEdit
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# Grey Haven Data Modeling Standards

Design **database schemas** for Grey Haven Studio's multi-tenant SaaS applications using SQLModel (FastAPI) and Drizzle ORM (TanStack Start) with PostgreSQL and RLS.

## Multi-Tenant Principles

### CRITICAL: Every Table Requires tenant_id

```typescript
// ✅ CORRECT - Drizzle
export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  tenant_id: uuid("tenant_id").notNull(), // REQUIRED!
  created_at: timestamp("created_at").defaultNow().notNull(),
  updated_at: timestamp("updated_at").defaultNow().notNull(),
  // ... other fields
});
```

```python
# ✅ CORRECT - SQLModel
class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True) # REQUIRED!
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    # ... other fields
```

### Naming Conventions

**ALWAYS use snake_case** (never camelCase):

```typescript
// ✅ CORRECT
email_address: text("email_address")
created_at: timestamp("created_at")
is_active: boolean("is_active")
tenant_id: uuid("tenant_id")

// ❌ WRONG
emailAddress: text("emailAddress")  // WRONG!
createdAt: timestamp("createdAt")   // WRONG!
```

### Standard Fields (Required on All Tables)

```typescript
// Every table should have:
id: uuid("id").primaryKey().defaultRandom()
created_at: timestamp("created_at").defaultNow().notNull()
updated_at: timestamp("updated_at").defaultNow().notNull()
tenant_id: uuid("tenant_id").notNull()
deleted_at: timestamp("deleted_at") // For soft deletes (optional)
```

## Core Tables

### 1. Tenants Table (Root)

```typescript
// Drizzle
export const tenants = pgTable("tenants", {
  id: uuid("id").primaryKey().defaultRandom(),
  name: text("name").notNull(),
  slug: text("slug").notNull().unique(),
  is_active: boolean("is_active").default(true).notNull(),
  created_at: timestamp("created_at").defaultNow().notNull(),
  updated_at: timestamp("updated_at").defaultNow().notNull(),
});
```

```python
# SQLModel
class Tenant(SQLModel, table=True):
    __tablename__ = "tenants"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=255)
    slug: str = Field(max_length=100, unique=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 2. Users Table (With Tenant Isolation)

```typescript
// Drizzle
export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  tenant_id: uuid("tenant_id").notNull(),
  email_address: text("email_address").notNull().unique(),
  full_name: text("full_name").notNull(),
  is_active: boolean("is_active").default(true).notNull(),
  created_at: timestamp("created_at").defaultNow().notNull(),
  updated_at: timestamp("updated_at").defaultNow().notNull(),
  deleted_at: timestamp("deleted_at"),
});

// Index for tenant_id
export const usersTenantIndex = index("users_tenant_id_idx").on(users.tenant_id);
```

```python
# SQLModel
class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True)
    email_address: str = Field(max_length=255, unique=True)
    full_name: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None
```

## Relationships

### One-to-Many

```typescript
// Drizzle - User has many Posts
export const posts = pgTable("posts", {
  id: uuid("id").primaryKey().defaultRandom(),
  tenant_id: uuid("tenant_id").notNull(),
  user_id: uuid("user_id").notNull(),
  title: text("title").notNull(),
  // ... other fields
});

// Relations
export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  user: one(users, {
    fields: [posts.user_id],
    references: [users.id],
  }),
}));
```

### Many-to-Many

```typescript
// Drizzle - User has many Roles through UserRoles
export const user_roles = pgTable("user_roles", {
  id: uuid("id").primaryKey().defaultRandom(),
  tenant_id: uuid("tenant_id").notNull(),
  user_id: uuid("user_id").notNull(),
  role_id: uuid("role_id").notNull(),
  created_at: timestamp("created_at").defaultNow().notNull(),
});

// Indexes for join table
export const userRolesUserIndex = index("user_roles_user_id_idx").on(user_roles.user_id);
export const userRolesRoleIndex = index("user_roles_role_id_idx").on(user_roles.role_id);
```

## RLS Policies

### Enable RLS on All Tables

```sql
-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Tenant isolation policy
CREATE POLICY "tenant_isolation"
ON users
FOR ALL
USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- Admin override policy
CREATE POLICY "admin_override"
ON users
FOR ALL
TO admin_role
USING (true);
```

## Indexes

### Required Indexes

```typescript
// ALWAYS index tenant_id
export const usersTenantIndex = index("users_tenant_id_idx").on(users.tenant_id);

// Index foreign keys
export const postsUserIndex = index("posts_user_id_idx").on(posts.user_id);

// Composite indexes for common queries
export const postsCompositeIndex = index("posts_tenant_user_idx")
  .on(posts.tenant_id, posts.user_id);
```

## Migrations

### Drizzle Kit

```bash
# Generate migration
bun run db:generate

# Apply migration
bun run db:migrate

# Rollback migration (manual)
```

### Alembic (SQLModel)

```bash
# Generate migration
alembic revision --autogenerate -m "add users table"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Supporting Documentation

All supporting files are under 500 lines per Anthropic best practices:

- **[examples/](examples/)** - Complete schema examples
  - [drizzle-models.md](examples/drizzle-models.md) - Drizzle schema examples
  - [sqlmodel-models.md](examples/sqlmodel-models.md) - SQLModel examples
  - [relationships.md](examples/relationships.md) - Relationship patterns
  - [rls-policies.md](examples/rls-policies.md) - RLS policy examples
  - [INDEX.md](examples/INDEX.md) - Examples navigation

- **[reference/](reference/)** - Data modeling references
  - [naming-conventions.md](reference/naming-conventions.md) - Field naming rules
  - [indexes.md](reference/indexes.md) - Index strategies
  - [migrations.md](reference/migrations.md) - Migration patterns
  - [INDEX.md](reference/INDEX.md) - Reference navigation

- **[templates/](templates/)** - Copy-paste ready templates
  - [drizzle-table.ts](templates/drizzle-table.ts) - Drizzle table template
  - [sqlmodel-table.py](templates/sqlmodel-table.py) - SQLModel table template

- **[checklists/](checklists/)** - Schema checklists
  - [schema-checklist.md](checklists/schema-checklist.md) - Pre-PR schema validation

## When to Apply This Skill

Use this skill when:
- Creating new database tables
- Designing multi-tenant data models
- Adding relationships between tables
- Creating RLS policies
- Generating database migrations
- Refactoring existing schemas
- Implementing soft deletes
- Adding indexes for performance

## Template Reference

These patterns are from Grey Haven's production templates:
- **cvi-template**: Drizzle ORM + PostgreSQL + RLS
- **cvi-backend-template**: SQLModel + PostgreSQL + Alembic

## Critical Reminders

1. **tenant_id**: Required on EVERY table (no exceptions!)
2. **snake_case**: All fields use snake_case (NEVER camelCase)
3. **Timestamps**: created_at and updated_at on all tables
4. **Indexes**: Always index tenant_id and foreign keys
5. **RLS policies**: Enable RLS on all tables for tenant isolation
6. **Soft deletes**: Use deleted_at instead of hard deletes
7. **Foreign keys**: Explicitly define relationships
8. **Migrations**: Test both up and down migrations
9. **Email fields**: Name as email_address (not email)
10. **Boolean fields**: Use is_/has_/can_ prefix
