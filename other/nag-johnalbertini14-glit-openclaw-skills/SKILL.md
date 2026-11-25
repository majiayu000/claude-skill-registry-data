---
name: nag
description: Persistent reminder system that keeps bugging you until you confirm completion. Use when setting up recurring reminders, nag schedules, or any task that needs follow-up until acknowledged. Handles daily resets, configurable nag windows, escalating urgency, and natural-language confirmation matching. Do NOT use for one-shot reminders (use cron instead) or time-sensitive alerts that need immediate action (use cron with wakeMode now).
---

# Nag — Persistent Reminders

Nag manages reminders that don't give up. Each reminder has a first-fire time, a nag window, and resets daily.

## When to Use

- Recurring daily habits (supplements, workouts, practice)
- Tasks that get ignored/forgotten without follow-up
- Anything where "remind me once" isn't enough

## When NOT to Use

- One-shot reminders ("remind me in 20 minutes") — use a cron job with `schedule.kind: "at"`
- Time-critical alerts that can't wait for a heartbeat cycle
- Reminders that don't need confirmation (informational only)

## Setup

### 1. State File

Create `memory/nag-state.json` in the workspace:

```json
{
  "date": "2026-02-15",
  "reminders": {}
}
```

The date field triggers automatic daily resets — when today's date differs from the stored date, all reminders reset to unconfirmed.

### 2. Reminder Config

Create `nag-config.json` in the workspace root:

```json
{
  "reminders": [
    {
      "id": "morning-supplements",
      "label": "morning supplements",
      "cronFirst": "0 8 * * *",
      "nagAfter": "09:00",
      "confirmPatterns": ["taken", "done", "took them", "did it", "yes"],
      "tone": "friendly but persistent, escalate to ALL CAPS drama after 3 nags",
      "messages": {
        "first": "Time for morning supplements!"
      }
    }
  ]
}
```

**Fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Unique identifier, used as key in state file |
| `label` | yes | Human-readable name for display |
| `cronFirst` | yes | Cron expression for initial reminder (create a cron job for this) |
| `nagAfter` | yes | Time (HH:MM, 24h) after which heartbeat nags begin |
| `confirmPatterns` | yes | Array of phrases that mark the reminder as done (case-insensitive, substring match) |
| `tone` | no | Personality guidance for generating nag messages. If absent, use a neutral friendly tone. The model has creative liberty to vary the wording each nag. |
| `messages.first` | no | Text sent by the cron job for the initial reminder. If absent, generate from label + tone. |
| `messages.nag` | no | Suggested nag text. If absent, generate contextually from label + tone + nagCount. |
| `messages.escalate` | no | Suggested text after 3+ ignored nags. If absent, generate with increased urgency from tone. |
| `days` | no | Array of weekday names to restrict when this reminder fires (e.g. `["monday", "wednesday", "friday"]`). Omit for every day. |

For more examples, see [references/config-examples.md](references/config-examples.md).

**Message generation:** When `messages.nag` or `messages.escalate` are absent, generate them on the fly using the `label` and `tone` fields. Vary the wording each time — don't repeat the same nag verbatim. Use nagCount to calibrate urgency: low count = gentle, 3+ = escalated.

### 3. Wire Up Cron + Heartbeat

**For each reminder**, create a cron job that fires `messages.first` at the `cronFirst` schedule.

**In HEARTBEAT.md**, add a nag check block:

```
## Nag Check
Read nag-config.json and memory/nag-state.json.
For each reminder in nag-config.json:
- If date in state differs from today, reset all reminders (set confirmed: false, nagCount: 0).
- Skip if today's weekday isn't in the reminder's `days` array (if specified).
- If current time is after `nagAfter` and confirmed is false: send a nag message to the user.
  - Generate the message from the reminder's label and tone (or use messages.nag if provided).
  - If nagCount >= 3, escalate urgency (use messages.escalate if provided, otherwise generate with more intensity).
  - Increment nagCount in state.
- Do NOT nag before the nagAfter time.
```

### 4. Confirmation Handling

When the user sends a message matching any `confirmPatterns` for a reminder, update `memory/nag-state.json`:

```json
{
  "date": "2026-02-15",
  "reminders": {
    "morning-supplements": {
      "confirmed": true,
      "confirmedAt": "09:06",
      "nagCount": 1
    }
  }
}
```

Match confirmation by checking if any pattern appears as a substring (case-insensitive) in the user's message. When ambiguous (multiple reminders could match), match the one currently in its nag window.

## Adding a New Reminder

1. Add entry to `nag-config.json`
2. Create a cron job for the `cronFirst` schedule
3. The heartbeat nag block handles everything else automatically

## Removing a Reminder

1. Remove entry from `nag-config.json`
2. Remove or disable the corresponding cron job
3. Optionally clean up its key from `memory/nag-state.json`
