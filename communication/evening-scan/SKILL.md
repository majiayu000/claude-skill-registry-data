---
name: evening-scan
description: >
  End-of-day response check and pipeline update. Run at 6 PM via cron.
  Checks all channels for replies via Chrome DevTools MCP + Zoho MCP,
  updates lead statuses, pauses cadence for responded leads,
  sends EOD report via Telegram.
tags: [daily, responses, pipeline, playbook, chrome-devtools]
---

# Evening Scan

Run at 6 PM daily via cron. Checks all channels for responses to outreach via Chrome DevTools MCP, updates lead statuses, and sends EOD report via Telegram.

## Prerequisites

- `agency.config.json` populated (tools, CRM)
- Active leads in outreach cadence
- Chrome Beta logged in: Zoho webmail, LinkedIn, Instagram
- Chrome DevTools MCP available

## Capabilities Used

1. `inbox-scanner` -- check all channels for replies via Chrome DevTools MCP
2. `reply-analyzer` -- classify response sentiment and intent (8 categories)
3. `crm-writer` -- update statuses, pause cadences

---

## Step 1.1: Check Email Replies

SKILL: `inbox-scanner`
TOOL: Zoho MCP (being integrated) + Chrome DevTools MCP (Zoho webmail)
AUTH: Already signed in via Chrome Beta

1. `mcp__chrome-devtools__navigate_page` to Zoho webmail inbox
2. Scan for new replies to outreach emails (since last scan)
3. Extract: sender, subject, reply text, timestamp
4. Match to CRM leads by email address

## Step 1.2: Check LinkedIn Messages

SKILL: `inbox-scanner`
TOOL: Chrome DevTools MCP → LinkedIn messaging
AUTH: Already signed in via Chrome Beta

1. `mcp__chrome-devtools__navigate_page` to LinkedIn messaging
2. Scan for new/unread messages from outreach contacts
3. Check for accepted connection requests at invitation manager
4. Extract: sender name, company, message text, timestamp

## Step 1.3: Check Instagram DMs

SKILL: `inbox-scanner`
TOOL: Chrome DevTools MCP → Instagram DMs
AUTH: Already signed in via Chrome Beta

1. `mcp__chrome-devtools__navigate_page` to Instagram Direct inbox
2. Scan for new/unread DM replies
3. Extract: sender username, message text, timestamp

## Step 2.1: Match Replies to CRM Leads

SKILL: `crm-writer` (READ)
TOOL: Google Sheets webhook

Match each reply to CRM leads by:
- Email address (exact match) for email replies
- Company name (fuzzy match) for LinkedIn/Instagram
- Contact name (fuzzy match) as fallback

Pull lead context: cadence_day, last_action, lead_status, tier, score

## Step 3.1: Classify Reply Sentiment (8 Categories)

SKILL: `reply-analyzer`
TOOL: None (LLM classification)

Categories:
| Category | Action |
|----------|--------|
| Positive + wants demo | Mark DEMO_BOOKED, send cal link, pause cadence |
| Positive + interested | Mark REPLIED, send more info, pause cadence |
| Neutral + questions | Mark REPLIED, answer questions, pause cadence |
| Negative + not interested | Mark NOT_INTERESTED, send polite close, pause cadence |
| Negative + angry/rude | Mark DO_NOT_CONTACT, no further outreach |
| Out of office | Note OOO, adjust cadence timing |
| Unsubscribe request | Mark DO_NOT_CONTACT, remove from all sequences |
| Referral | Mark REFERRED, follow up with referred contact |

## Step 3.2: Update CRM -- Pause Cadence, Set New Status

SKILL: `crm-writer` (UPDATE)
TOOL: Google Sheets webhook

For each responded lead:
1. Set `response_received` = "Yes"
2. Set `response_channel` = channel
3. Set `response_date` = today
4. Set `response_summary` = summary from analyzer
5. Update `lead_status` based on classification
6. Clear `next_action` and `next_action_date` (pause cadence)
7. If demo booked: add to calendar (if Google Calendar MCP available)

## Step 3.3: EOD Report + Telegram Notification

TOOL: Telegram Bot API

Send via Telegram:
```
EOD SCAN -- [Date]
---
RESPONSES RECEIVED: N
- Email replies: N
- LinkedIn messages: N
- LinkedIn connections accepted: N
- Instagram DM replies: N

RESPONSE DETAILS:
1. [Company] via [Channel]: [Summary] → [Action Taken]
2. ...

DEMOS BOOKED TODAY: N
NOT INTERESTED: N
DO NOT CONTACT: N

PIPELINE UPDATE:
- Total active leads: N
- In cadence: N
- Responded (awaiting follow-up): N
- Demo booked (total): N
- Breakup sent: N

RESPONSE RATE (trailing 7 days):
- Emails sent: N → Replies: N (X%)
- LinkedIn sent: N → Replies: N (X%)
- Overall: X%

ACTION ITEMS FOR TOMORROW:
- Follow-ups due: N
- Calls scheduled: N
- New leads to process: N
```

## Example Usage

Trigger phrases:
- "Run the evening scan"
- "Check for responses"
- "It's 6 PM, any replies?"
- "Update the pipeline with today's responses"
