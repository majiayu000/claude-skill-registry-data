---
name: swap-realtime
description: Move live UI updates off the shared Redis (a dedicated Redis, NATS, a hosted pub/sub). Use when the user decides realtime fan-out should leave the main Redis, or asks how live updates scale. Not for debugging; when something fails, use the debug skill.
disable-model-invocation: true
---

# Swap the realtime transport

- **Seam:** `createRealtime(schema)` in `packages/nest-common/src/realtime.ts` returns
  `publish(redis, channel, message)` and `RealtimeHub` (one subscriber connection per
  API process, fanned out to its SSE streams). There is no separate interface: the
  connection passed in is the swap point.
- **Today:** Redis pub/sub on the shared `REDIS_URL`, channels `realtime:user:<id>` and
  `realtime:org:<id>`. Best effort: messages only say "refetch".
- **Used in:** `apps/api/src/realtime.ts` (hub and publish), `apps/worker/src/realtime/`
  (publishes domain events from `events-realtime`), and `apps/ai/app/realtime.py`
  (Python publisher, same prefix and message contract).

## Swap

1. A dedicated Redis: give `RealtimeHub` and every `publish` call a connection to it,
   from a new variable (e.g. `REALTIME_REDIS_URL`) in the api's and worker's
   `src/env.ts` and `apps/ai/app/settings.py`, documented in `.env.example` and
   `docs/environment.md`. Nothing else changes.
2. Another broker: reimplement `createRealtime` with the same `publish` and
   `RealtimeHub.stream` signatures, and change `apps/ai/app/realtime.py` to publish there
   too. Keep channel names and the `realtimeMessage` contract
   (`packages/contracts/src/realtime.ts`).

## Tests

`packages/nest-common/test/realtime.integration.test.ts`,
`apps/worker/src/realtime/realtime.processor.test.ts`, the realtime case in
`apps/api/test/api.integration.test.ts`, and `apps/web/e2e/realtime.spec.ts`.

## Finish

1. The verify skill.
2. Ask the `reviewer` agent to review the change, and the `security-reviewer` agent: a
   new implementation brings its own credentials and sends data somewhere new. If you
   wrote a migration, the `migration-reviewer` agent too.
3. Update the seam's row in the README's "Scaling path" table if what's "Now" changed.
