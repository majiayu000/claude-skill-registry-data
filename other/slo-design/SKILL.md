---
name: slo-design
description: >
  Design and implement SLIs, SLOs, and error budgets for production services.
  Covers SLI selection, SLO target-setting, error budget calculation, burn-rate
  alerting, and error budget policy. Use when asked about "SLO", "SLI", "error
  budget", "reliability targets", "burn rate", "uptime SLA", or when designing
  alerting for a production service. Do NOT use for: application-level
  performance optimization — use `web-performance` for frontend.
origin: yamtam-original
license: MIT © 2025 Vũ Văn Tâm
version: 1.0.0
compatibility: "Any backend service. Examples use Prometheus/Grafana notation."
---

<!-- Original skill — synthesized from Google SRE Book (CC BY 4.0), SLOconf 2024
     talks, and public SRE engineering practices. No third-party skill file copied. -->

## When to Use

- Use when: defining reliability targets for a new service
- Use when: on-call alerts are too noisy or miss real outages
- Use when: engineering team wants to make a data-driven ship/hold decision
- Use when: SLA negotiation requires underlying SLO/SLI data
- Do NOT use for: application-level profiling or performance optimization

---

## SLI / SLO / SLA Hierarchy

```
SLI  (what you measure)
  └── SLO  (the target you set internally)
        └── SLA  (the commitment you make externally, usually softer)
```

**SLI** — a specific metric that measures service behavior:
```
Good requests / Total requests × 100 = availability SLI
p99 latency measured at load balancer = latency SLI
```

**SLO** — a target range for an SLI, measured over a rolling window:
```
Availability SLO: 99.9% of requests succeed over 30 days
Latency SLO:      p99 < 500ms for 95% of 5-minute windows over 30 days
```

**SLA** — an external contract. Typically 0.5–1% below the SLO to allow buffer:
```
If SLO = 99.9%, then SLA = 99.5% (external commitment)
```

Never set SLA = SLO. SLAs trigger legal/financial consequences; leave buffer.

---

## SLI Selection by Service Type

| Service type | Primary SLI | Secondary SLI |
|---|---|---|
| Public API | Request success rate | p99 latency |
| Batch job | Completion rate | Job duration vs. deadline |
| Data pipeline | Freshness (age of latest record) | Error rate per batch |
| Storage | Durability (objects readable) | Write success rate |
| Stream processing | Throughput (messages/sec) | Consumer lag |

Rules:
- 1–3 SLIs per service. More = noise, harder to act on.
- Measure at the user-facing boundary — not deep inside the stack.
- Latency SLI: track p99, not average. Average hides tail pain.

---

## Error Budget

```
Error budget = 100% − SLO target

Example: SLO = 99.9% → Error budget = 0.1% over 30 days
         = 0.1% × 30 × 24 × 60 min = 43.2 minutes of downtime/month
```

### Error budget policy (run this on every sprint planning)

| Budget remaining | Policy |
|---|---|
| > 50% | Ship freely. Full velocity. |
| 25–50% | Review risky changes. Require reliability review for major releases. |
| < 25% | Feature freeze. Reliability work only. All new deploys need on-call sign-off. |
| 0% (exhausted) | Full freeze. Incident review required before any new release. |

This policy must be written down and agreed by engineering + product before incidents happen.

---

## Burn-Rate Alerting

Burn rate = how fast the error budget is being consumed relative to expected pace.

```
Burn rate 1x = consuming budget at exactly the SLO-allowed rate
Burn rate 2x = consuming 2× the allowed rate — budget halved in remaining window
```

### Recommended alert thresholds (Google SRE model)

| Alert | Burn rate | Look-back window | Severity |
|---|---|---|---|
| Page now | 14× | 1 hour | Critical — wake on-call |
| Page now | 6×  | 6 hours | Critical — wake on-call |
| Ticket | 3×  | 1 day  | Warning — fix in business hours |
| Ticket | 1×  | 3 days | Info — trending toward depletion |

### Prometheus example
```yaml
# Alert: 14× burn rate over 1 hour (page-level)
- alert: HighErrorBudgetBurnRate
  expr: |
    sum(rate(http_requests_total{job="api", status=~"5.."}[1h]))
    /
    sum(rate(http_requests_total{job="api"}[1h]))
    > (14 * 0.001)   # 14× burn on 99.9% SLO = 0.1% budget
  for: 2m
  labels:
    severity: critical
  annotations:
    summary: "Error budget burning at 14× — page on-call"
```

---

## SLO Dashboard — Minimum Requirements

Every service with an SLO must have a dashboard showing:
```
□ Current SLI value (30-day rolling window)
□ Error budget remaining (% + absolute time/requests)
□ Error budget burn rate (current 1h and 6h)
□ SLO target line on the SLI graph
□ Recent incidents and their budget impact
```

---

## Common Mistakes

| Mistake | Why it's wrong | Fix |
|---|---|---|
| SLO = 100% | Unachievable; no budget for deploys | Start at 99.5%, tighten over quarters |
| Measuring internal health checks | Doesn't reflect user experience | Measure at API gateway or CDN edge |
| Alerting on SLI directly | Alert fatigue; misses budget exhaustion | Alert on burn rate, not raw error rate |
| No error budget policy | Budget data exists but no action taken | Write and agree policy before first incident |
| SLA > SLO | Commits to more than you can deliver | SLA must always be ≤ SLO |

---

## Anti-Fake-Pass Rules

Before claiming an SLO is "designed", you MUST show:
- [ ] SLI defined: metric, measurement point, time window
- [ ] SLO target set with explicit reasoning (not arbitrary 99.9%)
- [ ] Error budget calculated in absolute units (minutes / requests)
- [ ] Burn-rate alerts configured at ≥ 2 thresholds (fast burn + slow burn)
- [ ] Error budget policy written and agreed (not just "we'll figure it out")

Reference: `gates/anti-fake-pass-gate.md`
