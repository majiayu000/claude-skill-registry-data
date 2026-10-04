---
name: billing-monitor
description: "Monitor for API billing errors and alert the owner and admin immediately. Use when: an API billing error is detected, a peer PA reports a billing error, or during routine health checks. Handles detection, notification, and fallback model switching. Model-agnostic: works with any LLM provider (Anthropic, OpenAI, Google, etc.)."
---

# Billing Monitor Skill

## Minimum Model
Any model. Detection and alerting are rule-based. No reasoning required.

---

## When to Run This Skill

Run when you see ANY of these in an API response:
```
your API key has run out of credits
insufficient balance
billing_error
payment_required
exceeded your current quota
HTTP 402
"type": "billing_error"
```

## When NOT to Alert the Owner

- Routine billing check completed with no errors → **silent, no message**
- HTTP 200 / all clear → **silent, no message**
- ElevenLabs 401 (auth, not billing) → **silent unless TTS is actively needed**

**Only alert the owner if:**
1. HTTP 402 detected (out of credits)
2. LLM is unreachable and the agent cannot function
3. A peer PA reports a billing error

Routine health checks run silently. The owner does not need a "billing OK" message.

---

## Response Steps (Run in Order)

### Step 1 — Notify Owner

Send via WhatsApp (or preferred channel):

```
⚠️ Billing issue — I can't respond normally.
My API key ran out of credits (or was rate-limited).
Please top up or switch my API key in agent settings.
```

### Step 2 — Notify Admin

```
[PA Name] has a billing error.
Owner: [Owner Name]
Action: top up API credits or reassign key.
Time: [current timestamp]
```

### Step 3 — Switch to Fallback Model

1. Check if `config/billing-fallback.json` exists
2. If yes → read the `fallback_model` field
3. Run: `openclaw config set model "$FALLBACK_MODEL"`
4. If the command fails → tell owner: "Auto-switch failed — please update model manually in agent settings"
5. Notify owner: "Switched to [Fallback Model] temporarily while primary key is resolved"

If `billing-fallback.json` doesn't exist → skip this step and tell admin to configure it.

### Step 4 — Log the Incident

```bash
LOG_DIR="$HOME/.openclaw/workspace/logs"
mkdir -p "$LOG_DIR"

# Append one line to the log file
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) BILLING_ERROR api_key_exhausted" \
  >> "$LOG_DIR/billing-incidents.log"
```

---

## Health Check Script

Run this during heartbeat to catch billing issues before they cause failures:

```bash
#!/bin/bash
# billing-check.sh
# Checks the LLM provider API key configured in env vars

set -e

LOG_DIR="$HOME/.openclaw/workspace/logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Detect provider from env vars (check in order)
if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
  PROVIDER="Anthropic"
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "x-api-key: ${ANTHROPIC_API_KEY}" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "{\"model\":\"claude-haiku-20240307\",\"max_tokens\":1,\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}]}" \
    https://api.anthropic.com/v1/messages 2>/dev/null)

elif [ -n "${OPENAI_API_KEY:-}" ]; then
  PROVIDER="OpenAI"
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer ${OPENAI_API_KEY}" \
    -H "content-type: application/json" \
    -d "{\"model\":\"gpt-4o-mini\",\"max_tokens\":1,\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}]}" \
    https://api.openai.com/v1/chat/completions 2>/dev/null)

elif [ -n "${GOOGLE_API_KEY:-}" ]; then
  PROVIDER="Google"
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    "https://generativelanguage.googleapis.com/v1beta/models?key=${GOOGLE_API_KEY}" 2>/dev/null)

else
  echo "$TIMESTAMP SKIP no API key env var found" >> "$LOG_DIR/billing-incidents.log"
  exit 0
fi

# Act on the HTTP status code
case "$HTTP_STATUS" in
  200)
    echo "$TIMESTAMP OK $PROVIDER" >> "$LOG_DIR/billing-incidents.log"
    ;;
  402)
    echo "$TIMESTAMP BILLING_ERROR $PROVIDER HTTP_402" >> "$LOG_DIR/billing-incidents.log"
    echo "BILLING ERROR — run the 4-step response protocol above"
    exit 1
    ;;
  401)
    echo "$TIMESTAMP AUTH_ERROR $PROVIDER HTTP_401" >> "$LOG_DIR/billing-incidents.log"
    echo "AUTH ERROR — invalid API key, notify admin"
    exit 1
    ;;
  429)
    echo "$TIMESTAMP RATE_LIMITED $PROVIDER HTTP_429" >> "$LOG_DIR/billing-incidents.log"
    echo "RATE LIMITED — wait 60 seconds and retry. Not a billing issue."
    exit 2
    ;;
  *)
    echo "$TIMESTAMP UNKNOWN $PROVIDER HTTP_$HTTP_STATUS" >> "$LOG_DIR/billing-incidents.log"
    echo "UNKNOWN ERROR HTTP $HTTP_STATUS"
    exit 1
    ;;
esac
```

