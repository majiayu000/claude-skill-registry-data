---
name: postgres-neon-connection-and-migrations
description: >
  Standard patterns for connecting applications to Neon Postgres and
  managing schema changes via migrations (Alembic / SQLModel / SQLAlchemy),
  with attention to serverless connection behaviour.
---

# Postgres + Neon Connection and Migrations Skill

## When to use this Skill

Use this Skill whenever you are:

- Configuring a PostgreSQL connection for an app that runs on **Neon**.
- Setting up or refactoring database connection code (engines, pools).
- Adding or updating database **migrations** (Alembic or similar).
- Debugging issues related to connections, scaling-to-zero, or schema
  drift on Neon.

This Skill must work for any backend that uses Neon Postgres, not just
a specific framework or repository. [web:85][web:87][web:98]

## Core goals

- Use Neon’s **recommended connection patterns** for reliability and
  serverless behaviour:
  - Correct connection strings.
  - Respect Neon’s built-in pooling and scaling.
- Centralize database connection configuration in one module.
- Treat schema changes as **migrations**, not ad-hoc table creation.
- Keep environment and secrets out of code (use env vars).

## Neon-specific principles

- Neon is a **serverless Postgres**:
  - It can **scale to zero**, so idle connections may be dropped.
  - It has a built-in **connection pooler** (PgBouncer-like) that can
    handle many concurrent connections. [web:87][web:98]

- Connection best practices:
  - Use a single, long-lived engine/pool per application process where
    appropriate (for typical FastAPI apps). [web:85][web:98]
  - In serverless/edge functions, create short-lived pools or clients
    inside the request handler and close them at the end of the request,
    as recommended by Neon. [web:92][web:98]
  - Use Neon’s provided `DATABASE_URL` connection string and do not
    hard-code hostnames, ports, or credentials.

- Be prepared for occasional connection resets due to scaling-to-zero:
  - Enable pre-ping or equivalent health checks in your driver/ORM.
  - Handle reconnects gracefully.

## Environment variables and configuration

- The Neon connection string must come from environment variables, for
  example:

  - `DATABASE_URL` – primary Neon Postgres connection string.
  - Optional `DATABASE_URL_RW` / `DATABASE_URL_RO` if using read/write
    separation.

- Configuration rules:
  - Never commit real connection strings to source control.
  - Document required env vars in project docs, not hard-coded here.
  - Allow different `DATABASE_URL` values per environment (dev, staging,
    prod) without changing code.

## Connection patterns by runtime

- For **long-running app servers** (e.g. FastAPI, Node API server):

  - Create the engine/pool once at module import or app startup.
  - Reuse the same engine/pool for all requests.
  - Use a dependency or helper to create short-lived sessions/transactions
    per request. [web:53][web:57][web:85]

- For **serverless/edge runtimes**:

  - Follow Neon’s official guidance:
    - Create a pool/connection **inside** the handler.
    - Execute queries.
    - Close/end the pool/connection before returning, or via the
      platform’s background hooks. [web:92][web:98]
  - Avoid global, long-lived pools that might exceed connection limits.

## Migrations and schema management

- Treat the database schema as **code with history**:
  - Use a migration tool (e.g. **Alembic** for SQLModel/SQLAlchemy) to
    track schema changes over time. [web:88][web:91][web:99]

- Recommended pattern with Alembic:

  - Initialize Alembic in the project:
    - `alembic init alembic` (or equivalent command).
  - Configure `alembic.ini` to load `sqlalchemy.url` from the same
    env var used by the app (`DATABASE_URL`). [web:88][web:91]
  - Set `target_metadata` in `alembic/env.py` to your ORM models’
    metadata so migrations can be generated from model changes.
  - Use migrations to:
    - Create initial tables.
    - Add/remove columns or indexes.
    - Evolve relationships.

- Avoid calling `metadata.create_all()` in production startup paths for
  non-trivial apps; prefer running migrations as part of deploy/CI/CD.

## Migration workflow

- Typical workflow:

  - Define or update models in your ORM (SQLModel/SQLAlchemy).
  - Generate a new migration with Alembic (autogenerate if possible).
  - Review and adjust the migration script.
  - Apply the migration to Neon using Alembic commands. [web:88][web:91]

- The application should assume the schema is already up to date; it
  should not modify the schema at runtime under normal conditions.

## Health checks and observability

- Implement simple health checks for the database:

  - e.g. a lightweight query in a `/health` endpoint or startup probe.

- Log connection errors with enough context to debug issues related to:
  - Wrong connection string.
  - Expired credentials.
  - Exceeded connection limits.

- In serverless environments, pay attention to:
  - Cold starts.
  - Connection initialization time.

## Things to avoid

- Hard-coding Neon connection details (host, database, user, password)
  in source files.
- Creating new engines/pools on every request in a long-running server.
- Skipping migrations and relying only on `create_all()` for schema
  changes in production.
- Ignoring Neon’s characteristics (scaling-to-zero, connection pooling)
  and treating it as a static, always-on Postgres without pooling. [web:87][web:98]

## References inside the repo

When present, this Skill should align with:

- A central database configuration module (e.g. `db.py`, `database.py`,
  or `db/__init__.py`) that:
  - Reads `DATABASE_URL` from the environment.
  - Creates the engine/pool.
  - Exposes session/connection helpers.

- A migrations directory (e.g. `alembic/`) that:
  - Uses the same `DATABASE_URL`.
  - Imports ORM metadata for `target_metadata`.

If these are missing, propose creating them following Neon’s official
guides and the patterns described above instead of inventing a new,
ad-hoc connection/migration approach per project.
