---
name: observability
description: "Skill for the Observability area of paddock. 105 symbols across 26 files."
---

# Observability

105 symbols | 26 files | Cohesion: 93%

## When to Use

- Working with code in `src/`
- Understanding how detectAegisStarvation, getCurrentEntitlement, runDailyRefresh work
- Modifying observability-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `src/lib/observability/reconciler.ts` | now, tx, cursorKey, readCursor, writeCursor (+4) |
| `src/lib/provider-entitlement-detector.ts` | detect, sortProbesByPriority, getCurrentEntitlement, persistSnapshot, runProbeChain (+3) |
| `src/lib/observability/ingest-rate-state.ts` | now, readRow, narrowState, getIngestRateState, isAllowedIngestTransition (+3) |
| `src/lib/observability/ingest-admission.ts` | now, refillPerMs, refill, getBucket, diskBand (+1) |
| `src/lib/observability/otlp-receiver.ts` | resolveClientIp, isOver401Threshold, record401, errorBody, decompressBounded (+1) |
| `src/lib/observability/posted-effect.ts` | isAllowedPostedEffectTransition, loadEffectByCanonical, correctionsExistForCanonical, deriveState, getPostedEffectState (+1) |
| `src/lib/observability/dedupe.ts` | maxNullable, maxStringNullable, firstNonNullId, confidenceOf, mergeRawEvents (+1) |
| `src/lib/observability/correction-ledger.ts` | flushOne, appendCorrection, flushCorrection, flushDueCorrections, loadCanonicalCostAndId (+1) |
| `src/lib/observability/adapter-counters.ts` | key, recordAdapterCounter, getAdapterCounter, formatAdapterCountersAsProm, snapshotAdapterCounters (+1) |
| `src/lib/observability/self-obs-metrics.ts` | identity, normalizeLabels, incrementMetric, observeHistogram, getMetricsSnapshot |

## Entry Points

Start here when exploring this area:

- **`detectAegisStarvation`** (Function) — `src/lib/resource-aegis-starvation-detector.ts:77`
- **`getCurrentEntitlement`** (Function) — `src/lib/provider-entitlement-detector.ts:136`
- **`runDailyRefresh`** (Function) — `src/lib/provider-entitlement-detector.ts:229`
- **`runNearExpiryRefresh`** (Function) — `src/lib/provider-entitlement-detector.ts:261`
- **`detectInline`** (Function) — `src/lib/provider-entitlement-detector.ts:306`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `detectAegisStarvation` | Function | `src/lib/resource-aegis-starvation-detector.ts` | 77 |
| `getCurrentEntitlement` | Function | `src/lib/provider-entitlement-detector.ts` | 136 |
| `runDailyRefresh` | Function | `src/lib/provider-entitlement-detector.ts` | 229 |
| `runNearExpiryRefresh` | Function | `src/lib/provider-entitlement-detector.ts` | 261 |
| `detectInline` | Function | `src/lib/provider-entitlement-detector.ts` | 306 |
| `incrementMetric` | Function | `src/lib/observability/self-obs-metrics.ts` | 113 |
| `observeHistogram` | Function | `src/lib/observability/self-obs-metrics.ts` | 139 |
| `getMetricsSnapshot` | Function | `src/lib/observability/self-obs-metrics.ts` | 190 |
| `getIngestRateState` | Function | `src/lib/observability/ingest-rate-state.ts` | 145 |
| `isAllowedIngestTransition` | Function | `src/lib/observability/ingest-rate-state.ts` | 164 |
| `transitionIngestRateState` | Function | `src/lib/observability/ingest-rate-state.ts` | 181 |
| `recordIngestDrop` | Function | `src/lib/observability/ingest-rate-state.ts` | 236 |
| `resetIngestDrops` | Function | `src/lib/observability/ingest-rate-state.ts` | 253 |
| `admitIngestion` | Function | `src/lib/observability/ingest-admission.ts` | 155 |
| `tx` | Function | `src/app/api/governance/ingest/[source]/resume/route.ts` | 95 |
| `handleOtlpRequest` | Function | `src/lib/observability/otlp-receiver.ts` | 140 |
| `decodeOtlpTraces` | Function | `src/lib/observability/otlp-decoder.ts` | 59 |
| `decodeOtlpMetrics` | Function | `src/lib/observability/otlp-decoder.ts` | 78 |
| `POST` | Function | `src/app/api/otlp/v1/metrics/route.ts` | 17 |
| `POST` | Function | `src/app/api/otlp/v1/traces/route.ts` | 18 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `POST → NormalizeLabels` | cross_community | 4 |
| `POST → Identity` | cross_community | 4 |
| `POST → NormalizeLabels` | cross_community | 4 |
| `POST → Identity` | cross_community | 4 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Cluster_176 | 2 calls |
| Cluster_200 | 2 calls |
| Cluster_183 | 1 calls |
| [id] | 1 calls |

## How to Explore

1. `gitnexus_context({name: "detectAegisStarvation"})` — see callers and callees
2. `gitnexus_query({query: "observability"})` — find related execution flows
3. Read key files listed above for implementation details
