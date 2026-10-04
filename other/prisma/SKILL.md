---
name: prisma
description: "Model data with Prisma, manage migrations and transactions, and review relation queries for N+1 behavior."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["prisma", "orm", "typescript", "migrations", "postgres", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Prisma ORM AI Skill Guide

## Overview & Engine Architecture

Prisma maps a declarative `schema.prisma` to a generated TypeScript client. Migrations evolve the database; the client provides type-safe queries. Agents treat schema as source of truth, never edit prod schema by hand, use transactions for multi-step writes, and select only needed fields/relations to control payload size and N+1 risk.

```
schema.prisma -> migrate -> database
       \
        -> prisma generate -> @prisma/client
                              |
                         app query layer
```

## When to use this skill

- Modeling data and relations in Prisma
- Creating and applying migrations safely
- Writing typed queries and transactions
- Debugging client validation vs DB constraint errors

## Operational directives

1. Change schema -> `migrate dev` (local) / `migrate deploy` (CI/prod) - do not drift.
2. Use `include` / `select` intentionally; default wide includes hide cost.
3. Wrap multi-model writes in `$transaction`.
4. Keep a single PrismaClient instance (avoid new client per request in serverless without care).
5. Never commit `.env` with production `DATABASE_URL`.

## Schema + query sketch

```prisma
model Item {
  id        String   @id @default(cuid())
  sku       String   @unique
  qty       Int      @default(0)
  createdAt DateTime @default(now())
  ownerId   String
  owner     User     @relation(fields: [ownerId], references: [id])
}

model User {
  id    String @id @default(cuid())
  email String @unique
  items Item[]
}
```

```ts
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export async function createItem(ownerId: string, sku: string, qty: number) {
  return prisma.item.create({
    data: { ownerId, sku, qty },
    select: { id: true, sku: true, qty: true },
  });
}

export async function listOwnerItems(ownerId: string) {
  return prisma.item.findMany({
    where: { ownerId },
    orderBy: { createdAt: "desc" },
    take: 50,
  });
}
```

## Commands

```bash
npx prisma init
npx prisma migrate dev --name add_items
npx prisma generate
npx prisma studio
npx prisma migrate deploy
```

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| Editing DB without migration | Environment drift | Migrate always |
| Nested writes without tx | Partial commits | `$transaction` |
| Fetching entire graphs | Memory/latency | `select` / paginate |
| Multiple clients in serverless | Exhausted connections | Singleton + pooler |

## Best practices

- Use connection pooling (PgBouncer / Prisma Accelerate) for serverless.
- Add DB-level constraints that match schema uniqueness/FKs.
- Prefer `migrate diff` in CI to detect schema drift.
- Seed deterministic fixtures for tests; reset carefully.

## Limitations

- Raw SQL is still needed for complex reports and some locks.
- Multi-schema and exotic DB features vary by provider support.
- Prisma Accelerate / Pulse features are optional paid platform pieces.

## Related skills

- `@nodejs` / `@typescript` - runtime hosting the client
- `@supabase` / `@supabase-rls` - Postgres + RLS alongside Prisma
- `@graphql-apis` - Prisma under GraphQL resolvers
