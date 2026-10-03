---
name: sre-canary
description: Post-deploy monitoring and canary verification skill. Use when the user has just deployed and wants to verify production health, watch for console errors or performance regressions, run a post-deploy monitoring loop, or validate that a canary deployment is stable before rolling out to 100% traffic.
---

# SRE Canary — Post-Deploy Monitoring & Canary Verification

Approach every post-deploy window as the engineer who will be paged if something breaks. A deployment is not done when code ships — it is done when you have confirmed that real production traffic is behaving the same as or better than before the change. Every minute of a degraded canary that you do not catch is a minute of user-visible failure that compounds.

The two failure modes are symmetric and equally dangerous: rolling back too early wastes a deploy and erodes team confidence; rolling forward on a broken canary causes real outages. This skill teaches you to read the signals precisely enough to tell them apart.

---

## Step 0: Before You Start Monitoring

Before watching any signals, establish your baseline. Monitoring without a baseline is just staring at numbers.

1. **Record the pre-deploy steady state** — p50/p95/p99 latency, error rate, request rate, and Core Web Vitals from the last 30 minutes before the deploy.
2. **Note the deploy timestamp exactly** — you will overlay this on every graph. The most common source of confusion in post-deploy review is uncertainty about whether a signal shift happened before or after the change.
3. **Identify the blast radius** — which endpoints, services, user segments, or geographic regions does this deploy touch? Monitor those first; do not drown in unrelated signal.
4. **Know your rollback command before you deploy** — not after. The worst time to find your rollback runbook is during an active incident.
5. **Define success criteria in advance** — "error rate stays below 0.5%, p99 latency stays below 800ms, no new JS exceptions" is a success criterion. "Seems fine" is not.

---

## Post-Deploy Monitoring Loop

Run this loop continuously during the canary window. Do not walk away after pressing deploy.

### Phase 1: Immediate (0–5 minutes post-deploy)

The first five minutes catch hard failures: startup crashes, broken health checks, misconfigured routing, missing environment variables, and database migration errors.

**What to check:**

```bash
# 1. Confirm new pods/instances are running and healthy
kubectl get pods -n production -l app=<service> --watch

# 2. Check recent deployment events for errors
kubectl describe deployment <service> -n production | tail -30

# 3. Tail application logs for the new pods only
kubectl logs -n production -l app=<service>,version=<new-version> --since=5m -f

# 4. Watch the error rate in real time (adapt to your stack)
watch -n 5 'curl -s "http://prometheus:9090/api/v1/query?query=rate(http_requests_total{status=~\"5..\",service=\"<service>\"}[1m])" | jq .data.result[0].value[1]'

# 5. Confirm health check is passing on new instances
kubectl exec -n production deploy/<service> -- curl -sf http://localhost:8080/health
```

**Rollback immediately if:**
- Any new pod enters `CrashLoopBackOff` or `Error` state
- Health check returns non-200 on new instances
- Error rate jumps above 5× baseline within 2 minutes
- Application logs show unhandled exceptions on startup path

### Phase 2: Stabilization (5–15 minutes post-deploy)

The process is running but we are watching for regressions that only appear under real traffic: slow queries exposed by a schema change, memory growth from a leak, latency spikes from a missing cache warm-up.

**What to check:**

```bash
# HTTP error rate by status code — differentiate 4xx (client) from 5xx (server)
rate(http_requests_total{service="<service>",status=~"5.."}[2m])
rate(http_requests_total{service="<service>",status=~"4.."}[2m])

# Latency percentiles — watch p99 specifically; it moves first
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{service="<service>"}[2m]))
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{service="<service>"}[2m]))
histogram_quantile(0.50, rate(http_request_duration_seconds_bucket{service="<service>"}[2m]))

# Memory usage — a leak will show as monotonic growth here
container_memory_working_set_bytes{container="<service>", namespace="production"}

# CPU — sudden sustained spike on new version is a regression signal
rate(container_cpu_usage_seconds_total{container="<service>", namespace="production"}[2m])

# DB slow queries — a schema change or missing index will surface here
rate(db_query_duration_seconds_bucket{le="1",service="<service>"}[2m])
```

