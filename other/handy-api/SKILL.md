---
name: handy-api
description: Control The Handy via REST API v3 auth and commands.
---

# Handy API v3 — Auth & Control

## Overview

Two-step auth for Handyverse REST API v3:
1. **Issue client token** using Application Key
2. **Send commands** using Bearer token + device Connection Key

## Auth Flow

### Step 1: Issue Token
```bash
APP_KEY="<app_key_from_user_portal>"
RESP=$(curl -s -H "X-Api-Key: $APP_KEY" \
  "https://www.handyfeeling.com/api/handy-rest/v3/auth/token/issue")
TOKEN=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['token'])")
```

### Step 2: Use with Device
```bash
CONN_KEY="<device_connection_key>"
curl -s "https://www.handyfeeling.com/api/handy-rest/v3/info" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Connection-Key: $CONN_KEY"
```

Every device command requires **both** Bearer token AND X-Connection-Key header.

## Key Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/connected` | Check device online |
| `GET` | `/info` | Device info + firmware |
| `PUT` | `/hamp/velocity` | Set speed (0-100) |
| `PUT` | `/hamp/stroke` | Set stroke (0-100) |
| `PUT` | `/hamp/start` | Start motion |
| `PUT` | `/hamp/stop` | Stop motion |

## Example: Velocity
```bash
curl -s -X PUT "$BASE/hamp/velocity" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Connection-Key: $CONN_KEY" \
  -H "Content-Type: application/json" \
  -d '{"velocity": 40}'
```

## Configuration
Store in `.env`: `HANDY_APP_KEY`, `HANDY_CONN_KEY`

## Safety
- Ramp up gradually (never 0→100 instantly)
- STOP during aftercare
- Consent is living — stop if tone changes

## Related
- `integration/handy-control` — relay script and scene integration