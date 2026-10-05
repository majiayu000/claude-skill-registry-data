---
name: feature-store-design
description: "The pitch is often \"a central place to store features,\" which undersells it into"
---

# Feature Store Design (Verbose)

## Core Patterns

### Why a Feature Store Exists

The pitch is often "a central place to store features," which undersells it into
sounding like a database with a marketing team. The actual justification is
narrower and sharper: **training/serving skew**.

The default failure looks like this. A data scientist writes a Spark job computing
`orders_30d` from the warehouse and trains a model that scores 0.89 AUC. An
engineer implements the serving path in the API service, reading from Postgres,
and reimplements `orders_30d` from the schema — using a 30-day window that includes
today, while the offline version excluded the current partition. Nothing errors.
Every test passes. The model scores 0.71 in production and it takes six weeks to
find out why.

A feature store's core promise is one definition with two materializations: the
transformation is written once, and the platform materializes it to an offline
store for training and an online store for serving. Everything else — discovery,
reuse, lineage — is real but secondary.

### Offline and Online Stores

| Dimension | Offline store | Online store |
|---|---|---|
| Query shape | Scan + aggregate, millions of rows | Key lookup, 1–500 entities |
| Latency target | Seconds to minutes | p99 < 10 ms |
| Retention | Full history, all timestamps | Latest value per entity |
| Typical backend | Parquet/S3, BigQuery, Snowflake, Delta | Redis, DynamoDB, Cassandra, Bigtable |
| Consumers | Training, backfill, analysis, drift jobs | Live inference |
| Cost driver | Storage volume | Memory footprint and QPS |

The online store deliberately keeps only the current value per entity. That is what
makes a 2 ms lookup possible, and it is also why you cannot build a training set
from it — there is no history to reconstruct what a feature looked like last March.

Materialization is the bridge: a scheduled job reads the offline table and writes
current values into the online store.

```python
store.materialize_incremental(end_date=datetime.now(tz=timezone.utc))
```

Treat this job as production-critical. When it silently stops, inference keeps
returning 200s with month-old features.

### Point-in-Time Correctness

This is where the real engineering is, and where naive implementations leak labels.

The rule: for a training example whose label is observed at time `T`, every feature
must be the value **as it was known at `T`**. Not the current value. Not the value
at end of that day. The value visible to a system running at that instant.

```
label:    customer 42, churned=1, event_ts = 2026-03-15 09:00
features: customer 42, orders_30d = 12, feature_ts = 2026-03-10
          customer 42, orders_30d = 3,  feature_ts = 2026-03-14   ← use this
          customer 42, orders_30d = 0,  feature_ts = 2026-03-20   ← leaked
```

The third row is what leakage looks like. `orders_30d = 0` after the churn is
practically the label itself; a model trained on it learns "zero orders means
churn," reaches 0.97 AUC offline, and is useless in production because at scoring
time the customer has not churned yet.

```sql
-- ✅ Correct: as-of join on the feature timestamp
select
    l.customer_id,
    l.event_ts,
    l.churned,
    f.orders_30d,
    f.avg_basket_usd
from labels l
asof join customer_stats f
  on l.customer_id = f.customer_id
 and f.feature_ts <= l.event_ts

-- ✅ Portable equivalent where ASOF JOIN is unavailable
select * from (
  select l.customer_id, l.event_ts, l.churned, f.orders_30d, f.feature_ts,
         row_number() over (
           partition by l.customer_id, l.event_ts
           order by f.feature_ts desc
         ) as rn
  from labels l
  join customer_stats f
    on f.customer_id = l.customer_id
   and f.feature_ts <= l.event_ts
   and f.feature_ts >  l.event_ts - interval '7' day   -- respect the TTL
) where rn = 1

-- ❌ Wrong: no temporal condition; pulls whatever the feature is now
select l.*, f.orders_30d
from labels l join customer_stats f on l.customer_id = f.customer_id
```

The TTL lower bound in the correct version matters. Without it, a customer with no
feature row for two years still gets matched to an ancient value, and the model
learns from data that would have been considered stale and unusable at serving time.

A feature store's `get_historical_features` implements exactly this join for you:

```python
training_df = store.get_historical_features(
    entity_df=labels_df,                    # must contain entity keys + event_timestamp
    features=[
        "customer_stats:orders_30d",
        "customer_stats:avg_basket_usd",
    ],
).to_df()
```

Reaching for this API and then not passing real per-row event timestamps — using
`datetime.now()` for every row, say — silently discards the whole guarantee.

### Entities, Feature Views, and Definitions

```python
from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64

customer = Entity(name="customer", join_keys=["customer_id"])

source = FileSource(
    path="s3://feature-store/customer_stats.parquet",
    timestamp_field="event_ts",              # when the feature value became true
    created_timestamp_column="created_ts",   # when the row was written — for dedup
)

customer_stats = FeatureView(
    name="customer_stats",
    entities=[customer],
    ttl=timedelta(days=7),
    schema=[
        Field(name="orders_30d", dtype=Int64),
        Field(name="avg_basket_usd", dtype=Float32),
        Field(name="days_since_last_order", dtype=Int64),
    ],
    source=source,
)
```

