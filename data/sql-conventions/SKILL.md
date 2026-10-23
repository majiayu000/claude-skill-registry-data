---
name: sql-conventions
description: "Use when writing or reviewing SQL, schemas, indexes or database permissions on PostgreSQL, MySQL/InnoDB or SQLite: types, constraints, query and index shape, transactions and locking, DDL that locks, injection and least privilege. Engine-specific facts are marked with the engine; ORM and migration-runner tooling is not covered here."
---

# sql-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the SQL itself, whoever writes it: a hand-written query, a
migration file, an ORM's generated statement that someone reads in a log. It sits under the stack blocks
(`laravel-conventions`, `python-conventions` §7, `nestjs-node-conventions`, `dotnet-conventions`), which own
the mapper, and next to `devops-conventions` §6, which owns the deployment order of a schema change. Every
rule below holds in a repo with nothing installed (`CONVENTIONS.md`, rule A).

**Special status.** New block, no in-house production experience behind it: the content comes from the
engines' own manuals and from vendor-published guidance, read on 2026-10-02. A base to confront with the first
real project, not proven doctrine. Engine behaviour that depends on a version is marked; confirm the deployed
version before applying it.

**Step zero, every time.** Resolve three facts and state them before reading anything else: the **engine and
its major version**, the **deployment shape** (managed or self-run, behind a connection pooler or not), and
the **access layer** (hand-written SQL, a query builder, an ORM). A rule that holds on one engine can be false
on another (§1.4), and a pooler changes what session state survives (§4.8). If a fact is unknown, ask.

## When
A table, column, constraint, index, query, migration, role or grant is written or changed, or a slow or
blocked statement is diagnosed.

## Steps

**Read the rows whose trigger the task meets**, not the table.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Types and names | a table or column is created or changed | [`01-types-and-names.md`](./references/01-types-and-names.md) |
| 2 | Keys, constraints, NULL | a key, constraint, foreign key or nullable column is written | [`02-keys-constraints-null.md`](./references/02-keys-constraints-null.md) |
| 3 | Queries and indexes | a query is written, an index added, a statement is slow | [`03-queries-and-indexes.md`](./references/03-queries-and-indexes.md) |
| 4 | Transactions, isolation, locking | two writers can touch the same rows, a job claims work, a deadlock or timeout shows up | [`04-transactions-and-locking.md`](./references/04-transactions-and-locking.md) |
| 5 | DDL that locks | an `ALTER`, an index build, a constraint on a table that is in use | [`05-ddl-that-locks.md`](./references/05-ddl-that-locks.md) |
| 6 | Injection, privileges, row-level security | SQL is built from input, a role or grant is created, row security is used | [`06-access-and-injection.md`](./references/06-access-and-injection.md) |
| 7 | Engine notes: MySQL/InnoDB and SQLite | the engine is one of those two | [`07-engine-notes.md`](./references/07-engine-notes.md) |

## Output / checkpoint
Every new column has a type chosen for its meaning (§1), a stated nullability (§2), and every foreign key
has the index its parent's delete needs (§2.5). A new query was read as a plan on realistic data, not only
run (§3.1). A statement that needs a lock on a live table names the lock and the timeout (§5). Nothing here
writes a pipeline checkpoint.

## Guardrails
- Never build a statement by concatenating or interpolating input (§6.1).
- Never run a schema change that takes a strong lock on a live table without the lock named and a timeout set (§5).
- Never run `EXPLAIN ANALYZE` on a data-changing statement against data you cannot afford to change (§3.2).
- Never grant more than the role needs, and never to the catch-all public role (§6.3).
- Do not recite a figure (a pool size, a row count at which to partition, a batch size) as a rule: measure.
- No comments in the SQL or code produced.

## Origin
The PostgreSQL, MySQL and SQLite manuals and the PostgreSQL community's "don't do this" list, plus
vendor-published database guidance (MIT, Apache-2.0), read 2026-10-02 and rewritten. Provenance, licence
handling and the version stamps are in [`references/origin.md`](./references/origin.md).
