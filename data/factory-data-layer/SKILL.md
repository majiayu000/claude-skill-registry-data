---
name: factory-data-layer
description: Database schema, ORM, and migration conventions across builds. Drizzle as default with domain-partitioned schema modules, shared `timestamps` helper, multi-tenancy keys with cascade delete, `pgTableCreator` prefixing, JSONB for flexible attributes, schema-derived type exports, polymorphic table patterns, ESLint Drizzle rules. Covers when to escape to raw SQL or Supabase auto-types.
---

# Factory data layer

Each section leads with **Principle** (one sentence, stack-agnostic), then **Why** (constraint → option → tradeoff), then **Recipe** (the Drizzle / Postgres shape we use), and **Failure mode** when there's one to name. Sections that are pure style with no deeper truth are marked `Recipe only`.

## ORM pick — match the data shape, not the comfort

**Principle.** Use the ORM whose abstractions match your schema's shape; don't escape to raw SQL by default.

**Why.** Raw SQL with hand-mapped row-to-object code is verbose, error-prone, and gives the type system nothing to check. An ORM with `$inferSelect`-style derivation means the schema *is* the type — one source of truth, one place to refactor. The cost of an ORM is one query DSL to learn; the cost of raw SQL is every hand-written mapper and every silent type drift.

**Recipe.**

| ORM | Pick when |
|---|---|
| **Drizzle** | Default. Postgres + TypeScript. Type-safe queries. Pairs with Better Auth's `drizzleAdapter`. |
| **Supabase auto-generated types** | Project commits to Supabase Auth + RLS heavily. RLS does real work. |
| **SQLAlchemy (Python)** | Python service with relational data. Use with soft-delete mixin. |
| **Raw `pg`** | Never for new projects. Migrate if encountered. |

**Failure mode.** Encode/monorepo used raw `pg` with hand-mapped row-to-object code. Every new query meant another mapper, and the types drifted from the schema on every migration.

## Domain-partitioned schema modules

**Principle.** Partition schema files by domain; one mega-schema file ages worse than one file per domain.

**Why.** A 2,000-line `schema.ts` is unreadable, ungreppable, and a merge-conflict factory. Domain partitioning means a feature change touches one file, a domain audit reads one file, and the import paths name the domain. The cost is one extra directory and one re-export index; the benefit is linear in the schema's growth.

**Recipe.**

```
src/server/db/schemas/
├── _shared.ts           # timestamps helper, pgTableCreator
├── auth.ts              # users, sessions, accounts, verifications
├── <domain>.ts          # e.g. fleet.ts, payments.ts, analytics.ts
├── reference.ts         # lookup tables (countries, states)
└── index.ts             # re-exports all
```

## `_shared.ts` — table creator + timestamps

**Principle.** Reusable schema primitives live in `_shared.ts`; never copy-paste `createdAt`/`updatedAt` into every table.

