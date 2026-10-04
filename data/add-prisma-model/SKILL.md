---
name: add-prisma-model
description: Add a new Prisma model to schema.prisma, push it to PostgreSQL, regenerate the client, and document it in the vault. Use when the user asks to "add a table", "create a model", or "add X to the database".
---

# add-prisma-model

Add a new Prisma model. The schema is in `data/schema/prisma/schema.prisma`. Dev workflow uses `prisma db push` (no migration files) per ADR 005.

## Inputs to gather

- **Model name** (PascalCase singular or snake_case plural — match neighbors)
- **Fields** with types and nullability
- **Relations** (FK to which models?)
- **Indexes** needed for query patterns
- **Multi-tenant?** — if yes, **must** include `organizationId String` + index

## Steps

1. **Read** `data/schema/prisma/schema.prisma` to find the right place to add the model (group by domain — CRM, Pipeline, Pool, etc.).
2. **Add the model** following project conventions:
   - `id String @id @default(cuid())`
   - `createdAt DateTime @default(now())`
   - `updatedAt DateTime @updatedAt`
   - `deletedAt DateTime?` (soft delete pattern)
   - `organizationId String` + `@@index([organizationId])` if multi-tenant
   - Relations: `agent users @relation(...)` style with explicit `@relation` name
3. **Push** the schema:
   ```bash
   cd data/schema && npx prisma db push && npx prisma generate
   ```
   (Equivalent to running the `/db-push` skill.)
4. **Restart the API server** if it's running so the new client picks up the model.
5. **Update the vault**:
   - Append the model to `Aqarkom_Knowledge/Architecture/Database Schema.md` under the right domain block
   - If the model represents a new feature, add a Features/ note (run `/add-feature` or its sub-skill)
6. **Save a memory** if the model encodes a non-obvious decision (e.g., why a junction table over an array).

## Verification checklist

- [ ] `prisma db push` completes with no data loss warnings (or user explicitly accepts them)
- [ ] `prisma generate` completes
- [ ] New model appears in `node_modules/.prisma/client/index.d.ts`
- [ ] If multi-tenant: `organizationId` indexed + included in any new route's `where`
- [ ] Database Schema vault note updated

## Anti-patterns

- Don't run `prisma migrate dev` — this project uses `db push` for dev (per ADR 005)
- Don't add a multi-tenant model without `organizationId` — see [[Org Isolation]] in the vault
- Don't omit `deletedAt` if the table will hold user data — soft delete is the project default
- Don't use `enum` types in Prisma without checking the existing convention (some are strings constrained at the zod layer instead)
