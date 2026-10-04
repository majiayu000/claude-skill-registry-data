---
name: skylight
description: Control Skylight Calendar frame via the unofficial API. Use when managing family calendar events, chores, lists, task box items, and rewards on a Skylight family calendar display. Triggers on "skylight", "family calendar", "add event", "chore", "family schedule", "calendar event".
---

# Skylight Calendar

Control Skylight Calendar frame via the unofficial API.

## Setup

Set environment variables in ~/.openclaw/.env:
- `SKYLIGHT_EMAIL`: Your Skylight account email
- `SKYLIGHT_PASSWORD`: Your Skylight account password
- `SKYLIGHT_FRAME_ID`: Your frame/household ID (from ourskylight.com URL)
- `SKYLIGHT_URL`: Base URL (default: `https://app.ourskylight.com`)

## Authentication

Login and generate token:
```bash
source ~/.openclaw/.env
LOGIN=$(curl -s -X POST "$SKYLIGHT_URL/api/sessions" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$SKYLIGHT_EMAIL\",\"password\":\"$SKYLIGHT_PASSWORD\",\"resettingPassword\":\"false\"}")
USER_ID=$(echo $LOGIN | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
USER_TOKEN=$(echo $LOGIN | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['attributes']['token'])")
SKYLIGHT_TOKEN="Basic $(echo -n "${USER_ID}:${USER_TOKEN}" | base64)"
```

## Calendar Events

### List events
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/calendar_events?date_min=YYYY-MM-DD&date_max=YYYY-MM-DD" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

### Create event
```bash
curl -s -X POST "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/calendar_events" \
  -H "Authorization: $SKYLIGHT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "type": "calendar_event",
      "attributes": {
        "summary": "Event Title",
        "start": "YYYY-MM-DD",
        "start_time": "HH:MM",
        "end": "YYYY-MM-DD",
        "end_time": "HH:MM",
        "all_day": false
      }
    }
  }'
```

### Delete event
```bash
curl -s -X DELETE "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/calendar_events/{eventId}" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

## Chores

### List chores
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/chores?after=YYYY-MM-DD&before=YYYY-MM-DD" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

### Create chore
```bash
curl -s -X POST "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/chores" \
  -H "Authorization: $SKYLIGHT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "type": "chore",
      "attributes": {
        "summary": "Take out trash",
        "status": "pending",
        "start": "YYYY-MM-DD",
        "recurring": false
      }
    }
  }'
```

## Lists

### List all lists
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/lists" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

### Add item to list
```bash
curl -s -X POST "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/lists/{listId}/items" \
  -H "Authorization: $SKYLIGHT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data":{"type":"list_item","attributes":{"label":"Milk","status":"pending"}}}'
```

## Categories (Profiles)

### List categories/profiles
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/categories" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

## Notes
- API is unofficial/reverse-engineered — endpoints may change
- Tokens expire on logout
- Frame ID = household ID from ourskylight.com URL
- All responses use JSON:API format
