---
skill_id: session-memory
name: Session Memory
description: "Write and restore session state — session start, session end, memory write, handoff, continuation. Enforces what gets persisted so the next session resumes instead of restarting."
version: 1.0.0
category: session-memory
office: All
lead_agent: session-memory (built-in)
triggers:
  - session start
  - session end
  - memory write
  - handoff
collaborates_with:
  - operator-profile
  - memory-palace
---

# Session Memory — Enforcement Rules

> Domain: session-memory | Office: All (cross-office, always active)
> Version: 1.0.0 | Created: 2026-04-11
> This skill CANNOT be disabled. It runs on every session.

---

## Session Start Protocol

When any Claude session opens:

1. Check if `.claude-sessions-memory/` exists in the project root
   - If NO: inform the user — "No session memory directory found. Run /mxm-new-project or copy templates/session-memory/ to .claude-sessions-memory/ to initialize."
   - Do NOT create files silently without user confirmation on a new project
2. Read `.claude-sessions-memory/MEMORY.md` (master index)
3. Read `.claude-sessions-memory/project_current_state.md` (last checkpoint)
4. Read `.claude-sessions-memory/feedback_debugging_playbook.md` (known issues — scan for OPEN status)
5. Read `.claude-sessions-memory/handoff.md` (last session open items)
6. Report session start summary:

```
SESSION MEMORY LOADED
  Last session : [date from handoff.md]
  Phase        : [current phase from project_current_state.md]
  Open tasks   : [count from handoff.md]
  Known issues : [count of OPEN entries in debugging playbook]
  Next step    : [next logical step from project_current_state.md]
```

7. Check `.mxm-global/TASKS.md` (if exists):
   - List P1 tasks due today or overdue
   - Suggest: "Next recommended task: [task] in [project] — [reason]"
   - If no tasks due: "No urgent tasks. Run /mxm-tasks to see full list."

---

## During-Session Capture Rules

### On Every ERROR or RETRY

Append to `.claude-sessions-memory/feedback_debugging_playbook.md`:

```markdown
### [YYYY-MM-DD] — [Error Type / Short Label]

**Status:** OPEN | RESOLVED
**Context:** [what was being attempted when error occurred]
**Error:** [exact error message or description]
**Root Cause:** [diagnosed cause]
**Fix:** [what resolved it — or PENDING if unresolved]
**Prevention:** [how to avoid this class of error in future]
**Session:** [session date]
```

### On Every ARCHITECTURE or PRODUCT DECISION

Append to `.claude-sessions-memory/decision-log.md`:

```
[YYYY-MM-DD] | [DECISION TITLE] | [rationale] | Alternatives considered: [list] | Decided by: [agent/user]
```

### On Every Significant FILE WRITE

Check `.claude-sessions-memory/reference_key_files.md` — if the file is new and architecturally significant, add a row to the table.

Significance threshold: config files, schema files, agent definitions, skill files, migration scripts, test fixtures, environment templates.

Also flag the file for inclusion in the next auto-inventory scan (see `auto-inventory.md`).

### On Every TASK COMPLETION

Mark the task done in `.claude-sessions-memory/progress.md` and `.claude-sessions-memory/task_plan.md`. Do not leave completed items in the active queue.

---

## Session End Protocol

Before ending ANY session, execute in order:

1. **Update progress.md** — mark all items completed this session as DONE, move in-progress items to carry-forward
2. **Update project_current_state.md** — write the latest phase, completed work, active tasks, risks, and next logical step
3. **Update handoff.md** with:
   - Date of this session
   - Summary of what was accomplished
   - Open tasks (carry-forward)
   - Key decisions made this session
   - Exact next step for the next session
   - Any BLOCKED items and their blockers
