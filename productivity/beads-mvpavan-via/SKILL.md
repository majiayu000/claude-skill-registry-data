---
name: beads
description: Use for Beads dependencies, intake states, recovery, workstream tracking, or unfamiliar task-lifecycle operations. Routine tracking uses AGENTS.md and runtime context.
disable-model-invocation: false
---

# Beads

Use Beads as the durable work tracker, following `.beads/beads.md`. Routine
tracking follows AGENTS.md and supplied runtime context without loading this
reference workflow. Recover missing context with `bd prime`; if empty, use
`bd where`. For command syntax, consult `references/commands.md` or current help.

## Repository conventions

- Attribute every write with `--actor "<runtime>:<session-or-purpose>"`.
  Labels use lowercase kebab-case; priority is 0–4, with 0 critical.
- Reuse the work item's record. Create independent children only when the work
  benefits from separate ownership or acceptance; add actual prerequisite edges.
- Check for a governing spec before creating an epic. `--spec-id` carries the
  spec, `--design` the roadmap, and notes carry `plan: <path>`. Explain absence
  of a spec in the issue. Spec IDs do not inherit to children.
- Phase epic titles start `[<phase-id>]` and carry `ws-<name>`; stage acceptance
  must match the roadmap's Verify contract. Intake, idea and backlog states are
  defined in `.beads/beads.md`, not invented by each workflow.
- Close only after acceptance holds, with verification evidence in `--reason`.
  Generated workstream mirrors come from `scripts/bd-render-tracking.sh`;
  missing tooling is a reported limitation, not permission to hand-edit mirrors.

## Explicit repository overrides

Beads stores work, not general persistent knowledge. This repository deliberately
chose file-based memory over `bd remember`; preserve that choice unless changed.
Write persistent memory only when explicitly requested, and follow any higher-
priority runtime instructions governing its destination.

Use conservative Git authority. Session close normally refreshes the Beads export
when records changed; an explicit user restriction on writable paths takes
precedence, so report a deferred export rather than editing outside that scope.
