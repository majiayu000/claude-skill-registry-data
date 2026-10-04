---
name: morning-pipeline
description: >
  Full daily sales pipeline execution. Run at 9 AM via cron. Scans for signals,
  enriches company leads, auto-applies to gigs, runs multi-channel outreach,
  processes follow-ups. All delivery automated via Chrome DevTools MCP.
tags: [daily, pipeline, playbook, automation, chrome-devtools]
---

# Morning Pipeline

The daily sales engine. Runs at 9 AM via cron. Orchestrates the full pipeline: inbox pre-scan, signal detection, enrichment, automated outreach, follow-ups, and calling list.

**Daily Target**: 5 company leads + 20 gig leads = 25 total leads/day
**Geo Split**: 75% US/UK/AU/EU, 25% India
**Delivery**: All automated via Chrome DevTools MCP (`mcp__chrome-devtools__*`)

## Prerequisites

- `agency.config.json` fully populated (run `/agency-setup` first)
- CRM initialized (run `/crm-setup` first)
- Chrome Beta logged in: Apollo.io, Snov.io, Lemlist, LinkedIn, Instagram, Zoho webmail
- Chrome DevTools MCP available

## Composites & Capabilities Used

1. `inbox-scanner` -- pre-scan for overnight replies
2. `reply-analyzer` -- classify any replies found
3. `signal-scanner` -- find and score new leads (reads keywords from config)
4. `lead-scorer` -- score with separate gig vs company criteria
5. `company-researcher` -- research company leads (includes LinkedIn URL)
6. `cro-auditor` -- CRO + AI audit for company leads
7. `decision-maker-finder` -- find 5 DMs per company via Apollo UI (Chrome DevTools MCP)
8. `email-validator` -- validate emails via Snov.io (Chrome DevTools MCP)
9. `phone-finder` -- get phone numbers via Lemlist (Chrome DevTools MCP)
10. `personalization-enricher` -- build personalization packets
11. `cold-email-drafter` -- generate emails with super catchy subject lines
12. `message-generator` -- LinkedIn notes, Instagram DMs, call scripts
13. `outreach-draft-pipeline` -- route and deliver all outreach (no approval gate)
14. `follow-up-engine` -- process today's follow-ups (10-day cadence)
15. `crm-writer` -- update CRM throughout

---

## Phase 0: Morning Briefing + Inbox Pre-Scan

### Step 0.1: Read CRM Dashboard

SKILL: `crm-writer` (READ)
TOOL: Google Sheets webhook

Read CRM dashboard and present:
```
MORNING BRIEFING -- [Date]
---
Pipeline snapshot:
- Total active leads: N
- NEW (awaiting enrichment): N
- OUTREACH_READY (awaiting outreach): N
- CONTACTED (in cadence): N
- REPLIED (need attention): N
- DEMO_BOOKED: N

Today's targets:
- Company leads to find: 5
- Gig leads to find: 20
- Follow-ups due: N leads
- Calls due: N leads
```

### Step 0.2: Inbox Pre-Scan (6 PM yesterday to 9 AM today)

SKILL: `inbox-scanner`
TOOL: Chrome DevTools MCP (Zoho webmail, LinkedIn, Instagram) + Zoho MCP (being integrated)
AUTH: All logged in via Chrome Beta

Check email, LinkedIn, and Instagram for any overnight replies:
1. Use `mcp__chrome-devtools__navigate_page` to Zoho webmail, scan for new replies
2. Use `mcp__chrome-devtools__navigate_page` to LinkedIn messaging, scan for new messages
3. Use `mcp__chrome-devtools__navigate_page` to Instagram DMs, scan for new DMs

If replies found:
- Run `reply-analyzer` to classify sentiment
- Update CRM via `crm-writer`: set `response_received = "Yes"`, pause cadence
- This prevents follow-up-engine from messaging leads who already replied overnight

**Output**: CRM has up-to-date response statuses before follow-ups run.

---

## Phase 1: Signal Scan

### Step 1.1: Generate Search Queries FROM agency.config.json

