---
name: scheduledprompt
description: Schedule and cancel prompts for the current conversation with the schedule_prompt, cancel_scheduled_prompt, and cancel_all_scheduled_prompts tools. Use whenever the user asks to be reminded of something, wants a recurring nudge, wants the agent to do something later, or wants to stop, cancel, remove, or clear a reminder — for example "remind me to stand up every 30 minutes", "check in on me every morning", "cancel my stand-up reminder", or "clear all my reminders".
metadata:
  author: agent42
  version: "1.0"
---

# Reminders

You can schedule prompts for the current conversation with the `schedule_prompt` tool.
A prompt is a **scheduled instruction**: when it fires, its instruction is sent to you as a user
message in this conversation, and you act on it — your response is saved in the
conversation history for the user to see.

## When to use it

Call `schedule_prompt` whenever the user asks to be reminded about something, wants a
recurring nudge, or wants you to do something later — for example "remind me to stand up
every 30 minutes", "check in on me every morning", or "summarize this conversation in an
hour".

## How reminders behave

- They are backed by Orleans reminders, so they are **durable**: a reminder survives the
  agent being deactivated and the silo restarting, and it belongs to this conversation.
- When a reminder fires, its prompt arrives as a user message **while the user may be
  away**; answer it as a normal turn, addressed to the user, so it reads well when they
  come back.
- A reminder first fires after an initial delay and then **repeats on a fixed interval**;
  Orleans reminders always recur, there is no true one-shot.
- The smallest granularity Orleans supports is **one minute**, so both the initial delay
  and the repeat interval must be at least 1 minute. If the user asks for something
  faster, explain that one minute is the minimum.

## Arguments to provide

- `name` — a short, stable identifier such as `stand-up` or `daily-check-in`. Reusing an
  existing name **updates** that reminder instead of creating a duplicate.
- `prompt` — the instruction you will receive when the reminder fires. Write it as a
  self-contained instruction to your future self, e.g. "Remind the user to stand up and
  stretch." or "Write a short summary of the conversation so far."
- `dueInMinutes` — how long from now the reminder should first fire (must be ≥ 1).
- `repeatEveryMinutes` — how often it repeats after the first firing (must be ≥ 1). For a
  reminder the user wants only once, use a large interval and tell them it will keep
  repeating until it is cancelled.

## After scheduling

Confirm back to the user exactly what you scheduled — when it will first fire, how often
it repeats, and what will happen when it does. Never claim a reminder was set unless the
tool call actually succeeded; if the tool returns an error message, relay it and ask the
user how to adjust.

## Cancelling

To stop a reminder, use the cancel tools:

- `cancel_scheduled_prompt` — cancels **one** reminder. Pass its `name`, the same stable
  identifier used when it was scheduled (e.g. `stand-up`). Use this when the user wants to
  stop a specific reminder. If the name doesn't match a scheduled reminder, the tool says
  so — relay that rather than claiming success.
- `cancel_all_scheduled_prompts` — cancels **every** reminder in this conversation at once.
  Use it only when the user clearly wants to clear all of them, never to cancel a single one.

Both permanently unregister the durable reminder(s) so nothing fires again. After
cancelling, confirm to the user exactly what was cancelled, and only claim a reminder was
cancelled if the tool call actually succeeded.
