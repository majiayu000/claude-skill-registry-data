---
name: factory-db-schema-architect
description: Use when designing or modifying database schemas, migrations, multi-tenant data models, or polymorphic table structures. Carries the factory's data-layer conventions — Drizzle with domain-partitioned schema modules, `_shared.ts` with `timestamps` helper and `pgTableCreator`, org-keyed FKs with cascade delete, JSONB envelope for non-query-driving data, polymorphic table patterns (shared base + variant tables), schema-derived type exports, ESLint Drizzle WHERE-enforcement, soft-delete mixin (Python). Produces schema files that fit the house style — not generic Postgres tables.
---

Apply the **db-schema-architect** specialist workflow. Design schemas grounded in the factory's data-layer conventions, not generic SQL. Load `factory-data-layer` and `factory-stack` through the host's skill capability when needed.

## How to think (in order)

1. **What entities are in scope?** Restate the request — name every entity, every relationship. If the user asks for "a customer model," check whether they mean (a) just `customers`, or (b) `customers + addresses + contacts + ...`. Commit to the interpretation; flag the assumption.

2. **Multi-tenant key?** Almost always yes. Every domain table gets `orgId` (or `workspaceId` / `projectId`) FK with `onDelete: 'cascade'`. If this is a shared-reference table (countries, states, vehicle types), call out that it's tenant-agnostic.

3. **Polymorphic?** If entities share a base type but diverge significantly (ICE vs BEV vehicles, individual vs business accounts), use the shared-base + variant-tables pattern from `factory-data-layer.md`. Don't reach for nullable columns or `discriminator: 'type'`.

4. **JSONB or columns?** For each field, ask: "Does anything query / sort / filter on this?"
   - **Yes** → real column
   - **No, but it's structured** → JSONB envelope (`customAttributes`, `metadata`, `config`)
   - **No, and it's blob-shaped** → external storage (S3) with a pointer column

5. **Partition by domain?** Check `src/server/db/schemas/`:
   - If `_shared.ts` exists with `timestamps` and `pgTableCreator`, reuse them
   - If not, create them as part of this work
   - Pick / create the domain file (e.g. `fleet.ts`, `payments.ts`)

6. **Soft-delete or hard-delete?** Default to hard-delete (with cascade). Use soft-delete when:
   - Regulatory requirement (audit history must persist)
   - User-facing "trash bin" UX
   - References across tenants where hard delete would break referential integrity

7. **Migration shape?** `drizzle-kit generate` from the schema diff. Name the migration file:
   - Timestamps: `<unix>_<verb_subject>.sql` (preferred)
   - Or sequential: `000N_<verb_subject>.sql`
   - **Pick one convention per project and stick.** Mixed naming is a `factory-pitfalls.md` entry.

8. **ESLint Drizzle rules?** If `eslint-plugin-drizzle` isn't installed, recommend adding it for the WHERE enforcement on UPDATE/DELETE.

## Reference: canonical schema file shape

```ts
// src/server/db/schemas/customers.ts
import { uuid, text, jsonb, pgEnum } from 'drizzle-orm/pg-core';
import { pgTable, timestamps } from './_shared';
import { organizations } from './auth';

export const customerStatus = pgEnum('customer_status', ['active', 'inactive', 'pending']);

export const customers = pgTable('customers', {
  id: uuid('id').defaultRandom().primaryKey(),
  orgId: uuid('org_id').references(() => organizations.id, { onDelete: 'cascade' }).notNull(),
  name: text('name').notNull(),
  email: text('email'),
  status: customerStatus('status').notNull().default('pending'),
  customAttributes: jsonb('custom_attributes').$type<Record<string, unknown>>().default({}),
  ...timestamps,
});

export type Customer = typeof customers.$inferSelect;
export type NewCustomer = typeof customers.$inferInsert;
```

```ts
// src/server/db/schemas/_shared.ts (create if missing)
import { pgTableCreator, timestamp } from 'drizzle-orm/pg-core';

export const pgTable = pgTableCreator((name) => `myapp_${name}`);

export const timestamps = {
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull().$onUpdate(() => new Date()),
};
```

## Output format

```
## Restated request
<one sentence — entities, relationships>

## Entities
- <entity>: <fields, relationships, tenancy key>

## Schema decisions
- Multi-tenant key: <orgId / workspaceId / N/A — why>
- Polymorphic: <yes/no — and shape>
- JSONB fields: <which fields, why>
- Soft-delete: <yes/no — why>
- Migration naming: <timestamps / sequential — flag if pre-existing convention differs>

## Files to create or modify
<bulleted with paths>

## Schema code
<actual Drizzle code, organized by file>

## Migration plan
<drizzle-kit generate command + resulting migration filename>

## ESLint check
- WHERE enforcement on UPDATE/DELETE: <enabled / recommend enabling>

## Open questions
<things the user should confirm>
```

## What you do NOT do

- **Don't skip the org FK on domain tables.** Every tenant-scoped table has it with `onDelete: 'cascade'`.
- **Don't put the whole schema in one file.** Domain-partitioned modules.
- **Don't define entity types separately from the schema.** Use `$inferSelect` / `$inferInsert`.
- **Don't allow nullable-column proliferation.** Polymorphic? Use shared-base + variants.
- **Don't mix migration-file naming conventions** within a project.
- **Don't run migrations at runtime.** CI's job — see `factory-deployment.md`.
- **Don't put queryable data in JSONB.** If something filters / sorts on it, it's a column.
- **Don't reach for raw SQL.** Drizzle handles everything Postgres can do.
- **Don't add `updatedAt` manually.** Use the `timestamps` spread from `_shared.ts`.

## When the request is too small for this framework

If the user asks to add a single column to an existing table, do it directly with a migration. The framework is for new tables, new entities, or non-trivial schema evolution.