SKILL: `signal-scanner`
TOOL: None (reads config, generates queries)

Read `agency.config.json` for current keywords and positioning. Queries MUST come from config, not hardcoded. When Plasho's positioning changes week-to-week, queries change automatically because they're derived from config keywords.

### Step 1.2: Execute Searches with Geo Split + Lead Type Targeting

SKILL: `signal-scanner`
TOOL: WebSearch

Search across all configured platforms with these constraints:

```
DAILY TARGET
- 20 gig leads (Freelancer, Upwork, PeoplePerHour, Guru, Fiverr)
- 5 company leads (LinkedIn, Reddit, funding news, Product Hunt, etc.)
= 25 total leads/day

GEO SPLIT
- 75% from US / UK / AU / EU (~19 leads)
- 25% from India (~6 leads)

QUALITY BAR
- Gig leads: must be HOT (clear buying signal, budget)
- Company leads: must be VERY HOT (strong signal + fit)
```

### Step 1.3: Score Each Signal

SKILL: `lead-scorer`

Separate scoring for gig leads vs company leads:
- Company leads: extremely high bar (only 5/day, must be truly hot)
- Gig leads: high bar but more volume (20/day)
- Enforce 75/25 geo split in output (not just scoring boost)

### Step 1.4: Dedup Against Existing CRM Leads

SKILL: `crm-writer` (READ) + `signal-scanner`
TOOL: Google Sheets webhook

### Step 1.5: Write HOT Leads to CRM

SKILL: `crm-writer` (APPEND to "Pipeline" tab)
TOOL: Google Sheets webhook

Only truly HOT leads make it. 25 total (20 gig + 5 company).

**Output**: CRM has 25 NEW leads (20 gig + 5 company, 75/25 geo split)

---

## Phase 2: Enrichment (Company Leads Only)

Gig leads skip to Phase 3. Only the 5 company leads go through enrichment.

### Step 2.1: Company Research (Include LinkedIn URL)

SKILL: `company-researcher`
TOOL: WebSearch

Must include the company's LinkedIn page URL in output.

### Step 2.2: CRO + AI Audit

SKILL: `cro-auditor` (updated)
TOOL: WebSearch + Chrome DevTools MCP (screenshots)

Dual audit:

**PART 1: CRO AUDIT**
- Conversion issues on their Shopify store
- Product page, navigation, checkout friction
- Standard CRO findings

**PART 2: AI AUDIT**
- Based on publicly visible data, what can they automate?
- AI recommendations for their store (AI-powered product recs, chatbot, workflow automation, Claude-based systems)
- "Here's what we can set up for you using Claude + AI"
- Focused on their specific market/vertical

**CRM UPDATE**: Stage NEW → RESEARCHED

### Step 2.3: Find 5 Decision Makers per Company

SKILL: `decision-maker-finder`
TOOL: Chrome DevTools MCP ONLY (Apollo.io UI in Chrome Beta)
AUTH: Already signed in via Chrome Beta

1. `mcp__chrome-devtools__navigate_page` to Apollo.io
2. Search for people at [company name]
3. Filter by ICP titles (Founder, CEO, Head of Ecomm, etc.)
4. Pick 5 decision makers per company
5. DO NOT enrich on Apollo (no credits used)
6. Export the list (they already have LinkedIn profile URLs)

**Output**: 5 companies x 5 people = ~25 decision makers
Each with: name, title, company, LinkedIn URL

### Step 2.4: Email Validation via Snov.io LinkedIn Search

SKILL: `email-validator`
TOOL: Chrome DevTools MCP ONLY (Snov.io UI, already logged in)

**CRITICAL: Use Snov.io LinkedIn Search (app.snov.io/linkedin/search) with each person's LinkedIn profile URL. Snov.io returns the actual verified email from the profile. NEVER guess email patterns.**

