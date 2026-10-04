---
name: test-harness-health-check
description: Use before trusting a green integration test run, after editing tests/fixtures/db-test-helpers.ts or tests/integration/docker-compose.test.yml, when adding a new migration file to schemas/migrations, or when integration tests are flaky/failing in a way that looks environmental (auth failures, "relation does not exist", container crash loops). Verifies the test harness itself genuinely exercises a fresh environment instead of silently passing against a broken or partial setup.
---

# Test Harness Health Check

## Overview

This session found and fixed the SAME class of bug three separate times: the integration test
harness *looked* fine (tests ran, some even passed) while silently not exercising what it
claimed to. Before trusting "tests are green," re-verify the harness against these three known
failure modes — all previously real, all in this exact codebase.

## The Three Known Failure Classes (with evidence)

### 1. Migration chain gaps — tests pass against a schema the harness never fully built

`resetTestDatabase()` in `tests/fixtures/db-test-helpers.ts` once applied only
`0001_init.sql` — every HTTP-driven integration test downstream of signup failed with
"Authentication failed... app_user" because `app_user`/`platform_admin_role` are created by
`0003`/`0006`, never by `0001` alone. **Check:** does `MIGRATION_FILES` in
`db-test-helpers.ts` (currently 10 files: `0001, 0002, 0008, 0003, 0004, 0009, 0005, 0006, 0007,
0010`) list every file present in `schemas/migrations/`? Run:

```
ls schemas/migrations/*.sql | wc -l   # compare against MIGRATION_FILES.length in db-test-helpers.ts
```

A new migration added to `schemas/migrations/` without a matching entry in `MIGRATION_FILES`
means every fresh-container integration run silently tests against a stale schema — tests can
pass while proving nothing about the new column/table/policy.

### 2. Container path/layout convention drift — crash loops that look like "flaky CI"

Postgres 18 changed its data directory convention (`pg_ctlcluster`-compatible, versioned
subdirectory). A `tmpfs`/volume mount at the old `.../data` path crash-loops the container on
boot with "PostgreSQL data in ... (unused mount/volume)". **Check:** in both
`tests/integration/docker-compose.test.yml` and root `docker-compose.yml`, the mount must be
`/var/lib/postgresql` (not `/var/lib/postgresql/data`) for `postgres:18-alpine`. If the pinned
Postgres major version is ever bumped, re-verify this convention against that version's actual
image docs before assuming the old mount path still works — this is exactly the kind of
volatile, version-specific detail that silently breaks CI without a code change ever touching it.

### 3. Concurrent-file races corrupting shared reset state

Vitest runs test files in parallel by default; every integration test file calls
`resetTestDatabase()` in its own `beforeAll`. Against a truly fresh container, every file races
to `DROP SCHEMA public CASCADE` at once, producing "relation does not exist" in whichever files
lose. The fix (already in `db-test-helpers.ts`) is a `pg_advisory_lock` + double-checked
`tenantsTableExists()` re-check after acquiring it. **Check:** if you ever touch
`resetTestDatabase()`, confirm this lock-then-recheck shape survives — removing the lock
reintroduces the race, and removing the re-check turns two callers into two full
`DROP SCHEMA`+migrate cycles racing each other.

## How to Run the Check

```
# 1. Migration completeness
ls schemas/migrations/*.sql
grep -A15 "const MIGRATION_FILES" tests/fixtures/db-test-helpers.ts

# 2. Fresh-container proof, not just "tests passed" -- tear down volumes and recreate from nothing
npm run test:qa:integration:down   # docker compose ... down -v (removes the tmpfs/volumes)
npm run test:qa:integration:up
npm run test:qa:integration        # a run against a truly empty container is the only real proof

# 3. Confirm resetTestDatabase() took the FRESH branch (drop+migrate), not the shared/persistent
#    no-op branch -- add a temporary console.log or check container logs for the DROP SCHEMA
#    statement if in doubt.
```

A run against containers left over from a previous session (volumes NOT recreated) can pass even
with a broken migration chain, because the schema was already correct from before. Only a
volume-recreated (`down -v` then `up`) run is a genuine oracle for point 1 and 2 above.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Trusting a green run without recreating containers first | `docker compose -f tests/integration/docker-compose.test.yml down -v` before the run that matters |
| Adding a migration file without updating `MIGRATION_FILES` | Update `db-test-helpers.ts` in the same commit as any new `schemas/migrations/*.sql` file |
| Assuming CI flakiness is random | Check for the three failure classes above first — this project's "flaky" integration failures were deterministic environment bugs, not flakiness |
| Weakening/skip-ing a failing integration test to get green | `tests/` is QA-owned (loop-protocol Rule 4) — a failing test after a fresh-container run is signal, not noise; report/fix root cause, don't touch the test |
| Assuming `resetTestDatabase()` always resets | It's a no-op against a shared/persistent DB (detected via `tenantsTableExists`) — only the ephemeral/fresh path actually drops and rebuilds; know which mode you're running against |
