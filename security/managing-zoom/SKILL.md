---
name: managing-zoom
description: |
  Use when working with Zoom — zoom meeting and webinar management covering
  scheduled meetings, recordings, users, and usage analytics. Use when auditing
  Zoom usage, managing meetings, retrieving recordings, or analyzing meeting
  participation patterns across a Zoom account.
connection_type: zoom
preload: false
---

# Managing Zoom

Comprehensive Zoom meeting management and analytics via the Zoom REST API.

## Discovery Phase

```bash
#!/bin/bash
ZOOM_BASE="https://api.zoom.us/v2"

echo "=== Current User ==="
curl -s -H "Authorization: Bearer $ZOOM_TOKEN" \
  "$ZOOM_BASE/users/me" | jq '{id, email, first_name, last_name, type, status}'

echo ""
echo "=== Users in Account (top 30) ==="
curl -s -H "Authorization: Bearer $ZOOM_TOKEN" \
  "$ZOOM_BASE/users?page_size=30&status=active" \
  | jq -r '.users[] | "\(.id)\t\(.email)\t\(.type)\t\(.status)"' | column -t

echo ""
echo "=== Upcoming Meetings ==="
curl -s -H "Authorization: Bearer $ZOOM_TOKEN" \
  "$ZOOM_BASE/users/me/meetings?type=upcoming&page_size=20" \
  | jq -r '.meetings[] | "\(.id)\t\(.topic[0:40])\t\(.start_time // "recurring")\t\(.duration)min"' | column -t

echo ""
echo "=== Recent Recordings (last 30 days) ==="
FROM_DATE=$(date -v-30d +%Y-%m-%d 2>/dev/null || date -d "-30 days" +%Y-%m-%d)
curl -s -H "Authorization: Bearer $ZOOM_TOKEN" \
  "$ZOOM_BASE/users/me/recordings?from=$FROM_DATE&page_size=10" \
  | jq -r '.meetings[]? | "\(.topic[0:40])\t\(.start_time[0:10])\t\(.duration)min\t\(.total_size)"' | column -t
```

## Analysis Phase

```bash
#!/bin/bash
ZOOM_BASE="https://api.zoom.us/v2"
MEETING_ID="${1:?Meeting ID required}"

echo "=== Meeting Details ==="
curl -s -H "Authorization: Bearer $ZOOM_TOKEN" \
  "$ZOOM_BASE/meetings/$MEETING_ID" \
  | jq '{id, topic, type, start_time, duration, timezone, join_url, settings: {waiting_room: .settings.waiting_room, auto_recording: .settings.auto_recording}}'

echo ""
echo "=== Past Meeting Participants ==="
curl -s -H "Authorization: Bearer $ZOOM_TOKEN" \
  "$ZOOM_BASE/past_meetings/$MEETING_ID/participants?page_size=30" \
  | jq -r '.participants[]? | "\(.name)\t\(.email // "N/A")\t\(.duration)sec\t\(.join_time[0:19])"' | column -t

echo ""
echo "=== Account Dashboard ==="
curl -s -H "Authorization: Bearer $ZOOM_TOKEN" \
  "$ZOOM_BASE/report/daily?year=$(date +%Y)&month=$(date +%m)" \
  | jq '{total_meetings: .dates[-1].meetings, total_participants: .dates[-1].participants, total_meeting_minutes: .dates[-1].meeting_minutes}'
```

## Output Format

```
ZOOM ACCOUNT HEALTH
User:           [name] ([email])
Account Type:   [type]
Active Users:   [count]

UPCOMING MEETINGS
ID            Topic                    Start Time       Duration
[id]          [topic]                  [datetime]       [n]min

USAGE SUMMARY (Last 30 Days)
Meetings Held:    [count]
Total Minutes:    [minutes]
Avg Participants: [avg]
Recordings:       [count] ([size] total)
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

