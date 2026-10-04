---
name: signl4
description: Send and close SIGNL4 alerts using the SIGNL4 inbound webhook (team secret in URL).
metadata: {"openclaw":{"emoji":"🚨","requires":{"bins":["curl"],"env":["SIGNL4_TEAM_SECRET"]},"primaryEnv":"SIGNL4_TEAM_SECRET"}}
---

## Overview
Use this skill to interact with SIGNL4 via its **inbound webhook**:

- **Send alerts** to a SIGNL4 team
- **Close (resolve) alerts** using an external correlation ID

Authentication is handled via the **team secret embedded in the webhook URL**.

Webhook documentation:
https://docs.signl4.com/integrations/webhook/webhook.html

---

## Required configuration
The following environment variable must be set:

- `SIGNL4_TEAM_SECRET` – the SIGNL4 team secret used in the webhook URL

Optional (advanced):
- `SIGNL4_WEBHOOK_BASE` – defaults to `https://connect.signl4.com/webhook`

---

## Inputs to gather from the user

### When sending an alert
Required:
- **Title** – short summary
- **Message** – detailed description
- **External ID** – strongly recommended (required to close the alert later)

Optional:
- **Service** (`X-S4-Service`)
- **Alerting scenario** (`X-S4-AlertingScenario` – e.g. `single_ack`, `multi_ack`, `emergency`)
- **Location** (`X-S4-Location`, format: `"lat,long"`)

### When closing an alert
Required:
- **External ID** – must match the ID used when the alert was created

---

## How to send an alert

### Rules
- Always include `X-S4-ExternalID` if the alert might need to be closed later.
- Use `X-S4-Status: "new"` to create an alert.

### Command template
Set the webhook URL:

```sh
WEBHOOK_URL="${SIGNL4_WEBHOOK_BASE:-https://connect.signl4.com/webhook}/${SIGNL4_TEAM_SECRET}"
```

Send the alert:

```sh
curl -sS -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "Title": "<TITLE>",
    "Message": "<MESSAGE>",
    "X-S4-ExternalID": "<EXTERNAL_ID>",
    "X-S4-Status": "new",
    "X-S4-Service": "<OPTIONAL_SERVICE>",
    "X-S4-AlertingScenario": "<OPTIONAL_SCENARIO>",
    "X-S4-Location": "<OPTIONAL_LAT_LONG>",
    "X-S4-SourceSystem": "OpenClaw"
  }'
```

### What to report back
- Confirm that the alert was sent
- Repeat key details:
  - Title
  - External ID
  - Optional service/scenario

If the request fails:
- Check that `SIGNL4_TEAM_SECRET` is set and correct
- Ensure JSON fields are valid

---

## How to close (resolve) an alert

### Rules
To close an alert, you must:
- Use the **same External ID** as when the alert was created
- Set `X-S4-Status` to `resolved`

### Command template
```sh
curl -sS -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "X-S4-ExternalID": "<EXTERNAL_ID>",
    "X-S4-Status": "resolved"
  }'
```

### What to report back
- Confirm the resolve request was sent for the given External ID
- If the External ID is missing, ask the user for it

---

## Security notes
- Treat `SIGNL4_TEAM_SECRET` as confidential
- Never print or echo the team secret in responses or logs
