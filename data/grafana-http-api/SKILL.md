---
name: grafana-http-api
description: Comprehensive skill for interacting with Grafana's HTTP API to manage dashboards, data sources, folders, alerting, annotations, users, teams, and organizations. Use when Claude needs to (1) Create, read, update, or delete Grafana dashboards, (2) Manage data sources and connections, (3) Configure alerting rules, contact points, and notification policies, (4) Work with folders and permissions, (5) Manage users, teams, and service accounts, (6) Create or query annotations, (7) Execute queries against data sources, or any other Grafana automation task via API.
---

# Grafana HTTP API Skill

Programmatically manage Grafana resources including dashboards, data sources, alerting, folders, annotations, users, teams, and organizations.

## Authentication

### Service Account Token (Recommended)

```bash
curl -H "Authorization: Bearer <SERVICE_ACCOUNT_TOKEN>" \
     -H "Content-Type: application/json" \
     https://your-grafana.com/api/dashboards/home
```

### Basic Auth

```bash
curl -u admin:admin https://your-grafana.com/api/org
```

### Multi-Organization Header

Use `X-Grafana-Org-Id` header to specify target organization:

```bash
curl -H "Authorization: Bearer <TOKEN>" \
     -H "X-Grafana-Org-Id: 2" \
     https://your-grafana.com/api/org
```

## Quick Reference

### Dashboards

**Search dashboards:**

```bash
GET /api/search?type=dash-db&query=<search_term>&tag=<tag>&folderIds=<folder_id>
```

**Get dashboard by UID:**

```bash
GET /api/dashboards/uid/<dashboard_uid>
```

**Create/Update dashboard:**

```bash
POST /api/dashboards/db
{
  "dashboard": {
    "id": null,
    "uid": null,
    "title": "Production Overview",
    "tags": ["templated"],
    "timezone": "browser",
    "schemaVersion": 16,
    "refresh": "25s"
  },
  "folderUid": "l3KqBxCMz",
  "message": "Made changes to xyz",
  "overwrite": false
}
```

**Delete dashboard:**

```bash
DELETE /api/dashboards/uid/<dashboard_uid>
```

### Data Sources

**List all data sources:**

```bash
GET /api/datasources
```

**Get data source by UID:**

```bash
GET /api/datasources/uid/<datasource_uid>
```

**Create data source:**

```bash
POST /api/datasources
{
  "name": "Prometheus",
  "type": "prometheus",
  "url": "http://prometheus:9090",
  "access": "proxy",
  "basicAuth": false,
  "isDefault": true
}
```

**Query data source:**

```bash
POST /api/ds/query
{
  "queries": [
    {
      "refId": "A",
      "datasource": { "uid": "<datasource_uid>" },
      "expr": "up",
      "intervalMs": 1000,
      "maxDataPoints": 43200
    }
  ],
  "from": "now-1h",
  "to": "now"
}
```

**Health check:**

```bash
GET /api/datasources/uid/<datasource_uid>/health
```

### Folders

**List folders:**

```bash
GET /api/folders
```

**Create folder:**

```bash
POST /api/folders
{
  "title": "My Folder",
  "uid": "my-folder-uid"
}
```

**Get folder:**

```bash
GET /api/folders/<folder_uid>
```

**Update folder:**

```bash
PUT /api/folders/<folder_uid>
{
  "title": "Updated Folder Title",
  "version": 1
}
```

**Delete folder:**

```bash
DELETE /api/folders/<folder_uid>?forceDeleteRules=true
```

### Alerting

**List all alert rules:**

```bash
GET /api/v1/provisioning/alert-rules
```

**Get alert rule:**

```bash
GET /api/v1/provisioning/alert-rules/<rule_uid>
```

**Create alert rule:**

```bash
POST /api/v1/provisioning/alert-rules
{
  "title": "High CPU Alert",
  "ruleGroup": "CPU Alerts",
  "folderUID": "<folder_uid>",
  "noDataState": "OK",
  "execErrState": "OK",
  "for": "5m",
  "condition": "B",
  "annotations": { "summary": "CPU usage is high" },
  "labels": { "severity": "warning" },
  "data": [
    {
      "refId": "A",
      "relativeTimeRange": { "from": 600, "to": 0 },
      "datasourceUid": "<datasource_uid>",
      "model": {
        "expr": "100 - (avg(rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
        "refId": "A"
      }
    },
    {
      "refId": "B",
      "relativeTimeRange": { "from": 0, "to": 0 },
      "datasourceUid": "-100",
      "model": {
        "type": "classic_conditions",
        "refId": "B",
        "conditions": [{
          "evaluator": { "type": "gt", "params": [80] },
          "operator": { "type": "and" },
          "query": { "params": ["A"] },
          "reducer": { "type": "avg" }
        }]
      }
    }
  ]
}
```

**List contact points:**

```bash
GET /api/v1/provisioning/contact-points
```

**List notification policies:**

```bash
GET /api/v1/provisioning/policies
```

**Get active alerts:**

```bash
GET /api/alertmanager/grafana/api/v2/alerts
```

### Annotations

**Query annotations:**

