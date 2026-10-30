---
name: backend
description: Backend patterns for tereo — the one Express/Prisma service (auth, files, webhooks, audit). Use when creating or changing routes, controllers, Zod validation, error handling, db functions, Prisma models or migrations, permissions/roles/event types in definitions/, audit entries, or webhook events.
paths:
  - packages/tereo/src/**
  - packages/tereo/prisma/**
  - packages/tereo/openapi/**
---

# Backend Patterns

tereo is **one service** (`packages/tereo`, port 4001) with **one database** — a
Postgres schema per area (`auth`, `files`, `webhooks`, `audit`, plus `core` for the outbox, keys and
registry). Areas share one Express app, one `db` object and one env schema; nothing calls another area
over HTTP.

## Package Layout

```
packages/tereo/
├── prisma/schema.prisma          # The one schema; client generated to prisma/generated/client
├── openapi/{auth,files,webhooks,audit}/
└── src/
    ├── index.ts / app.ts / worker.ts   # Entry, Express app, background work (ROLE=all|api|worker)
    ├── preload.ts                       # First import of every entry point (loads .env)
    ├── env.ts                           # The one Zod env schema — `import env from "./env.js"`
    ├── definitions/                     # Core's declaration: permissions, roles, buckets, event types
    ├── middleware/                      # auth.ts, organizationId.ts, rateLimit.ts, accessLog.ts, …
    ├── routes/                          # Mirrors the URL (see below)
    │   └── v1/{area}/…/{resource}/
    │       ├── index.ts                 # The one router: imports and route wiring only
    │       ├── controllers.ts           # Handlers
    │       ├── schemas.ts               # Zod schemas
    │       ├── middleware.ts            # Route-local middleware (guards, multer wrappers), if any
    │       └── {item}/                  # The `/:id` sub-router (organization/, webhook/, …)
    ├── utils/
    │   ├── db/{table}.ts                # Prisma calls, one file per table group; db/index.ts = `db`
    │   ├── outbox.ts                    # logAuditTx, emitTx, computeChanges, the outbox reaper
    │   └── cursor.ts                    # applyCursorToWhere, buildCursorPageResponse
    ├── jobs/                            # BullMQ queues and workers
    └── tests/                           # Mirrors src/ (see the `test` skill and tests/README.md)
```

URL → folder: `routes/index.ts` is the root of the tree. It mounts `/health` (`routes/health/`),
core's own API under `/v1` (`routes/v1/`, composed in `routes/v1/index.ts` with each area's
body-size limit: `v1/account/`, `v1/admin/`, `v1/setup/`, `v1/files/`, `v1/webhooks/`, `v1/audit/`), the protocol endpoints at the root (`routes/oauth/`, `routes/well-known/`), and
last the admin UI, which takes every browser path outside the reserved prefixes in `utils/ui.ts`.
A new API route goes under `routes/v1/`.

## Route Layout and Registration Order

Where a route's files go, what each file holds, `:param` folders and the order routes register in
are in the `routes` skill (enforced by `tests/conventions/routeLayout.unit.test.ts`). **REQUIRED:** load it before
adding or moving a route.

## Validation

- Always Zod. `validateBody(schema, req)`, `validateParams(schema, req)`, `validateQuery(schema, req)`
  from `utils/validateReq.ts` — they throw `ValidationError` (400 `invalid_request`).
- Ids are UUIDv7: param schemas use `z.guid()` — any 8-4-4-4-12 hex id, as Postgres takes it (`z.uuid()` refuses ids outside RFC 9562's variants).
- **List endpoints are cursor-paginated**: `createCursorQuerySchema({ filters, sortFields, defaultSort })`
  from `utils/parseQueryString.ts`, then `applyCursorToWhere(query, baseWhere)` and
  `buildCursorPageResponse(result, query)` from `utils/cursor.ts` (cursors are HMAC-signed with
  `CURSOR_SIGNING_KEY_V{n}`). There is no offset pagination.
- Extra query flags (e.g. `includeArchived`) get a second schema; parse booleans with
  `z.enum(["true","false"]).transform(v => v === "true")`, never `z.coerce.boolean()`.

## Error Handling

- Throw the classes from `utils/errors.ts` — never `res.status().json()` for errors.
- `ValidationError` 400 · `BadRequestError(code, message)` 400 · `UnauthorizedError(message, code?)`
  401 · `ForbiddenError` 403 · `NotFoundError` 404 · `ConflictError(message, code?)` 409 ·
  `PreconditionFailedError` 412 · `PayloadTooLargeError` 413 · `UnprocessableEntityError(code, message)`
  422 · `TooManyRequestsError(retryAfter, message?)` 429 · `ServiceUnavailableError` 503 ·
  `OAuth2Error(error, description, status)` for OAuth/OIDC.
- Archive state: `ArchivedError` 409 `resource_archived` (changing an archived row),
  `AlreadyArchivedError` 409 `already_archived`, `NotArchivedError` 409 `not_archived`. A 404 means
  only that the row is not there or hidden. See `docs/errors.md` for the shared codes.
- Where nothing can be thrown (a stream's `error` event after the controller returned), use
  `sendError(res, err)` — same body and headers as the handler.
- Auth-specific: `InvalidTokenError` for bad/expired/revoked bearer tokens.
- Prisma constraint errors: `mapUniqueViolation(fn, msg, code)` and
  `rethrowRestrictedAsConflict(err, msg)` (`utils/prismaErrors.ts`) turn them into 409s with a
  specific message. Unmapped unique and foreign-key violations, in any of the shapes the driver
  adapter produces, reach `errorHandler` as a generic 409 `conflict`.
- `errorHandler` (last in `app.ts`, after a catch-all `NotFoundError`) answers in RFC 6749 form:
  `{ "error": "code", "error_description": "message" }`.

## Auth and Permissions

- Tokens are verified **in-process** by `requireAuth` (`middleware/auth.ts`) — signature, stored
  `access_tokens` row, revocation, session, then permissions from the user's roles. No introspection
  hop and **no test-mode shortcut**.
- `requireAuth` goes on the **area router** (`routes/v1/admin/index.ts`, `routes/v1/webhooks/index.ts`,
  `routes/v1/audit/index.ts`), followed by `rateLimitGeneral`. Areas with anonymous reads build their
  own with `createRequireAuth({ publicRoutes })` (`routes/v1/files/index.ts`); the controller still gates.
- `requirePermission(name)` goes on **each route**. Names come from `PERMISSIONS` in
  `definitions/permissions.ts` (files, webhooks, audit — `PERMISSIONS.WEBHOOKS.WRITE`,
  `PERMISSIONS.buckets.read`) or are literal for auth's admin routes (`"organizations.write"`).
- Hierarchy (`hasPermission`): `read (1) < write (2) < archive (3) < delete (4) < admin (5)`; a
  `x.admin` covers its whole subtree, and the bare `admin` permission covers everything.
- In controllers, `validateUser(req)` returns the `AuthContext`
  (`userId`, `email`, `permissions`, `organizationId`, `oauthClientId`, …).
- Finer checks are in code, not middleware: `requireOrgRole("member" | "admin" | "owner", req, orgId)`
  (`utils/orgRoleAuth.ts`) for org routes; `validateBucketAccess` / `validateBucketManagement`
  (`utils/bucketAccess.ts`) for the per-bucket grants files layer on top of permissions.

## Organization Context

- The tenant comes from the **token** (`req.auth.organizationId`), not a header.
- Webhooks: `resolveWebhookOrganizationId` sets `req.organizationId` (a `webhooks.admin` caller may
  override with `X-Organization-ID`); audit: `resolveAuditOrganizationId`. Controllers read it with
  `validateOrganizationId(req)` (`middleware/organizationId.ts`).
- Org-owned rows: load by id, then compare `row.organizationId` to the caller's and throw
  `ForbiddenError("Resource does not belong to this client")`. Lists put `organizationId` in the base
  `where` passed to `applyCursorToWhere`.

## Database Layer

- Prisma calls live in `utils/db/{table}.ts`, aggregated by `utils/db/index.ts` into one default
  export: `import db from "../../utils/db/index.js"` → `db.organizations.get(id)`.
- Controllers call `db.*`, not `prisma` (a few read-only admin aggregations are the exception).
- Every write function takes an optional transaction: `(…, tx?: Prisma.TransactionClient)` with
  `const db = tx ?? prisma;`. Controllers open `db.$transaction(async (tx) => …)`.
- `get` throws `NotFoundError`; `findById` / `getBy…` return `null` for the caller to decide.
- `getPaginated({ take, orderBy, where })` fetches `take + 1` and returns `{ data, hasMore }`.
- **Raw SQL** names the schema on every table — `"files"."objects"`, `"core"."outbox"`. There is no
  `public` schema.

## Prisma Conventions

- One `prisma/schema.prisma`; every model and enum carries `@@schema("auth" | "files" | "webhooks" |
  "audit" | "core")`. Import the client and types from `prisma/generated/client/index.js`.
- `id String @id @default(uuid(7)) @db.Uuid`; foreign keys `@db.Uuid` (`Bucket` alone keeps an
  autoincrement `Int` id).
- camelCase fields, `@map("snake_case")` columns, `@@map("table_name")` tables.
- `createdAt @default(now())`, `updatedAt @updatedAt`, both mapped.
- **Actors**: every "who" column (`createdBy`, `userId`, `writerUserId`, …) is a FK into `User` with
  `onDelete: Restrict`. Clients act as their service-account user; core acts as `SYSTEM_USER_ID`.
- **Archive, don't delete**: archivable rows have `archivedAt DateTime? @map("archived_at")` +
  `@@index([archivedAt])`; mutations on archived rows are blocked with `guardArchived` /
  `guardArchivedById`. Users and organizations are deactivated (`isActive`) or archived, never deleted.
  `deletedAt` exists only on `Bucket`, `Object` and `ObjectVersion`, where deletion is a storage
  lifecycle (cleanup jobs, delete markers) — filter `deletedAt: null` there.
- Tenant-owned models have `organizationId` with a `Restrict` relation to `Organization`.

## Migrations

- `npx prisma migrate dev --create-only --name <name>`, review, then `npx prisma migrate deploy`.
- Append raw SQL only for what Prisma can't express: range partitioning, partial/opclass indexes,
  CHECK constraints.
- On the partitioned tables (`audit_log_entries`, `webhook_deliveries`) Prisma emits a PK-reset
  statement Postgres rejects — delete only that statement.
- `src/scripts/seed.ts` is idempotent and runs after every migrate.

## Declared, Not Seeded

Core's permissions, system roles, buckets and event types are **code** in `src/definitions/`
(`CORE_DECLARATION`), registered by `registerCore()` on every start. Removing one there retires it
after `REGISTRY_RETIREMENT_GRACE_HOURS`. Admins never create permissions or edit system roles. App
services declare theirs in their provisioning documents (see `docs/provisioning.md`, `docs/registry.md`).

## Audit Entries + Webhook Events (Transactional)

Both happen **inside the mutation's transaction**, from `utils/outbox.ts`:

```typescript
const updated = await db.$transaction(async (tx) => {
  const next = await db.organizations.update(id, body, tx);
  await logAuditTx(tx, {
    auth,
    organizationId: next.id,
    action: "UPDATE",
    entityType: "Organization",
    entityId: next.id,
    entityName: next.name,
    changes: computeChanges(existing, next),
  });
  await emitTx(tx, {
    organizationId: getDefaultOrganizationId(),
    eventType: "auth.organization.updated",
    entityType: "Organization",
    entityId: next.id,
    data: formatOrganization(next) as Record<string, unknown>,
  });
  return next;
});
```

- `logAuditTx` inserts into `audit.audit_log_entries` directly (same database) — `userId` is the
  caller, `writerUserId` is `SYSTEM_USER_ID`, request id and IP come from AsyncLocalStorage.
- `emitTx` writes a `core.outbox` row; the worker's reaper fans it out to subscribed endpoints after
  commit, using the row id as the idempotency key. Don't pass one.
- `emitTx` throws on an event type not in `definitions/eventTypes.ts` — add it there first.
  Format `{area}.{resource}.{action}`: `auth.organization.created`, `file-service.bucket.updated`,
  `core.service.declared`.
- Platform events (auth, core) are emitted under `getDefaultOrganizationId()`; tenant data
  (buckets, objects) under the owning organization.
- `action`: `CREATE | UPDATE | DELETE | MERGE | ARCHIVE | RESTORE`.

For the reaper, dead-letters and the app-service side (`core.outbox` in @tereo-io/sdk), invoke
the `outbox` skill.

## App Wiring

- `app.ts` order: `trust proxy` → `createRequestIdMiddleware()` → `helmet()` → bucket CORS
  preflights → `apiCors` (credentialed CORS on the API only) → `authRequestLog` → `routes` (`routes/index.ts`) → catch-all
  `NotFoundError` → `errorHandler`.
- `routes/index.ts`: `/.well-known`, `/health` (DB + Redis probe, 503 `degraded` on failure),
  `/oauth`, `/v1` (`routes/v1/index.ts`: `/files`, `/webhooks`, `/audit`, `/account`,
  `/admin`, `/setup`, each with its body limit — `smallBodyParsers` from
  `middleware/bodyParsers.ts` for the auth ones), then the admin UI.
- `index.ts` start order: `loadKeys()` (before anything signs, verifies or decrypts) → Redis →
  default organization → `assertSystemUser()` → `registerCore()` → worker (if `ROLE` runs it) →
  `app` imported after Redis is up.
- Background work goes in `src/jobs/`: queues from `createQueue` (with `RETRY_POLICIES` /
  `REMOVAL_POLICIES`) in `utils/bullmq.ts`, BullMQ `Worker`s in the job modules, started from
  `worker.ts`.

## Environment Variables

- One schema: `src/env.ts`; default export `env`. Add the variable there with a Zod type and default.
- Never read `process.env` elsewhere. `src/preload.ts` must be the first import of every entry point.
- Booleans with the `bool("false")` helper; numbers with `z.coerce.number()`.
- Keys (`JWT_*`, `TOTP_ENCRYPTION_KEY`, `*_SIGNING_KEY_V1`) are optional — `loadKeys()` fills them
  from `core.secrets`, generating them on first start.

## OpenAPI Spec

One spec for the whole service under `packages/tereo/openapi/` (`openapi.yaml`,
`paths/<area>/`, `components/` with `components/<area>/`, generated `bundled-openapi.yaml`). Update
it with every route change — invoke the `openapi` skill.

## Adding a Resource

1. `src/routes/v1/{area}/…/{resource}/` with `index.ts`, `schemas.ts`, `controllers.ts`, plus
   `{item}/` for the `/:id` routes (see the `routes` skill)
2. Model in `prisma/schema.prisma` (right `@@schema`), migration via `--create-only`
3. `src/utils/db/{table}.ts`, added to `utils/db/index.ts`
4. Mount the router in its parent `index.ts` (respect registration order)
5. Permissions in `definitions/permissions.ts` (`PERMISSION_CATALOG` + `PERMISSIONS`), and in
   `definitions/roles.ts` if a system role should hold them
6. Event types in `definitions/eventTypes.ts`; `logAuditTx` + `emitTx` in every mutation
7. OpenAPI paths and schemas; tests mirroring the route under `src/tests/routes/` (see the `test` skill)

## DO

- Validate every input with `validateBody/Params/Query`; throw error classes for every failure
- Keep Prisma in `utils/db/`; pass `tx` through for writes inside a transaction
- `logAuditTx` + `emitTx` inside the mutation's transaction
- `requirePermission()` on every route; scope tenant data by the caller's organization
- Archive (`archivedAt`) instead of deleting; keep actor columns as FKs into `auth.users`
- `.js` on every relative import; imports sorted longest-first (`npm run sort-imports`)
- Log with Pino, object first: `logger.info({ orgId }, "msg")`

## DON'T

- Never `res.status(400).json(...)` — throw
- Never emit or audit outside the transaction, or fire-and-forget after commit
- Never seed permissions, roles or event types — declare them in `definitions/`
- Never put `requireAuth` on individual routes — it belongs to the area router
- Never read `process.env` outside `env.ts`, or sign/verify before `loadKeys()`
- Never write raw SQL without the schema prefix
- Never use `any` — `unknown` and narrow
- Never add external API integrations (they belong in [dianemo-plugins](https://github.com/dianemo/dianemo-plugins))

## Additional Resources

- Code examples (routers, schemas, controllers, db layer, raw SQL, definitions, Prisma model, env):
  [examples.md](examples.md)
- Related skills: `routes`, `outbox`, `openapi`, `test`
- Per-area notes: `packages/tereo/docs/{auth,files,webhooks,audit,registry,telemetry}.md`
- Conventions: `CLAUDE.md`, `docs/code-style.md`
