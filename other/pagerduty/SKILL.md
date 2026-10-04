---
name: pagerduty
description: Query PagerDuty incidents, services, and on-call schedules
activation_keywords: [pagerduty, incident, alert, oncall, escalation, service]
execution_mode: server
---

# PagerDuty Skill

Provides read-only PagerDuty operations via REST API:
- List and search incidents
- Get incident details and alerts
- List services with escalation policies
- List on-call schedules and who is on-call
- List escalation policies

Use `builtin_pagerduty` tool with fields:
- `operation`: one of "list_incidents", "get_incident", "list_services", "list_schedules", "on_call", "list_escalation_policies"
- `incident_id`: incident ID (required for get_incident)
- `api_key`: PagerDuty API key (from PAGERDUTY_API_KEY env var if not provided)
- `status`: filter incidents by status (triggered, acknowledged, resolved)
- `service_id`: filter by service ID
- `per_page`: results per page (default: 20)

Note: All operations are read-only.
The API key is used only for this request and never logged.
