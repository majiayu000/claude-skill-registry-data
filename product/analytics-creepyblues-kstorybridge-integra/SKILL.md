---
name: analytics
description: Generate GA4 analytics reports for KStoryBridge dashboard. Use for daily summaries, weekly deep-dives, funnel analysis, traffic source breakdowns, and realtime monitoring. Priority focus on user acquisition and growth metrics.
---

# GA4 Analytics Report Generator

Generate on-demand analytics reports for KStoryBridge dashboard using GA4 MCP tools.

## Commands

```
/analytics daily      # Yesterday's summary (5-min read)
/analytics weekly     # Weekly deep-dive with trends
/analytics funnel     # Trial and authenticated handoff signal analysis
/analytics sources    # Traffic sources breakdown (30 days)
/analytics realtime   # Current active users
```

## GA4 Property

- **Property ID**: 496541587
- **Measurement ID**: G-DWL6MV0MC2
- **Timezone**: America/Los_Angeles

---

## Mandatory evidence rules

1. Standard reports use **complete Pacific calendar days** ending yesterday. Realtime is diagnostic only and never a KPI.
2. Daily, weekly, and source reports query raw production traffic separately for scanner-share variance, but use the **clean production filter** for every behavioral conclusion, alert, source, page, device, and event table.
3. The clean filter values are centralized in `supabase/functions/_shared/analytics-filter-values.mjs` and composed by `analytics-filters.ts`: include only `kstorybridge.com`, `dashboard.kstorybridge.com`, and `creator.kstorybridge.com`; exclude the three observed Brevo/Sendinblue source-medium values and development referrers containing localhost, loopback, staging hosts, or `.vercel.app`.
4. Never interpret a missing canonical event as zero before its full-window `*_CONTRACT_LIVE_AT` gate. Render **Instrumentation pending** instead.
5. Event-name rows are independent leading signals, not proof that the same users completed an ordered journey. Do not calculate step-to-step or overall conversion rates from separate `totalUsers` rows. A conversion rate requires a GA closed-funnel exploration or user-level sequenced evidence with the same cohort, order, and window.
6. Do not use undocumented industry benchmarks. Founder-approved KStoryBridge targets are pending `AR-001`–`AR-004` and `AR-503`.
7. Activation and retention remain **Not reported** until their contracts and cohorts are approved. Sessions and sign-ins are not substitutes for meaningful retention.

### Clean production filter

The symbolic `CLEAN_PRODUCTION_FILTER` in the query examples means the following exact filter. Expand it before making a GA call; never send the symbolic name to the API. Append query-specific expressions, such as an event-name list, inside the same outer `and_group`.

```yaml
and_group:
  expressions:
    - filter:
        field_name: hostName
        in_list_filter:
          values: [kstorybridge.com, dashboard.kstorybridge.com, creator.kstorybridge.com]
          case_sensitive: false
    - not_expression:
        or_group:
          expressions:
            - filter: {field_name: sessionSourceMedium, string_filter: {match_type: EXACT, value: "lu001.r.sp1-brevo.net / referral", case_sensitive: false}}
            - filter: {field_name: sessionSourceMedium, string_filter: {match_type: EXACT, value: "lu001.r.a.d.sendibm1.com / referral", case_sensitive: false}}
            - filter: {field_name: sessionSourceMedium, string_filter: {match_type: EXACT, value: "lu001.r.bh.d.sendibt3.com / referral", case_sensitive: false}}
    - not_expression:
        or_group:
          expressions:
            - filter: {field_name: sessionSourceMedium, string_filter: {match_type: CONTAINS, value: localhost, case_sensitive: false}}
            - filter: {field_name: sessionSourceMedium, string_filter: {match_type: CONTAINS, value: 127.0.0.1, case_sensitive: false}}
            - filter: {field_name: sessionSourceMedium, string_filter: {match_type: CONTAINS, value: dashboard-staging.kstorybridge.com, case_sensitive: false}}
            - filter: {field_name: sessionSourceMedium, string_filter: {match_type: CONTAINS, value: creator-staging.kstorybridge.com, case_sensitive: false}}
            - filter: {field_name: sessionSourceMedium, string_filter: {match_type: CONTAINS, value: .vercel.app, case_sensitive: false}}
```

For the raw comparison, rerun only the traffic-summary query with this production-host filter and the identical date window. Never use the raw result for behavior or conversion conclusions.

```yaml
filter:
  field_name: hostName
  in_list_filter:
    values: [kstorybridge.com, dashboard.kstorybridge.com, creator.kstorybridge.com]
    case_sensitive: false
```

---

## Report Specifications

### `/analytics daily`

