---
name: flow-metrics-analysis
description: Analyze story and feature cycle time from in-progress to done, correlate with DORA lead time, and identify flow bottlenecks
triggers: [cycle time, flow metrics, story time, in progress to done, throughput, WIP, lead time, flow efficiency, aging work, blocked stories, sprint analysis, delivery flow]
audience: manager, engineer
---

# Flow Metrics Analysis

## Context
DORA's **Lead Time for Changes** measures from code commit to production. But the *full* delivery lead time starts much earlier — when work enters "In Progress". Flow metrics bridge this gap, giving you visibility into where time is actually spent: in queues, blocked, in review, or actively being worked.

This skill analyzes story/feature cycle time data to surface bottlenecks, predict delivery, and connect team-level flow health to your DORA metrics.

**Key concepts:**
- **Cycle Time** — time from "In Progress" (work started) → "Done"
- **Lead Time** — time from "To Do" (item created/committed) → "Done" (broader than cycle time)
- **Throughput** — number of items completed per unit of time (week/sprint)
- **WIP (Work In Progress)** — number of items actively being worked at any moment
- **Flow Efficiency** — % of cycle time spent actively working vs. waiting

---

## Instructions

### Step 1 — Gather the Data
Request or export the following fields per story/ticket for the last 4–12 weeks:

| Field | Description |
|-------|-------------|
| `id` | Ticket ID (e.g., PROJ-123) |
| `title` | Story/feature name |
| `type` | Story / Bug / Spike / Feature |
| `size` | Story points or t-shirt size (if estimated) |
| `created_at` | When the ticket was created |
| `in_progress_at` | When it moved to "In Progress" (cycle time start) |
| `in_review_at` | When it moved to "In Review" (optional but valuable) |
| `done_at` | When it moved to "Done" |
| `blocked_duration_days` | Total days marked as "Blocked" (if tracked) |

Supported data sources: Jira CSV export, Linear export, GitHub Projects, Notion, spreadsheet paste.

---

### Step 2 — Calculate Cycle Time
For each item:
```
cycle_time_days = done_at - in_progress_at
active_time_days = cycle_time_days - blocked_duration_days
flow_efficiency = active_time_days / cycle_time_days × 100%
```

**Compute the distribution** (not just the average — averages hide the truth):
| Percentile | Meaning |
|------------|---------|
| **50th (median)** | Half of stories complete within this time — your typical delivery |
| **85th** | 85% of stories complete within this — use for planning promises |
| **95th** | Near-worst case — use for SLA commitments |

> ⚠️ Never use average cycle time for planning. One outlier (30-day blocked story) skews the average and makes the team look worse than it is. Use the 85th percentile.

---

### Step 3 — Identify Bottlenecks

**Aging WIP Analysis**
Flag any item in "In Progress" or "In Review" that has exceeded the 85th percentile cycle time without moving to Done. These are your at-risk items.

```
aging_threshold = 85th_percentile_cycle_time
at_risk = items where (today - in_progress_at) > aging_threshold AND status != "Done"
```

**Stage Time Breakdown** (if `in_review_at` is available)
```
dev_time      = in_review_at - in_progress_at
review_time   = done_at - in_review_at
wait_time     = blocked_duration_days
```

If `review_time > dev_time`: review is the bottleneck — increase reviewer availability or reduce PR size.  
If `blocked_duration_days` is high: dependency or requirements issues — flag for process change.

**WIP Limit Check**
Plot daily WIP (items in "In Progress") over the period. If WIP is consistently high:
- Little's Law: `Cycle Time = WIP ÷ Throughput`
- Reducing WIP directly reduces cycle time — it's the highest-leverage lever

Recommended WIP limit per engineer: **1–2 items**. Teams that limit WIP see 30–50% cycle time reductions.

---

### Step 4 — Connect to DORA

| Flow Metric | DORA Connection |
|-------------|----------------|
| Cycle Time (in-progress → done) | Precursor to **Lead Time for Changes** — if cycle time is high, DORA lead time will be too |
| Throughput (stories/week) | Correlates with **Deployment Frequency** — if you ship fewer stories, you deploy less often |
| Flow Efficiency | Low efficiency = hidden queue time inflating **Lead Time for Changes** |
| Blocked duration | Correlates with **Change Failure Rate** — blockers often indicate unclear requirements → bugs in production |

