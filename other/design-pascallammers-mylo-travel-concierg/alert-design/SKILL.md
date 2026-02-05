---
name: alert-design
description: Design actionable alerts with appropriate severity and noise reduction
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Alert Design Skill

## When to Use This Skill

Use this skill when:

- **Alert Design tasks** - Working on design actionable alerts with appropriate severity and noise reduction
- **Planning or design** - Need guidance on Alert Design approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Design effective, actionable alerts that minimize noise and maximize signal.

## MANDATORY: Documentation-First Approach

Before designing alerts:

1. **Invoke `docs-management` skill** for alerting patterns
2. **Verify alerting best practices** via MCP servers (perplexity)
3. **Base guidance on SRE and on-call best practices**

## Alert Design Principles

```text
ALERT PRINCIPLES:

┌─────────────────────────────────────────────────────────────────┐
│                    GOOD ALERTS ARE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ACTIONABLE                                                      │
│  ├── Clear remediation steps exist                               │
│  ├── Responder knows what to do                                  │
│  └── Not just "something is wrong"                               │
│                                                                  │
│  RELEVANT                                                        │
│  ├── Tied to user impact or SLO                                  │
│  ├── Not monitoring internal metrics only                        │
│  └── Business-meaningful                                         │
│                                                                  │
│  TIMELY                                                          │
│  ├── Right urgency level                                         │
│  ├── Not too early (premature)                                   │
│  └── Not too late (missed opportunity)                           │
│                                                                  │
│  UNIQUE                                                          │
│  ├── No duplicate alerts for same issue                          │
│  ├── Aggregated where appropriate                                │
│  └── Clear ownership                                             │
│                                                                  │
│  DIAGNOSED                                                       │
│  ├── Include context and links                                   │
│  ├── Recent changes, related metrics                             │
│  └── Runbook reference                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    BAD ALERTS ARE                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✗ NOISY          → Too many, get ignored                        │
│  ✗ VAGUE          → "Something is wrong" with no detail          │
│  ✗ UNACTIONABLE   → No clear next step                           │
│  ✗ STALE          → Outdated thresholds                          │
│  ✗ DUPLICATED     → Same issue, many alerts                      │
│  ✗ FALSE POSITIVE → Fires when nothing is wrong                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Alert Severity Levels

```text
SEVERITY CLASSIFICATION:

┌─────────┬────────────────┬─────────────────────────────────────┐
│ Level   │ Response Time  │ Criteria                            │
├─────────┼────────────────┼─────────────────────────────────────┤
│ P1/SEV1 │ Immediate      │ - Revenue/users affected NOW        │
│ CRITICAL│ Page on-call   │ - Data loss risk                    │
│         │ < 5 min        │ - Security breach                   │
│         │                │ - SLO at risk of breach             │
├─────────┼────────────────┼─────────────────────────────────────┤
│ P2/SEV2 │ Within 1 hour  │ - Degraded experience               │
│ HIGH    │ Page if OOH    │ - Partial functionality loss        │
│         │                │ - High error rate                   │
│         │                │ - Error budget burning fast         │
├─────────┼────────────────┼─────────────────────────────────────┤
│ P3/SEV3 │ Business hours │ - Minor degradation                 │
│ MEDIUM  │ Next day OK    │ - Non-critical component            │
│         │                │ - Warning thresholds                │
│         │                │ - Capacity concerns                 │
├─────────┼────────────────┼─────────────────────────────────────┤
│ P4/SEV4 │ Best effort    │ - Informational                     │
│ LOW/INFO│ Track in ticket│ - Anomalies to investigate          │
│         │                │ - Optimization opportunities        │
└─────────┴────────────────┴─────────────────────────────────────┘

ROUTING BY SEVERITY:
┌─────────┬─────────────────────────────────────────────────────┐
│ Level   │ Notification Channels                                │
├─────────┼─────────────────────────────────────────────────────┤
│ P1      │ PagerDuty (page), Slack #incidents, Phone call      │
│ P2      │ PagerDuty (high), Slack #alerts, Email              │
│ P3      │ Slack #alerts, Email, Ticket auto-created           │
│ P4      │ Slack #monitoring, Dashboard only                   │
└─────────┴─────────────────────────────────────────────────────┘
```

## Alert Structure

```text
ALERT ANATOMY:

