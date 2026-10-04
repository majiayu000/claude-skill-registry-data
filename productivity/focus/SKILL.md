---
name: focus
description: Help the user enter and sustain focused work via session design, distraction blocking, and break structure.
category: productivity
aliases:
- deep-work
- concentration
- pomodoro
- focus-session
- get-in-the-zone
triggers:
- help me focus
- I can't concentrate
- I keep getting distracted
- deep work
- pomodoro
- let's do a focus session
- 25 minutes of focus
- I need to concentrate
keywords:
- focus
- concentrate
- distract
- attention
- deep
- work
- pomodoro
- session
- flow
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- focus-session
- deep-work
- distraction-blocking
- pomodoro
- break-structure
inputs:
- duration
- distraction-source
outputs:
- focus-session-plan
permissions:
  filesystem: read
  network: none
  shell: none
  secrets: none
compatibility:
  generic: true
  claude_code: true
  codex: true
  cursor: true
  cline: true
  opencode: true
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- attention
- concentrate
- distract
- focus
- productivity
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Focus

## Purpose

Design a single, well-structured focus session that the user can actually complete. The skill
operates on the *environment* and *session shape* — not on willpower.

## When to Use

- User says "help me focus" or "I can't concentrate"
- User wants to start a timed work session
- User is mid-session and losing focus
- User wants a Pomodoro or similar structure

## When NOT to Use

- User has not yet chosen a task (route to `unlazy` or `planning`)
- User wants help with distractions on the system level (route to `digital-minimalism` or platform-level tools)
- User is dealing with anxiety that blocks focus entirely (suggest professional support)

## Capabilities

- Design a focus session: duration, task, break length
- Recommend focus techniques (Pomodoro, timeboxing, single-task)
- Suggest environmental changes: notifications off, phone away, single tab
- Provide "loss-of-focus" recovery scripts
- Track session shape without requiring apps

## Inputs

- Task the user wants to focus on
- Available time
- Known distractions

## Workflow

1. **Confirm the task.** A focus session needs ONE named task, not "work on stuff."
2. **Set duration.** Default to 25 minutes (Pomodoro). Offer 50 (deep work) or 90 (flow). Adjust based on user energy.
3. **Design the environment.**
   - Phone face-down / in another room
   - One tab or window
   - Water nearby
   - Headphones (with or without music — user preference)
4. **Set the break.** Short breaks are sacred. After 25 min → 5 min. After 50 → 10.
5. **State the success criterion.** "After 25 minutes, I will have [specific output]."
6. **Mid-session recovery.** If focus breaks: name what broke it, write it on a parking-lot list, return to task. Do not start a new task.

## Tools

- Optional: timer (system clock, phone, browser extension)
- Optional: noise / music (white noise, focus playlists)
- Optional: distraction blocker (system-level, requires user setup)

## Examples

**User:** "Help me focus for 30 minutes."
**Response:** "What's the one thing? After 30 minutes, what will you have produced?"

**User:** "I keep losing focus every few minutes."
**Response:** "Let's audit the environment first: notifications, tabs, phone. Then we shrink the session to 10 minutes and add a parking-lot list for the distractions."

## Safety

- Encourage breaks — do not push for marathon sessions
- Warn against sleep-deprived focus attempts
- Respect user autonomy if they say they need to stop

## Source

Custom skill, written for this library.

## Notes

Pairs with:
- `task-decomposition` (large tasks first)
- `adhd` (when focus issues are chronic)
- `time-management` (broader scheduling)