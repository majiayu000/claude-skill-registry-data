---
name: add-app
description: Add a new deployable service or app to the monorepo (a NestJS worker or service, a Python service, a new client), wired into local dev, the database roles, images, the charts, CI and the docs. Use when work needs its own process that scales or fails separately, not just a module in an existing service.
argument-hint: <name>
disable-model-invocation: true
---

# Add an app or service

A new deployable is expensive to run and to keep: first check whether a module in an
existing service does the job (a queue consumer in apps/worker, a module in apps/api).
Services never import each other; they share `packages/*` and talk through the API
contract, queues and events. This is the checklist for a NestJS service `apps/<name>`;
apps/worker is the one to copy.

## The code

1. `apps/<name>/`: copy `apps/worker`'s `package.json` (name `@repo/<name>`, the same
   scripts), `tsconfig.json`, `tsdown.config.ts`, `vitest.config.ts`, `src/main.ts`,
   `src/telemetry.ts`, `src/app.module.ts`, `src/env.ts` (with `databaseEnv("<NAME>")`
   if it uses Postgres), and a `CLAUDE.md` (commands, where things are, gotchas). Give it
   the next free port (3005 and up) as `PORT: port(<n>)`, and `/health/live`,
   `/health/ready` and `/health/dependencies` through `HealthModule` from
   `@repo/nest-common`.
2. `bun install` to link it. Its integration tests take the next free Valkey database
   number (docs/testing.md lists them) and flush it with `flushTestDatabase`;
   `scripts/redis-databases.test.ts` fails if two suites share one.

## Its database role, if it uses Postgres

3. `app_<name>` in `infra/postgres/init/01-roles-and-databases.sql` (login,
   `NOBYPASSRLS NOINHERIT`, `CONNECT` on `app` and `app_test`), in `roles` in
   `deploy/charts/data/values.yaml`, in `ROLE_PASSWORDS` in
   `packages/db/src/testing/index.ts`, and in the doctor's role count
   (`scripts/doctor.ts`). Grants in a migration (the db-change skill), and
   `<NAME>_DATABASE_URL` in `.env.example`. An existing local volume needs the roles
   script rerun: the doctor says how.

## Local development

4. The root `package.json` `dev` script lists the core services with `--filter`: add
   `@repo/<name>` if it's core; `dev:full` runs every package's `dev` anyway. Add it to
   `SERVICES` in `scripts/e2e.ts` if end-to-end tests need it.

## Images, charts and CI

5. The image: `docker-bake.hcl` (`node-service`'s `matrix.service` and the `default`
   group), and the image lists in `.github/workflows/deploy.yml`, `preview.yml` and
   `ci.yml`'s images job (workflow changes: say so, the user decides).
6. The chart: an entry under `services` in `deploy/charts/stack/values.yaml` (image,
   port, `database: { role, envPrefix }`, `redis`, probes, `env`, `keda.queues` for its
   queues), a test in `deploy/charts/stack/tests/`, and a Secret
   `boilerplate-<name>` per environment if it has secrets (templates in
   docs/new-project.md). `bun run charts:check`.
7. Commit scopes need nothing: `commitlint.config.ts` reads the workspace folders.
   knip: an `entry` for `src/main.ts` and `src/telemetry.ts` in `knip.jsonc`, like the
   other workers.

## Docs

8. The README's "What's inside", the table in `docs/architecture.md`, the layout and
   port list in `CLAUDE.md`, and `docs/environment.md` for its variables (the `docs-sync`
   agent checks them).

A Python service copies `apps/ai` instead (its `pyproject.toml`, `deploy/docker/
ai.Dockerfile`, the `python` CI job). A new client app copies `apps/web` or `apps/mobile`
and talks to the API only through `packages/client`.

## Done when

- `bun run lint` (the boundary rules see the new app), `bun run check-types`,
  `bun run test`, `bun run test:integration` pass.
- `bun dev` starts it (in the background) and `curl localhost:<port>/health/dependencies`
  answers 200 (it's up and reaches its database and Redis).
- `bun run charts:check` passes, and `docker buildx bake <name>` builds.
- The `reviewer` agent, and `migration-reviewer` for its grants, report nothing blocking.
