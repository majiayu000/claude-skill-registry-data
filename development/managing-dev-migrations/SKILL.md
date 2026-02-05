---
name: managing-dev-migrations
description: Use migrate dev for versioned migrations; db push for rapid prototyping. Use when developing schema changes locally.
allowed-tools: Read, Write, Edit, Bash
---

## Decision Tree

**Use `prisma migrate dev` when:** Building production-ready features; working on teams with shared schema changes; needing migration history for rollbacks; version controlling schema changes; deploying to staging/production.

**Use `prisma db push` when:** Rapid prototyping and experimentation; early-stage development with frequent schema changes; personal projects without deployment concerns; testing schema ideas quickly; no migration history needed.

## migrate dev Workflow

```bash
npx prisma migrate dev --name add_user_profile
```

Detects schema changes in `schema.prisma`, generates SQL migration, applies to database, regenerates Prisma Client.

Review generated SQL before applying with `--create-only`:

```bash
npx prisma migrate dev --create-only --name add_indexes
```

Edit if needed, then apply:

```bash
npx prisma migrate dev
```

## db push Workflow

```bash
npx prisma db push
```

Syncs `schema.prisma` directly to database without creating migration files; regenerates Prisma Client with warnings on destructive changes. Use for throwaway prototypes or when recreating migrations later.

## Editing Generated Migrations

**When to edit:** Add custom indexes; include

data migrations; optimize generated SQL; add database-specific features.

**Example:** After `--create-only`:

```sql
CREATE TABLE "User" (
    "id" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "name" TEXT,
    "role" TEXT NOT NULL DEFAULT 'user',
    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

UPDATE "User" SET "role" = 'admin' WHERE "email" = 'admin@example.com';

CREATE UNIQUE INDEX "User_email_key" ON "User"("email");
```

Apply:

```bash
npx prisma migrate dev
```

## Workflow Examples

| Scenario            | Commands                                                                                                                                                      |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Feature Development | `npx prisma migrate dev --name add_comments`; `npx prisma migrate dev --name add_comment_likes`; `npx prisma migrate dev --name add_comment_moderation`       |
| Prototyping         | `npx prisma db push` (repeat); once stable: `npx prisma migrate dev --name initial_schema`                                                                    |
| Review & Customize  | `npx prisma migrate dev --create-only --name optimize_queries`; edit `prisma/migrations/[timestamp]_optimize_queries/migration.sql`; `npx prisma migrate dev` |

## Switching Between Workflows

**From `db push` to `migrate dev`:** Prisma detects current state and creates baseline migration:

```bash
npx prisma migrate dev --name initial_schema
```

**Handling conflicts** (unapplied migrations + `db push` usage):

```bash
npx prisma migrate reset
npx prisma migrate dev
```

## Common Patterns

| Pattern            | Command                                                                                            |
| ------------------ | -------------------------------------------------------------------------------------------------- |
| Daily Development  | `npx prisma migrate dev --name descriptive_name` (one per logical change)                          |
| Experimentation    | `npx prisma db push` (until design stable)                                                         |
| Pre-commit Review  | `npx prisma migrate dev --create-only --name feature_name` (review SQL, commit schema + migration) |
| Team Collaboration | `git pull`; `npx prisma migrate dev` (apply teammate migrations)                                   |

## Troubleshooting

**Migration Already Applied:** Normal when no schema changes exist. Run `npx prisma migrate dev`.

**Drift Detected:** Shows differences between database and migration history:

```bash
npx prisma migrate diff --from-migrations ./prisma/migrations --to-schema

-datamodel ./prisma/schema.prisma
```

Resolve by resetting or creating new migration.

**Data Loss Warnings:** Both commands warn before destructive changes. Review carefully before proceeding; migrate data or adjust schema to cancel.
