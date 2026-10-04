---
name: grafana
description: "Build Grafana dashboards and variables, configure data sources and alerting, and provision dashboards as code."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["grafana", "dashboards", "alerting", "observability", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Grafana Dashboards & Alerts AI Skill Guide

## Overview & Engine Architecture

Grafana visualizes metrics, logs, and traces from pluggable data sources (Prometheus, Loki, Tempo, CloudWatch, etc.). Dashboards are graphs of panels with template variables; unified alerting evaluates rules and routes notifications. Agents design readable operational dashboards (RED/USE), keep variables consistent, and attach runbook links to alerts.

```
Data sources (Prometheus/Loki/...)
        -> Grafana
            |- Dashboards / folders
            |- Explore
            |- Unified alerting -> contact points
```

## When to use this skill

- Building service or infrastructure dashboards
- Wiring Prometheus/Loki datasources
- Migrating UI dashboards to provisioning JSON/YAML
- Creating alert rules that page humans

## Operational directives

1. One dashboard purpose per audience (oncall service view vs executive KPI).
2. Use template variables for `env`, `service`, `namespace` - do not hardcode.
3. Prefer rate/error/duration panels near the top for services.
4. Alerts need severity labels and runbook URLs.
5. Provision dashboards as code for critical views so they are reviewable.

## Panel query example (Prometheus)

```promql
sum(rate(http_requests_total{service="$service",env="$env"}[5m])) by (status)
```

## Dashboard variables

| Variable | Type | Example |
| --- | --- | --- |
| `env` | custom/datasource | `dev`, `prod` |
| `service` | query label_values | `label_values(http_requests_total, service)` |
| `namespace` | query | Kubernetes namespace |

## Alerting sketch

- Condition: error ratio > 5% for 10 minutes
- Labels: `severity=page`, `service=api`
- Annotation: summary + `runbook_url`
- Contact point: PagerDuty/Slack with severity routing

## Best practices

- Keep units explicit (seconds, bytes, percent).
- Avoid dozens of high-cardinality legend series on one panel.
- Use repeat panels sparingly; they can explode load.
- Version-control provisioning under `grafana/dashboards/`.

## Limitations

- Auth (SSO/LDAP) and org/team permissions are deployment-specific.
- Some plugins are enterprise-licensed.
- Explore is for ad-hoc debug; durable knowledge belongs in dashboards/runbooks.

## Related skills

- `@prometheus` - metrics backend and alert expressions
- `@opentelemetry` - producing telemetry
- `@kubernetes` - container platform context for kube dashboards
