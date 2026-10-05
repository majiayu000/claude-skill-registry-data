---
name: sre-engineer
description: Site reliability engineering expertise for building and maintaining reliable production systems. Use when defining SLOs/SLIs/error budgets, designing.
---

# SRE Engineer

Specialized expertise in site reliability engineering, providing guidance on service-level objectives, observability, incident management, capacity planning, reliability patterns, and toil reduction. Grounded in the principles from Google's SRE books and adapted for real-world production environments.

## When to Use This Skill

Use this skill for:

- Defining SLOs, SLIs, and error budgets for services
- Designing and implementing observability pipelines (metrics, logs, traces)
- Building incident response processes and on-call rotations
- Conducting blameless post-incident reviews
- Capacity planning, load testing, and autoscaling design
- Implementing reliability patterns (circuit breakers, retries, bulkheads)
- Measuring and reducing operational toil
- Chaos engineering and resilience validation

**Trigger phrases**: "SLO", "SLI", "error budget", "incident response", "postmortem", "observability", "on-call", "capacity planning", "chaos engineering", "toil reduction", "reliability", "burn rate", "load shedding"

## What This Skill Does

Provides production-ready SRE patterns including:

- **SLOs/SLIs**: Service-level objective definitions, indicator measurement, error budget policies
- **Observability**: Metrics, logs, and traces pipeline design with correlation
- **Incident Management**: Severity levels, on-call design, commander protocols, communication templates
- **Post-Incident Review**: Blameless postmortem templates, contributing factor analysis, action tracking
- **Capacity Planning**: Load testing, autoscaling policies, resource quotas, cost optimization
- **Reliability Patterns**: Circuit breakers, retry strategies, graceful degradation, chaos engineering
- **Toil Reduction**: Measurement frameworks, automation ROI, self-healing systems, GitOps

## Instructions

### Step 1: Define SLOs, SLIs, and Error Budgets

Service-level objectives are the foundation of SRE practice. Every production service needs clearly defined SLIs that measure user-facing behavior, SLOs that set reliability targets, and error budgets that balance reliability investment against feature velocity.

**SLI Categories and Measurement**:

| SLI Type | What It Measures | Example Metric |
|----------|-----------------|----------------|
| **Availability** | Proportion of successful requests | `successful_requests / total_requests` |
| **Latency** | Proportion of requests faster than threshold | `requests_under_300ms / total_requests` |
| **Throughput** | Proportion of time system handles expected load | `minutes_above_baseline / total_minutes` |
| **Correctness** | Proportion of responses returning correct data | `correct_responses / total_responses` |
| **Freshness** | Proportion of data updated within threshold | `fresh_records / total_records` |

**SLO Specification Document**:

```yaml
# slo-spec.yaml - Service Level Objective specification
service: checkout-api
team: platform-payments
version: "1.2"

slis:
  - name: availability
    description: "Proportion of non-5xx responses to total requests"
    query: |
      sum(rate(http_requests_total{service="checkout-api", code!~"5.."}[5m]))
      /
      sum(rate(http_requests_total{service="checkout-api"}[5m]))
    unit: ratio

  - name: latency_p99
    description: "Proportion of requests completing under 500ms"
    query: |
      sum(rate(http_request_duration_seconds_bucket{service="checkout-api", le="0.5"}[5m]))
      /
      sum(rate(http_request_duration_seconds_count{service="checkout-api"}[5m]))
    unit: ratio

slos:
  - name: checkout-availability
    sli: availability
    target: 0.999          # 99.9% - allows ~8.7 hours downtime per year
    window: 30d            # rolling 30-day window
    alerting:
      burn_rate_short: 14.4  # 2% budget consumed in 1 hour
      burn_rate_long: 6.0    # 5% budget consumed in 6 hours

  - name: checkout-latency
    sli: latency_p99
    target: 0.99           # 99% of requests under 500ms
    window: 30d
    alerting:
      burn_rate_short: 14.4
      burn_rate_long: 6.0

error_budget_policy:
  actions:
    - condition: "budget_remaining > 50%"
      action: "Normal feature development velocity"
    - condition: "budget_remaining > 25%"
      action: "Prioritize reliability work alongside features"
    - condition: "budget_remaining > 0%"
      action: "Halt feature launches; focus on reliability"
    - condition: "budget_remaining <= 0%"
      action: "Freeze all changes; incident-level response"
```

**Burn Rate Alerting with Prometheus**:

```yaml
# prometheus-rules.yaml - Multi-window burn rate alerts
groups:
  - name: slo-alerts
    rules:
      # Fast burn: 2% of 30-day budget consumed in 1 hour
      - alert: CheckoutHighErrorBurnRate
        expr: |
          (
            1 - (sum(rate(http_requests_total{service="checkout-api", code!~"5.."}[1h]))
            / sum(rate(http_requests_total{service="checkout-api"}[1h])))
          )
          /
          (1 - 0.999) > 14.4
          AND
          (
            1 - (sum(rate(http_requests_total{service="checkout-api", code!~"5.."}[5m]))
            / sum(rate(http_requests_total{service="checkout-api"}[5m])))
          )
          /
          (1 - 0.999) > 14.4
        for: 2m
        labels:
          severity: critical
          team: platform-payments
        annotations:
          summary: "Checkout API burning error budget rapidly"
          description: "Burn rate {{ $value }}x over 1h window. Budget will exhaust in {{ printf \"%.1f\" (div 100 $value) }} hours."
          runbook: "https://runbooks.internal/checkout-api/high-error-rate"

      # Slow burn: 5% of 30-day budget consumed in 6 hours
      - alert: CheckoutSlowErrorBurnRate
        expr: |
          (
            1 - (sum(rate(http_requests_total{service="checkout-api", code!~"5.."}[6h]))
            / sum(rate(http_requests_total{service="checkout-api"}[6h])))
          )
          /
          (1 - 0.999) > 6.0
          AND
          (
            1 - (sum(rate(http_requests_total{service="checkout-api", code!~"5.."}[30m]))
            / sum(rate(http_requests_total{service="checkout-api"}[30m])))
          )
          /
          (1 - 0.999) > 6.0
        for: 5m
        labels:
          severity: warning
          team: platform-payments
        annotations:
          summary: "Checkout API burning error budget steadily"
          runbook: "https://runbooks.internal/checkout-api/slow-burn"

      # Error budget remaining gauge
      - record: slo:error_budget_remaining:ratio
        expr: |
          1 - (
            (1 - (sum_over_time((sum(rate(http_requests_total{service="checkout-api", code!~"5.."}[5m]))[30d:5m]))
            / sum_over_time((sum(rate(http_requests_total{service="checkout-api"}[5m]))[30d:5m]))))
            /
            (1 - 0.999)
          )
```

**Error Budget Calculation**:

```
Error budget (30 days) = 1 - SLO target
For 99.9% SLO:  error budget = 0.1% = 43.2 minutes of total downtime
For 99.95% SLO: error budget = 0.05% = 21.6 minutes of total downtime
For 99.99% SLO: error budget = 0.01% = 4.32 minutes of total downtime

Budget consumed = (actual_bad_minutes / allowed_bad_minutes) * 100
Budget remaining = 100% - budget_consumed
```

### Step 2: Design the Observability Stack

Observability requires three pillars (metrics, logs, traces) working together with correlation so that operators can move from alert to root cause in minutes rather than hours.

**Observability Architecture**:

```
                    ┌─────────────────────────────────────────────┐
                    │              Grafana Dashboards              │
                    │         (Unified view of all signals)        │
                    └───────┬──────────┬──────────┬───────────────┘
                            │          │          │
                    ┌───────▼───┐ ┌────▼────┐ ┌───▼──────────┐
                    │Prometheus │ │  Loki   │ │    Tempo      │
                    │ (Metrics) │ │ (Logs)  │ │  (Traces)     │
                    └───────▲───┘ └────▲────┘ └───▲──────────┘
                            │          │          │
                    ┌───────┴──────────┴──────────┴───────────┐
                    │         OpenTelemetry Collector           │
                    │   (Receives, processes, exports all       │
                    │    telemetry with unified pipeline)       │
                    └───────▲──────────▲──────────▲───────────┘
                            │          │          │
                   ┌────────┴──┐ ┌─────┴────┐ ┌──┴─────────┐
                   │ Service A │ │ Service B│ │ Service C  │
                   │ (OTel SDK)│ │(OTel SDK)│ │(OTel SDK)  │
                   └───────────┘ └──────────┘ └────────────┘
```

**OpenTelemetry Collector Configuration**:

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
  prometheus:
    config:
      scrape_configs:
        - job_name: 'kubernetes-pods'
          kubernetes_sd_configs:
            - role: pod
          relabel_configs:
            - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
              action: keep
              regex: true

processors:
  batch:
    timeout: 5s
    send_batch_size: 1000
  memory_limiter:
    check_interval: 1s
    limit_mib: 512
    spike_limit_mib: 128
  attributes:
    actions:
      - key: environment
        value: production
        action: upsert
      - key: cluster
        value: us-east-1-prod
        action: upsert
  tail_sampling:
    decision_wait: 10s
    policies:
      - name: errors-always
        type: status_code
        status_code: { status_codes: [ERROR] }
      - name: slow-requests
        type: latency
        latency: { threshold_ms: 1000 }
      - name: probabilistic-sample
        type: probabilistic
        probabilistic: { sampling_percentage: 10 }

exporters:
  prometheusremotewrite:
    endpoint: "http://prometheus:9090/api/v1/write"
  loki:
    endpoint: "http://loki:3100/loki/api/v1/push"
  otlp/tempo:
    endpoint: "tempo:4317"
    tls:
      insecure: true

service:
  pipelines:
    metrics:
      receivers: [otlp, prometheus]
      processors: [memory_limiter, batch]
      exporters: [prometheusremotewrite]
    logs:
      receivers: [otlp]
      processors: [memory_limiter, attributes, batch]
      exporters: [loki]
    traces:
      receivers: [otlp]
      processors: [memory_limiter, tail_sampling, batch]
      exporters: [otlp/tempo]
