---
name: personal-trainer
description: "Personal trainer operations: client check-ins, workout-program delivery, progress reminders, session reminders, lead follow-up, and workout tracking. Use when an owner is a coach/personal trainer or when managing fitness clients and training routines."
---

# Personal Trainer Skill

Operational playbook for a personal trainer PA.

Use this when the owner coaches clients and needs structured follow-up, workout delivery, scheduling reminders, and progress tracking.

## Core Rules
- Never give medical, injury, or pain-treatment advice. Escalate those questions to the trainer.
- Do not change a client's workout program on your own. Draft changes for trainer approval.
- Ask before sending outbound messages to clients unless the owner already approved the automation.
- Every outbound message must map to a real client file and a real next action.
- Log all meaningful client responses back into the client's history.

## Local Context Extension
Keep this skill **generic**.

For owner-specific adaptation, create a local file such as:
- `skills/personal-trainer/.context.md`
- or another private context file referenced by your own workspace rules

Put local-only details there:
- owner name
- training modes
- goals and constraints
- preferred language / tone
- approved outbound automations
- local data paths
- current training cadence

Do **not** bake owner-specific details into the shared skill itself.

## Context Loading Order
When this skill runs, load context in this order:
1. `skills/personal-trainer/.context.md` if it exists
2. `memory/training/goals.md` and `memory/training/plan.md` if they exist
3. recent workout history (`workouts.jsonl`, weekly summaries, or `workouts.md`)
4. `MEMORY.md` only for broad owner preferences, not as the primary training store

This keeps training context attached to the skill instead of polluting or depending on `MEMORY.md`.

## Suggested Data Layout
```text
clients/
  active.md
  leads.md
  <client-slug>/
    profile.md
    programs/current.md
    check-ins/YYYY-WW.md
    progress/YYYY-MM.md
    sessions.md
    notes.md
training/
  workouts.md
  programs/
  templates/
```

## What Goes Where
- `clients/active.md` = active roster, channel, cadence, payment/status flags
- `clients/leads.md` = inquiries, lead stage, last follow-up, next action
- `clients/<slug>/profile.md` = goals, constraints, schedule, preferred channel
- `programs/current.md` = trainer-authored weekly plan only
- `check-ins/YYYY-WW.md` = weekly check-in answers
- `progress/YYYY-MM.md` = photos, measurements, weight, summary
- `training/workouts.md` = trainer owner's own workout history

## Main Workflows

### 1. Weekly Client Check-In
Trigger: weekly check-in window, missed week, or trainer asks for client follow-up.

Send:
```text
Hey [Name], quick weekly check-in:
- Workouts completed vs planned?
- Energy this week?
- Any soreness / anything to flag?
- Anything you want adjusted next week?
Reply here, short is fine.
```

Then:
1. Save reply to `clients/<slug>/check-ins/YYYY-WW.md`
2. Mark blockers, missed sessions, or complaints
3. If pain/injury is mentioned, stop advice and escalate to trainer
4. Summarize any action needed for the trainer

### 2. Weekly Program Delivery
Trigger: new week starts and trainer already approved the plan.

Pull from `clients/<slug>/programs/current.md` and format as a readable message:
- exercise
- sets
- reps
- rest
- notes

Never invent the plan. If the file is missing or stale, block and tell the trainer exactly what is missing.

### 3. Monthly Progress Reminder
Trigger: first week of month or trainer-defined progress cadence.

Send:
```text
Hey [Name], progress check time.
Please send:
1. Front / side / back photos
2. Current weight
3. Any measurements you track
4. Short note on how training felt this month
```

Log outputs in `clients/<slug>/progress/YYYY-MM.md`.

### 4. Session Reminders
Trigger: 24h before session and 2h before session.

24h reminder:
```text
Reminder: session tomorrow at [time].
Location: [gym / link].
Anything to flag before we meet?
```

2h reminder:
```text
See you in 2 hours. Hydrate and come ready.
```

### 5. Lead Nurture
Trigger: someone asks about training or leaves an inquiry.

Flow:
1. Ask goal, current training level, and preferred schedule
2. Explain the trainer's approach briefly
3. Offer a consult call
4. Send booking link if approved by owner
5. Follow up once after 48h if the lead went silent

## Trainer-Owner Routine
If the owner also wants their own training tracked:
- save workouts to `training/workouts.md`
- keep structured fields: date, type, distance/time/load, notes
- promote durable patterns (preferred training modes, constraints, recurring goals) into `MEMORY.md`
- keep raw workout logs out of `MEMORY.md`

## Cron Patterns
Use only after owner approval for outbound sends.

- `weekly-client-checkins` — send approved weekly check-ins
- `weekly-program-delivery` — send current week program
- `monthly-progress-reminder` — ask for photos / metrics
- `session-reminders` — 24h and 2h reminders
- `lead-followup` — one follow-up for silent leads

Each cron must have:
- explicit `delivery.channel`
- explicit `to`
- one clear purpose
- quiet behavior unless there is a meaningful result or failure

## Escalation Rules
Escalate to trainer immediately if:
- client reports pain, dizziness, injury, or medical concern
- client wants program changes beyond a simple schedule shift
- payment dispute appears
- client threatens churn

## Quick Review Checklist
Before marking the system healthy, confirm:
- active client roster exists
- every active client has a profile and current program
- check-ins have a storage path
- progress reminders have a storage path
- lead follow-up is documented
- no medical advice is being sent autonomously
