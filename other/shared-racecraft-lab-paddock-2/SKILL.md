---
name: shared
description: "Skill for the _shared area of paddock. 33 symbols across 6 files."
---

# _shared

33 symbols | 6 files | Cohesion: 89%

## When to Use

- Working with code in `src/`
- Understanding how POST, seedSpec008Fixture, teardownSpec008Fixture work
- Modifying _shared-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `src/app/api/admin/spec-008/_shared/test-state-handlers.ts` | getDatabase, tableExists, readWorkspaceId, readString, readNumber (+9) |
| `src/app/api/admin/spec-008/_shared/fixture-seeder.ts` | getDatabase, tableExists, nowIso, insertResourcePolicies, insertOverrideGrant (+7) |
| `src/app/api/admin/workspaces/[id]/feature-flags/route.ts` | isFlagsMap, readExistingFlags, POST |
| `src/app/api/admin/spec-008/seed-fixture/route.ts` | parseBody, POST |
| `src/app/api/admin/spec-008/_shared/auth-gate.ts` | adminTestModeGate |
| `src/app/api/admin/spec-008/seed-fixture/[id]/route.ts` | DELETE |

## Entry Points

Start here when exploring this area:

- **`POST`** (Function) — `src/app/api/admin/spec-008/seed-fixture/route.ts:42`
- **`seedSpec008Fixture`** (Function) — `src/app/api/admin/spec-008/_shared/fixture-seeder.ts:251`
- **`teardownSpec008Fixture`** (Function) — `src/app/api/admin/spec-008/_shared/fixture-seeder.ts:272`
- **`adminTestModeGate`** (Function) — `src/app/api/admin/spec-008/_shared/auth-gate.ts:48`
- **`POST`** (Function) — `src/app/api/admin/workspaces/[id]/feature-flags/route.ts:58`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `POST` | Function | `src/app/api/admin/spec-008/seed-fixture/route.ts` | 42 |
| `seedSpec008Fixture` | Function | `src/app/api/admin/spec-008/_shared/fixture-seeder.ts` | 251 |
| `teardownSpec008Fixture` | Function | `src/app/api/admin/spec-008/_shared/fixture-seeder.ts` | 272 |
| `adminTestModeGate` | Function | `src/app/api/admin/spec-008/_shared/auth-gate.ts` | 48 |
| `POST` | Function | `src/app/api/admin/workspaces/[id]/feature-flags/route.ts` | 58 |
| `DELETE` | Function | `src/app/api/admin/spec-008/seed-fixture/[id]/route.ts` | 16 |
| `handleSeedState` | Function | `src/app/api/admin/spec-008/_shared/test-state-handlers.ts` | 80 |
| `handleAegisState` | Function | `src/app/api/admin/spec-008/_shared/test-state-handlers.ts` | 127 |
| `handleBreakerState` | Function | `src/app/api/admin/spec-008/_shared/test-state-handlers.ts` | 168 |
| `handleBulkPromoteState` | Function | `src/app/api/admin/spec-008/_shared/test-state-handlers.ts` | 212 |
| `handleCalibrationState` | Function | `src/app/api/admin/spec-008/_shared/test-state-handlers.ts` | 257 |
| `handleEmitDecision` | Function | `src/app/api/admin/spec-008/_shared/test-state-handlers.ts` | 294 |
| `handleEmitDispatch` | Function | `src/app/api/admin/spec-008/_shared/test-state-handlers.ts` | 333 |
| `handleOverrideGrantState` | Function | `src/app/api/admin/spec-008/_shared/test-state-handlers.ts` | 370 |
| `handleBudgetUtilization` | Function | `src/app/api/admin/spec-008/_shared/test-state-handlers.ts` | 431 |
| `parseBody` | Function | `src/app/api/admin/spec-008/seed-fixture/route.ts` | 28 |
| `getDatabase` | Function | `src/app/api/admin/spec-008/_shared/fixture-seeder.ts` | 38 |
| `tableExists` | Function | `src/app/api/admin/spec-008/_shared/fixture-seeder.ts` | 55 |
| `nowIso` | Function | `src/app/api/admin/spec-008/_shared/fixture-seeder.ts` | 66 |
| `insertResourcePolicies` | Function | `src/app/api/admin/spec-008/_shared/fixture-seeder.ts` | 131 |

## Connected Areas

| Area | Connections |
|------|-------------|
| [id] | 4 calls |
| Spec-008 | 1 calls |

## How to Explore

1. `gitnexus_context({name: "POST"})` — see callers and callees
2. `gitnexus_query({query: "_shared"})` — find related execution flows
3. Read key files listed above for implementation details