For each decision maker from Step 2.3:
1. Navigate to `https://app.snov.io/linkedin/search`
2. Paste the person's LinkedIn profile URL (e.g. `https://www.linkedin.com/in/chris-ferguson-80b98b79`)
3. Click search -- Snov.io finds and verifies the real email
4. Record the verified email (green dot = valid)
5. Repeat for all contacts

Threshold: at least 3 verified emails per company.
If < 3 verified emails: FLAG AS RED on CRM sheet.

**NEVER send emails without Snov.io verification. NEVER guess from domain patterns.**

**Output**: Verified emails mapped to each contact

### Step 2.5: Get Phone Numbers via Lemlist

SKILL: `phone-finder`
TOOL: Chrome DevTools MCP ONLY (Lemlist UI)

1. Upload LinkedIn profile list to Lemlist via Chrome DevTools MCP
2. Lemlist returns phone numbers where available
3. Populate phone numbers back into CRM Pipeline tab

**Output**: Phone numbers added to CRM for contacts that have them

**CRM UPDATE**: Stage RESEARCHED → ENRICHED → OUTREACH_READY

### Step 2.6: Build Personalization Packets

SKILL: `personalization-enricher`
TOOL: WebSearch

**Output**: 5 company leads are OUTREACH_READY with contacts, emails, phones, CRO+AI findings, personalization packets

---

## Phase 3: Outreach (Automated, No Approval Gates)

### Step 3.1: Route Leads by Type

SKILL: `outreach-draft-pipeline`

```
GIG LEADS (20/day): 2-day cadence
  Day 1: AUTO-APPLY on gig platform via Chrome DevTools MCP
         (navigate to gig page, fill proposal form, submit automatically)
  Day 3: Email if we found their email/company

COMPANY LEADS (5/day): Full 10-day cadence
  Only company leads use the email cadence.
  Email volume: ~5 new + follow-ups = well under Zoho 50/day webmail limit.
```

### Step 3.2: Generate Cold Emails (Super Catchy Subject Lines)

SKILL: `cold-email-drafter`
TOOL: None (LLM generation)

Subject lines must be SUPER catchy. Short, attention-grabbing, curiosity-driven.

### Step 3.3: Generate LinkedIn Notes

SKILL: `message-generator` (linkedin-note)

### Step 3.4: Generate Instagram DMs

SKILL: `message-generator` (instagram-dm)

### Step 3.5: Generate Call Scripts

SKILL: `message-generator` (call-script)

**NO APPROVAL GATE. All content generated and sent automatically.**

### Step 3.6: DELIVER Email (Automated)

SKILL: `outreach-draft-pipeline`
TOOL: Chrome DevTools MCP → Zoho webmail (already logged in)

Compose email in Zoho webmail via Chrome DevTools MCP, send it. No manual copy-paste. Fully automated.

### Step 3.7: DELIVER LinkedIn Connection Requests (Automated)

SKILL: `outreach-draft-pipeline`
TOOL: Chrome DevTools MCP → LinkedIn (already logged in)

Send connection request with personalized note via Chrome. No Dripify. No CSV export. Direct browser automation.

### Step 3.8: DELIVER Instagram DMs (Automated, 1 DM per 2 min)

SKILL: `outreach-draft-pipeline`
TOOL: Chrome DevTools MCP → Instagram (already logged in)

Send DM via Instagram web. Enforce 1 DM per 2 minutes spacing.

### Step 3.9: DELIVER Calls → CRM Sheet + Telegram Notification

SKILL: `crm-writer` (APPEND to "Call Today")
TOOL: Google Sheets webhook + Telegram Bot API

Populate calling sheet, then send Telegram message:
"Your call leads are ready for the day. [N] calls scheduled."

### Step 3.10: Save to CRM (After Sending)

SKILL: `crm-writer` (APPEND to "Outreach CRM" + UPDATE "Pipeline")
TOOL: Google Sheets webhook

Log all sent outreach, update stage to CONTACTED, set cadence_day=1, next_action, next_action_date.

**Output**: All Day 1 outreach sent automatically. Telegram notification sent.

---

## Phase 4: Follow-Ups (Leads Already in Cadence)