```

**Structured Logging Standard**:

```json
{
  "timestamp": "2026-03-20T14:23:01.123Z",
  "level": "ERROR",
  "service": "checkout-api",
  "trace_id": "abc123def456",
  "span_id": "789ghi012",
  "correlation_id": "order-98765",
  "message": "Payment processing failed",
  "error": {
    "type": "PaymentGatewayTimeout",
    "message": "Upstream timeout after 5000ms",
    "stack": "..."
  },
  "context": {
    "user_id": "u-12345",
    "order_id": "ord-98765",
    "payment_method": "credit_card",
    "amount_cents": 4999
  },
  "http": {
    "method": "POST",
    "path": "/api/v1/checkout",
    "status_code": 504,
    "duration_ms": 5023
  }
}
```

**Grafana Dashboard as Code**:

```json
{
  "dashboard": {
    "title": "Service SLO Dashboard",
    "panels": [
      {
        "title": "Error Budget Remaining (30d)",
        "type": "gauge",
        "targets": [{
          "expr": "slo:error_budget_remaining:ratio{service=\"checkout-api\"} * 100",
          "legendFormat": "Budget %"
        }],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                { "color": "red", "value": 0 },
                { "color": "orange", "value": 25 },
                { "color": "yellow", "value": 50 },
                { "color": "green", "value": 75 }
              ]
            },
            "min": 0, "max": 100, "unit": "percent"
          }
        }
      },
      {
        "title": "Request Rate and Errors",
        "type": "timeseries",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{service=\"checkout-api\"}[5m]))",
            "legendFormat": "Total RPS"
          },
          {
            "expr": "sum(rate(http_requests_total{service=\"checkout-api\", code=~\"5..\"}[5m]))",
            "legendFormat": "Error RPS"
          }
        ]
      },
      {
        "title": "Latency Distribution",
        "type": "heatmap",
        "targets": [{
          "expr": "sum(rate(http_request_duration_seconds_bucket{service=\"checkout-api\"}[5m])) by (le)",
          "legendFormat": "{{le}}"
        }]
      }
    ]
  }
}
```

### Step 3: Build Incident Management Processes

Effective incident management requires clear severity definitions, well-structured on-call rotations, defined roles, and communication protocols that minimize confusion during high-stress situations.

**Incident Severity Levels**:

| Severity | Criteria | Response Time | Notification | Example |
|----------|----------|--------------|--------------|---------|
| **SEV1** | Service down, all users affected, revenue impact | 5 minutes | Page on-call + IC + leadership | Complete checkout outage |
| **SEV2** | Major degradation, many users affected | 15 minutes | Page on-call + IC | Checkout latency 10x normal |
| **SEV3** | Partial degradation, subset of users affected | 30 minutes | Notify on-call | One payment provider failing |
| **SEV4** | Minor issue, workaround available | Next business day | Ticket | Slow dashboard loading |

**On-Call Rotation Configuration (PagerDuty)**:

```yaml
# pagerduty-terraform.tf equivalent as YAML spec
on_call_schedule:
  name: "platform-primary"
  timezone: "UTC"
  rotation:
    type: weekly
    handoff_time: "09:00"
    handoff_day: monday
    participants:
      - engineer_a
      - engineer_b
      - engineer_c
      - engineer_d
    # Minimum 4 engineers for sustainable rotation

escalation_policy:
  name: "platform-escalation"
  rules:
    - level: 1
      target: "platform-primary"        # On-call engineer
      timeout_minutes: 5
    - level: 2
      target: "platform-secondary"      # Backup on-call
      timeout_minutes: 10
    - level: 3
      target: "platform-engineering-manager"
      timeout_minutes: 15

on_call_expectations:
  acknowledgement_sla: "5 minutes for SEV1, 15 minutes for SEV2"
  laptop_required: true
  alcohol_restriction: true
  handoff_checklist:
    - "Review open incidents and active alerts"
    - "Check error budget dashboards"
    - "Read handoff notes from previous on-call"
    - "Verify pager and notification settings"
```

**Incident Commander Checklist**:

```markdown
## Incident Commander Actions

### First 5 Minutes
- [ ] Acknowledge the page and claim IC role
- [ ] Open incident channel: #inc-YYYYMMDD-short-description
- [ ] Post initial assessment: what is broken, who is affected, estimated severity
- [ ] Page additional responders if needed (subject matter experts)
- [ ] Start the incident timeline document

### Ongoing (every 15 minutes)
- [ ] Post status update to incident channel
- [ ] Update status page if customer-facing
- [ ] Coordinate between investigation streams
- [ ] Decide: escalate, mitigate, or continue investigating
- [ ] Track action items and owners

### Resolution
- [ ] Confirm service recovery with monitoring data
- [ ] Post final status update
- [ ] Update status page to resolved
- [ ] Schedule postmortem within 48 hours
- [ ] Send incident summary to stakeholders
```

**Communication Templates**:

```markdown
## Initial Notification (Internal)
INCIDENT DECLARED - SEV[1/2]
Service: [service name]
Impact: [user-facing description of the problem]
Start time: [HH:MM UTC]
IC: [name]
Channel: #inc-[date]-[slug]
Status page: [link]

