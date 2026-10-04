---
name: cache-invalidation-design
kind: skill
status: ready
provenance:
  principles:
  - P002
  claims:
  - C00020
  - C00021
  - C00031
  - C00032
  - C00033
  - C00034
  - C00035
  evidence:
  - E00009
  - E00010
  - E00014
  - E00015
  - E00016
  - E00017
  - E00018
  source_anchors:
  - 11ebbc818b96-c0000
  - 11ebbc818b96-c0001
  authored_from_digest: 883848b1bcfcf1eea99091b00e82feb8930542a1172e7665f46de438b51f2ac7
---

# Cache Invalidation & Consistency Design

## Purpose

Select a cache consistency strategy grounded in the actual root cause of inconsistency for the
system under review — not a default pattern. The procedure requires naming one of three distinct
root causes (write-without-invalidation, propagation lag, or divergent distributed nodes) before
a mitigation can be chosen, ensuring that the chosen strategy addresses the real failure mode
rather than an assumed one (P003). Pattern ownership (cache-aside vs write-through vs
write-behind) is determined by the write-latency budget and staleness tolerance once the root
cause is identified (P010). TTL is evaluated as a bounded but incomplete remedy and is
accepted only when approximate freshness is explicitly sufficient (P004). Side effects are
audited first; the skill declines if the audit is incomplete (P002).

## When to use

- Designing or reviewing a cache that sits in front of data subject to writes.
- Selecting or changing the write strategy (cache-aside, write-through, write-behind) for an
  existing cache that is producing stale or inconsistent reads.
- Diagnosing a reported consistency failure and mapping it to a mitigation.
- Evaluating whether TTL alone is sufficient for a stated consistency requirement.
- Any scenario where the profile quality bar cites P003 or P004 as required checks.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Operation inventory: all state mutations the operation performs | Required | Needed for P002 side-effect gate |
| Maximum acceptable staleness window | Required | Drives TTL sizing and mitigation selection |
| Write-latency tolerance | Required | Drives choice between write-through and write-behind |
| Deployment topology: single-node or distributed / multi-region | Required | Determines whether root cause 3 is in scope |
| Consistency requirement level: approximate freshness or strong consistency | Required | Determines whether TTL is admissible |
| Current caching pattern (if reviewing an existing design) | Conditional | Required for diagnose/change scenarios |

## Procedure

### Step 1 — Side-effect gate (P002)

List every external state mutation the operation implies: database writes, counter decrements,
payment charges, message sends, or any other observable side effect. If the inventory is
incomplete, **decline** and request that the team complete the side-effect audit before
proceeding. Proceed only when either (a) the operation is read-only with no mutations, or (b)
every side effect is idempotent or has an explicit replay design that is documented and agreed
upon. Caching a side-effecting operation without this guard is a documented source of
application failures and outages (c008, anchor h0017).

### Step 2 — State the consistency target

Record two values from the caller:

- **Maximum staleness window**: the longest duration for which a stale cached value is
  acceptable. Express as a time bound (for example, "up to 60 seconds of lag is acceptable
  for display counters") or as "none — any stale read is unacceptable."
- **Write-latency budget**: the maximum additional latency the application can absorb on a
  write path (for example, "writes must complete in under 20 ms end-to-end").

These two values constrain mitigation selection in all subsequent steps.

### Step 3 — Name the root cause (mandatory before selecting a mitigation)

Examine the system description and identify **exactly which of the three root causes applies**.
Do not proceed to Step 4 until the root cause is named. More than one may apply; list all that
are present.

**Root cause 1 — Write-without-invalidation**
The backing data store is updated by one code path but the cache is not informed of the change.
The cached entry continues to be served until it expires or is evicted. Indicators: cache
returns a stale value immediately after a source update; no invalidation call is issued on
write; cache-aside pattern without explicit delete-on-write (c009, anchor h0018).

**Root cause 2 — Propagation lag**
An update is issued to the cache but takes time to reach all consumers. The entry is
technically scheduled for update but remains stale during the lag interval. Indicators:
updates are eventually visible but with a measurable delay; TTL-based expiry is already in
place but the staleness window is larger than expected; the system involves asynchronous write
paths (c055, anchor h0103).

**Root cause 3 — Divergent distributed nodes**
Multiple cache nodes in a distributed or multi-region deployment hold different values for the
same key at the same point in time. No single node has authoritative state. Indicators:
different nodes return different values for the same key; Active-Active or multi-primary
topology; geographic distribution (c057, c058, anchors h0105).

### Step 4 — Select the mitigation matched to each named root cause

Apply the following mapping. Where more than one root cause was identified, apply each
mitigation in combination.

**Root cause 1 mitigation — Explicit invalidation on write or write-through**

Choose based on the write-latency budget and staleness tolerance (P010):

- **Cache-aside with explicit invalidation**: the application deletes or marks invalid the
  cache entry at the moment the backing store is updated. The next read repopulates the
  cache from the store. This is the simplest baseline when the write path already belongs to
  the application and write latency must remain low (c015, anchor h0026). Accept that a brief
  window of staleness exists between the write and the delete if they are not atomic.
- **Write-through**: the cache and the backing store are updated synchronously in the same
  write operation. The cache owns consistency; stale reads are eliminated. Use when the
  staleness tolerance from Step 2 is "none — any stale read is unacceptable" and the
  write-latency budget can absorb the additional round-trip cost (c016, anchor h0027).
- **Write-behind (write-back)**: the cache is updated immediately and the backing store is
  updated asynchronously. Write latency is minimised. A brief inconsistency window exists
  until the asynchronous flush completes. Use only when the write-latency budget is very
  tight and approximate freshness is acceptable during the flush window (c012, anchor h0023).
  Document the flush interval and confirm it falls within the staleness window from Step 2.

Selection rule: if the staleness tolerance is "none", write-through is the only admissible
choice from this group. If the staleness tolerance is a stated time bound, cache-aside with
invalidation or write-behind are both candidates; choose based on the write-latency budget.

**Root cause 2 mitigation — TTL bounded to the staleness window (P004)**

Set the TTL to no greater than the maximum staleness window recorded in Step 2. TTL bounds
the inconsistency to that window; it does not eliminate inconsistency within the window
(c057, anchor h0105). Confirm the acceptability constraint:

- If the caller stated "approximate freshness is acceptable" (for example, social media view
  counters, leaderboard scores), TTL alone is admissible. Record the TTL value and the
  rationale.
- If the caller stated strong consistency or "any stale read is unacceptable" (for example,
  financial balances, inventory counts, access control decisions), **TTL alone is
  insufficient**. TTL must be combined with explicit invalidation or write-through from the
  root cause 1 mitigations above (c058, anchor h0105).

**Root cause 3 mitigation — CRDT-based Active-Active replication**

For distributed or multi-region caches where nodes diverge, the mitigation is Active-Active
replication with CRDT-based conflict resolution. Each node accepts writes locally at low
latency; CRDT semantics merge divergent states deterministically without manual conflict
resolution (c057, c058, anchors h0105). This topology requires Redis Enterprise; it is not
available in open-source Redis (profile forbidden_behaviours, P007). Before recommending this
mitigation, confirm with the team that Redis Enterprise is in scope.

### Step 5 — Check pattern ownership consistency (P010)

Review the caching pattern selected or in use against the mitigation chosen in Step 4:

- **Cache-aside**: the application owns every cache operation — lookup, miss handling,
  population, and invalidation. The pattern is compatible with explicit invalidation
  (root cause 1) and TTL (root cause 2). It is not compatible with zero-staleness
  requirements unless the application is disciplined about invalidation on every write path
  (c014, anchor h0025).
- **Write-through**: the cache layer owns consistency synchronously. Staleness is eliminated
  at the cost of write latency. Required if strong consistency is the stated target and
  write-through latency is within budget.
- **Write-behind**: the cache layer owns the write but flushes asynchronously. The flush
  interval creates a staleness window; confirm the window is within the tolerance from Step 2.

If the pattern in use and the mitigation from Step 4 are inconsistent — for example,
cache-aside without explicit invalidation where strong consistency is required — flag the
mismatch as a design gap and recommend the corrective change.

### Step 6 — Confirm TTL admissibility summary

Produce a one-line admissibility verdict for TTL:

- "TTL admissible: staleness tolerance of [X seconds] stated; TTL set to [Y seconds];
  approximate freshness confirmed as acceptable."
- "TTL insufficient: strong consistency required; explicit invalidation / write-through
  required in addition to or instead of TTL."

This verdict must appear in the output regardless of which root causes were identified.

## Output

A consistency design document containing all of the following:

1. **Side-effect verdict**: safe to proceed / decline pending audit, with the list of
   identified side effects or the reason for decline.
2. **Consistency target**: staleness window and write-latency budget as stated by the caller.
3. **Named root cause(s)**: one or more of the three root causes from Step 3, with the
   specific evidence from the system description that supports the identification.
4. **Mitigation per root cause**: the chosen strategy (explicit invalidation, write-through,
   write-behind, TTL bounded to staleness window, CRDT Active-Active), with the rationale
   linking back to the consistency target.
5. **Pattern ownership check**: confirmation that the selected caching pattern is consistent
   with the chosen mitigation, or a description of the mismatch and the corrective
   recommendation.
6. **TTL admissibility verdict**: the one-line verdict from Step 6.

The output is a recommendation document. No executable configuration or code is produced.

## References

- `skills/ttl-selection/SKILL.md` — detailed TTL sizing procedure when TTL is selected as
  part of the mitigation.
- `skills/active-active-conflict-assessment/SKILL.md` — CRDT conflict assessment when root
  cause 3 is identified and Active-Active is the mitigation.
- `references/redis-maxmemory-policy-cheatsheet.md` — Redis volatile-ttl and per-key EXPIRE
  options relevant to TTL-based expiry.

## Provenance

Primary grounding: P003 (three inconsistency root causes and their distinct mitigations —
c009/e006/h0018, c055/e026/h0103, c057/e027/h0105, c058/e028/h0105). Supporting: P010
(write-through/write-behind/cache-aside pattern ownership — c012/e008/h0023,
c014/e009/h0025, c015/e010/h0026, c016/e011/h0027). P004 (TTL bounds staleness but does
not eliminate inconsistency; insufficient for strong consistency — c057/e027/h0105,
c058/e028/h0105). P002 (side-effect gate — c008/e005/h0017). All source material from
"Caching at Scale With Redis" (Atchison 2021), rights status distillation-only; all content
paraphrased, no verbatim quotation.
