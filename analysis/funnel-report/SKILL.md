---
name: funnel-report
description: Generate comprehensive signup funnel analysis for KStoryBridge. Analyzes the complete user journey from first visit through trial to signup completion, identifies drop-off points, and provides actionable recommendations.
---

# Signup Funnel Report Generator

Generate detailed funnel analysis for KStoryBridge user acquisition using GA4 MCP tools.

## Commands

```
/funnel-report              # Full 30-day funnel analysis (default)
/funnel-report 7            # Last 7 days
/funnel-report 14           # Last 14 days
/funnel-report compare      # This week vs last week comparison
```

## GA4 Property

- **Property ID**: 496541587
- **Measurement ID**: G-DWL6MV0MC2
- **Timezone**: America/Los_Angeles

---

## Funnel Stages

The KStoryBridge signup funnel consists of these stages:

| Stage | Event Name | Description |
|-------|------------|-------------|
| 1. First Visit | `first_visit` | User lands on site for first time |
| 2. Trial Page | `trial_page_view` | User views trial page |
| 3. Tool Selected | `trial_tool_selected` | User clicks a tool (chat/comps/mandates) |
| 4. Search Completed | `trial_search_completed` | User completes a search |
| 5. Limit Reached | `trial_limit_reached` | User hits trial usage limit |
| 6. Signup CTA | `trial_signup_cta_clicked` | User clicks signup button |
| 7. Signup Complete | `signup_completed` | User completes registration |

**Tool-Specific Events**:
- `trial_comps_search` - Comps Navigator search in trial
- `trial_mandate_search` - Mandate Matcher search in trial
- `trial_chat_message_sent` - Chat message in trial

---

## Queries to Run

Execute these queries **in parallel** for efficiency:

### Query 1: Funnel Events (30 days)

```
mcp__analytics-mcp__run_report:
  property_id: 496541587
  date_ranges: [{start_date: "30daysAgo", end_date: "yesterday", name: "Last30Days"}]
  dimensions: ["eventName"]
  metrics: ["eventCount", "totalUsers"]
  dimension_filter:
    filter:
      field_name: "eventName"
      in_list_filter:
        values: [
          "first_visit",
          "trial_page_view",
          "trial_tool_selected",
          "trial_comps_search",
          "trial_mandate_search",
          "trial_chat_message_sent",
          "trial_search_completed",
          "trial_limit_reached",
          "trial_signup_cta_clicked",
          "signup_completed",
          "signup_started",
          "page_view",
          "session_start"
        ]
        case_sensitive: true
  order_bys: [{metric: {metric_name: "eventCount"}, desc: true}]
```

### Query 2: Page Performance

```
mcp__analytics-mcp__run_report:
  property_id: 496541587
  date_ranges: [{start_date: "30daysAgo", end_date: "yesterday"}]
  dimensions: ["pagePath"]
  metrics: ["activeUsers", "sessions", "bounceRate", "engagementRate"]
  dimension_filter:
    filter:
      field_name: "pagePath"
      in_list_filter:
        values: ["/trial", "/signup", "/auth/callback", "/buyers/home", "/buyers/chat", "/", "/producers", "/signin"]
        case_sensitive: false
  order_bys: [{metric: {metric_name: "sessions"}, desc: true}]
```

### Query 3: Landing Page Analysis

```
mcp__analytics-mcp__run_report:
  property_id: 496541587
  date_ranges: [{start_date: "30daysAgo", end_date: "yesterday"}]
  dimensions: ["landingPage"]
  metrics: ["sessions", "newUsers", "engagementRate", "bounceRate"]
  order_bys: [{metric: {metric_name: "sessions"}, desc: true}]
  limit: 15
```

### Query 4: Daily Funnel Trend

```
mcp__analytics-mcp__run_report:
  property_id: 496541587
  date_ranges: [{start_date: "30daysAgo", end_date: "yesterday"}]
  dimensions: ["eventName", "date"]
  metrics: ["eventCount", "totalUsers"]
  dimension_filter:
    filter:
      field_name: "eventName"
      in_list_filter:
        values: [
          "first_visit",
          "trial_page_view",
          "trial_tool_selected",
          "trial_search_completed",
          "trial_signup_cta_clicked",
          "signup_completed"
        ]
        case_sensitive: true
  order_bys: [{dimension: {dimension_name: "date"}, desc: false}]
```

