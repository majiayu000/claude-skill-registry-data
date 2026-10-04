---
name: time-tracking
description: "Track time spent across contexts. Use when logging time, checking hours, or when user mentions 'log time', 'time spent', 'hours worked', 'track time'."
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Time Tracking

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Track and report time spent across all contexts.

## Commands

- `/time log {context} {hours} [description]` - Log time
- `/time today` - Today's time across contexts
- `/time week [context]` - Weekly summary
- `/time month [context]` - Monthly summary
- `/time report` - Comprehensive report

## Process

### `/time log {context} {hours} [description]`

1. Validate context exists in registry
2. Find file: `contexts/{context}/time-tracking.yaml`
3. Append entry:
   ```yaml
   entries:
     - date: "YYYY-MM-DD"
       hours: {hours}
       description: "{description}"
       logged_at: "{ISO timestamp}"
   ```
4. Display: logged hours, today total, week total

### `/time today` / `/time week` / `/time month`

1. Scan all `contexts/*/time-tracking.yaml`
2. Filter entries for period
3. Display summary table: Context | Hours | Description (today) or Context | Hours | % (week/month)

### `/time report`

Generate: total hours, working days, average/day, breakdown by context with %, week-over-week comparison.

## File Schema

```yaml
context: {name}
year: 2026
config:
  weekly_target: 40  # null if no target
  billable: false
entries:
  - date: "YYYY-MM-DD"
    hours: 4
    description: "Task description"
    logged_at: "ISO timestamp"
```

## Notes

- Hours in decimals (1.5, 0.5)
- Entries are append-only
- Use with `/dashboard time` for visual summary

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
