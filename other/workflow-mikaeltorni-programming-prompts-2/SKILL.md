---
name: workflow
description: >-
  v1.0.20 — Coordinate an end-to-end programming task as an ordered workflow
  only when the user explicitly invokes this skill.
---

# Programming workflow

## Activation and ownership

Run this workflow only when the user explicitly invokes `$workflow` (or the
host's equivalent explicit skill command). Its presence in an installed skill
catalog does not activate it.

This skill coordinates independently selected companions; none depends
on workflow. Keep dependency and routing instructions here. Do not add a
`workflow` dependency or invocation to another skill.

Own the end-to-end sequence for the current programming request. Break the
work into ordered phases that fit the request, finish each phase before moving
to the next, and keep the user's stated goal and constraints visible throughout
the task.

## Read the enabled skills

Before building the phase sequence, inspect the current user prompt and the
skill instructions actually supplied in the conversation. Make a short
inventory containing only the companion skills explicitly invoked by the user
or loaded as applicable by the host. Assign each inventoried skill to the phase
where its instructions apply.
An enabled skill may have no work for this request: for example, `debug` is
selected but not applicable when no failure was reported. Record that as
`debug (not applicable)`, not as an unavailable skill requiring replacement.

Do not treat a skill as enabled merely because it is installed, discoverable,
mentioned as an example, or known to exist in the repository. Do not load or
apply an unselected companion on this skill's behalf.

If a requested companion is unavailable, unreadable, or absent from the
supplied skill context, mark it skipped in the plan and continue with the
remaining phases and enabled skills. Do not install it, reconstruct its rules
from memory, or fail the whole workflow merely because the companion is
missing.

### No-companion fallback

When the inventory contains no available companion skills, create and maintain
the Markdown plan, then implement the user's requested code directly under the
repository and user instructions already in force. Do not synthesize or apply
the conventions of `worktree`, `commits`, `debug`, `srp`, `logging`,
`commenting`, `docs`, or any other unselected skill. In this fallback, code
writing is the only execution phase after planning.

## Phase order

Follow this order:

1. **Plan.** Before tracked repository mutation, translate the user's goal into an
   actionable sequence that preserves their constraints and names the expected
   deliverables. If `ACC_WORKFLOW_FILE` is set to an absolute Markdown path
   inside the launch project's `tmp/workflow/` directory, use that exact path;
   ACC gives each wrapped agent its own file so simultaneous agents in one
   repository never overwrite each other's plan. Read the variable from the
   current shell before writing the plan. Resolve and retain one absolute path
   variable before the first write; do not type a fresh plan filename at each
   update. Read back that exact file and its four-row table before implementing
   anything. Otherwise use the fixed fallback
   `<project-root>/tmp/workflow.md`. For a Git launch project, resolve
   `<project-root>` from that project's `git rev-parse --show-toplevel` before
   entering a linked worktree: a launch checkout at `/Projects/app` uses
   `/Projects/app/tmp/workflow.md`, never `/Projects/tmp/workflow.md`.
   Create the needed `tmp/` directory and write the file literally named
   `workflow.md` inside it; a sibling such as `<project-root>/tmp_workflow.md`
   is not the plan. Do not place
   the plan in the skill directory, an agent home, or the system `/tmp/`. Keep
   all progress in that one file; update it as phases advance, and do not stage
   or commit it unless the user explicitly asks. A `WORKFLOW.md` in the task
   checkout does not replace the selected plan path in the launch project.
   The terminal overlay reads
   the table below and renders `complete` as `[x]`, `in_progress` as `[>]`,
   `pending` as `[ ]`, and `skipped` as `[-]`:

   ```markdown
   # Workflow

   ## Goal
   The requested outcome and concrete deliverables.

   ## Enabled skills
   The independently selected companions, or `none`.

   ## Tasks
   | Order | Task | Status | Details |
   | --- | --- | --- | --- |
   | 1 | Plan | complete | Scope and deliverables recorded. |
   | 2 | Establish worktree | pending | Use the worktree companion if enabled. |
   | 3 | Write code | pending | Implement the requested behavior. |
   | 4 | Write documentation | pending | Use the docs companion if enabled. |
   ```

   Resolve the chosen plan path to an absolute path in the launch project
   before entering a linked worktree. Keep using that exact absolute path for
   every update, even when the current directory changes; never create a
   second `tmp/workflow.md` inside the linked worktree. A relative
   `tmp/workflow.md` after changing directories updates the wrong plan.

   Keep the headings, table columns, four task names, row numbers, and order
   exactly as shown. The `## Tasks` table has exactly four data rows: put
   workflow phase progress and task-specific deliverables in `Details`, not
   in extra task rows or a second progress checklist. Name deliverables in
   `Details`; do not put a numeric Feature or capability-sentence count there.
   The ledger owns that count. A selected `commits`
   companion may keep its verbatim capability ledger in a `## Feature ledger`
   section after the task table in this same file; that section is supporting
   detail, not another workflow phase or progress file. When a ledger is present,
   update each entry's commit reference before marking `Write code` complete;
   a `pending` ledger entry and a `complete` code row contradict each other.
   Check every ledger entry for `pending` before completing `Write code`;
   a claim in Details or a visible Git commit does not update that entry.
   Escape any `|` in a
   detail cell so the table remains parseable. Set each `Status` to exactly one
   of `pending`, `in_progress`, `complete`, or `skipped`. After the skill
   inventory, write `none` under `## Enabled skills` when there are no
   independently selected companions; naming `workflow` itself is harmless,
   but it does not make another companion selected. Mark optional phases
   `skipped` immediately when their companions
   are not enabled or available. The initial file records `Plan` as `complete`.
   Before each later enabled phase starts, set its row to `in_progress`; after
   it finishes, rewrite the whole four-row `## Tasks` table in place as one
   block so that same row is `complete` with updated details. Never append a
   second row, a second table, or a leftover copy of an earlier row. In
   particular, finish the `Write code` row and any selected `commits` ledger
   references before moving to `Write documentation`; a completed
   documentation row cannot coexist with an in-progress code row or pending
   Feature commit. After any required commits, merge, and consumer
   reapplication, reread this original absolute file and reconcile its
   existing four rows and ledger with what finished. Before normal handoff,
   no enabled phase may remain `pending` or `in_progress`. Never create a
   workflow-owned verification row or another progress file.

   Preserve the original plan through Git housekeeping and recovery. An
   ignored or untracked progress file is still the authoritative plan; never
   overwrite it by redirecting a recovery command that may fail. Recover into
   a separate candidate first, require successful output with the expected
   headings and four task rows, then replace the plan. After every update or
   recovery, read back that exact path. If it is empty or loses its Tasks
   table, reconstruct it from the original request and verified commits before
   advancing; a successful shell exit alone does not prove the plan survived.

   Treat plan updates as edits that can fail: if replacing an old row or ledger
   reference finds no exact match, rewrite the existing plan section instead of
   silently leaving it unchanged. The committed Feature's ledger entry must
   contain its actual commit hash before the next Feature begins. Prefer plain
   commit hashes in ledger cells; formatting delimiters are unnecessary. If a
   targeted replacement fails, rewrite the complete affected section rather
   than repeatedly patching stale text. A ledger row
   combining separate capability sentences or sharing one introducing commit
   with another row is not complete merely because the code works. Conversely,
   multiple commands in one capability sentence stay in one ledger row and may
   share its one commit. Count ledger entries from source sentences, not from
   the number of commands.
   At handoff, count the ledger entries and reread every Details cell for a
   numeric Feature claim or a Details cell that still says a completed
   phase is next. Remove such counts and rewrite those details to describe
   the current state before marking the plan
   complete; a correct ledger does not excuse a contradictory Plan row.
2. **Establish the worktree when enabled.** If the `worktree` companion is in
   the enabled-skill inventory and available, follow it to create the task's
   isolated worktree before editing repository files. Otherwise skip this
   phase.
3. **Write the code.** Implement the plan inside that worktree while applying
   the programming skills supplied for the task.
4. **Write the documentation when enabled.** If a documentation companion is
   in the enabled-skill inventory and available, apply its guidance after the
   code-writing phase. Otherwise skip this phase.

Do not reorder implementation ahead of planning or documentation ahead of the
code it describes.

### Code-writing companions

When present in the enabled-skill inventory, apply `logging`, `commenting`,
`srp`, and `testing` during **Write the code**. Their requirements shape the
implementation in that phase; do not defer logging, code comments/docstrings,
single-responsibility structure, or testing to the documentation phase. Preserve each
companion's own scope and exact rules instead of restating weaker substitutes
here.

## Handoff gate

Immediately before you stop, reread the original absolute plan file and
rewrite its `## Tasks` table in place as one complete four-row block.
Rewrite each Details cell from the completed deliverables, including the Plan
row; do not carry forward an early sentence-count guess. Remove any numeric
Feature/capability count from Details and name the completed deliverables
instead. The ledger retains the exact boundaries and commit references. Do not
append rows, do not add a second table, and do not leave an earlier copy of a
row above or below the replacement. Then confirm all of the following; if any
check fails, edit that same file now and do not hand off:

1. The table still has exactly four data rows, named once, in order:
   `Plan`, `Establish worktree`, `Write code`, `Write documentation`.
2. No task name appears twice.
3. Every enabled row is `complete` or `skipped`. None is `pending` or
   `in_progress`, even when the Details cell already describes finished work.
4. If `Write documentation` is `complete`, `Write code` is also `complete`
   and every Feature-ledger entry has an introducing commit distinct from the
   other entries. Inspect the
   whole `## Feature ledger` section for any leftover `pending` reference;
   fix it in this same file even when the task table says `complete`.
5. Skipped companions stay `skipped`; do not invent extra rows for them.

## No workflow verification phase

Do not add a standalone verification, review, test, or validation phase to this
workflow. The workflow ends after the documentation phase and the normal task
handoff. When an independently enabled companion skill requires checks, honor
that requirement within the phase that skill owns; do not represent it as an
extra phase supplied by this skill.

This applies to plan entries as well as headings: do not add a separate check,
test, review, validation, or verification task merely because it is customary.
The four-row plan must not grow another step for that work. Checking code during
`Write code` is allowed, and its `Details` may mention checks performed or
planned within that row. Such a mention does not create a separate step, and
this skill does not require checks when no companion does.

At each phase boundary, record what was completed and what phase comes next so
the task remains resumable. Apply the Handoff gate before stopping. Do not
broaden the user's scope merely to make the workflow more elaborate.
