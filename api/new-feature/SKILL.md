---
name: new-feature
description: End-to-end checklist for adding a feature to tereo — declaration, schema, routes, audit and events, OpenAPI, tests, docs, SDK and UI
disable-model-invocation: true
argument-hint: "<feature-name> [area: auth|files|webhooks|audit|registry]"
---

# New Feature Checklist

End-to-end guide for adding **$ARGUMENTS** to tereo.

Core is one service, `packages/tereo` (port 4001), with one Postgres
database and a schema per area (`auth`, `files`, `webhooks`, `audit`, plus `core`).
All paths below are relative to `packages/tereo` unless they start with
`packages/`. Commands are in the `dev` skill.

## Step 1: Declaration (`src/definitions/`)

Core's permissions, system roles, buckets and event types are **declared, not
seeded**: `CORE_DECLARATION` (`definitions/declaration.ts`) is registered by
`registerCore()` on every start. Removing an item retires it a day later. Admins
never create permissions or edit system roles.

- [ ] Permissions → `definitions/permissions.ts`
  - Add a group with `domainPermissions(domain, displayName, description, actions?)`
    (generates `domain.read|write|delete|admin`; pass a subset, or include
    `archive`), or explicit entries for one-off names (`services.approve`,
    `webhooks.emit`)
  - Spread the group into `PERMISSION_CATALOG`
  - Add constants to `PERMISSIONS` if call sites use them
  - Hierarchy: `write` includes `read`, `delete` includes `write`, `admin`
    includes all
- [ ] System roles → `definitions/roles.ts` (`ROLES`) — only if an existing role
      (`admin`, `platform_admin`, the `*_admin` roles) shouldn't simply cover it
- [ ] Buckets core itself writes → `definitions/buckets.ts` (`BUCKETS`)
- [ ] Webhook event types → `definitions/eventTypes.ts` (`EVENT_TYPES`), format
      `<area>.<resource>.<verb>` (e.g. `auth.organization.created`). `emitTx`
      throws on any event type not listed here
- [ ] Never declare under a namespace an app service owns — app services declare
      their own in provisioning documents (`docs/provisioning.md`)

## Step 2: Database model (`prisma/schema.prisma`)

- [ ] Add the model under its area's section, with `@@schema("<area>")` and
      `@@map("snake_case_table")`; columns get `@map("snake_case")`
  - `id String @id @default(uuid(7)) @db.Uuid`
  - `organizationId String @map("organization_id") @db.Uuid` with a relation to
    `Organization` (`onDelete: Restrict`) when the row is tenant-scoped
  - Every "who" column (`createdBy`, `userId`, …) is `@db.Uuid` with a relation
    to `User` (`onDelete: Restrict`). Clients act as their service-account user;
    core acts as `SYSTEM_USER_ID` (`definitions/systemUser.ts`)
  - `createdAt DateTime @default(now()) @map("created_at")`,
    `updatedAt DateTime @updatedAt @map("updated_at")`
  - Things that are retired get `archivedAt DateTime? @map("archived_at")` —
    users and organizations are deactivated or archived, never deleted
  - `@@index` the foreign keys and the columns lists filter on
- [ ] `npx prisma migrate dev --create-only --name <name>`
- [ ] Append raw SQL only for what Prisma can't express — range partitioning,
      partial and opclass indexes, CHECK constraints. On `audit_log_entries` /
      `webhook_deliveries`, delete only the PK-reset statement Prisma emits
- [ ] Raw SQL anywhere names tables with their schema (`"files"."objects"`) —
      there is no `public` schema
- [ ] `npx prisma migrate deploy`, `npx prisma generate`
- [ ] DB functions in `src/utils/db/<resource>.ts` (get, getPaginated, create,
      update, …), each taking an optional `tx?: Prisma.TransactionClient`; add the
      module to the default export in `src/utils/db/index.ts`. Throw
      `NotFoundError` etc. from `src/utils/errors.ts` here, as
      `utils/db/organizations.ts` does
- [ ] Seed data, if any, goes in `src/scripts/seed.ts` and must stay idempotent

## Step 3: Routes (`src/routes/`)

The folder tree mirrors the URL: the protocol endpoints at the root (`oauth/`, `well-known/`,
wired in `routes/index.ts`); everything else is core's API under `v1/` (`v1/account/`, `v1/admin/`,
`v1/setup/`, `v1/files/`, `v1/webhooks/`, `v1/audit/`), wired in
`routes/v1/index.ts`. A new API route goes under `routes/v1/`. Follow the `routes` skill for
where each file goes and the registration order — `tests/conventions/routeLayout.unit.test.ts` enforces the layout.

- [ ] `routes/<…>/<resources>/schemas.ts` — Zod schemas: create/update bodies,
      `:id` params, and the list query via `createCursorQuerySchema()` from
      `utils/parseQueryString.ts`
- [ ] `routes/<…>/<resources>/controllers.ts` — handlers
  - `validateBody/validateParams/validateQuery` from `utils/validateReq.ts`
  - `validateUser(req)` from `middleware/auth.ts` for the caller
  - Call `db.<resource>.*`, not Prisma directly
  - Throw the error classes from `utils/errors.ts` — never
    `res.status(400).json(...)`
  - Lists: `applyCursorToWhere` + `buildCursorPageResponse` from
    `utils/cursor.ts`; shape responses with a `format*` function in
    `utils/transformers.ts`
