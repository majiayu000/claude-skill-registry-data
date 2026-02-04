---
name: slo-sli-design
description: Design Service Level Objectives, Indicators, and error budgets
allowed-tools: Read, Glob, Grep, Write, Edit
---

# SLO/SLI Design Skill

## When to Use This Skill

Use this skill when:

- **Slo Sli Design tasks** - Working on design service level objectives, indicators, and error budgets
- **Planning or design** - Need guidance on Slo Sli Design approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Design Service Level Objectives, Indicators, and error budget policies.

## MANDATORY: Documentation-First Approach

Before designing SLOs:

1. **Invoke `docs-management` skill** for SLO/SLI patterns
2. **Verify SRE practices** via MCP servers (perplexity)
3. **Base guidance on Google SRE and industry best practices**

## SLO/SLI/SLA Hierarchy

```text
SLO/SLI/SLA RELATIONSHIP:

┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  SLA (Service Level Agreement)                                   │
│  ├── External promise to customers                               │
│  ├── Legal/contractual implications                              │
│  └── Example: "99.9% monthly uptime"                             │
│                                                                  │
│       ▲                                                          │
│       │ Buffer (SLO should be tighter)                           │
│       │                                                          │
│  SLO (Service Level Objective)                                   │
│  ├── Internal reliability target                                 │
│  ├── Tighter than SLA (headroom)                                 │
│  └── Example: "99.95% monthly availability"                      │
│                                                                  │
│       ▲                                                          │
│       │ Measured by                                              │
│       │                                                          │
│  SLI (Service Level Indicator)                                   │
│  ├── Actual measurement                                          │
│  ├── Quantitative metric                                         │
│  └── Example: "successful_requests / total_requests"             │
│                                                                  │
│       ▲                                                          │
│       │ Derived from                                             │
│       │                                                          │
│  Error Budget                                                    │
│  ├── Allowable unreliability: 100% - SLO                         │
│  ├── Example: 0.05% = 21.6 minutes/month                         │
│  └── Spent on: releases, incidents, maintenance                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Common SLI Types

```text
SLI CATEGORIES:

AVAILABILITY SLI:
"The proportion of requests that are served successfully"

Formula: successful_requests / total_requests × 100%

Good Events: HTTP 2xx, 3xx, 4xx (client errors)
Bad Events: HTTP 5xx, timeouts, connection failures

Example Prometheus query:
  sum(rate(http_requests_total{status!~"5.."}[5m]))
  /
  sum(rate(http_requests_total[5m]))

───────────────────────────────────────────────────────────────

LATENCY SLI:
"The proportion of requests that are served within threshold"

Formula: requests_below_threshold / total_requests × 100%

Thresholds (example):
- P50: 100ms (median experience)
- P95: 500ms (95th percentile)
- P99: 1000ms (tail latency)

Example Prometheus query:
  sum(rate(http_request_duration_bucket{le="0.5"}[5m]))
  /
  sum(rate(http_request_duration_count[5m]))

───────────────────────────────────────────────────────────────

QUALITY/CORRECTNESS SLI:
"The proportion of requests that return correct results"

Formula: correct_responses / total_responses × 100%

Good Events: Valid data, expected format
Bad Events: Data corruption, stale data, wrong results

───────────────────────────────────────────────────────────────

FRESHNESS SLI:
"The proportion of data that is updated within threshold"

Formula: fresh_records / total_records × 100%

Example: "95% of records updated within 5 minutes"

───────────────────────────────────────────────────────────────

THROUGHPUT SLI:
"The proportion of time system handles expected load"

Formula: time_at_capacity / total_time × 100%

Example: "System handles 1000 req/s 99% of the time"
```

## Error Budget Calculation

```text
ERROR BUDGET MATH:

Monthly Error Budget (30 days):

SLO Target  │ Error Budget │ Allowed Downtime
────────────┼──────────────┼──────────────────
99%         │ 1%           │ 7h 18m
99.5%       │ 0.5%         │ 3h 39m
99.9%       │ 0.1%         │ 43m 50s
99.95%      │ 0.05%        │ 21m 55s
99.99%      │ 0.01%        │ 4m 23s
99.999%     │ 0.001%       │ 26s

Error Budget Consumption:
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Monthly Budget: 21m 55s (99.95% SLO)                            │
│                                                                  │
│  ████████████████░░░░░░░░░░░░░░░░  Used: 8m (36%)               │
│                                                                  │
│  Incidents:                                                      │
│  - Jan 5: Database failover - 5m                                 │
│  - Jan 12: Deployment rollback - 3m                              │
│                                                                  │
│  Remaining: 13m 55s (64%)                                        │
│                                                                  │
│  Status: ✓ HEALTHY                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## SLO Design Process

