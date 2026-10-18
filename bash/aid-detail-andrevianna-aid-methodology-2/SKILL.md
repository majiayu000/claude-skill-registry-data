---
name: aid-detail
description: >
  Break deliverables into small, dependency-driven, typed tasks -- each one a reviewable
  unit. The ultimate breakdown. Use this skill when a delivery has been planned and the
  actual work items are needed before execution starts. It detects each task's type from the
  SPEC's own signals -- RESEARCH, DESIGN, IMPLEMENT, TEST, DOCUMENT, MIGRATE, REFACTOR,
  CONFIGURE -- gives every task exactly one type, and builds the delivery's execution graph
  with explicit dependencies and the parallelism they allow.
allowed-tools: Read Glob Grep Write Edit Bash Shell Terminal
argument-hint: "work-001 (required if multiple works)  [--reset] clear deliveries/delivery-NNN/tasks/"
---

# Detail — The Ultimate Breakdown

Break each deliverable from PLAN.md into small, sequential, testable tasks.
Each task = one agent session = one reviewable unit = one human review.

## ⚠️ Pre-flight Checks

### Check 1: Locate Work

1. If arg provided → use that work directory
2. If no arg → enumerate works **cross-worktree**: run
   `bash .aid/runtime/scripts/works/enumerate-works.sh` (main tree + every git
   worktree; never the local `.aid/works/` glob, which is empty on `master`), taking
   each record's field-1 `work_id`
3. Single record → auto-select it
4. Multiple records → list them, ask user to choose
5. Zero records on any worktree → **STOP.** "No works found. Run `/aid-describe` first."

### Locate + Enter the Work's Worktree

**As soon as Check 1 resolves the work id** and **before** Check 2 checks for
`.aid/works/{work}/PLAN.md`, follow `.aid/runtime/templates/downstream-worktree-entry.md` to
normalize `<work-id>` to its bare `work-NNN` branch name, `locate` the worktree (which **always
exits 0** and returns `<path>\t<status>`), and enter the returned path. Keep the defensive
empty-path/non-zero backstop that stops rather than operate blindly — it should not fire against
the real helper. Never create a new worktree — creation belongs to the work-starting skills only.

### Check 2: Verify PLAN.md Exists

1. Check for `.aid/works/{work}/PLAN.md`
2. If missing → **STOP.** "No PLAN.md found. Run `/aid-plan` first."

### Check 3: Verify Not in Plan Mode

- ✅ `Default` or `Auto-accept edits` → Proceed.
- ❌ `Plan mode` → **STOP.**

## State Detection

State detection reads the files on disk, every run; nothing remembered from an earlier run counts as state.

- No `deliveries/delivery-NNN/tasks/task-NNN/DETAIL.md` exists under `.aid/works/{work}/` → **FIRST-RUN**
- At least one `deliveries/delivery-NNN/tasks/task-NNN/DETAIL.md` exists → **REVIEW**
- Tasks complete and grade ≥ minimum → **DONE**

Print the state-entry line and "you are here" map:

**FIRST-RUN:**
```
[State: FIRST-RUN] — No task files yet; begin proposing task breakdown per deliverable.
aid-detail  ▸ you are here
  [● FIRST-RUN ] → [ REVIEW ] → [ DONE ]
```

**REVIEW:**
```
[State: REVIEW] — Existing tasks found; re-review against current PLAN.md and SPECs.
aid-detail  ▸ you are here
  [✓ FIRST-RUN ] → [● REVIEW ] → [ DONE ]
```

**DONE:**
```
[State: DONE] — Task list approved and meets minimum grade.
aid-detail  ▸ you are here
  [✓ FIRST-RUN ] → [✓ REVIEW ] → [● DONE ]
```

## Dispatch

| State | Detail | Worker | Advance |
|-------|--------|--------|---------|
| FIRST-RUN | `references/first-run.md` | `aid-architect` | `→ REVIEW` |
| REVIEW | `references/review.md` | `aid-reviewer` | `→ DONE` |
| DONE | — | `inline` | `→ halt` |

Load the `Detail` file for the detected state and execute it.

On state completion, route by its `**Advance:**` type (per [`state-machine-chaining.md`](../../aid/templates/state-machine-chaining.md)):
- **CHAIN** → begin the next state's reference doc within the same invocation; no exit.
- **PAUSE-FOR-USER-ACTION** / **PAUSE-FOR-USER-DECISION** → print the pause reason + resume command and exit.
- **HALT** → print the closing summary and exit (DONE prints the task summary).
