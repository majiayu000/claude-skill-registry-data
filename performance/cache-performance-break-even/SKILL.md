---
name: cache-performance-break-even
kind: skill
status: ready
provenance:
  principles:
  - P001
  claims:
  - C00022
  - C00023
  - C00024
  - C00113
  - C00114
  - C00115
  - C00116
  - C00117
  - C00118
  - C00119
  evidence:
  - E00011
  - E00012
  - E00013
  - E00051
  - E00052
  - E00053
  - E00054
  - E00055
  - E00056
  - E00057
  source_anchors:
  - 11ebbc818b96-c0000
  - 11ebbc818b96-c0003
  authored_from_digest: 5bbaae67acf6099f960eeeef7a4a53b4e78da3cf9d4c848c69dd83949922bb9f
---

# Cache Performance Break-Even Analysis

## Purpose

Determine, quantitatively, whether a proposed cache delivers a net latency benefit before it
is built — and, for an existing cache, whether the observed hit rate justifies keeping it.
This skill produces the minimum viable hit rate (H_min) and the projected average request
time at a target hit rate, so a go/no-go decision rests on arithmetic rather than intuition
(P009, anchors h0114/h0153).

## When to use

- A go/no-go decision on adding a cache to a service path.
- Justifying a target hit rate or cache size to stakeholders.
- Diagnosing whether a deployed cache is actually reducing average latency.
- Confirming that P001 viability conditions have been met before committing to
  implementation (cache must be faster with fewer resources than the backing call).

Do not apply this skill when the cache is deployed solely for availability (serving results
while the backing store is down); in that case the effectiveness formula does not govern the
decision.

## Inputs

| Symbol | Name | Required | Notes |
|--------|------|----------|-------|
| S | `Service_Call_Time` | Yes | Latency of the uncached backing operation (ms or equivalent unit). |
| C_check | `Cache_Check` | Yes | Time to perform a cache lookup, paid on every request (ms). |
| C_write | `Cache_Write` | Yes | Time to populate the cache on a miss (ms). |
| H | Hit rate | If available | Observed or target fraction of requests satisfied by the cache (0–1). |

`Cache_Overhead` is the combined per-miss penalty: `C_check + C_write`.

If `S`, `C_check`, or `C_write` is unknown, stop and request an estimate. Do not fabricate
either value — this is a forbidden behaviour (P009, profile `forbidden_behaviours`).

## Procedure

### Step 1 — Model the two request paths (c066/c067, anchors c0115–c0120)

In a cache-aside strategy there are two distinct cost paths:

- **Cache miss** (must still call the backing service):
  `Miss_Time = C_check + S + C_write`
  This is higher than calling the service without a cache, because the lookup and write are
  extra steps paid on top of the service call.

- **Cache hit** (backing service not called):
  `Hit_Time = C_check`
  Only the lookup cost is incurred.

State both values explicitly before proceeding.

### Step 2 — Compute the weighted average request time (c068, anchors c0125/c0126)

For a given hit rate H (and therefore miss rate 1 − H):

```
Request_Time_With_Cache = (1 − H) × Miss_Time + H × Hit_Time
```

Expanded:

```
Request_Time_With_Cache = (1 − H) × (C_check + S + C_write) + H × C_check
```

For the cache to provide a net benefit, this must be less than `S` (the uncached baseline).

### Step 3 — Derive the break-even hit rate H_min (c068, anchors c0136/c0137)

Set `Request_Time_With_Cache = S` (the break-even boundary) and solve for H:

```
H_min = Cache_Overhead / (S + Cache_Overhead)

where Cache_Overhead = C_check + C_write
```

State H_min explicitly. This is the primary output of the skill.

- When `H > H_min`: the cache reduces average request time below the uncached baseline.
- When `H < H_min`: the cache increases average request time — it degrades performance
  relative to the uncached baseline.

### Step 4 — Interpret the Cache_Overhead-to-S ratio (c070/c071, anchors c0151/c0152/h0153)

The ratio `Cache_Overhead / S` governs how easy or hard it is to benefit from the cache:

- `Cache_Overhead ≪ S` (expensive backing call, cheap lookup and write): H_min is small,
  meaning even a modest hit rate produces a net gain. The greater the service call time
  relative to cache overhead, the more dramatic the latency reduction at any given hit rate.
- `Cache_Overhead ≈ S` or `Cache_Overhead > S`: H_min approaches or exceeds 1.0 (100%),
  making a net benefit practically unreachable. In this case, decline the cache rather than
  proceed (P001 viability condition: cache access must be faster with fewer resources).

Name the interpretation explicitly so the caller understands the risk profile.

### Step 5 — Project latency at the target hit rate (c068/c070, anchors c0144–c0152)

If a target or observed hit rate H_target is available, compute the projected average:

```
Projected_Avg = (1 − H_target) × Miss_Time + H_target × Hit_Time
```

Also compute the percentage improvement over the uncached baseline:

```
Improvement = (S − Projected_Avg) / S × 100%
```

Note that this improvement grows substantially as either H increases or S increases relative
to Cache_Overhead. A higher backing-service cost amplifies the benefit of every percentage
point of hit rate.

### Step 6 — Record the calculation and flag it as a hypothesis

The pre-deployment calculation is an estimate, not a measurement. Record:

- The input values used (S, C_check, C_write, and whether they are measured or estimated).
- H_min and the projected average at the target hit rate.
- The go/no-go verdict.

Flag that the estimate must be validated against observed hit/miss metrics after deployment
(P009). If observed hit rate after deployment falls below H_min, the cache should be
reassessed or removed.

## Output

A break-even verdict containing:

1. **H_min** — the minimum viable hit rate, expressed as a percentage, with the formula
   values substituted.
2. **Projected average latency** at the target or observed hit rate, with the percentage
   improvement over the uncached baseline.
3. **Go/no-go recommendation** — "net-beneficial" if H > H_min, "degrades performance" if
   H < H_min, or "not viable" if H_min is unreachable (Cache_Overhead ≥ S).
4. On a "no" verdict: the specific failing condition (overhead too close to backing cost, or
   hit rate too low) stated by name.

Hand the accepted H_min to the implementation team as the minimum performance gate;
it is a measurable contract, not a guideline (handoff_rules).

## References

- `references/cache-performance-formula-sheet.md` — the formula with a worked example.
- Profile `always_on`: "Performance formula and break-even analysis (P009)" for the
  Request_Time_With_Cache definition and H_min derivation.

## Provenance

Principle P009 (cache performance break-even formula); P001 (effectiveness viability
conditions — cache must be faster with fewer resources). Claims c066 (cache overhead
concept and miss-path cost model), c067 (hit-path cost model), c068 (weighted average
request time and break-even derivation), c070 (effect of higher service call time on
latency reduction magnitude), c071 (per-opportunity calculation requirement). Evidence
records e031–e033, e035–e036. Source: *Caching at Scale With Redis* (Atchison 2021),
Chapter 9 — distillation-only; no verbatim quotation.
