---
name: plan
description: 'Turn requirements nobody scheduled into well-described tasks, edit tasks and milestones, and reconcile TASKS.md with the team''s own tracker Arguments: add <what> | sync | status | milestone <id> | (empty = find unplanned work).'
---

Use `macstack-dev:planning`.

**First, before any number is reported**, bring the statuses in line with what the audit
actually found:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/planning/references/task_status.py" macstack [--apply]
```

A task sitting `todo` that the code finished weeks ago inflates every count below it; a
task sitting `done` whose case the audit found `absent` deflates them, which is worse
because nobody goes looking behind a closed task. Report the moves, apply them with
`--apply` once the user agrees, and only then count.

With no argument: find the work nobody has planned. Run

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/planning/references/uncovered.py" macstack [--emit]
```

which classifies every case into five states — already planned · confirmed done by the
newest conformance review · found partial or blocked by it · **awaiting the client** ·
**neither planned nor checked**. Only the fifth is work.

**A case awaiting the client does not become a task.** Its text names a live `§A` id, so
nobody can finish it today; `TASKS.md` is a queue somebody picks from, and an item that
stops the person who picked it makes the whole queue untrustworthy. The `§A` question
holds that work — its *where the answer goes* line says what the answer unlocks — and the
task is written the day the answer lands. `--emit` withholds those skeletons and says how
many it withheld.

Read the audit verdicts before reporting a number. The first version of this reported
"63 cases with no plan" where 35 were already confirmed implemented: true, and useless.
A work list nobody believes is a work list nobody reads.

Then do the part the script cannot: **read the code** and fill each skeleton's `files`
and `acceptance`. Use `generated/ARCHITECTURE.md` as the map rather than a blind grep.
Acceptance names a test, and its strongest form is *remove X and this named test
reddens*. A bare filename is not acceptance; a line number is banned outright.

Three things this refuses to do:

- **Guess `files` or `acceptance` without reading the code.** If the codebase does not
  answer where something belongs, that is a finding — say so and leave the field empty
  rather than filling it plausibly.
- **Plan a case an audit already passed.**
- **Plan a case that is waiting on the client.** Name the `§A` ids and stop.
- **Invent a milestone.** A new milestone is a decision about scope and dates and it
  belongs to the owner. Take the last `M<n>` and ask before going past it.

Then stop. The handoff is the point: open plan mode and say *"take M15-T2 from
macstack/history/TASKS.md"*. Do not start coding here.

`sync` reconciles with the team's tracker in both directions and stops at every
disagreement rather than picking a winner. `status` and `milestone <id>` report
progress against `done_when`.