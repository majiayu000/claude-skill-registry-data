---
name: schedule-management
description: |
  Legacy/migration guidance for v1 Schedule entities. In v2, define
  recurring cadences as Binding(type=time-window) records with recurrence
  conditions instead of creating new Schedule records.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-schedule-management
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: processkit
    layer: 3
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
    provides:
      primitives: [Schedule]
      templates: [schedule]
---

# Schedule Management

## Intro

In v1, a Schedule was a time-based trigger describing when a process or
reminder should fire. In v2, Schedule is not a first-class primitive
authoring surface. Use `Binding(type=time-window)` with recurrence
conditions, and let an external runner perform execution.

## Overview

### v2 shape

```yaml
---
apiVersion: processkit.projectious.work/v2
kind: Binding
metadata:
  id: BIND-daily-standup-window
  created: 2026-04-06T00:00:00Z
spec:
  type: time-window
  subject: BACK-daily-standup-run
  target: ART-daily-standup-recurrence
  conditions:
    recurrence_rule: "FREQ=DAILY;BYHOUR=9;BYMINUTE=0"
    timezone: Europe/Berlin
---
```

### Workflow

1. Pick the WorkItem, Scope, or Artifact governed by the time window.
2. Create or reuse an Artifact for the recurrence contract if the rule
   needs a durable definition.
3. Create a `time-window` Binding with `conditions.recurrence_rule`.
4. Include `conditions.timezone` when wall-clock time matters.
5. Let the external runner read active time-window Bindings.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Time window without timezone.** "Daily at 9am" is meaningless
  across DST boundaries and timezone-distributed teams. Always
  specify the timezone explicitly (`UTC`, `Europe/Berlin`, etc.).
  Time windows without timezone drift twice a year.
- **Recurring time window without an end date or `until`.** Some
  cadences genuinely run forever; others should end with the
  project, the quarter, or the team member's tenure. Make the
  termination condition explicit, even if it's "indefinite" — the
  decision to make it indefinite is itself a decision worth
  recording.
- **Forgetting to handle missed runs.** What happens if the
  time window fires but the action fails? Does it retry? Skip? Page
  oncall? A cadence without a missed-run policy silently
  accumulates errors.
- **Time window fires without an action target.** A time-window Binding must
  point at a WorkItem, Scope, Artifact, or other actionable
  artifact. "Trigger something at 9am" with no target is a
  reminder, not a durable cadence.
- **Confusing cadence definition vs execution.** The time-window
  Binding defines WHEN something fires; the actual fire events
  should be LogEntries (`schedule.fired`). Don't put execution
  history in the Binding itself.
- **Hand-rolled cron expressions instead of using the schema.**
  Cron strings are infamous for off-by-one errors (every 5
  minutes vs every minute past the 5th). Use structured recurrence
  fields or an explicit recurrence rule when possible;
  reserve cron strings for cases the schema can't express.
- **Cadence that overlaps with another.** "Daily standup at 9am"
  and "weekly review at 9am Monday" both fire at 9am Monday. Be
  explicit about precedence — does one preempt the other, do
  both run, or does the agent skip one?

## Full reference

### Fields

| Field       | Type         | Notes                                              |
|-------------|--------------|----------------------------------------------------|
| `name`      | string       | Kebab-case identifier                              |
| `description` | string     | Human-readable                                     |
| `cadence`   | enum         | `daily`/`weekly`/`monthly`/`quarterly`/`adhoc`/`custom` |
| `cron`      | string       | Standard cron expression                           |
| `timezone`  | string       | IANA timezone name                                 |
| `triggers`  | list[object] | What fires: processes, reminders, events           |
| `active`    | bool         | `false` = suspended                                |
| `last_run`  | datetime     | Advisory — set by whoever runs the schedule        |
| `next_run`  | datetime     | Advisory                                           |

### Execution

processkit does NOT execute cadences. It describes them. An external
runner (GitHub Actions, cron, a human, an agent on a loop) reads active
`time-window` Bindings and fires the target at the right time.

### Scoped cadences

A daily standup runs in one scope, not globally. Use the governed Scope
or a scoped WorkItem as the Binding subject:

```yaml
kind: Binding
spec:
  type: time-window
  subject: SCOPE-project-x
  target: ART-daily-standup-recurrence
```

Then the runner fetches active time-window Bindings for the scope it is
acting on.
