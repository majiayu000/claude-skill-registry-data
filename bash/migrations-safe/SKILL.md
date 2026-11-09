---
name: migrations-safe
description: Write and review database schema migrations so they do not lose data, break the code already running, or lock a busy table. Use when creating or reviewing a migration file (raw SQL, Prisma, Drizzle, Flyway, Liquibase, goose, dbmate, golang-migrate, Atlas, Alembic, Django, Knex, Rails), when dropping, renaming or retyping columns or tables, adding NOT NULL or an index to a populated table, when a migration failed or locked production, when an applied migration was edited, or when two branches' migrations collide. Not for data modelling from scratch, SELECT or index tuning, ORM usage, moving data between database products, or upgrading the database server.
allowed-tools:
  - Bash(node ${CLAUDE_SKILL_DIR}/scripts/*)
  - Bash(node "${CLAUDE_SKILL_DIR}/scripts/*")
---

# Safe migrations

A migration runs once, against data you have not seen, while the previous version of the code is still
serving traffic. It is safe when three things hold: **no data is lost** without a decision, **the code
already deployed keeps working** against the new schema, and **no lock stops traffic** for longer than a
few seconds. Two more concern the history: what is already applied is never rewritten, and every
environment applies the new files in the same order.

## Method

### 1. Lint every new migration before it is applied

The npm package `migrations-safe` ships these scripts as one command: `migrations-safe lint ...` is
`migration-lint.mjs ...` and `migrations-safe rehearse ...` is `rehearse.mjs ...`. If the project lists it in its
`devDependencies`, run `npx --no-install migrations-safe lint|rehearse` instead of
`node "${CLAUDE_SKILL_DIR}/scripts/<name>.mjs"` in every command below: it is the version CI runs. Without it, the
commands below run the copy in this skill.

```bash
node "${CLAUDE_SKILL_DIR}/scripts/migration-lint.mjs" db/migrations/20261030_add_due_on.sql
node "${CLAUDE_SKILL_DIR}/scripts/migration-lint.mjs" --history          # migrations new in this branch + git checks
node "${CLAUDE_SKILL_DIR}/scripts/migration-lint.mjs" prisma/migrations --fail-on warning
python manage.py sqlmigrate shop 0042 | node "${CLAUDE_SKILL_DIR}/scripts/migration-lint.mjs" - --runner django
```

The same commands work in PowerShell: `${CLAUDE_SKILL_DIR}` is replaced with the skill's path before the
shell sees the command, so it is not an environment variable.

- Needs Node 22.13+. No database needed; reads `.sql` files or SQL on stdin (`-`). The rehearsal in step 4
  needs the `docker` CLI for PostgreSQL, MySQL, MariaDB, SQL Server, Oracle and Db2.
- The runner (Prisma, Drizzle, Flyway, Liquibase, goose, dbmate, golang-migrate, Atlas, Alembic, Django,
  Knex, Rails, EF Core, DbUp, SqlPackage, or plain SQL) and the dialect (PostgreSQL, SQLite, MySQL, SQL Server,
  Oracle, Db2) are detected from the project; override with `--runner` and `--dialect`. Details per runner, and how to feed Alembic, Django, Knex and Rails:
  [references/runners.md](references/runners.md). Read it when the project uses any of them.
- Exit 0 nothing at the failure level, 1 findings, **2 could not run, which is never a pass** (0 files
  linted, shallow clone, bad arguments).
- `--fail-on warning|error|<rule>,...` sets what fails (default: errors; `--strict` is `warning`).
  `--format json|sarif|github` for machines (JSON has `schemaVersion: 1`).
- `--history` compares with the base (`origin/main`, `main`, `--base <ref>`): edited, renamed or deleted
  applied migrations, a new one that sorts before the base's newest, duplicate versions. It needs full
  history: in CI use `fetch-depth: 0`. Re-run it against the current tip of main just before merging.
- For PostgreSQL also run `squawk` as a second opinion: the linter here is regex-based, not a parser.

### 2. Classify each change: additive, or several releases?

Additive and safe in one step: a new table, a new nullable column, a new column with a **constant**
default (PostgreSQL 11+, MySQL 8 instant), an index built concurrently, a constraint added `NOT VALID`.

Anything that removes, renames or narrows needs **expand, migrate, contract**, each its own deploy,
because during a rolling deploy (and after a rollback) the old code runs against the new schema:

| Step | Schema | Code |
|---|---|---|
| Expand | Add the new column or table next to the old one | Writes both; reads old |
| Migrate | Backfill in batches; then enforce (NOT NULL, FK) with `NOT VALID` plus `VALIDATE` | Reads new (flag if it matters) |
| Contract | Drop the old one in a later release, once no deployed version reads it | Old path deleted |

For ORMs that cache column lists (Rails, Hibernate), tell the ORM to ignore the column (`ignored_columns`,
`@Transient`) one release before dropping it. Tools that automate expand: pgroll, Reshape; for MySQL tables
too big for `ALTER`: gh-ost, pt-online-schema-change.

### 3. Fix findings by root cause

Every rule, why it breaks, the correct fix and the wrong one: [references/rules.md](references/rules.md).
Load it when a finding needs explaining. In short:

- **Data loss** (`drop-*`, `truncate`, `delete-all`, `update-all`, `rebuild-drops-column`,
  `prisma-data-loss-warning`): contract step only, verified backup, recorded approval; backfills in
  batches outside the DDL migration.
- **Breaks running code** (`rename-*`, `change-column-type`, `not-null-without-default`): expand, migrate,
  contract. Never a fake default to make NOT NULL pass.
- **Locks** (`set-not-null`, `constraint-*`, `*-index-*`, `volatile-default`, `rewriting-column`,
  `missing-lock-timeout`): `NOT VALID` then `VALIDATE`, `CONCURRENTLY` in its own no-transaction file,
  `SET lock_timeout` before the first `ALTER`.
- **MySQL and MariaDB** (`mysql-*`): which `ALGORITHM` the operation and the server version allow, metadata-lock
  waits (`SET SESSION lock_wait_timeout`), foreign keys, FULLTEXT, primary keys, ENUM, charset and rebuilds.
  Pass `--mysql-version 8.0.28|8.4|mariadb-10.6` (default 8.0, or the image in the project's compose file); big
  tables go through gh-ost or pt-online-schema-change. Tables and caveats: [references/mysql.md](references/mysql.md).
- **SQL Server** (`mssql-*`): online DDL needs Enterprise, so the rules depend on `--edition standard|enterprise|azure`
  (default `standard`) and `--server-version 2016|2019|2022|2025`: NOT NULL with a default, `ALTER COLUMN`,
  offline index builds, `ONLINE` on an edition without it, `LOCK_TIMEOUT`, `WITH CHECK` constraints. Details:
  [references/mssql.md](references/mssql.md).
- **Oracle** (`oracle-*`): `--edition se2|ee` (default `se2`), `--server-version`: column defaults before 12.1,
  `DDL_LOCK_TIMEOUT` (Oracle fails at once instead of queueing), DDL that commits earlier DML, `ONLINE`,
  `ENABLE NOVALIDATE`, a PL/SQL block without `/`. Details: [references/oracle.md](references/oracle.md).
- **Db2 LUW** (`db2-*`): `DROP COLUMN`, `SET NOT NULL` and `SET DATA TYPE` leave the table REORG-pending until
  a `CALL SYSPROC.ADMIN_CMD('REORG TABLE t')`, at most three such units of work, constraint checks, lock
  timeout. Details: [references/db2.md](references/db2.md).
- **Transactions and rollback** (`concurrently-in-transaction`, `transaction-conflict`, `not-atomic`,
  `missing-down`): know whether the runner wraps the file; a down that runs, or an `irreversible` plan.
- **History** (`applied-migration-changed`, `out-of-order`, `duplicate-sequence`): restore the applied file
  and write a **new** migration; renumber the branch's migration, never main's. `flyway repair`,
  `alembic stamp`, `prisma migrate resolve`, `atlas migrate hash` are a person's recorded decision.

Silencing is a recorded decision, as a comment of its own that starts with `migration-lint:`, a known
rule, and a reason; anything else silences nothing and raises `invalid-directive`:

```sql
-- migration-lint: allow drop-column -- contract step, approved by <who> on <date>, backup <id>
-- migration-lint: allow-file not-atomic -- the runner wraps each file in a transaction
-- migration-lint: irreversible -- restore from the nightly snapshot if needed
```

A migration is also **self-contained**: it does not import the application's current models, enums or
services (Django `apps.get_model`; Rails: a minimal model class inside the migration). And the schema
history must match the model: `makemigrations --check`, `alembic check`, `prisma migrate diff --exit-code`,
`drizzle-kit check`.

SQLite cannot alter most column properties, so tools rebuild the table (create `new_t`, `INSERT ... SELECT`,
drop, rename). The linter checks the rebuild against the table as earlier migrations in the folder (or
`--schema <sql>`) left it, and reads Prisma's `Warnings` comment; the rehearsal checks the data.

### 4. Rehearse on a copy with realistic data

An empty test database proves almost nothing. SQLite is rehearsed on a copy of the file; PostgreSQL, MySQL,
MariaDB, SQL Server, Oracle and Db2 on a throwaway Docker container of the same engine and version as production:

```bash
node "${CLAUDE_SKILL_DIR}/scripts/rehearse.mjs" app.db db/migrations/0007_due.sql
node "${CLAUDE_SKILL_DIR}/scripts/rehearse.mjs" seed.sql 0007.up.sql --down 0007.down.sql        # up, down, up
node "${CLAUDE_SKILL_DIR}/scripts/rehearse.mjs" --engine postgres:16 seed.sql db/migrations/0007_due.sql --down
node "${CLAUDE_SKILL_DIR}/scripts/rehearse.mjs" --engine mysql:8.4 --dump prod-subset.sql.gz 0007.sql --lock-budget 1s
```

Every run applies the migrations in order the way the runner does (transaction wrapping, down sections) and
reports, per table, rows and columns added, dropped or emptied. It fails on lost rows or values and on
migrations that do not run; SQLite also on new foreign-key orphans. With `--engine` it also reports each
migration's duration and the write-blocking locks it held (PostgreSQL `pg_locks`, MySQL and MariaDB metadata
locks, SQL Server `sys.dm_tran_locks`, Oracle `v$lock`, Db2 `MON_GET_LOCKS`, polled from a second session; Db2
also fails a migration that leaves a table REORG-pending), and fails when one is held longer than `--lock-budget` (default 2s).
The container is removed when the run ends, also on failure, Ctrl+C and SIGTERM (a hard kill leaves it; the
next run sweeps it); `--keep` leaves it and prints how to remove it.
Exit 2 means docker is missing or cannot pull the image, never a pass. How to seed, read the output and what
the lock numbers mean: [references/rehearsal.md](references/rehearsal.md). Load it before rehearsing.

### 5. Verify and report

Finish when the linter shows **0 errors, or each remaining finding is allowed in the file with its
reason**. Do not loop on warnings by editing around them, and do not add an `allow` to get green.

- Linter exit code and last line per run; every `allow` with its reason.
- Rehearsal: where (engine, version, data size), duration, longest lock, rows and columns before and after,
  the N-1 code's test suite against the migrated schema.
- The release plan when the change has several steps: which deploy carries which migration.
- What could not run, said as such ("rehearsal could not run: no copy of production available").

## Limits

- Regex over statements, not a SQL parser: standard DDL only; `DO` blocks and procedural bodies are skipped.
- "Existing table" means not created earlier in the same file (or earlier new migration with `--history`).
  Table sizes are unknown: a lock error on a ten-row table can be allowed with that reason; on a
  hundred-million-row table it is an outage.
- ORM migrations in Ruby, Python or TypeScript are not read; lint the SQL they produce.
- MySQL and MariaDB are covered at the depth of the online DDL tables (see step 3), for the server version
  given with `--mysql-version`; Percona and other forks follow MySQL. SQL Server, Oracle and Db2 LUW have rules
  by version and edition; T-SQL without semicolons is split by keyword heuristics, not a parser. Db2 for z/OS
  and Db2 for i are not covered, and Azure SQL is linted (`--edition azure`) but not rehearsed. Oracle SE2 is
  not emulated by the rehearsal (Free has the Enterprise features).
