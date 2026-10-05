---
name: anomaly-detection-techniques
description: "\"Anomaly\" covers three distinct problems, and a detector built for one is close to"
---

# Anomaly Detection Techniques (Verbose)

## Core Patterns

### Naming the Anomaly Before Choosing a Method

"Anomaly" covers three distinct problems, and a detector built for one is close to
useless on the others.

| Type | Definition | Example | Approach |
|---|---|---|---|
| Point | A single observation is extreme | $40,000 charge on a $50/mo card | Robust z, Isolation Forest |
| Contextual | Normal in general, wrong here | 500 req/s at 4am Sunday | Deseasonalize, then score residual |
| Collective | Each point fine, the sequence is not | 200 logins, each valid, in 60s | Windowed aggregates, sequence models |

Most production incidents are contextual or collective. Teams reach for a point
detector, get poor recall, and conclude anomaly detection does not work — when the
actual failure was scoring raw values instead of residuals against an expectation.

### Robust Univariate Screening

```python
import numpy as np

def robust_z(x: np.ndarray) -> np.ndarray:
    med = np.median(x)
    mad = np.median(np.abs(x - med))
    if mad == 0:                              # >50% identical values
        mad = np.mean(np.abs(x - med)) or 1e-9
    return 0.6745 * (x - med) / mad

flags = np.abs(robust_z(x)) > 3.5
```

The classic 3-sigma rule fails through **masking**: the outliers you are hunting
sit inside the sample used to compute σ, so a few extreme points inflate σ enough
to bring themselves back inside the threshold. Ten large outliers in a thousand
points can double σ and hide each other. Median and MAD have a 50% breakdown
point — half the data can be arbitrary before the estimate moves.

The `0.6745` constant is `Φ⁻¹(0.75)`, which makes MAD a consistent estimator of σ
under normality, so the familiar 3-ish cutoff still means roughly what you expect.
The conventional threshold is 3.5.

Heavy-tailed data (latency, revenue, file sizes) needs a log transform first, or
even the robust threshold will flag the natural right tail every time.

### Multivariate Detection

```python
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

iso = make_pipeline(
    StandardScaler(),
    IsolationForest(n_estimators=300, max_samples=256,
                    contamination="auto", random_state=0),
)
iso.fit(X_clean)                                  # fit on a known-good window
scores = -iso[-1].score_samples(iso[:-1].transform(X_new))   # higher = anomalous

lof = LocalOutlierFactor(n_neighbors=20, novelty=True).fit(X_clean)
lof_scores = -lof.score_samples(X_new)
```

Isolation Forest builds random trees and scores by average path length —
anomalies sit in sparse regions and get isolated in few splits. `max_samples=256`
is the paper's default and is deliberately small; subsampling reduces *swamping*,
where dense normal clusters make genuinely isolated points look ordinary.

Local Outlier Factor compares a point's local density to its neighbors'. This is
the one that catches an anomaly sitting *between* two dense clusters — globally
unremarkable, locally in a void. It requires `novelty=True` at construction to be
usable on unseen data; the default object only exposes `fit_predict` on the
training set.

Scaling matters more than method choice for distance- and density-based
detectors: an unscaled feature measured in bytes dominates every distance
computation. Fit the scaler on clean data only — one fitted on contaminated data
has its variance inflated by the anomalies, which shrinks them toward the center.

### Time Series Anomalies

```python
from statsmodels.tsa.seasonal import STL

stl = STL(series, period=24 * 7, robust=True).fit()
resid = stl.resid
score = np.abs(robust_z(resid.values))
```

Score the residual, never the level. `robust=True` uses iteratively reweighted
fitting so a spike does not get absorbed into the seasonal or trend component —
without it, a large anomaly partly explains itself away and its residual shrinks.

For a forecast-based detector the prediction interval *is* the threshold: flag
observations outside it, and let the interval widen where the model is genuinely
uncertain instead of using one global cutoff. Multiple seasonalities (daily *and*
weekly) need MSTL or explicit Fourier terms; a single `period` leaves the other
cycle in the residual and produces a recurring wave of false positives.

See time-series-preprocessing for the causality rules — a detector whose expected
value was fitted using future points looks excellent offline and detects nothing
live.

### Evaluation

