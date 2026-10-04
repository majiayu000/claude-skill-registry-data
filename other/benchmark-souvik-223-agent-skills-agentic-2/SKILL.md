---
name: benchmark
description: "Skill for the Benchmark area of Securacy. 7 symbols across 3 files."
---

# Benchmark

7 symbols | 3 files | Cohesion: 100%

## When to Use

- Working with code in `model-compass/`
- Understanding how cleanAndParseJson, calculateAccuracy, normalize work
- Modifying benchmark-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `model-compass/src/lib/scoring-engine.ts` | toStr, calculateAccuracy, normalize, scoreCategory |
| `model-compass/src/app/api/benchmark/route.ts` | POST, makeErrorResult |
| `model-compass/src/lib/utils.ts` | cleanAndParseJson |

## Entry Points

Start here when exploring this area:

- **`cleanAndParseJson`** (Function) — `model-compass/src/lib/utils.ts:7`
- **`calculateAccuracy`** (Function) — `model-compass/src/lib/scoring-engine.ts:17`
- **`normalize`** (Function) — `model-compass/src/lib/scoring-engine.ts:46`
- **`scoreCategory`** (Function) — `model-compass/src/lib/scoring-engine.ts:48`
- **`POST`** (Function) — `model-compass/src/app/api/benchmark/route.ts:25`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `cleanAndParseJson` | Function | `model-compass/src/lib/utils.ts` | 7 |
| `calculateAccuracy` | Function | `model-compass/src/lib/scoring-engine.ts` | 17 |
| `normalize` | Function | `model-compass/src/lib/scoring-engine.ts` | 46 |
| `scoreCategory` | Function | `model-compass/src/lib/scoring-engine.ts` | 48 |
| `POST` | Function | `model-compass/src/app/api/benchmark/route.ts` | 25 |
| `toStr` | Function | `model-compass/src/lib/scoring-engine.ts` | 9 |
| `makeErrorResult` | Function | `model-compass/src/app/api/benchmark/route.ts` | 204 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `POST → Normalize` | intra_community | 4 |
| `POST → ToStr` | intra_community | 4 |
| `POST → CleanAndParseJson` | intra_community | 3 |

## How to Explore

1. `gitnexus_context({name: "cleanAndParseJson"})` — see callers and callees
2. `gitnexus_query({query: "benchmark"})` — find related execution flows
3. Read key files listed above for implementation details