Generate a quick daily summary comparing yesterday to the day before.

**Queries to Run** (in parallel):

1. **Traffic Overview**:
```
mcp__analytics-mcp__run_report:
  property_id: 496541587
  date_ranges:
    - {start_date: "yesterday", end_date: "yesterday", name: "Yesterday"}
    - {start_date: "2daysAgo", end_date: "2daysAgo", name: "DayBefore"}
  dimensions: ["date"]
  metrics: ["activeUsers", "newUsers", "sessions", "engagementRate", "averageSessionDuration", "bounceRate"]
  dimension_filter: CLEAN_PRODUCTION_FILTER
```

2. **Traffic Sources** (top 5):
```
mcp__analytics-mcp__run_report:
  property_id: 496541587
  date_ranges: [{start_date: "yesterday", end_date: "yesterday"}]
  dimensions: ["sessionSourceMedium"]
  metrics: ["sessions", "newUsers", "engagementRate"]
  dimension_filter: CLEAN_PRODUCTION_FILTER
  limit: 5
  order_bys: [{metric: {metric_name: "sessions"}, desc: true}]
```

3. **Key Events**:
```
mcp__analytics-mcp__run_report:
  property_id: 496541587
  date_ranges: [{start_date: "yesterday", end_date: "yesterday"}]
  dimensions: ["eventName"]
  metrics: ["eventCount"]
  dimension_filter: CLEAN_PRODUCTION_FILTER
  order_bys: [{metric: {metric_name: "eventCount"}, desc: true}]
  limit: 20
```

**Output Format**:
```markdown
# KStoryBridge Daily Analytics - [DATE]

## Traffic Overview
| Metric | Yesterday | Day Before | Change |
|--------|-----------|------------|--------|
| Active Users | X | X | ±X% |
| New Users | X | X | ±X% |
| Sessions | X | X | ±X% |
| Engagement Rate | X% | X% | ±Xpp |

## Top Traffic Sources
| Source | Sessions | New Users |
|--------|----------|-----------|
| ... | ... | ... |

## Key Events
| Event | Count | Insight |
|-------|-------|---------|
| signup_completed | X | New signups |
| trial_page_view | X | Trial visitors |
| ... | ... | ... |

## Alerts
- [Flag clean external new-user decline of at least 20% only when the prior baseline is at least 5]
- [Flag a missing canonical event only after its full-window live gate and documented volume floor]

## Insights
[Brief analysis and recommended actions]
```

---

### `/analytics weekly`

Generate comprehensive weekly analysis with trends.

**Queries to Run**:

1. **7-Day User Growth**:
```
mcp__analytics-mcp__run_report:
  property_id: 496541587
  date_ranges:
    - {start_date: "7daysAgo", end_date: "yesterday", name: "ThisWeek"}
    - {start_date: "14daysAgo", end_date: "8daysAgo", name: "LastWeek"}
  dimensions: ["date"]
  metrics: ["activeUsers", "newUsers", "sessions", "engagementRate"]
  dimension_filter: CLEAN_PRODUCTION_FILTER
  order_bys: [{dimension: {dimension_name: "date"}, desc: false}]
```

2. **Traffic Sources**:
```
mcp__analytics-mcp__run_report:
  property_id: 496541587
  date_ranges: [{start_date: "7daysAgo", end_date: "yesterday"}]
  dimensions: ["sessionSourceMedium"]
  metrics: ["sessions", "newUsers", "engagementRate"]
  dimension_filter: CLEAN_PRODUCTION_FILTER
  limit: 10
  order_bys: [{metric: {metric_name: "sessions"}, desc: true}]
```

3. **Landing Pages**:
```
mcp__analytics-mcp__run_report:
  property_id: 496541587
  date_ranges: [{start_date: "7daysAgo", end_date: "yesterday"}]
  dimensions: ["landingPage"]
  metrics: ["sessions", "bounceRate", "engagementRate"]
  dimension_filter: CLEAN_PRODUCTION_FILTER
  limit: 10
  order_bys: [{metric: {metric_name: "sessions"}, desc: true}]
```

4. **Key Events**:
```
mcp__analytics-mcp__run_report:
  property_id: 496541587
  date_ranges: [{start_date: "7daysAgo", end_date: "yesterday"}]
  dimensions: ["eventName"]
  metrics: ["eventCount", "totalUsers"]
  dimension_filter:
    and_group:
      expressions:
        - CLEAN_PRODUCTION_FILTER_EXPRESSIONS
        - filter:
            field_name: "eventName"
            in_list_filter:
              values: ["signup_completed", "signin_completed", "trial_page_view", "trial_tool_selected",
                       "trial_limit_reached", "trial_signup_cta_clicked", "chat_message_sent",
                       "comps_search_submitted", "mandate_search_submitted", "checkout_started",
                       "subscription_started", "interest_submitted", "favorite_added",
                       "audience_path_selected", "feature_promo_selected", "trial_cta_clicked",
                       "signup_cta_clicked", "signin_cta_clicked", "creator_inquiry_started",
                       "creator_inquiry_submitted", "creator_inquiry_failed"]
              case_sensitive: true
```

