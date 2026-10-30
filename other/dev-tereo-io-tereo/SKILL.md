---
name: dev
description: tereo dev command reference. Use when starting core locally, managing the Docker stack, completing first-boot setup, running tests, building packages, running Prisma (generate, migrations, seed), or running the format/lint/import-order checks before a PR.
---

# tereo Dev Commands

There is no project CLI. Everything is a root npm script, an Nx target from a
`packages/*/project.json`, Docker Compose, or Prisma run inside
`packages/tereo`. Commands below say which directory they run from.

## Quick Reference

| Task | Command | Run from |
|------|---------|----------|
| Install | `npm install` | root |
| Start Postgres + Redis only | `docker compose up -d postgres redis` | root |
| Start the whole stack (core, migrate, Postgres, Redis) | `docker compose up` | root |
| Find the setup token (Docker) | `docker compose logs core \| grep "not set up"` | root |
| Run core locally (watch, telemetry loaded) | `npm run dev` | `packages/tereo` |
| Run the admin UI's dev server (:4000) | `npm run dev` | `packages/tereo-ui` |
| Build the admin UI (base `/`, served by core) | `npm run build -w tereo-ui` | root |
| Run the unit tests (no database, Redis or server) | `npm run test:unit` | `packages/tereo` |
| Run the integration tests against local Postgres/Redis | `npm run test:int` | `packages/tereo` |
| Run one test file | `npx vitest run --project int src/tests/routes/v1/admin/users/users.test.ts` | `packages/tereo` |
| Run tests by tag | `npm run test:local -- --tags-filter "auth && race"` (`npx vitest --list-tags`) | `packages/tereo` |
| Run the suite in an isolated Docker stack | `docker/test/run.sh` | root |
| Regenerate the Prisma client | `npx prisma generate` | `packages/tereo` |
| Create a migration (don't apply yet) | `npm run db:migrate -- --name <name>` | `packages/tereo` |
| Apply migrations | `npm run db:migrate:deploy` | `packages/tereo` |
| Seed (idempotent) | `npx tsx src/scripts/seed.ts` | `packages/tereo` |
| Browse the database | `npx prisma studio` | `packages/tereo` |
| Format (fix / check) | `npm run format` / `npm run format:check` | root |
| Import order (fix / check) | `npm run sort-imports` / `npm run sort-imports:check` | root |
| Lint | `npm run lint` | root |
| Lint / re-bundle the OpenAPI spec | `npm run openapi:lint` / `npm run openapi:build` | `packages/tereo` |
| Type-check every package | `npm run check` | root |
| Create a version plan | `npm run version-plan` | root |

## Root npm scripts (`package.json`)

| Script | Runs |
|--------|------|
| `format` / `format:check` | Prettier over `packages/*/src/**/*.{ts,tsx,js,jsx,css}` and `scripts/` |
| `lint` | `eslint packages/ scripts/`, then each workspace's own `lint` script if it has one |
| `sort-imports` / `sort-imports:check` | `scripts/sort-imports.ts` — every package's `src/`. Sort specific paths with `npx tsx scripts/sort-imports.ts <file-or-dir>...` |
| `check` | `nx run-many -t check` (`tsc --noEmit` in every package) |
| `version-plan` | `nx release plan` — writes a file under `.nx/version-plans/` |

## Nx targets (`packages/*/project.json`)

Run with `npx nx run <project>:<target>`, or across projects with
`npx nx run-many -t <target>`.

| Project | Targets |
|---------|---------|
| `tereo` | `generate` (prisma generate), `build` (tsc, after `^build` + `generate`), `check` (tsc --noEmit, after `^build` + `generate`), `dev` (`tsx watch ./src/index.ts`), `test` (`vitest run`), `test:unit` (`vitest run --project unit`), `test:docker` (`./docker/test/run.sh`), `docker` (`docker build -f docker/Dockerfile -t tereo .`, after `build`), `clean` |
| `@tereo-io/sdk` | `build`, `check` (both after `^build`), `test` (`vitest run`), `test:docker`, `clean` |
| `tereo-ui` | `build` (`vite build` → `dist/`, base `/`), `check`, `dev` (`vite`, :4000), `clean` |

The Nx `dev` target starts core **without** the telemetry `--import`; prefer
`npm run dev` in `packages/tereo`, which loads
`src/telemetry/register.ts` first.

## `packages/tereo` npm scripts

| Script | Runs |
|--------|------|
| `dev` | `tsx watch --import ./src/telemetry/register.ts src/index.ts` |
| `test` | `../../docker/test/run.sh` — the **Docker** suite, not local vitest |
| `test:unit` / `test:int` | `vitest run --project unit` / `--project int` |
| `test:local` | `vitest run` (both projects) |
| `test:watch` / `test:coverage` | `vitest` / `vitest run --coverage` |
| `test:logs` / `test:clean` | `docker/test/run.sh logs -f runner` / `docker/test/run.sh down -v` |
| `db:generate`, `db:migrate:deploy`, `db:seed`, `db:studio` | `prisma generate`, `prisma migrate deploy`, `tsx src/scripts/seed.ts`, `prisma studio` |
| `db:migrate` | `prisma migrate dev --create-only` — creates a migration, doesn't apply it |
| `openapi:lint` / `openapi:build` | `redocly lint` / `redocly lint && redocly bundle`, over the one spec in `redocly.yaml` (`openapi/openapi.yaml` → `openapi/bundled-openapi.yaml`) |

## When to Use What

### Starting development

```sh
npm install
docker compose up -d postgres redis                      # host ports 5442 / 6389
cp packages/tereo/.env.example packages/tereo/.env   # no keys needed
cd packages/tereo
npx prisma generate && npx prisma migrate deploy && npx tsx src/scripts/seed.ts
npm run dev                                              # http://localhost:4001
```

- **Just want it running**: `docker compose up` from the root. It builds the
  image from source, runs the `migrate` service (`docker/migrate-and-seed.sh`:
  `prisma migrate deploy` + seed), then starts `core` on 4001. No `.env` needed.
  The image carries the admin UI: core serves it at http://localhost:4001
  (`/` redirects there), and compose sets `UI_BASE_URL` to match. The image is
  only built when missing — use `docker compose up --build` after code changes.
- **Admin UI in development**: `npm run dev` in `packages/tereo-ui`
  (`cp .env.example .env.development.local` first) → http://localhost:4000,
  calling core on :4001 cross-origin. Core's `UI_BASE_URL` defaults to :4000
  outside production, so consent/login redirects, CORS and the login client's
  redirect URI already point there.
- **Core serves whatever UI build it finds** at `UI_DIST_PATH` (default
  `packages/tereo-ui/dist`); with none it logs `Admin UI build not
  found` and serves the API alone. To log in through `:4001` from
  `npm run dev`, set `UI_BASE_URL=http://localhost:4001` in `.env` and
  re-run the seed, which adds that redirect URI to the login client.
- Host ports are overridable: `CORE_POSTGRES_PORT` (5442), `CORE_REDIS_PORT`
  (6389), `CORE_PORT` (4001).
- Keys come from env if set, otherwise from `core.secrets`, generated on first
  start. Nothing to fill in.

### First-boot setup

Until an admin exists, every start of core logs a fresh one-time setup token
(valid 24h) — `Core is not set up. Complete setup at …/setup with this token: …`.
Restarting core prints a new one.

```sh
docker compose logs core | grep "not set up"     # Docker; with npm run dev it's in the terminal
curl http://localhost:4001/v1/setup/status
curl -X POST http://localhost:4001/v1/setup -H 'Content-Type: application/json' -d '{
  "token": "7QK4-M2XD-9PWA",
  "admin": { "email": "you@example.com", "name": "You", "password": "Choose-a-long-one-1" },
  "organization": { "name": "Acme", "slug": "acme", "code": "ACME" }
}'
```

`POST /v1/setup` returns 404 once setup is done. The seed creates no person; the
first admin always comes from setup.

### Running tests

- `npm run test:int` (in `packages/tereo`) reads `.env` and points it at
  a separate database and Redis db: `DATABASE_URL` with `_test` appended to the
  database name, and Redis db `1`. `TEST_DATABASE_URL` / `TEST_REDIS_URL` (shell
  or `.env`) override them, and `TEST_PORT` moves the server. `globalSetup` migrates and seeds that
  database itself. `npm run test:unit` needs no `.env`, database or Redis.
- The `int` project starts its **own server on port 4001** — stop `npm run dev` or the
  compose `core` container first.
- `int` files run serially (shared server and database); expect a few minutes. Where a test
  goes and how it is tagged: `packages/tereo/src/tests/README.md`.
- `docker/test/run.sh` needs only Docker: it builds a runner, splits the suite
  into `TEST_SHARDS` shards (default 4) run at once, each in its own throwaway
  stack (`TEST_STACK_PREFIX` names them), and tears them down. Compose args pass through to every shard's
  stack, e.g. `docker/test/run.sh logs -f runner`.
- SDK tests: `npx nx run @tereo-io/sdk:test`.

### After Prisma schema changes

1. Edit `packages/tereo/prisma/schema.prisma`.
2. `npm run db:migrate -- --name <what_changed>` — generates the
   migration under `prisma/migrations/` without applying it.
3. Edit the generated SQL only where Prisma can't express something: append raw
   SQL for range partitioning, partial/opclass indexes and CHECK constraints. On
   the partitioned tables (`audit_log_entries`, `webhook_deliveries`) delete the
   PK-reset statement Prisma emits — only that statement.
4. `npm run db:migrate:deploy`, then `npx prisma generate` if the client didn't
   regenerate.
5. Re-run the seed if the change touches seeded rows. The test database is
   migrated by `globalSetup` on the next `npm run test:int`.

### After changing permissions, roles, buckets or event types

Nothing to run. They're declared in `packages/tereo/src/definitions/`
and registered by `registerCore()` on every start — restart core (`npm run dev`
picks it up on save). Removing one there retires it a day later.

### Before creating a PR

The same checks CI runs:

1. `npm run format` (then `npm run format:check`)
2. `npm run sort-imports` (then `npm run sort-imports:check`)
3. `npm run lint`
4. `npm run check`
5. `npm run openapi:lint` in `packages/tereo` if a spec changed
   (`npm run openapi:build` to re-bundle)
6. `npm run test:unit` and the focused `int` tests in `packages/tereo` (or `docker/test/run.sh`), plus
   `npx nx run @tereo-io/sdk:test` if the SDK changed
7. `npm run version-plan` if `@tereo-io/sdk`, `tereo` or `tereo-ui` changed — commit the file in
   `.nx/version-plans/`.

### Docker management

| Command | Purpose |
|---------|---------|
| `docker compose up -d postgres redis` | Backing services for `npm run dev` |
| `docker compose up` / `docker compose up --build` | Whole stack / rebuild the image first |
| `docker compose logs -f core` | Tail core |
| `docker compose down` | Stop, keep data |
| `docker compose down -v` | Stop **and delete** the database, its generated keys, and stored files — ask first |
| `npx nx run tereo:docker` | Build the image tagged `tereo` (compose uses its own `tereo:local`). It builds the admin UI too |

### Troubleshooting

- `.env not found at …` from vitest → copy `.env.example` to `.env` in
  `packages/tereo`.
- `EADDRINUSE` on port 4001 in tests → a dev server or the compose `core` container is
  still running.
- Login from the UI fails with an invalid `redirect_uri` → the UI sends
  `${origin}/callback` (built) or `http://localhost:4000/callback` (dev
  server), and the login client only accepts `${UI_BASE_URL}/callback` for the
  `UI_BASE_URL` the seed last ran with. Set `UI_BASE_URL` and re-run the seed.
- Prisma client out of date (missing model/field types) → `npx prisma generate`.
- Lost the setup token → restart core; each start logs a new one while setup is
  pending.

## Prisma and destructive database commands

Prisma detects when an AI agent runs it and refuses destructive commands —
`prisma migrate reset`, `prisma db push --force-reset`,
`prisma db push --accept-data-loss` — with a message telling the agent to stop
and ask. The override is the `PRISMA_USER_CONSENT_FOR_DANGEROUS_AI_ACTION` env
var.

**Never set that variable on your own judgment, and never work around the
guard** — no `DROP SCHEMA` through `psql`, no `docker compose down -v` to get the
same effect. Stop and tell the user the exact command, why you want it, that it
irreversibly destroys the data, and which database it would hit (`core` dev data
or `core_test`). Only if the user then explicitly consents in their own reply may
the command be rerun with the variable set, as Prisma's message describes. The
test database rarely needs resetting — `docker/test/run.sh` gives a throwaway
one.

## DO

- Run Prisma, the seed and vitest from `packages/tereo` (Prisma reads
  `DATABASE_URL` from `.env` there via `prisma.config.ts`).
- Generate migrations with `npm run db:migrate` (`--create-only`) and review the
  SQL before applying.
- Run the CI checks before pushing.

## DON'T

- Don't run `npm test` in `packages/tereo` expecting local vitest — it's
  the Docker suite; use `npm run test:unit` / `test:int`.
- Don't point tests at the dev database; `TEST_DATABASE_URL` exists to move the
  test database, not to share one.
- Don't run `prisma migrate reset`, `db push --force-reset` or
  `docker compose down -v` without the user's say-so.