**HTTP status meanings:**
- `200` → OK
- `402` → Billing error → run 4-step protocol
- `401` → Invalid key → notify admin
- `429` → Rate limit (temporary) → wait and retry, do NOT trigger billing protocol

---

## Fallback Config File

Create `config/billing-fallback.json` in your workspace:

```json
{
  "primary_provider": "your-primary-provider",
  "primary_model": "your-primary-model",
  "fallback_provider": "your-fallback-provider",
  "fallback_model": "your-fallback-model",
  "admin_phone": "+1XXXXXXXXXX",
  "alert_channel": "whatsapp"
}
```

Replace placeholders with real values. Examples:
- Anthropic → OpenAI: `"primary_provider": "anthropic"`, `"primary_model": "claude-haiku-20240307"`, `"fallback_provider": "openai"`, `"fallback_model": "gpt-4o-mini"`

---

## Recovery (After Credits Restored)

1. Owner confirms credits are topped up.
2. Read the primary model name from config:
   ```bash
   PRIMARY=$(python3 -c "
   import json
   with open('config/billing-fallback.json') as f:
       print(json.load(f)['primary_model'])
   ")
   ```
3. Switch back to primary:
   ```bash
   openclaw config set model "$PRIMARY"
   ```
4. Log the recovery:
   ```bash
   echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) BILLING_RESTORED" \
     >> ~/.openclaw/workspace/logs/billing-incidents.log
   ```
5. Notify owner: "✅ Primary model restored. Normal service resumed."

---

## Edge Cases

| Scenario | Action |
|---|---|
| 429 rate limit | Wait 60s, retry. Do NOT trigger billing protocol. |
| 5xx server error | Retry 2x with 10s delay. If persists → notify owner. |
| Both primary AND fallback billing errors | Escalate to admin immediately. Agent cannot function. |
| No API key env var set | Log as config issue. Notify admin. |
| Peer PA reports billing error | Log it. Notify admin if you are the network coordinator. |

---

## Cost Tips

- **Cheap:** Health checks with `curl` — no LLM cost at all
- **Expensive:** Running health checks too frequently wastes money. Every 2 hours is enough.
- **Batch:** Combine billing check with other heartbeat checks in one script run
- **Small model OK:** This skill needs no reasoning — any model can send a notification message

---

## Running via Cron (Recommended)

Instead of a plugin, run billing-monitor as a scheduled skill via cron:

```json
{
  "id": "billing-health-check",
  "schedule": { "kind": "cron", "expr": "0 * * * *", "tz": "UTC" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run the billing-monitor skill: check all configured API keys for billing errors. If any provider returns 402, send an alert to the admin phone and update billing-status.json. Reply HEARTBEAT_OK if all clear."
  },
  "delivery": { "mode": "silent" }
}
```

This runs every hour and alerts automatically — no plugin required.
