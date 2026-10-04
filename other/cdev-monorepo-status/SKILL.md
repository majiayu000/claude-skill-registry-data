---
name: cdev-monorepo-status
description: Use when the user asks where a CDev Monorepo workspace stands — progress of the active SYSTEM sprint (or a named one) across its repositories, measured on three axes, functional requirements, non-functional requirements and user stories — after a wave of SYSTEM_BATCHes has run, before deciding what to run next, or when coming back to the workspace. Also when the user invokes /cdev-monorepo-status or asks "status of the system sprint", "where is the monorepo", "status funcional del monorepo", "por dónde va el sistema".
---

# CDev Monorepo Status

A read-only reading of a conditioned **workspace**: how far a SYSTEM sprint's intent has been
walked across its repositories. **It edits no file and marks no state** — not in the workspace,
not in any repository.

Requires a conditioned workspace (`workspace/repos.yaml` and a global `docs/develop/`). Not
conditioned → propose the `bootstrap-monorepo` skill and stop.

**The method is not restated here.** The three axes, how each item is engineered at read
time, the states, the estimated percentages, the report's shape, the `since` delta and the
rules live in one place — the `cdev-status` skill: resolve this skill's base directory to its
real path, read `../cdev-status/SKILL.md`, and apply it to the SYSTEM sprint. What follows is
only what the system level adds.

## Scope

The `ACTIVE` SYSTEM sprint of the global `SPRINTS.md`; an argument names another, `all` rolls
up every SYSTEM sprint. Two independent numberings: a SYSTEM sprint is never a local one.

## Sources, beyond those of `cdev-status`

- The SYSTEM_BATCHes of the sprint and their references (repo / local sprint / local batch /
  required / depends_on), and their declared sync points.
- The cross-repo contracts under `workspace/contracts/` — acceptance written there is a
  first-class source of requirements.
- **Local truth.** For every affected repository, its own `SPRINTS.md` and
  `AGENT_PROGRESS.md`, reached through the bidirectional references and read **in the
  repository itself**. Where the workspace and a repository disagree about a state, flag the
  divergence and report the repository's. The workspace's state snapshot file is a photograph
  and decides nothing: never read a state from it.
- **Read narrowly, here above all — slices, never fewer sources.** A reference names the local
  sprint and the local batch: read that batch **and its handoff entries** in the repository —
  not the repository's whole plan or log, and nothing of a repository the SYSTEM sprint does
  not reference. The sprint's contracts and the decisions about it are still read: "met"
  rests on a handoff entry, and a contract's acceptance is a requirement. One pass, one
  reader.

## What the report adds

After the three axes and before the executive reading, one compact table:

`Repository | Local batches for this SYSTEM sprint | State | Blockers`

A repository that cannot be reached reads **"not derivable"** for that repository, by name —
the system-level axes then say which of their items rest on it.

The executive reading also carries the system-level risks: SYSTEM_BATCHes `BLOCKED` on a human
decision, sync points whose artifact does not exist yet, system verification recorded
`not-run` over references that read done.
