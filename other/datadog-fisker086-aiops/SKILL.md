---
name: datadog
description: Query Datadog monitors, dashboards, and metrics
activation_keywords: [datadog, monitor, dashboard, metric, apm, log, trace]
execution_mode: server
---

# Datadog Skill

Provides read-only Datadog operations via HTTP API:
- List and search monitors
- Get monitor details and status
- List dashboards
- Query metrics
- List incidents
- List SLOs

Use `builtin_datadog` tool with fields:
- `operation`: one of "list_monitors", "get_monitor", "list_dashboards", "query_metrics", "list_incidents", "list_slos"
- `monitor_id`: monitor ID (required for get_monitor)
- `dd_site`: Datadog site (default: "datadoghq.com", use "datadoghq.eu" for EU)
- `api_key`: Datadog API key (from DD_API_KEY env var if not provided)
- `app_key`: Datadog Application key (from DD_APP_KEY env var if not provided)
- `query`: metric query (required for query_metrics, e.g. "avg:system.cpu.user{*}by{host}")
- `per_page`: results per page (default: 20)

Note: All operations are read-only.
API keys are used only for this request and never logged.
