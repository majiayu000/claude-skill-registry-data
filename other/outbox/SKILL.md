---
name: outbox
description: Transactional audit entries and webhook events — core's own `logAuditTx`/`emitTx` and the `core.outbox` that app services get from @tereo-io/sdk. Use when writing an audit entry or emitting a webhook event from a mutation, adding an event type, touching the outbox reaper, or wiring the outbox into an app service.
paths:
  - packages/tereo/src/routes/**
  - packages/tereo/src/jobs/**
  - packages/tereo/src/utils/outbox.ts
  - packages/tereo/src/utils/registry.ts
  - packages/tereo/src/worker.ts
  - packages/tereo/src/definitions/eventTypes.ts
  - packages/tereo-sdk/src/clients/outbox.ts
  - packages/tereo-sdk/src/utils/outboxSchema.ts
  - packages/tereo-sdk/src/types/outbox.ts
  - packages/tereo-sdk/src/coreClient.ts
---

# Transactional Outbox — Audit Entries + Webhook Events

There are **two outboxes**, one on each side of core's API. Both give the same guarantee: the audit
entry or event exists exactly when the business write commits, and not at all when it rolls back.

| | Inside core | In an app service |
|---|---|---|
| Code | `packages/tereo/src/utils/outbox.ts` | `@tereo-io/sdk` — `src/clients/outbox.ts` |
| Write an audit entry | `logAuditTx(tx, …)` — inserts into `audit.audit_log_entries` directly | `core.outbox.audit(tx, …)` — outbox row, `destination = "audit"` |
| Emit a webhook event | `emitTx(tx, …)` — row in `core.outbox`, `destination = "webhook"` | `core.outbox.emit(tx, …)` — outbox row, `destination = "webhook"` |
| Table | `core.outbox` (Prisma model `Outbox`) | the app's own, default `core_outbox`, created by the app's migration |
| Reaper | `createOutboxReaper` in `worker.ts` (`ROLE=worker` or `all`) | `OutboxClient`, started by `core.start()` |
| Dispatch | in-process: `emitWithIdempotency` (`utils/processEvent.ts`) | HTTP to core: `audit.logAsync` / `webhooks.emitAsync` |
| Event types | `definitions/eventTypes.ts` | the service's provisioning document (`service.eventTypes`) |

There is no separate outbox package here, no `outboxClient.ts`, and no
`initializeOutbox`.

## Mental model

1. **Inside a Prisma transaction**, make the business write and record the entry or event on the same
   `tx`.
2. **Post-commit**, a reaper claims due rows with `FOR UPDATE SKIP LOCKED`, dispatches each, and
   **deletes the row on success**. Failures back off; after `maxAttempts` the row is
   **dead-lettered and kept** for replay.
3. **The outbox row id is the idempotency key**, injected by the reaper at dispatch. A retry after a
   crash between dispatch and delete is deduplicated by core.

Core writes audit entries directly because `audit` is a schema in the same database — no outbox
needed. Webhook fan-out enqueues BullMQ jobs in Redis, which cannot join a Postgres transaction, so
events go through `core.outbox`. An app service's database is not core's, so both go through its
outbox.

---

# Part 1 — Inside core

## Call-site pattern (controllers)

```typescript
// packages/tereo/src/routes/v1/admin/things/thing/controllers.ts
import { getDefaultOrganizationId } from "../../../../utils/defaultOrganization.js";
import { validateBody, validateParams } from "../../../../utils/validateReq.js";
import { validateUser } from "../../../../utils/auth.js";
import { ThingIdParamSchema } from "../schemas.js";
import type { Request, Response } from "express";
import { UpdateThingSchema } from "./schemas.js";
import db from "../../../../utils/db/index.js";
import {
  computeChanges,
  emitTx,
  logAuditTx,
} from "../../../../utils/outbox.js";


export const updateThing = async (req: Request, res: Response) => {
  const auth = validateUser(req);
  const params = validateParams(ThingIdParamSchema, req);
  const body = validateBody(UpdateThingSchema, req);

  const existing = await db.things.get(params.id);

  const updated = await db.$transaction(async (tx) => {
    await db.things.update(params.id, body, tx);
    const next = await db.things.get(params.id, tx);

    await logAuditTx(tx, {
      auth,
      action: "UPDATE",
      entityType: "Thing",
      entityId: next.id,
      entityName: next.name,
      changes: computeChanges(existing, next),
    });

    await emitTx(tx, {
      organizationId: getDefaultOrganizationId(),
      eventType: "auth.thing.updated",
      entityType: "Thing",
      entityId: next.id,
      data: { id: next.id, name: next.name },
    });

    return next;
  });

  res.json(updated);
};
```

`routes/v1/admin/roles/role/controllers.ts` (`updateRole`) is the real version of this.

**Boundary rule**: controllers open transactions with `db.$transaction` from `utils/db/index.ts` —
every controller in `src/routes/` does; none calls `prisma.$transaction`. Mutation helpers in
`utils/db/{model}.ts` take an optional trailing `tx?: Prisma.TransactionClient`.

**Which organization**: org-scoped resources use their own org. A bucket's events spread
`bucketEventScope(bucket)` (`utils/outbox.ts`): its organization, or for a bucket outside any
(an app service's) `organizationId: null` plus the bucket's `serviceId`, which fans out only to
endpoints of all organizations and that service's endpoints. Never skip an emit because a bucket
has no organization. System-wide ones — organizations, roles, clients, services, registrations — use
`getDefaultOrganizationId()` from `utils/defaultOrganization.ts`, cached at startup so it is
synchronous.

**Background jobs and unauthenticated paths** act as the system user:
`auth: { userId: SYSTEM_USER_ID, email: null }` (`definitions/systemUser.ts`) — see
`routes/v1/files/signed/objects/bucket/by-id/object/controllers.ts`, `jobs/webhookDelivery.ts`, `utils/processEvent.ts`.

## logAuditTx input

`AuditLogInput`:

| Field            | Required | Notes                                                                                    |
| ---------------- | -------- | ---------------------------------------------------------------------------------------- |
| `auth`           | yes      | `{ userId, email }` — usually `validateUser(req)`; `userId` is a FK into `auth.users`     |
| `action`         | yes      | `"CREATE" \| "UPDATE" \| "DELETE" \| "MERGE" \| "ARCHIVE" \| "RESTORE"`                    |
| `entityType`     | yes      | The model name, e.g. `"Role"`                                                            |
| `entityId`       | yes      | Id of the affected row                                                                   |
| `organizationId` | no       | Defaults to null                                                                         |
| `entityName`     | no       | Human-readable label                                                                     |
| `changes`        | no       | `computeChanges(existing, next)` for UPDATE                                              |
| `metadata`       | no       | Free-form JSON                                                                           |
| `correlationId`  | no       | Defaults to the current request id (`getRequestId()`)                                    |

Set by `logAuditTx`, not the caller: `source = "tereo"` (`SOURCE`), `ipAddress` from the
request context (null outside a request), and `writerUserId = SYSTEM_USER_ID` — the entry was written
in-process, not through the audit API.

## emitTx input

`EmitTxInput`:

| Field            | Required | Notes                                                                                      |
| ---------------- | -------- | ------------------------------------------------------------------------------------------ |
| `organizationId` | yes      | Tenant scope — see *Which organization* above; null for a resource outside any             |
| `serviceId`      | no       | With a null organization: the service whose resource it is (its endpoints get the event)   |
| `eventType`      | yes      | Must be listed in `definitions/eventTypes.ts`                                              |
| `entityType`     | yes      | The model name                                                                             |
| `entityId`       | yes      | Id of the affected row                                                                     |
| `data`           | yes      | The payload subscribers receive                                                            |

**`eventType` is checked at publish time.** `emitTx` throws
`Unknown webhook event type "…" — add it to definitions/eventTypes.ts` before writing the row, so a
typo fails the request instead of dead-lettering later.

There is no `idempotencyKey` field on either input: the reaper uses the row id.

`emitTx` also captures the active W3C trace context (`traceparent`/`tracestate`) on the row; the
reaper dispatches under it, so the delivery chains off the request that caused it.

## Two key invariants

1. **Inside the transaction**: `logAuditTx` and `emitTx` write to the same `tx` as the business write,
   so they commit or roll back together. Call them last, just before returning from the callback.
2. **Outside the transaction**: side effects with no database write — WebSocket notifications
   (`websocket/emitters/`) — run after `db.$transaction` resolves. `updateRole` is the example.

## Adding a new event type

1. Add `{ eventType, description }` to the right group in `definitions/eventTypes.ts` (`authEvents`,
   `fileEvents`, `webhookEvents`, `serviceEvents`). Existing prefixes: `auth.`, `file-service.`,
   `webhook.`, `core.service.`.
2. Use it in `emitTx({ eventType: "…" })`.
3. That is all: `EVENT_TYPES` is part of `CORE_DECLARATION`, registered by `registerCore()` on every
   start, which is what makes it subscribable and lets `processEvent` accept it. Removing one there
   retires it a day later — don't remove a type subscribers rely on without saying so.

If the API docs should list it, add a webhook definition to the OpenAPI spec under `webhooks:` (see the
`openapi` skill).

## Reaper behavior (core)

`createOutboxReaper(options)` in `utils/outbox.ts`, started by `startWorker()` in `worker.ts` — so
only in processes with `ROLE=worker` or `ROLE=all`. It registers one dispatcher, `webhook` (`dispatchOutboxEvent`), which
parses the payload with `emitEventSchema` and calls `emitWithIdempotency({ ...event, idempotencyKey: row.id })`.

| Option | Default |
|---|---|
| `pollIntervalMs` | 1000 |
| `batchSize` | 100 |
| `maxAttempts` | 100 (≈ 12 hours of retry runway) |
| `retryBaseMs` | 2000 |
| `maxBackoffMs` | 30 min |
| `claimTtlMs` | 60 s — a claim older than this may be re-claimed |

- Claims with `UPDATE … WHERE id IN (SELECT … FOR UPDATE SKIP LOCKED) RETURNING`, so any number of
  workers can run one.
- Dispatches the claimed batch **in parallel** (`Promise.all`).
- Success → `DELETE`. Failure → exponential backoff with full jitter.
- A dispatcher throws `PermanentDispatchError` for a row that can never succeed; it is
  dead-lettered at once. Core's `webhook` dispatcher (`dispatchOutboxEvent` in
  `utils/processEvent.ts`) does so for a malformed payload and for a 4xx `AppError` other than
  409/429 (an unregistered or retired event type).
- A row with no dispatcher, or past `maxAttempts`, is **dead-lettered**: a structured
  `outbox.dead_letter` error log, and the row stays with `dead_lettered_at` set.
- **Replay**: clear `dead_lettered_at`, set `attempts = 0` and `next_attempt_at = NOW()`.

## Delivery semantics (core)

- **At-least-once, deduplicated.** `emitWithIdempotency` keys on
  `(caller, organizationId, eventType, idempotencyKey)` in Redis — the caller is the system user
  for the reaper — for 24 hours, so a re-dispatched row creates no second set of deliveries. The
  claim on a key in progress lasts 60 s, so a worker that dies mid-dispatch doesn't strand the row.
- **Unordered.** A batch dispatches in parallel, so a `created` and an `updated` for the same entity
  can fan out in either order. Subscribers should tolerate reordering.
- **`correlationId` asymmetry.** `logAuditTx` fills `correlationId` from the request id; events carry
  none. Put it in `data` if a subscriber needs it.

---

# Part 2 — In an app service (`@tereo-io/sdk`)

App services never reach core's database. `core.outbox` gives them the same pattern against **their
own** database. The authority is `packages/tereo-sdk/README.md` (section *Outbox*).

## Setup

1. **Create the table** in the app's own migration. Default name `core_outbox`; `schema.table` works
   (`billing.core_outbox`). Names must be lowercase letters, digits and `_` — they are interpolated into
   SQL. Either:
   - add the `CoreOutbox` Prisma model from the SDK README (`@@map("core_outbox")`), or
   - use `outboxTableSql(table)` — the `CREATE TABLE` plus a partial index on pending rows
     (`WHERE "dead_lettered_at" IS NULL`).

   The reaper's SQL is hard-coded to these column names — do not rename them.

2. **Pass `outbox` to `createCoreClient`** and start it at boot:

```typescript
import { createCoreClient } from "@tereo-io/sdk";
import { prisma } from "./db/prisma.js";
import { Redis } from "ioredis";

export const core = createCoreClient({
  service: "product-service",
  redis: new Redis(process.env.REDIS_URL!, { maxRetriesPerRequest: null }),
  outbox: { db: prisma },
});

await core.start();
```

The event types and the roles (`webhook_publisher`, `audit_writer`) come from the service's
provisioning document, not from a call at boot:

```json
{ "version": "1.0.0", "service": { "slug": "product-service", "name": "Product",
  "secretFrom": "PRODUCT_CLIENT_SECRET",
  "access": { "roles": ["webhook_publisher", "audit_writer"] },
  "eventTypes": [{ "eventType": "product.item.created", "description": "Item created" }] } }
```

`OutboxOptions`: `db` (required — anything with `$executeRawUnsafe`/`$queryRawUnsafe`: a Prisma
client or transaction; Postgres only), `table`, `dispatch` (default true; `false` on write-only
replicas), and the same tuning knobs and defaults as core's reaper (`pollIntervalMs`, `batchSize`,
`maxAttempts`, `retryBaseMs`, `maxBackoffMs`, `claimTtlMs`).

Without the `outbox` option, reading `core.outbox` throws. `core.start()` starts the reaper;
`core.stop()` stops it.

The service needs the `audit_writer` and `webhook_publisher` roles (approved by an admin) for the
reaper's sends to succeed.

## Call-site pattern

```typescript
await prisma.$transaction(async (tx) => {
  const item = await tx.item.create({ data });
  await core.outbox.audit(tx, {
    userId,
    action: "CREATE",
    entityType: "Item",
    entityId: item.id,
  });
  await core.outbox.emit(tx, {
    organizationId,
    eventType: "product.item.created",
    entityType: "Item",
    entityId: item.id,
    data: item,
  });
});
```

- `audit(tx, entry)` takes `AuditLogEntryInput`: `userId`, `action`, `entityType`, `entityId`, and
  optionally `organizationId`, `userEmail`, `entityName`, `changes`, `metadata`, `ipAddress`,
  `correlationId`. **Nothing is filled from a request context** — pass `ipAddress` and
  `correlationId` yourself if you want them. `source` is the `service` given to `createCoreClient`.
- `emit(tx, event)` takes `EmitEventParams`: `organizationId`, `eventType`, `entityType`, `entityId`,
  `data`. It calls `webhooks.assertEventType` first, so an event type not in the declaration (or in
  `eventTypes`) throws now, not at dispatch.
- `AuditLogServiceClient.computeChanges(old, next)` (static) gives the same field diff as core's.
- Leave `idempotencyKey` out: the reaper overwrites it with the row id.

## Reaper behavior (SDK)

Same claim query, backoff, dead-lettering and replay as core's, with these differences:

- **Sequential within a batch**, oldest `next_attempt_at` first. A full batch schedules the next pass
  immediately.
- Two dispatchers, fixed: `audit` → `audit.logAsync`, `webhook` → `webhooks.emitAsync`, each with
  `idempotencyKey: row.id`. There is no extension point for other destinations.
- `processBatch()` is public — tests call it to drain the outbox deterministically.

## Delivery semantics (SDK)

- **At-least-once, deduplicated by core.** `POST /v1/audit/entries` keys on (writer user, key) and
  `POST /v1/webhooks/events` on (writer user, organization, event type, key), both in Redis for 24
  hours.
- **A permanent rejection dead-letters at once.** Core answers 400 for an audit entry whose `userId`
  or `organizationId` is not in `auth`, and for an unregistered or retired event type; any 4xx except
  401, 408, 409 (the same key still in flight) and 429 dead-letters the row on that attempt. Network
  errors and 5xx back off as usual. Watch for `outbox.dead_letter` logs.

---

## Don't

- **Don't run `logAuditTx`, `emitTx` or `core.outbox.*` outside a transaction.** If there is no
  paired write (rare), open a transaction just for the record.
- **Don't open `prisma.$transaction` in a core controller** — use `db.$transaction`.
- **Don't emit an event type that isn't declared** — core: `definitions/eventTypes.ts`; app: the
  declaration.
- **Don't use `audit.log` / `webhooks.emit` (or the `Async` variants) for state-changing writes in an
  app service.** They are best-effort and bypass the outbox; the reaper is their real caller.
- **Don't write audit entries through the HTTP API from inside core.** `logAuditTx` inserts directly.
- **Don't add audit or webhook calls to read endpoints.**

## Common gotchas

- **`utils/audit.ts` is not the audit log.** Its `authLog` writes security events (`auth_failure`,
  `token_issued`, …) to the Pino logger. Audit entries come from `logAuditTx`.
- **`webhook.test` is registered but never emitted through the outbox** — only
  `POST /v1/webhooks/webhooks/:id/test` uses it.
- **`processEvent` audits only HTTP emits** (`WebhookEvent`, one per event, under the caller). Core's
  own events write no such entry; one that reaches no endpoint is only logged at debug level.

- **`computeChanges` skips `createdAt`, `updatedAt`, `deletedAt`, `archivedAt`** and returns
  `undefined`, not `{}`, when nothing else changed. Pass it straight through.
- **The reaper runs under test too** — `NODE_ENV=test` skips only the webhook-delivery and
  partition workers. Fan-out is asynchronous, so a test polls for its effect:
  `src/tests/flows/webhooks/` (e.g. `endpointEvents.test.ts`) waits (`waitFor`) for the `WebhookDelivery` row an `emitTx` leads to.
