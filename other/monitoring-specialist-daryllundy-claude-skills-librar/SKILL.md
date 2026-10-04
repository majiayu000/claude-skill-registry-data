---
name: monitoring-specialist
description: Infrastructure-level monitoring configuration for metrics, dashboards,
  alerting, logging backends, and SLO/SLI policy. Use when asked to set up monitoring,
  create a Grafana dashboard, write Prometheus alerting rules, define SLOs, configure
  Alertmanager routing, set up centralized logging with Loki or Elasticsearch, configure
  tracing backends such as Jaeger or Tempo, or write an on-call runbook.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: infrastructure-platform
  tags:
  - monitoring
  - prometheus
  - grafana
  - alerting
  - slo
  - sli
  - elk
  - loki
  - tracing
  - observability
---

# Monitoring Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `set up monitoring`, `Grafana dashboard`, `Prometheus alert`.
- The requested work fits this skill's lane: monitoring setup, dashboard design, alert rules, SLO definition, logging backends, tracing backends, and runbooks.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: application instrumentation code and in-process metrics or tracing changes (use observability-specialist).

## First actions
1. `Glob('**/prometheus/**', '**/grafana/**', '**/alertmanager/**', '**/monitoring/**', '**/loki/**')` — find existing monitoring config
2. Read existing prometheus.yml and alert rules to understand current scrape targets and alert conventions
3. Identify monitoring stack: Prometheus+Grafana, ELK, Datadog, CloudWatch, or custom

## Decision rules
- Alert on symptoms (user-facing impact), not causes (disk space, CPU) — unless directly linked to user impact
- Every alert must have: `severity` label, `runbook_url` annotation, and `for:` duration to avoid flapping
- SLO alerts: use multi-window multi-burn-rate (1h + 6h for fast burn, 3d + 30d for slow burn)
- For new stacks: recommend Prometheus + Grafana + Loki + Tempo (open-source) unless a commercial tool is already in use

## Steps

### Step 1: Assess current monitoring coverage
Identify gaps in scrape targets, dashboards, alert coverage, logging backends, and tracing backends.

### Step 2: Design the monitoring stack
For each signal path: metrics collection, log storage and querying, tracing backend, alert routing, and SLO reporting.

### Step 3: Write configurations
Prometheus: scrape configs, recording rules, alert rules. Grafana: dashboard JSON with proper variables for multi-environment use. Alertmanager: routing tree with correct receiver grouping.

### Step 4: Validate
```bash
# Validate Prometheus config
promtool check config prometheus.yml
# Validate alert rules
promtool check rules alerts/*.yml
# Validate Grafana dashboard JSON (look for syntax errors)
python3 -m json.tool dashboard.json > /dev/null
```

## Output contract
- Prometheus alert rules: follow naming convention `[Service][Metric][Condition]` (e.g., `APIHighErrorRate`)
- Grafana dashboards: include `uid` field, template variables for `environment` and `service`, and thresholds on panels
- SLO definitions: include the SLI query, target percentage, error budget calculation, and burn rate alert thresholds
- Runbooks: include trigger condition, diagnostic steps, and resolution steps

## Constraints
- NEVER create alerts without a runbook or at minimum a diagnostic note in the annotation
- NEVER alert on CPU/memory alone - tie resource alerts to user-facing symptoms
- Scope boundary: adding metrics, spans, correlation IDs, or structured logging inside application source code belongs to observability-specialist

## Examples

### Example 1: Set up Prometheus alerting
User says: "Set up alerting for my API - I need to know when error rate is high or latency is bad"
Actions:
1. Glob for existing Prometheus config
2. Write alert rules: APIHighErrorRate (>5% 5xx for 5min), APIHighLatency (p99 >500ms for 5min)
3. Write Alertmanager routing to send critical to PagerDuty, warning to Slack
Result: alerts.yml + alertmanager.yml with runbook annotations

## Troubleshooting
**Alerts firing but Alertmanager not sending notifications**
Cause: Alertmanager routing misconfiguration or receiver auth failure
Fix: Check `amtool config routes` and test receiver with `amtool alert add`

**Grafana dashboard showing "No data"**
Cause: Datasource misconfigured, wrong label selectors, or metric doesn't exist
Fix: Test query directly in Prometheus UI; check label names with `{__name__=~"metric_name"}`

## Reference
- `references/legacy-agent.md`: Prometheus patterns, PromQL reference, Grafana dashboard patterns, SLO/SLI frameworks, ELK stack, Loki, distributed tracing, incident response
