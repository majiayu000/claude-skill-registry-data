---
name: ml-deployment
description: "A model in production is never just weights."
---

# ML Deployment (Verbose)

## Core Patterns

### The Deployable Unit

A model in production is never just weights. It is a bundle whose parts must move
together, because any one of them changing alters the predictions.

```
model-registry/churn/v1.4.2/
  model.onnx                # portable graph — no Python pickle at serve time
  preprocessor.joblib       # the FITTED transformer from the training run
  feature_spec.json         # names, order, dtypes, null policy, allowed ranges
  requirements.lock
  metadata.json
```

```json
{
  "model_version": "1.4.2",
  "git_sha": "8e1c3af",
  "training_data": {"uri": "s3://lake/churn/2026-06-01/", "sha256": "9f2b..."},
  "framework": "scikit-learn==1.3.2",
  "metrics": {"auc": 0.871, "pr_auc": 0.402},
  "trained_at": "2026-06-02T04:11:09Z"
}
```

The `training_data` hash is the field teams skip and later regret. Without it you
can reproduce the code but not the run, and "why does v1.4.2 score differently
from v1.4.1" becomes unanswerable. The MLOps pipeline skill covers how that hash
gets produced.

Exporting to ONNX or TorchScript removes the Python version, the framework
version, and the pickle format from your serving risk surface, at the cost of an
export-time numerical equivalence check.

### Eliminating Training/Serving Skew

Skew is the defining failure mode of ML deployment. The model is fine; the inputs
it sees in production are not the inputs it was trained on. Three mechanisms
produce it, in rough order of frequency.

**Reimplemented feature logic.** Training runs in Spark or pandas; serving runs
inside the request path in a different language or library. Rounding, timezone
handling, null semantics, and category ordering all diverge silently.

```python
# features/transforms.py — the single definition, imported by BOTH paths
def account_age_days(signup_at: datetime, at: datetime) -> int:
    return (at.astimezone(timezone.utc) - signup_at.astimezone(timezone.utc)).days

def encode_plan(plan: str | None) -> int:
    return PLAN_ORDINALS.get(plan, PLAN_ORDINALS["__unknown__"])
```

**Re-fit rather than loaded transformers.** A `StandardScaler` fit on a serving
batch centres on that batch's mean, not the training mean.

**Point-in-time leakage.** Training joins a feature table as it looks *today*;
serving sees it as it looked at request time. Training on a
`lifetime_order_count` computed after the label event teaches the model to read
the future, and the offline metrics look wonderful.

Detect skew rather than trusting discipline: in shadow, recompute the
training-side features for live entities, compare against what serving used, and
emit a `skew.mismatch` counter on any value outside tolerance.

### Rollout Strategies for Models

Model rollouts differ from service rollouts in one decisive way: a broken model
is *healthy*. It returns 200s at normal latency and predicts badly. Any deploy
strategy that observes only infrastructure signals will pass it through.

| Strategy | Live traffic | Detects | Time to signal | When to use |
|---|---|---|---|---|
| Shadow / mirror | 0% (responses discarded) | Skew, latency, exceptions, distribution shift | Hours | Always, before anything else |
| Canary | 1–10%, ramped | Business-metric regression, segment-specific harm | Days–weeks (label delay) | Any model touching revenue or users |
| A/B (held split) | Fixed split, fixed horizon | Causal effect on the target metric | Weeks | When you need a defensible number |
| Blue-green | 0→100% | Infra faults only | Minutes | Low-stakes or offline batch models |
| Bandit | Adaptive | Best-of-N under exploration | Continuous | Many candidates, fast feedback |

Shadow mode catches the embarrassing failures: schema mismatches, a missing
feature defaulting to zero, 10× latency, a preprocessor mapping every unseen
category to the same bucket.

```python
async def predict(req: Request) -> Response:
    live = await champion.predict(req.features)
    asyncio.create_task(shadow_compare(req, live))   # never block the response
    return live

async def shadow_compare(req, live):
    try:
        cand = await challenger.predict(req.features)
        log.info("shadow", champion=live.score, challenger=cand.score,
                 delta=abs(cand.score - live.score), model=challenger.version)
    except Exception:
        metrics.increment("shadow.error")            # a shadow failure is not an outage
```

