---
name: eviction-policy-selection
kind: skill
status: ready
provenance:
  principles:
  - P003
  claims:
  - C00041
  - C00042
  - C00043
  - C00044
  - C00045
  - C00050
  evidence:
  - E00019
  - E00020
  - E00021
  - E00022
  - E00023
  - E00024
  source_anchors:
  - 11ebbc818b96-c0001
  authored_from_digest: 2a28c7758ae390d9c5d46f2391dc8e4c98ac461462223c7997732d9f4a88f3d5
---

# Eviction Policy Selection

## Purpose

Select the cache eviction algorithm that fits the workload's observed access distribution,
configure it correctly in Redis, and diagnose eviction-related pathologies such as cache
thrashing — so the cache preserves entries that are likely to be needed again rather than
discarding them (P005).

The choice is always **situation-dependent**. LRU and LFU are starting points matched to
the distribution shape, not mechanical defaults. Determining the right policy may require
measuring the actual access pattern or running a trial before committing (quality_bar,
P005).

## When to use

- A new Redis cache requires an eviction policy and the working dataset will not fit
  entirely in available memory.
- An existing cache shows an elevated miss rate, thrashing symptoms, or unexpected
  eviction of entries that are immediately re-requested.
- A caller asks for a comparison or trade-off between eviction algorithms in the context
  of Redis.

This skill does **not** apply when the full working dataset fits in memory and no eviction
is required (no-eviction / permanent cache scenario per P005 `does_not_apply_when`).

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| Access-distribution shape | Yes | Is reuse driven by recency, by frequency, or by a time-bounded validity window? |
| Whether volatile (TTL-bearing) or allkeys scope is needed | Yes | Determines `volatile-*` vs `allkeys-*` Redis policy |
| Current miss rate or thrashing symptoms | If tuning | Needed to distinguish wrong-algorithm from undersized-cache |
| Approximate cache size and working-dataset size | Recommended | Informs whether undersizing is a contributing factor |

## Procedure

### Step 1 — Characterise the access distribution

Determine which of the following best describes the workload. If the distribution shape is
not yet known, state that measurement or trial will be needed before committing to a policy.

- **Recency-skewed**: recently accessed entries are disproportionately likely to be
  requested again in the near future.
- **Frequency-skewed**: a stable set of entries is requested repeatedly over long time
  windows, independent of when they were last accessed.
- **Time-bounded validity**: entries become stale or irrelevant after a natural expiry
  period, regardless of access recency or frequency.
- **Mixed or unknown**: distribution is not yet characterised; a measurement step or
  trial period is required.

### Step 2 — Map distribution shape to a candidate algorithm

Use the distribution characterisation as a **starting point**, not a deterministic match.
The source acknowledges that both LRU and LFU are situation-dependent and that no
systematic benchmark establishes universal superiority of one over the other (e013,
evidence_strength: moderate, support_level: partially_supported).

| Distribution shape | Candidate algorithm | Rationale |
|--------------------|---------------------|-----------|
| Recency-skewed | LRU | Evicts the entry that has gone longest without access; fits the premise that recent access predicts future access (c026) |
| Frequency-skewed | LFU | Evicts the entry with the lowest access count; fits workloads where a stable popular set recurs over long windows (c026) |
| Time-bounded validity | TTL (per-key EXPIRE) | Data expires on a schedule independent of access pattern; in Redis this is a key-level setting, not a maxmemory-policy (c023) |
| Unknown / mixed | Measure first, then trial LRU as the more common default | Do not commit without evidence |

**Do not select random eviction in production.** Random eviction more often removes entries
that are still needed, increasing miss rates when those evicted entries are re-requested
shortly after (source anchor h0032, c026).

### Step 3 — Select the Redis `maxmemory-policy` value

Map the algorithm choice to a concrete Redis configuration value (c029, c030,
source anchor h0039):

| Scope | LRU | LFU |
|-------|-----|-----|
| All keys (any key may be evicted) | `allkeys-lru` | `allkeys-lfu` |
| Volatile keys only (only keys with a TTL set) | `volatile-lru` | `volatile-lfu` |

