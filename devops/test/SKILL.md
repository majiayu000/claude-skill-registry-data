---
name: test
description: Testing patterns for tereo — the Vitest suite (unit and int projects) where int runs one real server against a dedicated test database with real users and tokens, plus the SDK's unit tests. Use when writing tests, deciding where a test goes, running the suite, or debugging test failures.
paths:
  - packages/tereo/src/tests/**
  - packages/tereo/vitest.config.ts
  - packages/tereo-sdk/src/tests/**
  - docker/test/**
---

# Testing Patterns

The rules live in [`packages/tereo/src/tests/README.md`](../../../packages/tereo/src/tests/README.md):
layout, filenames, the size cap, projects, tags, what gets tested where, and a "where does my test
go" list with worked cases. `src/tests/conventions/testLayout.unit.test.ts` enforces them and names
the offending paths. Read the README first; this skill covers the parts it does not.

## Where does my test go?

`src/tests` mirrors `src/`:

| Changing | Test |
|----------|------|
| a route | `routes/<URL path>/<folder>.test.ts`, named for the router folder (`routes/v1/webhooks/webhooks/webhooks.test.ts`) |
| the root router (`routes/index.ts`) | `routes/routes.test.ts`, `routes/routes.<aspect>.test.ts` |
| an entry point | `index.test.ts`, `app.test.ts`, `worker.test.ts` |
| a Zod schema | `<base>.validation.unit.test.ts`, one `it.each` table |
| a util or module | `utils/<name>.unit.test.ts` (pure) or `.test.ts` (database, Redis) |
| a job | `jobs/<job>.test.ts` |
| a sequence across routes | `flows/<area>/<flow>.test.ts` |
| the repo's own conventions | `conventions/<name>.unit.test.ts` |

Filename form: `<base>[.<aspect>][.<method>][.unit].test.ts`. Aspects are `validation`,
`permissions`, `races`, `audit`, `limits`, `errors`; a file without one holds the main behaviour.
Split by aspect only when the main file nears the cap. A test that exercises one route belongs to
that route even if it sets up state through others. The README has the full table and five worked
cases.

Tags go at the top, one `// @module-tag` per line, in this order: the tier (`unit` or `int`), the
primary area, then any other area or detail tags. The primary area comes from `AREA_BY_PATH` in
`src/tests/setup/tags.ts` (longest prefix wins): `routes/v1/admin` is `auth` except
`routes/v1/admin/notifications` (`notifications`) and `routes/v1/admin/services` (`provisioning`).
Paths with no prefix (mostly `jobs/` and `utils/`) accept any area: pick the one the code serves.

## Running tests

```sh
cd packages/tereo
npm run test:unit                                    # unit project; no server, database or Redis
npm run test:int                                     # int project; Postgres and Redis up, own server
npm run test:local -- --tags-filter "auth && race"   # any tag expression, both projects
npx vitest --list-tags                               # the declared tags
npx vitest run src/tests/jobs/shareSweep.test.ts     # one file (add --project int)
npx vitest run -t "rotates the signing secret"       # by test name
npm run test:watch / test:coverage

docker/test/run.sh                    # repo root: isolated Docker stacks, one shard each
TEST_SHARDS=1 docker/test/run.sh      # the whole suite in one stack (default 4 shards)
TEST_STACK_PREFIX=tereo-test-x docker/test/run.sh   # distinct compose names for a concurrent run
cd packages/tereo-sdk && npx vitest run             # SDK unit tests, no server or database
```

`npm test` in the package runs `docker/test/run.sh`; CI runs `nx affected -t test:docker`.

During work, run the focused tests (the file, or a tag expression) — CI runs the full suite.

## Setup

- Local runs read `packages/tereo/.env` (`cp .env.example .env`; no keys needed). A missing `.env`
  fails `int` at startup with a clear error, while `unit` needs none. `docker/test/run.sh` needs no
  `.env` (`DOCKER_TEST=true`).
- Postgres and Redis up for `int`: `docker compose up -d postgres redis` (host ports 5442 / 6389).
- `src/tests/setup/testEnv.ts` points `int` at **`<db>_test`** and **Redis db 1**; `TEST_DATABASE_URL`,
  `TEST_REDIS_URL` and `TEST_PORT` (shell or `.env`) override, so two worktrees can run side by side.
  `NODE_ENV=test`, `LOG_LEVEL=silent`. `unit` gets an env with an unreachable database and Redis.
- `setup/globalSetup.ts` migrates and seeds the test database, registers core's declaration, seeds
  the fixtures, marks first-launch setup complete, then starts **one server** (port 4001 unless
  `TEST_PORT`) that every `int` file talks to. Stop `npm run dev` first if it holds the port.
- `int` files run serially (`fileParallelism: false`) in no promised order.
- The running server's own worker runs its sweeps and reapers mid-test. A test that needs a queue
  quiet pauses it, waits for it to be idle, and resumes it in `afterAll` (see
  `jobs/idempotencySweep.test.ts`).

## Auth in Tests

**There is no test-mode token.** Every token is a real signed JWT with a stored `access_tokens` row,
verified by `requireAuth` exactly as in production; permissions come from a role assigned to a real
user.

```typescript
const token = await getTestPrincipalToken({
  permissions: ["webhooks.write"],
  organizationId: "00000000-0000-7002-0000-000000000001", // or a label: "other-org-1"; null = no org
  userId: FIXTURE_USER_IDS[0], // optional — omit for a fresh user
});
```

- `getTestPrincipalToken` (`src/tests/support/principals.ts`) upserts the user, the organization
  (`testOrgId(label)` maps any label to a stable UUID) and a `test-perms-<hash>` role holding the
  permissions. Tokens are cached per (user, org, permissions) within a file.
- A user's permissions are the **union of their roles** — two token requests for the same user with
  different permission sets give that user both. Use a fresh user (the default) for a narrower set.
- Area helpers wrap it: `getTestAccessToken()` in `support/webhooks.ts` (`webhooks.admin`,
  org-scoped), `support/files.ts` (`file-service.admin`), `support/audit.ts` (`audit-logs.admin`).
  Auth tests log in for real with `support/auth/*`: `createAdminUser()` +
  `getAccessTokenForUser(user, client)` drive `/oauth/authorize` → `/oauth/token`.
- Fixed ids: `FIXTURE_USER_IDS`, `FIXTURE_ORGANIZATION_IDS` (created by `globalSetup`),
  `DEFAULT_ORGANIZATION_ID` and `SYSTEM_USER_ID` from `src/definitions/index.js`.
- Permissions, roles and event types a test needs that core doesn't declare are owned by the **test
  service** (`support/testService.ts`: `ensurePermission(name)`; `createTestEventType()` in
  `support/webhooks.ts`), never by core — core's declaration would retire them.
- `@tereo-io/sdk` has a `test-token-…` parser and stubs, behind `createCoreClient({ testMode: true })`,
  for **app services'** tests. Core's server accepts neither.

### Route auth is generated

`routes/routes.permissions.test.ts` walks every mounted route (`support/routeTable.ts`) and asserts
401 without a token and 403 for a token with no permissions, and that the 403 comes from a
permission gate. Routes that take no bearer token, or only a signed-in user, or are scoped to a
resource are listed with a reason in `support/routeAllowlists.ts`. It does **not** prove which
permission or level a route needs, or resource-scoped access (organization, grants, ownership). So a
new route needs no generic 401/403 test, but does need a `.permissions` test for its own rules, and
one for the permission it requires if getting that wrong would matter.

## Integration Test Pattern

```typescript
// @module-tag int
// @module-tag webhooks
import { getTestPrincipalToken } from "../../../../support/principals.js";
import { BASE_URL, HTTP_STATUS, createTestEventType } from "../../../../support/webhooks.js";
import { describe, it, expect } from "vitest";
import axios from "axios";

describe("POST /v1/webhooks/webhooks", () => {
  it("returns 403 without webhooks.write", async () => {
    const readToken = await getTestPrincipalToken({
      organizationId: "00000000-0000-7002-0000-000000000001",
      permissions: ["webhooks.read"],
    });
    const et = await createTestEventType();

    const response = await axios.post(
      `${BASE_URL}/webhooks`,
      { url: "https://example.com/hook", eventTypes: [et.eventType] },
      {
        headers: { Authorization: `Bearer ${readToken}` },
        validateStatus: () => true,
      }
    );

    expect(response.status).toBe(HTTP_STATUS.FORBIDDEN);
  });
});
```

`validateStatus: () => true` makes axios return every status so the test asserts on it; errors come
back as `{ error, error_description }`. Tags are one `// @module-tag` per line at the top.

## Asserting Side Effects

Tests may read the test database through `prisma` (`src/utils/db/prisma.js`) to check what the API
can't show. Write one test per mutation for its side effects (in `.audit` when the main file is near
the cap):

- **Audit**: `prisma.auditLogEntry.findFirst({ where: { entityId, entityType } })` →
  `action`, `source: "tereo"`, `writerUserId: SYSTEM_USER_ID`.
- **Webhook events**: subscribe an endpoint to the event type, trigger the mutation, then
  `waitFor(() => prisma.webhookDelivery.count(...) > 0)` — the outbox reaper dispatches after commit.
  The delivery worker itself is off under test, so assert that the delivery row exists, not its outcome.
- **Background jobs**: call the job's exported function directly (`processDeliveryRetention()`,
  `processEntryRetention()`), then check the rows.

## DO

- Put each test where the README says; one tier tag (`unit` or `int`, matching `.unit`) first, then
  the path's primary area tag, per file, **one `// @module-tag` per line** (several on a line drop all but the first)
- Keep every file at 800 lines or fewer; split by aspect, then method. A file that cannot fit goes in
  `conventions/oversize.ts` with a ceiling and a reason
- Put validation in `.validation.unit` tables against the route's exported Zod schema, with one 400
  case in the route's `int` file proving the schema is wired in
- Test through HTTP against the running server for anything a route does
- Get tokens from `getTestPrincipalToken` or an area's `getTestAccessToken` — never hand-craft one
- Test route-specific authorization (`.permissions`), 404 (e.g. `NON_EXISTENT_UUID`), and
  cross-organization access (403 with an `other-org-*` token); the generated test covers bare 401/403
- Put multi-route sequences in `flows/<area>/`, and a one-route test with the route
- Assert the audit entry (and webhook delivery where relevant) for new mutations
- Remove a duplicate from the more expensive tier, and list it in the commit message as
  `removed: <old file> > <test name> -> covered by <new file> > <test name>`
- Track what you create and remove it in `afterAll` (`cleanupTestEntities`); cleanup deletes through
  `prisma` because much of the API archives rather than deletes
- Add stragglers to the area's `cleanupAllTestEntities`, which `globalSetup` teardown calls
- Use unique names (`generateUniqueId()`) — the database persists across runs
- Use descriptive names: `it("returns 409 when the slug is taken by an archived organization")`
- Run the focused tests while working (the file, or `--tags-filter`); leave the full suite to CI

## DON'T

- Don't mock the database, Redis or auth — `int` hits real Postgres, Redis and `requireAuth`
- Don't import `utils/db/`, `utils/redis.ts`, `app.ts`, `index.ts`, `worker.ts`, `setup/` (except
  `tags.ts`) or `support/` (except `support/pure/`) in a `.unit` file
- Don't name a file after a bug or ticket, or invent an aspect or a free-form name
- Don't create permissions, roles or event types under core — use the test service
- Don't assume a clean database: migrations apply forward and the seed is idempotent, nothing is reset
- Don't point tests at the dev database or run them while the dev server holds the port
- Don't rely on another file's state, or on the server's worker being idle
- Don't forget `.js` on relative imports; sort imports longest-first like source files

## Additional Resources

- Complete examples (an `int` file, a flow, helpers, principals, setup files, vitest config, a unit
  test): [examples.md](examples.md)