### Query 5: Traffic Sources

```
mcp__analytics-mcp__run_report:
  property_id: 496541587
  date_ranges: [{start_date: "30daysAgo", end_date: "yesterday"}]
  dimensions: ["sessionSourceMedium"]
  metrics: ["newUsers", "sessions", "engagementRate"]
  order_bys: [{metric: {metric_name: "newUsers"}, desc: true}]
  limit: 10
```

---

## Output Format

Generate the report in this exact format:

```markdown
# KStoryBridge Signup Funnel Analysis

**Period**: [START_DATE] - [END_DATE] ([X] days)

---

## Funnel Visualization

\`\`\`
Step 1: First Visit                    [XXX events / XXX users] ████████████████████ 100%
           ↓ (X.X% proceed to trial)
Step 2: Trial Page View                [XXX events / XXX users] ██                    X.X%
           ↓ (XX.X% select a tool)
Step 3: Trial Tool Selected            [XXX events / XXX users] █                     X.X%
           ↓ (XX.X% complete search)
Step 4: Trial Search Completed         [XXX events / XXX users] █                     X.X%
           ↓ (XX.X% click signup CTA)
Step 5: Trial Signup CTA Clicked       [XXX events / XXX users] ▏                     X.X%
           ↓ (XX.X% complete signup)
Step 6: Signup Completed               [XXX events / XXX users] ▏                     X.X%
\`\`\`

---

## Funnel Metrics

| Stage | Users | Events | Step Conversion | Overall Rate |
|-------|-------|--------|-----------------|--------------|
| First Visit | XXX | XXX | - | 100% |
| Trial Page View | XXX | XXX | X.X% | X.X% |
| Tool Selected | XXX | XXX | XX.X% | X.X% |
| Search Completed | XXX | XXX | XX.X% | X.X% |
| Signup CTA Click | XXX | XXX | XX.X% | X.X% |
| Signup Complete | XXX | XXX | XX.X% | X.X% |

---

## Tool Usage Breakdown

| Tool | Trial Searches | Users |
|------|----------------|-------|
| Comps Navigator | XXX | XXX |
| Mandate Matcher | XXX | XXX |
| AI Chat | XXX | XXX |

---

## Page Performance

| Page | Sessions | Users | Engagement | Bounce |
|------|----------|-------|------------|--------|
| `/` (Homepage) | XXX | XXX | XX.X% | XX.X% |
| `/trial` | XXX | XXX | XX.X% | XX.X% |
| `/signup` | XXX | XXX | XX.X% | XX.X% |
| `/buyers/home` | XXX | XXX | XX.X% | XX.X% |
| `/buyers/chat` | XXX | XXX | XX.X% | XX.X% |

---

## Landing Page Analysis

| Landing Page | Sessions | New Users | Engagement | Bounce |
|--------------|----------|-----------|------------|--------|
| [page] | XXX | XXX | XX.X% | XX.X% |
| ... | ... | ... | ... | ... |

---

## Traffic Sources

| Source | New Users | Sessions | Engagement |
|--------|-----------|----------|------------|
| [source] | XXX | XXX | XX.X% |
| ... | ... | ... | ... |

---

## Critical Findings

### Major Drop-offs

1. **[Stage A] → [Stage B]: X.X%** ([Severity])
   - [X] users at stage A, only [Y] proceeded
   - [Explanation of the issue]

2. **[Stage B] → [Stage C]: X.X%** ([Severity])
   - [Explanation]

### Positive Signals

- [Positive finding 1]
- [Positive finding 2]

---

## Alerts

- [Alert 1: e.g., "Trial traffic significantly decreased (-XX%)"]
- [Alert 2: e.g., "Signup completion rate is 0%"]
- [Alert 3: e.g., "Landing page /producers has 62% bounce rate"]

---

## Funnel Benchmarks vs Actuals

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| First Visit → Trial | >10% | X.X% | [Below/On/Above] target |
| Trial → Tool Select | >70% | XX.X% | [Below/On/Above] target |
| Tool → Search | >80% | XX.X% | [Below/On/Above] target |
| Search → CTA Click | >30% | XX.X% | [Below/On/Above] target |
| CTA → Signup | >50% | XX.X% | [Below/On/Above] target |
| Overall Conversion | >5% | X.X% | [Below/On/Above] target |

---

## Recommendations

### Immediate Actions (High Priority)

1. **[Action 1]**
   - [Specific recommendation based on data]

2. **[Action 2]**
   - [Specific recommendation]

### Medium-term Improvements

3. **[Action 3]**
   - [Recommendation]

4. **[Action 4]**
   - [Recommendation]
```

