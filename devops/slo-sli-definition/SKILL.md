---
name: slo-sli-definition
description: "**SLO (Service Level Objective):** What we promise (99.9%)"
---

# SLO/SLI Definition (Verbose)

## Relationship Between SLO and SLI

**SLO (Service Level Objective):** What we promise (99.9%)
**SLI (Service Level Indicator):** How we measure (actual: 99.95%)

```
Business Promise (SLO)
        ↓
Measurable Target (SLI)
        ↓
Monitoring/Alerts
```

## Defining SLOs

### Availability SLO
```
Target: 99.9%
Meaning: Service available 99.9% of the time
Calculated: (successful_requests / total_requests)

Monthly budget:
100% - 99.9% = 0.1% = 0.001 × month
0.001 × 2,592,000 seconds = 2,592 seconds = 43 minutes
```

### Latency SLO
```
Target: p95 < 200ms
Meaning: 95% of requests complete in < 200ms
5% of requests may take longer

p50 (median): < 50ms (typical)
p95: < 200ms (slow users)
p99: < 500ms (worst 1%)
```

### Error Rate SLO
```
Target: < 0.1%
Meaning: 99.9% of requests succeed
< 0.1% may fail
```

## Measuring SLIs

```promql
# Availability SLI (monthly)
sum(rate(http_requests_total{status="200"}[30d])) /
sum(rate(http_requests_total[30d]))

# Example: 99.95% (exceeds 99.9% target) ✓

# Latency SLI
histogram_quantile(0.95, 
  rate(http_request_duration_seconds_bucket[1h])
)
# Example: 145ms (exceeds 200ms target) ✓

# Error Rate SLI
sum(rate(http_requests_total{status=~"5.."}[1h])) /
sum(rate(http_requests_total[1h]))
# Example: 0.05% (exceeds 0.1% target) ✓
```

## Error Budget Concept

```
"You have X minutes of downtime per month"

SLO 99.9% = 43 minutes/month
SLO 99.95% = 21 minutes/month
SLO 99.99% = 4 minutes/month

Usage example:
├─ 10 min: Deploys
├─ 15 min: Experiments/chaos testing
├─ 10 min: Cleanup/maintenance
├─ 8 min: Contingency
└─ 0 min: Done (fully spent)

When budget low (<25%):
- Stop deployments
- Postpone experiments
- Focus on stability
```

## SLO Selection by Industry

```
Internal Tools (99.0%):
- Users: Employees (can wait)
- Cost: Low SLA cost
- Acceptable downtime: 7.2 hours/month

SaaS Platform (99.9%):
- Users: Paying customers
- Cost: Significant infrastructure
- Acceptable downtime: 43 minutes/month

Financial Systems (99.99%):
- Users: Traders (money on line)
- Cost: Very high (redundancy, testing)
- Acceptable downtime: 4 minutes/month

Critical Infrastructure (99.999%):
- Users: Public (safety critical)
- Cost: Extreme (redundancy everywhere)
- Acceptable downtime: 26 seconds/month
```

## Common Mistakes

❌ SLO too loose → Team doesn't prioritize reliability  
✅ SLO achievable but challenging

❌ SLO too tight → Team burned out, can't innovate  
✅ SLO reflects actual business need

❌ No error budget → Team overly conservative  
✅ Use budget strategically for experiments

❌ SLO not measured → Theater, not real  
✅ Measure every day, review weekly
