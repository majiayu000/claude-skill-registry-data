---
name: teach
description: Teach a concept in small paced lessons with hands-on commands. Use when the user wants to learn or understand a topic, says "explain", "teach me", "I don't understand", or "I am overwhelmed" — or to resume a previous learning topic.
argument-hint: "What do you want to learn?"
---

# Teach

Paced, stateful teaching. The failure mode this skill exists to prevent: a
comprehensive wall-of-text dump. Never do that, even if asked a broad question —
break it down instead.

## State

Lessons persist in `.teaching/<topic-slug>.md` in the repo root (create the
directory on first use and offer to add `.teaching/` to `.gitignore`). Each topic
file holds: the lesson plan with per-lesson status (`pending` / `done` /
`struggled`), and a short log of what tripped the user up. On invocation, list
existing topic files — if one matches, resume where it left off.

## Protocol

1. **Gauge first.** One question about what they already know. Not a quiz — just
   enough to pitch the level.
2. **Plan small.** Break the topic into 5–8 lessons, each covering exactly one
   concept. Write the plan to the topic file and show it as a one-line-per-lesson
   list.
3. **One lesson per turn.** A lesson is: the concept in plain language (a few
   sentences, no jargon without defining it), one hands-on command or exercise —
   preferably against this repo so it's real — and one check question. Then stop
   and wait.
4. **Adapt.** If the answer to the check question wobbles, mark the lesson
   `struggled`, re-explain a different way, and do not advance. If the user says
   they're overwhelmed at any point, halve the lesson size.
5. **Record.** Update the topic file after every lesson so a future session can
   resume cold.

## Rules

- Never more than one concept per turn, no matter how the user phrases the ask.
- Ground examples in the grenmet codebase whenever the topic allows.
- Analogies before acronyms; define every term on first use.
- End each session by showing the plan with progress marked, so the user sees
  movement.
