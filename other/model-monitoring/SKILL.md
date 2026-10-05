---
name: model-monitoring
description: "The layers trade timeliness against definitiveness."
---

# Model Monitoring (Verbose)

## Core Patterns

### The Monitoring Stack, By Detection Latency

The layers trade timeliness against definitiveness. Build them in this order,
because the fast layers are what actually page you.

| Layer | Example signals | Detects in | Confidence |
|---|---|---|---|
| Operational | latency, 5xx, saturation, model load failures | Seconds | Certain, but only about infrastructure |
| Input integrity | schema, null rate, out-of-range, unseen categories | Minutes | High — usually a genuine upstream bug |
| Prediction drift | score mean, score histogram, class-rate | Hours | Medium — behavior changed, cause unknown |
| Quality vs labels | AUC, precision@k, calibration | Days–weeks | Definitive, but too late to be the only alert |
| Business outcome | conversion, chargeback rate, revenue per session | Weeks | What actually matters |

Teams commonly build only the fourth layer, then discover it cannot fire until
labels arrive.

### Prediction Drift Beats Feature Drift for Alerting

The reason is arithmetic. Run a two-sample test per feature per day on 200
features at α = 0.05 and roughly ten fire daily by chance alone. Add the
genuine-but-harmless shifts — a campaign changing traffic mix, a seasonal cycle,
a new device model — and the channel is muted inside a fortnight.

Prediction drift is one distribution, and it is the model's own summary of every
input it consumed. If the inputs moved in a way the model weighs, the score
distribution moves; if not, it does not.

```python
def population_stability_index(baseline, current, bins=10) -> float:
    edges = np.quantile(baseline, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf          # absorb out-of-range values
    b = np.clip(np.histogram(baseline, edges)[0] / len(baseline), 1e-6, None)
    c = np.clip(np.histogram(current,  edges)[0] / len(current),  1e-6, None)
    return float(np.sum((c - b) * np.log(c / b)))
```

| PSI | Interpretation | Action |
|---|---|---|
| < 0.10 | No meaningful shift | None |
| 0.10 – 0.25 | Moderate shift | Investigate; check segments |
| > 0.25 | Major shift | Page; consider rollback or retrain |

PSI beats a KS test at scale for one reason: KS p-values shrink with sample size,
so at ten million predictions a day everything is "significant". PSI is an effect
size and has no such problem.

```yaml
- alert: PredictionDriftHigh
  expr: model_prediction_psi{model="churn"} > 0.25
  for: 30m
  labels: {severity: page}
  annotations: {runbook: "check input integrity first"}
```

Keep feature drift computed and dashboarded — as a **diagnostic you open after a
prediction-drift alert**, to find which inputs moved. Debugging tool, not pager.

### Delayed Ground Truth

This is the hard problem in model monitoring, and it has no clean solution — only
compensations. Label delay is intrinsic: churn is known after the renewal window,
fraud after the chargeback deadline, default after months of payments — while the
model decides continuously.

**Compensation 1 — lagged metrics.** Compute quality only over predictions whose
label window has closed:

```sql
SELECT date_trunc('day', p.ts) AS day, count(*) AS n, auc(l.label, p.score) AS auc
FROM predictions p JOIN labels l USING (request_id)
WHERE p.ts < now() - interval '60 days'    -- the maturity horizon
GROUP BY 1 ORDER BY 1;
```

Chart it as "AUC (60-day lag)". A dashboard implying today's quality is known is
worse than no dashboard.

**Compensation 2 — proxy labels that mature fast.**

| Model | True label | Delay | Proxy | Delay |
|---|---|---|---|---|
| Churn | Non-renewal | 30–90d | Login frequency drop, downgrade | 1–7d |
| Fraud | Chargeback | 30–120d | Manual review outcome, 3DS failure | Hours |
| Ranking | Purchase | Days | Click-through, dwell time | Minutes |
| Credit | Default | 6–24mo | First missed payment | 30d |

Proxies are biased — click-through is not purchase — so track their historical
correlation to the true label and treat them as leading indicators.

**Compensation 3 — selection bias in the labels you do get.**

If the model blocks a transaction, you never learn whether it was fraudulent. The
labeled set is filtered by the model's own decisions, so measured precision looks
excellent while recall is unknowable. The fix is a small randomized control
holdout — say `hash_bucket(request_id, 1000) < 5`, allowed through unscored. It
costs real money and is nearly always worth it: it is the only unbiased estimate
of your true error rate you will ever have.

