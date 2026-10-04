---
name: managing-ably
description: |
  Use when working with Ably — ably real-time messaging platform management
  covering channels, presence, connections, usage analytics, and account health.
  Use when monitoring active channels, analyzing connection metrics, reviewing
  usage quotas, managing Ably apps and keys, or troubleshooting real-time
  messaging issues.
connection_type: ably
preload: false
---

# Ably Management Skill

Manage and analyze Ably real-time messaging resources including channels, connections, and usage.

## API Conventions

### Authentication
All API calls use Basic Auth with API key, injected automatically.

### Base URL
`https://rest.ably.io` (REST API) and `https://control.ably.net/v1` (Control API)

### Core Helper Function

```bash
#!/bin/bash

ably_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -u "$ABLY_API_KEY" \
            -H "Content-Type: application/json" \
            "https://rest.ably.io${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -u "$ABLY_API_KEY" \
            "https://rest.ably.io${endpoint}"
    fi
}

ably_control() {
    local method="$1"
    local endpoint="$2"
    curl -s -X "$method" \
        -H "Authorization: Bearer $ABLY_CONTROL_TOKEN" \
        "https://control.ably.net/v1${endpoint}"
}
```

## Output Rules
- Target ≤50 lines per script output
- Use `jq` to extract only needed fields
- Never dump full API responses

## Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Active Channels ==="
ably_api GET "/channels?limit=20" \
    | jq -r '.[] | "\(.channelId)\t\(.status.isActive)\toccupancy:\(.status.occupancy.metrics.connections // 0)"' \
    | column -t | head -20

echo ""
echo "=== App Stats (current hour) ==="
ably_api GET "/stats?unit=hour&limit=1" \
    | jq '.[0] | {
        messages_published: .all.messages.count,
        connections_peak: .all.connections.peak,
        api_requests: .all.apiRequests.succeeded
    }'

echo ""
echo "=== Account Apps ==="
ably_control GET "/accounts/$ABLY_ACCOUNT_ID/apps" \
    | jq -r '.[] | "\(.id)\t\(.name)\t\(.status)\t\(.created[0:10])"' \
    | head -15
```

## Phase 2: Analysis

### Channel Health

```bash
#!/bin/bash
echo "=== Channel Occupancy ==="
ably_api GET "/channels?limit=50" \
    | jq -r '.[] | select(.status.isActive == true) | "\(.channelId)\tconns:\(.status.occupancy.metrics.connections // 0)\tpresence:\(.status.occupancy.metrics.presenceMembers // 0)"' \
    | sort -t$'\t' -k2 -rn | head -15

echo ""
echo "=== Presence Members (active channels) ==="
ably_api GET "/channels?limit=20" \
    | jq -r '.[] | select(.status.occupancy.metrics.presenceMembers > 0) | .channelId' | while read ch; do
    echo "--- $ch ---"
    ably_api GET "/channels/$(echo $ch | sed 's/:/%3A/g')/presence" \
        | jq -r '.[] | "\(.clientId)\t\(.connectionId[0:12])"' | head -5
done | head -20
```

### Usage Analytics

```bash
#!/bin/bash
echo "=== Usage (last 24h, hourly) ==="
ably_api GET "/stats?unit=hour&limit=24" \
    | jq -r '.[] | "\(.intervalId)\tmsgs:\(.all.messages.count)\tconns:\(.all.connections.peak)\tapi:\(.all.apiRequests.succeeded)"' \
    | column -t | head -24

echo ""
echo "=== Monthly Usage Summary ==="
ably_api GET "/stats?unit=month&limit=1" \
    | jq '.[0] | {
        total_messages: .all.messages.count,
        peak_connections: .all.connections.peak,
        api_requests: .all.apiRequests.succeeded,
        api_errors: .all.apiRequests.failed
    }'
```

## Output Format

```
=== Ably App ===
Active Channels: <n>  Peak Connections: <n>

--- Hourly Stats ---
Messages: <n>  Connections: <n>  API Requests: <n>

--- Channel Health ---
<channel>: <connections> connections, <presence> presence

--- Monthly Usage ---
Messages: <n>  Peak Connections: <n>
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

## Common Pitfalls
- **Two APIs**: REST API for real-time data, Control API for account management (different auth)
- **Channel encoding**: Encode `:` as `%3A` in channel names in URLs
- **Stats intervals**: Use `unit` param: `minute`, `hour`, `day`, `month`
- **Rate limits**: 100 requests/second for REST API
- **Pagination**: Use `limit` and response `Link` headers for cursor pagination
