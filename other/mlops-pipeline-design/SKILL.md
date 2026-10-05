---
name: mlops-pipeline-design
description: "Software CI assumes a git sha plus a lockfile determines the build."
---

# MLOps Pipeline Design (Verbose)

## Core Patterns

### Reproducibility Requires Data Versioning, Not Just Code Versioning

Software CI assumes a git sha plus a lockfile determines the build. ML breaks
that: the same commit trained on Tuesday's table and Thursday's table produces
two different models, both labelled with the same sha.

A reproducible run pins code, data, and configuration under one identifier.

```python
@dataclass(frozen=True)
class RunFingerprint:
    git_sha: str            # code, including the feature library
    dataset_uri: str        # s3://lake/churn/snapshot_date=2026-06-01/
    dataset_sha256: str     # hash of the sorted file manifest (path, size, etag)
    params_hash: str        # hash of the resolved config, defaults included
    env_hash: str           # hash of requirements.lock / conda env

    def run_key(self) -> str:
        return sha256("|".join(astuple(self)).encode()).hexdigest()[:16]
```

Hash a *manifest* (sorted paths plus etags) rather than streaming terabytes: it
is cheap, stable, and detects files added, removed, or rewritten under you.

The most effective structural change is making stage one materialize an immutable
snapshot:

```sql
CREATE TABLE churn_snapshot_2026_06_01 AS
SELECT * FROM events WHERE event_ts < TIMESTAMP '2026-06-01 00:00:00';
```

Mutable sources make the "reproducible" pipeline a fiction. Re-running last
quarter's job against `SELECT * FROM events` trains on data that did not exist
then — and if those rows post-date the labels, you have manufactured leakage that
only shows up in production.

### Stage Decomposition and Caching

```
ingest → validate → build_features → train → evaluate → register(staging)
```

Each stage declares its inputs and outputs, so the orchestrator (Kubeflow,
Airflow, Metaflow, Dagster) can skip any stage whose inputs are unchanged.

| Stage | Cache key | Typically re-runs when |
|---|---|---|
| ingest | snapshot date | New snapshot |
| validate | dataset hash | New data |
| build_features | dataset hash + feature-lib sha | Data or transform change |
| train | features hash + params hash | Hyperparameter sweep |
| evaluate | model hash + holdout hash | New model |

Correct decomposition turns a hyperparameter sweep from hours of repeated
ingestion into minutes of training. One script doing everything makes each
experiment pay full price, which is why teams stop experimenting.

Fix the evaluation holdout by rule, not by random split per run:

```python
# ✅ Deterministic, stable across runs and comparable between models
holdout = df[hash_bucket(df.entity_id, 100) < 10]           # fixed 10%
train_df = df[hash_bucket(df.entity_id, 100) >= 10]

# ❌ A fresh random split per run makes two runs' AUCs incomparable
train_df, holdout = train_test_split(df, test_size=0.1)     # no seed, no rule
```

For time-series or any temporally ordered target, split by time, never at random:
a random split lets the model see the future for the same entity.

### Data Validation as a Blocking Gate

```python
def validate(df: pd.DataFrame) -> None:
    failures = []
    if len(df) < MIN_ROWS:
        failures.append(f"row count {len(df)} < {MIN_ROWS} — partial upstream load")
    if (unknown := (~df["plan"].isin(KNOWN_PLANS)).mean()) > 0.01:
        failures.append(f"unseen plan categories at {unknown:.3f}")
    if abs(df["label"].mean() - BASE_RATE) > 0.05:
        failures.append(f"label base rate {df['label'].mean():.3f} vs {BASE_RATE:.3f}")
    if failures:
        raise DataValidationError("; ".join(failures))
```

The rule is that validation *fails the run*. Emitting a warning into a dashboard
nobody reads is how a model gets trained on a half-loaded partition and shipped.

The subtle checks are the valuable ones: a shifted label base rate usually means
the label-generation join changed; a spike in unseen categories means an upstream
enum grew. Both train cleanly and degrade in production.

### Registry and Promotion

The training pipeline registers; it does not promote. Separating them is what
keeps a bad Tuesday-night run from reaching users.