┌─────────────────────────────────────────────────────────────────┐
│ ALERT: OrdersApi High Error Rate                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ SEVERITY: P2/High                                                │
│ SERVICE: orders-api                                              │
│ ENVIRONMENT: production                                          │
│                                                                  │
│ SUMMARY:                                                         │
│ Error rate is 5.2% (threshold: 1%). Affecting checkout flow.     │
│                                                                  │
│ IMPACT:                                                          │
│ ~500 users/minute seeing checkout failures.                      │
│ Revenue impact: ~$2,000/minute at risk.                          │
│                                                                  │
│ DETAILS:                                                         │
│ - Current error rate: 5.2%                                       │
│ - Normal rate: 0.3%                                              │
│ - Started: 14:32 UTC (12 minutes ago)                            │
│ - Error type: 503 Service Unavailable                            │
│                                                                  │
│ POSSIBLE CAUSES:                                                 │
│ - Recent deployment (14:28 UTC - payment-service v2.3.1)         │
│ - Database connection pool exhaustion                            │
│ - Downstream dependency failure                                  │
│                                                                  │
│ QUICK ACTIONS:                                                   │
│ 1. Check recent deployments: [Deploy Dashboard]                  │
│ 2. Check dependencies: [Dependency Status]                       │
│ 3. View error logs: [Kibana Query]                               │
│                                                                  │
│ RUNBOOK: https://wiki.example.com/runbooks/orders-high-error     │
│                                                                  │
│ RELATED:                                                         │
│ - Grafana Dashboard: [Link]                                      │
│ - Service Map: [Link]                                            │
│ - Recent Incidents: [Link]                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Alert Types

```text
ALERT CATEGORIES:

SYMPTOM-BASED (Preferred):
┌─────────────────────────────────────────────────────────────────┐
│ Alert on what users experience, not internal metrics            │
│                                                                  │
│ ✓ "Error rate > 1% for 5 minutes"                                │
│ ✓ "P95 latency > 2s for 10 minutes"                              │
│ ✓ "Availability < 99.9% (SLO breach risk)"                       │
│ ✓ "Order completion rate dropped 20%"                            │
│                                                                  │
│ ✗ "CPU > 80%" (cause, not symptom)                               │
│ ✗ "Memory > 90%" (cause, not symptom)                            │
│ ✗ "Pod restarts" (might not affect users)                        │
└─────────────────────────────────────────────────────────────────┘

CAUSE-BASED (Supporting):
┌─────────────────────────────────────────────────────────────────┐
│ Use for capacity planning and early warning                     │
│                                                                  │
│ ✓ "Disk 80% full" (warning, lower severity)                      │
│ ✓ "Certificate expires in 7 days"                                │
│ ✓ "Connection pool 90% utilized"                                 │
│                                                                  │
│ These should be WARNING/INFO, not PAGE-worthy                    │
└─────────────────────────────────────────────────────────────────┘

SLO-BASED (Burn Rate):
┌─────────────────────────────────────────────────────────────────┐
│ Alert when error budget is burning too fast                     │
│                                                                  │
│ Multi-window burn rate alerts:                                   │
│                                                                  │
│ Critical: 14.4x burn rate over 1h AND 6x over 5m                │
│ → Budget exhausted in ~2 days if continues                       │
│                                                                  │
│ Warning: 6x burn rate over 6h AND 3x over 30m                   │
│ → Budget exhausted in ~5 days if continues                       │
│                                                                  │
│ Info: 1x burn rate over 3d                                       │
│ → On track to exhaust budget                                     │
└─────────────────────────────────────────────────────────────────┘
```

## Alert Configuration Examples

```yaml
# Prometheus Alertmanager rules
# alerting-rules.yaml

groups:
  - name: orders-api-slo
    rules:
      # SLO Burn Rate - Critical
      - alert: OrdersApiHighErrorBudgetBurn
        expr: |
          (
            sum(rate(http_requests_total{service="orders-api",status=~"5.."}[1h]))
            /
            sum(rate(http_requests_total{service="orders-api"}[1h]))
          ) > (14.4 * 0.001)
          and
          (
            sum(rate(http_requests_total{service="orders-api",status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total{service="orders-api"}[5m]))
          ) > (6 * 0.001)
        for: 2m
        labels:
          severity: critical
          service: orders-api
          slo: availability
        annotations:
          summary: "OrdersApi error budget burning rapidly"
          description: |
            Error budget is burning at 14.4x rate.
            If this continues, budget will be exhausted in ~2 days.
            Current error rate: {{ $value | humanizePercentage }}
          runbook_url: "https://wiki.example.com/runbooks/slo-burn-rate"
          dashboard_url: "https://grafana.example.com/d/orders-slo"

      # Latency SLO
      - alert: OrdersApiHighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket{service="orders-api"}[5m]))
            by (le)
          ) > 2
        for: 5m
        labels:
          severity: high
          service: orders-api
          slo: latency
        annotations:
          summary: "OrdersApi P95 latency exceeds 2s"
          description: |
            P95 latency is {{ $value | humanizeDuration }}.
            Threshold: 2 seconds.
            This affects user experience for 5% of requests.
          runbook_url: "https://wiki.example.com/runbooks/high-latency"

  - name: orders-api-capacity
    rules:
      # Capacity warning (lower severity)
      - alert: OrdersApiHighCPU
        expr: |
          avg(rate(container_cpu_usage_seconds_total{container="orders-api"}[5m]))
          by (pod) > 0.8
        for: 15m
        labels:
          severity: warning
          service: orders-api
          category: capacity
        annotations:
          summary: "OrdersApi CPU usage high"
          description: |
            CPU usage is {{ $value | humanizePercentage }} for 15+ minutes.
            Consider scaling or optimization.
          runbook_url: "https://wiki.example.com/runbooks/capacity-cpu"

      # Disk space warning
      - alert: OrdersApiDiskSpaceLow
        expr: |
          (node_filesystem_avail_bytes{mountpoint="/data"}
          /
          node_filesystem_size_bytes{mountpoint="/data"}) < 0.2
        for: 5m
        labels:
          severity: warning
          category: capacity
        annotations:
          summary: "Disk space below 20%"
          description: "{{ $value | humanizePercentage }} disk space remaining"
```

