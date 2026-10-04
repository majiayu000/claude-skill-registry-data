---
name: managing-heap
description: |
  Use when working with Heap — heap analytics management — monitor auto-captured
  events, defined events, user segments, and data health. Use when inspecting
  autocapture coverage, reviewing defined events, debugging tracking gaps, or
  auditing data volume.
connection_type: heap
preload: false
---

# Managing Heap

Manage and monitor Heap product analytics — autocapture, defined events, segments, and data health.

## Discovery Phase

```bash
#!/bin/bash

HEAP_API="https://heapanalytics.com/api"
AUTH="Authorization: Bearer $HEAP_API_TOKEN"

echo "=== Account Info ==="
curl -s -H "$AUTH" "$HEAP_API/v1/account" \
  | jq '{id: .id, name: .name, plan: .plan, domain: .domain}'

echo ""
echo "=== Defined Events ==="
curl -s -H "$AUTH" "$HEAP_API/v1/events/defined" \
  | jq -r '.[] | [.id, .name, .type, .lastTriggered] | @tsv' | column -t | head -15

echo ""
echo "=== User Properties ==="
curl -s -H "$AUTH" "$HEAP_API/v1/user-properties" \
  | jq -r '.[] | [.name, .type, .source] | @tsv' | column -t | head -15

echo ""
echo "=== Segments ==="
curl -s -H "$AUTH" "$HEAP_API/v1/segments" \
  | jq -r '.[] | [.id, .name, .size, .lastComputed] | @tsv' | column -t | head -10
```

## Analysis Phase

```bash
#!/bin/bash

HEAP_API="https://heapanalytics.com/api"
AUTH="Authorization: Bearer $HEAP_API_TOKEN"

echo "=== Event Volume (Last 7 Days) ==="
curl -s -H "$AUTH" -X POST "$HEAP_API/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"query":{"measures":[{"type":"total"}],"time":{"kind":"dynamic","value":"7d"},"group_by":["event_name"]}}' \
  | jq -r '.results[:15][] | [.event_name, .value] | @tsv' | sort -t$'\t' -k2 -rn | column -t

echo ""
echo "=== Active Users (DAU) ==="
curl -s -H "$AUTH" -X POST "$HEAP_API/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"query":{"measures":[{"type":"unique_users"}],"time":{"kind":"dynamic","value":"7d"},"granularity":"day"}}' \
  | jq -r '.results[] | [.date, .value] | @tsv' | column -t

echo ""
echo "=== Pageview Distribution ==="
curl -s -H "$AUTH" -X POST "$HEAP_API/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"query":{"event":"pageview","measures":[{"type":"total"}],"time":{"kind":"dynamic","value":"7d"},"group_by":["path"]}}' \
  | jq -r '.results[:10][] | [.path, .value] | @tsv' | column -t

echo ""
echo "=== Data Health ==="
curl -s -H "$AUTH" "$HEAP_API/v1/data-health" \
  | jq '{eventsToday: .events_today, usersToday: .users_today, lastEventAt: .last_event_at, status: .status}'
```

## Output Format

```
ACCOUNT
Name:       <account-name>
Plan:       <plan>
Domain:     <domain>

TOP EVENTS (7d)
Event Name           Volume
<event-name>         <count>

ACTIVE USERS (DAU)
Date          Users
<date>        <n>

DATA HEALTH
Events Today:    <n>
Users Today:     <n>
Last Event:      <timestamp>
Status:          <status>
```

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

