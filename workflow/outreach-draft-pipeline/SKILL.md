---
name: outreach-draft-pipeline
description: >
  Generates and delivers all outreach for OUTREACH_READY leads.
  Automated delivery via Chrome DevTools MCP -- email, LinkedIn, Instagram.
  Gig leads auto-applied on platform. No approval gates.
tags: [outreach, pipeline, multi-channel, chrome-devtools, automated]
---

# Outreach Draft Pipeline

Takes OUTREACH_READY leads, generates personalized outreach, and delivers automatically via Chrome DevTools MCP. No approval gates. Gig leads are auto-applied on their platform.

## Prerequisites

- `agency.config.json` populated (outreach, tools, case studies)
- Leads in CRM with stage = OUTREACH_READY
- Personalization packets (for HOT leads, from `personalization-enricher`)

## Capabilities Used

1. `cold-email-drafter` -- generate emails (Touch 1)
2. `message-generator` -- LinkedIn notes, Instagram DMs, call scripts
3. `crm-writer` -- save drafts and update statuses

## Phase 0: Intake

Read `agency.config.json`:
- `outreach.company_cadence` -- 10-day action map for company leads
- `outreach.gig_cadence` -- 2-day action map for gig leads
- `outreach.tone`, `outreach.banned_phrases`, `outreach.sign_off`
- `case_studies` -- for proof points
- `tools.browser_automation` -- Chrome DevTools MCP config
- `notifications` -- Telegram bot config

Query CRM for leads with stage = OUTREACH_READY, sorted by score.

All delivery channels use Chrome DevTools MCP:
- Email: Chrome DevTools MCP -> Zoho webmail
- LinkedIn: Chrome DevTools MCP -> LinkedIn
- Instagram: Chrome DevTools MCP -> Instagram (1 DM per 2 min)
- Gig platforms: Chrome DevTools MCP -> platform apply form
- Calling: CRM sheet + Telegram notification

### Per-Lead Channel Merging

For each lead, merge tool availability AND lead's `contact_surfaces`.
A channel is draftable only if BOTH the tool is available AND the lead has that surface:
- Email: tool available AND (`contact_surfaces.has_email` = true OR email found during enrichment)
- LinkedIn: tool available AND `contact_surfaces.has_linkedin` = true
- Instagram: tool available AND `contact_surfaces.has_instagram` = true
- Phone: tool available AND `contact_surfaces.has_phone` = true
- Website: always usable for research, not a direct outreach channel

## Phase 1: Route by Lead Type

### Gig Leads (from gig platforms)
Route to gig application flow:
1. Auto-apply on gig platform via Chrome DevTools MCP
2. If email/company found: queue Day 3 email

### Company Leads (from non-gig platforms)
Route to full 10-day cadence:
1. Generate cold email (Touch 1) with super catchy subject line
2. Generate LinkedIn connection note
3. Generate Instagram engagement strategy
4. Generate call script

Map each lead to their personalization tier:
- HOT leads with personalization packet: Tier 3
- WARM leads with company research: Tier 2
- All others: Tier 1

## Phase 2: Generate Emails

For each lead, execute `cold-email-drafter`:
- Pass lead context + personalization tier
- For Tier 3: include CRO findings, person's posts, signal context
- For Tier 2: include industry-specific angle + case study
- For Tier 1: basic merge fields
- Generate 3 variants for review
- Select best (or let user choose)

## Phase 3: Generate LinkedIn Notes

For leads with LinkedIn profiles, execute `message-generator` with config `linkedin-note`:
- Max 300 characters (LinkedIn limit)
- Reference something specific (their post, role, company achievement)
- No hard sell -- focus on relevance
- Include personalization points from person-researcher (Tier 3)

## Phase 4: Generate Instagram DMs

For leads with Instagram accounts, execute `message-generator` with config `instagram-dm`:
- Casual, brand-appropriate tone
- Reference something from their Instagram (recent post, aesthetic)
- Under 3 sentences
- Day 1 is engagement (like/comment), not DM. DM comes on Day 2.

## Phase 5: Generate Call Scripts

For leads scheduled for calls, execute `message-generator` with config `call-script`:
- Opening hook (15 seconds)
- Value prop (30 seconds)
- Discovery question
- Case study reference
- Objection handlers
- CTA (book a demo)

## Phase 6: Automated Delivery

No approval gate. All outreach is delivered automatically.

### Gig Lead Delivery (20/day)
Via Chrome DevTools MCP:
1. `mcp__chrome-devtools__navigate_page` to gig URL
2. `mcp__chrome-devtools__click` apply/submit proposal button
3. `mcp__chrome-devtools__fill_form` with proposal content
4. `mcp__chrome-devtools__click` submit button
5. Verify submission success

### Email Delivery (Company Leads)
Via Chrome DevTools MCP -> Zoho webmail:
1. `mcp__chrome-devtools__navigate_page` to Zoho webmail compose
2. `mcp__chrome-devtools__fill` recipient email
3. `mcp__chrome-devtools__fill` subject line
4. `mcp__chrome-devtools__fill` email body
5. `mcp__chrome-devtools__click` send button

### LinkedIn Delivery
Via Chrome DevTools MCP -> LinkedIn:
1. `mcp__chrome-devtools__navigate_page` to contact's LinkedIn profile
2. `mcp__chrome-devtools__click` Connect button
3. `mcp__chrome-devtools__click` "Add a note"
4. `mcp__chrome-devtools__fill` connection note
5. `mcp__chrome-devtools__click` Send button

### Instagram Delivery (1 DM per 2 min)
Via Chrome DevTools MCP -> Instagram web:
1. `mcp__chrome-devtools__navigate_page` to Instagram DMs
2. Search for contact's handle
3. `mcp__chrome-devtools__fill` DM text
4. `mcp__chrome-devtools__click` send
5. Wait 2 minutes before next DM

### Call Delivery
1. Add lead to CRM "Call Today" tab via `crm-writer`
2. Send Telegram notification: "Your call leads are ready for the day. [N] calls scheduled."

## Phase 7: Save to CRM

Execute `crm-writer`:
- Log all sent outreach to "Outreach CRM" tab
- Update lead stage: OUTREACH_READY -> CONTACTED
- Set cadence_day = 1
- Set next_action = Day 2 action from cadence
- Set next_action_date = tomorrow (skip weekends)
- For gig leads: set gig_cadence_day = 1, next_action = Day 3 email (if applicable)

## Phase 8: Summary

```
OUTREACH SUMMARY -- [Date]
---
COMPANY LEADS:
- Emails sent (Zoho webmail): N
- LinkedIn connection requests sent: N
- Instagram engagement: N
- Call scripts to sheet: N

GIG LEADS:
- Platform applications submitted: N
- Day 3 emails queued: N

DELIVERY STATUS:
- All sent via Chrome DevTools MCP
- Telegram notification sent

Next step: Run /evening-scan at 6 PM to check for responses
```

## Example Usage

**Trigger phrases:**
- "Draft outreach for today's leads"
- "Generate messages for OUTREACH_READY leads"
- "Create outreach drafts for [company]"
- "Write emails for this batch"
