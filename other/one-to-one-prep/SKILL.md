---
name: one-to-one-prep
description: "Generates a structured prep document for monthly 1-on-1 meetings with direct reports.
  Aggregates context from previous meeting notes and task tracker data, tracks action item status,
  and generates prioritized discussion topics with motivation and wellbeing questions. Use when
  preparing for one-on-one meetings, 1:1 check-ins, manager-employee meetings, one-to-one prep,
  1-on-1 agenda generation, preparing for regular reports meetings.
  Russian triggers: подготовь 1-on-1, prep для ван-он-вана, готовлюсь к 1:1, подготовка к встрече
  с сотрудником, сгенерируй агенду для 1-on-1, подготовь встречу один на один."
version: 1.0.0
---

# Skill: one-to-one-prep

A skill for team leads, engineering managers, and department heads. Generates a structured
prep document for monthly 1-on-1 meetings with direct reports, based on previous meeting
notes and task tracker data.

---

## Triggers

**Russian:** «подготовь 1-on-1», «prep для ван-он-вана», «готовлюсь к 1:1», «подготовка к встрече с сотрудником», «сгенерируй агенду для 1-on-1», «one-to-one prep», «подготовь встречу один на один»
**English:** "prep for 1-on-1", "one-to-one prep", "prepare for 1:1", "1-on-1 agenda", "prepare for my one-on-one", "generate 1:1 prep", "one on one meeting prep"

---

## Language Detection

1. Detect the language of the user's first message.
2. If the message is in Russian — use Russian throughout the conversation and in the prep document.
3. If the message is in English — use English throughout the conversation and in the prep document.
4. If the language is ambiguous (mixed text, transliteration) — default to Russian.
5. Language is fixed at the start of the session and does not change until generation is complete.

---

## Input

**Required:**
- Notes from the previous 1-on-1 (free-form text). If absent — activate first-meeting mode.
- Employee task list / activity log for the period since the last meeting (paste from any tracker: Jira, Linear, Asana, ClickUp, Notion, or plain text).

**Optional:**
- Employee career goals
- Individual Development Plan (IDP)
- Current OKRs

If required data is missing — request it before generating.

## Output

Markdown prep document with the following sections:
1. Action item status from the previous 1-on-1
2. Key events of the period
3. Prioritized discussion topics
4. Motivation and wellbeing questions
5. New action items template

---

## Instructions

### Step 1 — Check for Required Data

Verify that the user has provided both required parameters: previous 1-on-1 notes and the task list.

If notes are absent — activate **first-meeting mode**: skip action item tracking and instead generate onboarding questions (expectations from meetings, current priorities, working style).

If the task list is missing — explicitly request it before proceeding.

If the request is clearly outside the skill's scope (write a performance review, rate an employee, create a ranking, etc.) — explain the skill's purpose and offer a specific alternative: "If you'd like to prepare for a meeting where you'll discuss this topic — I can generate a prep document for that context."

### Step 2 — Analyze Previous Meeting Notes

Extract from the notes:
- Action items with dates and owners (if specified)
- Topics left open or requiring follow-up
- Agreements that need to be verified

Goal: identify what needs to be tracked at the current meeting.

### Step 3 — Analyze the Task List

Extract from the task list:
- Completed tasks (status Done / Closed / Completed or equivalent)
- Tasks without progress (no updates for more than 5 working days, deadline passed or approaching)
- Tasks not started (status "not started" / "backlog" / "todo") that should already be in progress given the period context — flag as potential risk
- Blockers — explicit (tag, comment) or implicit (task not moving)
- Anomalies: many re-openings, tasks without estimates, sudden volume spike
- If OKRs are provided: compare task progress against the goal trajectory (e.g., a task In Progress at 40% with an OKR of 80% is a risk of falling behind — flag as "at risk")

Goal: build an objective picture of the period to verify with the employee.

### Step 4 — Generate Discussion Topics

Generate 3–5 topics based on Steps 2 and 3. Prioritize using the table:

| Priority | Criteria |
|----------|---------|
| High | Overdue action items; active blockers; deadline risk |
| Medium | Tasks without progress; open questions from previous 1-on-1; OKR deviation (progress below expected trajectory) |
| Low | Achievements; routine updates on career goals, IDP, or OKR (progress on track) |

If career goals, IDP, or OKRs are provided — add a development topic at the end of the list.

### Step 5 — Generate Motivation and Wellbeing Questions

Generate 3–4 open-ended, non-evaluative questions. Select based on context:

- Baseline (always relevant): How is the workload feeling? What was the hardest thing this period?
- When blockers are present: What's preventing progress? How can I help?
- When career goals are provided: How is progress going toward goal X?

Do not generate a checklist — only the 3–4 most relevant questions.

### Step 6 — Assemble the Prep Document

Use the structure below. Fill in the employee's name and date from context; if not provided — use "[Employee]" and "[meeting date]".

```
# 1-on-1 Prep: [Employee Name] — [date]

## Action Items from Last Meeting
| Task | Status | Comment |
|------|--------|---------|
| ...  | Done / In Progress / Overdue | ... |

## Key Events This Period
**Completed:** ...
**At Risk / No Progress:** ...
**Blockers:** ...

## Discussion Topics
1. [High] ...
2. [Medium] ...
3. [Low] ...

## Motivation & Wellbeing Questions
- ...
- ...

## New Action Items
| Task | Owner | Due Date |
|------|-------|----------|
|      |       |          |
```

---

## Constraints

- Does not maintain meeting history between sessions — each run is independent
- Does not access external systems — analyzes only the provided text
- Does not evaluate employee performance — only structures data for conversation
- Does not replace the meeting — only prepares for it
- When data is insufficient — requests it, does not infer
- Does not generate performance reviews, ratings, or scores