```python
from sklearn.metrics import average_precision_score, precision_recall_curve

ap = average_precision_score(y_true, scores)          # PR-AUC

order = np.argsort(-scores)
for k in (10, 50, 100, 500):
    print(k, y_true[order[:k]].mean())                # precision@k
```

| Metric | At 0.1% base rate | Verdict |
|---|---|---|
| Accuracy | 99.9% for "always normal" | Meaningless |
| ROC-AUC | 0.95 while 95% of alerts are false | Misleading |
| PR-AUC (AP) | Tracks true/false alert ratio | Use it |
| Precision@k | Directly the operator's experience | Use it |
| Recall@fixed-alert-budget | Coverage at sustainable load | Use it |

ROC-AUC is the trap. Its x-axis is false positive *rate*, normalized by the huge
negative class, so 10,000 false positives out of 10 million negatives moves it by
0.001 — while making the alert queue 10,000 items long. PR-AUC and precision@k use
raw false positive counts and reflect what the on-call engineer actually sees.

Set `k` from the triage budget: if the team can investigate 40 alerts a day, the
only question is how many of the top 40 are real. For streaming systems, detection
latency belongs beside precision — a detector that finds an outage with 100%
precision six hours later has not detected it.

### Thresholding and Operations

`contamination` in scikit-learn sets `offset_` so that the given fraction of
training data is labeled anomalous. It does not affect the score *ranking* — so
persist the raw scores and threshold them yourself against a labeled or
operator-reviewed sample. Setting `contamination` blindly to 0.01 on data whose
true rate is 0.0001 guarantees a 100:1 false positive ratio.

Feed dismissals back. A detector without a feedback loop degrades silently: data
drifts, the score distribution shifts, and the threshold calibrated in March is
mute or screaming by September. Recalibrate on a rolling quantile of recent
scores, and exclude confirmed anomalies from the refit window.

## Common Anti-Patterns

❌ **Reporting accuracy.** At a 0.1% base rate, a detector that does nothing scores
99.9%.
✅ Precision@k and PR-AUC, with `k` set by triage capacity.

❌ **Reporting ROC-AUC as the headline.** Stays near 0.95 while nearly every alert
is false.
✅ Average precision, plus the raw confusion counts at the operating threshold.

❌ **Mean ± 3σ on skewed or contaminated data.** The outliers inflate σ and mask
themselves.
✅ Median/MAD, and log-transform heavy-tailed quantities first.

❌ **Scoring raw values on a seasonal series.** Every quiet night is an anomaly.
✅ Decompose or forecast, then score the residual.

❌ **Refitting nightly on data containing yesterday's undetected anomalies.** The
model learns them as normal and stops flagging them.
✅ Fit on a curated clean window; exclude confirmed incidents from refits.

❌ **Fitting the scaler on contaminated data.** Anomalies inflate the variance and
get pulled toward the center.
✅ Fit scaler and detector together on the clean reference period.

❌ **Trusting `contamination` to set the threshold.** It is a guess about the base
rate, not a calibration.
✅ Keep raw scores; calibrate the cutoff against reviewed samples and alert budget.

❌ **A fixed threshold that never moves.** Drift makes it mute or deafening.
✅ Rolling recalibration with alert-rate monitoring.

❌ **No feedback capture.** You never learn precision, so you cannot improve it.
✅ Record every alert's disposition; it becomes the labeled set you lacked.

## Anomaly Detection Checklist

- [ ] Anomaly type identified: point, contextual, or collective
- [ ] Seasonality and trend removed before scoring time series
- [ ] Robust statistics (median/MAD) used instead of mean/σ
- [ ] Heavy-tailed features log-transformed before thresholding
- [ ] Features scaled, with the scaler fitted on clean data only
- [ ] Multivariate method used when anomalies are combinations, not extremes
- [ ] Precision@k and PR-AUC reported; accuracy and ROC-AUC not headlined
- [ ] `k` set from actual triage capacity
- [ ] Detection latency measured for streaming detectors
- [ ] Threshold calibrated against reviewed samples, not `contamination`
- [ ] Confirmed anomalies excluded from the refit window
- [ ] Alert disposition captured as feedback and as future labels
- [ ] Score distribution monitored for drift