---

## Benchmarks Reference

### Target Conversion Rates

| Stage Transition | Target | Alert Threshold |
|------------------|--------|-----------------|
| First Visit → Trial Page | >10% | <5% |
| Trial Page → Tool Selected | >70% | <50% |
| Tool Selected → Search Completed | >80% | <60% |
| Search → Signup CTA Click | >30% | <15% |
| Signup CTA → Signup Complete | >50% | <30% |
| **Overall: First Visit → Signup** | >5% | <2% |

### Page Benchmarks

| Page | Target Engagement | Target Bounce |
|------|-------------------|---------------|
| Homepage `/` | >60% | <40% |
| Trial `/trial` | >80% | <20% |
| Signup `/signup` | >90% | <15% |
| Landing pages | >50% | <50% |

---

## Alert Conditions

Automatically flag these conditions:

1. **Critical**: Overall conversion rate <1%
2. **Critical**: Signup CTA → Complete rate = 0%
3. **Warning**: Trial page views down >30% week-over-week
4. **Warning**: Any landing page bounce rate >60%
5. **Warning**: First Visit → Trial <5%
6. **Info**: Traffic spike without corresponding signup increase

---

## Compare Mode (`/funnel-report compare`)

When running in compare mode, run additional queries:

### Query 6: This Week vs Last Week Funnel

```
mcp__analytics-mcp__run_report:
  property_id: 496541587
  date_ranges:
    - {start_date: "7daysAgo", end_date: "yesterday", name: "ThisWeek"}
    - {start_date: "14daysAgo", end_date: "8daysAgo", name: "LastWeek"}
  dimensions: ["eventName"]
  metrics: ["eventCount", "totalUsers"]
  dimension_filter:
    filter:
      field_name: "eventName"
      in_list_filter:
        values: [
          "first_visit",
          "trial_page_view",
          "trial_tool_selected",
          "trial_search_completed",
          "trial_signup_cta_clicked",
          "signup_completed"
        ]
        case_sensitive: true
  order_bys: [{metric: {metric_name: "eventCount"}, desc: true}]
```

**Compare Output Format**:

```markdown
## Week-over-Week Comparison

| Stage | This Week | Last Week | Change |
|-------|-----------|-----------|--------|
| First Visit | XXX | XXX | ±XX% |
| Trial Page | XXX | XXX | ±XX% |
| Tool Selected | XXX | XXX | ±XX% |
| Search Completed | XXX | XXX | ±XX% |
| Signup CTA | XXX | XXX | ±XX% |
| Signup Complete | XXX | XXX | ±XX% |

### Trend Analysis
- [Insight about week-over-week changes]
```

---

## Calculation Formulas

```
Step Conversion Rate = (Users at Step N) / (Users at Step N-1) × 100

Overall Conversion Rate = (Users at Final Step) / (Users at First Step) × 100

Bounce Rate = Sessions with single page view / Total sessions × 100

Engagement Rate = Engaged sessions / Total sessions × 100
```

---

## Related Skills

- `/analytics daily` - Quick daily traffic summary
- `/analytics weekly` - Comprehensive weekly analysis
- `/analytics sources` - Deep dive into traffic sources
- `/health-check` - Verify system health