### Drift Is Not Decay

Four situations, routinely conflated:

| Input drift | Quality drop | Name | Response |
|---|---|---|---|
| Yes | No | Benign covariate shift | Note it; do nothing |
| Yes | Yes | Covariate shift with impact | Retrain on recent data |
| No | Yes | Concept drift — the X→y relationship changed | Retrain; revisit features |
| Yes (sudden, structural) | Yes | Upstream data bug | **Fix the pipeline; do not retrain** |

The fourth row is why automatic retrain-on-drift is dangerous. A renamed upstream
column defaulting to null produces massive drift; retraining on that data teaches
the model the null is normal, putting the bug inside the weights where a pipeline
fix cannot reach it. Gate automatic retraining on data validation passing first
(see the MLOps pipeline skill).

### Prediction Logging as the Substrate

Everything above requires that you kept the predictions and their inputs.

```python
prediction_log.write({          # asynchronously, off the request path
    "request_id": req.id, "ts": now_utc().isoformat(),
    "model_version": MODEL_VERSION,
    "features": req.features,   # raw values, pre-transform
    "score": score,
    "decision": decision,       # what the system did with the score
    "latency_ms": elapsed_ms,
    "shadow_score": shadow,     # if a challenger is running
})
```

Sample at high volume by hashing the request id, not randomly, so a request
appears everywhere or nowhere and joins stay consistent. Retain 100% of
high-consequence events (declines, blocks, top-decile scores) regardless. Two
fields earn their keep repeatedly: `model_version`, which makes every metric
sliceable by rollout, and `decision`, which is what the business experienced.

### Segment-Level Monitoring

```sql
SELECT tenure_bucket, region, count(*) AS n,
       auc(label, score) AS auc,
       avg(score) - avg(label) AS calibration_gap
FROM predictions_with_labels
WHERE ts BETWEEN now() - interval '90 days' AND now() - interval '60 days'
GROUP BY 1, 2 HAVING count(*) > 1000 ORDER BY auc ASC;
```

Aggregate metrics are dominated by the largest segment, so a model can lose badly
on new users while overall AUC moves 0.002. Sort by the worst segment. Track
`calibration_gap` separately: a model can rank correctly while its absolute
probabilities drift, breaking any downstream fixed threshold or expected-value
calculation.

## Common Anti-Patterns

❌ **Per-feature drift tests across hundreds of features, all paging.**
✅ Alert on prediction drift; use feature drift as post-alert diagnosis.

❌ **KS-test p-values as the drift threshold at high volume.**
✅ Effect sizes such as PSI or Wasserstein distance, which do not degrade with n.

❌ **Automatically retraining whenever drift fires.**
✅ Validate the data first; distinguish an upstream bug from a real distribution change.

❌ **Reporting model quality as if labels were current.**
✅ Publish it with the maturity lag stated, paired with fast proxy metrics.

❌ **Measuring precision only on cases the model allowed through.**
✅ A small randomized control holdout gives an unbiased error estimate.

❌ **Logging the score without the features.**
✅ Log raw inputs so predictions can be joined, reproduced, and re-analysed — with hash-bucket sampling so joins stay consistent.

❌ **Aggregate metrics only.**
✅ Break out by tenure, region, device, and channel; alert on the worst segment.

❌ **Tracking discrimination (AUC) but never calibration.**
✅ Track both — thresholded decisions break on calibration drift while AUC holds.

## Model Monitoring Checklist

- [ ] Operational metrics (latency, errors, saturation) alerting on the serving path
- [ ] Input schema and range validation at request time, with a rejection metric,
      plus an alert on the unseen-category rate
- [ ] Prediction distribution monitored with an effect size (PSI or similar), with
      feature drift computed as a diagnostic rather than a pager
- [ ] Every prediction logged with raw features, model version, and decision
- [ ] Hash-bucket sampling; 100% retention of high-consequence events
- [ ] Label maturity horizon documented and quality metrics lagged by it
- [ ] Fast proxy labels defined and their correlation to true labels tracked
- [ ] Randomized control holdout where model decisions filter the labels
- [ ] Quality and calibration broken out by segment, alerting on the worst
- [ ] Retraining triggers gated on data validation passing
- [ ] Runbook distinguishing an upstream data bug from a genuine shift
