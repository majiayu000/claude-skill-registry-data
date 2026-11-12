---
name: monitoring-conventions
description: Alert on symptoms, prevent alert fatigue, link runbooks, and separate health from readiness checks. Use when editing infrastructure code (CDK, Terraform, serverless config, CI workflows) or adding metrics and alerts.
license: MIT
compatibility: "Claude Code"
---

# Monitoring and alerting rules

- Alert on SYMPTOMS such as error rate above 1%, p99 above 2 seconds, or a growing queue; do not page on causes such as CPU above 80% or memory use. Causes belong on dashboards.
- Prevent alert fatigue. If an alert fires three times without action, tune its threshold or remove it. An ignored alert is worse than no alert.
- Every paging alert links to a runbook that says what to inspect, what to restart, and whom to escalate to. Do not add an alert without a runbook.
- Separate `/health` for process liveness and load balancers from `/ready` for dependency readiness and orchestration. A health check does not query the database.
- Add a new metric or alert in the same change as the feature it observes. Do not defer monitoring to an unspecified later task.
