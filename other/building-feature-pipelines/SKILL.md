---
name: building-feature-pipelines
description: Build ML feature pipelines and feature stores — point-in-time-correct joins to avoid label leakage, offline/online parity, feature freshness and backfills, and materialization with tools like Feast. Use when engineering features for ML, preventing train/serve skew or data leakage, building a feature store, or backfilling historical features for training.
---

# Building Feature Pipelines

## When to use

- Engineering features for ML models from warehouse/stream data.
- Preventing label leakage and train/serve skew.
- Setting up a feature store, online serving, or historical backfills.
- Do NOT use for general modeling/aggregation (use dbt/Spark skills) unless it
  feeds ML features.

## Workflow

```
- [ ] Define each feature with an entity key and an event timestamp
- [ ] Build training sets with point-in-time-correct joins (as-of the label time)
- [ ] Share ONE definition for offline (training) and online (serving)
- [ ] Set freshness/materialization for online features
- [ ] Backfill historical features idempotently for training
```

1. **Point-in-time correctness.** Join features as of each label's timestamp — use
   only data that was known before the prediction time. This prevents **label
   leakage**, the most damaging feature bug.
2. **Offline/online parity.** Compute a feature the same way for training (offline,
   batch) and serving (online, low-latency). Divergent logic causes **train/serve
   skew** and silent production degradation.
3. **Freshness.** Online features must be materialized on a schedule that meets the
   model's staleness tolerance.
4. **Idempotent backfills.** Recomputing historical features must be repeatable
   (see `designing-backfills-and-replays`).

## Patterns

**Point-in-time (as-of) join** — pick the latest feature value strictly before
each label event:

```sql
SELECT l.entity_id, l.label_ts, f.value AS feature
FROM labels l
LEFT JOIN features f
  ON f.entity_id = l.entity_id
 AND f.event_ts <= l.label_ts          -- only past data; no leakage
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY l.entity_id, l.label_ts ORDER BY f.event_ts DESC) = 1;
```

**Single definition, two paths** — define the feature once (e.g. Feast
`FeatureView`); materialize to an offline store for training and an online store
for serving so both use identical logic.

**Freshness + materialization** — schedule online materialization; monitor feature
freshness like any dataset SLA (`implementing-pipeline-observability`).

## Common pitfalls

- **Label leakage** — joining features computed after the label time inflates
  offline metrics and collapses in production; always as-of join.
- **Train/serve skew** — separate offline and online implementations drift; share
  one definition.
- **Stale online features** — model serves on old values; set and monitor
  freshness.
- **Non-reproducible backfills** — inconsistent training history; make feature
  recomputation idempotent.
- **No entity/timestamp keys** — features can't be joined correctly across time;
  require both.
- **Unversioned features** — silent redefinition breaks model comparability;
  version feature definitions.
