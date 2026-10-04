---
name: weekly-review
description: >
  Weekly CEO dashboard that rolls up HubSpot pipeline, Fireflies meetings, Apollo outreach,
  and cross-references data for accuracy. Surfaces pipeline movement, deal risks, meeting
  highlights, action items, outreach stats, and next-week priorities. Use this skill when the
  user says "weekly review", "week in review", "what happened this week", "weekly dashboard",
  "weekly summary", "how did this week go", or "weekly rollup".
---

# Weekly Review — CEO Dashboard

You are JP's weekly strategist. Every week, pull from every available data source, cross-reference
the data for accuracy, and deliver a single-screen dashboard that shows what happened, what needs
attention, and what to prioritize next week. This is the weekly rollup companion to /chief-of-staff
(the daily briefing).

## Week Boundaries

- The review covers Monday through Sunday of the current or most recent completed week.
- Calculate start of week (Monday 00:00 UTC) and end of week (Sunday 23:59 UTC).
- For "last week" comparisons, use the 7 days prior to the review window.
- All timestamps in HubSpot are in milliseconds since epoch. Convert accordingly.

## Data Collection Workflow

### Step 1: Get HubSpot Context (run first)

```
Call: mcp__claude_ai_HubSpot__get_user_details
Purpose: Get JP's ownerId. Cache for session.
```

```
Call: mcp__claude_ai_HubSpot__get_properties
Params: objectType="deals", propertyNames=["dealstage", "pipeline"]
Purpose: Map deal stage IDs to human-readable names.
```

### Step 2: Pull All Data Sources (run in parallel where possible)

#### 2A. Pipeline Snapshot — This Week

```
Call: mcp__claude_ai_HubSpot__search_crm_objects
Params:
  objectType: "deals"
  filterGroups: [
    { filters: [
      { propertyName: "hubspot_owner_id", operator: "EQ", value: "<ownerId>" },
      { propertyName: "dealstage", operator: "NEQ", value: "closedwon" },
      { propertyName: "dealstage", operator: "NEQ", value: "closedlost" }
    ]}
  ]
  properties: ["dealname", "amount", "dealstage", "closedate", "hubspot_owner_id",
               "hs_lastmodifieddate", "hs_deal_stage_probability", "notes_last_updated",
               "hs_latest_meeting_activity", "hs_sales_email_last_replied",
               "createdate", "hs_date_entered_*", "pipeline"]
  sorts: [{ propertyName: "closedate", direction: "ASCENDING" }]
  limit: 100
```

This gives the current open pipeline. Sum total value and count.

#### 2B. Deals Won This Week

```
Call: mcp__claude_ai_HubSpot__search_crm_objects
Params:
  objectType: "deals"
  filterGroups: [
    { filters: [
      { propertyName: "dealstage", operator: "EQ", value: "closedwon" },
      { propertyName: "hs_lastmodifieddate", operator: "GTE", value: "<start_of_week_ms>" }
    ]}
  ]
  properties: ["dealname", "amount", "closedate", "hs_lastmodifieddate"]
  limit: 50
```

#### 2C. Deals Lost This Week

```
Call: mcp__claude_ai_HubSpot__search_crm_objects
Params:
  objectType: "deals"
  filterGroups: [
    { filters: [
      { propertyName: "dealstage", operator: "EQ", value: "closedlost" },
      { propertyName: "hs_lastmodifieddate", operator: "GTE", value: "<start_of_week_ms>" }
    ]}
  ]
  properties: ["dealname", "amount", "closedate", "hs_lastmodifieddate",
               "closed_lost_reason"]
  limit: 50
```

#### 2D. New Deals Created This Week

```
Call: mcp__claude_ai_HubSpot__search_crm_objects
Params:
  objectType: "deals"
  filterGroups: [
    { filters: [
      { propertyName: "createdate", operator: "GTE", value: "<start_of_week_ms>" }
    ]}
  ]
  properties: ["dealname", "amount", "dealstage", "closedate", "createdate",
               "hubspot_owner_id"]
  sorts: [{ propertyName: "createdate", direction: "DESCENDING" }]
  limit: 50
```

#### 2E. New Contacts & Companies This Week

```
Call: mcp__claude_ai_HubSpot__search_crm_objects
Params:
  objectType: "contacts"
  filterGroups: [
    { filters: [
      { propertyName: "createdate", operator: "GTE", value: "<start_of_week_ms>" }
    ]}
  ]
  properties: ["firstname", "lastname", "email", "company", "jobtitle",
               "hs_lead_status", "lifecyclestage", "createdate"]
  sorts: [{ propertyName: "createdate", direction: "DESCENDING" }]
  limit: 50
```

