---
name: inbox-scanner
description: >
  Check all outreach channels for replies using Chrome DevTools MCP.
  Scans Zoho webmail, LinkedIn messaging, and Instagram DMs.
tags: [inbox, responses, email, monitoring, chrome-devtools]
---

# Inbox Scanner

Checks email, LinkedIn, and Instagram inboxes for replies to outreach messages. Matches responses against the CRM outreach log to provide full lead context. Used by the `evening-scan` playbook as the first step before `reply-analyzer`.

## Prerequisites

- `agency.config.json` at repo root with `tools.email_sending`, `tools.linkedin_outreach`, `tools.instagram_outreach`
- `crm-writer` skill for matching responses to CRM leads
- For browser path: Chrome DevTools MCP available (`mcp__chrome-devtools__*`)
- Chrome Beta logged in: Zoho webmail, LinkedIn, Instagram

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `tools.email_sending` -- provider, access method, domains
   - `tools.linkedin_outreach` -- provider, access method
   - `tools.instagram_outreach` -- provider, access method
   - `tools.browser_automation` -- Chrome DevTools MCP config
   - `tools.inbox_scanning` -- inbox scanning config
   - `crm.tabs.outreach_log` -- tab name for matching replies to sent outreach
   - `crm.tabs.pipeline` -- tab name for lead pipeline data
3. Accept parameters:
   - `channels` -- list of channels to check (default: `["email", "linkedin", "instagram"]`, i.e., all)
   - `time_window` -- how far back to scan (default: `"24h"`)

## Phase 1: Check Email

### Chrome DevTools MCP (Zoho webmail)

Use Chrome DevTools MCP to scan Zoho webmail inbox:

1. `mcp__chrome-devtools__navigate_page` to Zoho webmail inbox
2. `mcp__chrome-devtools__wait_for` inbox to load
3. `mcp__chrome-devtools__take_snapshot` to read recent emails
4. Look for replies to outreach emails (matching subject lines, sender addresses)
5. For each reply:
   - `mcp__chrome-devtools__click` to open the email
   - `mcp__chrome-devtools__take_snapshot` to read reply content
   - Extract: sender name, sender email, subject, reply text, timestamp

### Backup: Gmail MCP

If Chrome DevTools MCP is unavailable for Zoho, fall back to Gmail MCP:
- Search Gmail for replies (last 24 hours)
- Use BODY.PEEK[] to preserve read/unread status

### API Path (access: "api")

For Smartlead, Instantly, or other email platforms with API access:

1. Query the platform's campaign reply endpoint using the API key from the env var specified in `tools.email_sending.api_key_env`.
2. For Smartlead: `GET /api/v1/campaigns/{id}/replies`
3. For Instantly: `GET /api/v1/campaign/replies`
4. Filter by `time_window`.
5. Extract: sender name, sender email, reply text, campaign name, timestamp.

### Manual Path (access: "manual")

Ask the user directly:

```
Any email replies since the last scan?
Paste them here, or list the companies/contacts that responded.
Format: Company Name - Contact Name - brief summary of their reply
```

Collect and structure whatever the user provides.

## Phase 2: Check LinkedIn

### Chrome DevTools MCP

1. `mcp__chrome-devtools__navigate_page` to `https://www.linkedin.com/messaging/`
2. `mcp__chrome-devtools__wait_for` messaging inbox to load
3. `mcp__chrome-devtools__take_snapshot` to read recent messages
4. For each new message from an outreach contact:
   - Extract: sender name, sender headline/company, message text, timestamp
5. Check connection request acceptances:
   - `mcp__chrome-devtools__navigate_page` to `https://www.linkedin.com/mynetwork/invitation-manager/sent/`
   - `mcp__chrome-devtools__take_snapshot` to read accepted requests

### Manual Path (access: "manual")

Ask the user:

```
Any LinkedIn responses since the last scan?
- New messages from outreach contacts?
- Connection requests accepted?
Format: Name - Company - what they said (or just "accepted connection")
```

## Phase 3: Check Instagram

### Chrome DevTools MCP

