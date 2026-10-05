---
name: weekly-reverse-review
description: "Reverse weekly review for turning inbox noise, daily plans, diaries, calendars, annual plans, and long-range life plans into one happiness-and-peace-centered weekly plan. Use when the user asks for 週檢視, 反向週計劃, 8 Big Rocks, Inbox Zero weekly review, 幸福寧靜週, or wants to synthesize Todoist/inbox notes, daily diaries, calendars, yearly plans, and life plans into iMandalArt/FIRE/JSON outputs."
---

# Weekly Reverse Review

## Purpose

Turn one week of evidence into the next week's meaningful plan by asking:

`Is this making me prove myself, or bringing real happiness and peace?`

This skill is a reverse planning skill. It does not start by adding tasks. It first gathers evidence from life, removes noise, checks long-range meaning, then produces a compact weekly plan.

## Core Principle

Use the center phrase `幸福寧靜週` unless the user gives another five-Han-character center.

Default final question:

`那件事情能帶來真正的幸福與寧靜？`

Default operating sentence:

`少說，陪伴，慢慢做。`

## Inputs

Gather only the sources available in the user request or local context:

- Inbox or Todoist export: loose tasks, reminders, and noise.
- Daily plan / diary / calendar: what actually happened.
- Year plan / hundred-year life plan: long-range meaning and values.
- Existing weekly plan: user's human-made 8 Big Rocks.
- Photos, social posts, TheBrain, AIDA, or other record stores when provided.

When source files are present, read them before synthesizing.

## Skill Connections

Use these skills when available and relevant:

- `fire-analysis-card`: semantic analysis, numbering, index, route, evolution.
- `imandalart`: final 2.01 hard-line weekly 3x3 card.
- `todays-daily-plan`: daily plan and diary extraction.
- `markdown-nine-grid-clipboard`: Markdown table version of the weekly card.
- `project-note-json-to-epub`: publishing-ready project-note JSON when weekly reviews become manuscript material.
- Calendar skills or apps: calendar evidence, not planning fantasy.

## Workflow

1. **Collect evidence**
   - Inbox: what is asking for attention?
   - Diary/calendar: what actually happened?
   - Year/life plan: what matters over a longer arc?
   - Existing weekly plan: what the human brain already chose.

2. **Detect imbalance**
   - Identify the strongest domain.
   - Identify domains being swallowed by the strongest domain.
   - Health, leisure, and finance often need explicit minimum actions.

3. **Reverse-check motives**
   - Is this for proving myself?
   - Is this for real happiness and peace?
   - Does this support family, friendship, service, health, or meaningful work?
   - What should be deleted, delayed, delegated, or downgraded?

4. **Choose weekly rocks**
   - Keep eight domains, but make each domain evidence-backed.
   - Give every weak domain a minimum viable action.
   - Convert people meetings into `person / theme / next step` cards.
   - Convert writing progress into at most three manuscript cards.

5. **Produce outputs**
   - Short recommendation.
   - FIRE-style semantic summary when requested or when enough evidence exists.
   - iMandalArt weekly card in the fixed weekly layout.
   - Optional JSON using `references/output-json-schema.md`.

## Fixed Weekly Layout

When generating iMandalArt weekly plans, use the user's weekly-domain layout, not the default process layout:

```text
Ⓕ內在　Ⓒ財流　Ⓖ學習
...
...

Ⓑ工作　◎◎◎◎◎　Ⓓ家庭
...　幸福寧靜週　...
...　◎◎◎◎◎　...

Ⓔ社群　Ⓐ健康　Ⓗ休閒
...
...
```

Read `references/weekly-eight-domain-layout.md` for the full mapping and phrase guidance.

## Reverse Questions

Before finalizing, ask internally:

- Which one thing brings the most genuine happiness and peace?
- What can be smaller and still count?
- Which domain needs a minimum action rather than a heroic plan?
- Which relationship needs presence instead of advice?
- Which writing task becomes a card instead of a vague ambition?

Read `references/reverse-review-questions.md` when the review needs deeper diagnosis.

## Default Output

For a normal weekly review, return:

1. One concise diagnosis.
2. One iMandalArt weekly card.
3. Three minimum actions.
4. Three cards to keep or publish.
5. One short "do less" note.

Do not over-explain unless the user asks for a full analysis.

## Quality Rules

- Prefer evidence from files over generic productivity advice.
- Do not optimize only for achievement; optimize for happiness, peace, service, health, and meaningful work.
- Keep the weekly plan small enough to live.
- Mark uncertain claims as `待證`, `推論`, or `需補`.
- If writing or tool-building dominates, explicitly protect health, leisure, and finance.
- If relationships appear, turn them into presence and next-step cards, not contact chores.
