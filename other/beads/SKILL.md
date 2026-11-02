---
name: beads
description: Use for Beads (bd) work beyond the core rules injected at session start - creating epics, plans or decision beads, dependencies and gates, triage, recovery, workstream tracking, reviews, setting up or joining a Beads project, or questions about Beads policy.
disable-model-invocation: false
---

# Beads

Beads (`bd`) is the durable work tracker. Every session receives the core
rules (`references/prime.md`) at start and after compaction. If they are
missing, run `bd prime`:

- it prints nothing: run `bd where`;
- it prints bd's built-in text instead of `# Beads: core rules`:
  `.beads/PRIME.md` is not linked (`references/setup.md` §2, step 8).

## In short

- Six types: `epic` (top level), `feature`, `task`, `bug`, `spike` (questions
  and ideas), `decision`. One label: `human`.
- Fields have one job each: description why/what, design how, acceptance
  done-when, `spec_id` the anchoring document, `bd note` running state and
  the plan path, `bd comment` attributed evidence and answers, close reason
  the evidence.
- Every wait is an edge: a `blocks` dependency, a `human` task, or a gate.
  Not now is `bd defer`; deferred beads are the backlog.
- Every write carries `--actor "<coding-agent>:<unique-id>"`, the same all
  session. Claim when starting, unclaim on pause, close with evidence.
- Conservative git authority: no commits, pushes or Dolt sync without the
  owner's authority.
- Knowledge goes in files, not `bd remember` or `bd kv`. Preserve that
  choice unless the owner changes it.
- Repository exceptions (`references/usage.md` §22): the workflow engine's
  `wf:attention` label, and a deferred export when the owner restricts
  writable paths.

## Read when needed

| Need | Read |
|---|---|
| Any rule in detail: types, fields, workstreams, waits and gates, triage, claims, reviews, session close, hygiene, traps, commands | `references/usage.md` |
| Installing bd, adopting Beads in a project, joining from a new machine or clone | `references/setup.md` |
| The exact text sessions receive, including the common commands | `references/prime.md` |
| Whether bd really behaves a certain way: the tested guide to every feature | `harness_lifecycle/beads/capabilities-1.3.0.md` |
| An exact command, subcommand or flag (generated; search it, do not read it whole) | `harness_lifecycle/beads/cli-1.3.0.md`, then `bd <command> --help` |
| Upgrading bd or migrating Beads databases (owner procedure) | `harness_lifecycle/beads/upgrades.md` |
| bd's built-in prime text, for comparing after an upgrade | `harness_lifecycle/beads/prime-original-1.3.0.md` |

## Scripts

- `scripts/bd-render-tracking.sh` regenerates the workstream status files
  from Beads (`usage.md` §16). Run it with `BD_RENDER=1`; never hand-edit
  its output. The ideas board lists deferred spikes; the backlog board lists
  every other deferred bead.