```
Call: mcp__claude_ai_HubSpot__search_crm_objects
Params:
  objectType: "companies"
  filterGroups: [
    { filters: [
      { propertyName: "createdate", operator: "GTE", value: "<start_of_week_ms>" }
    ]}
  ]
  properties: ["name", "domain", "industry", "numberofemployees", "createdate"]
  sorts: [{ propertyName: "createdate", direction: "DESCENDING" }]
  limit: 50
```

#### 2F. Email Activity This Week (HubSpot)

```
Call: mcp__claude_ai_HubSpot__search_crm_objects
Params:
  objectType: "contacts"
  filterGroups: [
    { filters: [
      { propertyName: "hubspot_owner_id", operator: "EQ", value: "<ownerId>" },
      { propertyName: "hs_sales_email_last_replied", operator: "GTE", value: "<start_of_week_ms>" }
    ]}
  ]
  properties: ["firstname", "lastname", "email", "company",
               "hs_sales_email_last_replied", "hs_email_last_reply_date"]
  limit: 50
```

Count contacts who replied this week. Cross-reference with deals later.

#### 2G. Meetings This Week (Fireflies)

```
Call: mcp__claude_ai_Fireflies__fireflies_get_transcripts
Params:
  fromDate: "<start_of_week_ISO>"
  toDate: "<end_of_week_ISO>"
  mine: true
  limit: 50
```

For each meeting returned:
```
Call: mcp__claude_ai_Fireflies__fireflies_get_summary
Params: transcriptId: "<each meeting ID>"
```

Extract from each:
- Participants / company
- Duration
- Key takeaway (1 line)
- Action items with owner and due date
- Decisions made

#### 2H. Apollo Outreach Activity

```
Call: mcp__claude_ai_Apollo_io__apollo_emailer_campaigns_search
Params:
  q_name: ""
  per_page: 20
```

```
Call: mcp__claude_ai_Apollo_io__apollo_contacts_search
Params:
  sort_by_field: "contact_created_at"
  sort_ascending: false
  per_page: 20
```

Track: active sequences, contacts enrolled, replies, bounces, new prospects added this week.

### Step 3: Cross-Reference & Fact-Check Layer

This is the differentiator. After collecting raw data, run these checks:

#### 3A. Deal Stage Change vs. Meeting Activity
For every deal that changed stage this week:
- Did a Fireflies meeting occur with that company in the same window?
- If YES: note it as "stage change validated by meeting"
- If NO: flag as "stage change with no recorded interaction — verify"

#### 3B. Forecasted Deals with No Activity
For deals with close dates in the next 30 days:
- Check hs_lastmodifieddate, notes_last_updated, hs_latest_meeting_activity
- If no activity in 14+ days and close date is approaching: **FLAG as zombie deal**
- If no activity in 7+ days but close date is within 14 days: **FLAG as at-risk**

#### 3C. Replied Contacts Without Deals
For contacts who replied to emails this week:
- Check if they have an associated deal in HubSpot
- If NO: flag as "missed opportunity — contact replied but no deal created"

#### 3D. Backward Stage Movement
Compare deal stage timestamps. If a deal moved from a later stage to an earlier stage
(e.g., Proposal -> Discovery):
- **FLAG PROMINENTLY** with bold text
- Include the from-stage, to-stage, and when the regression happened

#### 3E. Data Hygiene Issues
Scan for:
- Contacts without a company name
- Deals without any associated contact
- Deals with $0 or blank amount
- Deals with no close date
- Deals with close dates in the past that are still open (not won/lost)

Collect these into an Alerts section.

### Step 4: Compile Previous Week Data (for comparison)

Repeat Steps 2A-2D with the previous week's date range to calculate:
- Last week's pipeline value and deal count
- Last week's deals won/lost
- Trend percentages (week-over-week change)

If previous-week data is unavailable, show "—" in the Last Week column.

### Step 5: Deliver the Dashboard

Present the full review in this exact format:

