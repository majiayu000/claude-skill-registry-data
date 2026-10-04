---
name: user-journey
description: Build a persona-grounded user journey map for a product flow
argument-hint: "[flow or task the user is trying to complete]"
---

# User Journey

You help map a user journey for a specific task or flow. The output is a markdown journey artifact that names the persona, walks through stages, and highlights friction, emotion, and opportunities.

## Input

The user provides via `$ARGUMENTS`:
- A short description of the task or flow (e.g., "first-time API integration", "renewing a subscription", "handling a support escalation")

## Workflow

### 1. Pick the persona

Read `research/personas/` to see what personas exist.

**If one persona clearly matches**: confirm with the user - "I'll ground this journey in [[persona]]. OK?"

**If multiple could match or none exists**: ask the user which persona to use via `AskUserQuestion`, offering personas from `research/personas/` plus an "Other - I'll describe it" option.

**If no personas exist yet**: prompt the user to run `/personalize --deep` or describe the persona in a short paragraph. Build the journey with an inline persona description at the top.

### 2. Define the task and its boundaries

Clarify in ONE `AskUserQuestion` round (skip any that are already answered):

- **Starting point**: what triggers the user to begin this journey? (A specific event, not "they want to use the product".)
- **End state**: what does "done" look like? (A specific measurable outcome.)
- **Context**: time pressure, skill level, tools available.
- **Happy path or full path**: do we map the ideal flow or include edge cases?

### 3. Map the journey

Produce a table-and-prose journey map with these columns:

| Stage | What the user does | What the user thinks | What the user feels | Friction / opportunity |
|-------|--------------------|-----------------------|----------------------|-------------------------|

Keep stages at the right level of granularity - for most journeys, 5-8 stages is the sweet spot. Fewer misses detail; more turns into a task list.

For each stage:
- **What the user does**: concrete action.
- **What the user thinks**: internal voice, first-person.
- **What the user feels**: emotion in one or two words.
- **Friction / opportunity**: what's slow, confusing, or a moment of truth - and what could be improved.

Use specific, first-person voice ("I paste my API key and...") over generic ("The user enters credentials...").

### 4. Highlight the 2-3 biggest moments of truth

A "moment of truth" is a stage where the user's experience makes or breaks their trust in the product. Below the table, call out the 2-3 most critical:

```
### Moments of truth

1. **[Stage name]**: Why it's critical, what good looks like, what bad looks like.
2. ...
```

### 5. Propose opportunities and experiments

In the last section, list 3-5 concrete things to improve the journey. For each:
- What the opportunity is.
- What experiment would validate the fix.
- Rough effort (small / medium / large).

These feed into `/opportunity-solution-tree` or a follow-up epic.

### 6. File location and naming

- **Folder**: `research/journeys/`. Create if it doesn't exist.
- **Filename**: `YYYY-MM-DD - [Persona] - [Flow].md`. Example: `2026-04-20 - Dana (Backend Dev) - First API Integration.md`.
- **Frontmatter**: `tags: Journey`, `persona: [[persona file]]`, `created: YYYY-MM-DD`.

### 7. Link the journey

- **Daily journal**: under `## Notes`.
- **Related epic**: if this journey was built for a specific epic, add a link in that epic's `## Breakdown > Scope` section.
- **Persona file**: append a reference to the journey at the bottom of the persona's Research Sources section.

### 8. Output summary

```
✅ Journey mapped: [[YYYY-MM-DD - Persona - Flow]]
✅ Linked in today's journal
[if epic] ✅ Linked in [[Epic]]

Persona: [[persona]]
Stages: [N]

🎯 Moments of truth:
1. [Stage name]
2. [Stage name]

💡 Top opportunity: [One-line summary]

Next step: run `/opportunity-solution-tree` to explore solutions for the top opportunity.
```

## Notes

- **First-person voice beats third-person.** Readers feel the journey more when it's "I" instead of "the user".
- **Emotion matters.** A journey map without emotion is just a flowchart.
- **One persona per journey.** If a journey serves multiple personas, the stages and friction are usually different - build a separate map per persona and compare.
- **Not a full feature spec.** The journey highlights where the problems are; the epic describes what to build about them.
