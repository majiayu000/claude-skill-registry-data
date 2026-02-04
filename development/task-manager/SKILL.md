---
name: task-manager
description: Create and manage development tasks after the user approves a plan. Initializes folders/files, updates the backlog, and keeps progress notes synchronized.
---
<task_manager>
# Task Manager Skill

## When to Use
Use this skill **immediately after the user approves a plan** for code changes. It creates the task folder, scaffolds files, records the plan and context, and updates the backlog.

> Do **not** use for brainstorming or unapproved ideas.

---

## Task Structure (authoritative)
Each task lives at:  
`.meridian/tasks/TASK-###/`

**Files inside (exact names):**
- `TASK-###.yaml` — Task brief (objective, scope, constraints, acceptance criteria, deliverables, risks, out of scope, links)
- `TASK-###-plan.md` — **Exact plan approved by the user** (freeze this; changes require re‑approval)
- `TASK-###-context.md` — Relevant context (Why decisions were made), key files, timestamped progress notes (log decisions, blockers, links, PRs)

> **IDs**: 3‑digit, zero‑padded, uppercase folder prefix: `TASK-001`, `TASK-002`, …

---

## Preconditions
1) The user has explicitly approved the plan (or you have an approved summary of the plan).  
2) You know the short, action‑oriented title (≤80 chars).  
3) No secrets or PII are copied into task files.

---

## Creating a Task

### Step 1 — Create the folder and files
Run the helper script:
- `python3 $CLAUDE_PROJECT_DIR/.claude/skills/task-manager/scripts/create-task.py`
  - It will automatically create a new folder for a task with 3 files:
    - `$CLAUDE_PROJECT_DIR/.meridian/tasks/TASK-###/TASK-###.yaml`
    - `$CLAUDE_PROJECT_DIR/.meridian/tasks/TASK-###/TASK-###-plan.md`
    - `$CLAUDE_PROJECT_DIR/.meridian/tasks/TASK-###/TASK-###-context.md`

### Step 2 — Populate files
- Read each file before writing (System limitation)
- Fill `TASK-###.yaml` using the **Task Brief YAML Template**.
- Paste the approved plan into `TASK-###-plan.md`
- Add an initial entry to `TASK-###-context.md`

### Step 3 — Update the backlog
Append/update an entry in `.meridian/task-backlog.yaml` with:
- `id`, `title`, `status: todo`, `priority`, and the relative path to the task folder.

---

### `task-backlog.yaml` — quick guide

* **Purpose:** Single source of truth for all tasks (status, priority, location).
* **Structure:** Top‑level key `tasks:`, each item is one task entry.
* **When to add:** Immediately after creating `TASK-###`; set `status: todo`.
* **When to update:** On start (`in_progress`), when blocked (`blocked` + reason in the task’s context file), and on completion (`done`).
* **What to edit:** `status`, `priority`
* **Never:** Rename `id`, delete finished tasks (mark `done` instead).
* **Allowed values:**

  * `status`: `todo` | `in_progress` | `blocked` | `done`
  * `priority`: `P0` | `P1` | `P2` | `P3` (P0 = highest)
* **Consistency:** `id` must match the folder name and the files inside it.

#### Example entry (recommended)

```yaml
tasks:
  - id: TASK-037
    title: "Add cursor-based pagination to /api/orders"
    priority: P1
    status: in_progress
    path: ".meridian/tasks/TASK-037/"
```

---

## During Execution

**Status transitions**  
- `todo` → `in_progress` when you start coding.  
- Optional: `blocked` when waiting on dependency/decision; record reason in context.  
- `in_progress` → `done` when the Definition of Done is met.

**What to update**
1) `TASK-###-context.md`: Add timestamped notes for:
   - Decisions, tradeoffs, key files, and blocked reasons.
   - Links to PR(s), commit SHAs, builds, or dashboards.
   - “Memory candidates” (facts worth persisting) — flag with `MEMORY:`; **then use `memory-curator`** (never write memory.jsonl manually).
2) `$CLAUDE_PROJECT_DIR/.meridian/task-backlog.yaml`:
   - Update `status`.
3) `TASK-###.yaml`:

---

## Finishing a Task (Definition of Done)
Mark `done` only when **all** are true:
- Code compiles; typecheck/lint/test/build pass.
- Tests added/updated for new behavior; critical flows covered.
- Docs updated where relevant (README/snippets/endpoint contracts).
- No secrets/PII in code, commits, or logs. UI/API changes meet accessibility/security checks.
- If schema/data changed: migration applied and rollback plan documented in the plan or context.
- `TASK-###-context.md` has a final note with the merged PR link(s).
- Run `memory-curator` to add any durable architectural decisions (don’t edit memory manually).
- Update `.meridian/task-backlog.yaml` to `done`.

---

## Editing Scope or Plan
- **Any material change** to goals, acceptance criteria, or approach requires re‑approval.
- Update `TASK-###-plan.md` with a short “Amendment <date>” section describing the change.
- Log the reason and reference in `TASK-###-context.md`.

---

## Splitting / Merging / Cancelling Tasks
- **Split**: Create new tasks, move relevant sections, and update backlog. In originals, add: “Superseded by: …”.
- **Merge**: Keep one task as primary; close the others as `done` with “Merged into: …” notes.
- **Cancel**: Set status to `done` with `resolution: canceled`; explain in context; keep history.
</task_manager>