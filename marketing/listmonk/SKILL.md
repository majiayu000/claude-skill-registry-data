---
name: listmonk
description: "Managing email lists, subscribers, and newsletter campaigns (create draft, test send, schedule/run, view stats) via the self-hosted Listmonk REST API."
homepage: https://listmonk.app/docs/apis/apis/
metadata:
  {
    "marketingclaw":
      {
        "emoji": "📧",
        "requires":
          { "bins": ["curl", "jq"], "env": ["LISTMONK_URL", "LISTMONK_USER", "LISTMONK_TOKEN"] },
        "primaryEnv": "LISTMONK_TOKEN",
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "jq",
              "bins": ["jq"],
              "label": "Install jq (brew)",
            },
          ],
      },
  }
---

# Listmonk Skill

Listmonk is a self-hosted newsletter/mailing-list manager. This skill covers lists, subscribers,
and campaigns over its REST API with HTTP Basic auth.

## Hard rule: draft → test → approval → run

**A campaign is never set to `running` without an explicit human go-ahead.** Every campaign you
create starts as `draft` (Listmonk's default for new campaigns). Before asking for approval,
send at least one test email to a real inbox you control. Only after the human explicitly
approves may you flip status to `scheduled` (with `send_at`) or `running`. Never skip the test
send, and never chain straight from "draft this campaign" into sending it.

## Setup

1. Log into your Listmonk admin UI → Settings → Users → create an API user, or use an existing
   admin user.
2. Admin → Users → generate an API token for that user.
3. Set environment variables:
   ```bash
   export LISTMONK_URL="https://newsletter.example.com"
   export LISTMONK_USER="api-user"          # the Listmonk username tied to the token
   export LISTMONK_TOKEN="your-api-token"
   ```

All requests use HTTP Basic auth: `curl -u "$LISTMONK_USER:$LISTMONK_TOKEN"`.

## Lists

```bash
# List all lists
curl -s -u "$LISTMONK_USER:$LISTMONK_TOKEN" "${LISTMONK_URL%/}/api/lists" | jq '.data.results[] | {id, name, subscriber_count}'

# Create a list
curl -s -u "$LISTMONK_USER:$LISTMONK_TOKEN" -X POST "${LISTMONK_URL%/}/api/lists" \
  -H "Content-Type: application/json" \
  -d '{"name": "Product Updates", "type": "public", "optin": "single"}' | jq
```

## Subscribers

```bash
# Search subscribers (SQL-ish query against the subscribers table)
curl -s -u "$LISTMONK_USER:$LISTMONK_TOKEN" \
  "${LISTMONK_URL%/}/api/subscribers?query=subscribers.email%20LIKE%20%27%25@acme.com%27" | jq '.data.results[] | {id, email, name}'

# Add a subscriber to list(s)
curl -s -u "$LISTMONK_USER:$LISTMONK_TOKEN" -X POST "${LISTMONK_URL%/}/api/subscribers" \
  -H "Content-Type: application/json" \
  -d '{"email": "person@example.com", "name": "Person Name", "lists": [1], "status": "enabled"}' | jq

# Update a subscriber (partial update — PATCH changes only the fields you send).
# Caution: use PATCH, not PUT — PUT requires the full subscriber object, and a partial
# PUT clears every omitted field (silently dropping all list subscriptions).
curl -s -u "$LISTMONK_USER:$LISTMONK_TOKEN" -X PATCH "${LISTMONK_URL%/}/api/subscribers/SUBSCRIBER_ID" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Name", "lists": [1, 2], "status": "enabled"}' | jq

# Delete a subscriber
curl -s -u "$LISTMONK_USER:$LISTMONK_TOKEN" -X DELETE "${LISTMONK_URL%/}/api/subscribers/SUBSCRIBER_ID"
```

## Campaigns: draft → test → approve → run

```bash
# 1. Create the campaign — always lands as status=draft
curl -s -u "$LISTMONK_USER:$LISTMONK_TOKEN" -X POST "${LISTMONK_URL%/}/api/campaigns" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "July product update",
    "subject": "Here'\''s what shipped this month",
    "lists": [1],
    "type": "regular",
    "content_type": "richtext",
    "body": "<p>Hello {{ .Subscriber.Name }}, here is what shipped...</p>"
  }' | jq
# => note the returned "id"

# 2. Send a test to yourself/team BEFORE asking for approval.
#    The test endpoint takes the FULL campaign payload (same fields as create) plus subscribers.
curl -s -u "$LISTMONK_USER:$LISTMONK_TOKEN" -X POST "${LISTMONK_URL%/}/api/campaigns/CAMPAIGN_ID/test" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "July product update",
    "subject": "Here'\''s what shipped this month",
    "lists": [1],
    "type": "regular",
    "content_type": "richtext",
    "body": "<p>Hello {{ .Subscriber.Name }}, here is what shipped...</p>",
    "subscribers": ["you@example.com"]
  }' | jq

# 3. STOP — show the draft + test result to the human, wait for explicit approval.

# 4a. Once approved, schedule for later. There is no PATCH — PUT /api/campaigns/{id} REPLACES
#     the whole campaign, so NEVER PUT a partial body (just send_at) or it blanks name/subject/
#     body/lists. Fetch the full campaign, add send_at, and PUT it all back. GET returns lists
#     as {id,name} objects but PUT wants list ids, so map them. (Simplest alternative: set
#     send_at directly in the step-1 create payload.)
BODY=$(curl -s -u "$LISTMONK_USER:$LISTMONK_TOKEN" "${LISTMONK_URL%/}/api/campaigns/CAMPAIGN_ID" \
  | jq '.data | (.lists |= map(.id)) + {send_at: "2026-07-15T14:00:00Z"}')
curl -s -u "$LISTMONK_USER:$LISTMONK_TOKEN" -X PUT "${LISTMONK_URL%/}/api/campaigns/CAMPAIGN_ID" \
  -H "Content-Type: application/json" -d "$BODY" | jq
curl -s -u "$LISTMONK_USER:$LISTMONK_TOKEN" -X PUT "${LISTMONK_URL%/}/api/campaigns/CAMPAIGN_ID/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "scheduled"}' | jq

# 4b. Or, once approved, send immediately:
curl -s -u "$LISTMONK_USER:$LISTMONK_TOKEN" -X PUT "${LISTMONK_URL%/}/api/campaigns/CAMPAIGN_ID/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "running"}' | jq
```

Valid status transitions: `draft` → `scheduled` or `running`; `running` → `paused`/`cancelled`;
`scheduled` → `draft`. Only `draft` and `paused` campaigns can start running.

## Campaign stats

```bash
# Live counters for a running/finished campaign
curl -s -u "$LISTMONK_USER:$LISTMONK_TOKEN" \
  "${LISTMONK_URL%/}/api/campaigns/running/stats?campaign_id=CAMPAIGN_ID" | jq

# Views / link clicks / bounces over a date range
curl -s -u "$LISTMONK_USER:$LISTMONK_TOKEN" \
  "${LISTMONK_URL%/}/api/campaigns/analytics/views?id=CAMPAIGN_ID&from=2026-07-01T00:00:00Z&to=2026-07-31T23:59:59Z" | jq
```

## Notes

- `content_type` can be `richtext`, `html`, `markdown`, or `plain`; `body` must match it.
- Campaigns need at least one target list (`lists: [id, ...]`); use the Lists section above to
  find or create list ids.
- **Verify on first use**: analytics sub-endpoint names (`views`/`links`/`clicks`/`bounces`) and
  exact response shapes can shift between Listmonk versions — confirm against
  `https://listmonk.app/docs/apis/campaigns/` for the instance's installed version.
- Never log or paste `$LISTMONK_TOKEN` into chat.