5. **Device Breakdown**:
```
mcp__analytics-mcp__run_report:
  property_id: 496541587
  date_ranges: [{start_date: "7daysAgo", end_date: "yesterday"}]
  dimensions: ["deviceCategory"]
  metrics: ["activeUsers", "engagementRate"]
  dimension_filter: CLEAN_PRODUCTION_FILTER
```

**Output Format**: Full weekly report with:
- A compact operating scorecard covering acquisition, buyer/creator activation readiness, engagement, retention readiness, and commercial outcomes
- Executive summary (2-3 sentences)
- Daily breakdown table with week-over-week comparison
- Current-versus-previous clean app engagement for the buyer dashboard and creator app
- Traffic sources with engagement rates
- Landing page performance
- Tool usage (chat/comps/mandates events)
- Event-level leading-signal analysis; include a closed-cohort conversion funnel only when the query itself enforces cohort, order, and window
- Key insights and action items

Until the founder approves activation and retention definitions, show those values as **Not reported** with the relevant `AR-*` gate. Never render unavailable activation or retention as zero, and never substitute sessions or sign-ins for meaningful retention.

---

### `/analytics funnel`

Analyze trial and authenticated handoff signals over the last 30 complete days. This command does **not** produce a conversion rate from event-name totals.

**Query**:
```
mcp__analytics-mcp__run_report:
  property_id: 496541587
  date_ranges: [{start_date: "30daysAgo", end_date: "yesterday"}]
  dimensions: ["eventName"]
  metrics: ["eventCount", "totalUsers"]
  dimension_filter:
    and_group:
      expressions:
        - CLEAN_PRODUCTION_FILTER_EXPRESSIONS
        - filter:
            field_name: "eventName"
            in_list_filter:
              values: ["trial_page_view", "trial_tool_selected", "trial_comps_search",
                       "trial_mandate_search", "trial_chat_message_sent", "trial_search_completed",
                       "trial_limit_reached", "trial_signup_cta_clicked", "signup_completed",
                       "signin_completed", "chat_message_sent", "comps_search_submitted",
                       "mandate_search_submitted", "checkout_started", "subscription_started"]
              case_sensitive: true
```

**Output Format**:
```
Handoff Signals (Last 30 Complete Days)
=======================================

| Signal | Users | Events | Evidence status |
|--------|------:|-------:|-----------------|
| Trial page viewed | XXX | XXX | Live / Instrumentation pending |
| Trial tool selected | XXX | XXX | Live / Instrumentation pending |
| Trial search completed | XXX | XXX | Live / Instrumentation pending |
| Trial signup CTA clicked | XXX | XXX | Live / Instrumentation pending |
| Signup completed | XXX | XXX | Live / Instrumentation pending |

Conversion rate: Not reported from event rows. These totals do not prove that the same users progressed in order.

Recommendations:
- [Based on observed signal volume, source quality, and independently reconciled outcomes]
```

---

### `/analytics sources`

Deep dive into traffic sources (last 30 days).

**Query**:
```
mcp__analytics-mcp__run_report:
  property_id: 496541587
  date_ranges: [{start_date: "30daysAgo", end_date: "yesterday"}]
  dimensions: ["sessionSourceMedium"]
  metrics: ["sessions", "newUsers", "engagementRate", "bounceRate"]
  dimension_filter: CLEAN_PRODUCTION_FILTER
  limit: 20
  order_bys: [{metric: {metric_name: "sessions"}, desc: true}]
```

**Output Format**:
```
Traffic Sources (Last 30 Days)
==============================

| Source/Medium | Sessions | New Users | Engagement | Bounce |
|---------------|----------|-----------|------------|--------|
| direct/(none) | XXX | XXX | XX% | XX% |
| google/organic| XXX | XXX | XX% | XX% |
| ... | ... | ... | ... | ... |

Quality Analysis:
- Best engagement: [source] at XX%
- Most new users: [source] with XXX
- Highest bounce: [source] at XX% (investigate)

Recommendations:
- [Based on source quality]
```

---

### `/analytics realtime`

Show current active users.