## Noise Reduction Strategies

```text
NOISE REDUCTION TECHNIQUES:

1. APPROPRIATE THRESHOLDS
   ┌────────────────────────────────────────────────────────────┐
   │ Don't alert on every anomaly                               │
   │                                                            │
   │ Bad:  CPU > 70% for 1 minute                               │
   │ Good: CPU > 90% for 15 minutes                             │
   │                                                            │
   │ Bad:  Any 5xx error                                        │
   │ Good: Error rate > 1% for 5 minutes                        │
   └────────────────────────────────────────────────────────────┘

2. PROPER FOR DURATION
   ┌────────────────────────────────────────────────────────────┐
   │ Wait long enough to confirm it's real                      │
   │                                                            │
   │ Transient spike: for: 0m    → Too noisy                    │
   │ Brief issue:     for: 2m    → May still be transient       │
   │ Confirmed issue: for: 5m    → Likely real                  │
   │ Capacity issue:  for: 15m   → Sustained trend              │
   └────────────────────────────────────────────────────────────┘

3. ALERT AGGREGATION
   ┌────────────────────────────────────────────────────────────┐
   │ Group related alerts into one notification                 │
   │                                                            │
   │ Instead of:                                                │
   │ - Pod A unhealthy                                          │
   │ - Pod B unhealthy                                          │
   │ - Pod C unhealthy                                          │
   │                                                            │
   │ Send:                                                      │
   │ - 3 pods unhealthy in orders-api deployment                │
   └────────────────────────────────────────────────────────────┘

4. INHIBITION RULES
   ┌────────────────────────────────────────────────────────────┐
   │ Suppress child alerts when parent fires                    │
   │                                                            │
   │ If "Database down" fires:                                  │
   │   Suppress all "DB connection error" alerts                │
   │                                                            │
   │ If "Kubernetes node down" fires:                           │
   │   Suppress all pod alerts on that node                     │
   └────────────────────────────────────────────────────────────┘

5. MAINTENANCE WINDOWS
   ┌────────────────────────────────────────────────────────────┐
   │ Silence alerts during planned maintenance                  │
   │                                                            │
   │ Schedule silences before:                                  │
   │ - Deployments                                              │
   │ - Database migrations                                      │
   │ - Infrastructure changes                                   │
   └────────────────────────────────────────────────────────────┘
```

## Alert Template

```markdown
# Alert Specification: {Alert Name}

## Overview

| Attribute | Value |
|-----------|-------|
| Alert Name | [Name] |
| Service | [Service name] |
| Severity | [P1/P2/P3/P4] |
| Category | [SLO/Capacity/Security/Business] |
| Owner | [Team] |

## Condition

**Expression:**
```promql
[PromQL or query expression]
```

**Threshold:** [Value]
**Duration (for):** [Duration]

## Meaning

**What it means:**
[Explain what this alert indicates]

**User impact:**
[How users are affected]

**Business impact:**
[Revenue, reputation, compliance implications]

## Triage Steps

1. **Verify the alert**
   - Check [dashboard link]
   - Confirm [metric] is actually [condition]

2. **Assess impact**
   - How many users affected?
   - Which user journeys impacted?

3. **Identify cause**
   - Check recent deployments
   - Check dependencies
   - Review error logs

## Remediation

**Immediate actions:**

1. [First action]
2. [Second action]
3. [Third action]

**Escalation:**

- If not resolved in [X] minutes, escalate to [team/person]

## Runbook

Link: [Runbook URL]

## Alert Configuration

```yaml
- alert: {AlertName}
  expr: |
    [expression]
  for: [duration]
  labels:
    severity: [severity]
    service: [service]
  annotations:
    summary: "[Summary]"
    description: "[Description]"
    runbook_url: "[URL]"
```

## Review History

| Date | Change | Reason |
|------|--------|--------|
| [Date] | [Change] | [Why] |

```text

```

## Workflow

When designing alerts:

1. **Start with SLOs**: Alert on SLO burn rate first
2. **Focus on Symptoms**: Alert on user impact, not internal metrics
3. **Set Appropriate Severity**: Not everything is P1
4. **Include Context**: Dashboards, runbooks, recent changes
5. **Define Escalation**: Who gets notified, when to escalate
6. **Reduce Noise**: Proper thresholds, aggregation, inhibition
7. **Review Regularly**: Tune based on false positives/negatives

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
