---
name: add-load-test
description: Add a load-test scenario for an API path (k6, in load/), or change the load budget. Use when the user wants to know how a new endpoint holds up under traffic, or before a launch.
argument-hint: <path or scenario>
---

# Add a load test

`load/api.ts` is a k6 script run in Docker (`bun run test:load`), against a running API,
with users signed in first (`apps/api/src/load-users.ts`, sessions in
`load/.sessions.json`). docs/testing.md, "Load", has the profiles.

1. **The traffic.** An exported function per journey in `load/api.ts`, like `read` and
   `write`: requests over `/api/v1` with the virtual user's session (`user()`), tagged
   with a `name`, each with a `check` on the status and the body. Keep the check that a
   user sees only their own workspace's rows when the path returns tenant data.
2. **Its share of the traffic.** A scenario for it in both profiles in `profiles`:
   `smoke` (a constant low rate for 30 s) and `load` (`ramp(<exec>, <rate>)`, a fraction
   of `TARGET_RPS`).
3. **The budget.** Its latency threshold in `options.thresholds`
   (`"http_req_duration{scenario:<name>}": ["p(95)<…", "p(99)<…"]`); the failure and
   check rates already apply to every request. The run fails when one does; raise one
   only on purpose. Data the journey needs that a fresh user lacks is created through
   the API in the function itself or in `setup()`, never in the database.
4. **Types.** `bun run --filter @repo/load check-types` (k6's types from `@types/k6`).
5. **Run it.** The API up (`bun dev`, in the background), then `bun run test:load` (the
   30-second smoke CI runs); `PROFILE=load bun run test:load` for the ramp to
   `TARGET_RPS`. Against another environment: `BASE_URL`, with that environment's
   variables so the sessions are made in its database.

## Done when

The smoke passes locally, `check-types` passes, and the nightly run's target
(`LOAD_TARGET_RPS`, docs/repository-settings.md) still holds.