1. `mcp__chrome-devtools__navigate_page` to `https://www.instagram.com/direct/inbox/`
2. `mcp__chrome-devtools__wait_for` DM inbox to load
3. `mcp__chrome-devtools__take_snapshot` to read recent DMs
4. For each new DM from an outreach contact:
   - Extract: sender username, sender display name, message text, timestamp
5. Skip: story reactions, emoji-only replies, automated responses

### Manual Path (access: "manual")

Ask the user:

```
Any Instagram DM replies since the last scan?
Format: @username (Company) - what they said
```

## Phase 4: Match to CRM

For each response found across all channels:

1. Use `crm-writer` (READ operation) to query the outreach log tab (`crm.tabs.outreach_log`).
2. Match the response to an existing lead using these strategies (in order of reliability):
   - **Email address** (exact match) -- most reliable for email replies
   - **Company name** (fuzzy match, case-insensitive, strip Ltd/Inc/LLC) -- for LinkedIn/Instagram where email may not be visible
   - **Contact name** (fuzzy match) -- fallback, combine with company for higher confidence
3. For each matched lead, pull context from the CRM:
   - `cadence_day` -- which day in the outreach cadence they are on
   - `last_action` -- what was the last outreach action (e.g., "EMAIL_1", "LINKEDIN_CONNECT")
   - `lead_status` -- current status (e.g., "CONTACTED", "FOLLOW_UP")
   - `tier` -- lead tier/temperature (e.g., "HOT", "WARM", "COLD")
   - `score` -- lead score if available
4. If no CRM match is found:
   - Mark `crm_match` as `null`
   - Flag as "unmatched response" for manual review
   - Still include in the output

## Phase 5: Output

Return a structured JSON array of all responses found:

```json
[
  {
    "channel": "email",
    "from_name": "Sarah Chen",
    "from_email": "sarah@brandx.com",
    "company": "Brand X",
    "reply_text": "Hey, this sounds interesting. What are your rates for a CRO audit?",
    "timestamp": "2024-01-15T14:30:00Z",
    "thread_subject": "Re: Quick question about your Shopify store",
    "crm_match": {
      "lead_id": "row_42",
      "cadence_day": 4,
      "last_action": "EMAIL_2",
      "lead_status": "CONTACTED",
      "tier": "HOT",
      "score": 72
    }
  },
  {
    "channel": "linkedin",
    "from_name": "Rahul Kapoor",
    "from_email": null,
    "company": "FreshFit Foods",
    "reply_text": "Thanks for connecting! Yes, we are actually looking at revamping our Shopify store.",
    "timestamp": "2024-01-15T11:20:00Z",
    "thread_subject": null,
    "crm_match": {
      "lead_id": "row_67",
      "cadence_day": 2,
      "last_action": "LINKEDIN_CONNECT",
      "lead_status": "CONTACTED",
      "tier": "WARM",
      "score": 55
    }
  },
  {
    "channel": "instagram",
    "from_name": "Active Gear",
    "from_email": null,
    "company": "Active Gear",
    "reply_text": "Not interested right now, thanks.",
    "timestamp": "2024-01-15T16:45:00Z",
    "thread_subject": null,
    "crm_match": null
  }
]
```

Print a summary line:

```
Inbox Scan Complete (last 24h):
- Email replies: 3
- LinkedIn messages: 1
- LinkedIn connections accepted: 2
- Instagram DM replies: 1
- Total responses: 7
- Matched to CRM leads: 5
- Unmatched (manual review needed): 2
```

## Example Usage

Trigger phrases:
- "Check inboxes for replies"
- "Scan all channels for responses"
- "Any replies today?"
- "Run inbox scanner"
- "Check email and LinkedIn for responses"

```
User: Check all inboxes for replies
Assistant: [reads config, checks Zoho webmail via Chrome DevTools MCP, checks LinkedIn via Chrome DevTools MCP, checks Instagram via Chrome DevTools MCP, matches all replies to CRM leads, returns structured array with summary]
```

```
User: Just check email, skip LinkedIn and Instagram
Assistant: [same flow but channels=["email"] only]
```
