---
name: database-prisma
description: >
  Prisma ORM and PostgreSQL database management for EFT-Tracker.
  Handles schema design, migrations, client generation, and Neon database branches.
  Activates when user mentions: database, schema, migration, Prisma, model,
  relation, PostgreSQL, Neon, db push, db pull.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Database & Prisma Skill

## Capabilities

- Schema design and modification
- Migration management (`db push` vs `migrate`)
- Prisma client generation
- Neon database branch management
- Relation design patterns
- Data modeling best practices

## Activation Triggers

- "Add a new field to the schema"
- "Create a database migration"
- "Update the Prisma model"
- "Add a relation between tables"
- "Sync schema to database"
- "Generate Prisma client"

## Quick Reference

### Schema Changes Workflow

```bash
# 1. Modify prisma/schema.prisma
# 2. Push to database (development)
npx prisma db push

# 3. Generate client (if not auto-generated)
npx prisma generate
```

### db push vs migrate

| Command | Use When |
| ------- | -------- |
| `db push` | Development, prototyping, schema iteration |
| `migrate dev` | Production-ready migrations with history |
| `migrate deploy` | CI/CD production deployments |

**This project uses `db push`** for development simplicity with Neon branches.

## Database Environments

Use separate databases for different workflows:

| Environment | Database | When to Use |
| ----------- | -------- | ----------- |
| Local dev | Personal dev database | Feature work |
| Development | `DATABASE_URL_DEVELOP` | Testing develop branch |
| Production | `DATABASE_URL` | Never use locally |

**Critical:** Never connect to production database from local development.

## Schema Design Patterns

### Required Fields

Always include these fields on new models:

```prisma
model Example {
  id        String   @id @default(cuid())
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  // ... other fields
}
```

### Relations

```prisma
// One-to-many
model User {
  id     String  @id @default(cuid())
  posts  Post[]
}

model Post {
  id       String @id @default(cuid())
  author   User   @relation(fields: [authorId], references: [id])
  authorId String
}

// Many-to-many (implicit)
model Post {
  tags Tag[]
}

model Tag {
  posts Post[]
}
```

### Indexes

Add indexes for frequently queried fields:

```prisma
model Quest {
  id       String @id
  traderId String

  @@index([traderId])
}
```

## Neon-Specific Patterns

### Connection Pooling

Neon uses connection pooling. Use the pooled connection string:

```
postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/db?sslmode=require
```

### Branch Management

Neon branches are used for isolated development:

- `main` branch = production data
- Feature branches = development/testing

## Validation Integration

Pre-push hooks validate Prisma:

```
✓ Prisma client generation works
```

If validation fails with Prisma errors:

```bash
# Regenerate client
pnpm --filter @eft-tracker/web run prisma:generate

# Re-run validation
npm run validate
```

## Checklists

### Before Schema Change

- [ ] Understand the data requirements
- [ ] Check for existing similar models/fields
- [ ] Consider backward compatibility
- [ ] Plan index requirements
- [ ] Review relation cardinality

### After Schema Change

- [ ] Run `npx prisma db push`
- [ ] Verify no data loss warnings
- [ ] Run `npx prisma generate`
- [ ] Update TypeScript types if needed
- [ ] Test affected API routes
- [ ] Update any affected tests

## Common Issues

### "Prisma client out of sync"

```bash
npx prisma generate
```

### "Database drift detected"

Schema differs from database. Options:

1. Push schema: `npx prisma db push`
2. Pull database: `npx prisma db pull` (overwrites schema)

### "Migration failed"

Check for:

- Data that violates new constraints
- Missing default values for required fields
- Relation integrity issues

## Model Selection

**Database schema changes require Sonnet** (not Haiku) due to:

- High risk of data loss
- Complex relation implications
- Need for careful constraint design
