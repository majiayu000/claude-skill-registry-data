---
name: unlazy
description: Activate the user out of procrastination, avoidance, or "I don't want to start" states using tiny first steps and momentum framing.
category: productivity
aliases:
- anti-procrastination
- motivation
- get-started
- just-start
- overcome-procrastination
triggers:
- I'm procrastinating
- I don't want to work
- I keep avoiding this
- I can't get started
- help me start
- I'm being lazy
- I don't feel like it
- I should be working but I'm not
- motivation
keywords:
- procrastinate
- avoid
- lazy
- stuck
- start
- begin
- momentum
- motivation
- avoidant
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- start-task
- momentum
- next-action
- two-minute-rule
- anti-procrastination
- body-doubling
inputs:
- task
- stuck-duration
- attempts
outputs:
- next-action
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
  gemini_cli: true
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- avoid
- lazy
- procrastinate
- productivity
- stuck
- unlazy
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Unlazy

## Purpose

Move a stuck or avoidant user from inertia into a *single, tiny, winnable* action. The skill
does NOT lecture about discipline. It does NOT produce a 10-step plan. It produces the smallest
viable next move that breaks avoidance.

## When to Use

Activate when the user:

- Says they are procrastinating, stuck, or unmotivated
- Has a clear task in front of them but can't start
- Reports "I don't want to", "I keep avoiding", "I'm being lazy"
- Has already articulated a goal but not a next step
- Is in a shame spiral about not having started

## When NOT to Use

- User has an emergency or acute distress (route to a human / professional)
- User genuinely does not know what they want to work on (route to `planning`)
- User is burned out and needs rest (do not push — recommend recovery)
- The "task" is actually a values conflict (route to `decision-making`)

## Capabilities

- Reframe avoidance as data, not failure
- Identify the *smallest* possible first move (often 2 minutes or less)
- Offer concrete momentum builders (timer, accountability, body-doubling prompts)
- Suggest the "5-second rule" or "2-minute rule" frameworks
- Provide a single, named next action — never a list of ten

## Inputs

- The task or subject the user is avoiding (optional but very helpful)
- How long the user has been stuck (optional)
- What the user has already tried (optional)

## Workflow

1. **Acknowledge without judgment.** Avoidance is information, not moral failure.
2. **Identify the target.** Ask: "What specifically are you avoiding?" If unclear, surface 2–3 candidate tasks and let the user pick.
3. **Shrink the first step.** Ask: "What is the *tiniest* version of this that you could do in 2 minutes?" If the user says "I can't even do that," shrink again until they can.
4. **Name the first move.** A single verb phrase, e.g., "Open the file." Not "sketch the outline."
5. **Offer a booster.** Pick one: 5-min timer, body-doubling prompt, accountability text, or environmental change (close tabs, put phone away).
6. **Stop.** Do not produce a roadmap. The next move is enough.

## Tools

- None required. Pure language and structure.

## Examples

**User:** "I'm procrastinating on my essay."
**Response:** "OK. The smallest first move is opening the document and typing your working title.
That's it. Want to do that now, or pick an even smaller step?"

**User:** "I keep avoiding my code review."
**Response:** "Let's shrink it. Instead of reviewing the whole PR, can you read the first 20 lines and write one comment? That's a complete review."

**User:** "I don't want to study."
**Response:** "Sounds like a values check first — do you want to be studying at all? If yes, the smallest version is one practice problem. If no, that's important information and we should talk about why."

## Safety

- Do not pressure users who express burnout or distress
- Do not diagnose ADHD, depression, or anxiety
- Suggest professional support when appropriate
- Do not promise motivation will last — momentum is the goal, not feeling

## Source

Custom skill, written for this library.

## Notes

Pairs naturally with:
- `task-decomposition` (when the task is large)
- `focus` (after the user has started)
- `planning` (when the user lacks direction)