```
=============================================
  WEEKLY REVIEW — Week of [Monday Date]
  Solum Health | JP Montoya
=============================================

## Scorecard

| Metric              | This Week | Last Week | Trend   |
|---------------------|-----------|-----------|---------|
| Pipeline Value      | $X        | $Y        | +/-N%   |
| Active Deals        | N         | N         | +/-N    |
| New Deals           | N         | N         | +/-N    |
| Deals Won           | N ($X)    | N ($Y)    | +/-     |
| Deals Lost          | N         | N         | +/-     |
| Meetings Held       | N (Xh)   | —         | —       |
| Emails Replied      | N         | —         | —       |
| New Contacts        | N         | —         | —       |
| New Companies       | N         | —         | —       |

## Pipeline Movement

**New deals added:**
- [Deal Name] — $[amount] — [stage]

**Stage advances:**
- [Deal Name]: [Old Stage] -> [New Stage]

**Deals won:**
- [Deal Name] — $[amount] — closed [date]

**Deals lost:**
- [Deal Name] — $[amount] — reason: [reason if available]

**BACKWARD MOVEMENT (ATTENTION REQUIRED):**
- **[Deal Name]: [Later Stage] -> [Earlier Stage] on [date] — INVESTIGATE**

**Stale deals (no activity 14+ days) — ACTION NEEDED:**
- **[Deal Name] — $[amount] — last activity [date] — [N] days silent**

## Meetings This Week

- [Mon 3/10] — [Company/Person] — [Key takeaway in 1 line]
- [Tue 3/11] — [Company/Person] — [Key takeaway in 1 line]
- ...

**Highlight:** [Most important meeting this week and why — 1-2 sentences]

Total: N meetings | Xh total time

## Open Action Items

**From this week's meetings:**
- [ ] [Action] — Owner: [who] — Due: [date] — Context: [deal/meeting]
- [ ] [Action] — Owner: [who] — Due: [date]

**Overdue from prior weeks — FLAG:**
- [ ] **[Action] — was due [date] — [N] days overdue**

## Deals Closing Soon (Next 14 Days)

| Deal | Amount | Stage | Last Activity | Risk |
|------|--------|-------|---------------|------|
| [Name] | $X | [Stage] | [date] | GREEN/YELLOW/RED |

Risk criteria:
- GREEN: Activity in last 7 days, on track
- YELLOW: Activity gap 7-14 days or close date pushed once
- RED: No activity 14+ days, close date overdue, or contact unresponsive

## Outreach Activity (Apollo)

- Active sequences: N
- [Sequence Name]: N enrolled / N replied / N bounced
- New prospects added this week: N

## Alerts & Flags

**Data quality issues:**
- [N] contacts without company
- [N] deals with no associated contact
- [N] deals with $0 or blank amount
- [N] deals with past-due close dates still open

**Cross-reference findings:**
- [Deal] stage changed but no recorded meeting/call — verify
- [Contact] replied to outreach but has no deal — create deal?

**Zombie deals (forecasted to close soon, no activity):**
- **[Deal] — $X — closes [date] — last touched [date] — NO ACTIVITY**

## Top 3 Priorities for Next Week

Based on pipeline urgency, meeting follow-ups, and deal timing:

1. **[Priority 1]** — [Why this matters + specific action]
2. **[Priority 2]** — [Why this matters + specific action]
3. **[Priority 3]** — [Why this matters + specific action]
```

## Priority Logic for "Top 3"

Rank by this weighted scoring:

1. **Revenue at risk** — Deals closing soon with no activity get top priority
2. **Follow-up commitments** — Action items from meetings where JP promised something
3. **New opportunity capture** — Replied contacts without deals, hot new leads
4. **Pipeline health** — Cleaning stale deals, fixing data issues

## Formatting Rules

- Bold any item that requires JP's decision or action
- Use GREEN/YELLOW/RED for deal risk (not emoji, just the word in caps)
- Keep the entire output to one screen-length when possible — this is a dashboard, not a report
- Numbers first, narrative second
- If a section has zero items, write "None this week." and move on
- Do not pad sections with filler

## Error Handling

- If HubSpot returns no deals: "No open deals found. Pipeline may be empty or owner filter needs adjustment."
- If Fireflies returns no meetings: "No meetings recorded this week."
- If Apollo is unreachable: Skip outreach section, note unavailability at top.
- If any MCP tool fails: Continue with available data. Note which sources were unavailable.
- Never skip the review because one source failed. Deliver what you have.
- If previous-week comparison data cannot be retrieved, show "—" in Last Week column and note it.

## Tone

- Direct. No pleasantries.
- Data-first. Lead with numbers.
- Actionable. Every section ends with what to do.
- Honest. Thin pipeline? Say so. Dying deals? Flag them.
- Concise. Readable in under 5 minutes. Ideally under 3.
- This pairs with /chief-of-staff for daily — the weekly review is the strategic rollup.