**Alert thresholds — stabilization phase:**

| Signal | Warning | Critical |
|---|---|---|
| 5xx error rate | > 2× baseline | > 5× baseline or > 1% absolute |
| p99 latency | > 1.5× baseline | > 2× baseline or > 2s absolute |
| p95 latency | > 1.3× baseline | > 1.75× baseline |
| Memory growth | > 20% above baseline | > 50% above baseline or OOM risk |
| CPU | > 30% above baseline | > 60% above baseline, sustained |
| New JS exceptions | Any new error type | Error rate > 1/min |

### Phase 3: Confidence Window (15–60 minutes post-deploy)

Traffic has flowed through the new version. You are now watching for issues that only emerge over time: connection pool saturation, cache eviction patterns, slow memory leaks, and long-tail edge cases.

**Extended checks:**

```bash
# Connection pool saturation
db_connection_pool_used{service="<service>"} / db_connection_pool_max{service="<service>"}

# Cache hit rate — a regression here causes latency spikes at the DB
cache_hits_total{service="<service>"} / (cache_hits_total + cache_misses_total)

# Queue depth — if the service processes async work, watch for backup
rabbitmq_queue_messages{queue="<service>-queue"}
# or
aws_sqs_approximate_number_of_messages_visible{QueueName="<service>-queue"}

# Downstream service health — your change may affect dependencies
rate(http_requests_total{client="<service>",status=~"5.."}[5m])

# Apdex score — composite satisfaction metric
(
  rate(http_request_duration_seconds_bucket{le="0.3",service="<service>"}[5m]) +
  rate(http_request_duration_seconds_bucket{le="1.2",service="<service>"}[5m]) / 2
) / rate(http_request_duration_seconds_count{service="<service>"}[5m])
```

---

## Canary Deployment Verification

A canary routes a small percentage of production traffic to the new version while the old version handles the rest. You compare the two cohorts directly — same traffic, same load, same conditions — to detect regressions with statistical confidence before full rollout.

### Traffic Split Configuration

**Kubernetes with Argo Rollouts:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-service
  namespace: production
spec:
  replicas: 10
  strategy:
    canary:
      canaryService: my-service-canary
      stableService: my-service-stable
      trafficRouting:
        nginx:
          stableIngress: my-service-ingress
      steps:
        - setWeight: 5       # Step 1: 5% canary traffic
        - pause: {duration: 10m}
        - analysis:
            templates:
              - templateName: success-rate
        - setWeight: 20      # Step 2: 20% canary traffic
        - pause: {duration: 15m}
        - analysis:
            templates:
              - templateName: success-rate
              - templateName: latency-p99
        - setWeight: 50      # Step 3: 50% canary traffic
        - pause: {duration: 20m}
        - analysis:
            templates:
              - templateName: success-rate
              - templateName: latency-p99
              - templateName: error-budget
        # Step 4: 100% — promoted if all analyses pass
  selector:
    matchLabels:
      app: my-service
  template:
    metadata:
      labels:
        app: my-service
```

**AnalysisTemplate — success rate:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
  namespace: production
spec:
  metrics:
    - name: success-rate
      interval: 1m
      successCondition: result[0] >= 0.995
      failureLimit: 2
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            sum(rate(http_requests_total{service="my-service-canary",status!~"5.."}[2m]))
            /
            sum(rate(http_requests_total{service="my-service-canary"}[2m]))
```

**AnalysisTemplate — p99 latency:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: latency-p99
  namespace: production
spec:
  metrics:
    - name: latency-p99
      interval: 1m
      successCondition: result[0] <= 0.8   # 800ms
      failureLimit: 2
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            histogram_quantile(0.99,
              sum(rate(http_request_duration_seconds_bucket{service="my-service-canary"}[2m]))
              by (le)
            )