```bash
GET /api/annotations?from=<epoch_ms>&to=<epoch_ms>&tags=tag1&tags=tag2&limit=100
```

**Create annotation:**

```bash
POST /api/annotations
{
  "dashboardUID": "jcIIG-07z",
  "panelId": 2,
  "time": 1507037197339,
  "timeEnd": 1507180805056,
  "tags": ["tag1", "tag2"],
  "text": "Annotation Description"
}
```

**Update annotation:**

```bash
PUT /api/annotations/<annotation_id>
{
  "time": 1507037197339,
  "timeEnd": 1507180805056,
  "text": "Updated annotation",
  "tags": ["updated-tag"]
}
```

**Delete annotation:**

```bash
DELETE /api/annotations/<annotation_id>
```

### Users & Teams

**Search users (admin):**

```bash
GET /api/users/search?perpage=10&page=1&query=<search_term>
```

**Get current user:**

```bash
GET /api/user
```

**List teams:**

```bash
GET /api/teams/search?perpage=50&page=1&name=<team_name>
```

**Create team:**

```bash
POST /api/teams
{
  "name": "MyTeam",
  "email": "team@example.com"
}
```

**Add user to team:**

```bash
POST /api/teams/<team_id>/members
{
  "userId": <user_id>
}
```

### Organizations

**Get current organization:**

```bash
GET /api/org
```

**List all organizations (admin):**

```bash
GET /api/orgs
```

**Create organization (admin):**

```bash
POST /api/orgs
{
  "name": "New Org"
}
```

### Service Accounts

**List service accounts:**

```bash
GET /api/serviceaccounts/search?perpage=10&page=1
```

**Create service account:**

```bash
POST /api/serviceaccounts
{
  "name": "automation-sa",
  "role": "Editor"
}
```

**Create service account token:**

```bash
POST /api/serviceaccounts/<service_account_id>/tokens
{
  "name": "token-name",
  "secondsToLive": 86400
}
```

## Reference Documentation

For detailed API documentation by domain:

- **[Dashboards API](references/dashboards.md)**: Complete dashboard CRUD, versions, permissions
- **[Data Sources API](references/datasources.md)**: Data source management, queries, health checks
- **[Alerting API](references/alerting.md)**: Alert rules, contact points, notification policies, silences
- **[Folders API](references/folders.md)**: Folder management and permissions
- **[Annotations API](references/annotations.md)**: Create, query, update annotations
- **[Users & Teams API](references/users_teams.md)**: User management, team operations
- **[Common Patterns](references/common_patterns.md)**: Error handling, pagination, Python utilities

## Python Helper Library

Use `scripts/grafana_api.py` for a reusable Python client:

```python
from grafana_api import GrafanaAPI

# Initialize client
grafana = GrafanaAPI(
    base_url="https://your-grafana.com",
    token="your-service-account-token"
)

# List dashboards
dashboards = grafana.search_dashboards(query="production")

# Get dashboard details
dashboard = grafana.get_dashboard_by_uid("abc123")

# Create annotation
grafana.create_annotation(
    dashboard_uid="abc123",
    text="Deployment completed",
    tags=["deploy", "production"]
)

# Query data source
result = grafana.query_datasource(
    datasource_uid="prometheus-uid",
    expr="up",
    start="now-1h",
    end="now"
)
```

## Common Operations

### Export Dashboard as JSON

```bash
curl -H "Authorization: Bearer <TOKEN>" \
     https://your-grafana.com/api/dashboards/uid/<uid> | jq '.dashboard'
```

### Import Dashboard

```bash
curl -X POST -H "Authorization: Bearer <TOKEN>" \
     -H "Content-Type: application/json" \
     -d @dashboard.json \
     https://your-grafana.com/api/dashboards/db
```

### Bulk Delete Dashboards by Tag

```python
dashboards = grafana.search_dashboards(tag="deprecated")
for dash in dashboards:
    grafana.delete_dashboard(dash['uid'])
```

### Clone Dashboard to Another Folder

```python
source = grafana.get_dashboard_by_uid("source-uid")
source['dashboard']['id'] = None
source['dashboard']['uid'] = None
source['dashboard']['title'] = f"{source['dashboard']['title']} (Copy)"
source['folderUid'] = "target-folder-uid"
grafana.create_or_update_dashboard(source)
```

## Error Handling

Common HTTP status codes:

- `200`: Success
- `400`: Bad request (invalid JSON, missing required fields)
- `401`: Unauthorized (invalid/missing token)
- `403`: Forbidden (insufficient permissions)
- `404`: Not found
- `409`: Conflict (resource already exists)
- `412`: Precondition failed (version mismatch)
- `422`: Unprocessable entity (validation error)

## Tips

1. **Use UIDs over IDs**: UIDs are portable across Grafana instances
2. **Include version for updates**: Prevents overwriting concurrent changes
3. **Use `overwrite: true` carefully**: Only when you want to force-update
4. **Paginate large results**: Use `limit` and `page` parameters
5. **Test in dev first**: Always test API calls on non-production instances
6. **Service accounts over API keys**: API keys are deprecated in newer Grafana versions
