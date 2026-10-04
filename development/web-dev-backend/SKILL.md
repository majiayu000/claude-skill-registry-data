---
name: web-dev-backend
description: "Web backend work in Node/TypeScript (Express, Fastify) and Python (FastAPI, Django): routes, middleware, async I/O, validation, type discipline. Use when building or reviewing backend services, API endpoints, database schemas and migrations, or files under api/, backend/, or server/."
license: MIT
metadata:
  display-name: "Web Backend"
  version: "1.1"
  platforms: "claude-code codex"
  tags: "backend nodejs python api"
---

# Web dev - backend

## Type discipline

### TypeScript / Node.js
- `strict: true` + `noUncheckedIndexedAccess: true` + `exactOptionalPropertyTypes: true` in `tsconfig.json`.
- Validate every request/response with `zod`. Inferred types come from schemas, not the other way around.
- Use `unknown` at boundaries (`req.body: unknown`); narrow with `schema.parse(...)` before touching.
- Avoid `as` casts. If types disagree, fix the type - don't override the checker.

### Python
- Type-annotate every function signature in new code. `mypy --strict` (or `pyright`) on changed modules. No `# type: ignore` to silence.
- `pydantic` v2 models for I/O boundaries - validation + types + serialization in one.
- `from __future__ import annotations` for forward refs and deferred eval.

## Project layout & packaging

### TypeScript / Node.js
- Monorepo? Use workspaces (npm/pnpm). Shared modules become `@scope/<pkg>` packages with their own `package.json`.
- `dist/` is build output - gitignored unless a `file:` workspace dep requires committed builds.
- Pin Node version in `package.json` (`"engines": { "node": ">=20" }`) and `.nvmrc`. Lockfile (`package-lock.json` or `pnpm-lock.yaml`) is committed.
- One `tsconfig.json` for build, optional `tsconfig.test.json` for tests.

### Python
- `src/` layout for libraries (`pyproject.toml` + `src/<package>/`). Avoids the import-from-cwd footgun.
- Pin Python version in `pyproject.toml` (`requires-python = ">=3.11"`). Pin runtime deps with upper bounds. Lock with `uv lock` / `pip-compile` / `poetry lock`.
- `requirements.txt` is for deployment lockfiles, not authoring. Author in `pyproject.toml`.
- Use `uv` or `poetry` for new projects.

## Async vs sync

### Node.js
- Everything is async by default. Never block the event loop with sync I/O or CPU-bound work (`fs.readFileSync`, `JSON.parse` of a 1GB file, sync crypto).
- CPU-bound work: `worker_threads` or a separate process.
- Streams beat buffering for large payloads. `pipeline()` from `node:stream/promises` handles cleanup correctly.

### Python
- Pick one I/O model per service. Don't mix async and sync database clients in the same request path - you'll deadlock or block the event loop.
- In async code: never call sync I/O (`requests`, `time.sleep`, blocking DB drivers). Use `httpx`, `asyncio.sleep`, async DB drivers (`asyncpg`, `motor`).
- CPU-bound work in an async service goes in a thread pool (`asyncio.to_thread` - Python 3.9+) or a separate process.

## Web frameworks

### Express / Fastify (Node.js)
- Validate at the edge with `zod` - reject before any business logic runs.
- Middleware order matters: security headers → CORS → rate-limit → body parser → auth → routes → error handler.
- One router file per resource (`routes/users.ts`, `routes/cases.ts`). Don't dump every endpoint in `app.ts`.
- Always set `trust proxy` correctly behind a load balancer or you'll log/limit the wrong IP.

### FastAPI
- Pydantic models for every request/response. Use `Depends()` for auth, db sessions, settings - not module globals.
- Always validate input at the edge. Never trust query strings, headers, JSON bodies, or path params.

### Django
- Fat models, thin views; use `select_related` / `prefetch_related` to kill N+1 queries.

### Flask
- Factory pattern (`create_app()`); blueprints for grouping; `flask-smorest` if you want OpenAPI.

## Data & I/O

### SQL (SQLite, Postgres, MySQL)
- Parameterized queries *always*. Template literals / f-strings into SQL = SQL injection waiting to happen.
- SQLite specifics: `PRAGMA journal_mode = WAL` for concurrent reads; `PRAGMA foreign_keys = ON` (off by default!); `PRAGMA busy_timeout = 5000` to avoid `SQLITE_BUSY`.
- Postgres: use a connection pool; `LISTEN`/`NOTIFY` beats polling for change feeds.
- Indexes: cover the queries you actually run. `EXPLAIN ANALYZE` before adding a new one.

### Files & streams
- Use context managers / `using` patterns for files, connections, locks. Don't rely on GC.
- Stream large files - don't `.read()` / `.readFile()` a 4GB CSV into memory.
- Temp files: `tmp` / `tempfile` with auto-cleanup, not hardcoded `/tmp/foo`.

### Dataframes (Python)
- Prefer `polars` for new pipelines (faster, eager-or-lazy, better memory).
- `pandas` is fine if the project already uses it.

## Auth, sessions, tokens

Auth, JWT, and password discipline lives in the `security-review` skill - read it before wiring up auth in a new service. The short version: bcrypt/scrypt/argon2id only, JWT signature verified before claims, authorization is per-request not per-session, sessions are httpOnly + sameSite cookies.

## Errors & logging

- Raise/throw specific errors, catch specific errors. Generic `catch (e)` / `except Exception` only at the top of a worker loop, and re-raise after logging.
- Use `pino` (Node) or `structlog` / `logging` (Python). Configure once, at app entry. Never `console.log` / `print` in production code paths.
- Log structured fields, not interpolated strings: `log.info({ caseId, ms }, 'processed')` beats `log.info("processed " + caseId)`.
- Don't log secrets, tokens, full request bodies, PII/PHI.
- Redact array in the logger config covers every API key the app handles.

## Concurrency safety

- Module-level mutable state is a bug. If you need shared state, use a lock or a dedicated store.
- Idempotency keys on any external mutation (payment, email, queue publishes) - retries are inevitable; double-sends are not.
- Database transactions: keep them short; don't await network calls inside them.

## Tooling baseline

### Node.js / TypeScript
- `eslint` + `prettier` (or `biome` for both). Config in `package.json` or `.eslintrc`.
- `tsc --noEmit` in CI on every PR.
- `vitest` or `jest` for tests (see `qa-automation` skill).

### Python
- `ruff` for lint + format (replaces `flake8`, `isort`, partly `black`). Config in `pyproject.toml`.
- `mypy` / `pyright` for type checking.
- `pytest` for tests (see `qa-automation` skill).
- `pre-commit` to run lint + types on staged files.

## Verification before declaring done

- Type-check passes (`tsc --noEmit`, `mypy`, `pyright`).
- Tests pass (`vitest run`, `pytest -x`).
- For services: hit the endpoint with `curl` / `httpie` and verify the response shape matches the schema. Don't assume.
- For migrations: run forward + rollback against a real DB copy before merging.
