---
name: debug
description: Find out why something fails locally, in CI or in a deployed environment. Use when the user reports an error, a failing request, a job that never ran, an email that never arrived, or a service that won't start.
argument-hint: <symptom, error or request id>
---

# Debug

Reproduce first, then read the logs for that one request. Fix the cause, not the
symptom (CLAUDE.md principle 1).

## Follow one request

Every HTTP request gets an id, returned in the `x-request-id` response header and in
every API error's `data.requestId` (`errorRequestId` in `packages/client/src/errors.ts`).
The same id is the `requestId` field on every log line
written for that request, and it travels with queued jobs and outbox events, so one
search covers api → queue → worker → notifications.

- Local: the turbo UI (`bun dev`), one pane per service. Pretty logs in development,
  JSON elsewhere; `LOG_LEVEL=debug` via `bun run env:set LOG_LEVEL=debug` for more.
- After `bun run test:e2e`: `logs/<service>.log` for every service it started.
- A cluster: `kubectl -n boilerplate logs deploy/boilerplate-<service> | grep <requestId>`
  (previews: namespace `pr-<number>`).

## Where to look

1. `bun run doctor`: tools, `.env` drift (a variable in `.env.example` missing from
   `.env`), services up.
2. A service exits at boot: its `src/env.ts` (t3-env) names the variable that failed
   validation. Set it with `bun run env:set KEY=value`; never read `.env`.
3. Local services: `docker compose logs <postgres|valkey|mailpit|rustfs|clamav> --tail 100`.
   `bun run db:up` refuses to start containers that don't fit in Docker's memory and
   says so. Who holds a port: `lsof -nP -iTCP:<port> -sTCP:LISTEN` (without
   `-sTCP:LISTEN`, `lsof` also lists every process merely connected to it, such as a
   service talking to Postgres). A local ClamAV that stopped answering (uploads stay
   pending, the worker logs `clamd timed out`): `docker compose restart clamav`.
4. Types or imports missing after a pull: `bun run gen`. Tables missing:
   `bun run db:deploy`.
5. Something should have happened but didn't (an email, a webhook, an indexed
   document): `bun run jobs` for queue counts, `bun run jobs failed <queue>` for the
   failures and their error. Fix the cause, then `bun run jobs retry <queue> [ids]`.

## Common failures

| Symptom | Usual cause |
|---|---|
| A list is empty for data that exists | query not run through `withTenant`/`tenantTx`, or the wrong org (row-level security hides it) |
| `permission denied for table` | the migration has no grant for that service's role (db-change skill) |
| `NO_ACTIVE_ORGANIZATION` | the session has no active workspace, or the user left it |
| `FEATURE_DISABLED` | the feature's variables aren't set (`apps/api/src/features.ts`) |
| `CLIENT_OUTDATED` | the app sent `x-app-version` below `MINIMUM_CLIENT_VERSION` |
| Email or code never arrives | notifications isn't running, or it went to Mailpit (http://localhost:58025) |
| Job queued, never processed | the consuming service isn't running (`bun dev` starts the core ones; ai and its worker come with `bun dev:full`) |
| Event handled twice or out of order | consumers must be idempotent on the event id and order-independent |
| AI calls fail with `UPSTREAM_UNAVAILABLE` | apps/ai isn't running (`bun dev:full`) or `AI_URL`/`AI_SERVICE_SECRET` differ |

## CI

The fix-ci skill has the whole procedure. In short: `gh run list --branch <branch>`,
then `gh run view <id> --log-failed`, and the same command locally.

`docs/troubleshooting.md` is the human version of this page's local half.
