---
name: batch-vs-realtime-scoring
description: "The choice is not about scale or sophistication."
---

# Batch vs Realtime Scoring (Verbose)

## Core Patterns

### The Decision Framework

The choice is not about scale or sophistication. It is about whether the model's
inputs can change between the moment you would precompute and the moment the
prediction is used.

| Dimension | Batch scoring | Realtime scoring |
|---|---|---|
| Entity set | Enumerable in advance | Unknown until the request |
| Input freshness | Hours to days old | Sub-second |
| In-session context | Unavailable | Available |
| Latency at use | 1–5 ms (a lookup) | 20–200 ms (full path) |
| Cost per 1M predictions | Cents (one job, spot instances) | Dollars (always-on capacity) |
| Failure mode | Stale scores, degrades gracefully | User-visible error or timeout |
| Operational burden | A scheduled job | Autoscaling, warm pools, canaries |
| Model size ceiling | Effectively none | Bounded by the latency budget |

Worked examples: **churn propensity** — known user set, features move over days,
consumed by an email campaign — batch, decisively. **Card-present fraud** — the
transaction does not exist until it happens and the decision blocks a payment —
realtime, no alternative. **Search ranking** — the query is unknown but the
corpus is known — hybrid: precomputed item embeddings, realtime query scoring.

A common and expensive error is choosing realtime because the model is "for a
user-facing product", when the score is read from a nightly-refreshed profile.

### Batch Scoring

```python
def nightly_scoring(snapshot_date: str) -> None:
    ids, features = load_active_entities(snapshot_date)     # point-in-time features
    scores = model.predict_proba(features)[:, 1]

    with redis.pipeline() as p:
        for uid, s in zip(ids, scores):
            p.setex(f"churn:{uid}", 60 * 60 * 36, f"{s:.6f}")   # 36h TTL > 24h cadence
        p.execute()

    warehouse.write(f"scores/churn/dt={snapshot_date}/",       # history, not just cache
                    pd.DataFrame({"entity_id": ids, "score": scores,
                                  "model_version": MODEL_VERSION}))
```

Three details separate a working batch system from a fragile one:

- **TTL longer than the cadence.** Without it, one failed run empties the store.
  With it, consumers read a slightly stale score and nothing breaks.
- **Write to a warehouse table as well as the cache.** Monitoring, backfills, and
  "what did we say about this account in March" all need the history.
- **Handle the cold entity.** A user created after the last run has no score. Use
  an explicit default — the base rate or a cheap heuristic — rather than a null
  that a downstream service interprets as zero.

```python
score = redis.get(f"churn:{uid}")
if score is None:
    metrics.increment("score.miss")
    score = POPULATION_BASE_RATE          # explicit default, not None
```

Cost is the underrated advantage: a nightly spot-instance job scoring ten million
entities costs a few dollars, while the equivalent always-on realtime tier costs
orders of magnitude more and needs on-call coverage.

### Realtime Scoring and the Latency Budget

Write the budget down before designing anything, at p99 — averages hide exactly
the tail that times out.

```
p99 end-to-end budget            50 ms
  ingress + TLS + serialization   8 ms
  feature retrieval              20 ms   <- the design problem
  preprocessing + inference      10 ms
  business logic + response       5 ms
  headroom                        7 ms
```

Inference is rarely the bottleneck — a gradient-boosted tree scores a row in
microseconds, a small neural net in a few milliseconds on CPU. Feature retrieval
is where the budget goes.

**The consequence: realtime scoring forces feature precomputation.** A feature
like `orders_30d` requires scanning a month of events — a multi-second query that
no index tuning fits into 20 ms. The aggregation must already exist when the
request arrives.

A stream processor (Flink, Spark Structured Streaming) maintains the aggregation
in an online store; the request path does a single-digit-millisecond point
lookup. Split every feature by volatility:

| Tier | Freshness | Computed by | Examples |
|---|---|---|---|
| Static / slow | Daily | Batch job | account_age, segment, lifetime_value |
| Streaming | Seconds–minutes | Stream processor | orders_1h, failed_logins_5m, velocity |
| Request-time | Immediate | Inline, in-process | amount, merchant_id, device, hour_of_day |

The request-time tier must be pure arithmetic on the request payload; the moment
it needs I/O, it belongs in another tier.

