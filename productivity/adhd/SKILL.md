---
name: adhd
description: Support ADHD-style working memory, initiation, and attention patterns with external scaffolding and task design.
category: productivity
aliases:
- adhd-assistant
- attention
- working-memory
- executive-function
triggers:
- ADHD
- I have ADHD
- I just remembered
- I started something else
- I can't remember what I was doing
- I have 100 tabs open
- executive function
- I keep losing track
keywords:
- adhd
- attention
- working
- memory
- hyperfocus
- executive
- function
- distract
- initiat
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- scaffolding
- working-memory
- task-design
- attention
- reminder
- external-structure
inputs:
- task
- attention-state
- context
outputs:
- scaffold-plan
- reminder
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
- adhd
- attention
- memory
- productivity
- working
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# ADHD

## Purpose

Provide practical, kind, non-medical scaffolding for users with ADHD-style attention and
initiation patterns. The skill externalizes working memory, breaks initiation barriers, and
designs tasks that fit attention shape.

## When to Use

- User self-identifies as having ADHD or ADHD-like patterns
- User describes chronic initiation problems
- User describes chronic working-memory loss (forgetting tasks mid-step)
- User describes hyperfocus followed by collapse
- User has many parallel threads and can't pick

## When NOT to Use

- This is NOT a diagnostic tool. Do not diagnose.
- For medication or treatment decisions, route to a clinician.
- For acute crisis, prioritize safety resources.

## Capabilities

- Externalize working memory: write everything down, leave nothing in head
- Break tasks to fit 5–15 minute windows
- Suggest environmental scaffolding: visible cues, body doubling, timers
- Handle task-switching: parking-lot lists, transition rituals
- Support hyperfocus awareness: prep food/water, set hard stop alarms
- Reduce shame: reframe executive-function lapses as design problems, not character flaws

## Inputs

- Current task or goal
- Typical attention window
- Known triggers and patterns
- Whether medication is in play (so we don't push beyond window)

## Workflow

1. **Externalize.** Ask: "Where is this task written down?" If nowhere, write it down right now.
2. **Match window.** If the user's window is 10 minutes, design a 10-minute task — not a 60-minute task with a 10-minute slice.
3. **Reduce initiation friction.** Pre-stage materials. Open files. Close distractions. Make the first move the smallest possible.
4. **Use transitions deliberately.** Between tasks, take a 1-minute "transition ritual" — stand, stretch, name what was finished, name what's next.
5. **Plan for hyperfocus.** If hyperfocus is a pattern: set a hard stop alarm, pre-place food and water, set a "decompression" plan for after.
6. **Track patterns, not failures.** Encourage the user to notice *what works* rather than catalog *what doesn't*.

## Tools

- Task list (paper, app, anything visible)
- Visible timer
- Body-doubling (real or virtual)
- Body doubling apps / streams

## Examples

**User:** "I have ADHD and I can't start."
**Response:** "Where is this written down? Let's get it out of your head and onto paper. Then we'll design the smallest first 5-minute move that doesn't require you to remember anything else."

**User:** "I just hyperfocused for 4 hours and forgot to eat."
**Response:** "That happened. Now: hydrate, eat something small, and don't beat yourself up. Next time we can pre-stage food and set a stop alarm at hour 2 — would that help?"

**User:** "I started something else."
**Response:** "That's a sign your attention moved. Quick parking lot: write down what you were doing and what you started. Then we pick one to continue."

## Safety

- This skill is support, not treatment
- Do not provide medical advice
- Encourage professional evaluation if user is undiagnosed and struggling
- Validate the experience; do not minimize

## Source

Custom skill, written for this library. Based on commonly-recommended practices from ADHD coaches
and clinical psychology (Barkley, Brown). Not a substitute for professional care.

## Notes

Pairs with:
- `unlazy` (initiation barrier)
- `focus` (session design)
- `task-decomposition` (window-sized tasks)
- `time-management` (broad planning)