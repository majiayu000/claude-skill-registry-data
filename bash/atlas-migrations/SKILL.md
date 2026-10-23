---
name: atlas-migrations
description: "Authors and runs Atlas database schema migrations - declarative HCL or SQL schema definition with `atlas schema apply` for desired-state apply OR `atlas migrate diff` to generate versioned migrations against a dev DB; `atlas migrate apply` to deploy; `atlas migrate lint` to flag destructive / locking / data-loss patterns; `atlas migrate hash` to detect tampering. Supports PostgreSQL, MySQL, SQL Server, ClickHouse, SQLite, MariaDB, Snowflake, Oracle, Redshift, Spanner, CockroachDB, Databricks. Use when the user wants Terraform-style declarative DB schema management or modern SQL-first migration linting beyond Flyway / Liquibase."
---

# atlas-migrations

## Overview

Atlas manages and migrates database schemas as code - define the
desired schema and Atlas plans, lints, tests, and applies the changes
(per [atlasgo.io/getting-started][at-start]). Two operating modes:

[at-start]: https://atlasgo.io/getting-started

1. **Declarative** - define desired state in HCL or SQL; Atlas
   computes diff and applies (`atlas schema apply`).
2. **Versioned** - Atlas generates timestamped migration files from
   schema diffs (`atlas migrate diff`); migrations apply forward
   (`atlas migrate apply`).

Most production teams use versioned mode for the audit trail; dev
loops often use declarative mode for fast iteration.

## How to use

Follow Steps 1-9 in order - lint (Step 6) is the gate before apply
(Step 5).

## Step 1 - Install

Per [at-start][at-start]:

```bash
# Homebrew (macOS / Linux)
brew install ariga/tap/atlas

# Docker: nothing to install, mount the migrations directory
docker run --rm --net=host -v "$(pwd)/migrations:/migrations" \
  arigaio/atlas migrate apply --url "$DATABASE_URL"
```

In GitHub Actions, `uses: ariga/setup-atlas@v0` puts the CLI on the
runner (Step 8, per [at-gha][at-gha]). The getting-started page also
lists per-platform binaries with md5 and sha256 checksums; verify the
checksum before running a downloaded binary. Prefer these over piping
the vendor install script into a shell, which runs unreviewed remote
code.

[at-gha]: https://atlasgo.io/integrations/github-actions

## Step 2 - Define schema

Per [at-start][at-start], schema can be SQL (most common) or HCL. SQL
example (PostgreSQL):

```sql
-- schema.sql
CREATE TABLE users (
  id serial PRIMARY KEY,
  name varchar(255) NOT NULL,
  email varchar(255) UNIQUE NOT NULL,
  created_at timestamptz DEFAULT now()
);
```

For the same schema expressed in Atlas's HCL DSL and guidance on when
HCL vs SQL matters, see [references/hcl-schema.md](references/hcl-schema.md).

The dev DB referenced via `--dev-url` is a **temporary scratch
database** Atlas uses to compute the diff (Atlas applies the desired
state to the scratch DB, then computes the migration vs production).

## Step 3 - Apply schema (declarative mode)

Per [at-start][at-start]:

```bash
atlas schema apply --url "$DATABASE_URL" --to file://schema.sql \
  --dev-url "docker://postgres/17/dev?search_path=public"
```

`--url` = target DB; `--to` = desired schema definition; `--dev-url`
= scratch DB for diff computation. Atlas prints the planned changes
and prompts for confirmation by default.

## Step 4 - Generate versioned migrations

Per [at-start][at-start]:

```bash
atlas migrate diff initial --to file://schema.sql \
  --dev-url "docker://postgres/17/dev?search_path=public"
```

This generates a timestamped migration file in `migrations/` (e.g.,
`20260506120000_initial.sql`). Subsequent calls with a new schema
generate new migrations against the previous state.

## Step 5 - Apply versioned migrations

**Verify (gate before applying):** run Step 6 lint first and assert it
reports no destructive / data-loss findings; if it flags one, fix the
migration (add a `DEFAULT`, split the change, or add a new migration)
and re-run lint until clean. Only then apply:

```bash
atlas migrate apply --url "$DATABASE_URL"
```

Atlas tracks state in `atlas_schema_revisions` table - each applied
migration is recorded with its hash, so tampering is detected on
subsequent applies.

## Step 6 - Lint migrations

Per [at-start][at-start]:

```bash
atlas migrate lint --dev-url "..." --latest 1
```

Lints the most recent migration for: data loss, narrow-column
operations (e.g., `varchar(50)` → `varchar(20)`), missing default
on a `NOT NULL` add, lock-escalating ops on large tables, schema
backwards-incompatibility.

The lint output is the value-add over Flyway / Liquibase - those
tools are syntax-only; Atlas knows about destructive patterns.

## Step 7 - Hash + integrity

Atlas computes hashes for each migration file. If a developer edits
an already-applied migration, `atlas migrate apply` fails until
`atlas migrate hash` re-syncs (intentional act). This protects
against silent migration tampering.

## Step 8 - CI integration

```yaml
- uses: ariga/setup-atlas@v0
- name: Lint migrations
  run: atlas migrate lint --dir "file://migrations" \
    --dev-url "docker://postgres/17/dev?search_path=public" \
    --latest 1
- name: Apply migrations to staging
  run: atlas migrate apply --url "${{ secrets.STAGING_DB_URL }}"
```

GitHub Action `ariga/setup-atlas@v0` provides Atlas in the runner;
the `atlas-action` orchestrator provides PR-comment integration with
diff visualization.

## Step 9 - Composition with sister tools

Beyond `atlas migrate lint`, apply adversarial review with
team-specific risk policies that Atlas's built-in lint doesn't
capture (e.g., "no `DROP TABLE` without DBA approval").

## Worked example

Add a `NOT NULL` column `status` to a 40M-row `users` table:

1. Edit `schema.sql` to add
   `status varchar(20) NOT NULL DEFAULT 'active'` on `users`.
2. `atlas migrate diff add_status --to file://schema.sql --dev-url
   "docker://postgres/17/dev?search_path=public"` writes
   `migrations/20260506120000_add_status.sql`.
3. `atlas migrate lint --dev-url "docker://postgres/17/dev?search_path=public"
   --latest 1` passes because the `NOT NULL` add ships a `DEFAULT`
   (a `NOT NULL` add with no default is flagged).
4. CI runs the same lint on the PR, then
   `atlas migrate apply --url "$STAGING_DB_URL"` records the
   migration in `atlas_schema_revisions`.
5. A teammate later edits that applied file; their
   `atlas migrate apply` fails on hash mismatch until an intentional
   `atlas migrate hash` re-sync - the tamper guard working as
   designed.

## Anti-patterns and limitations

The failure modes (editing applied migrations, skipping `--dev-url`,
declarative `schema apply` straight to production, skipping lint in
CI, blind `atlas migrate hash`) and the tool's limitations (partial
HCL for some DBMS features, general-purpose lint rules, `--dev-url`
requiring a real DBMS, paid Atlas Cloud) are catalogued in
[references/atlas-caveats.md](references/atlas-caveats.md).

## References

- [at-start][at-start] - getting-started, install commands,
  example schema, all `atlas` commands, supported databases
- [at-gha][at-gha] - `ariga/setup-atlas` GitHub Action
- atlasgo.io/docs - full documentation
- github.com/ariga/atlas - repository
- `flyway-migrations`,
  `liquibase-migrations`,
  `sqlmesh-migrations` - sister
  tools (Flyway / Liquibase = imperative versioned; SQLMesh =
  data-pipeline + schema)