**Why.** Timestamps and the table-name prefix are universal — every table needs them, and they need to agree. Defining them once in `_shared.ts` means a change to "when does `updatedAt` fire?" is one diff, not 40. The `pgTableCreator` prefix lets the schema coexist with other apps in the same database (a small thing until you're sharing a Neon project across two services).

**Recipe.**

```ts
import { pgTableCreator, timestamp } from 'drizzle-orm/pg-core';

// Prefix tables so the schema can share a DB with other apps
export const pgTable = pgTableCreator((name) => `myapp_${name}`);

// Reusable timestamps spread into every table definition
export const timestamps = {
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull().$onUpdate(() => new Date()),
};
```

Use in domain files:

```ts
export const customers = pgTable('customers', {
  id: uuid('id').defaultRandom().primaryKey(),
  orgId: uuid('org_id').references(() => organizations.id, { onDelete: 'cascade' }).notNull(),
  name: text('name').notNull(),
  ...timestamps,
});
```

## Multi-tenancy keys — cascade delete on every domain table

**Principle.** Every domain table has the tenant FK (`orgId` / `workspaceId` / `projectId`) with `onDelete: 'cascade'`.

**Why.** Org deletion is a real operation — customers churn, free trials expire, GDPR right-to-delete requests arrive. Without cascade, deleting an org leaves orphan rows scattered across every domain table, and the cleanup script becomes its own bug surface. Cascade makes the schema the cleanup engine: one delete at the parent, the children disappear by the constraint, no application code involved.

**Recipe.** Every domain table has `orgId` FK with `onDelete: 'cascade'`. The org middleware (see `factory-auth.md`) injects `orgId` into the request context; every query filters by it.

## Custom attributes as JSONB — only when the field doesn't drive queries

**Principle.** What drives a query gets a real column. What doesn't can live in a JSONB envelope. Never query inside JSONB at app speed.

**Why.** JSONB is tempting because it sidesteps migration cost — add a field, ship. The trap is that "we only need to filter by this once in a while" reliably becomes "this is on the dashboard now." Querying inside JSONB is unindexed and slow; once a column is filterable, promote it. The rule is binary: if a field drives a query, it's a column.

**Recipe.**

```ts
customAttributes: jsonb('custom_attributes').$type<Record<string, unknown>>().default({}),
```

**Failure mode.** Putting time-series data in JSONB to "avoid the migration" and then querying inside it at dashboard load time — N seconds per page render, no index to fix it.

## Polymorphic tables — shared base + variant tables

**Principle.** When entities share most fields but diverge on a few, split into a shared base table plus variant tables; don't accumulate nullable columns.

**Why.** A single table with all-fields-nullable lets the schema represent impossible states (an ICE vehicle with a battery kWh, a BEV with MPG). The base + variants pattern makes those states unrepresentable: each variant table only carries its own fields, and the shared identity lives in the base. Cost: one extra join when you need variant-specific fields. Benefit: the type system enforces what the domain enforces.

**Recipe.**

```ts
export const vehicleTypes = pgTable('vehicle_types', {
  id: uuid('id').defaultRandom().primaryKey(),
  make: text('make').notNull(),
  model: text('model').notNull(),
  // shared fields
});

export const iceVehicles = pgTable('ice_vehicles', {
  id: uuid('id').defaultRandom().primaryKey(),
  vehicleTypeId: uuid('vehicle_type_id').references(() => vehicleTypes.id).notNull(),
  // ICE-specific fields (fuel type, MPG, etc.)
});

export const bevVehicles = pgTable('bev_vehicles', {
  id: uuid('id').defaultRandom().primaryKey(),
  vehicleTypeId: uuid('vehicle_type_id').references(() => vehicleTypes.id).notNull(),
  replacingIceVehicleId: uuid('replacing_ice_vehicle_id').references(() => iceVehicles.id),
  // BEV-specific fields (battery kWh, charger type, etc.)
});
```

## Schema-derived type exports

**Principle.** The schema is the source of truth for entity types; never declare entity interfaces by hand.

**Why.** Hand-declared interfaces drift from the schema on every migration — somebody adds a column, forgets the interface, and TypeScript happily accepts the now-incomplete row. Schema-derived types (`$inferSelect`, `InferSelectModel`) re-derive on every build, so the drift is impossible by construction.

**Recipe.**

```ts
// src/db/index.ts
export type CustomerTable = typeof customers.$inferSelect;
export type NewCustomer = typeof customers.$inferInsert;
```

Re-export from one entry point. `InferSelectModel<typeof customers>` is the same thing in different syntax — pick one and use it consistently.

## Soft-delete — query helper, not memorized convention

**Principle.** If you soft-delete, every read goes through a helper that filters by `deletedAt`. "Remember to add the filter" is a bug waiting to happen.

**Why.** Soft-delete works only if every read respects it. Hand-adding `where(isNull(deletedAt))` to every query means one missed filter ships deleted rows to the user. Wrapping reads in a helper makes the filter the default; opting out requires explicit code, which is the right direction for the asymmetry.

**Recipe.**

```py
class SoftDeleteMixin:
    deleted_at = Column(DateTime, nullable=True)

class Customer(Base, SoftDeleteMixin):
    __tablename__ = 'customers'
    # ...

# Queries always filter
stmt = select(Customer).where(Customer.deleted_at.is_(None))
```

For TypeScript / Drizzle: add `deletedAt: timestamp('deleted_at')` and wrap reads in a base query helper that applies `where(isNull(table.deletedAt))`.

## Migrations — CI, not runtime

**Principle.** Migrations run in CI against an ephemeral branch DB; never at application startup.

**Why.** Runtime migrations turn deployment into a database operation — a slow migration blocks the boot, a failed one leaves the app in a half-migrated state, and rolling back a deploy means rolling back the schema (which may have written rows already). CI migrations against an ephemeral DB make the schema change a separate gate; the deploy that follows is just code.

**Recipe.**

```sh
# Local dev — apply schema directly during prototyping
drizzle-kit push

# Pre-merge — generate migration files
drizzle-kit generate

# CI — apply migrations against the ephemeral Neon branch DB
drizzle-kit migrate
```

Never run migrations at app startup. Never run them inside a Cloud Run container's CMD.

## Migration file naming — pick one convention

**Principle.** Pick one migration file-naming convention and never mix.

**Why.** Schema evolution order is the most important property of migration files. Mixing timestamps with sequential numbers (`0000_create_simulations.ts` next to `add_vehicle_description.ts`) makes the order ambiguous — different tools sort them differently, and a developer reading the directory can't tell which came first. Pick one; stick.

**Recipe.** Either timestamps (`20260514_create_customers.sql`) or sequential numbers (`0001_create_customers.sql`). Don't mix.

**Failure mode.** Ford-analysis mixed conventions; the next migration created broke prod because the file order on disk didn't match the intended apply order.

## Boot-time assertion: preview ≠ prod DB

**Principle.** Configuration mistakes that could write preview data to the prod DB fail loud at boot.

**Why.** A misconfigured preview deployment that connects to the prod database is the silent kind of incident — preview writes look like real writes, no error fires, the data is contaminated days before anyone notices. A boot-time assertion that checks "preview env, prod DATABASE_URL → crash" makes the mistake instant and visible. The cost is three lines of code; the savings are the cost of the incident that didn't happen.

**Recipe.**

```ts
// src/db/index.ts
const isPreview = process.env.VERCEL_ENV === 'preview';
const isProduction = process.env.VERCEL_ENV === 'production';

if (isPreview && process.env.DATABASE_URL === process.env.PROD_DATABASE_URL) {
  throw new Error('Preview deployment must not use prod DB');
}
```

## ESLint Drizzle rules — enforce WHERE on mutations

**Principle.** Mutations without a WHERE clause are bugs; let the linter enforce.

**Why.** `db.update(customers).set({...})` without `where` updates every row — a five-second outage at best, a customer-facing incident at worst. The error is easy to make and hard to spot in review. The ESLint rule makes it impossible to commit.

**Recipe.**

```js
// eslint.config.js
{
  rules: {
    'drizzle/enforce-delete-with-where': 'error',
    'drizzle/enforce-update-with-where': 'error',
  },
}
```

## Activity log table — fire-and-forget

**Principle.** The audit log table never blocks the mutation that wrote to it.

**Why.** Audit logs are after-the-fact reconstruction artifacts. If the log insert fails, the mutation succeeded — that's the correct semantics. If the log insert blocks, every mutation is gated on the log table's availability. See `factory-api.md §audit logging at mutation boundary` for the same principle on the API side.

**Recipe.**

```ts
export const adminActions = pgTable('admin_actions', {
  id: uuid('id').defaultRandom().primaryKey(),
  actorId: uuid('actor_id').notNull(),
  action: text('action').notNull(),
  subjectType: text('subject_type'),
  subjectId: uuid('subject_id'),
  metadata: jsonb('metadata'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

export async function logAdminAction(input: NewAdminAction): Promise<void> {
  try {
    await db.insert(adminActions).values(input);
  } catch (err) {
    console.error('audit log failed', err);
  }
}
```

## Source patterns

Fleet-advisor (`_shared.ts`, `timestamps`, domain-partitioned schemas, `pgTableCreator`, cascade-delete, ESLint Drizzle rules, custom attributes JSONB), duezy (Drizzle relations with `InferSelectModel`, RDS IAM auth, lazy DB singleton via Proxy), ford-analysis (polymorphic vehicle tables, `$inferSelect` / `$inferInsert` exports, Vercel preview-DB safety check, time-series JSONB envelope), cothon (SoftDelete mixin with SQLAlchemy, async session management), kairos (admin_actions table, fire-and-forget audit log, Supabase auto-types).
