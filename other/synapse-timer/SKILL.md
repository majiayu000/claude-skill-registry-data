---
name: synapse.timer
description: "Set countdown timers by duration — acknowledges the request and notes that firing requires the cron system."
version: "1.0.0"
author: "synapse-core"
triggers: ["set a timer", "timer for", "start a timer", "countdown"]
model_hint: "casual"
permissions: []
cloud_safe: true
enabled: true
---

# Timer Skill

You are helping the user set a countdown timer.

## When invoked

The user wants to start a timer for a specific duration (e.g., "set a timer for 10 minutes").

## How to respond

1. **Confirm the timer** — parse the duration from the user's message and confirm it clearly
   (e.g., "Timer set for 10 minutes!").
2. **State when it will fire** — calculate and mention the expected completion time
   (e.g., "That's 3:45 PM" if the current time is 3:35 PM).
3. **Be transparent about notifications** — timer firing with push notifications requires
   the cron system, which will be available in a future update. Let the user know they can
   ask "how long until my timer?" to check remaining time.
4. **Keep it brief** — one or two lines is ideal.

## Duration parsing examples

| User says | Parse as |
|-----------|----------|
| "10 minutes" | 600 seconds |
| "half an hour" | 1800 seconds |
| "45 mins" | 2700 seconds |
| "2 hours" | 7200 seconds |
| "1 hour 30 minutes" | 5400 seconds |

## Example response

"Timer set for 10 minutes (finishes at 3:45 PM). Heads up: push notifications aren't active
yet — ask me 'check my timer' to see the remaining time."

## Notes

- If no duration is specified, ask the user how long the timer should run.
- Do not invent push notification or alarm-sounding capabilities that aren't implemented.
- Timers are recorded in `~/.synapse/timers/` as JSON for portability.
