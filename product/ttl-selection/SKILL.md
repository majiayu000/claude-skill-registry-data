---
name: ttl-selection
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

# TTL Selection

## Purpose

Choose a time-to-live duration that bounds the staleness window of cached values to a level
the application can tolerate, while recognising that TTL expiry reduces but does not eliminate
inconsistency (P004). When approximate freshness is sufficient — for example, social counters
or slowly-changing configuration — TTL is the right consistency mechanism. When strong
consistency is required — for example, financial balances or inventory counts — TTL alone is
insufficient and the skill routes the caller to explicit invalidation or write-through instead.

## When to use

- The application has stated a maximum acceptable staleness window and can tolerate reads that
  are slightly out of date within that window.
- The data changes occasionally or regularly but not on every access (dynamically-changing
  backing data is explicitly in scope per the source, h0105).
- Simpler consistency mechanisms are preferred over explicit invalidation, and the use case
  does not require that every read reflects the most recent write.

Do not use this skill when:

- Any stale read would cause a correctness, financial, or safety failure (P004
  `does_not_apply_when`). Route to `cache-invalidation-design` for explicit invalidation or
  write-through patterns instead.
- The data is immutable or append-only (no inconsistency risk; TTL adds no benefit over a
  permanent entry).

## Inputs

| Input | Required | Description |
|---|---|---|
| Maximum staleness tolerance | Yes | The longest period of stale data the caller's application can accept, expressed in concrete units (seconds, minutes, hours). |
| Consistency requirement | Yes | Whether strong consistency (every read reflects the latest write) or approximate freshness (bounded staleness) is required. |
| Data change frequency | Recommended | How often the backing data changes — informs whether the TTL will be hit frequently or rarely. |
| Deployment topology | Recommended | Single-node or geographically distributed / multi-node cache — affects whether cross-node propagation lag must be added to the TTL calculation. |
| Eviction policy in use | Optional | The configured `maxmemory-policy` — TTL-based per-key expiry is distinct from the eviction algorithm and both can be active simultaneously (P005). |

## Procedure

### Step 1: Gate on consistency requirement

Ask whether a stale read would cause a correctness, financial, or safety failure.

- If yes: **do not proceed with TTL-only consistency.** The root cause is that the backing data
  changes without the cache being updated (c055, root cause 1), and the mitigation must be
  explicit invalidation on write or write-through (P003). Redirect to the
  `cache-invalidation-design` skill. Document the reason for the redirect.
- If no (approximate freshness is acceptable): continue to Step 2.

Examples of approximate-freshness contexts (acceptable for TTL): social engagement counters,
product catalogue entries, feature-flag configuration, recommendation lists.

Examples of strong-consistency contexts (not acceptable for TTL alone): financial account
balances, inventory stock counts, access-control permissions.

### Step 2: Identify the root cause of potential inconsistency

Classify which consistency failure mode applies (c055, P003):

- **Root cause 2 — update propagation lag:** The backing store changes and the cache is
  notified, but there is a delay before the cached value is updated (h0105). TTL bounds the
  window during which a stale value may be served.
- **Root cause 3 — cross-node inconsistency:** In geographically distributed or highly scaled
  caches, different nodes may temporarily hold different values while an update propagates
  (h0106, c059). TTL alone does not prevent inter-node divergence but does limit how long a
  single stale entry persists on any node.

If root cause 1 (underlying data changes with no cache update at all) is the dominant mode and
no invalidation mechanism is in place, TTL is only a partial mitigation: stale entries will
persist for up to one full TTL period after each change. If the update rate is high relative
to the TTL, consider adding explicit invalidation on write (P003) alongside TTL as a safety
net.

### Step 3: Derive the TTL value from the acceptable staleness window

Set TTL to equal the maximum staleness the application can tolerate (c057). The TTL is a
direct expression of that tolerance:

- A shorter TTL reduces the maximum staleness but increases the miss rate, driving more
  requests to the backing data source.
- A longer TTL reduces backing-source load but widens the window during which stale data may
  be served.

Concrete derivation approach:

1. Obtain the caller's maximum staleness tolerance (e.g. "counters may be up to 60 seconds
   stale").
2. Set TTL = that duration (e.g. 60 seconds).
3. If the backing data changes on a known schedule (e.g. refreshed every 5 minutes), a TTL
   longer than the refresh period wastes nothing and reduces unnecessary misses; a TTL shorter
   than the refresh period is the more conservative choice.

Do not fabricate or assume a staleness tolerance. If the caller has not stated one, ask before
proceeding.

### Step 4: Adjust for cross-node propagation lag (distributed deployments)

If the cache is geographically distributed or uses replica nodes (c059, h0106):

- The time to propagate an update to all nodes is additional latency on top of any per-key
  expiry.
- The effective staleness window from a client's perspective is: TTL + worst-case propagation
  lag.
- Reduce the TTL by the estimated propagation lag so that the total staleness window stays
  within tolerance.

Example: if the tolerated staleness is 120 seconds and cross-region propagation typically
takes 15 seconds, set TTL to 105 seconds or less.

For single-node deployments, propagation lag is zero and this adjustment is not required.

### Step 5: Confirm TTL is a per-key setting, separate from eviction policy

TTL expiry is applied per key (via Redis `EXPIRE` or inline at write time). It is not the same
as the `maxmemory-policy` eviction algorithm (P005). Both mechanisms can be active at the same
time:

- `maxmemory-policy` (e.g. `volatile-lru`, `allkeys-lfu`) determines which keys Redis removes
  when the cache is full.
- Per-key TTL determines when a specific key becomes eligible for expiry regardless of memory
  pressure.

Ensure the caller understands the distinction so that enabling an eviction policy is not
mistaken for having set TTL-based consistency, and vice versa.

### Step 6: Document the TTL decision

Produce the output artifact described below, recording the rationale so the TTL is not
adjusted later without revisiting the staleness-tolerance assumptions.

## Output

A TTL recommendation containing all of the following:

1. **Recommended TTL value** (explicit duration with units).
2. **Staleness window justification** — the maximum staleness the TTL is designed to bound,
   with the tolerance stated by the caller.
3. **Consistency class** — confirmation that approximate freshness is acceptable for this use
   case, or (if applicable) a redirect note explaining why TTL alone is insufficient and which
   alternative skill was invoked.
4. **Propagation-lag adjustment** (if distributed topology) — the propagation-lag estimate and
   how it was deducted from the raw TTL.
5. **Eviction-policy note** — a one-line statement that this TTL is per-key expiry and is
   independent of any configured `maxmemory-policy`.

## References

- `principles/principles.yaml` — P003 (consistency root causes), P004 (TTL inconsistency
  boundary rule), P005 (eviction policy selection).
- `evidence/evidence-records.yaml` — e026 (c055, h0103: three root causes), e027 (c057,
  h0105: TTL bounds staleness window), e028 (c058, h0105: TTL insufficient for financial
  data), e029 (c059, h0106: geo-distributed propagation lag).
- `skills/cache-invalidation-design/SKILL.md` — for explicit invalidation and write-through
  patterns when strong consistency is required.
- `references/redis-maxmemory-policy-cheatsheet.md` — `volatile-ttl` and TTL-aware eviction
  policy options.

## Provenance

Derived from principles P004 (primary), P003 (consistency root-cause classification), and P005
(TTL as eviction choice). Evidence records: e027 (c057, h0105), e028 (c058, h0105), e029
(c059, h0106), e026 (c055, h0103). Source: Atchison, "Caching at Scale With Redis" (2021),
distillation-only rights — no verbatim quotation of source text.