The canary gate should sit on prediction distribution and on early business
proxies — not on error rate, which will be flat.

```yaml
# Argo Rollouts analysis: fail the canary on distribution shift, not just 5xx
metrics:
  - name: prediction-mean-shift
    interval: 10m
    successCondition: result < 0.05
    provider:
      prometheus:
        query: |
          abs(
            avg(model_prediction_score{version="{{args.canary}}"})
            - avg(model_prediction_score{version="{{args.stable}}"})
          )
```

### Serving Topology

```python
MODEL = load_model(os.environ["MODEL_URI"])          # load once at startup
PREP  = joblib.load(os.environ["PREPROCESSOR_URI"])  # never per request

@app.post("/predict")
def predict(req: PredictRequest) -> PredictResponse:
    validate(req.features, FEATURE_SPEC)             # fail loudly on schema drift
    x = PREP.transform(to_frame(req.features))
    return PredictResponse(score=float(MODEL.predict_proba(x)[0, 1]),
                           model_version=MODEL_VERSION)
```

Two sizing facts that surprise people arriving from web services:

- **CPU inference on small models is memory-bandwidth bound, not core bound.**
  Doubling replicas usually beats doubling cores per replica.
- **Batching helps GPU throughput and hurts p99.** A 20 ms batch window at 50 rps
  spends most of its time waiting. Dynamic batching starts paying off in the
  hundreds of rps, and the window must fit inside the latency budget.

Pin thread counts (`OMP_NUM_THREADS`) explicitly. BLAS defaults to the host core
count, which inside a container with a 1-CPU limit means constant throttling.

### Versioning and Rollback

Serve through an alias so promotion and rollback are pointer moves — `production`
points at v1.4.2, `canary` at v1.5.0, and neither is baked into an image.

```bash
# Rollback is a config change, not a build
mlflow models set-alias --name churn --alias production --version 1.4.1
```

Keep the previous version warm. A rollback that requires re-downloading a 4 GB
artifact and re-warming a cache is an outage with a plan attached.

## Common Anti-Patterns

❌ **Feature logic written twice — once in the training job, once in the API.**
✅ One shared library, or a feature store serving both paths, plus a skew check running in shadow.

❌ **Deploying straight to 100% because staging looked fine.**
✅ Shadow, then canary with a distribution gate. Staging traffic is not production traffic.

❌ **Unpinned framework versions in the serving image.**
✅ Pin exactly, and export to ONNX/TorchScript where practical.

❌ **Using `/healthz` returning 200 as the deploy gate.**
✅ Assert golden predictions on fixed rows — a wrong model loads perfectly.

❌ **No record of which data trained the artifact.**
✅ Store the dataset URI and content hash in the model metadata.

❌ **Re-fitting the preprocessor at serving time.**
✅ Serialize the fitted transformer and load it alongside the model.

❌ **Treating rollback as "redeploy the old commit".**
✅ Alias-based promotion, with the prior version kept warm.

❌ **Letting unbounded input values reach the model.**
✅ Validate against `feature_spec.json` and reject or clamp out-of-range inputs — models extrapolate confidently and wrongly.

## ML Deployment Checklist

- [ ] Model, fitted preprocessor, and feature spec versioned as one artifact
- [ ] Training data URI and content hash recorded in metadata
- [ ] Framework versions pinned; export format chosen deliberately
- [ ] Feature transformations defined once and imported by both paths
- [ ] Automated skew check comparing online and offline feature values
- [ ] Golden-prediction test runs in the deploy pipeline
- [ ] Input validated against the feature spec at request time
- [ ] Shadow deployment run before any live traffic
- [ ] Canary gated on prediction distribution, not only error rate
- [ ] Alias-based promotion with rollback in under a minute
- [ ] Previous model version kept warm and loadable
- [ ] Model version returned in every prediction response and logged
- [ ] Thread counts pinned to the container CPU limit
- [ ] Latency verified at expected peak concurrency, not single-request
