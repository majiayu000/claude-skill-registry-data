---
name: flyway-migrations
description: "Authors and runs Flyway database migrations - versioned (`V1__add_users.sql`), repeatable (`R__refresh_views.sql`), and undo (`U1__remove_users.sql`) migration files in `db/migration/`; runs `flyway migrate` / `info` / `validate` / `clean` / `baseline` / `repair`; tracks state in the `flyway_schema_history` table; supports 50+ databases including Oracle / SQL Server / MySQL / PostgreSQL / MariaDB / Snowflake / BigQuery; integrates with Maven, Gradle, CLI, and Docker. Use when the user works with Flyway-managed schemas, asks about migration ordering, or needs CI gates on schema changes."
---

# flyway-migrations

## Overview

Flyway tracks applied migrations in a per-database `flyway_schema_history`
table and applies pending migrations in order by version number
([fw-how][fw-how]).

[fw-home]: https://documentation.red-gate.com/fd/flyway-documentation-138346877.html
[fw-how]: https://documentation.red-gate.com/fd/quickstart-how-flyway-works-184127223.html

## When to use

- The repo has a `db/migration/` (or configured) directory of
  `V*.sql` / `R*.sql` files.
- The user works with Flyway CLI / Docker / Maven plugin / Gradle
  plugin.
- A CI workflow needs a migration gate against a per-PR ephemeral
  database (e.g., Testcontainers) before merge.
- The team migrates from manual SQL scripts to versioned migration
  control.

## How to use

Follow Steps 1 - 7 below in order; each numbered step is the single source
for that part of the workflow.

## Step 1 - Install

Flyway runs on Windows, macOS, Linux, and Docker, plus Maven and Gradle
plugin distributions ([fw-home][fw-home]). Common install paths:

```bash
# Docker (zero-install for CI)
docker run --rm -e FLYWAY_PASSWORD flyway/flyway -url=jdbc:postgresql://host/db -user=usr migrate

# Homebrew (macOS / Linux)
brew install flyway

# Maven plugin (Spring Boot etc.)
# add to pom.xml under <build><plugins>
```

Never put the password on the command line or in a committed file. Flyway
reads it from `FLYWAY_PASSWORD` ([fw-pass][fw-pass]), and per
[docker-env][docker-env] a bare `-e FLYWAY_PASSWORD` forwards the host's
value into the container; CI sets it from its secret store.

[fw-pass]: https://documentation.red-gate.com/fd/environment-password-setting-277578929.html
[docker-env]: https://docs.docker.com/reference/cli/docker/container/run/

## Step 2 - First migration

Migrations may be written in SQL, Java, or other scripting languages
([fw-how][fw-how]). File naming places migrations in the configured
`locations` (default `db/migration`):

```
db/migration/
├── V1__create_users.sql
├── V2__add_email_index.sql
├── R__refresh_active_users_view.sql      # repeatable, reruns on checksum change
└── U1__remove_users.sql                   # undo (Flyway Teams)
```

The prefix scheme:

| Prefix | Type | Reruns? | Use |
|---|---|---|---|
| `V<n>__` | Versioned | Once | New schema changes; immutable after merge |
| `R__` | Repeatable | When checksum changes | Views / stored procs / seed data |
| `U<n>__` | Undo | Inverse of versioned | Rollback (Teams edition) |

`__` (double underscore) separates version + description; `.sql` (or
configured suffix) marks the file as a migration.

## Step 3 - Core commands

The daily loop is `flyway info` (preview pending) -> `flyway migrate` (apply
pending) -> `flyway validate` (checksum-verify applied files before deploy).
After a failed migration, `flyway repair` fixes `flyway_schema_history` -
never edit an applied file. Full command reference (baseline, undo, clean,
and the rest): [references/commands.md](references/commands.md).

## Step 4 - Pending-migration semantics

