---
name: grafana-reader
description: Read Grafana dashboards, panels, and alerts
activation_keywords: [grafana, dashboard, panel, alert, visualization, monitoring]
execution_mode: server
---

# Grafana Reader Skill

Provides read-only Grafana operations:
- List available dashboards
- Get dashboard details and panels
- Query panel data
- List alert rules and their status

Use `builtin_grafana_reader` tool with fields:
- `operation`: one of "dashboards", "dashboard", "panels", "alerts"
- `grafana_url`: Grafana server URL (optional, default: http://localhost:3000)
- `dashboard_uid`: Dashboard UID (required for dashboard/panels operations)
- `api_key`: Grafana API key (optional)

Note: All operations are read-only.