Retrieve in one round trip, and always bound the wait:

```python
# ❌ N round trips: 12 features × 3 ms = 36 ms, blowing the budget
feats = {name: redis.get(f"{name}:{uid}") for name in FEATURE_NAMES}

# ✅ One round trip, with a timeout
try:
    values = await asyncio.wait_for(
        store.mget([f"{n}:{uid}" for n in FEATURE_NAMES]), timeout=0.020)
    feats = dict(zip(FEATURE_NAMES, values))
except asyncio.TimeoutError:
    metrics.increment("feature_store.timeout")
    feats = DEFAULT_FEATURES              # degrade, never hang the request
```

A model that cannot answer within budget is worse than a heuristic that can. Every
realtime scoring path needs a defined fallback — a cached previous score, a simple
rule, or a fixed default — chosen deliberately and load-tested.

### The Hybrid Pattern

Most large systems precompute the expensive stage offline and run a cheap,
context-aware stage inline.

```python
def recommend(user_id: str, session: Session, k: int = 20) -> list[Item]:
    candidates = redis.lrange(f"cands:{user_id}", 0, 499)   # batch, ~2 ms lookup
    ctx = {"items_viewed": session.viewed, "dwell": session.dwell_ms,
           "hour": datetime.now(timezone.utc).hour}
    return reranker.top_k(candidates, ctx, k=k)             # realtime, ~15 ms
```

The economics work because retrieval over millions of items is expensive and
tolerates staleness, while re-ranking a few hundred is cheap and needs freshness.
Cost per prediction should be compared across options before committing.

A second hybrid shape is **precompute-then-adjust**: serve a nightly batch score,
then apply realtime overrides for a few fast-moving signals (a fraud flag raised
an hour ago, a subscription cancelled this morning).

### Consistency Between Paths

The moment a system has both a batch and a realtime path, it has two
implementations of the same feature, and they will diverge — the training/serving
skew described in the ML deployment skill, arriving through a different door.

Share the definition, but be aware that shared code does not guarantee shared
semantics. Three divergences are worth checking explicitly:

- **Window boundaries.** Batch computes "last 30 days as of midnight UTC";
  streaming computes "trailing 30 days from now". At 23:00 those differ by a day.
- **Late-arriving events.** The batch job sees an event that landed after the
  streaming watermark passed. The two counts will not match, permanently.
- **Null handling.** A missing streaming key returns `None`; the batch job's join
  produced `0`. The model treats those very differently.

Reconcile continuously: sample entity ids, fetch both the online and the offline
value, and publish the p99 absolute delta as a gauge. A gap that grows is a bug
you would otherwise find during an incident.

## Common Anti-Patterns

❌ **Choosing realtime because the product is user-facing.**
✅ Choose by input freshness. A user-facing page reading a daily-refreshed profile wants batch.

❌ **Computing aggregations with a query in the request path.**
✅ Precompute into an online store; the request path does point lookups only.

❌ **Stating the latency budget as an average.**
✅ Budget at p99 — the tail is what times out and what users remember.

❌ **Unbounded waits on the feature store, or no fallback when the model is down.**
✅ Per-call timeouts plus a load-tested default — cached score, heuristic, or base rate.

❌ **Batch writes without a TTL longer than the run interval, or nulls for entities never scored.**
✅ TTL exceeding the cadence, plus an explicit cold-start default and a miss-rate metric.

❌ **Separate batch and streaming implementations of the same feature.**
✅ Shared definitions, plus a running reconciliation job that measures the gap.

## Scoring Architecture Checklist

- [ ] Required input freshness stated explicitly before choosing an architecture
- [ ] Batch chosen wherever the entity set is enumerable and staleness is tolerable
- [ ] Latency budget written at p99 and decomposed by stage
- [ ] Features tiered by volatility: static, streaming, request-time
- [ ] All non-trivial aggregations precomputed into an online store, retrieved in
      a single batched round trip
- [ ] Timeouts on every external call, with a load-tested fallback prediction
- [ ] Batch writes carry a TTL longer than the run interval
- [ ] Cold-start default defined; store miss rate monitored
- [ ] Scores persisted to a warehouse as well as the serving cache
- [ ] Batch and streaming feature definitions shared, with running reconciliation of
      values, window boundaries, and late-event semantics
