---
name: weekly-report
description: >
  Monday morning full pipeline review with metrics, channel performance,
  and forecast. Reads all CRM tabs, calculates deltas vs previous week,
  and generates actionable recommendations.
tags: [weekly, reporting, analytics, pipeline, playbook]
---

# Weekly Report

Full pipeline review designed to run every Monday morning. Pulls data from all CRM tabs, computes week-over-week deltas, and generates a structured report with metrics, channel performance, lead quality analysis, revenue forecasting, and concrete recommendations for the week ahead.

## Prerequisites

- `agency.config.json` fully populated (run `/agency-setup` first)
- CRM initialized with data from at least one week of pipeline activity
- Tool stack configured (Apollo, email validator, email sender, LinkedIn tool)

## Composites & Capabilities Used

1. `crm-writer` -- read CRM data from all tabs
2. `pipeline-dashboard` -- pull aggregated metrics (if built)

## Phase 0: Data Collection

Read from CRM all tabs:
- **Pipeline tab**: all leads with stages, scores, dates, and ownership
- **Outreach log**: all actions this week (emails, LinkedIn, Instagram, calls)
- **Email drafts**: sent vs drafted counts, subject lines, reply tracking
- **Calling tab**: calls made, outcomes (connected, voicemail, no answer, meeting booked)
- **Dashboard tab**: previous week's numbers for comparison

Pull the date range: Monday 00:00 through Sunday 23:59 of the reporting week.

## Phase 1: Pipeline Metrics

Calculate and present:

```
WEEKLY PIPELINE REPORT -- Week of [Date]
===

PIPELINE SNAPSHOT:
- Total active leads: N (delta vs last week: +/-N)
- By stage:
  NEW:             N
  RESEARCHED:      N
  ENRICHED:        N
  OUTREACH_READY:  N
  CONTACTED:       N
  REPLIED:         N
  DEMO_BOOKED:     N
  WON:             N
  LOST:            N

NEW LEADS THIS WEEK: N
- Signal scan: N
- Platform scraper: N
- Inbound: N
- Referral: N
```

Include stage-by-stage delta vs previous week. Highlight any stage with > 20% change.

## Phase 2: Outreach Performance

```
OUTREACH METRICS (Last 7 Days):
---
Emails:
- Sent: N
- Opens: N (X%) [if trackable]
- Replies: N (X%)
- Positive replies: N
- Demo from email: N

LinkedIn:
- Connections sent: N
- Accepted: N (X%)
- DMs sent: N
- Replies: N (X%)

Instagram:
- DMs sent: N
- Replies: N (X%)

Calls:
- Made: N
- Connected: N (X%)
- Meetings booked: N

BEST PERFORMING:
- Best email subject: "[subject]" (X% reply rate)
- Best channel: [channel] (X% response rate)
- Best touch point: Touch N (X% response rate)
```

Break down by day of week if enough data exists to surface timing patterns.

## Phase 3: Lead Quality

```
LEAD QUALITY:
---
HOT leads generated: N
WARM leads generated: N
COOL leads (filtered): N

Conversion funnel:
Signal -> Lead: X%
Lead -> Enriched: X%
Enriched -> Contacted: X%
Contacted -> Replied: X%
Replied -> Demo: X%
Demo -> Won: X%

Average lead score: N
Top platforms by quality: [ranked list]
```

Flag any funnel stage with conversion below historical average.

## Phase 4: Revenue Impact

```
REVENUE PIPELINE:
---
Demos booked this week: N
Demos booked total: N
Proposals sent: N
Deals in negotiation: N
Deals won this week: N
Revenue won: $X

Pipeline value (weighted):
- HOT leads * close rate: $X
- Demos scheduled: $X
- Proposals out: $X
Total pipeline value: $X
```

Use close rate estimates from `agency.config.json` if available, otherwise use industry defaults (HOT: 15%, Demo: 30%, Proposal: 50%).

## Phase 5: Credit Usage

```
TOOL CREDITS:
---
Apollo credits used: N / N remaining
ZeroBounce credits used: N / N remaining
Email sends: N / N daily cap
```

Flag if any tool is below 20% remaining credits. Calculate projected depletion date at current burn rate.

## Phase 6: Insights & Recommendations

Based on the data, generate 3-5 specific recommendations:
- If reply rate < 3%: "Email copy needs revision. Consider testing new subject lines."
- If LinkedIn outperforms email: "Shift more outreach to LinkedIn. Increase daily connection cap."
- If HOT leads are low: "Expand signal scan to more platforms or broaden keywords."
- If follow-ups are being missed: "N leads had overdue follow-ups. Catch up today."
- If one segment outperforms: "India D2C segment has 2x reply rate. Prioritize."
- If demo-to-won rate is dropping: "Review demo quality. Consider pre-qualifying harder."
- If pipeline is top-heavy (many NEW, few CONTACTED): "Enrichment is the bottleneck. Allocate more time to Phase 2."

Each recommendation includes: observation, impact estimate, and suggested action.

## Phase 7: Next Week Plan

Suggest adjustments based on this week's data:
- Target lead count for next week (increase if pipeline is thin, maintain if healthy)
- Channels to prioritize (based on Phase 2 performance data)
- Cadence adjustments (touch timing, sequence changes)
- Content angles to test (new subject lines, new value props, new case studies)
- Specific accounts to focus on (stalled deals, high-value prospects)

```
NEXT WEEK TARGETS:
---
New leads: N
Enrichments: N
Outreach drafts: N
Follow-ups: N
Demos target: N
Calls target: N

PRIORITY ACTIONS:
1. [Specific action with owner and deadline]
2. [Specific action with owner and deadline]
3. [Specific action with owner and deadline]
```

## Example Usage

**Trigger phrases:**
- "Run the weekly report"
- "Monday pipeline review"
- "How did we do this week?"
- "Generate weekly sales metrics"