- [ ] `routes/<…>/<resources>/index.ts` — the router. Item routes go in a
      singular subfolder (`<resource>/index.ts`, `Router({ mergeParams: true })`)
      mounted with `router.use("/:id", …)`; see `routes/v1/admin/services/`
  - `requireAuth` on the parent router (`admin/`, `files/`, `webhooks/`,
    and `audit/` index files already apply it)
  - `requirePermission("<name>")` on every route
- [ ] Mount the router in its parent `index.ts`
- [ ] ESM: `.js` on every relative import, directory imports included
      (`./services/index.js`)
- [ ] Imports sorted by the repo rule — `npm run sort-imports`

## Step 4: Audit and webhooks — in the transaction

- [ ] Wrap each mutation in `db.$transaction(async (tx) => { … })`
- [ ] `logAuditTx(tx, { auth, organizationId, action, entityType, entityId, entityName, changes?, metadata? })`
      from `utils/outbox.ts` — `action` is `CREATE | UPDATE | DELETE | MERGE | ARCHIVE | RESTORE`
- [ ] For updates, `computeChanges(old, new)` (same file) for `changes`
- [ ] `emitTx(tx, { organizationId, eventType, entityType, entityId, data })` —
      writes `core.outbox`; the worker's reaper fans it out after commit
- [ ] Both commit or roll back with the business write. No fire-and-forget calls
      for anything that must happen

Pattern: `routes/v1/admin/organizations/controllers.ts` (`createOrganization`).

## Step 5: OpenAPI (`openapi/`)

One spec covers every area; files are split by area (`auth`, `files`, `webhooks`, `audit`).

- [ ] Path file: `openapi/paths/<area>/<resource>.yaml` (admin auth routes live in
      `openapi/paths/auth/admin/`), keyed by the full path including the mount
      (`/v1/files/buckets/{name}`, `/v1/webhooks/webhooks`)
- [ ] Schemas: `openapi/components/<area>/schemas.yaml` (shared responses, parameters and
      headers are in `openapi/components/*.yaml`)
- [ ] Reference the path in the root `openapi/openapi.yaml`, and tag it with a tag from that
      area's `x-tagGroups` entry
- [ ] Every operation declares `security` — the root's `BearerAuth` applies to any that
      doesn't, so a public one must say `security: []`
- [ ] Lint and re-bundle from `packages/tereo`: `npm run openapi:build`

## Step 6: Tests (`src/tests/routes/<URL path>/`)

One suite against one server; `globalSetup` migrates and seeds `<db>_test`.

- [ ] `src/tests/routes/<URL path>/<folder>.test.ts`, plus `.validation.unit` and `.permissions` files as
      `src/tests/README.md` says; tags one per line
- [ ] Real users and tokens — no test-mode shortcut:
      `getTestPrincipalToken({ permissions: [...], organizationId?, userId? })`
      from `tests/support/principals.ts`; area helpers in
      `tests/support/<area>.ts`
- [ ] Permissions, roles and event types a test needs that aren't core's: make
      them under the test service (`ensurePermission`, `TEST_SERVICE_ID` from
      `tests/support/testService.ts`), never under core — core's declaration would
      retire them
- [ ] Cover: create, read, update, delete/archive, list with cursor pagination
- [ ] Cover: 403 without the permission, 400 on bad input, 404 on unknown ids
- [ ] Assert the audit entry and the outbox row where the mutation writes them
- [ ] Clean up what the file creates (`afterAll`, or the area's
      `cleanupAllTestEntities`)

## Step 7: SDK (`packages/tereo-sdk`) — if app services need it

- [ ] Request in `src/requests/<area>/<resource>/index.ts` using
      `tryHandleRequest` with `CORE_CLIENT` (see
      `requests/auth/organizations/index.ts`); export it from the area's `index.ts`
- [ ] Types in `src/requests/<area>/types.ts` or `src/types/<area>.ts`
- [ ] Method on the area client in `src/clients/<area>.ts`, reachable from
      `createCoreClient` (`src/coreClient.ts`)
- [ ] Tests in `src/tests/`
- [ ] `npm run version-plan` — the SDK is a released library

## Step 8: UI

The admin app is `packages/tereo-ui` (Vite + React):

- [ ] Build any screen from [`@kosmeo-ui/react`](https://github.com/kosmeo-ui/kosmeo-ui) primitives (`Page`,
      `InfiniteScroll` + `useInfiniteCursor`, `Modal`, `BorderedSection`,
      `DetailField`)
- [ ] A missing primitive goes into `@kosmeo-ui/react` upstream, not a one-off here
- [ ] Put the screen in its feature folder (`src/features/<area>/`), export what other features need
      from the feature's `index.ts`, and add its route under `src/app/routes/`
- [ ] Gate it on the permission the API requires, as the existing sidebars and routes do

## Step 9: Documentation

- [ ] `packages/tereo/docs/<area>.md` (`auth`, `files`, `webhooks`,
      `audit`, `registry`, `telemetry`) — new resource, endpoints, permissions,
      events
- [ ] Root `CLAUDE.md` / `README.md` if layout, conventions or the "Current state"
      section changed

## Step 10: Finalize

- [ ] `npm run format` and `npm run sort-imports`
- [ ] `npm run lint` and `npm run check`
- [ ] `npm run test:unit` plus the feature's own `int` files in `packages/tereo` (the full suite runs
      in CI, or once at the end with `docker/test/run.sh`);
      `npx nx run @tereo-io/sdk:test` if the SDK changed
- [ ] `npm run version-plan` if `@tereo-io/sdk`, `tereo` or `tereo-ui` changed
