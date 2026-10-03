---
name: surrealkit
description: "SurrealKit schema sync, rollout migrations, seeding, and declarative testing for SurrealDB apps. Part of the surreal-skills collection."
license: MIT
metadata:
  version: "1.7.1"
  author: "24601"
  parent_skill: "surrealdb"
  snapshot_date: "2026-06-17"
  upstream:
    repo: "surrealdb/surrealkit"
    release: "v0.6.3"
    sha: "7771b93ea563"
---

# SurrealKit -- Schema Management for SurrealDB Apps

SurrealKit manages SurrealDB application schemas as desired-state `.surql`
files, with separate paths for disposable development databases and shared or
production rollouts.

Tracked upstream snapshot: **v0.6.3** pre-release (`7771b93ea563`, 2026-05-13).
The v0.6.1 -> v0.6.3 patch line added library-lock fixes, template variables,
comment-stripping cleanup, `DROP ... IF EXISTS` handling, and `DEFINE` coverage
for `BUCKET`, `SEQUENCE`, and `CONFIG`.

## Quick Start

```bash
# Install
cargo binstall surrealkit
# or: cargo install surrealkit

# Scaffold project structure
surrealkit init

# Reconcile local/disposable database to local schema files
surrealkit sync

# Generate and apply a reviewed rollout for shared/prod
surrealkit rollout plan --name add_customer_indexes
surrealkit rollout start 20260410120000__add_customer_indexes
surrealkit rollout complete 20260410120000__add_customer_indexes
```

## Core Commands

| Command | Use |
|---------|-----|
| `surrealkit sync` | Desired-state reconciliation for local, preview, or disposable DBs |
| `surrealkit sync --watch` | Local development loop with file watching |
| `surrealkit rollout baseline` | Establish rollout tracking on an existing shared DB |
| `surrealkit rollout plan --name <name>` | Create a reviewed manifest from current schema diff |
| `surrealkit rollout start <id>` | Apply the expansion phase |
| `surrealkit rollout complete <id>` | Apply the contract/destructive phase after cutover |
| `surrealkit rollout rollback <id>` | Roll back an in-flight rollout |
| `surrealkit rollout lint <id>` | Validate a rollout without mutating the DB |
| `surrealkit rollout status` | Inspect rollout state stored in the DB |
| `surrealkit seed` | Apply seed data |
| `surrealkit test` | Run declarative schema, permission, and API tests |

## When to Use It

- Use `sync` when the database should mirror local files immediately.
- Use `rollout` when changes need staging, review, rollback, or controlled cutover.
- Use `seed` for deterministic fixture data.
- Use `test` in CI to validate permissions, schema behavior, and API contracts.

## Environment

SurrealKit reads these variables:

- `SURREALDB_HOST` (fallback: `DATABASE_HOST`)
- `SURREALDB_NAME` (fallback: `DATABASE_NAME`)
- `SURREALDB_NAMESPACE` (fallback: `DATABASE_NAMESPACE`)
- `SURREALDB_USER` (fallback: `DATABASE_USER`)
- `SURREALDB_PASSWORD` (fallback: `DATABASE_PASSWORD`)
- `SURREALDB_AUTH_LEVEL` (fallback: `DATABASE_AUTH_LEVEL`)

## Testing

Declarative suites in `database/tests/suites/*.toml` support:

- `sql_expect`
- `permissions_matrix`
- `schema_metadata`
- `schema_behavior`
- `api_request`

Example:

```bash
surrealkit test --fail-fast --json-out artifacts/surrealkit-tests.json
```

## Full Documentation

See the main skill rule for full operating guidance:
- **[rules/surrealkit.md](../../rules/surrealkit.md)** -- sync vs rollout strategy, env vars, seeds, declarative tests, and CI patterns
- **[surrealdb/surrealkit](https://github.com/surrealdb/surrealkit)** -- upstream repository