**Query**:
```
mcp__analytics-mcp__run_realtime_report:
  property_id: 496541587
  dimensions: ["unifiedScreenName"]
  metrics: ["activeUsers"]
```

**Output Format**:
```
Realtime Activity
=================

Active Users: X

Current Pages:
- /trial: X users
- /buyers/chat: X users
- /buyers/home: X users
```

Realtime may include internal, scanner, or otherwise unclassified activity. Label it diagnostic and never use it to claim acquisition, activation, conversion, or retention performance.

---

## Key Metrics Reference

### Approved operating alerts

| Condition | Current rule |
|-----------|--------------|
| Scanner contamination | Show raw-versus-clean variance; alert when excluded scanner share exceeds 10% |
| Acquisition decline | Alert at a clean external new-user decline of at least 20% with a prior baseline of at least 5 |
| Missing product or website events | Alert only after the corresponding full-window live gate and at least 3 clean sessions in that app |
| Reconciliation drift | Alert only after the corresponding live gate and use the documented 5% tolerance |
| Activation or retention decline | Not reported until founder-approved contracts, cohorts, cadence, and volume floors exist |

Targets remain pending `AR-503`. Do not turn descriptive engagement or bounce rates into pass/fail thresholds without a documented KStoryBridge baseline and owner.

### Key Events

| Event | Meaning |
|-------|---------|
| `trial_page_view` | User visited trial page |
| `trial_tool_selected` | User clicked on a tool (chat/comps/mandates) |
| `trial_signup_cta_clicked` | User clicked signup from trial |
| `signup_completed` | User completed registration |
| `chat_message_sent` | User sent a chat message |
| `comps_search_submitted` | Authenticated user submitted a comps request |
| `mandate_search_submitted` | User searched with a mandate |
| `checkout_started` | User started checkout |
| `subscription_started` | Stripe confirmed an active paid subscription |

### Event cutover policy

- Public-trial events such as `trial_comps_search` remain distinct trial outcomes; do not merge them with authenticated product events.
- Never query or add the obsolete authenticated aliases `signin`, `comps_search`, or `checkout_completed` to canonical values.
- Use `signin_completed`, `comps_search_submitted`, and webhook-confirmed `subscription_started` for the corresponding canonical outcomes.
- A reporting window is contract-live only when its full start is after the recorded deployment timestamp. If a window crosses a cutover, label canonical counts as instrumentation pending; do not backfill them by summing legacy aliases.

---

## Email Delivery (Required)

**IMPORTANT**: After generating ANY report, you MUST send it via email to all admins.

### How to Send

After the report is generated and displayed to the user, call the `send-analytics-report` edge function:

```bash
curl -X POST "https://dlrnrgcoguxlkkcitlpd.supabase.co/functions/v1/send-analytics-report" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "reportType": "daily",
    "reportDate": "January 7, 2026",
    "reportMarkdown": "[FULL REPORT MARKDOWN HERE]",
    "invocationKey": "manual-daily:2026-01-07:operator-v1",
    "alerts": ["Traffic drop >20%: -55%", "Zero signups detected"],
    "sendSlack": true
  }'
```

Never use the anon key or a user JWT. The service-role key must come from an approved server-only environment and must not be printed. Reuse the same privacy-safe `invocationKey` for a retry so recipients already marked sent are not contacted twice.

### Payload Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `reportType` | string | Yes | One of: `daily`, `weekly`, `funnel`, `sources`, `realtime` |
| `reportDate` | string | Yes | Human-readable date, e.g., "January 7, 2026" |
| `reportMarkdown` | string | Yes | The full markdown report (will be converted to HTML) |
| `invocationKey` | string | Recommended | Stable privacy-safe manual-run key for idempotent retry; never include an email, query, title, URL, or secret |
| `alerts` | string[] | No | Array of triggered alert messages |
| `sendSlack` | boolean | No | Send Slack notification (default: true) |

### What Happens

1. Edge function requires the exact service-role credential and claims one manual audit run
2. It snapshots active admin IDs without storing email or report content in the ledger
3. It converts markdown to styled HTML email (KStoryBridge brand)
4. It claims and sends only unsent admin/Slack deliveries
5. It persists aggregate success or controlled error codes and returns the durable status

### Response

```json
{
  "success": true,
  "status": "succeeded",
  "results": {
    "emailsSent": 2,
    "emailsFailed": 0,
    "slackSent": true
  }
}
```

### After Sending

Confirm to user: "Report sent to X admin(s) via email and Slack."

---

## Related Skills

- `/health-check` - Verify system health before running analytics
- `/cost-report` - Track API costs alongside traffic
- `/deploy-staging` - Deploy changes based on analytics insights
