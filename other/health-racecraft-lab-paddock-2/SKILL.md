---
name: health
description: "Skill for the Health area of paddock. 28 symbols across 6 files."
---

# Health

28 symbols | 6 files | Cohesion: 88%

## When to Use

- Working with code in `src/`
- Understanding how extractSchema, validateSchema, scanMemoryFiles work
- Modifying health-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `src/lib/memory-utils.ts` | extractSchema, validateSchema, scanMemoryFiles, walk, buildLinkGraph (+7) |
| `src/app/api/gateways/health/route.ts` | ensureGatewaysTable, parseGatewayVersion, hasOpenClaw32ToolsProfileRisk, ipv4InCidr, ipv4ToNum (+3) |
| `src/app/api/gateways/health/health-utils.test.ts` | ipv4ToNum, ipv4InCidr, isBlockedUrl |
| `src/app/api/memory/health/route.ts` | mergeReports, GET |
| `src/app/api/memory/context/route.ts` | mergeContextPayloads, GET |
| `src/app/api/memory/process/route.ts` | POST |

## Entry Points

Start here when exploring this area:

- **`extractSchema`** (Function) — `src/lib/memory-utils.ts:64`
- **`validateSchema`** (Function) — `src/lib/memory-utils.ts:94`
- **`scanMemoryFiles`** (Function) — `src/lib/memory-utils.ts:136`
- **`walk`** (Function) — `src/lib/memory-utils.ts:144`
- **`buildLinkGraph`** (Function) — `src/lib/memory-utils.ts:200`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `extractSchema` | Function | `src/lib/memory-utils.ts` | 64 |
| `validateSchema` | Function | `src/lib/memory-utils.ts` | 94 |
| `scanMemoryFiles` | Function | `src/lib/memory-utils.ts` | 136 |
| `walk` | Function | `src/lib/memory-utils.ts` | 144 |
| `buildLinkGraph` | Function | `src/lib/memory-utils.ts` | 200 |
| `runHealthDiagnostics` | Function | `src/lib/memory-utils.ts` | 283 |
| `generateMOCs` | Function | `src/lib/memory-utils.ts` | 507 |
| `generateContextPayload` | Function | `src/lib/memory-utils.ts` | 561 |
| `reflectPass` | Function | `src/lib/memory-utils.ts` | 612 |
| `reweavePass` | Function | `src/lib/memory-utils.ts` | 653 |
| `gapDetectPass` | Function | `src/lib/memory-utils.ts` | 709 |
| `consolidatePass` | Function | `src/lib/memory-utils.ts` | 829 |
| `POST` | Function | `src/app/api/memory/process/route.ts` | 18 |
| `GET` | Function | `src/app/api/memory/health/route.ts` | 40 |
| `GET` | Function | `src/app/api/memory/context/route.ts` | 34 |
| `POST` | Function | `src/app/api/gateways/health/route.ts` | 161 |
| `mergeReports` | Function | `src/app/api/memory/health/route.ts` | 12 |
| `mergeContextPayloads` | Function | `src/app/api/memory/context/route.ts` | 9 |
| `ensureGatewaysTable` | Function | `src/app/api/gateways/health/route.ts` | 4 |
| `parseGatewayVersion` | Function | `src/app/api/gateways/health/route.ts` | 46 |

## Connected Areas

| Area | Connections |
|------|-------------|
| [id] | 6 calls |

## How to Explore

1. `gitnexus_context({name: "extractSchema"})` — see callers and callees
2. `gitnexus_query({query: "health"})` — find related execution flows
3. Read key files listed above for implementation details
