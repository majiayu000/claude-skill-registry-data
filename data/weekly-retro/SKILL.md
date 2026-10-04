---
name: weekly-retro
description: >
  Weekly business retrospective for a solo founder. Reviews the past 7 days across all channels:
  deals closed/lost (HubSpot), calls made and quality (Fireflies), content published, outreach
  performance (Apollo), conference pipeline, and revenue vs. target. Produces a scored report
  with wins, losses, learnings, and priorities for next week. Use this skill when the user says
  "weekly retro", "weekly review", "how did this week go", "business retro", "founder retro",
  "end of week review", "weekly scorecard", "weekly report", or any variation of wanting a
  structured look-back at the past week's business performance.
  NOTE: This is different from gstack's /retro which analyzes engineering commit history and
  code patterns. This skill analyzes business execution: revenue, pipeline, calls, content, outreach.
---

# Weekly Business Retro — Founder Scorecard

Every Friday, take 15 minutes to look at what actually happened this week across every
business channel. No narrative. Just data, scores, and honest assessment.

## Core Principle

Garry Tan's `/retro` reviews engineering execution (commits, PRs, test coverage). This
retro reviews business execution (revenue, pipeline, calls, content, outreach). Both
matter. This one tells you if you're closing the gap to $2M.

## Data Collection (run ALL in parallel)

### Channel 1: Revenue & Pipeline (HubSpot)

**Deals won this week:**
```
search_crm_objects: objectType="deals"
  filterGroups: [{ filters: [
    { propertyName: "dealstage", operator: "EQ", value: "closedwon" },
    { propertyName: "closedate", operator: "GTE", value: "{weekStart}" }
  ]}]
  properties: ["dealname", "amount", "closedate", "hs_analytics_source"]
```

**Deals lost this week:**
```
search_crm_objects: objectType="deals"
  filterGroups: [{ filters: [
    { propertyName: "dealstage", operator: "EQ", value: "closedlost" },
    { propertyName: "closedate", operator: "GTE", value: "{weekStart}" }
  ]}]
```

**Pipeline movement:**
```
search_crm_objects: objectType="deals"
  filterGroups: [{ filters: [
    { propertyName: "hs_lastmodifieddate", operator: "GTE", value: "{weekStart}" },
    { propertyName: "dealstage", operator: "NEQ", value: "closedwon" },
    { propertyName: "dealstage", operator: "NEQ", value: "closedlost" }
  ]}]
  properties: ["dealname", "amount", "dealstage", "closedate",
               "hs_lastmodifieddate", "hs_deal_stage_probability"]
```

**New contacts added:**
```
search_crm_objects: objectType="contacts"
  filterGroups: [{ filters: [
    { propertyName: "createdate", operator: "GTE", value: "{weekStart}" }
  ]}]
  properties: ["firstname", "lastname", "company", "jobtitle",
               "hs_analytics_source", "hs_lead_status"]
  limit: 50
```

### Channel 2: Sales Calls (Fireflies)

```
fireflies_get_transcripts: mine=true, fromDate={weekStart}, toDate={weekEnd}, limit=30
```

For each call, get summary:
```
fireflies_get_summary: transcriptId={id}
```

**Classify calls:**
- Prospect calls (demos, assessments, FUPs)
- Client calls (onboarding, touchpoints, support)
- Internal calls (team, investor, recruiting)

**Extract from prospect calls:**
- Outcome (meeting booked, trial started, deal advanced, stalled, lost)
- Pricing discussed? Score 1-5 per pricing-coach rubric
- Key objections raised
- Follow-up commitments made

### Channel 3: Outreach Performance (Apollo)

```
apollo_emailer_campaigns_search: per_page=20
```

**Extract:**
- Emails sent this week
- Opens, replies, bounces
- Reply rate by sequence
- Best performing message
- Worst performing message

### Channel 4: Content Published

Search for content activity this week:
- Blog posts published (check Webflow CMS)
- LinkedIn posts/carousels published
- X posts published
- Conference one-pagers created

### Channel 5: Conference Pipeline

Check for any conference-related activity:
- Conferences attended this week
- Follow-up sequences launched
- Conference deals in pipeline

## Scoring Framework

### Weekly Scorecard (1-5 per channel)

