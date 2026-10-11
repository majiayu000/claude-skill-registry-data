---
name: monitoring
description: Observability stack — Prometheus/Grafana, Datadog, metrics, alerting.
---

# Monitoring & Observability

## Core Principle

Instrument first → aggregate second → alert third. Never set up alerts before you know what to measure.

---

## Stack Selection

| Scenario | Recommended |
|----------|-------------|
| VPS / single server, cost-sensitive | Prometheus + Grafana (self-hosted via Docker) |
| AWS-native stack | CloudWatch (Metrics + Logs + Alarms) |
| GCP-native stack | Cloud Monitoring + Cloud Logging |
| Azure-native stack | Azure Monitor + Log Analytics |
| Multi-cloud or mixed stack | Datadog (SaaS) or Grafana Cloud |
| High log volume, self-hosted | Loki + Grafana (avoid ELK unless already invested) |

For full setup details, load the matching reference:

| Stack | Reference |
|-------|-----------|
| Prometheus + Grafana (+ Loki) | `references/prometheus-grafana.md` |
| AWS CloudWatch | `references/cloudwatch.md` |
| Datadog | `references/datadog.md` |

---

## Application Instrumentation Requirements

Confirm with the backend developer before setting up any monitoring stack:

| Language | Library |
|----------|---------|
| Node.js | `prom-client` |
| Python | `prometheus-client` |
| Go | `prometheus/client_golang` |
| Java | Micrometer |
| PHP | `promphp/prometheus_client_php` |

Minimum metrics every app must expose:
- HTTP request count (by method, path, status)
- HTTP request duration (histogram — P50/P95/P99)
- Active connections or queue depth
- Error count (by type)

---

## Before Declaring Done

- [ ] Application exposes `/metrics` with the minimum metrics above
- [ ] All critical services have a `ServiceDown` alert
- [ ] Error rate and latency alerts defined and routing to a notification channel
- [ ] Disk usage alert on every host > 80%
- [ ] Dashboard created: request rate, error rate, latency P95, CPU, memory
- [ ] Log aggregation collecting from all services
- [ ] Log retention policy set — never unlimited
- [ ] Runbook URL in alert annotations
- [ ] **If Prometheus**: AlertManager configured and test alert delivered to Slack/PagerDuty
- [ ] **If Loki**: label cardinality reviewed — no high-cardinality labels on streams
- [ ] **If Datadog**: Unified Service Tagging applied; APM traces visible for at least one critical flow
- [ ] **If CloudWatch**: retention policy on every log group; Log Insights tested with a sample query