## Status Page Update (External)
Title: [Service] Degraded Performance
Status: Investigating
Body: We are investigating reports of [brief description]. Some users
may experience [specific symptoms]. Our engineering team is actively
working on resolution. We will provide updates every 30 minutes.

## Resolution Notification (Internal)
INCIDENT RESOLVED - SEV[1/2]
Service: [service name]
Duration: [X hours Y minutes]
Root cause: [one sentence]
Mitigation: [what was done to fix it]
Postmortem scheduled: [date/time]
Action items: [count] items tracked in [link]
```

### Step 4: Conduct Post-Incident Reviews

Blameless postmortems are the primary mechanism for organizational learning after incidents. The goal is to understand what happened, identify systemic improvements, and prevent recurrence without assigning individual blame.

**Blameless Postmortem Template**:

```markdown
# Postmortem: [Incident Title]

**Date**: YYYY-MM-DD
**Severity**: SEV-X
**Duration**: X hours Y minutes
**Author**: [name]
**Reviewers**: [names]
**Status**: Draft | In Review | Approved | Action Items Complete

## Executive Summary

[2-3 sentences describing what happened, the impact, and the resolution.
Write for an audience that was not involved in the incident.]

## Impact

- **Users affected**: [number or percentage]
- **Revenue impact**: [estimated dollar amount or "none"]
- **SLO impact**: [X% of monthly error budget consumed]
- **Duration of user-visible impact**: [time]
- **Support tickets generated**: [count]

## Timeline (all times UTC)

| Time | Event |
|------|-------|
| 14:00 | Deployment of checkout-api v2.3.1 begins |
| 14:05 | Error rate increases from 0.1% to 5% |
| 14:07 | Burn rate alert fires, on-call paged |
| 14:09 | On-call acknowledges, begins investigation |
| 14:15 | IC declared, incident channel opened |
| 14:22 | Root cause identified: database connection pool exhaustion |
| 14:25 | Rollback initiated |
| 14:31 | Rollback complete, error rate returning to baseline |
| 14:45 | Confirmed recovery, incident resolved |

## Contributing Factors