Both timestamps are load-bearing. `timestamp_field` is *event time* and drives the
point-in-time join. `created_timestamp_column` is *processing time* and resolves
which row wins when a backfill rewrites history for the same event time.

Serving is the mirror image of the training read:

```python
features = store.get_online_features(
    features=["customer_stats:orders_30d", "customer_stats:avg_basket_usd"],
    entity_rows=[{"customer_id": 42}],
).to_dict()
```

Same feature names, same definitions, different store. If a serving path constructs
feature values by any other route, the guarantee is gone.

### Freshness, TTL, and Staleness

| Feature class | Update cadence | Backing computation |
|---|---|---|
| Static attributes (signup country) | On change | CDC or nightly batch |
| Daily aggregates (orders_30d) | Nightly | Batch job |
| Session aggregates (clicks_5m) | Streaming | Kafka + windowed aggregation |
| Request-time (basket size now) | Per request | Computed in the request, not stored |

The last row is worth naming: not every feature belongs in a store. Values known
only at request time should be computed on the request path and passed to the model
alongside the fetched features.

Give every feature view a TTL and monitor materialization lag as a first-class
metric. Feature staleness is the most common silent ML production failure —
throughput is normal, error rate is zero, and predictions are made from data three
weeks old.

```
alert: feature_materialization_lag_seconds{view="customer_stats"} > 7200
alert: feature_online_null_rate{view="customer_stats"} > 0.02
```

### Verifying Skew Is Actually Gone

Having a feature store does not prove you have no skew. Verify it: log the features
actually served at inference time, then recompute the same features offline for the
same entity and timestamp, and compare.

```python
mismatch = (
    served.merge(recomputed, on=["customer_id", "event_ts"], suffixes=("_srv", "_off"))
          .assign(delta=lambda d: (d.orders_30d_srv - d.orders_30d_off).abs())
)
assert (mismatch.delta > 0).mean() < 0.001
```

Logging served feature vectors also gives you drift monitoring and per-prediction
debuggability for free — see `model-monitoring`.

### When Not to Build One

| Situation | Recommendation |
|---|---|
| One model, batch scoring, one team | Versioned table + shared transformation module |
| Several models sharing features | Feature store pays for itself |
| Real-time inference with < 100 ms budget | Online store is effectively required |
| Features change definition weekly | Stabilize definitions first; a store will not fix churn |

Adopting a feature store for a single batch model buys operational cost — a
materialization job, an online store to run, a registry to keep current — against
a problem you do not yet have. For pipeline orchestration around training and
deployment, see `mlops-pipeline-design`; for batch-versus-realtime serving choices,
see `batch-vs-realtime-scoring`.

## Common Anti-Patterns

❌ **Feature logic implemented twice, once for training and once for serving.**
✅ One definition, materialized to both stores by the same pipeline.

❌ **Joining features to labels on entity key alone.**
✅ As-of join bounded by both the label timestamp and the feature TTL.

❌ **Using `datetime.now()` as the event timestamp for every training row.**
✅ Real per-row event timestamps; otherwise the point-in-time join is decorative.

❌ **Treating the online store as a general database** — scanning it, running
analytics on it, expecting history from it.
✅ Key lookups only; history lives offline.

❌ **No TTL and no materialization-lag alert.**
✅ Explicit freshness contract per feature view, alerted on.

❌ **Trusting that the store eliminated skew without measuring it.**
✅ Log served features and reconcile against offline recomputation.

❌ **Putting request-time values in the store** — they are stale the moment they
are written.
✅ Compute them on the request path and pass them to the model directly.

❌ **Anonymous features** (`feature_v2_final_new`) with no owner or description.
✅ Registry entries with owner, definition, source, and change history.

## Feature Store Checklist

- [ ] Each feature has exactly one definition, used by training and serving
- [ ] Offline store holds full history with event timestamps
- [ ] Online store holds latest value only, sized for p99 lookup target
- [ ] Training sets built with a point-in-time-correct as-of join
- [ ] As-of join bounded below by the feature TTL
- [ ] Entity keys and join keys explicitly modeled
- [ ] Both event time and processing time recorded on feature rows
- [ ] TTL declared per feature view
- [ ] Materialization lag monitored and alerted
- [ ] Online null / missing-key rate monitored
- [ ] Served feature vectors logged with prediction id and model version
- [ ] Skew verified by reconciling served vs offline-recomputed values
- [ ] Request-time features computed on the request path, not stored
- [ ] Registry records owner, description, and source for every feature
- [ ] Backfill path exists and produces values identical to the streaming path
