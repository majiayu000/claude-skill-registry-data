---
name: follow-up-engine
description: >
  Determines all follow-up actions due today across the 10-day outreach cadence.
  Generates content and delivers automatically via Chrome DevTools MCP.
  Sends Telegram confirmation after completion.
tags: [outreach, follow-up, cadence, chrome-devtools, automated]
---

# Follow-Up Engine

Processes all leads in an active outreach cadence and executes the actions due today. Each follow-up adds new value -- never repeats the same angle.

## Prerequisites

- `agency.config.json` populated (outreach cadence, tools)
- Leads in CRM with stage = CONTACTED and active cadence

## Capabilities Used

1. `cold-email-drafter` -- follow-up emails (Touch 2-4)
2. `message-generator` -- LinkedIn messages, Instagram DMs
3. `crm-writer` -- update CRM, add to call sheet

## Phase 0: Intake

Read `agency.config.json`:
- `outreach.company_cadence` -- 10-day action map for company leads
- `outreach.gig_cadence` -- 2-day action map for gig leads
- `tools.browser_automation` -- Chrome DevTools MCP config
- `notifications` -- Telegram bot config

Query CRM for leads where:
- Stage = CONTACTED
- `next_action_date` <= today
- `response_received` != "Yes" (skip responded leads)

## Phase 1: Classify Actions

For each company lead, determine today's action:

| Day | Action |
|-----|--------|
| Day 1 | EMAIL_1 + IG_ENGAGE |
| Day 2 | LINKEDIN_CONNECT (personalized note) |
| Day 3 | CALL_1 (first call) |
| Day 4 | EMAIL_2 (new pain point angle) |
| Day 5 | CALL_2 + IG_DM_FOLLOWUP |
| Day 6 | REST |
| Day 7 | EMAIL_3 (Kibi Sports case study) |
| Day 8 | LINKEDIN_MSG (if accepted) + CALL_3 |
| Day 9 | REST |
| Day 10 | EMAIL_BREAKUP ("not a priority, thanks") |

For gig leads:

| Day | Action |
|-----|--------|
| Day 1 | PLATFORM_APPLY |
| Day 3 | EMAIL_1 (if email found) |

Group by action type:
- Emails to send (Touch 2, 3, or breakup)
- LinkedIn messages
- Instagram follow-ups
- Calls to schedule

## Phase 2: Generate Follow-Up Content

### Email Follow-Ups (Company Leads)

| Cadence Day | Touch | Angle |
|------------|-------|-------|
| Day 4 | Touch 2 | New pain point (NOT a "bump"). Different from Email 1 |
| Day 7 | Touch 3 | Kibi Sports case study + Plasho's work |
| Day 10 | Breakup | "Looks like this isn't a priority right now. Thanks for your time. If things change, we're here." |

Each follow-up MUST:
- Add new value (different angle from previous touches)
- Reference something new (not repeat Touch 1 content)
- Be shorter than Touch 1 (40-60 words for Touch 2-3, 30-50 for breakup)
- Thread on the original email (same subject line with "Re:")

### LinkedIn Messages (Day 8)

For leads where connection was accepted:
- Send a value message referencing something from their profile or recent activity
- Keep it conversational, not salesy

For leads where connection was NOT accepted:
- No action. Skip entirely. Do not re-request.

### Instagram Follow-Ups

For Day 5 Instagram follow-up:
- Reference the Day 1 DM or engagement
- Keep casual and brand-relevant
- Under 2 sentences

### Call Sheet Updates

For Day 3, Day 5, and Day 8:
- Add lead to `crm.tabs.calling` with:
  - Contact name, company, LinkedIn URL
  - Call purpose (Initial / Follow-up)
  - Brief talking points
  - Previous touchpoint summary

## Phase 3: Automated Delivery

No approval gate. All follow-ups are delivered automatically via Chrome DevTools MCP.

### Email Delivery
- `mcp__chrome-devtools__navigate_page` -> Zoho webmail
- Compose reply in thread (Re: original subject)
- Send automatically

### LinkedIn Delivery
- `mcp__chrome-devtools__navigate_page` -> LinkedIn messaging
- Send message to accepted connections
- Skip unaccepted connections

### Instagram Delivery
- `mcp__chrome-devtools__navigate_page` -> Instagram DMs
- Send follow-up DM
- Enforce 1 DM per 2 minutes spacing

### Call Delivery
- Add to CRM "Call Today" tab via `crm-writer`
- Send Telegram notification: "Call leads added to sheet"

## Phase 4: CRM Update

For each delivered follow-up, update CRM:
- `last_action` = action taken
- `last_action_date` = today
- `next_action` = next action from cadence
- `next_action_date` = calculated date (skip weekends)
- `cadence_day` = current day

For breakup emails (Day 10):
- Update stage: CONTACTED -> BREAKUP_SENT
- No next action scheduled
- Cadence is complete

## Phase 5: Telegram Confirmation

After all follow-ups are sent, send Telegram message:

"Follow-ups completed. [N] emails, [N] LinkedIn messages, [N] IG DMs sent. [N] calls added to sheet."

If no follow-ups were due: "No follow-ups due today."

## Phase 6: Summary

```
FOLLOW-UP SUMMARY -- [Date]
---
Follow-ups executed: N
- Emails sent: N (Touch 2: X, Touch 3: Y, Breakup: Z)
- LinkedIn messages: N
- Instagram DMs: N
- Added to call sheet: N

Skipped (lead responded): N
Skipped (LinkedIn not accepted, Day 8): N
Leads at breakup: N (cadence complete)

Telegram notification: Sent
```

## Example Usage

**Trigger phrases:**
- "Run today's follow-ups"
- "What follow-ups are due today?"
- "Process the cadence for active leads"
- "Send follow-up emails"