- Use an `allkeys-*` policy when every key in the cache should be evictable under memory
  pressure. This is the typical choice for a cache-only Redis instance.
- Use a `volatile-*` policy only when some keys must never be evicted (they carry no TTL),
  while others (with a TTL set) may be evicted. If no volatile keys exist when memory
  pressure occurs, `volatile-*` policies behave like no-eviction and writes will fail.
- For **TTL-based expiry** (time-bounded validity), set a per-key `EXPIRE` on each entry.
  This is independent of `maxmemory-policy` and applies whether or not the cache is full.

### Step 4 — Account for Redis approximation behaviour

Redis LRU and LFU are **sampled approximations**, not globally exact algorithms (c030,
source anchor h0040). Rather than scanning all keys, Redis samples a subset of keys and
evicts the worst candidate from that sample. In practice the approximation tracks the
statistical expectation closely, but precision is not guaranteed.

- If eviction precision is critical for the workload, note that the sample size is
  configurable (`maxmemory-samples`); a larger sample improves accuracy at the cost of
  additional CPU per eviction.
- State this limitation explicitly when recommending LRU or LFU for latency-sensitive
  workloads.

### Step 5 — Diagnose thrashing (if present)

Cache thrashing occurs when recently evicted entries are re-requested almost immediately,
creating a cycle of evict → miss → re-fetch → evict (c023, source anchor h0035).

To diagnose:
1. Confirm the symptom: miss rate is elevated and the same keys are being evicted and then
   re-populated repeatedly.
2. Determine the cause:
   - **Wrong algorithm** for the workload's distribution shape → switch policy (Step 2–3).
   - **Cache is undersized** for the working dataset → increasing capacity may be required
     in addition to or instead of changing the policy (P006 cross-reference).
3. Do not assume one cause without evidence; both may be present simultaneously.

### Step 6 — State confidence and flag if measurement is needed

If the access distribution is not known or only assumed:
- Label the recommendation as a **starting point** pending measurement.
- Describe what to measure (e.g., key-access frequency distribution, recency of re-requests
  after eviction) and for how long before treating the result as confirmed.

## Output

A recommendation that includes:

1. The identified (or assumed) access-distribution shape, with confidence level.
2. The candidate algorithm (LRU, LFU, or TTL expiry) with the specific Redis
   `maxmemory-policy` value or per-key `EXPIRE` guidance.
3. Whether `allkeys-*` or `volatile-*` scope applies, with the reason.
4. A note on the approximation behaviour of Redis LRU/LFU if precision matters.
5. A thrashing diagnosis and remediation (algorithm change, capacity increase, or both),
   if thrashing symptoms were reported.
6. A flag indicating if measurement or trial is needed before the recommendation can be
   treated as confirmed.

The output is a recommendation document. No executable configuration files or scripts are
produced.

## References

- `references/eviction-strategy-comparison-table.md` — algorithms compared side by side.
- `references/redis-maxmemory-policy-cheatsheet.md` — all Redis policy names and their
  scopes.
- P005 in `principles/principles.yaml` — governing principle for eviction policy selection.
- P006 in `principles/principles.yaml` — scaling diagnosis (storage-limit vs resource-limit)
  when thrashing is caused by insufficient capacity.

## Provenance

Principle P005; evidence records e012 (c023, TTL eviction — source anchor h0033),
e013 (c026, comparing eviction types including LRU/LFU/random — source anchor h0036,
evidence_strength: moderate, support_level: partially_supported), e014 (c029, Redis
maxmemory-policy configuration — source anchor h0039), e015 (c030, Redis approximation
algorithms — source anchor h0040). Cache thrashing described at source anchor h0035.
Source: Atchison (2021), *Caching at Scale with Redis* — distillation-only; no verbatim
quotation. Eviction policy selection is heuristic; LRU/LFU preference is situation-dependent
and the source explicitly hedges that no universal verdict is available (e013 limitations).