```

### Canary Rollout Gates — 5% → 20% → 50% → 100%

Each gate is a set of conditions that must be true before advancing. Treat them as mandatory, not advisory.

#### Gate 1: 5% → 20% (after 10 minutes at 5%)

Pass conditions:
- [ ] 5xx error rate on canary ≤ baseline × 1.2 (20% tolerance)
- [ ] p99 latency on canary ≤ baseline × 1.2
- [ ] No new unhandled exception types in canary logs
- [ ] All canary instances passing health checks
- [ ] Memory usage on canary ≤ baseline × 1.3

Fail conditions (auto-rollback):
- [ ] 5xx rate on canary > 5× baseline for 2+ consecutive minutes
- [ ] p99 latency > 2× baseline for 3+ consecutive minutes
- [ ] Any canary pod in `CrashLoopBackOff`
- [ ] Health check failure rate > 0

#### Gate 2: 20% → 50% (after 15 minutes at 20%)

Pass conditions (all Gate 1 conditions, plus):
- [ ] Apdex score on canary ≥ Apdex score on stable × 0.98
- [ ] DB query p95 on canary ≤ baseline × 1.15
- [ ] Cache hit rate on canary ≥ baseline × 0.95
- [ ] No alerts firing on canary-specific dashboards
- [ ] Queue depth (if applicable) not growing on canary traffic

Fail conditions (auto-rollback):
- [ ] Apdex degradation > 5% from stable
- [ ] Any memory leak signal (sustained growth > 20% over 10 minutes)
- [ ] Error budget burn rate > 3× normal

#### Gate 3: 50% → 100% (after 20 minutes at 50%)

Pass conditions (all previous, plus):
- [ ] Error budget consumed during canary window < 10% of hourly budget
- [ ] No customer-escalated incidents attributable to canary
- [ ] SLO compliance rate ≥ SLO target
- [ ] All Core Web Vitals within acceptable range (if frontend change)
- [ ] No anomalous patterns in structured logs (no new error codes, unusual request patterns)
- [ ] Downstream service health unaffected by canary traffic

Promotion command:

```bash
# Argo Rollouts
kubectl argo rollouts promote my-service -n production

# Verify promotion
kubectl argo rollouts status my-service -n production
```

Rollback command:

```bash
# Argo Rollouts — abort and return all traffic to stable
kubectl argo rollouts abort my-service -n production
kubectl argo rollouts undo my-service -n production

# Verify rollback
kubectl argo rollouts get rollout my-service -n production --watch
```

---

## Health Check Patterns

Health checks are the foundation of every automated canary gate. A misconfigured health check gives you false confidence during the canary window.

### Liveness vs. Readiness vs. Startup

- **Liveness:** Is the process alive and not deadlocked? If this fails, the container is restarted. Liveness checks should be simple — if they are expensive, a degraded service will fail the check, restart, and oscillate.
- **Readiness:** Is the instance ready to receive traffic? If this fails, the instance is removed from the load balancer without being restarted. Use readiness to signal warm-up, dependency unavailability, or overload.
- **Startup:** Has the application finished initializing? Prevents premature liveness checks from killing slow-starting containers.

```yaml
# Kubernetes probe configuration — production-grade
livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3    # 30 seconds of failure before restart

readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 2    # 10 seconds before removed from LB

startupProbe:
  httpGet:
    path: /health/live
    port: 8080
  failureThreshold: 30
  periodSeconds: 5       # Allow up to 150 seconds for startup
```

### Health Endpoint Implementation

```python
# Python / FastAPI example — production health endpoint
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import time

app = FastAPI()
START_TIME = time.time()