| Channel | Score 5 | Score 3 | Score 1 |
|---------|---------|---------|---------|
| **Revenue** | Deals closed, MRR grew | Pipeline moved, no close | No activity, deals stalled |
| **Sales Calls** | 5+ prospect calls, clear outcomes | 2-4 calls, mixed outcomes | 0-1 calls or no follow-through |
| **Outreach** | 100+ emails, 10%+ reply rate | 50+ emails, 5%+ reply rate | <50 emails or <3% reply |
| **Content** | 3+ pieces published | 1-2 pieces published | Nothing published |
| **Pipeline Health** | Growing, deals advancing | Flat, some movement | Shrinking, deals stuck |

### Revenue Pace Check

Calculate against the $2M target:

```
Annual target: $2,000,000
Monthly target: $166,667
Weekly target: $41,667

YTD revenue: $[actual]
YTD target: $[prorated]
Gap: $[difference]
Pace: [ahead/behind] by [X]%
Weeks remaining: [X]
Required weekly run rate to hit target: $[amount]
```

## Report Structure

```
# Weekly Business Retro
## Week of {weekStart} — {weekEnd}

### WEEKLY SCORE: X.X / 5.0

| Channel | Score | Highlight |
|---------|-------|-----------|
| Revenue | X/5 | [one line] |
| Sales Calls | X/5 | [one line] |
| Outreach | X/5 | [one line] |
| Content | X/5 | [one line] |
| Pipeline | X/5 | [one line] |

---

### REVENUE PACE
Target: $2M | YTD: $[X] | Pace: [X]% | Gap: $[X]
Weekly run rate needed: $[X]/week for remaining [X] weeks

---

### WINS (what worked)
1. [Specific win with numbers]
2. [Specific win with numbers]
3. [Specific win with numbers]

### LOSSES (what didn't)
1. [Specific loss with context and why]
2. [Specific loss with context and why]

### LEARNINGS (what to change)
1. [Specific insight that changes behavior next week]
2. [Specific insight that changes behavior next week]

---

### DEALS THIS WEEK

Won:
- [Deal] — $[amount] — [source] — [days in pipeline]

Lost:
- [Deal] — $[amount] — [reason]

Advanced:
- [Deal] — $[amount] — [from stage] → [to stage]

Stalled:
- [Deal] — $[amount] — [days stuck] — [recommended action]

---

### CALLS SCORECARD

| Call | Date | Type | Outcome | Pricing Score |
|------|------|------|---------|--------------|
| ... | ... | ... | ... | X/5 |

Total: X prospect calls, X client calls, X internal
Avg pricing score: X.X/5

---

### OUTREACH SCORECARD

| Sequence | Sent | Opens | Replies | Reply Rate |
|----------|------|-------|---------|------------|
| ... | ... | ... | ... | X% |

Best message: "[subject line]" — X% reply rate
Worst message: "[subject line]" — X% reply rate

---

### CONTENT PUBLISHED

| Piece | Platform | Engagement |
|-------|----------|-----------|
| ... | ... | ... |

---

### NEXT WEEK PRIORITIES (ranked)

1. [MUST] [action] — [why, what's at stake]
2. [MUST] [action] — [why]
3. [SHOULD] [action] — [why]
4. [SHOULD] [action] — [why]
5. [COULD] [action] — [if time allows]

---

### TREND (vs. last week)

| Metric | Last Week | This Week | Trend |
|--------|-----------|-----------|-------|
| Weekly score | X.X | X.X | arrow |
| Deals won | X | X | arrow |
| Prospect calls | X | X | arrow |
| Emails sent | X | X | arrow |
| Reply rate | X% | X% | arrow |
| Content pieces | X | X | arrow |
```

## Delivery

1. Save report to `~/Documents/Claude/SALES/Weekly_Retro_{YYYY-MM-DD}.md`
2. Display: Weekly score, revenue pace, top win, top loss, #1 priority for next week
3. Compare to previous week's retro if it exists in the output directory
4. Ask: "Want me to drill into any channel, specific deal, or plan next week's priorities?"

## Important Rules

- **Run every Friday.** Consistency matters more than depth. A quick retro every week beats a deep one monthly.
- **Score honestly.** A 2/5 week is useful data. Inflating scores hides problems.
- **Revenue pace is the anchor.** Every other metric exists to serve the $2M target.
- **Track trends, not just snapshots.** Week-over-week deltas reveal whether efforts are compounding.
- **Name specific deals and people.** "Pipeline grew" is useless. "$45K deal with Attain ABA moved to negotiation" is actionable.
- **Learnings must change behavior.** "I should do more calls" is not a learning. "Starting the call with their data instead of a deck increased pricing acceptance to 4/5" is.
- **This is NOT gstack /retro.** That reviews code. This reviews business execution. Use both.
