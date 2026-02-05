---
name: slo-alerting
description: "Define SLIs, SLOs, and implement burn-rate alerting"
triggers:
  - "SLO definition"
  - "SLI metrics"
  - "error budget"
  - "burn rate alerting"
priority: 2
---

# SLO Alerting

Define SLIs, set SLO targets, alert on burn rate (not raw error rate).

## Concepts

| Term | Definition | Example |
|------|------------|---------|
| **SLI** | Quantitative measure | % successful requests |
| **SLO** | Target for SLI | 99.9% success |
| **Error Budget** | Allowed failure | 0.1% = 43 min/month |
| **Burn Rate** | Budget consumption speed | 10x = exhausted in 3 days |

## Common SLIs

```
Availability: successful_requests / total_requests
Latency:      requests_under_threshold / total_requests
Error Rate:   error_requests / total_requests
```

## Burn Rate Alerting

Alert on how fast you're consuming budget, not raw error rate:

| Alert Level | Burn Rate | Time to Exhaust |
|-------------|-----------|-----------------|
| Page (critical) | 14.4x | 2 days |
| Page (warning) | 6x | 5 days |
| Ticket (medium) | 3x | 10 days |

## Multi-Window Strategy

Use long + short windows to balance speed and noise:

```yaml
# Critical: Fast burn (14.4x over 1h AND 5m)
- alert: HighBurnRate_Critical
  expr: (rate_1h / budget > 14.4) and (rate_5m / budget > 14.4)
  severity: critical

# Warning: Slower burn (6x over 6h AND 30m)
- alert: HighBurnRate_Warning
  expr: (rate_6h / budget > 6) and (rate_30m / budget > 6)
  severity: warning
```

## Dashboard Essentials

- Current burn rate
- Error budget remaining (%)
- Time until exhaustion at current rate

## Anti-Patterns

- **Too many SLOs** → SLO per user journey, not per endpoint
- **Alerting on raw error rate** → Noisy, doesn't account for budget
- **No budget visualization** → Teams don't understand burn rate

## References

- `references/methodology/sli-slo-framework.md`
