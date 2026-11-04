---
name: grafana
description: Investigate production issues, query logs and metrics, and explore dashboards on the Mattermost Grafana instance at grafana.internal.mattermost.com.
allowed-tools: mcp__grafana__list_datasources, mcp__grafana__search_dashboards, mcp__grafana__get_dashboard_by_uid, mcp__grafana__get_dashboard_summary, mcp__grafana__get_dashboard_panel_queries, mcp__grafana__query_prometheus, mcp__grafana__list_prometheus_metric_names, mcp__grafana__list_prometheus_metric_metadata, mcp__grafana__list_prometheus_label_names, mcp__grafana__list_prometheus_label_values, mcp__grafana__query_loki_logs, mcp__grafana__list_loki_label_names, mcp__grafana__list_loki_label_values, mcp__grafana__query_loki_stats, mcp__grafana__query_loki_patterns, mcp__grafana__get_annotations, mcp__grafana__list_oncall_schedules, mcp__grafana__get_current_oncall_users, mcp__grafana__list_alert_groups, mcp__grafana__generate_deeplink
---

## Grafana Investigation Skill

You are investigating production issues on the Mattermost Grafana instance.

### Environment

- **Grafana URL**: https://grafana.internal.mattermost.com
- **Loki data source**: `Loki Production`
- **Prometheus data source**: `Prometheus Prod`

### Namespace identifiers

| Product     | Namespace UID                    |
|-------------|----------------------------------|
| Community   | `rxocmq9isjfm3dgyf4ujgnfz3c`     |
| Hub         | `c4ja3w3h8tgwiy5c5dbmhmkpje`     |

These namespace UIDs appear as the `namespace` label in both Loki and Prometheus. Always filter by namespace when the user's question is scoped to a specific product.

### Data source UIDs (pre-cached — do not call `list_datasources`)

| Data source       | UID                   |
|-------------------|-----------------------|
| Loki Production   | `P4F55509B51A00EB7`   |
| Prometheus Prod   | `P27C405C01959D762`   |

Use these directly. Only call `list_datasources` if a query fails with an unknown UID error.

### Querying logs (Loki)

Use `query_loki_logs` with:
- `datasourceUid`: the UID for `Loki Production`
- `query`: a LogQL expression, e.g. `{namespace="rxocmq9isjfm3dgyf4ujgnfz3c"} |= "error"`
- `timeRange`: `{from: "now-1h", to: "now"}` unless the user specifies otherwise
- `limit`: 100 (default); increase if needed

When exploring unknown log structure, first call `list_loki_label_names` and `list_loki_label_values` to understand available labels.

For volume/rate queries, prefer `query_loki_stats` over fetching raw lines.

### Querying metrics (Prometheus)

Use `query_prometheus` with:
- `datasourceUid`: the UID for `Prometheus Prod`
- `query`: a PromQL expression
- Omit `time` for current value; provide it for historical point-in-time

When discovering metrics, use `list_prometheus_metric_names` and `list_prometheus_label_names`. Use `list_prometheus_metric_metadata` to understand a metric's type and help text before writing PromQL.

### Finding dashboards

Use `search_dashboards` with a descriptive query. Then use `get_dashboard_summary` to understand panel layout before fetching the full JSON with `get_dashboard_by_uid`. Use `get_dashboard_panel_queries` to see what PromQL/LogQL a panel runs.

### Generating links

Use `generate_deeplink` to produce a Grafana Explore or dashboard URL to share with the user. Always include the relevant time range.

### Workflow

1. **Clarify scope**: determine which product (Community, Hub, or both) and time range.
2. **Use pre-cached datasource UIDs** from the table above — do not call `list_datasources`.
3. **Find relevant dashboards** with `search_dashboards`.
4. **Query logs and metrics** as needed to answer the question.
5. **Synthesise findings**: summarise what you found, including error rates, patterns, and relevant log lines.
6. **Provide a deeplink** to the most relevant dashboard or Explore query so the user can drill in further.

Always prefer targeted queries over broad ones — filter by namespace and narrow time ranges first, then widen if needed.
