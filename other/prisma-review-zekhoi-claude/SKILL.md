---
name: prisma-review
description: Review TypeScript code that uses Prisma Client for correctness, safety, transactions, and performance, and report findings with severity and file locations. Use when asked to review database query code, repositories, services, or data-access changes in a project that uses Prisma. Do not use for projects without Prisma, for writing migrations or schema changes (use agent-kit:database-design), for Kysely or Drizzle code (use agent-kit:kysely-review or agent-kit:drizzle-review), or for general code review; this skill reports and does not edit code.
---

# Prisma review

Report findings without modifying code unless the user asks for fixes.

## 1. Understand the schema and conventions

- Read `schema.prisma`: models, relations, `@unique` and `@@unique`, `@@index`, optional fields, and `onDelete` behavior. Note the Prisma major version, where the client is generated (`@prisma/client`, or a custom `output` path with the `prisma-client` generator), and any client extensions, middleware, or driver adapters.
- Find how the client is created (one shared `PrismaClient`, not one per request), how transactions are written, and how errors such as `P2002` and `P2025` are handled.

## 2. Check each query

**Correctness**

- `updateMany` and `deleteMany` with an empty or missing `where` affect every row (or fail with `P2003` when a required relation restricts the delete). Flag them unless that is clearly intended.
- `findUnique` and `findFirst` return `null`; flag non-null assertions or unchecked access, and suggest an explicit check or `findUniqueOrThrow`/`findFirstOrThrow`. `update` and `delete` throw `P2025` when nothing matches; check callers catch it, or use `updateMany`/`deleteMany` and check `count`.
- `findFirst` and paginated `findMany` need a deterministic `orderBy`. Cursor pagination needs a unique cursor field. `upsert` needs a unique `where`; concurrent upserts can still raise `P2002`.

**Safety**

- `$queryRaw` and `$executeRaw` as tagged templates are parameterized. `$queryRawUnsafe`, `$executeRawUnsafe`, and `Prisma.raw()` with interpolated input are injection: require parameters or an allowlist for identifiers.
- Without `select` or `omit`, queries return every scalar field, including password hashes and tokens; flag results passed straight to API responses and suggest `select`, `omit`, or a global `omit` on the client. Check tenant or owner filters are present on every query that needs them, including nested writes.

**Transactions**

- Writes that must succeed together belong in `prisma.$transaction([...])` or an interactive `$transaction(async (tx) => ...)`. Inside an interactive transaction every query must use `tx`, not `prisma`, and be awaited.
- Avoid slow external calls inside interactive transactions; they hold a connection and can hit the transaction timeout.

**Performance**

- Queries in loops (N+1) should become one query with `where: { id: { in: ids } }`, `include`, or nested `select`. Deep `include` trees can fetch far more data than needed; prefer `select`.
- Use `createMany` for many rows, and check that filtered and sorted fields have an index in the schema.

## 3. Verify and report

Confirm each finding by reading the query, the schema, and its callers; run the project's type check or tests when available. Report findings ordered by severity (critical, high, medium, low) with `file:line`, the problem, a concrete scenario, and a fix. If there are no findings, say so and list what was checked.

## Examples

- Use: "Review the queries in src/orders.ts." "Check this service for Prisma mistakes."
- Skip: "Add a status field to the Order model and migrate." "Review this Kysely query." "Add an endpoint that lists orders."
