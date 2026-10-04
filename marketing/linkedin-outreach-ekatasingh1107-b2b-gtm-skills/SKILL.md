---
name: linkedin-outreach
description: LinkedIn connection requests and DM sequences adapted to tool stack
tags: [linkedin, outreach, connections, dms]
---

# LinkedIn Outreach

Generates LinkedIn connection request notes, follow-up DMs, and InMails for a list of leads. Adapts delivery method to the configured tool stack: CSV export for Dripify/Expandi, browser automation, or manual copy-paste.

## Prerequisites

- `agency.config.json` at repo root with `tools.linkedin_outreach`, `outreach`, and `case_studies` sections
- `crm-writer` skill for tracking outreach actions
- `message-generator` skill for personalization
- Optional: Chrome automation (for browser delivery mode)

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `tools.linkedin_outreach.tool` -- the automation tool name (e.g., "dripify", "expandi", "manual")
   - `tools.linkedin_outreach.access` -- delivery method: `"csv_export"`, `"browser"`, or `"manual"`
   - `tools.linkedin_outreach.daily_limit` -- max connection requests per day (respect this cap strictly)
   - `outreach.tone` -- voice and tone guidelines for messages
   - `outreach.banned_phrases` -- phrases that must never appear in any message
   - `case_studies` -- available case studies for social proof references
3. Accept parameters:
   - `leads` -- array of lead objects, each with: `name`, `title`, `company`, `linkedin_url`, and optionally `recent_post`, `role_change`, `company_achievement`
   - `message_type` -- one of: `"connect"`, `"dm"`, `"inmail"`, or `"all"` (default: `"connect"`)

## Phase 1: Generate Content

For each lead, generate messages based on `message_type`. Every message must be checked against `outreach.banned_phrases` before inclusion. Match the voice from `outreach.tone`.

### Connection Request Note (max 300 characters)

- Include one specific personalization point. Pick from, in priority order:
  1. Their recent LinkedIn post (if `recent_post` provided)
  2. A role change or promotion (if `role_change` provided)
  3. A company achievement or news (if `company_achievement` provided)
  4. Their title + company combination (fallback)
- Include one reason to connect: shared industry, mutual interest, or a brief value signal.
- **NO pitch in the connection note.** Zero selling language. This is a human-to-human connection.
- Keep under 300 characters including spaces. LinkedIn truncates at 300.

Example structure:
```
Hey {first_name}, saw your post on {topic} -- really resonated.
I work with {industry} brands on {area}. Would love to connect and exchange notes.
```

### Follow-up DM (max 150 words, for accepted connections)

- Reference the connection acceptance: "Thanks for connecting" or similar.
- Share one insight, resource, or observation relevant to their role or company.
- Soft CTA: ask a question, do not pitch. Frame as curiosity or offering help.
- Use a different angle than the connection note. Do not repeat the same personalization point.

Example structure:
```
Thanks for connecting, {first_name}.

I was looking at {company}'s store and noticed {observation}.
We worked on something similar with {case_study_client} and saw {result}.

Curious -- is {topic} something your team is focused on right now?
```

### InMail (max 200 words, if InMail credits available)

- Subject line: under 40 characters. Make it specific, not generic. Avoid "Quick question" or "Opportunity."
- Lead with value or an insight about their business, not about your agency.
- Reference one case study with a specific metric.
- Soft CTA: propose a brief call or ask a question. Not "Let's schedule a demo."

Example structure:
```
Subject: {company}'s {specific_page} conversion

Hi {first_name},

I was reviewing {company}'s {specific_area} and noticed {observation}.

We helped {case_study_client} fix a similar issue, which led to a {X%} increase in {metric}.

Would it be worth a 15-minute look at what we found? Happy to share the analysis either way.

{sender_name}
```

## Phase 2: Delivery

Check `tools.linkedin_outreach.access` to determine delivery method.

### CSV Export (access: "csv_export")

For tools like Dripify, Expandi, or LinkedHelper:

1. Generate a CSV file with these columns:
   - `LinkedIn_URL` -- the lead's LinkedIn profile URL
   - `First_Name` -- extracted from lead name
   - `Last_Name` -- extracted from lead name
   - `Company` -- lead's company
   - `Title` -- lead's job title
   - `Connection_Note` -- the 300-char connection request note
   - `Follow_Up_DM` -- the follow-up DM text (used as sequence step 2)

2. Save to `output/linkedin-outreach-{YYYY-MM-DD}.csv`

3. Provide tool-specific import instructions:
   - **Dripify**: "Go to Campaigns > Create Campaign > Import CSV. Map LinkedIn_URL to 'Profile URL', Connection_Note to 'Connection Message', Follow_Up_DM to 'Follow-up Message 1'."
   - **Expandi**: "Go to Campaigns > New > CSV Import. Upload the file. Map columns in the field mapper."

### Browser (access: "browser")

Use Chrome automation to send connection requests directly:

1. Navigate to each lead's `linkedin_url`.
2. Click the "Connect" button.
3. If "Add a note" option appears, paste the `Connection_Note`.
4. Send the request.
5. Wait 30-60 seconds between requests (randomized to avoid detection).
6. Stop when `daily_limit` is reached, even if leads remain. Report how many were sent and how many are queued for tomorrow.

### Manual (access: "manual")

For manual copy-paste workflow:

1. Display each lead in sequence with:
   - Lead name, title, company
   - LinkedIn profile URL (clickable)
   - Connection note (ready to copy)
   - Follow-up DM (for after acceptance)
2. Format for easy scanning and quick copy-paste.

## Phase 3: Track

After delivery (or generation):

1. Log each action to CRM via `crm-writer` skill, writing to the outreach_log tab.
2. For each lead, log:
   - Date
   - Lead name
   - Company
   - LinkedIn URL
   - Action taken (connection_sent, dm_sent, inmail_sent, csv_exported)
   - Message content (condensed)
   - Cadence day (Day 1 for new connections)
   - Next action (e.g., "Follow-up DM after acceptance" or "Check acceptance in 3 days")
3. Respect `daily_limit`: if the limit is reached mid-batch, stop and report remaining leads as "queued."

## Phase 4: Summary

Present a summary report:

```
LinkedIn Outreach Summary ({date}):

Connections sent: {N}
DMs sent: {N}
InMails sent: {N}
Daily limit remaining: {N}
CSV exported to: output/linkedin-outreach-{date}.csv (if applicable)

Queued for tomorrow: {N} leads (daily limit reached)

Leads processed:
1. {Name} @ {Company} -- connection note sent
2. {Name} @ {Company} -- DM sent (already connected)
...
```

## Example Usage

Trigger phrases:
- "Send LinkedIn connections to these leads"
- "Generate LinkedIn outreach for this list"
- "Create Dripify CSV for LinkedIn"
- "Draft LinkedIn DMs for accepted connections"
- "Run LinkedIn outreach"

```
User: Send LinkedIn connections to 10 leads from the signal scanner
Assistant: [reads config, checks daily limit, generates personalized connection notes, delivers via configured method, logs to CRM, reports summary]
```

```
User: Create a Dripify CSV for these LinkedIn leads
Assistant: [generates connection notes + follow-up DMs, exports CSV to output/, provides Dripify import instructions]
```