4. **Append to feedback files** if any errors or lessons occurred during the session
5. **Update MEMORY.md index** if new files were created this session
6. **Write `.claude-sessions-memory/session-[YYYY-MM-DD].md`** with full session summary
7. **Offer a continuation handoff prompt (ADR-023)** — ALWAYS ask "Generate a continuation handoff prompt for a fresh window? (y/n)". Proactively recommend YES when you self-assess context is heavy (long transcript · high tool-call volume · compaction already fired · many files touched) — phrase it as judgement, NEVER a fabricated context percentage. If yes → run `/mxm-handoff`: fill `templates/continuation-prompt.template.md` from VERIFIED state only, write `.claude-sessions-memory/CONTINUATION-PROMPT.md`, and print it inline. The prompt points to source-of-truth + forces verification (the files win); it never embeds stale counts/HEADs. This is the *portable* (fresh-window) cousin of `auto-compact.md` (same-conversation compaction).

Session file format:
```markdown
---
name: Session [YYYY-MM-DD]
description: [one-line summary of what was done]
type: project
---

## Session Summary — [YYYY-MM-DD]

### Completed
- [item]

### Decisions Made
- [decision] — rationale: [rationale]

### Files Modified
- [path] — [what changed]

### Open Items (carry-forward)
- [item]

### Next Session Start Point
[exact instruction for where to begin]
```

---

## Staleness Prevention (runs after session memory writes)

After completing all session end writes, check for stale global state:

### Current working project (full check)
1. `.mxm-global/TASKS.md` — mark completed tasks done
2. `.mxm-global/GLOBAL-CONTEXT.md` — update project count if changed
3. `.mxm-global/portfolio-registry/project_state.md` — verify this project listed at correct version
4. `.claude-sessions-memory/file_inventory.md` — run auto-inventory diff
5. Version sync — check current project's version files for drift (warn user if mismatch)

### Other portfolio projects (light check)
6. For each project in portfolio registry: check `mxm_version` in their manifest
7. If behind current Maxim version: add update task to `.mxm-global/TASKS.md`
8. Do NOT auto-fix other projects — only log the staleness

**Rule: don't warn — fix it.** If TASKS.md has stale entries, update them. If project_state.md is outdated, rewrite it. Only version mismatches in OTHER projects get logged as tasks (not auto-fixed).

---

## Deduplication Rules

| File Type | Canonical Location | NEVER create at |
|---|---|---|
| task_plan.md | .claude-sessions-memory/ | root, planning/, *-planning/ |
| progress.md | .claude-sessions-memory/ | root, planning/ |
| findings.md | .claude-sessions-memory/ | root, planning/ |
| debugging playbook | .claude-sessions-memory/feedback_debugging_playbook.md | .mxm-skills/, root |
| lessons learned | .claude-sessions-memory/feedback_lessons_learned.md | .mxm-skills/, root |
| decision log | .claude-sessions-memory/decision-log.md | .mxm-skills/, root |
| handoff | .claude-sessions-memory/handoff.md | .mxm-skills/, root |
| session summaries | .claude-sessions-memory/session-*.md | .mxm-skills/, root |
| PRD, FRD, SRD, ARCHITECTURE | documents/architecture/ | root, planning/, random folders |
| Build intakes, API keys, secrets | documents/architecture/.secrets/ | root, config/, committed |
| Investor narrative, financial models | documents/business/ | root, random folders |
| Prototypes, v0 demos, POCs | prototypes/ | root, src/, apps/ |

If a duplicate is found at a non-canonical location:
1. Read non-canonical content
2. Merge (append) into canonical file
3. Backup original to `.mxm-backup/[filename]-[date]`
4. Log dedup action in `decision-log.md`
5. Inform the user — never silently delete

---

## Template Initialization

To initialize session memory for a new project, copy all files from:
`templates/session-memory/` → `.claude-sessions-memory/`

Then edit each file to replace placeholder values with project-specific content.

Standard file set:
- `MEMORY.md`
- `project_current_state.md`
- `feedback_debugging_playbook.md`
- `feedback_lessons_learned.md`
- `reference_key_files.md`
- `handoff.md` (blank — created on first session end)
- `progress.md` (blank — created on first session end)
- `task_plan.md` (blank — created on first session end)
- `decision-log.md` (blank — created on first session end)

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
