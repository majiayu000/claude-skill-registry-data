---
name: vault-activity
description: Get a summary of vault activity over a period. Triggers on "activity summary", "vault activity", "what happened this week", "editing patterns".
auto_trigger: true
trigger_keywords:
  - "activity summary"
  - "vault activity"
  - "what happened this week"
  - "editing patterns"
  - "recent activity"
  - "activity report"
  - "work summary"
  - "how active"
  - "what's happening"
  - "editing history"
  - "activity log"
  - "work history"
  - "productivity"
  - "how much editing"
  - "vault changes"
allowed-tools: mcp__flywheel__get_activity_summary
---

# Vault Activity Summary

Get a comprehensive summary of vault editing activity over a time period.

## When to Use

Invoke when you want to:
- Understand your recent vault activity
- See editing patterns and trends
- Prepare weekly/monthly reviews
- Track productivity

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `days` | No | 7 | Number of days to analyze |

## Process

### 1. Parse User Input

Identify the time period:
- "show vault activity this week"
- "what have I been working on lately?"
- "activity summary for the last 30 days"
- "how active has my vault been?"

### 2. Call MCP Tool

```
mcp__flywheel__get_activity_summary(
  days: 7
)
```

### 3. Format Results

```
Vault Activity Summary
=================================================

Period: Last 7 days (2025-12-24 to 2025-12-31)

-------------------------------------------------

Overview:
  Notes modified:     42
  Notes created:       8
  Total edits:       127
  Avg edits/day:      18

-------------------------------------------------

Daily Breakdown:

  Date          Modified  Created  Edits
  ────────────────────────────────────────
  2025-12-31       12        2       28   ████████
  2025-12-30        8        1       19   █████
  2025-12-29        6        0       15   ████
  2025-12-28        4        2       12   ███
  2025-12-27        3        0        8   ██
  2025-12-26        5        1       14   ████
  2025-12-25        2        1        6   ██
  2025-12-24        2        1        5   █

Most active day: 2025-12-31 (28 edits)
Quietest day: 2025-12-24 (5 edits)

-------------------------------------------------

Activity by Folder:

  Folder              Notes   % of Activity
  ────────────────────────────────────────
  daily-notes/          7        17%
  projects/            12        29%
  tech/                 8        19%
  work/                 6        14%
  personal/             5        12%
  other                 4         9%

-------------------------------------------------

Most Active Notes (by edit count):

  1. projects/Alpha.md           (15 edits)
  2. daily-notes/2025-12-31.md   (12 edits)
  3. tech/frameworks/React.md     (8 edits)
  4. work/projects/Beta.md        (7 edits)
  5. personal/goals/2026.md       (6 edits)

-------------------------------------------------

Patterns Detected:

  📈 Trending up: 68% more activity in last 3 days
  🕐 Peak hours: 14:00-18:00 (afternoon focus)
  📁 Focus area: projects/ folder (29% of activity)
  🔄 Consistent: Daily notes updated each day

-------------------------------------------------

Week Summary:
  Strong activity week with focus on project work.
  End-of-year push visible in 2025-12-31 spike.

=================================================
```

**Low Activity Period:**
```
Vault Activity Summary
=================================================

Period: Last 7 days (2025-08-01 to 2025-08-07)

-------------------------------------------------

Overview:
  Notes modified:      5
  Notes created:       1
  Total edits:        12
  Avg edits/day:     1.7

⚠️ Lower than usual activity

-------------------------------------------------

Daily Breakdown:

  Date          Modified  Created  Edits
  ────────────────────────────────────────
  2025-08-07        2        0        3   █
  2025-08-05        1        0        2   █
  2025-08-03        1        1        4   █
  2025-08-01        1        0        3   █

No activity: 2025-08-02, 2025-08-04, 2025-08-06

-------------------------------------------------

Suggestions:
  - Vacation period? This is normal for breaks
  - Check if sync issues occurred
  - Review stale notes with /vault-stale

=================================================
```

## Time Periods

| Days | Use Case |
|------|----------|
| 7 | Weekly review |
| 14 | Bi-weekly check |
| 30 | Monthly summary |
| 90 | Quarterly review |

## Use Cases

- **Weekly review**: "Show activity for my weekly summary"
- **Productivity tracking**: "How active have I been?"
- **Pattern discovery**: "What are my editing patterns?"
- **Session-start context**: Used in greeting workflow

## Integration

Works well with other skills:
- **vault-concurrent**: Deep dive into specific sessions
- **vault-stale**: Find notes that need attention
- **rollup**: Include in periodic summaries
- **vault-health**: Combine with structural health

---

**Version:** 1.0.0
