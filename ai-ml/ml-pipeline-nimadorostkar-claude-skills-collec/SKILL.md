---
name: ml-pipeline
description: Use when building or operating a machine learning pipeline. Covers feature engineering, training reproducibility, train/serve skew, deployment, monitoring for drift, and retraining.
metadata:
  category: ai
  version: 1.0.0
  tags: [mlops, pipeline, features, drift, deployment]
---

# ML Pipeline

## Purpose

Build a machine learning pipeline that produces the same model twice and behaves in production the way it did in training. The two defining failure modes are irreproducible training and train/serve skew — the model sees different features in production than it saw in training, and quietly degrades.

## When to Use

- Building a training or inference pipeline.
- A model that performed well offline and poorly in production.
- Setting up monitoring for a deployed model.
- Establishing a retraining cadence.

## Capabilities

- Feature engineering and feature-store design.
- Reproducible training: data versioning, seeds, environment pinning.
- Train/serve consistency.
- Deployment: batch, real-time, shadow.
- Monitoring: data drift, prediction drift, performance decay.

## Inputs

- The prediction task and the label definition.
- The data: its sources, its freshness, and its leakage risks.
- Latency and throughput requirements at serving time.

## Outputs

- A reproducible training pipeline with a versioned dataset and model.
- Features computed by the same code in training and serving.
- Drift and performance monitoring with alerts.

## Workflow

1. **Define the label precisely** — Including the time at which it becomes known. A label that is only available thirty days after the prediction cannot be used to evaluate a model deployed today, and this constraint shapes everything.
2. **Check for leakage first** — Any feature computed from information that would not exist at prediction time will make the offline model look excellent and the production model useless. This is the most common and most expensive ML bug.
3. **Compute features once, use them twice** — The same code path for training and serving. Two implementations of the same feature will diverge, silently, and the model will degrade without any code changing.
4. **Version everything** — Data, code, environment, hyperparameters, and the model artifact. "Which data produced this model" must be answerable a year later.
5. **Shadow before you serve** — Run the new model on live traffic, log its predictions, and compare — without acting on them.
6. **Monitor drift and performance** — Input distribution, prediction distribution, and (when labels arrive) actual accuracy. A model degrades silently; nothing errors.

## Best Practices

- Target leakage is the defining ML failure. If a feature is suspiciously predictive, it is almost certainly leaking. A model with 0.99 AUC on a hard problem is not a triumph; it is a bug.
- Time-based splits, not random splits, for any problem with a temporal component. A random split lets the model see the future, and the offline score is then a fiction.
- A feature store exists to solve train/serve skew. If you do not have one, use one code path — never two implementations of the same feature.
- Monitor the input distribution, not just the model's accuracy. Accuracy requires labels, which arrive late; drift in the inputs is visible immediately and is the early warning.
- A model that has not been retrained in a year is running on a world that no longer exists. Set a cadence and a trigger.
- Baseline against something trivial. If a logistic regression on three features is within a point of your deep model, ship the logistic regression.

## Examples

**Target leakage — the bug that looks like success:**

```python
# The task: predict at signup whether a user will churn within 90 days.
features = [
    "plan_tier",
    "signup_channel",
    "company_size",
    "days_since_last_login",       # LEAK: computed from the full history, including
                                   # after the churn event. In production, at signup,
                                   # this is always 0.
    "total_support_tickets",       # LEAK: counts tickets over the whole lifetime,
                                   # including ones filed after the prediction point.
    "cancelled_at_is_null",        # LEAK: this IS the label, wearing a hat.
]
# Offline AUC: 0.97. Production AUC: 0.54 — barely better than a coin flip.

# Correct: every feature must be computable using only data available at the
# prediction timestamp.
features_at_prediction_time = [
    "plan_tier",
    "signup_channel",
    "company_size",
    "signup_day_of_week",
    "referrer_domain",
]
# Offline AUC: 0.71. Production AUC: 0.69. Honest, and actually useful.
```

**One code path for features, in training and in serving:**

```python
# The feature definition lives in exactly one place.
@feature_view(entities=[user], ttl=timedelta(days=90))
def user_activity_features(df: DataFrame) -> DataFrame:
    return df.assign(
        orders_last_30d=count_orders(df, window="30d"),
        avg_order_cents=avg_order_value(df, window="90d"),
        days_since_first_order=days_since(df, "first_order_at"),
    )

# Training reads it as of a historical point in time (point-in-time correct join).
train = store.get_historical_features(
    entity_df=labels,                  # each row has an event_timestamp
    features=["user_activity_features:orders_last_30d", ...],
)

# Serving reads it as of now — the same definition, the same code.
features = store.get_online_features(
    features=["user_activity_features:orders_last_30d", ...],
    entity_rows=[{"user_id": user_id}],
)
```

**Drift monitoring that fires before the accuracy does:**

```python
# Labels arrive 90 days late. Waiting for accuracy to drop means finding out
# in three months. Input drift is visible today.
for feature in MONITORED_FEATURES:
    psi = population_stability_index(
        reference=training_distribution[feature],
        current=production_distribution(feature, window="7d"),
    )
    if psi > 0.25:                     # >0.25 is a substantial shift by convention
        alert(f"Feature '{feature}' has drifted (PSI={psi:.2f}). "
              f"The model is now being served inputs unlike its training data.")
```

## Notes

- A point-in-time correct join is the mechanism that prevents leakage in a feature store: it retrieves each feature's value *as of* the label's timestamp, not as of now. Doing this by hand with a simple join is how leakage gets in.
- Population Stability Index above 0.25 is the conventional threshold for "this feature's distribution has meaningfully changed". It is a heuristic, but it is a heuristic that fires before your accuracy metric can.
- The most common reason a model performs worse in production than offline, after leakage, is that the offline evaluation used a random split on temporal data.
