---
name: create-observability-config
description: Setup observability platform configuration (Datadog, Prometheus, Splunk) with REQ-* dashboards and alerts. Creates monitors for each requirement with SLA tracking. Use when deploying to production or setting up monitoring.
allowed-tools: [Read, Write, Edit]
---

# create-observability-config

**Skill Type**: Actuator (Runtime Setup)
**Purpose**: Setup observability with REQ-* dashboards and alerts
**Prerequisites**: Code deployed or ready to deploy, telemetry tagged

---

## Agent Instructions

You are setting up **observability** with **requirement-level monitoring**.

**Create**:
1. Dashboards per REQ-* (success rate, latency, errors)
2. Alerts for SLA violations
3. Log aggregation with REQ-* filtering
4. Trace visualization with REQ-* tags

---

## Platform Configurations

### Datadog Configuration

**Dashboard per Requirement**:

```yaml
# datadog/dashboards/req-f-auth-001.json

{
  "title": "<REQ-ID>: User Login Monitoring",
  "description": "Real-time monitoring for user login functionality",
  "widgets": [
    {
      "title": "Login Success Rate",
      "definition": {
        "type": "timeseries",
        "requests": [{
          "q": "sum:auth.login.attempts{req:<REQ-ID>,success:true}.as_count() / sum:auth.login.attempts{req:<REQ-ID>}.as_count()"
        }]
      }
    },
    {
      "title": "Login Latency (p95)",
      "definition": {
        "type": "timeseries",
        "requests": [{
          "q": "p95:auth.login.duration{req:<REQ-ID>}"
        }],
        "markers": [{
          "value": 500,  // REQ-NFR-PERF-001 threshold
          "display_type": "error dashed"
        }]
      }
    },
    {
      "title": "Failed Login Reasons",
      "definition": {
        "type": "toplist",
        "requests": [{
          "q": "top(auth.login.failures{req:<REQ-ID>} by {error}, 10, 'sum', 'desc')"
        }]
      }
    }
  ]
}
```

**Alerts**:

```yaml
# datadog/monitors/req-f-auth-001-latency.json

{
  "name": "<REQ-ID>: Login latency exceeded",
  "type": "metric alert",
  "query": "avg(last_5m):p95:auth.login.duration{req:<REQ-ID>} > 500",
  "message": "Login latency exceeded 500ms threshold (REQ-NFR-PERF-001)\n\nRequirement: <REQ-ID> (User Login)\nSLA: < 500ms\nCurrent: {{value}}ms\n\n@slack-alerts",
  "tags": ["req:<REQ-ID>", "sla:performance"],
  "options": {
    "thresholds": {
      "critical": 500,
      "warning": 400
    },
    "notify_no_data": true,
    "no_data_timeframe": 10
  }
}
```

---

### Prometheus Configuration

**Recording Rules**:

```yaml
# prometheus/rules/req-f-auth-001.yml

groups:
  - name: req_f_auth_001
    interval: 30s
    rules:
      # Success rate
      - record: req:auth_login_success_rate
        expr: |
          sum(rate(auth_login_attempts_total{req="<REQ-ID>",success="true"}[5m]))
          /
          sum(rate(auth_login_attempts_total{req="<REQ-ID>"}[5m]))
        labels:
          req: "<REQ-ID>"

      # Latency p95
      - record: req:auth_login_duration_p95
        expr: histogram_quantile(0.95, rate(auth_login_duration_seconds_bucket{req="<REQ-ID>"}[5m]))
        labels:
          req: "<REQ-ID>"
```

**Alerts**:

```yaml
# prometheus/alerts/req-f-auth-001.yml

groups:
  - name: req_f_auth_001_alerts
    rules:
      - alert: REQ_F_AUTH_001_LatencyHigh
        expr: req:auth_login_duration_p95{req="<REQ-ID>"} > 0.5
        for: 5m
        labels:
          severity: critical
          req: <REQ-ID>
          sla: performance
        annotations:
          summary: "Login latency exceeded (<REQ-ID>)"
          description: "p95 latency is {{ $value }}s (threshold: 0.5s)"
          requirement: "REQ-NFR-PERF-001: Login response < 500ms"
          runbook: "docs/runbooks/performance-degradation.md"
```

---

### Splunk Configuration

**Log Search**:

```
# Splunk saved search for <REQ-ID>

index=production sourcetype=app_logs req="<REQ-ID>"
| stats count by success, error
| eval success_rate = round(count(eval(success="true")) / count() * 100, 2)
```

**Dashboard**:

```xml
<dashboard>
  <label><REQ-ID>: User Login</label>
  <row>
    <panel>
      <title>Login Success Rate</title>
      <single>
        <search>
          <query>
            index=production req="<REQ-ID>"
            | stats count by success
            | eval rate = round(count(eval(success="true")) / count() * 100, 2)
          </query>
        </search>
      </single>
    </panel>
  </row>
</dashboard>
```

---

## Output Format

```
[TELEMETRY TAGGING - <REQ-ID>]

Platform: Datadog

Configuration Created:

Dashboards (1):
  ✓ datadog/dashboards/req-f-auth-001.json
    - Login success rate widget
    - Login latency (p95) widget with 500ms threshold
    - Failed login reasons widget
    - Active users widget

Monitors/Alerts (3):
  ✓ datadog/monitors/req-f-auth-001-latency.json
    - Alert: p95 latency > 500ms (REQ-NFR-PERF-001)
    - Warning: > 400ms
    - Critical: > 500ms

  ✓ datadog/monitors/req-f-auth-001-errors.json
    - Alert: Error rate > 5%
    - Links to: <REQ-ID>

  ✓ datadog/monitors/req-f-auth-001-lockouts.json
    - Alert: Lockout rate > 10%
    - Links to: BR-003

Logs:
  ✓ All log statements tagged with req="<REQ-ID>"
  ✓ Searchable: logs.req:<REQ-ID>

Metrics:
  ✓ auth.login.attempts{req:<REQ-ID>}
  ✓ auth.login.duration{req:<REQ-ID>}
  ✓ auth.login.lockouts{req:<REQ-ID>}

Traces:
  ✓ Span "auth.login" tagged with req="<REQ-ID>"

Backward Traceability Enabled:
  Alert → req:<REQ-ID> → docs/requirements/auth.md → INT-100 ✅

✅ Observability Setup Complete!
```

---

## Notes

**Why observability per requirement?**
- **Requirement-level SLAs**: Monitor each REQ-* separately
- **Impact analysis**: Know which requirements are problematic
- **Feedback loop**: Alerts trace back to original intent
- **Business visibility**: Dashboards show feature health

**Homeostasis Goal**:
```yaml
desired_state:
  all_requirements_monitored: true
  alerts_tagged_with_req: true
  dashboards_per_requirement: true
```

**"Excellence or nothing"** 🔥
