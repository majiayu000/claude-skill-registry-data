---
name: key
description: "Skill for the [key] area of paddock. 25 symbols across 5 files."
---

# [key]

25 symbols | 5 files | Cohesion: 76%

## When to Use

- Working with code in `src/`
- Understanding how normalizeBoolean, parseWorkspaceFlags, isFeatureFlagKey work
- Modifying [key]-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `src/lib/feature-flag-service.ts` | lastFeatureFlagChange, dependencyBlockers, scopeBlockers, mutationBlockers, featureFlagBlockers (+4) |
| `src/lib/feature-flags.ts` | normalizeBoolean, parseWorkspaceFlags, isFeatureFlagKey, getFeatureFlagDefinition, readWorkspaceFlagValue (+3) |
| `src/app/api/feature-flags/[key]/route.ts` | isHumanAdmin, parseWorkspaceId, requestIp, PATCH |
| `src/lib/feature-flags-openfeature.ts` | contextToFeatureFlagContext, resolveBooleanEvaluation |
| `src/app/api/feature-flags/[key]/preflight/route.ts` | parseWorkspaceId, POST |

## Entry Points

Start here when exploring this area:

- **`normalizeBoolean`** (Function) — `src/lib/feature-flags.ts:325`
- **`parseWorkspaceFlags`** (Function) — `src/lib/feature-flags.ts:340`
- **`isFeatureFlagKey`** (Function) — `src/lib/feature-flags.ts:357`
- **`getFeatureFlagDefinition`** (Function) — `src/lib/feature-flags.ts:361`
- **`readWorkspaceFlagValue`** (Function) — `src/lib/feature-flags.ts:417`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `normalizeBoolean` | Function | `src/lib/feature-flags.ts` | 325 |
| `parseWorkspaceFlags` | Function | `src/lib/feature-flags.ts` | 340 |
| `isFeatureFlagKey` | Function | `src/lib/feature-flags.ts` | 357 |
| `getFeatureFlagDefinition` | Function | `src/lib/feature-flags.ts` | 361 |
| `readWorkspaceFlagValue` | Function | `src/lib/feature-flags.ts` | 417 |
| `explicitlyDisabledCascadePrerequisite` | Function | `src/lib/feature-flags.ts` | 425 |
| `cascadeImpliedByDependent` | Function | `src/lib/feature-flags.ts` | 438 |
| `evaluateFeatureFlagCore` | Function | `src/lib/feature-flags.ts` | 451 |
| `flags` | Function | `src/lib/feature-flag-service.ts` | 213 |
| `getFeatureFlagPreflight` | Function | `src/lib/feature-flag-service.ts` | 238 |
| `getFeatureFlagMutationBlockers` | Function | `src/lib/feature-flag-service.ts` | 329 |
| `assertFeatureFlagKey` | Function | `src/lib/feature-flag-service.ts` | 379 |
| `PATCH` | Function | `src/app/api/feature-flags/[key]/route.ts` | 30 |
| `POST` | Function | `src/app/api/feature-flags/[key]/preflight/route.ts` | 14 |
| `resolveBooleanEvaluation` | Method | `src/lib/feature-flags-openfeature.ts` | 28 |
| `contextToFeatureFlagContext` | Function | `src/lib/feature-flags-openfeature.ts` | 15 |
| `lastFeatureFlagChange` | Function | `src/lib/feature-flag-service.ts` | 84 |
| `dependencyBlockers` | Function | `src/lib/feature-flag-service.ts` | 118 |
| `scopeBlockers` | Function | `src/lib/feature-flag-service.ts` | 129 |
| `mutationBlockers` | Function | `src/lib/feature-flag-service.ts` | 139 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `PATCH → EnsureDirExists` | cross_community | 7 |
| `PATCH → CalculateAgentTrustScore` | cross_community | 7 |
| `PATCH → Generate` | cross_community | 7 |
| `PATCH → NormalizeSecurityEventType` | cross_community | 6 |
| `PATCH → HashPassword` | cross_community | 6 |
| `GET → ParseWorkspaceFlags` | cross_community | 5 |
| `GET → NormalizeBoolean` | cross_community | 5 |
| `GET → IsFeatureFlagKey` | cross_community | 5 |
| `GET → ParseWorkspaceFlags` | cross_community | 5 |
| `GET → NormalizeBoolean` | cross_community | 5 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Spec-008 | 7 calls |
| [id] | 5 calls |
| Feature-flags | 3 calls |
| Cluster_94 | 3 calls |
| Cluster_264 | 1 calls |

## How to Explore

1. `gitnexus_context({name: "normalizeBoolean"})` — see callers and callees
2. `gitnexus_query({query: "[key]"})` — find related execution flows
3. Read key files listed above for implementation details