```text
SLO DESIGN WORKFLOW:

Step 1: IDENTIFY USER JOURNEYS
┌─────────────────────────────────────────────────────────────────┐
│ What do users care about?                                        │
│                                                                  │
│ Critical User Journeys (CUJs):                                   │
│ - Login and authentication                                       │
│ - Search and browse products                                     │
│ - Add to cart and checkout                                       │
│ - View order status                                              │
│                                                                  │
│ For each journey:                                                │
│ - What constitutes success?                                      │
│ - What latency is acceptable?                                    │
│ - What's the business impact of failure?                         │
└─────────────────────────────────────────────────────────────────┘

Step 2: DEFINE SLIs
┌─────────────────────────────────────────────────────────────────┐
│ What can we measure that represents user happiness?              │
│                                                                  │
│ For "Checkout" journey:                                          │
│ - Availability: checkout completes without error                 │
│ - Latency: checkout completes within 3 seconds                   │
│ - Correctness: order total matches cart                          │
│                                                                  │
│ SLI Specification:                                               │
│ - What events are we measuring?                                  │
│ - What's a "good" event vs "bad" event?                          │
│ - Where do we measure? (server, client, synthetic)               │
└─────────────────────────────────────────────────────────────────┘

Step 3: SET SLO TARGETS
┌─────────────────────────────────────────────────────────────────┐
│ What reliability level should we target?                         │
│                                                                  │
│ Consider:                                                        │
│ - Current baseline (what are we achieving now?)                  │
│ - User expectations (what do users tolerate?)                    │
│ - Business requirements (any SLAs?)                              │
│ - Cost vs reliability trade-off                                  │
│                                                                  │
│ Start achievable, improve iteratively                            │
│ SLO = Current baseline - small margin                            │
└─────────────────────────────────────────────────────────────────┘

Step 4: DEFINE ERROR BUDGET POLICY
┌─────────────────────────────────────────────────────────────────┐
│ What happens when budget is exhausted?                           │
│                                                                  │
│ Error Budget Policy:                                             │
│ - Budget > 50%: Normal operations                                │
│ - Budget 25-50%: Slow down risky changes                         │
│ - Budget < 25%: Focus on reliability                             │
│ - Budget = 0%: Feature freeze, reliability only                  │
│                                                                  │
│ Escalation:                                                      │
│ - Who gets notified at each threshold?                           │
│ - What actions are required?                                     │
└─────────────────────────────────────────────────────────────────┘
```

## SLO Document Template

```markdown
# SLO: {Service Name} - {Journey/Feature}

## Service Overview

| Attribute | Value |
|-----------|-------|
| Service | [Service name] |
| Owner | [Team name] |
| Criticality | [Critical/High/Medium/Low] |
| User Journey | [Journey name] |

## SLI Specification

### Availability SLI

**Definition:** The proportion of [event type] that [success criteria].

**Good Event:** [What counts as success]
**Bad Event:** [What counts as failure]

**Measurement:**
- Source: [Prometheus/Azure Monitor/etc.]
- Query:
  ```promql
  sum(rate(http_requests_total{status!~"5.."}[5m]))
  /
  sum(rate(http_requests_total[5m]))
  ```

### Latency SLI

**Definition:** The proportion of requests served within [threshold].

**Thresholds:**

| Percentile | Threshold |
|------------|-----------|
| P50 | [X]ms |
| P95 | [X]ms |
| P99 | [X]ms |

**Measurement:**

```promql
histogram_quantile(0.95,
  rate(http_request_duration_bucket[5m]))
```

## SLO Targets

| SLI | Target | Window |
|-----|--------|--------|
| Availability | [99.9%] | 30 days rolling |
| Latency (P95) | [99%] below 500ms | 30 days rolling |

## Error Budget

| SLO | Error Budget | Allowed Downtime (30d) |
|-----|--------------|------------------------|
| 99.9% availability | 0.1% | 43m 50s |
| 99% latency | 1% | 7h 18m |

## Error Budget Policy

### Budget Thresholds

| Budget Remaining | Status | Actions |
|------------------|--------|---------|
| > 50% | 🟢 Healthy | Normal operations |
| 25-50% | 🟡 Caution | Review recent changes |
| 10-25% | 🟠 Warning | Slow deployments, reliability focus |
| < 10% | 🔴 Critical | Feature freeze |
| Exhausted | ⛔ Frozen | Reliability-only work |

### Escalation

| Threshold | Notify | Action Required |
|-----------|--------|-----------------|
| < 50% | Team lead | Awareness |
| < 25% | Engineering manager | Review deployment pace |
| < 10% | Director | Feature freeze decision |
| Exhausted | VP Engineering | Incident response mode |

## Alerting

### SLO Burn Rate Alerts

| Severity | Burn Rate | Time Window | Example |
|----------|-----------|-------------|---------|
| Critical | 14.4x | 1h | Budget exhausted in ~2 days |
| Warning | 6x | 6h | Budget exhausted in ~5 days |
| Info | 1x | 3d | Budget on track to exhaust |

### Alert Configuration

```yaml
- alert: SLOHighBurnRate
  expr: |
    (
      sum(rate(http_requests_total{status=~"5.."}[1h]))
      /
      sum(rate(http_requests_total[1h]))
    ) > (14.4 * 0.001)  # 14.4x burn rate for 99.9% SLO
  for: 2m
  labels:
    severity: critical
  annotations:
    summary: "High error budget burn rate"
    description: "Error budget burning at 14.4x rate"