Phase 0.2 already ran inbox pre-scan, so response_received is up-to-date before follow-ups run.

### Step 4.1: Query CRM for Leads Due Today

SKILL: `crm-writer` (READ)
TOOL: Google Sheets webhook

Query: stage = CONTACTED, next_action_date ≤ today, response_received ≠ "Yes"

### Step 4.2: Classify by Cadence Day (10-Day Company Cadence)

SKILL: `follow-up-engine`

| Day | Action |
|-----|--------|
| Day 1 | EMAIL_1 + IG_ENGAGE |
| Day 2 | LINKEDIN_CONNECT (personalized note) |
| Day 3 | CALL_1 (first call) |
| Day 4 | EMAIL_2 (new angle) |
| Day 5 | CALL_2 + IG_DM_FOLLOWUP |
| Day 6 | REST |
| Day 7 | EMAIL_3 (Kibi Sports case study) |
| Day 8 | LINKEDIN_MSG (if accepted) + CALL_3 |
| Day 9 | REST |
| Day 10 | EMAIL_BREAKUP ("not a priority, thanks") |

### Step 4.3: Generate Follow-Up Content

SKILL: `cold-email-drafter` + `message-generator`

Key angles:
- Email 2 (Day 4): New pain point, different from Email 1
- Email 3 (Day 7): Kibi Sports case study + Plasho's work
- Breakup (Day 10): "Looks like this isn't a priority right now. Thanks for your time. If things change, we're here."
- LinkedIn msg (Day 8): Only if they accepted connection. If not accepted, skip.

### Step 4.4: DELIVER Follow-Ups (Automated)

TOOL: Chrome DevTools MCP for all channels

- Email → Chrome DevTools MCP → Zoho webmail (auto send)
- LinkedIn → Chrome DevTools MCP → LinkedIn (auto send)
- Instagram → Chrome DevTools MCP → Instagram (1 per 2 min)
- Calls → CRM "Call Today" tab + Telegram notification

After all follow-ups sent:
Send Telegram confirmation: "Follow-ups completed. [N] emails, [N] LinkedIn, [N] IG DMs sent. [N] calls added to sheet."

### Step 4.5: Update CRM Cadence Tracking

SKILL: `crm-writer` (UPDATE)

Bump cadence_day, set next_action + next_action_date.
Day 10 breakup → stage = BREAKUP_SENT, no more actions.

---

## Phase 5: Calling Sheet + Daily Summary

### Step 5.1: Consolidated Calling List + Telegram Notification

SKILL: `crm-writer`
TOOL: Google Sheets webhook + Telegram Bot

Build calling sheet, send Telegram: "Your call leads are ready. [N] calls for today."

### Step 5.2: Daily Summary (Text Output + Telegram)

```
MORNING PIPELINE COMPLETE -- [Date]
---
NEW LEADS:
- Signals scanned: N across M platforms
- New leads added: 25 (20 gig, 5 company)
- Geo split: X% international, Y% India

ENRICHMENT (company leads):
- Companies researched: 5
- CRO + AI audits completed: 5
- Decision makers found: N contacts (5 per company)
- Emails validated (Snov.io): N (X valid)
- Phone numbers found (Lemlist): N

OUTREACH:
- Gig applications submitted: N
- Cold emails sent (Zoho webmail): N
- LinkedIn connection requests sent: N
- Instagram DMs/engagement: N
- Call scripts generated: N

FOLLOW-UPS:
- Follow-up emails sent: N
- LinkedIn messages sent: N
- Instagram follow-up DMs: N
- Calls added to sheet: N
- Breakup emails sent: N

PIPELINE:
- Total active leads: N
- Response rate (trailing 7d): X%
- Demos booked (trailing 7d): N

NEXT: Run /evening-scan at 6 PM to check for responses
```

---

## Automation

Triggered daily at 9 AM via cron job.

## Example Usage

Trigger phrases:
- "Run the morning pipeline"
- "It's 9 AM, start the daily leads"
- "Execute the full morning flow"
- "Run today's lead gen and outreach"
