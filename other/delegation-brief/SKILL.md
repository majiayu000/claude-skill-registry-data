---
name: delegation-brief
description: "Interactive skill for Cowork that generates a structured delegation brief
  by asking the user up to 5 targeted questions: what to do, expected result, files
  involved, what not to touch, and success criteria. Outputs a ready-to-use task
  instruction for a new Cowork session. Use when delegating tasks to an AI assistant,
  structuring a vague request, or preparing clear instructions before starting work.
  Triggers RU: «бриф», «составь бриф», «помоги делегировать», «структурируй задачу».
  Triggers EN: 'brief', 'delegation brief', 'help me delegate', 'structure my task'."
version: 1.0.0
---

# Skill: delegation-brief

Asks the user up to 5 targeted questions and generates a structured task brief — a ready-to-use instruction for a new Cowork session. Solves the problem of vague requests that lead to unexpected results, damaged files, and wasted tokens.

Target audience: new Cowork users, non-technical professionals.

---

## Triggers

**Russian:** «бриф», «составь бриф», «помоги делегировать», «структурируй задачу», «создай бриф», «напиши бриф», «хочу делегировать», «как правильно описать задачу», «помоги сформулировать задачу»
**English:** "brief", "delegation brief", "task brief", "help me delegate", "structure my task", "create a brief", "write a brief", "how to describe a task to Claude"

---

## Language Detection

Determine the language of the user's request:
- If the request is in Russian → respond in Russian
- Otherwise → respond in English

---

## Input

Trigger phrase — no prior input required. All data is collected through the dialogue in Steps 1–2.

## Output

Structured text brief in chat with five sections:

1. Task
2. Expected result
3. Files to modify
4. Off-limits
5. Success criteria

---

## Instructions

### Step 0 — Extract context from the trigger

Before launching `AskUserQuestion`, check: does the user's message already contain answers to one or more of the 5 questions?

Action:
- If yes — extract that data internally and skip the corresponding questions in AskUserQuestion
- If no, or if input is minimal (one or two words) — do not ask for clarification; proceed directly to Step 1 with the full set of questions

Examples:
- "Collect files from /reports and create a summary document" → Q1 and Q2 are known, Q3 is partially known; ask only the remaining questions
- "Brief" / "Create a brief" → nothing is known; ask all 5 questions without requesting clarification

### Step 1 — Collect data: questions 1–4

Use `AskUserQuestion` to ask the unknown questions from Q1–Q4 simultaneously (after Step 0). Combining questions into one call reduces friction — the user responds at once without waiting for follow-ups.

Ask the following questions:

**Q1 — What needs to be done?**
- options: "Create a new file or document", "Modify an existing file", "Find or analyze information", "Other task"
- multiSelect: false

**Q2 — What does the expected result look like?**
- options: "A finished file (document, code, spreadsheet)", "Edits to an existing file", "Text or answer directly in chat", "Other format"
- multiSelect: false

**Q3 — Which files or folders does the task involve?**
- options: "A specific file (I'll provide the name)", "All files in a folder", "Files don't exist yet", "No files / not sure"
- multiSelect: false

**Q4 — What must not be touched?**
- options: "No particular restrictions", "Specific files or folders", "Style and formatting", "Data or structure"
- multiSelect: false

### Step 2 — Collect data: question 5

Use `AskUserQuestion` for the fifth question separately — it sets the quality bar and requires a deliberate answer.

**Q5 — What does success look like?**
- options: "File created and matches the request", "Changes applied without errors", "Result is immediately usable", "I'll specify my own criterion"
- multiSelect: false

### Step 3 — Generate the brief

Generate the brief based on the answers. Rules:

| Situation | Action |
|-----------|--------|
| User selected a preset option | Rephrase into a concrete statement |
| User typed custom text (Other) | Use verbatim, without edits |
| Answer "No restrictions" on Q4 | Record: "No restrictions" |
| Answer "don't know", "not sure", "haven't decided" on any question | Record: "Not specified — clarify before starting" |
| No files involved | Write: "New file — clarify path before starting" |

Output the brief strictly in this format:

**If the user's language is Russian:**
```
## Бриф задачи

**Задача:** [что нужно сделать — 1-2 предложения]

**Конечный результат:** [формат и вид готового результата]

**Файлы к изменению:** [список или «Не указано»]

**Что нельзя трогать:** [ограничения или «Без ограничений»]

**Критерий успеха:** [как выглядит выполненная задача]
```

**If the user's language is English:**
```
## Task Brief

**Task:** [what needs to be done — 1-2 sentences]

**Expected result:** [format and shape of the output]

**Files to modify:** [list or "Not specified"]

**Off-limits:** [restrictions or "No restrictions"]

**Success criteria:** [what a completed task looks like]
```

After the brief, add a tip on a separate line:

- RU: > Скопируй бриф и вставь в начало нового диалога с Cowork как инструкцию к задаче.
- EN: > Copy the brief and paste it at the start of a new Cowork session as your task instruction.

---

## Constraints

- Does not perform the task itself — only generates the brief
- Does not access the file system
- Asks no more than 5 questions — if data is insufficient, generates the brief with "Not specified — clarify before starting" in the relevant section
- Does not estimate priorities, deadlines, or tech stack — records only what the user provides
- Does not save the brief to a file unless the user explicitly requests it