@app.get("/health/live")
async def liveness():
    """
    Liveness: is the process functional?
    Only check internal process state — not external dependencies.
    A liveness failure causes a restart; do not be trigger-happy.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "live", "uptime_seconds": int(time.time() - START_TIME)}
    )

@app.get("/health/ready")
async def readiness():
    """
    Readiness: can this instance serve traffic?
    Check critical dependencies. A failure removes from LB without restart.
    """
    checks = {}
    overall_ok = True

    # Database connectivity
    try:
        await db.execute("SELECT 1")
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"
        overall_ok = False

    # Cache connectivity
    try:
        await redis.ping()
        checks["cache"] = "ok"
    except Exception as e:
        checks["cache"] = f"error: {str(e)}"
        # Degrade gracefully — cache failure may not require removing from LB
        # Adjust based on your caching criticality

    http_status = status.HTTP_200_OK if overall_ok else status.HTTP_503_SERVICE_UNAVAILABLE
    return JSONResponse(status_code=http_status, content={"status": "ready" if overall_ok else "not_ready", "checks": checks})
```

### Synthetic Health Checks (Active Probing)

In addition to Kubernetes probes, run active synthetic checks that simulate real user flows:

```bash
# Canary synthetic check script — run every 60 seconds during canary window
#!/bin/bash
set -e

CANARY_HOST="${CANARY_HOST:-https://canary.example.com}"
STABLE_HOST="${STABLE_HOST:-https://www.example.com}"
MAX_LATENCY_MS="${MAX_LATENCY_MS:-800}"
ERROR_THRESHOLD="${ERROR_THRESHOLD:-0.01}"

check_endpoint() {
  local host="$1"
  local path="$2"
  local label="$3"

  START=$(date +%s%3N)
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "${host}${path}")
  END=$(date +%s%3N)
  DURATION=$((END - START))

  echo "[${label}] ${path} → HTTP ${HTTP_CODE} in ${DURATION}ms"

  if [[ "$HTTP_CODE" -ge 500 ]]; then
    echo "FAIL: 5xx on ${label} ${path}"
    return 1
  fi

  if [[ "$DURATION" -gt "$MAX_LATENCY_MS" ]]; then
    echo "WARN: Latency ${DURATION}ms exceeds ${MAX_LATENCY_MS}ms threshold on ${label} ${path}"
  fi
}

# Run the same checks against canary and stable
for path in "/" "/api/products" "/api/users/me" "/api/search?q=test"; do
  check_endpoint "$CANARY_HOST" "$path" "CANARY"
  check_endpoint "$STABLE_HOST" "$path" "STABLE"
  echo "---"
done
```

---

## Alert Thresholds and Rollback Triggers

### Error Rate Thresholds

Define error budgets before the deploy, not during the incident.

| SLO Target | Error Budget / 30 days | Max hourly burn | Auto-rollback threshold |
|---|---|---|---|
| 99.9% | 43.8 minutes | ~1.5 minutes | 5xx rate > 0.5% for 3 min |
| 99.5% | 3.65 hours | ~7.5 minutes | 5xx rate > 1.0% for 3 min |
| 99.0% | 7.3 hours | ~15 minutes | 5xx rate > 2.0% for 5 min |

**Canary-specific alert: error rate comparison**

The most actionable canary alert is not the absolute error rate — it is the ratio of canary error rate to stable error rate. A 0.5% error rate is fine if the stable version also has 0.5%. A 0.5% error rate is a regression if the stable version has 0.05%.

```promql
# Alert when canary error rate is more than 3× stable error rate
(
  rate(http_requests_total{service="my-service-canary",status=~"5.."}[5m])
  /
  rate(http_requests_total{service="my-service-canary"}[5m])
)
/
(
  rate(http_requests_total{service="my-service-stable",status=~"5.."}[5m])
  /
  rate(http_requests_total{service="my-service-stable"}[5m])
) > 3
```

### Latency Thresholds

```promql
# Alert when canary p99 latency is 50% worse than stable p99
(
  histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{service="my-service-canary"}[5m]))
)
/
(
  histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{service="my-service-stable"}[5m]))
) > 1.5
```

### Automatic Rollback Triggers

Define these before deploying. Automation is faster than humans when something breaks at 3am.

**Hard rollback triggers (automated, immediate):**
- 5xx error rate on canary > 5% absolute for 2 consecutive minutes
- p99 latency on canary > 3× baseline for 3 consecutive minutes
- Any canary pod in `CrashLoopBackOff`
- Health check failure rate on canary > 0 for 1 minute
- Error budget burn rate > 10× normal (consuming an hour's budget in 6 minutes)

**Soft rollback triggers (alert + human decision within 5 minutes):**
- 5xx error rate on canary > 2× stable for 5 minutes
- p99 latency on canary > 1.5× stable for 5 minutes
- New JavaScript exception type appearing at rate > 1/minute
- Cache hit rate drops > 10% on canary
- Apdex degradation > 3% vs. stable

```bash
# Manual rollback — always test this before you need it
kubectl argo rollouts abort my-service -n production && \
kubectl argo rollouts undo my-service -n production

# Verify traffic is back on stable
kubectl argo rollouts get rollout my-service -n production
kubectl get pods -n production -l app=my-service

# Confirm error rate is recovering
watch -n 10 'kubectl top pods -n production -l app=my-service'
```

---

## SLO/SLA Monitoring During Canary

### Error Budget Burn Rate

Burn rate is the rate at which you are consuming your monthly error budget. A burn rate of 1 means you are burning exactly at budget — you will use up the month's budget by end of month. A burn rate of 10 means you will exhaust the budget in 1/10 of the month (about 3 days).

During a canary, burn rate spikes are your highest-signal alert.

```promql
# 5-minute burn rate — short window, fast response
(
  1 - (
    rate(http_requests_total{service="my-service",status!~"5.."}[5m])
    /
    rate(http_requests_total{service="my-service"}[5m])
  )
) / (1 - 0.999)  # Replace 0.999 with your SLO target

# 1-hour burn rate — medium window, catches gradual degradation
(
  1 - (
    rate(http_requests_total{service="my-service",status!~"5.."}[1h])
    /
    rate(http_requests_total{service="my-service"}[1h])
  )
) / (1 - 0.999)
```

**Burn rate alert thresholds (Google SRE Workbook recommendations):**

| Window | Burn Rate | Action |
|---|---|---|
| 5 minutes | > 14.4× | Page immediately — critical |
| 1 hour | > 14.4× | Page immediately — critical |
| 6 hours | > 6× | Ticket + investigate |
| 3 days | > 3× | Review and plan |

### SLO Dashboard During Canary Window

A canary-window SLO dashboard should show, side-by-side:

1. **Error rate: canary vs. stable** — the comparison is more informative than the absolute value
2. **Latency percentiles: canary vs. stable** — p50, p95, p99, all on the same chart
3. **Error budget remaining** — how much of the monthly budget is left
4. **Current burn rate** — 5-minute and 1-hour windows
5. **Apdex score: canary vs. stable**
6. **Request rate: canary vs. stable** — to verify traffic is actually being split as configured

If your observability platform is Grafana, add a deploy marker annotation:

```bash
# Post a Grafana deploy annotation — creates a vertical line on all dashboards
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${GRAFANA_API_KEY}" \
  "${GRAFANA_URL}/api/annotations" \
  -d "{
    \"dashboardId\": ${DASHBOARD_ID},
    \"time\": $(date +%s000),
    \"text\": \"Deploy: ${SERVICE} ${VERSION} — Canary ${CANARY_WEIGHT}%\",
    \"tags\": [\"deploy\", \"canary\", \"${SERVICE}\"]
  }"
```

---

## Core Web Vitals Monitoring

For frontend deployments, Core Web Vitals are the highest-signal user-experience metrics. A canary that degrades CWV is hurting real users even if the API error rate is zero.

### Thresholds

| Metric | Good | Needs Improvement | Poor (Rollback) |
|---|---|---|---|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5s – 4.0s | > 4.0s |
| INP (Interaction to Next Paint) | < 200ms | 200ms – 500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1 – 0.25 | > 0.25 |
| FCP (First Contentful Paint) | < 1.8s | 1.8s – 3.0s | > 3.0s |
| TTFB (Time to First Byte) | < 800ms | 800ms – 1800ms | > 1800ms |

### Real User Monitoring (RUM) During Canary

Collect Core Web Vitals from real users in the canary cohort using the `web-vitals` library:

```javascript
// Install: npm install web-vitals
import { onCLS, onINP, onLCP, onFCP, onTTFB } from 'web-vitals';

function sendToAnalytics({ name, value, id, delta, rating }) {
  // Tag with canary version so you can segment in your analytics
  const payload = {
    metric: name,
    value: Math.round(name === 'CLS' ? value * 1000 : value),
    delta: Math.round(name === 'CLS' ? delta * 1000 : delta),
    id,
    rating,                             // 'good' | 'needs-improvement' | 'poor'
    app_version: window.__APP_VERSION__, // injected at build time
    canary: window.__IS_CANARY__,       // true for canary instances
    page: window.location.pathname,
  };

  // Send to your analytics endpoint
  if (navigator.sendBeacon) {
    navigator.sendBeacon('/api/vitals', JSON.stringify(payload));
  } else {
    fetch('/api/vitals', { method: 'POST', body: JSON.stringify(payload), keepalive: true });
  }
}

onCLS(sendToAnalytics);
onINP(sendToAnalytics);
onLCP(sendToAnalytics);
onFCP(sendToAnalytics);
onTTFB(sendToAnalytics);
```

**Segment your CWV data by canary flag** in your analytics platform. The rollback signal is not just "LCP got worse" — it is "LCP is worse for the canary cohort and stable for the stable cohort."

### Lighthouse CI in the Canary Pipeline

```yaml
# .github/workflows/canary-cwv-check.yml
name: Core Web Vitals — Canary Check

on:
  workflow_dispatch:
    inputs:
      canary_url:
        description: 'Canary URL to check'
        required: true
      stable_url:
        description: 'Stable URL to compare against'
        required: true

jobs:
  cwv-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Lighthouse against canary
        uses: treosh/lighthouse-ci-action@v11
        with:
          urls: ${{ github.event.inputs.canary_url }}
          configPath: '.lighthouserc.json'
          uploadArtifacts: true
          temporaryPublicStorage: true

      - name: Compare results
        run: |
          # Extract LCP, CLS, INP from LHCI output and compare to baseline
          node scripts/compare-cwv.js --canary=lhci-results.json --threshold=10
```

---

## Log Analysis During Canary Window

### What to Watch in Logs

Structure your logs as JSON from day one. Canary log analysis on unstructured text is slow and error-prone.

**Critical log signals during canary:**

```bash
# 1. New error types not seen in stable — the most important signal
# Compare error.code or error.type distribution between canary and stable
kubectl logs -n production -l version=canary --since=15m \
  | jq -r 'select(.level=="error") | .error.code // .error.type // "unknown"' \
  | sort | uniq -c | sort -rn

# 2. Exception stack traces — new ones indicate new code paths failing
kubectl logs -n production -l version=canary --since=15m \
  | jq -r 'select(.level=="error") | .error.stack // empty' \
  | head -50

# 3. Slow operations — queries, external calls, serialization
kubectl logs -n production -l version=canary --since=15m \
  | jq 'select(.duration_ms > 500) | {path: .path, duration_ms, trace_id}'

# 4. Warning-level signals that precede errors
kubectl logs -n production -l version=canary --since=15m \
  | jq -r 'select(.level=="warn") | .message' \
  | sort | uniq -c | sort -rn

# 5. Correlation IDs for end-to-end trace reconstruction
# If you see an error in logs, pull the full trace:
kubectl logs -n production -l app=my-service --since=1h \
  | jq --arg tid "your-trace-id" 'select(.trace_id==$tid)'
```

### Log Anomaly Detection

During the canary window, compare log volume and error distribution between canary and stable:

```bash
#!/bin/bash
# canary-log-compare.sh — run during canary window
NAMESPACE="${1:-production}"
SERVICE="${2:-my-service}"
WINDOW="${3:-15m}"

echo "=== Error distribution: CANARY ==="
kubectl logs -n "$NAMESPACE" -l "app=${SERVICE},version=canary" --since="$WINDOW" \
  | jq -r 'select(.level=="error") | .error_code // .message // "unclassified"' \
  | sort | uniq -c | sort -rn | head -20

echo ""
echo "=== Error distribution: STABLE ==="
kubectl logs -n "$NAMESPACE" -l "app=${SERVICE},version=stable" --since="$WINDOW" \
  | jq -r 'select(.level=="error") | .error_code // .message // "unclassified"' \
  | sort | uniq -c | sort -rn | head -20

echo ""
echo "=== Slow requests (>500ms): CANARY ==="
kubectl logs -n "$NAMESPACE" -l "app=${SERVICE},version=canary" --since="$WINDOW" \
  | jq -c 'select(.duration_ms != null and .duration_ms > 500) | {path, duration_ms, method, status}' \
  | head -20

echo ""
echo "=== NEW error types in CANARY not seen in STABLE ==="
CANARY_ERRORS=$(kubectl logs -n "$NAMESPACE" -l "app=${SERVICE},version=canary" --since="$WINDOW" \
  | jq -r 'select(.level=="error") | .error_code // empty' | sort -u)
STABLE_ERRORS=$(kubectl logs -n "$NAMESPACE" -l "app=${SERVICE},version=stable" --since="$WINDOW" \
  | jq -r 'select(.level=="error") | .error_code // empty' | sort -u)
comm -23 <(echo "$CANARY_ERRORS") <(echo "$STABLE_ERRORS")
```

### Structured Logging Best Practices During Canary

Tag every log line with the version/canary identifier:

```python
import logging
import json
import os
import time

class StructuredLogger:
    def __init__(self, service_name: str):
        self.service = service_name
        self.version = os.getenv("APP_VERSION", "unknown")
        self.is_canary = os.getenv("IS_CANARY", "false").lower() == "true"

    def _log(self, level: str, message: str, **kwargs):
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "level": level,
            "message": message,
            "service": self.service,
            "version": self.version,
            "canary": self.is_canary,
            **kwargs
        }
        print(json.dumps(entry), flush=True)

    def info(self, message: str, **kwargs):
        self._log("info", message, **kwargs)

    def error(self, message: str, error: Exception = None, **kwargs):
        error_info = {}
        if error:
            error_info = {
                "error": {
                    "type": type(error).__name__,
                    "message": str(error),
                    "code": getattr(error, "code", None),
                }
            }
        self._log("error", message, **{**error_info, **kwargs})
```

---

## Console Error Monitoring

For frontend deployments, JavaScript console errors are a leading indicator of user-facing failures. Monitor them during the canary window.

### Browser Error Capture

```javascript
// error-capture.js — load early in your bundle, before other scripts
(function () {
  const APP_VERSION = window.__APP_VERSION__ || 'unknown';
  const IS_CANARY = window.__IS_CANARY__ || false;

  // Capture unhandled JavaScript errors
  window.addEventListener('error', function (event) {
    reportError({
      type: 'js_error',
      message: event.message,
      source: event.filename,
      line: event.lineno,
      column: event.colno,
      stack: event.error?.stack,
    });
  });

  // Capture unhandled promise rejections
  window.addEventListener('unhandledrejection', function (event) {
    reportError({
      type: 'unhandled_rejection',
      message: String(event.reason),
      stack: event.reason?.stack,
    });
  });

  // Capture failed resource loads (images, scripts, stylesheets)
  window.addEventListener('error', function (event) {
    if (event.target && event.target.tagName) {
      reportError({
        type: 'resource_error',
        resource_type: event.target.tagName.toLowerCase(),
        resource_src: event.target.src || event.target.href,
      });
    }
  }, true /* capture phase to catch resource errors */);

  function reportError(data) {
    const payload = {
      ...data,
      app_version: APP_VERSION,
      canary: IS_CANARY,
      page: window.location.pathname,
      user_agent: navigator.userAgent,
      timestamp: new Date().toISOString(),
    };

    // Non-blocking — use sendBeacon to not impact page performance
    navigator.sendBeacon('/api/errors/browser', JSON.stringify(payload));
  }
})();
```

### API Error Rate Monitoring

Track client-side API call failures — these are distinct from server-side 5xx rates because they include network errors and client-side request cancellations:

```javascript
// api-monitor.js — wrap your fetch client
const originalFetch = window.fetch;
window.fetch = async function (url, options = {}) {
  const start = performance.now();

  try {
    const response = await originalFetch(url, options);
    const duration = performance.now() - start;

    if (!response.ok && response.status >= 500) {
      reportApiError({
        url: typeof url === 'string' ? url : url.url,
        method: options.method || 'GET',
        status: response.status,
        duration_ms: Math.round(duration),
        type: 'server_error',
      });
    }

    if (duration > 3000) {
      reportSlowRequest({
        url: typeof url === 'string' ? url : url.url,
        duration_ms: Math.round(duration),
      });
    }

    return response;
  } catch (error) {
    reportApiError({
      url: typeof url === 'string' ? url : url.url,
      method: options.method || 'GET',
      error: error.message,
      type: 'network_error',
    });
    throw error;
  }
};
```

---

## Canary Runbook

Keep this runbook open and ready during every canary deploy.

### Before Deploy
- [ ] Baseline metrics recorded (error rate, p99 latency, Apdex, CWV if frontend)
- [ ] Rollback command tested in staging within the last 30 days
- [ ] On-call engineer notified that a canary deploy is in progress
- [ ] Deploy annotation sent to monitoring platform
- [ ] Canary success criteria documented and agreed upon

### During Deploy — 5% Phase (0–10 min)
- [ ] New pods healthy (`kubectl get pods`)
- [ ] Error rate on canary ≤ 1.2× baseline
- [ ] p99 latency on canary ≤ 1.2× baseline
- [ ] No new exception types in canary logs
- [ ] Health checks passing on all canary instances

### During Deploy — 20% Phase (10–25 min)
- [ ] All 5% gate checks still passing
- [ ] Apdex score on canary ≥ 98% of stable
- [ ] DB query latency within 15% of baseline
- [ ] Cache hit rate within 5% of baseline
- [ ] No customer support escalations

### During Deploy — 50% Phase (25–45 min)
- [ ] All previous gate checks still passing
- [ ] Error budget burn rate < 3× normal
- [ ] CWV within threshold (frontend only)
- [ ] Queue depths stable (async workers)
- [ ] No anomalies in log comparison (canary vs. stable)

### Promote to 100%
- [ ] All gate checks passed at 50% phase
- [ ] SLO compliance rate ≥ SLO target throughout canary window
- [ ] No open incidents attributable to canary
- [ ] Post-deploy annotation updated in monitoring platform

### Rollback Decision Tree

```
Error rate spike detected
│
├─ Is it isolated to canary cohort? ──── NO ──→ Pre-existing issue, not canary. Investigate separately.
│
└─ YES
   │
   ├─ How severe?
   │   ├─ > 5× baseline → ROLLBACK IMMEDIATELY (automated or manual)
   │   ├─ 2–5× baseline → Alert team, watch for 3 minutes, rollback if not improving
   │   └─ 1.2–2× baseline → Investigate root cause, continue at current weight, do not advance
   │
   └─ After rollback:
       ├─ Confirm error rate returning to stable baseline within 3 minutes
       ├─ Write incident timeline with deploy timestamp and rollback timestamp
       └─ Do not re-deploy without root cause identified
```

---

## Definition of Done — Canary Verification

A canary is complete and the deploy is done when ALL of these are true:

- [ ] Traffic at 100% — no canary split remaining
- [ ] Error rate at 100% traffic is ≤ pre-deploy baseline (not just ≤ gate threshold)
- [ ] p99 latency at 100% traffic is ≤ pre-deploy baseline
- [ ] Error budget consumed during canary window < 5% of daily budget
- [ ] Zero new unhandled exception types introduced
- [ ] Core Web Vitals stable or improved (frontend deployments)
- [ ] Log anomaly check clean — no new error codes vs. stable
- [ ] All synthetic health checks passing
- [ ] Deploy annotation in monitoring platform with final status (promoted / rolled back)
- [ ] Rollback runbook confirmed to be current and tested
- [ ] Post-deploy monitoring continued for 30 minutes at 100% before declaring done
- [ ] If any gate required a hold: root cause documented even if deploy ultimately succeeded
