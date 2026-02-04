---
name: backend-mvp-guardrails
description: Use when designing or reviewing a backend MVP with tight budget, evolving schema, and reliance on third-party backends where idempotency, replay, and responsibility attribution are high-risk.
---

# Backend MVP Guardrails

## Overview
Minimize irreversible decisions. Every write must be idempotent, every aggregate must be replayable, and every incident must be attributable with minimal evidence.

## When to Use
- MVP backend with single-digit USD/month budget or strict capacity limits
- Fast schema evolution or new data sources with unknown fields
- Third-party backend dependency (e.g., InsForge) with no status page or DB metrics
- Repeated ambiguity about whether failures are vendor or application issues

When NOT to use: throwaway prototypes where data loss and misattribution are acceptable.

## Core Pattern (Two Layers)

### Layer 1: Principle Guardrails (platform-agnostic)
1) **Source of truth is immutable or append-only.** Avoid online recomputation on read paths.
2) **Idempotent writes.** Deterministic keys + upsert or unique constraint.
3) **Replayable aggregates.** Derived tables can be rebuilt from the source of truth.
4) **Evidence-first attribution.** No structured evidence, no blame, no destructive fix.
5) **Cost-first queries.** Pre-aggregate, cap ranges, enforce limits, avoid full scans.
6) **Schema evolution is additive.** New fields are optional and versioned; unknown fields are rejected by allowlist.

### Layer 2: Platform Mapping (InsForge example)
- **Fact table:** half-hour buckets (e.g., `vibescore_tracker_hourly`)
- **Idempotency key:** `user_id + device_id + source + model + hour_start`
- **Aggregates:** derived from buckets; do not read raw event tables for dashboards
- **Retention:** keep aggregates longer; cap any event-level tables
- **Backfill:** limited window + upsert; must be replayable
- **Observability:** M1 structured logs (see below)

## Responsibility Attribution Protocol (M1)
**Required fields:** `request_id`, `function`, `stage`, `status`, `latency_ms`, `error_code`, `upstream_status`, `upstream_latency_ms`

**Attribution rules:**
- Missing `upstream_status` => **UNKNOWN** (do not change data semantics)
- `upstream_status` is 5xx/timeout and function status is 5xx => likely vendor/backbone issue
- `upstream_status` is 2xx and function status is 4xx/5xx => likely application validation/logic issue
- `latency_ms` high and `upstream_latency_ms` low => likely application-side bottleneck

**Stop rule:** no data rewrite, schema change, or semantic patch without a replay plan and rollback.

## Quick Reference
| Guardrail | Why | Minimum Implementation |
| --- | --- | --- |
| Idempotent writes | Prevent double-counting | Unique key + upsert |
| Replayable aggregates | Safe fixes | Source-of-truth table + backfill job |
| Cost caps | Fit low budget | Range limits + pre-aggregates |
| Evidence-first | Avoid misfix | M1 structured logs |
| Schema allowlist | Avoid data bloat | Reject unknown fields |

## Implementation Example (Structured Log)
```js
const start = Date.now();
const requestId = crypto.randomUUID();
const log = (entry) =>
  console.log(JSON.stringify({
    request_id: requestId,
    function: 'example-function',
    ...entry
  }));

try {
  const upstreamStart = Date.now();
  const res = await fetch(upstreamUrl);
  const upstreamLatency = Date.now() - upstreamStart;

  log({
    stage: 'upstream',
    status: res.status,
    upstream_status: res.status,
    upstream_latency_ms: upstreamLatency,
    latency_ms: Date.now() - start,
    error_code: res.ok ? null : 'UPSTREAM_ERROR'
  });
} catch (err) {
  log({
    stage: 'exception',
    status: 500,
    upstream_status: null,
    upstream_latency_ms: null,
    latency_ms: Date.now() - start,
    error_code: 'UPSTREAM_TIMEOUT'
  });
  throw err;
}
```

## Common Mistakes
- Online aggregation in dashboard endpoints under low budget
- Adding new data sources without updating idempotency keys
- Blame without `upstream_status` evidence
- Storing full payloads "just in case" (privacy and cost risk)
- Changing data semantics without replay/backfill plan

## Rationalization Table
| Excuse | Reality |
| --- | --- |
| "We are a tiny team, logs are overkill" | Small teams need stronger evidence, not weaker. |
| "Vendor is unstable, we cannot know" | You still need M1 logs to avoid misfixes. |
| "Budget is low so scans are fine" | Low budget means scans fail sooner. |
| "We can patch the numbers" | Patches without replay create permanent drift. |

## Red Flags - STOP
- No structured logs but attempting responsibility attribution
- Data rewrite without replay/backfill plan
- Dashboard reads from raw event tables
- Unknown fields stored without allowlist
- Idempotency key not updated when adding dimensions
