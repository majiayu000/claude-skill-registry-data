---
name: cowork-session-planner
description: "Generate a pre-session brief for Cowork: current status, session goal, and prioritised work plan from local project files — before your first real message. Use when starting a session, returning after a break, or needing focus. Triggers: 'session brief', 'prepare my session', 'start my cowork session', 'бриф сессии', 'подготовь сессию', 'что делать в этой сессии'."
version: 1.0.0
---

# Cowork Session Planner

This skill generates a pre-session brief for non-technical Cowork users by scanning available project files (context.md, logs, tasks, CLAUDE.md) and producing a minimal structured brief: current project status, recommended session goal, and a prioritised work plan. It runs at the very start of a session — before any real work task is requested — so the user knows exactly where to focus.

**Input:** Current workspace / project folder. Optional: explicit session goal as free text.

**Output:** Structured markdown brief (inline response). Optionally saved to `output/session-brief.md` on user request.

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Parse Input

1. Check if the user provided an explicit session goal (free text after the trigger phrase).
   - If yes: store as `stated_goal`; use it as the primary session focus in Step 4.
   - If no: `stated_goal` is empty; derive focus from project files in Step 3.

2. Identify the project folder to scan.
   - Default: current workspace / selected folder.
   - If user specifies a path, use that path.

---

### Step 2: Scan Project Files

1. Look for the following files in the workspace (in order of priority):
   - `context.md` or `CLAUDE.md` — project overview and status
   - `logs/log.md` — recent activity log
   - `TASKS.md` or any file containing open tasks
   - Any `output/skill-spec.md` or in-progress output files

2. For each found file, extract:
   - **context.md / CLAUDE.md:** project name, current status, open questions
   - **logs/log.md:** last log entry (date + action description)
   - **TASKS.md:** open tasks (status: pending or in_progress)
   - **skill-spec.md:** if present, note "skill spec in progress"

3. Note any missing files for the Notes section of the brief.

**Edge Cases:**
- If no context.md or CLAUDE.md found: proceed without project overview; flag as missing in Notes.
- If log file is empty or absent: skip last-action extraction; open brief with "No activity log found."
- If multiple task files found with conflicting state: list all sources; flag conflict in Notes.

---

### Step 3: Determine Session Focus

1. If `stated_goal` is set: use it as the session goal. Skip to Step 4.

2. Otherwise, derive focus from extracted data:
   - Check open tasks (status: pending / in_progress) — select the highest-priority item.
   - If no tasks, check last log entry — infer next logical step from last completed action.
   - If neither available: propose "Define session goal" as the first task.

3. Compile a prioritised work list (max 5 items):
   - Item 1: derived or stated session goal
   - Items 2–5: remaining open tasks or logical next steps

---

### Step 4: Assemble Brief

1. Build the pre-session brief with these sections:
   - **Project / Status:** project name + 1-sentence current state
   - **Session Goal:** recommended or stated goal (1 sentence)
   - **Work Plan:** numbered list, max 5 items
   - **Blockers:** any open blockers or conflicts from Step 2; "None" if clean
   - **Notes:** any missing files, file conflicts, or flags from Step 2

2. Use bilingual headers (EN + RU) if Russian was detected; English-only otherwise.

3. Display the brief inline. Do not save to file unless user explicitly requests it.

---

### Step 5: Handle Save Request

1. If user says "save" or "save to file": write brief to `output/session-brief.md`.
2. Confirm file written and provide path.

---

## Negative Cases

- **No project files found (empty workspace):** Return: "No project files found. Please select your project folder or provide a session goal to get started." Do not generate an empty or partial brief.
- **User invokes mid-session (active tasks detected):** Detect in-progress tasks or recent log entries (within last hour). Note: "It looks like you're already mid-session." Offer a **re-focus brief** instead of an initial brief (same format, but titled "Re-focus Brief").

---

## Output Format

Inline markdown response:

```
## Сессионный бриф / Session Brief
**Проект / Project:** [project name or folder]
**Статус / Status:** [1-sentence current state]

### Фокус сессии / Session Goal
[Recommended or stated session goal — 1 sentence]

### План работы / Work Plan
1. [Task 1 — highest priority]
2. [Task 2]
3. [Task 3]
...

### Блокеры / Blockers
- [Blocker 1 if any, otherwise: None]

### Заметки / Notes
- [Missing files, conflicts, or flags — if any]
```

**Field rules:**
- Work Plan: 1–5 items; each item is a specific, actionable task (not a vague category)
- Blockers: specific obstacle or "None"
- Notes: only populated when something is flagged (missing file, conflict, mid-session detection)