---

### Step 5 — Produce the Report

**Team Flow Summary (per 4-week period):**
```
Period: [date range]
Items analyzed: N
Throughput: X items/week (trend: ↑ / ↓ / →)

Cycle Time Distribution:
  50th percentile (median): X days
  85th percentile:          X days  ← use this for planning
  95th percentile:          X days

Flow Efficiency: X%  (industry benchmark: 15–40% is typical; > 40% is excellent)

Stage Breakdown (if available):
  Avg dev time:    X days
  Avg review time: X days
  Avg blocked:     X days

Aging WIP (at risk):
  [PROJ-123] — "Feature X" — 14 days in progress (85th pct: 8 days) → ESCALATE
  [PROJ-456] — "Bug Y" — 11 days in progress → MONITOR

WIP at time of analysis: X items in flight
Recommended WIP limit: X items (current team size × 1.5)
```

**Recommended Actions (prioritized):**
1. Highest-leverage improvement based on the data
2. Second improvement
3. Third improvement

---

### Step 6 — Sprint/Iteration Retrospective Use
After each sprint, run this analysis to answer:
- Did cycle time improve or regress vs. last sprint?
- What percentage of committed stories were completed? (Completion rate)
- What was the average age of items carried over?
- Were there outliers? What caused them?

Trend these metrics quarter-over-quarter. Present as: *"Our 85th percentile cycle time dropped from 12 days to 7 days after we introduced WIP limits in Q1."*

---

## Benchmarks (industry reference)
| Team Performance | Median Cycle Time | Flow Efficiency |
|-----------------|-------------------|-----------------|
| Elite | 1–3 days | > 40% |
| High | 3–7 days | 25–40% |
| Medium | 7–14 days | 15–25% |
| Low | > 14 days | < 15% |

*Source: DORA State of DevOps, Kanban Maturity Model*

---

## Principles
- Source: [DORA — Lead Time for Changes](https://dora.dev/guides/dora-metrics-four-keys/)
- Source: [Actionable Agile Metrics — Daniel Vacanti] — cycle time percentiles, WIP limits, Little's Law
- Source: [Project to Product — Mik Kersten] — Flow Framework connecting feature flow to DORA
- Source: [LeadDev — Engineering Metrics](https://leaddev.com)
- Key idea: *"Average cycle time is a vanity metric. The 85th percentile cycle time is a planning tool. The difference between them reveals your risk."*

---

## Output Format
When applying this skill, the agent should:
1. Accept ticket data in any tabular format (CSV, markdown table, JSON, pasted spreadsheet)
2. Calculate cycle time distribution (50th, 85th, 95th percentiles)
3. Identify and list aging WIP items by name, age, and risk level
4. Calculate flow efficiency if blocked time is available
5. Break down time by stage (dev, review, blocked) if stage timestamps exist
6. Connect findings to DORA metric implications
7. Produce the Team Flow Summary report
8. Generate 3 prioritized, specific improvement recommendations

## MCP Integration

**Pull cycle time data via Jira JQL:**
```
jira_search_issues(jql: "project = PROJ AND issuetype in (Story, Bug) AND status changed to Done after '<start_date>' ORDER BY resolutiondate ASC", max_results: 100)
```

**Get age of in-progress items (WIP age):**
```
jira_search_issues(jql: "project = PROJ AND status in ('In Progress', 'In Review') ORDER BY updated ASC")
```

**Calculate throughput for the last N sprints:**
```
jira_search_issues(jql: "project = PROJ AND sprint in closedSprints() AND status = Done AND sprint in sprintsInDateRange('<start_date>', '<end_date>')")
```

**Publish the Team Flow Summary report to Confluence:**
```
confluence_create_page(space_key: "TEAM", title: "Flow Metrics Report — <Month/Quarter>", content: "<team flow summary with charts and recommendations>", parent_page_id: "<metrics_page_id>")
```

**Graceful fallback:** Ask the user to provide CSV/JSON export from Jira. Parse timestamps manually and produce the flow metrics report as Markdown.