[List systemic factors, not individual mistakes. Use "the system"
or "the process" as the subject, never a person's name.]

1. **Missing connection pool limits**: The new database client library defaults to unlimited connections, and the deployment did not include explicit pool size configuration.
2. **No canary deployment**: The change was rolled out to 100% of instances simultaneously, preventing early detection of the issue in a smaller blast radius.
3. **Alert gap**: Existing alerts monitored HTTP error rates but not database connection pool utilization, delaying root cause identification by several minutes.

## What Went Well

- On-call response time was under 2 minutes
- Rollback procedure worked as documented
- Incident communication was clear and timely
- Status page was updated within 10 minutes

## What Could Be Improved

- Canary deployments should have caught this before full rollout
- Database connection metrics should be part of standard dashboards
- The deployment checklist does not include verifying connection pool settings

## Action Items

| ID | Action | Owner | Priority | Due Date | Status |
|----|--------|-------|----------|----------|--------|
| AI-1 | Add connection pool size to deployment checklist | @alice | P1 | 2026-04-01 | Open |
| AI-2 | Implement canary deployment for checkout-api | @bob | P1 | 2026-04-15 | Open |
| AI-3 | Add database connection pool utilization alert | @carol | P2 | 2026-04-05 | Open |
| AI-4 | Add connection pool dashboard panel | @carol | P3 | 2026-04-10 | Open |

## Lessons Learned

[Broader takeaways that apply beyond this specific incident.]

1. Library upgrades that change default connection behavior need explicit review of resource limits.
2. Any service handling financial transactions should use canary deployments.
3. Dashboard coverage should include all resource pool metrics (connections, threads, file descriptors).
```

**Action Item Tracking and Verification**:

```bash
#!/usr/bin/env bash
set -euo pipefail

# postmortem-tracker.sh - Track and verify postmortem action items
# Queries your issue tracker for open postmortem actions

log_info()  { printf "[INFO]  %s\n" "$*" >&2; }
log_error() { printf "[ERROR] %s\n" "$*" >&2; }

readonly LABEL="postmortem-action"
readonly OVERDUE_DAYS=14

check_overdue_actions() {
    local cutoff_date
    cutoff_date=$(date -d "-${OVERDUE_DAYS} days" +%Y-%m-%d 2>/dev/null \
                  || date -v-${OVERDUE_DAYS}d +%Y-%m-%d)

    log_info "Checking for postmortem actions overdue since ${cutoff_date}"

    local overdue_count
    overdue_count=$(gh issue list \
        --label "${LABEL}" \
        --state open \
        --json createdAt,title,assignees,number \
        --jq "[.[] | select(.createdAt < \"${cutoff_date}\")] | length")

    if [[ "${overdue_count}" -gt 0 ]]; then
        log_error "${overdue_count} postmortem action(s) are overdue"
        gh issue list \
            --label "${LABEL}" \
            --state open \
            --json number,title,assignees,createdAt \
            --jq ".[] | select(.createdAt < \"${cutoff_date}\") | \"#\(.number): \(.title) (assigned: \(.assignees | map(.login) | join(\", \")))\""
        return 1
    fi

    log_info "No overdue postmortem actions found"
    return 0
}

check_overdue_actions
```

### Step 5: Plan Capacity and Scaling

Capacity planning combines load testing, resource modeling, and autoscaling configuration to ensure services handle current traffic with headroom for growth while avoiding wasteful over-provisioning.

**Load Testing Methodology with k6**:

```javascript
// load-test.js - Staged load test with SLO validation
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const latencyP99 = new Trend('latency_p99');

export const options = {
  stages: [
    { duration: '5m',  target: 100 },   // Ramp up to baseline
    { duration: '10m', target: 100 },   // Sustain baseline
    { duration: '5m',  target: 300 },   // Ramp to 3x baseline
    { duration: '10m', target: 300 },   // Sustain 3x
    { duration: '5m',  target: 500 },   // Ramp to 5x (stress)
    { duration: '10m', target: 500 },   // Sustain stress
    { duration: '5m',  target: 0 },     // Ramp down
  ],
  thresholds: {
    'http_req_duration': ['p(99)<500'],    // 99th percentile < 500ms
    'errors':            ['rate<0.001'],    // Error rate < 0.1%
    'http_req_failed':   ['rate<0.001'],
  },
};

export default function () {
  const params = {
    headers: {
      'Content-Type': 'application/json',
      'X-Load-Test': 'true',
    },
    timeout: '10s',
  };

  // Simulate realistic user journey
  const responses = http.batch([
    ['GET',  'https://api.example.com/products',        null, params],
    ['GET',  'https://api.example.com/cart',             null, params],
    ['POST', 'https://api.example.com/cart/items',
      JSON.stringify({ product_id: 'prod-123', qty: 1 }), params],
  ]);

  responses.forEach((res) => {
    check(res, {
      'status is 2xx': (r) => r.status >= 200 && r.status < 300,
      'latency < 500ms': (r) => r.timings.duration < 500,
    });
    errorRate.add(res.status >= 500);
    latencyP99.add(res.timings.duration);
  });

  sleep(1);
}
```

**Kubernetes Autoscaling Configuration**:

```yaml
# hpa.yaml - Horizontal Pod Autoscaler with custom metrics
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: checkout-api
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: checkout-api
  minReplicas: 3
  maxReplicas: 50
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 50           # Scale up by at most 50% at a time
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10           # Scale down slowly to avoid flapping
          periodSeconds: 120
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "100"
---
# vpa.yaml - Vertical Pod Autoscaler for right-sizing
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: checkout-api-vpa
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: checkout-api
  updatePolicy:
    updateMode: "Off"       # Recommendation-only mode initially
  resourcePolicy:
    containerPolicies:
      - containerName: checkout-api
        minAllowed:
          cpu: 100m
          memory: 128Mi
        maxAllowed:
          cpu: 4
          memory: 8Gi
```

**Resource Quotas and Limits**:

```yaml
# resource-quota.yaml - Namespace resource governance
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    requests.cpu: "100"
    requests.memory: 200Gi
    limits.cpu: "200"
    limits.memory: 400Gi
    pods: "500"
    services: "50"
    persistentvolumeclaims: "100"
---
# limit-range.yaml - Default container resource bounds
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: production
spec:
  limits:
    - default:
        cpu: 500m
        memory: 512Mi
      defaultRequest:
        cpu: 100m
        memory: 128Mi
      type: Container
```

**Capacity Model Spreadsheet Format**:

```
Service: checkout-api
Current baseline: 1,000 RPS
Current instances: 5 (c5.xlarge equivalent)
Per-instance capacity: ~250 RPS at p99 < 500ms

Growth forecast:
  3 months:  1,500 RPS (+50%)  -> 6 instances + 2 headroom = 8
  6 months:  2,200 RPS (+120%) -> 9 instances + 3 headroom = 12
  12 months: 3,500 RPS (+250%) -> 14 instances + 4 headroom = 18

Cost projection (on-demand):
  Current:   5 x $0.17/hr  = $612/month
  3 months:  8 x $0.17/hr  = $979/month
  6 months:  12 x $0.17/hr = $1,468/month
  12 months: 18 x $0.17/hr = $2,203/month

Savings with reserved (1yr, no upfront):
  12 months: 18 x $0.11/hr = $1,426/month (35% savings)
```

### Step 6: Implement Reliability Patterns

Reliability patterns prevent cascading failures, manage load during degraded conditions, and validate system resilience through controlled experiments.

**Circuit Breaker Pattern (Envoy Sidecar)**:

```yaml
# envoy-circuit-breaker.yaml - Istio DestinationRule
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: payment-service
  namespace: production
spec:
  host: payment-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
        connectTimeout: 5s
      http:
        h2UpgradePolicy: DEFAULT
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
        maxRequestsPerConnection: 10
        maxRetries: 3
    outlierDetection:
      consecutive5xxErrors: 5       # Trip after 5 consecutive 5xx
      interval: 10s                 # Check every 10 seconds
      baseEjectionTime: 30s         # Eject for 30 seconds minimum
      maxEjectionPercent: 50        # Never eject more than 50% of hosts
      minHealthPercent: 30          # Disable ejection below 30% healthy
```

**Retry with Exponential Backoff (Application Level)**:

```python
import random
import time
import logging
from functools import wraps
from typing import TypeVar, Callable, Any

logger = logging.getLogger(__name__)
T = TypeVar("T")


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    retryable_exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator implementing retry with exponential backoff and jitter."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception: Exception | None = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e
                    if attempt == max_retries:
                        logger.error(
                            "All %d retries exhausted for %s: %s",
                            max_retries, func.__name__, e,
                        )
                        raise
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    jitter = random.uniform(0, delay * 0.1)
                    total_delay = delay + jitter
                    logger.warning(
                        "Attempt %d/%d for %s failed (%s), retrying in %.1fs",
                        attempt + 1, max_retries, func.__name__, e, total_delay,
                    )
                    time.sleep(total_delay)
            raise last_exception  # type: ignore[misc]
        return wrapper
    return decorator


@retry_with_backoff(max_retries=3, base_delay=0.5, retryable_exceptions=(TimeoutError, ConnectionError))
def call_payment_gateway(order_id: str, amount_cents: int) -> dict[str, Any]:
    """Call external payment gateway with automatic retry."""
    # Implementation here
    ...
```

**Graceful Degradation Configuration**:

```yaml
# feature-flags.yaml - Degradation levels
degradation_levels:
  normal:
    recommendations: enabled
    search_autocomplete: enabled
    analytics_tracking: enabled
    image_quality: high

  level_1:  # Shed non-essential features
    recommendations: disabled
    search_autocomplete: enabled
    analytics_tracking: async_only
    image_quality: medium
    trigger: "error_budget_remaining < 50%"

  level_2:  # Protect core functionality
    recommendations: disabled
    search_autocomplete: disabled
    analytics_tracking: disabled
    image_quality: low
    trigger: "error_budget_remaining < 25% OR p99_latency > 2s"

  level_3:  # Emergency mode
    recommendations: disabled
    search_autocomplete: disabled
    analytics_tracking: disabled
    image_quality: disabled
    static_content_only: true
    trigger: "error_budget_exhausted OR SEV1_active"
```

**Chaos Engineering Experiment (LitmusChaos)**:

```yaml
# chaos-experiment.yaml - Pod kill experiment
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: checkout-pod-kill
  namespace: production
spec:
  appinfo:
    appns: production
    applabel: "app=checkout-api"
    appkind: deployment
  engineState: active
  chaosServiceAccount: litmus-admin
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: "60"            # Kill pods for 60 seconds
            - name: CHAOS_INTERVAL
              value: "10"            # Kill a pod every 10 seconds
            - name: FORCE
              value: "false"         # Graceful termination
            - name: PODS_AFFECTED_PERC
              value: "30"            # Affect 30% of pods
        probe:
          - name: "slo-check"
            type: "promProbe"
            mode: "Continuous"
            runProperties:
              probeTimeout: 5
              interval: 10
              retry: 3
            promProbe/inputs:
              endpoint: "http://prometheus:9090"
              query: |
                sum(rate(http_requests_total{service="checkout-api", code!~"5.."}[1m]))
                / sum(rate(http_requests_total{service="checkout-api"}[1m]))
              comparator:
                type: "float"
                criteria: ">="
                value: "0.999"       # SLO must hold during chaos
---
# chaos-schedule.yaml - Run weekly in staging
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosSchedule
metadata:
  name: weekly-resilience-test
  namespace: staging
spec:
  schedule:
    repeat:
      timeRange:
        startTime: "2026-01-01T09:00:00Z"
      properties:
        minChaosInterval: "168h"     # Weekly
      workDays:
        includedDays: "Tue"
  engineTemplateSpec:
    appinfo:
      appns: staging
      applabel: "app=checkout-api"
      appkind: deployment
    experiments:
      - name: pod-delete
      - name: pod-network-latency
      - name: pod-cpu-hog
```

**Load Shedding with Priority Queues**:

```yaml
# envoy-rate-limit.yaml - Priority-based rate limiting
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: checkout-rate-limit
  namespace: production
spec:
  workloadSelector:
    labels:
      app: checkout-api
  configPatches:
    - applyTo: HTTP_FILTER
      match:
        context: SIDECAR_INBOUND
        listener:
          filterChain:
            filter:
              name: envoy.filters.network.http_connection_manager
      patch:
        operation: INSERT_BEFORE
        value:
          name: envoy.filters.http.local_ratelimit
          typed_config:
            "@type": type.googleapis.com/udpa.type.v1.TypedStruct
            type_url: type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
            value:
              stat_prefix: http_local_rate_limiter
              token_bucket:
                max_tokens: 1000
                tokens_per_fill: 1000
                fill_interval: 1s
              filter_enabled:
                runtime_key: local_rate_limit_enabled
                default_value:
                  numerator: 100
                  denominator: HUNDRED
```

### Step 7: Reduce Toil Through Automation

Toil is repetitive, manual, automatable work that scales linearly with service growth. SRE teams should measure toil, prioritize automation by ROI, and build self-healing systems that handle routine operational tasks without human intervention.

**Toil Measurement Framework**:

| Characteristic | Question | Score (1-5) |
|---------------|----------|-------------|
| **Manual** | Does it require a human to perform? | |
| **Repetitive** | Does it recur regularly? | |
| **Automatable** | Could a machine do it? | |
| **Tactical** | Is it reactive rather than strategic? | |
| **No lasting value** | Does the system return to its previous state? | |
| **Scales linearly** | Does effort grow with service size? | |

```
Toil score = sum of all characteristics / 30
Toil > 0.5: High priority for automation
Toil 0.3-0.5: Medium priority
Toil < 0.3: Low priority or may not be true toil
```

**Automation ROI Calculation**:

```
Time saved per occurrence:     T_save = T_manual - T_automated
Occurrences per month:         N
Development cost (one-time):   T_dev (hours to build automation)
Maintenance cost (monthly):    T_maint (hours to maintain)

Monthly savings:   S_monthly = (T_save * N) - T_maint
Break-even point:  T_dev / S_monthly = months to ROI

Example: Certificate renewal
  T_manual = 2 hours (per renewal, including verification)
  T_automated = 0.1 hours (monitoring check)
  N = 12 per month (across all services)
  T_dev = 40 hours
  T_maint = 2 hours/month

  S_monthly = (1.9 * 12) - 2 = 20.8 hours/month
  Break-even = 40 / 20.8 = 1.9 months
```

**Self-Healing with Kubernetes Operators**:

```yaml
# self-healing-rules.yaml - Custom operator configuration
apiVersion: remediation.sre.io/v1
kind: RemediationRule
metadata:
  name: restart-on-oom
  namespace: production
spec:
  selector:
    matchLabels:
      app: checkout-api
  triggers:
    - type: event
      event:
        reason: OOMKilled
        count: 2
        window: 10m
  actions:
    - type: restart
      params:
        strategy: rolling
        maxUnavailable: 1
    - type: notify
      params:
        channel: "#sre-alerts"
        message: "Auto-restarted {{ .PodName }} after repeated OOM kills. Investigate memory leak."
    - type: ticket
      params:
        project: SRE
        type: bug
        title: "Repeated OOM kills on {{ .Deployment }}"
        labels: ["auto-generated", "memory-leak"]
---
apiVersion: remediation.sre.io/v1
kind: RemediationRule
metadata:
  name: scale-on-queue-depth
  namespace: production
spec:
  selector:
    matchLabels:
      app: order-processor
  triggers:
    - type: metric
      metric:
        query: "avg(sqs_queue_depth{queue='orders'})"
        threshold: 1000
        for: 5m
  actions:
    - type: scale
      params:
        replicas: "+50%"
        maxReplicas: 30
        cooldown: 10m
    - type: notify
      params:
        channel: "#sre-alerts"
        message: "Auto-scaled order-processor due to queue depth {{ .MetricValue }}. Current replicas: {{ .CurrentReplicas }} -> {{ .NewReplicas }}"
```

**GitOps for Infrastructure (Flux)**:

```yaml
# flux-system/kustomization.yaml - GitOps reconciliation
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: production-apps
  namespace: flux-system
spec:
  interval: 5m
  retryInterval: 2m
  timeout: 10m
  sourceRef:
    kind: GitRepository
    name: infrastructure
  path: ./clusters/production
  prune: true
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: checkout-api
      namespace: production
    - apiVersion: apps/v1
      kind: Deployment
      name: order-processor
      namespace: production
  patches:
    - patch: |
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: all
        spec:
          template:
            metadata:
              annotations:
                sidecar.istio.io/inject: "true"
      target:
        kind: Deployment
        namespace: production
---
# flux-system/alerts.yaml - GitOps failure notifications
apiVersion: notification.toolkit.fluxcd.io/v1beta3
kind: Alert
metadata:
  name: deployment-failures
  namespace: flux-system
spec:
  providerRef:
    name: slack-provider
  eventSeverity: error
  eventSources:
    - kind: Kustomization
      name: "*"
    - kind: HelmRelease
      name: "*"
  summary: "GitOps reconciliation failure detected"
```

**Runbook Automation Script**:

```bash
#!/usr/bin/env bash
set -euo pipefail

# runbook-db-failover.sh - Automated database failover runbook
# Executes pre-validated steps for RDS failover with safety checks

log_info()  { printf "[INFO]  %s\n" "$*" >&2; }
log_error() { printf "[ERROR] %s\n" "$*" >&2; }

readonly DB_CLUSTER="${1:?Usage: runbook-db-failover.sh <cluster-identifier>}"
readonly REGION="${AWS_REGION:-us-east-1}"
readonly MAX_WAIT_SECONDS=300

preflight_checks() {
    log_info "Running preflight checks"

    # Verify cluster exists and has a replica
    local reader_count
    reader_count=$(aws rds describe-db-clusters \
        --db-cluster-identifier "${DB_CLUSTER}" \
        --region "${REGION}" \
        --query "DBClusters[0].DBClusterMembers[?IsClusterWriter==\`false\`] | length(@)" \
        --output text)

    if [[ "${reader_count}" -lt 1 ]]; then
        log_error "No read replicas found for cluster ${DB_CLUSTER}. Cannot failover."
        return 1
    fi

    log_info "Found ${reader_count} read replica(s). Preflight passed."
    return 0
}

execute_failover() {
    log_info "Initiating failover for cluster ${DB_CLUSTER}"

    aws rds failover-db-cluster \
        --db-cluster-identifier "${DB_CLUSTER}" \
        --region "${REGION}"

    log_info "Failover initiated. Waiting for cluster to become available."

    local elapsed=0
    while [[ "${elapsed}" -lt "${MAX_WAIT_SECONDS}" ]]; do
        local status
        status=$(aws rds describe-db-clusters \
            --db-cluster-identifier "${DB_CLUSTER}" \
            --region "${REGION}" \
            --query "DBClusters[0].Status" \
            --output text)

        if [[ "${status}" == "available" ]]; then
            log_info "Cluster ${DB_CLUSTER} is available after failover"
            return 0
        fi

        log_info "Cluster status: ${status}. Waiting... (${elapsed}s / ${MAX_WAIT_SECONDS}s)"
        sleep 10
        elapsed=$((elapsed + 10))
    done

    log_error "Cluster did not become available within ${MAX_WAIT_SECONDS}s"
    return 1
}

verify_failover() {
    log_info "Verifying failover success"

    local new_writer
    new_writer=$(aws rds describe-db-clusters \
        --db-cluster-identifier "${DB_CLUSTER}" \
        --region "${REGION}" \
        --query "DBClusters[0].DBClusterMembers[?IsClusterWriter==\`true\`].DBInstanceIdentifier" \
        --output text)

    log_info "New writer instance: ${new_writer}"

    # Verify application connectivity
    log_info "Checking application health endpoint"
    local health_status
    health_status=$(curl --max-time 10 --connect-timeout 5 -s -o /dev/null -w "%{http_code}" \
        "https://api.example.com/health")

    if [[ "${health_status}" == "200" ]]; then
        log_info "Application health check passed (HTTP ${health_status})"
        return 0
    else
        log_error "Application health check failed (HTTP ${health_status})"
        return 1
    fi
}

main() {
    log_info "=== Database Failover Runbook ==="
    log_info "Cluster: ${DB_CLUSTER}"
    log_info "Region: ${REGION}"

    preflight_checks
    execute_failover
    verify_failover

    log_info "=== Failover Complete ==="
}

main
```

## Best Practices

- **Set SLOs before building features**: reliability targets should drive architectural decisions, not be retrofitted after launch
- **Alert on symptoms, not causes**: users care about error rates and latency, not CPU utilization or disk space in isolation
- **Keep error budgets visible**: display remaining budget on team dashboards so everyone understands the reliability posture
- **Practice incidents before they happen**: run regular game days and tabletop exercises with realistic failure scenarios
- **Automate the second occurrence**: the first time a manual task appears, document it as a runbook; the second time, automate it
- **Measure toil quarterly**: track the percentage of engineering time spent on toil and set reduction targets
- **Make postmortems blameless in practice, not just in policy**: focus on system improvements, and never name individuals as root causes
- **Use progressive rollouts**: canary deployments, feature flags, and traffic shifting reduce the blast radius of changes
- **Test your monitoring**: if you have never seen an alert fire, you do not know if it works
- **Keep runbooks current**: stale runbooks are worse than no runbooks because they create false confidence

## Quality Checklist

- [ ] SLOs defined for all user-facing services
- [ ] Error budgets calculated and tracked on dashboards
- [ ] Burn rate alerts configured with multi-window strategy
- [ ] Structured logging with trace/correlation ID propagation
- [ ] On-call rotation with at least 4 engineers
- [ ] Incident severity levels defined and documented
- [ ] Postmortem template adopted and action items tracked
- [ ] Load tests run before major releases
- [ ] Autoscaling configured with appropriate min/max bounds
- [ ] Circuit breakers on all external service calls
- [ ] Chaos experiments running in staging on a schedule
- [ ] Toil measured and reduction targets set

## Related Skills

- `cloud-architect` - Cloud infrastructure design
- `kubernetes-expert` - Container orchestration and scaling
- `observability-setup` - Monitoring and alerting implementation
- `terraform-specialist` - Infrastructure as code
- `cicd-architect` - Deployment pipeline design

---

**Version**: 1.0.0
**Last Updated**: March 2026
**Based on**: Google SRE books, OpenTelemetry standards, Kubernetes best practices


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
