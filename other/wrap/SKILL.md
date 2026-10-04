---
name: wrap
description: >
  Freezes and wraps up inbox task work — reads ongoing tasks, cross-checks each
  against the project registry to catch misfiled project-owned tasks, updates
  status, writes per-task session logs, archives completed/abandoned tasks, and
  relocates any confirmed-misfiled task to its owning project's memory/tasks/.
  Scoped to `{agency-root}/tasks/inbox/` plus read-only access to
  `{agency-root}/core/memory/medium-term.md` and write access limited to
  `{project}/memory/tasks/` for relocation only. Trigger when the session ends
  with inbox tasks in progress, when switching focus away from inbox work, or
  when the user says "wrap up" or "wrap" for non-project tasks.
---

# Wrap — Inbox Task Session Freeze

Spawns a subagent that reads ongoing inbox tasks, updates their status, writes
per-task session logs, and archives completed/abandoned tasks. Caller spawns and
waits — zero work done in the calling session.

## Step 1 — Spawn Subagent

Use the Agent tool to spawn a general-purpose sonnet subagent. The subagent owns
the entire ritual — do not do any reading or writing yourself.

Subagent prompt:

"You own the wrap ritual for inbox tasks. Run it completely.

PERMISSIONS: read-write-create on all inbox paths below. No restrictions there.
Additionally: READ-ONLY on `{agency-root}/core/memory/medium-term.md` (ownership
cross-check only). For relocation of a confirmed-misfiled task (Step 2.5),
write access to the destination project's
`{project-memory-path}/tasks/{ongoing|completed}/{slug}/` ONLY — do not touch
any other file in that project's memory.

## Scope
- Inbox root: `{agency-root}/tasks/inbox/`
- Ongoing dir: `{agency-root}/tasks/inbox/ongoing/`
- Completed dir: `{agency-root}/tasks/inbox/completed/`
- Archived dir: `{agency-root}/tasks/inbox/archived/`
- Task session dir: `{agency-root}/tasks/inbox/ongoing/{slug}/sessions/`
- Active task dirs: `{agency-root}/tasks/inbox/ongoing/*/TASK.md`
- Registry (read-only): `{agency-root}/core/memory/medium-term.md`
- Relocation destination (write, misfiled tasks only): `{project-memory-path}/tasks/{ongoing|completed}/{slug}/`

## Step 1 — Inventory Ongoing Tasks

Read every `{agency-root}/tasks/inbox/ongoing/*/TASK.md` simultaneously.
Collect per task: slug (folder name), title, status, priority, description.
Build a brief summary for each.

## Step 1.5 — Ownership Backstop Check (mandatory)

The inbox is for tasks with NO existing owning project — see
`{agency-root}/tasks/inbox/index.md`. Root-cause pattern this backstop guards
against: a task's slug/title/body names an existing project, but it sat in
the inbox anyway because the initiating session (parent-ai direct, no project
of its own) had no other place to file it. Task ownership follows the
project the work is ABOUT, not the session that initiated it — do not repeat
this.

For each ongoing task inventoried in Step 1, cross-check its slug, title, and
body text against the project table in `{agency-root}/core/memory/medium-term.md`
(slug list) — does the task name or describe work belonging to an existing
project?

- **No match:** genuinely ownerless — proceed normally in Step 2.
- **Match found:** flag it. Do NOT silently continue managing it as an inbox
  task. Present the match to the user in Step 2 with a recommended action:
  move the task folder to `{project-memory-path}/tasks/{ongoing|completed}/{slug}/`
  (same TASK.md + sessions/ structure) instead of archiving/continuing it here.

## Step 2 — Present Summary

Summarize each ongoing task clearly:
- slug, title, priority, one-line description
- ownership flag from Step 1.5, if any: "⚠ matches project {slug} — recommend moving to {project-memory-path}/tasks/"

Then ask the user (via the calling session) to classify each:
- Which are DONE this session?
- Which are ABANDONED?
- Which remain ONGOING (still in progress)?
- Which are flagged for MISFILED (belongs to an existing project) — move now?

Wait for user input before proceeding.

## Step 2.5 — Relocate Misfiled Tasks

For each task the user confirms as MISFILED:
1. Move the whole folder `{agency-root}/tasks/inbox/ongoing/{slug}/` → `{project-memory-path}/tasks/ongoing/{slug}/` (or `completed/` if the user says it's done) — preserve TASK.md + sessions/ intact, no rewriting.
2. Do NOT leave a copy behind in the inbox.
3. Note the relocation in the per-task session log (Step 4) of the destination, not the inbox.

## Step 3 — Archive Tasks

For each task marked DONE:
1. Update TASK.md status to "done"
2. Move folder to `{agency-root}/tasks/inbox/completed/`

For each task marked ABANDONED:
1. Update TASK.md status to "abandoned"
2. Move folder to `{agency-root}/tasks/inbox/archived/`

For each task marked ONGOING:
1. Leave in `{agency-root}/tasks/inbox/ongoing/`
2. Append session notes to TASK.md
3. Create per-task session log (see Step 4)

## Step 4 — Write Per-Task Session Logs

For each ONGOING task, create:
`{agency-root}/tasks/inbox/ongoing/{slug}/sessions/YYYY-MM-DD.md`

## Session — YYYY-MM-DD HH:MM UTC

**was_doing**: [what was being worked on]
**just_finished**: [what completed before stopping]
**doing_next**: [specific next action]

### Notes
- [any session notes]

## Step 5 — Update TASK.md for Ongoing Tasks

Append to the Notes section of each ongoing task's TASK.md:

---
## Session Wrap — YYYY-MM-DD
**status_check**: still in progress
**last_action**: [brief description]
**next_action**: [specific next step]
**blockers**: [any blockers hit, or "none"]
---

## Step 6 — Confirm

Output only: wrap done!
Then stop. No further narration.

subagent_type: general-purpose
model: sonnet

Wait for the subagent to complete. You (the caller) do nothing else.