Migrations with a version lower than the history table's current version are
ignored by default; the rest are pending - available but not applied
([fw-how][fw-how]). Safety property: a developer who pulls main and runs
`flyway migrate` applies only the new migrations; those already in
`flyway_schema_history` are not re-run.

## Step 5 - Configuration

Configuration via `flyway.conf` file, env vars (`FLYWAY_*`), or CLI
flags. Key settings:

```properties
flyway.url=jdbc:postgresql://localhost:5432/mydb
flyway.user=myuser
# no flyway.password here - export FLYWAY_PASSWORD instead (Step 1)
flyway.locations=filesystem:db/migration,classpath:db/migration
flyway.baselineOnMigrate=true        # auto-baseline empty schemas
flyway.cleanDisabled=true            # CRITICAL for prod - disable destructive `clean`
flyway.outOfOrder=false              # reject migrations with versions lower than max applied
flyway.validateOnMigrate=true        # checksum-validate before applying
```

`cleanDisabled=true` is a **mandatory production guard** - 
`flyway clean` drops every object in the schema. Always set this in
production config; only enable for ephemeral test databases.

## Step 6 - CI integration

Gate every PR on an ephemeral DB (Docker / Testcontainers): spin the DB,
apply migrations, run tests against the migrated schema. The full GitHub
Actions job and the Testcontainers `@BeforeAll` pattern are in
[references/commands.md](references/commands.md).

## Step 7 - Composition with sister tools

Before merge, apply adversarial review of new migrations -
classify each as additive / breaking / data-loss / locking.

## Worked example

Add an index on `users.email` and ship it through CI:

1. Create `db/migration/V2__add_email_index.sql` with
   `CREATE INDEX idx_users_email ON users(email);`.
2. Locally run `flyway info` - it lists `V2` as pending while `V1`
   shows applied.
3. `flyway migrate` applies only `V2` and appends a row to
   `flyway_schema_history` with its checksum.
4. In the PR, CI starts an ephemeral Postgres, runs the Docker
   `flyway ... migrate`, then `mvn test` against the migrated schema.
5. A teammate later edits the merged `V2` file; on their next run
   `flyway validate` fails with a checksum mismatch, so they add
   `V3__...` instead of mutating `V2`.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Edit a previously-applied versioned migration | Checksum mismatch; `validate` fails on next run | Add a new V_n+1 migration that adjusts |
| `cleanDisabled=false` in production config | One stray `flyway clean` drops the schema | Always `cleanDisabled=true` (Step 5) |
| Mixing versioned + repeatable migrations for the same object | Repeatable applies after every versioned change → race | Pick one per object class |
| `outOfOrder=true` without team agreement | Lower-version migrations apply mid-stream; ordering breaks | Default `false`; enable per change with team review |
| Skip CI gating on per-PR ephemeral DB | Migrations break in production for the first time | Always run migrations in CI (Step 6) |

## Limitations

- Undo migrations are a Teams (paid) feature - OSS users implement
  rollback manually via inverse versioned migrations.
- `flyway clean` is irreversible; the `cleanDisabled=true` guard is
  the only protection.
- 50+ supported DBMS but rule depth varies - consult per-database
  pages on [fw-home][fw-home] for vendor-specific syntax.
- Requires JVM (CLI bundles its own JRE; Docker / Maven plugin
  inherit it).

## References

- [references/commands.md](references/commands.md) - full command table + CI job
- [fw-home][fw-home] - main documentation, command list, supported
  databases
- [fw-how][fw-how] - conceptual model: schema_history table,
  pending-migration semantics, ordering
- [fw-pass][fw-pass] - `FLYWAY_PASSWORD` environment variable
- [docker-env][docker-env] - `docker run -e VAR` forwards the host value
- github.com/flyway/flyway - repository
- `liquibase-migrations`,
  `atlas-migrations`,
  `sqlmesh-migrations` - sister
  tools (Liquibase = changelog-driven; Atlas = declarative HCL;
  SQLMesh = data-pipeline + schema)
