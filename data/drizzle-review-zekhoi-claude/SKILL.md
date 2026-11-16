---
name: drizzle-review
description: Review TypeScript code that builds SQL with Drizzle ORM for correctness, safety, transactions, and performance, and report findings with severity and file locations. Use when asked to review database query code, repositories, or data-access changes in a project that uses Drizzle. Do not use for projects without Drizzle, for writing migrations or schema changes (use agent-kit:database-design), for Kysely or Prisma code (use agent-kit:kysely-review or agent-kit:prisma-review), or for general code review; this skill reports and does not edit code.
---

# Drizzle review

Report findings without modifying code unless the user asks for fixes.

## 1. Understand the schema and conventions

- Read the table definitions (`pgTable`, `mysqlTable`, `sqliteTable`), relations (`relations()` or `defineRelations()`), indexes, unique constraints, and which columns are nullable or have defaults.
- Find the `drizzle()` instance and driver, whether the code uses the SQL-like API (`db.select().from()`) or the relational query API (`db.query.users.findMany`), and how transactions and errors are handled.

## 2. Check each query

**Correctness**

- `db.update(table).set(...)` and `db.delete(table)` without `.where()` affect every row. Flag them unless that is clearly intended.
- Select queries return arrays: flag code that treats `const [row] = await ...` as always defined, and `findFirst` results used without a check for `undefined`.
- `leftJoin` makes the joined table's columns nullable; check the result handling. `limit`/`offset` pagination needs a deterministic `orderBy`. Upserts need the right `onConflictDoUpdate` target (MySQL uses `onDuplicateKeyUpdate` and has no `.returning()`).
- Conditions combined from optional filters must use `and(...)`/`or(...)` correctly; `and()` of all-`undefined` conditions returns no filter and matches every row.

**Safety**

- Values inside the `sql` template are parameterized. `sql.raw()` and `sql.identifier()` with user input are not: flag injection and require an allowlist. Dynamic column choices should map strings to column objects.
- Check tenant or owner filters on every query that needs them, and that responses do not return sensitive columns from `select()` without a column list.

**Transactions**

- Inside `db.transaction(async (tx) => ...)`, every query must use `tx`, not `db`, and be awaited before the callback returns. Avoid slow external calls while the transaction holds locks.

**Performance**

- Queries in loops (N+1) should become one query with `inArray(col, ids)`, a join, or the relational API's `with`. Select only needed columns, check filtered and sorted columns are indexed, and insert many rows with one `insert().values([...])`, guarding against an empty array, which throws.

## 3. Verify and report

Confirm each finding by reading the query, the schema, and its callers; run the project's type check or tests when available. Report findings ordered by severity (critical, high, medium, low) with `file:line`, the problem, a concrete scenario, and a fix. If there are no findings, say so and list what was checked.

## Examples

- Use: "Review the queries in src/orders.ts." "Check this repository for Drizzle mistakes."
- Skip: "Generate a Drizzle migration for a new column." "Review this Prisma query." "Add an endpoint that lists orders."