```python
result = evaluate(model, holdout)
champion = registry.get_model("churn", alias="production")
champion_metrics = evaluate(champion, holdout)      # SAME holdout, both models

if result.auc < champion_metrics.auc - REGRESSION_TOLERANCE:
    raise PipelineFailed(f"AUC regression: {result.auc:.4f} vs {champion_metrics.auc:.4f}")

for segment, m in result.by_segment.items():        # aggregate wins can hide harm
    if m.auc < champion_metrics.by_segment[segment].auc - SEGMENT_TOLERANCE:
        raise PipelineFailed(f"segment regression in {segment}")

registry.register("churn", model, stage="staging", fingerprint=fp.run_key())
```

Per-segment comparison is the check most pipelines lack. A model can gain 0.004
AUC overall while losing badly on a small but important cohort.

### Feature Definitions vs Materialization

One definition, two materializations, is the structural answer to training/serving
skew (covered operationally in the ML deployment skill).

The offline path must be **point-in-time correct**: joining a label at time *t*
to feature values as of *t*, not as of now. Naively joining a current feature
table to historical labels is the single most common cause of an offline AUC that
does not survive contact with production.

```python
# ✅ as-of join: each label row gets the feature value that existed at its timestamp
training_df = store.get_historical_features(
    entity_df=labels[["user_id", "label_timestamp", "label"]],
    features=["orders_30d", "account_age_days"],
)
```

### Orchestration and Triggers

| Trigger | Fires on | Good for | Watch out for |
|---|---|---|---|
| Schedule | Cron | Stable, slow-moving domains | Burns compute when nothing changed |
| Data arrival | New partition landed | Batch pipelines | Needs a reliable completion signal |
| Drift alarm | Monitoring signal | Fast-moving distributions | Retraining on drifted data can bake in the drift |
| Code merge | Feature-library change | Any pipeline | Requires a fast, trustworthy eval gate |
| Manual | Human decision | High-stakes models | Becomes the bottleneck |

Retraining on a drift alarm deserves care: if the drift is a genuine distribution
change, retraining is right; if it is an upstream data bug, retraining hard-codes
the bug into the model. Gate automatic retraining on validation passing first.

## Common Anti-Patterns

❌ **Versioning the code but not the data.**
✅ Record the dataset URI and manifest hash in every run; snapshot mutable sources as stage one.

❌ **Reading `SELECT * FROM events` at training time.**
✅ Read an immutable, date-partitioned snapshot so old runs stay reproducible.

❌ **A single monolithic `train.py` that ingests, transforms, trains, and uploads.**
✅ Discrete stages with explicit inputs, outputs, and content-hash caching.

❌ **Random train/test split regenerated per run.**
✅ Deterministic hash-bucket split, fixed across runs — and split by time whenever
the target is temporally ordered, since a random split leaks the future.

❌ **Data quality checks that log a warning.**
✅ Checks that raise and fail the run before compute is spent.

❌ **The training job promoting its own output to production.**
✅ Register to staging; promotion is a separate, gated decision.

❌ **Absolute metric thresholds as the quality gate.**
✅ Compare against the live champion on the identical holdout, overall and per segment.

❌ **Feature transforms defined inside the training script.**
✅ A shared feature library or feature store with point-in-time-correct historical retrieval.

❌ **Hyperparameters edited in the source and lost after the run.**
✅ Resolved config logged as run parameters, defaults included.

## MLOps Pipeline Checklist

- [ ] Every run records git sha, dataset URI, dataset hash, params, and env hash
- [ ] Mutable sources snapshotted immutably as the first stage
- [ ] Pipeline decomposed into independently re-runnable, cacheable stages
- [ ] Data validation raises and blocks the run
- [ ] Row-count, null-rate, category-cardinality, and label-base-rate checks in place
- [ ] Holdout split deterministic and stable across runs; time-based where the
      target is temporally ordered
- [ ] Historical feature retrieval is point-in-time correct
- [ ] Feature definitions shared between training and serving
- [ ] Evaluation compares against the live champion on the same holdout
- [ ] Per-segment regression check, not just an aggregate metric
- [ ] Training registers to staging; promotion is a separate decision
- [ ] Retraining triggers defined beyond a bare cron schedule
- [ ] Automatic retraining gated on data validation passing
- [ ] Any past model rebuildable from its recorded fingerprint alone