```

## Review Schedule

- **Weekly:** SLO dashboard review
- **Monthly:** Error budget retrospective
- **Quarterly:** SLO target review

## Appendix: Historical Performance

[Include baseline measurements and trends]

```text

```

## .NET SLO Implementation

```csharp
// SLO metric implementation in .NET
// Infrastructure/Telemetry/SloMetrics.cs

using System.Diagnostics.Metrics;

public class SloMetrics
{
    private readonly Counter<long> _totalRequests;
    private readonly Counter<long> _successfulRequests;
    private readonly Counter<long> _failedRequests;
    private readonly Histogram<double> _requestDuration;

    public SloMetrics(IMeterFactory meterFactory)
    {
        var meter = meterFactory.Create("OrdersApi.SLO");

        _totalRequests = meter.CreateCounter<long>(
            "slo.requests.total",
            "{request}",
            "Total requests for SLO calculation");

        _successfulRequests = meter.CreateCounter<long>(
            "slo.requests.successful",
            "{request}",
            "Successful requests (good events)");

        _failedRequests = meter.CreateCounter<long>(
            "slo.requests.failed",
            "{request}",
            "Failed requests (bad events)");

        _requestDuration = meter.CreateHistogram<double>(
            "slo.request.duration",
            "ms",
            "Request duration for latency SLI");
    }

    public void RecordRequest(
        string endpoint,
        int statusCode,
        double durationMs)
    {
        var tags = new TagList
        {
            { "endpoint", endpoint },
            { "status_code", statusCode.ToString() }
        };

        _totalRequests.Add(1, tags);

        // Availability SLI: 5xx = bad, everything else = good
        if (statusCode >= 500)
        {
            _failedRequests.Add(1, tags);
        }
        else
        {
            _successfulRequests.Add(1, tags);
        }

        // Latency SLI
        _requestDuration.Record(durationMs, tags);
    }
}

// Middleware to capture SLO metrics
public class SloMetricsMiddleware
{
    private readonly RequestDelegate _next;
    private readonly SloMetrics _sloMetrics;

    public SloMetricsMiddleware(RequestDelegate next, SloMetrics sloMetrics)
    {
        _next = next;
        _sloMetrics = sloMetrics;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var stopwatch = Stopwatch.StartNew();

        try
        {
            await _next(context);
        }
        finally
        {
            stopwatch.Stop();

            var endpoint = context.GetEndpoint()?.DisplayName ?? "unknown";
            var statusCode = context.Response.StatusCode;
            var durationMs = stopwatch.Elapsed.TotalMilliseconds;

            _sloMetrics.RecordRequest(endpoint, statusCode, durationMs);
        }
    }
}
```

## Error Budget Dashboard Queries

```promql
# Availability SLI (30-day rolling)
1 - (
  sum(increase(slo_requests_failed_total[30d]))
  /
  sum(increase(slo_requests_total[30d]))
)

# Latency SLI (P95 < 500ms, 30-day)
sum(increase(slo_request_duration_bucket{le="500"}[30d]))
/
sum(increase(slo_request_duration_count[30d]))

# Error Budget Remaining (availability)
1 - (
  (1 - 0.999)  # SLO target (99.9%)
  -
  (1 - (
    sum(increase(slo_requests_failed_total[30d]))
    /
    sum(increase(slo_requests_total[30d]))
  ))
) / (1 - 0.999)

# Error Budget Burn Rate (1h)
(
  sum(rate(slo_requests_failed_total[1h]))
  /
  sum(rate(slo_requests_total[1h]))
) / (1 - 0.999)  # Divide by error budget (0.1%)
```

## Workflow

When designing SLOs:

1. **Identify User Journeys**: What do users care about?
2. **Define SLIs**: What can we measure?
3. **Measure Baseline**: What are we achieving now?
4. **Set SLO Targets**: Achievable but aspirational
5. **Define Error Budget Policy**: What happens when budget is low?
6. **Implement Alerting**: Multi-window burn rate alerts
7. **Create Dashboards**: Visibility into SLO status
8. **Review Regularly**: Adjust based on learning

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
