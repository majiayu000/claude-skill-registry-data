---
name: whatsapp-diagnostics
description: "Diagnose and fix WhatsApp connectivity issues for OpenClaw agents. Use when: a PA is not responding, WhatsApp shows connected but messages don't arrive, the agent is online but not replying, or troubleshooting a new agent setup."
---

# WhatsApp Diagnostics Skill

## Minimum Model
Any model. All diagnostics are CLI-based — follow the decision tree.

---

## Diagnostic Tree (Start Here)

```
PA not responding?
│
├─ Dashboard shows "Connected and listening"?
│   ├─ YES → Check Messages count
│   │   ├─ Messages = 0 → INGEST ISSUE → go to Case 2
│   │   └─ Messages > 0 → RUNTIME ISSUE → go to Case 3
│   └─ NO → CONNECTION ISSUE → go to Case 1
│
└─ Agent exists in platform?
    ├─ YES → Follow Case 1
    └─ NO → Full setup needed (see pa-onboarding skill)
```

---

## Case 1 — Connection Issue (WhatsApp not linked)

**Symptom:** Dashboard shows disconnected or no channel configured.

**Fix:**
1. Open agent settings in OpenClaw platform
2. Go to Channels → WhatsApp → click **Connect** or **Re-link**
3. Scan the QR code with WhatsApp Business app
4. Confirm the phone number matches
5. Wait 30 seconds for status to update

**Most common cause:** WhatsApp session expired (happens after ~14 days of inactivity or after a phone restart).

---

## Case 2 — Ingest Issue (Connected but Messages = 0)

**Symptom:** Dashboard shows "Connected and listening" but message count stays at 0.

**Meaning:** WhatsApp is connected at protocol level, but messages are not reaching the agent runtime.

**Fix:**

```bash
# Step 1: Check gateway status
openclaw gateway status

# Step 2: Restart the gateway
openclaw gateway restart

# Step 3: Send a test message, wait 30 seconds

# Step 4: If count is still 0, check gateway logs
openclaw gateway logs --last 50
```

**What to look for in logs:**
- `binding failed`
- `session dropped`
- `ingest error`

If any of these appear → escalate to platform admin. This is an infrastructure issue.

---

## Case 3 — Runtime Issue (Messages arriving, no reply)

**Symptom:** Message count increments, but agent doesn't respond.

**Meaning:** Messages reach the agent, but the agent runtime is failing.

**Fix:**

```bash
# Step 1: Check for billing errors in agent log
grep -i "billing\|402\|credits" ~/.openclaw/logs/agent.log | tail -20
# If billing error found → see billing-monitor skill

# Step 2: Check agent status
openclaw status

# Step 3: Verify API key (pick your provider below)

# For Anthropic:
curl -s -o /dev/null -w "%{http_code}" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  https://api.anthropic.com/v1/models

# For OpenAI:
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models

# For Google:
curl -s -o /dev/null -w "%{http_code}" \
  "https://generativelanguage.googleapis.com/v1beta/models?key=$GOOGLE_API_KEY"

# Expected: 200. If 401 → invalid key. If 402 → billing error.

# Step 4: Check recent runtime errors
openclaw logs --last 100 | grep -i error
```

**Interpret results:**
- `200` → API key is valid. Problem is elsewhere (check Step 4).
- `401` → Invalid API key. Update the key in agent settings.
- `402` → Billing error. Follow the billing-monitor skill.

---

## Quick Health Check Script

```bash
#!/bin/bash
# whatsapp-health-check.sh
# Run this when the agent is unresponsive to get a quick status overview.

echo "=== WhatsApp Diagnostics ==="

# Check gateway status
echo -n "Gateway: "
openclaw gateway status 2>&1 | grep -o "running\|stopped\|error" | head -1 || echo "unknown"

# Check API key — detect provider from env vars
echo -n "API key: "

if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
  PROVIDER="Anthropic"
  # Test with a minimal request to the models endpoint
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "x-api-key: ${ANTHROPIC_API_KEY}" \
    -H "anthropic-version: 2023-06-01" \
    https://api.anthropic.com/v1/models 2>/dev/null)

elif [ -n "${OPENAI_API_KEY:-}" ]; then
  PROVIDER="OpenAI"
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer ${OPENAI_API_KEY}" \
    https://api.openai.com/v1/models 2>/dev/null)

elif [ -n "${GOOGLE_API_KEY:-}" ]; then
  PROVIDER="Google"
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    "https://generativelanguage.googleapis.com/v1beta/models?key=${GOOGLE_API_KEY}" 2>/dev/null)

else
  echo "⚠️ no API key env var found"
  PROVIDER=""
  STATUS=""
fi

# Interpret the HTTP status code
if [ -n "$STATUS" ]; then
  case $STATUS in
    200) echo "✅ valid ($PROVIDER)" ;;
    401) echo "❌ invalid key ($PROVIDER)" ;;
    402) echo "⚠️ billing error ($PROVIDER) — see billing-monitor skill" ;;
    *)   echo "? HTTP $STATUS ($PROVIDER)" ;;
  esac
fi

# Count recent errors in agent logs
echo -n "Recent errors: "
ERROR_COUNT=$(openclaw logs --last 100 2>/dev/null | grep -ic error || echo 0)
echo "$ERROR_COUNT found"

echo "=== Done ==="
```

---

## When to Escalate to Platform Admin

Escalate if:
- Gateway restart does NOT fix Messages = 0
- Logs show `socket`, `binding`, or `session` errors
- Multiple agents on the same server are affected at the same time

Include in your escalation message:
- Agent name and phone number
- Time the issue started
- Output of `openclaw gateway status`
- Messages count shown in dashboard

---

## Prevention

| Action | Why |
|---|---|
| Send at least one message every 7 days | Prevents WhatsApp session expiry |
| Check Messages count during heartbeat | Catches ingest issues early |
| Keep the phone number on record | Needed for QR re-linking |
| Don't use the same number on two devices | WhatsApp only allows one active session |

---

## Cost Tips

- **Very cheap:** All diagnostics use CLI + curl — no LLM tokens needed
- **Small model OK:** Any model can follow this decision tree and interpret curl output
- **Avoid:** Don't run diagnostics on every heartbeat — only run when the agent is not responding
- **Batch:** Run the Quick Health Check script once to get all info, rather than running each check separately
