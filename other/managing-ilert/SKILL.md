---
name: managing-ilert
description: |
  Use when working with Ilert — iLert alerting and incident management covering
  alert source configuration, on-call scheduling, escalation policies, status
  page management, heartbeat monitoring, uptime tracking, and notification
  channel setup. Use when configuring iLert alert sources, managing on-call
  rotations, setting up status pages, monitoring heartbeats, or analyzing
  incident response metrics.
connection_type: ilert
preload: false
---

# iLert Management Skill

Manage iLert alerting, on-call schedules, escalation policies, status pages, and heartbeat monitoring.

## API Conventions

### Authentication
All API calls use the `Authorization: XXXXXX` header — injected automatically. Never hardcode tokens.

### Base URL
`https://api.ilert.com/api`

### Core Helper Function

```bash
#!/bin/bash

il_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: $ILERT_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.ilert.com/api${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: $ILERT_API_KEY" \
            "https://api.ilert.com/api${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target ≤50 lines per script output

## Alert Sources

### List Alert Sources
```bash
il_api GET "/alert-sources" | jq '[.[] | {
  id, name, status, integrationType,
  escalationPolicy: .escalationPolicy.name,
  teams: [.teams[]?.name]
}]'
```

### Get Alert Source Details
```bash
il_api GET "/alert-sources/ALERT_SOURCE_ID" | jq '{
  name, status, integrationType,
  escalationPolicy: .escalationPolicy.name,
  supportHours, autoResolutionTimeout
}'
```

## Incidents

### List Active Incidents
```bash
il_api GET "/incidents?states=PENDING,ACCEPTED" | jq '[.[] | {
  id, summary, status, priority,
  alertSource: .alertSource.name,
  assignedTo: .assignedTo.username,
  createdAt, acceptedAt
}]'
```

### Get Incident Timeline
```bash
il_api GET "/incidents/INCIDENT_ID/log-entries" | jq '[.[] | {
  type, text, timestamp,
  user: .user.username
}]'
```

## On-Call Schedules

### List Schedules
```bash
il_api GET "/schedules" | jq '[.[] | {
  id, name, timezone,
  currentOnCall: .currentShift.user.username,
  teams: [.teams[]?.name]
}]'
```

### Get Schedule Shifts
```bash
il_api GET "/schedules/SCHEDULE_ID/shifts?from=2024-01-01&until=2024-01-31" | jq '[.[] | {
  user: .user.username,
  start, end
}]'
```

## Escalation Policies

### List Escalation Policies
```bash
il_api GET "/escalation-policies" | jq '[.[] | {
  id, name,
  rules: [.escalationRules[] | {
    delayMinutes: .escalationTimeout,
    targets: [.users[]?.username // .schedules[]?.name]
  }]
}]'
```

## Status Pages

### List Status Pages
```bash
il_api GET "/status-pages" | jq '[.[] | {id, name, status, url, services: [.services[] | {name, status}]}]'
```

### Update Status Page Component
```bash
il_api PUT "/status-pages/PAGE_ID/services/SERVICE_ID" '{
  "status": "DEGRADED"
}'
```

## Heartbeat Monitoring

### List Heartbeat Monitors
```bash
il_api GET "/heartbeats" | jq '[.[] | {
  id, name, status, intervalSec,
  alertSource: .alertSource.name,
  lastPingAt
}]'
```

### Check Heartbeat Status
```bash
il_api GET "/heartbeats/HEARTBEAT_ID" | jq '{
  name, status, intervalSec,
  lastPingAt, lastAlertAt,
  alertSource: .alertSource.name
}'
```

## Common Tasks

1. **Configure alert sources** — set up integrations with monitoring tools and route to escalation policies
2. **Manage on-call schedules** — create rotation-based schedules with override support
3. **Build escalation policies** — define multi-step escalation with timeouts
4. **Maintain status pages** — update service status during incidents for external communication
5. **Monitor heartbeats** — verify critical services are sending regular health pings

## Output Format

Present results as a structured report:
```
Managing Ilert Report
═════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

