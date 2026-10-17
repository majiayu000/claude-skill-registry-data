---
name: pm-weekly-update
created_by: Aman Parmar
last_modified: 20-04-2026
description: |
  Generate weekly or monthly status updates from local PM data. Use this skill when:
  - It's end of week and you need a status update for leadership or stakeholders
  - You need a monthly executive summary
  - You want to draft an email update using data from meetings, tracker tickets, and decisions
  - The user says "weekly update", "status report", "what happened this week?", "weekly summary"
  - The user says "Friday update", "send status email", "EOW update"
  Pulls from work logs, meetings, ticket tracker, and decisions — no manual input needed.
---

# PM Weekly / Monthly Update Generator

Generate structured status updates by reading local PM data from `.local/`. No manual input needed — everything is pulled from synced data.

## Prerequisites

Before generating an update, ensure data is fresh:
1. Refresh ticket-tracker data (e.g., `/pm-sync` if available)
2. Ensure meetings from the period are processed

If data looks stale (e.g., sprint file is from 3 days ago), warn the user and offer to sync first.

## Weekly Update Workflow

### Step 1: Gather Data

Read these files from `.local/`:

| Source | File | What to Extract |
|--------|------|-----------------|
| Sprint progress | `tracker/sprints/<active-sprint>.md` | Points done vs total, issues moved |
| Meetings | `meetings/processed/*.md` (this week only) | Meeting count, key discussions |
| Action items | `meetings/meeting-action-items.md` | New items this week, closed items |
| Decisions | `decisions/decision-log.md` | Decisions made this week |
| Epics | `tracker/epics.md` | Epic-level progress |

Also cross-reference meetings for this week to ensure completeness (list meetings with a `this_week` time range, compare against processed files).

Also pull from the ticket-tracker API directly for most current data:
- Tickets created this week: `project = [PROJECT_KEY] AND created >= startOfWeek()`
- Tickets resolved this week: `project = [PROJECT_KEY] AND resolved >= startOfWeek()`
- Tickets in progress: `project = [PROJECT_KEY] AND status = "In Progress"`

### Step 2: Generate the Update

Write to `.local/updates/weekly/YYYY-WNN.md`:

```markdown
# Weekly Update — Week N (Mon DD – Fri DD, Month YYYY)

> Project: [your project] ([PROJECT_KEY])
> Author: [your name]
> Generated: DD-MM-YYYY

## Sprint Progress: "<Sprint Name>"
- **Velocity**: X/Y story points completed (Z%)
- **Issues**: A done, B in progress, C to do (of D total)

### Completed This Week
| Key | Summary | Type | Points |
|-----|---------|------|--------|
| [PROJECT-XX] | ... | Story | 3 |

### In Progress
| Key | Summary | Assignee | Points |
|-----|---------|----------|--------|
| [PROJECT-XX] | ... | Name | 5 |

### Blocked / At Risk
| Key | Summary | Blocker |
|-----|---------|---------|
<!-- If any -->

## Key Decisions
| Decision | Context | Date |
|----------|---------|------|
| ... | From meeting X | Mon |

## Meetings This Week
- **Mon**: <Meeting title> — <1-line summary>
- **Tue**: <Meeting title> — <1-line summary>
- ...

## Action Items Status
- **New this week**: X items
- **Closed this week**: Y items
- **Still open**: Z items

## Risks & Blockers
<!-- From decisions log and meetings -->

## Next Week Focus
<!-- Infer from in-progress items and upcoming meetings -->
```

### Step 3: Generate Shareable Formats

Also produce a **short version** for Slack/email at the bottom of the file:

```markdown
---

## Slack / Email Version

**[your project] — Week N Update**

Sprint: X/Y pts done (Z%)
- <Top 3 things completed>
- <Top 3 things in progress>
- <Any blockers>

Decisions: <1-2 key decisions>
Next week: <Focus areas>
```

### Step 4: Offer to Send

After generating, ask:
- "Update saved. Want me to draft an email version for leadership?"
- If yes, write a polished email to `.local/mail/drafts/weekly-YYYY-WNN.md`

## Monthly Executive Summary Workflow

When the user asks for a monthly summary:

### Step 1: Gather Monthly Data
- Read all weekly updates from `.local/updates/weekly/` for the month
- Read all decisions from the month
- Pull tracker data: tickets created/resolved in the month

### Step 2: Generate Summary

Write to `.local/updates/monthly/YYYY-MM.md`:

```markdown
# Monthly Executive Summary — <Month YYYY>

> Project: [your project] ([PROJECT_KEY])
> Author: [your name]

## Highlights
- <Top 3-5 achievements this month>

## Sprint Summary
| Sprint | Planned (pts) | Completed (pts) | Velocity |
|--------|--------------|-----------------|----------|
| Sprint N | X | Y | Z% |

## Key Metrics
- **Tickets created**: X
- **Tickets resolved**: Y
- **Story points delivered**: Z
- **Active epics**: N

## Major Decisions
| Decision | Date | Impact |
|----------|------|--------|
| ... | ... | ... |

## Risks & Mitigations
| Risk | Status | Mitigation |
|------|--------|------------|

## Next Month Focus
- <Planned epics/features>
- <Key milestones>
```

## Important Rules

1. **Data-driven** — every claim must be backed by a ticket, meeting note, or decision log entry
2. **No fluff** — stakeholders want facts, not filler
3. **Highlight blockers** — never hide problems. Surface them with proposed mitigations
4. **Keep it scannable** — tables over paragraphs, bullets over prose
5. **Time-box data** — only include data from the relevant period (week/month)
6. **Always offer the short version** — stakeholders read chat more than docs

## Anti-Patterns

1. **Fabricating numbers** when data is missing — always cite source or mark "data unavailable"
2. **Rewriting the same narrative** for both weekly and monthly — roll up, don't repeat
3. **Listing every ticket** instead of aggregating — stakeholders want signal, not a changelog
4. **Hiding blockers** to make the update look better — surfacing risks builds trust

## Quality Checklist

- [ ] Every metric has a source (ticket ID, meeting file, decision log)
- [ ] Blockers and risks are explicitly called out
- [ ] Short version (Slack/email) is present alongside the full update
- [ ] Dates are formatted DD-MM-YYYY
- [ ] Ticket IDs are hyperlinked to the tracker
- [ ] Next-week focus is inferred from in-progress items, not invented
