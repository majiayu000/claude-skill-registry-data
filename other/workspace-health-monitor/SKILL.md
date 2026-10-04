---
name: workspace-health-monitor
description: "Audits a manager's workspace files (meeting notes, plans, tasks, logs) to
  detect orphaned files, forgotten action items, duplicates, and plan-to-reality drift.
  Use when you want to clean up your workspace, run a weekly hygiene check, find forgotten
  commitments buried in notes, or spot conflicting information across project documents.
  Triggers RU: «аудит воркспейса», «проверь рабочую папку», «найди забытые задачи»,
  «почисти workspace», «что я забыл сделать».
  Triggers EN: workspace audit, workspace health check, find forgotten tasks, orphaned files,
  weekly cleanup."
version: 1.0.0
---

# Workspace Health Monitor

Audits a manager's workspace — scans files, notes, tasks, and logs to detect orphaned files,
forgotten action items, duplicates, and drift between plans and reality.

For: PMs, team leads, department heads — anyone who maintains working notes and files.

---

## Triggers

**Russian:** «аудит воркспейса», «проверь рабочую папку», «найди забытые задачи», «почисти workspace»,
«аудит заметок», «осиротевшие файлы», «еженедельная гигиена», «что я забыл сделать»
**English:** "workspace audit", "workspace health check", "clean up my workspace", "find forgotten
tasks", "orphaned files", "workspace hygiene", "weekly cleanup", "check my notes"

---

## Language Detection

Determine the language of the user's first message — it sets the language for the entire
session and the audit report.
Russian input → report in Russian. English input → report in English.

---

## Input

**Required:**
- Content of workspace files: meeting notes, plans, task lists, logs, drafts
- Delivery method: (a) direct access via Cowork file access, (b) manual file upload, (c) paste text into chat

**Optional:**
- List of currently active projects (name + brief description)
- Time horizon: "last 2 weeks", "last quarter", etc.

## Output

Structured audit report in five sections:
1. Orphaned files — not linked to any active project
2. Forgotten action items — mentioned in notes, never transferred to a task tracker
3. Duplicates and conflicts — repeated or contradictory information
4. Cleanup recommendations — what to delete, transfer, or merge
5. Clutter score — overall verdict with prioritized action items

---

## Instructions

### Step 1 — Collect and Inventory Materials

Ask the user to provide workspace file contents via one of:
- Cowork: "Allow me to read your workspace folder" + Read on the specified directory
- File upload: "Upload the files you want audited"
- Text paste: "Paste the contents of your files into the chat"

If active projects are not provided, ask one question:
"List your currently active projects (names are enough) — this helps identify which files
are orphaned versus still relevant."

Build an internal inventory: filename → type (note / plan / tasks / log / other) → date (if available).

### Step 2 — Identify Active Projects

If the project list was not provided, infer it from file contents:
- Look for mentions of projects, products, or teams with active tasks
- Mark inferred projects as "assumed" — the user can correct them

Compile the active project list for use in Step 3.

### Step 3 — Find Orphaned Files

A file is orphaned if it:
- Does not mention any active project (from Step 2)
- Is not linked to any current task
- Is dated more than 30 days ago with no signs of recent updates

For each orphaned file, state: name, last date referenced, reason for flagging.
Flag uncertain cases as "likely orphaned" — do not assert without confidence.

### Step 4 — Find Forgotten Action Items

Scan all files for patterns:
- "TODO", "Action", "Action item", "Agreed", "Owner: [name]", "By [date]"
- Incomplete checklists ([ ] or unchecked bullet items)
- Named commitments ("Ask Alex", "Send to Maria", "Follow up with team")

For each found action item, state: wording, source (filename), date if available.
Exclude action items that are explicitly closed in the same or another file.

### Step 5 — Find Duplicates and Conflicts

**Duplicates:** files with similar content (two plans for one project, multiple PRD versions).
State: which files duplicate each other, what they share, which is likely more current.

**Conflicts:** contradictory information across files.
Example: one file says deadline March 15, another says April 1.
State: what conflicts, in which files, which version is likely correct.

### Step 6 — Formulate Recommendations

For each category, propose a concrete action:

| Category | Action |
|----------|--------|
| Orphaned file | Archive / Delete / Clarify |
| Forgotten action item | Transfer to task tracker / Close as irrelevant |
| Duplicate | Keep the current version, archive the older one |
| Conflict | Investigate and unify |

Prioritize recommendations: first "Critical" (named commitments), then "Important" (conflicts),
then "Suggested" (archiving).

### Step 7 — Score Clutter and Deliver Report

If active projects could not be determined (neither provided nor inferred from files):
- Do not assign a clutter score
- State: "Score unavailable — active projects could not be determined.
  Provide a project list for a complete audit."
- Deliver only the "Forgotten action items" section based on available files

Otherwise — calculate the score as the percentage of **orphaned files** out of total files.
Duplicates and conflicts appear only in recommendations and do not affect the percentage.

- **Clean (0–20% orphaned):** "Workspace is in good shape"
- **Moderate (21–40%):** "Some cleanup needed, not critical"
- **Cluttered (41–60%):** "Needs attention — set aside an hour"
- **Chaos (>60%):** "Significant cleanup required"

Report format:

```
## Workspace Audit Report — [date]

### Score: [verdict]
[1–2 sentence summary]

### 1. Orphaned Files ([N])
[list with explanations]

### 2. Forgotten Action Items ([N])
[list with sources]

### 3. Duplicates and Conflicts ([N])
[list with explanations]

### 4. Recommendations (prioritized)
[action list]
```

---

## Constraints

- Does not delete or move files — recommendations only
- Does not connect to task trackers directly (Jira, Asana, Linear, etc.)
- Does not analyze binary files without readable text content (images, archives)
- Does not conclude "delete" without high confidence — uses "likely orphaned"
- With more than 50 files, prioritizes by date (oldest first) and type (meeting notes > plans > logs)
- If active projects are neither provided nor inferable — reports this and requests clarification
  before Step 3
- Does not replace the user's judgment: the report is diagnostic, not an instruction to delete immediately
