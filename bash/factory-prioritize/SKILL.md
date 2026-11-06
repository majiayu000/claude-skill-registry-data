---
name: factory-prioritize
description: Change what the claude-factory works on next in this repo. Use when the user says "do X first", "bump this" or "put that on hold". Use also when the user says "unqueue" or "stop the factory working on Y". Use also when the user says "reprioritize the factory" or asks why the factory picked a bead. Works with bd alone or with a local factory CLI.
---

# factory-prioritize

The factory picks queued beads in this order:

1. The pm's plan (`factory plan show`), when it is less than 2 hours old. The pm ranks each rig's ready beads once an hour, and soon after a run finishes.
2. Otherwise, `bd ready` order: priority first (`0` is the most urgent, `4` is the backlog), then the oldest.

The pm can change the order of P2 to P4 beads. It does not change a P0 or P1 bead. It only proposes such a change. To make sure that a bead goes first, give it P0 or P1.

Always show the user the change before you make it. List the bead ids and their old and new state. Then wait for a yes.

## See the queue

```bash
bd list --label factory --status open --sort priority     # queued, in priority order
bd ready --label factory                                   # queued and able to start now
factory plan show 2>/dev/null                              # the pm's ranking and reasons, local factory
```

## Change the order

| The user wants | Command |
|---|---|
| This first | `bd update <id> --priority 1` (or `0` for an incident) |
| Lower | `bd update <id> --priority 3` |
| Queue it | `bd update <id> --add-label factory` (or `factory queue <rig> <id>`) |
| Unqueue it, keep it open | `bd update <id> --remove-label factory` |
| Hold it until a date | `bd defer <id> --until 2026-11-01` |
| Hold it until another bead is done | `bd dep add <id> <other-id>` |
| Never | `bd close <id> --reason "..."`, only on the user's explicit word |

Add a comment with the reason, so that the pm and the manager see it: `bd comment <id> "Owner: first, because ..."`.

If bd syncs this repo to another machine, run `bd dolt push` after the change. The factory pulls every 5 minutes.

## A bead that a run already holds

A bead in progress with the assignee `factory/<run>/...` is in a run. A label or a priority change does not stop that run.

- **Tell the run**: `factory mail <run> manager "<text>"` (local factory). Otherwise, put a comment on the bead. The manager reads the bead comments.
- **Stop the run**: `factory abort <run>`. This ends the run's work in progress. Do it only when the user explicitly asks for it. After the abort, the bead has no assignee and has the deferred status. Undefer it to hand it back.

## Do not

- Do not change a bead that has the label `owner`, `human` or `ship` without the user's word. These labels mark the user's decisions and the ship queue.
- Do not remove another person's assignee.
- Do not change the rig's goal or `rigs.json`. That is the user's change, in the factory home.
