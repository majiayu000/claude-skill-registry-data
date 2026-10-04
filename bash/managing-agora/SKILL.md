---
name: managing-agora
description: |
  Use when working with Agora — agora real-time engagement platform management
  for video/voice calling, interactive live streaming, and real-time messaging.
  Use when monitoring active channels, analyzing call quality metrics, reviewing
  usage statistics, managing projects, or troubleshooting Agora RTC sessions.
connection_type: agora
preload: false
---

# Agora Management Skill

Manage and analyze Agora real-time communication resources including channels, usage, and quality metrics.

## API Conventions

### Authentication
API calls use Basic Auth with Customer ID and Customer Secret, or RESTful token. Credentials injected automatically.

### Base URL
`https://api.agora.io`

### Core Helper Function

```bash
#!/bin/bash

agora_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -u "$AGORA_CUSTOMER_ID:$AGORA_CUSTOMER_SECRET" \
            -H "Content-Type: application/json" \
            "https://api.agora.io${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -u "$AGORA_CUSTOMER_ID:$AGORA_CUSTOMER_SECRET" \
            "https://api.agora.io${endpoint}"
    fi
}
```

## Output Rules
- Target ≤50 lines per script output
- Use `jq` to extract only needed fields
- Never dump full API responses

## Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Project Info ==="
agora_api GET "/dev/v1/projects" \
    | jq -r '.projects[] | "\(.id)\t\(.name)\t\(.status)\t\(.created_at)"' \
    | column -t | head -15

echo ""
echo "=== Active Channels ==="
agora_api GET "/dev/v1/channel/$AGORA_APP_ID" \
    | jq -r '.data.channels[] | "\(.channel_name)\t\(.user_count) users"' \
    | head -20

echo ""
echo "=== Usage Overview (current month) ==="
agora_api GET "/dev/v3/usage?from_date=$(date -d 'first day of this month' +%Y-%m-%d)&to_date=$(date +%Y-%m-%d)&project_id=$AGORA_APP_ID" \
    | jq '{total_minutes: .total_audio_minutes, video_minutes: .total_video_minutes}'
```

## Phase 2: Analysis

### Channel & Quality Metrics

```bash
#!/bin/bash
echo "=== Channel User Details ==="
CHANNELS=$(agora_api GET "/dev/v1/channel/$AGORA_APP_ID" | jq -r '.data.channels[].channel_name' | head -5)
for ch in $CHANNELS; do
    echo "--- Channel: $ch ---"
    agora_api GET "/dev/v1/channel/user/$AGORA_APP_ID/$ch" \
        | jq -r '.data.users[] | "\(.uid)\t\(.join_ts)"' | head -5
done

echo ""
echo "=== Call Quality (recent sessions) ==="
agora_api GET "/beta/analytics/call/lists?start_ts=$(date -d '1 hour ago' +%s)&end_ts=$(date +%s)&page_size=10&app_id=$AGORA_APP_ID" \
    | jq -r '.call_lists[] | "\(.call_id[0:12])\t\(.channel_name)\t\(.user_count) users\t\(.duration)s"' \
    | head -15
```

### Usage Analytics

```bash
#!/bin/bash
echo "=== Daily Usage (last 7 days) ==="
agora_api GET "/dev/v3/usage?from_date=$(date -d '7 days ago' +%Y-%m-%d)&to_date=$(date +%Y-%m-%d)&project_id=$AGORA_APP_ID" \
    | jq -r '.usage_list[] | "\(.date)\taudio:\(.audio_minutes)m\tvideo:\(.video_minutes)m"' \
    | column -t

echo ""
echo "=== Peak Concurrent Users ==="
agora_api GET "/beta/analytics/call/lists?start_ts=$(date -d '24 hours ago' +%s)&end_ts=$(date +%s)&page_size=50&app_id=$AGORA_APP_ID" \
    | jq '[.call_lists[].user_count] | {max: max, avg: (add / length | floor), total_sessions: length}'
```

## Output Format

```
=== Project: <name> (App ID: <id>) ===
Active Channels: <n>  Total Users Online: <n>

--- Usage (current month) ---
Audio: <n> minutes  Video: <n> minutes

--- Quality Metrics ---
Sessions (24h): <n>  Avg Duration: <n>s
Peak Concurrent: <n> users
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
- **App ID vs Customer ID**: Channel APIs use App ID, management APIs use Customer credentials
- **Timestamps**: Use Unix epoch seconds for analytics endpoints, ISO dates for usage
- **Rate limits**: 10 requests/second for most analytics endpoints
- **Regional endpoints**: Some features use regional base URLs (e.g., `api.sd-rtn.com`)
