---
name: datadog-incidents
description: Work with Datadog Incidents API - fetch incidents with enrichment, update incident fields, understand incident data structures. Use when working with incidents or the dd get-incident/update-incident commands.
---

# Datadog Incidents API

## CLI Commands

```bash
# Get incident by ID (public ID like 152, or UUID)
dd get-incident 152

# Get enriched incident with user details
dd get-incident 152 --include users

# Get fully enriched with incident type and integrations
dd get-incident 152 --include users --enrich

# Update incident
dd update-incident 152 --title "New Title" --severity SEV-2 --state resolved
```

## Enrichment Levels

### Basic (no flags)
Returns incident data with UUIDs for users - less useful for human analysis.

### With `--include users`
Transforms user references:
```json
"created_by": {
  "data": {
    "type": "users",
    "id": "0082a465-...",
    "attributes": {
      "name": "Peter Chang",
      "email": "peterc@wonder.com"
    }
  }
}
```

### With `--enrich`
Adds `enrichment` section with:
- **Incident type**: Name, description, prefix
- **Integrations**: Slack channels, Jira tickets with direct links

## Update Fields

### Standard fields
- `--title` - Incident title
- `--severity` - SEV-1, SEV-2, etc.
- `--state` - active, stable, resolved
- `--customer-impacted` - true/false
- `--customer-impact-scope` - Description of impact

### Custom fields
```bash
dd update-incident 152 --field "root_cause=Database timeout" --field "teams=backend"
```

## Key Notes

- **CLI accepts public IDs**: Use `152` instead of full UUID
- **API requires UUIDs**: CLI handles conversion internally
- **Permission requirements**: App key owner needs incident management permissions
- The `include` parameter only works for `users` and `attachments`

## curl Examples

```bash
# Get with user enrichment
curl -X GET "https://api.$DD_SITE/api/v2/incidents/$INCIDENT_UUID?include=users" \
  -H "DD-API-KEY: $DD_API_KEY" \
  -H "DD-APPLICATION-KEY: $DD_APP_KEY"

# Get integrations (Slack/Jira)
curl -X GET "https://api.$DD_SITE/api/v2/incidents/$INCIDENT_UUID/relationships/integrations" \
  -H "DD-API-KEY: $DD_API_KEY" \
  -H "DD-APPLICATION-KEY: $DD_APP_KEY"

# Get incident type config
curl -X GET "https://api.$DD_SITE/api/v2/incidents/config/types/$TYPE_UUID" \
  -H "DD-API-KEY: $DD_API_KEY" \
  -H "DD-APPLICATION-KEY: $DD_APP_KEY"
```
