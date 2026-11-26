---
name: multi-agent-relay
description: >-
  Stand up and drive multiple coordinating agents that build a feature through a filesystem
  relay: a driver that authors one task prompt at a time, an implementation agent (a standing
  poll-loop session OR a freshly spawned subagent) that implements and tests, and a shipping
  agent that commits, reviews, fixes, and ships - all coordinating through report files with a
  fixed status-line protocol and background monitors. Use when executing an approved multi-task
  sequence across one or more repos with separate agents that must stay in distinct lanes.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task
---

# Multi-agent filesystem relay

A way to build a feature as an ordered sequence of tasks, with the work split across separate
agents that never talk directly - they coordinate by writing and polling files in one directory.
The filesystem is the only channel: no agent pastes work into another's chat, and each agent
watches exactly one glob so it only ever sees its own traffic.

This is a standalone, three-role pattern with two interchangeable implementer forms (a standing
poll-loop session, or a subagent spawned per task) and monitors that also catch fix-batch
hand-offs. It runs the build itself; it is not a NightVision scan. Pair it with the security
skills (run `chain-attacks`, `authz-review`, `app-security-scan`, or `ship-check` as tasks or as
the shipping agent's review lenses) when the feature being built needs security work.

## Portability

The relay is just files, `bash`, `curl`-free report polling, and either a standing session or a
subagent spawn, so it runs on any coding agent and any model, Codex included. The one
host-specific piece is how the driver spawns the implementer in the spawned-subagent mode (the
`Task`/Agent tool in Claude Code, the equivalent in another harness). Where the host cannot spawn
a subagent, use the standing poll-loop mode instead: a human starts the implementer session once
from a bootstrap prompt, and everything else is identical. Nothing here depends on a
NightVision-specific tool.

## When to use

- An approved, ordered task sequence exists (a sequence doc with per-task files/acceptance), and
  you want each task implemented, reviewed, and shipped as a discrete unit.
- The work spans one or more repos on a shared feature branch.
- You want implementation isolated from shipping (commit / review / push / tracker), so the
  implementer stays in one narrow lane and the shipper in another.

Do NOT reach for this for a single task, a quick fix, or work with no review/ship cycle - the
coordination overhead only pays off across a sequence.

## The three roles

| Role | Does | Does NOT |
|---|---|---|
| **Driver** (you) | Author one `*-impl.md` task prompt at a time; create/verify its tracker ticket; arm a monitor; on a terminal status, author the next task. Optionally apply small fixes and author `*-fix.md` batches. | Commit, review, push, move the tracker, or implement (unless the run says the driver also ships). |
| **Implementation agent** | Implement one task + its tests, run them green, keep a live report file, flag judgment calls, apply `*-fix.md` batches. Two forms: a **standing** session polling a glob, or a **spawned subagent** that implements once and returns. | Commit, push, run reviews, or touch the tracker. Decide design questions - it flags them. |
| **Shipping agent** ("the driver" in report wording) | Commit per touched repo, run the review lenses, consolidate findings, send `*-fix.md` batches, run the full suite, push, move the tracker, set the terminal status line and name the next task. | Implement the feature itself. |

Keep the role names straight in prompts: the report contract calls the **shipping agent** "the
driver", because from the implementer's view that is who drives commit-and-ship. If you (the task
author) also call yourself "driver" in your notes, disambiguate in memory.

## The filesystem channel

One directory holds every request and report, e.g. `analysis/<thread>/prompts/`. Naming is
symmetric (request -> report) and the `-report` suffix keeps each agent's watch-glob off its own
output:

| File (`<task>-` prefix) | Written by | Consumed by | Watcher's glob |
|---|---|---|---|
| `<task>-impl.md` | driver | implementation agent | `*-impl.md` |
| `<task>-impl-report.md` | implementation agent | driver, shipping agent | (polled) |
| `<task>-fix.md` | shipping agent (or driver) | implementation agent | `*-fix.md` |
| `<task>-design-review.md` | driver | design-review agent (optional lane) | `*-design-review.md` |
| `<task>-design-review-report.md` | design-review agent | driver | (polled) |

`*-impl.md` never matches `*-impl-report.md`; `*-design-review.md` never matches its own report.
So each standing agent sees only its own requests, never the other agent's traffic or its own
output. Use absolute paths inside every file: a relayed file may be read from a different working
directory than the one that wrote it, so relative paths break. ASCII only (anything may reach a
tracker).

## The status-line protocol

Every report file carries a single top line `**Status: ...**` with a local timestamp. It is the
state machine the whole relay turns on; monitors key on it. The states:

- `**Status: IN PROGRESS: <step> (<time>)**` - set on pickup; kept current.
- `**Status: DONE, awaiting fix batch (<time>)**` - implementation is green; the implementer now
  polls `*-fix.md` (standing) or stops and returns (spawned subagent).
- `**Status: FIX BATCH n IN PROGRESS (<time>)**` - applying a relayed `*-fix.md`; returns to
  `DONE, awaiting fix batch` when done.
- `**Status: DONE, shipped by the driver (<time>). Next: <next-task>**` - TERMINAL. Only the
  shipping agent sets this. This is the driver's trigger to author the next task.
- `**Status: BLOCKED on owner: <one-line question>**` - a design decision the agent must not make;
  surface to the human, do not proceed.
- `**Status: BLOCKED: <why>**` - a tooling or safeguard stop on the WORK itself (not a design
  question); surface it (see "If a safeguard blocks a task").

The driver's ONLY completion trigger is `DONE, shipped ... Next:`. The implementer's
`DONE, awaiting fix batch` is NOT the driver's trigger - it is the shipping agent's. Keep that
distinction or you will author the next task before the current one ships.

## The driver loop

1. Read the next task's entry in the sequence doc; cross-check every cited symbol/line against the
   actual code (lines drift). Distill the load-bearing spec INTO the prompt - do not tell the agent
   to read the whole design doc.
2. Create/verify the tracker ticket for the task (a child of the parent/epic ticket in your issue
   tracker). If a prior ship pre-created it, verify and reuse; never file a duplicate - search the
   tracker first.
3. Write `<task>-impl.md` from the template, carrying the domain's security/trust constraints
   verbatim and pinning the report contract and the `Next:` task.
4. Arm a background monitor on `<task>-impl-report.md` (see Monitors).
5. Hold. On the monitor firing:
   - `DONE, shipped ... Next: <n>` -> read the close-out, record it, author task `<n>`.
   - a `<task>-*-fix.md` appeared and no standing implementer is polling -> apply it (spawn a fresh
     subagent, or apply mechanical fixes yourself).
   - `BLOCKED on owner` -> surface to the human; do not proceed.
6. Record each milestone to durable memory or the sequence doc (the loop outlives context
   compaction).

## Monitors

Watch by waiting, never by re-reading in a tight loop. Run `templates/monitor.sh` in the
background; it fires on a TERMINAL status line or on a fix-batch file appearing, and re-invokes you
on exit. Use `/usr/bin/grep` (zsh's `grep` may be ugrep and mis-handle `-E`/globs). One monitor per
in-flight task; re-arm at each pickup because prompts get amended.

## Writing a good task prompt

The prompt must stand alone for a fresh agent that has only the repo, not your conversation:

- **Distill the spec into the prompt.** Inline the load-bearing requirements; have the agent read
  CODE (the precedents to mirror at `file:line`, the dependency tasks' code), not the whole design
  doc - that burns budget and invites scope creep.
- **Be concrete and structural.** Name the exact files, symbols, and lines; state what changes and
  what stays byte-for-byte; state what is OUT of scope (the parts belonging to adjacent tasks).
- **Carry the domain's security/trust constraints verbatim** so the implementer honors them.
- **Give acceptance tests that fail without the change** (prove RED -> GREEN), and the repo's
  conventions (formatter, lint, ASCII, migrations, the repo's own testing skills).
- **Pin a fixed report contract** (status lines + a `## Progress` log) and the `Next:` task.
- **Verify your distillation against the source** before handing over - a deliverable summarized
  out is a deliverable dropped.

## If a safeguard blocks a task

A safety classifier or permission check stopping a task is an oversight signal, not an obstacle to
engineer around. Do not reword, obfuscate, or re-route the request to get the same blocked action
through by another path. Instead:

1. Set/record the block plainly (`**Status: BLOCKED: <why>**`).
2. Surface it to the human with what was being attempted and why, and let them decide.
3. If only part of a task is blocked, finish the unblocked part and report the remainder as blocked.

This applies to the driver and to every agent the run uses.

## Two implementer modes

Pick one; they are interchangeable from the shipping agent's view (both end at a report file).

**Standing poll-loop** - a long-lived implementer session the human starts once from a
domain-neutral bootstrap prompt (`templates/impl-agent-bootstrap.md`) kept OUT of the polled
directory so it never matches a watch-glob. It polls `*-impl.md` / `*-fix.md`, does the work,
writes its report, polls again. Use when you want a persistent implementer, or when the driver's
key cannot spawn the implementer model itself.

**Spawned subagent** - the driver spawns a fresh implementer per task via the host's subagent tool.
Use when the driver can spawn the implementer model directly (one less standing session to manage).
Points:
- `model` set to the implementer model; set `effort` only if the human asked; use a fresh
  (non-fork) agent so it starts clean on a self-contained prompt.
- The spawn prompt (`templates/subagent-spawn.md`) points the subagent to the task file as the
  single source of truth and states the report contract; the task file carries the detail.
- The subagent implements, writes the report to `DONE, awaiting fix batch`, then STOPS and returns
  a summary - it does NOT poll. The shipping agent still ships from the report. Because no standing
  implementer is polling, arm the combined monitor that also catches a `*-fix.md`, and apply any
  fix batch by spawning a fresh subagent.

Verify the report's top status line in the file (ground truth), not only the agent's hand-back - a
relay summary can drift from the file.

## Setup (fresh stand-up)

1. Resolve: the sequence doc, the repo root + feature branch, the parent/epic ticket, the
   implementer model, and the security/trust constraints to carry verbatim.
2. Pick the implementer mode (standing vs spawned).
3. Confirm a shipping agent exists and is watching the report files (or that the run folds shipping
   into the driver). Ask the human if unsure - a missing shipper stalls every task silently.
4. Create the prompts directory: `mkdir -p analysis/<thread>/prompts`.
5. If standing: hand the human the bootstrap prompts for the implementation agent and (optionally)
   the design-review agent; they start those sessions. If spawned: nothing to pre-start.
6. Run the driver loop, one task at a time.

## Templates

- `templates/implementation-task.md` - the per-task `*-impl.md` prompt (distill + report contract).
- `templates/subagent-spawn.md` - the subagent-tool prompt for the spawned-subagent mode.
- `templates/impl-agent-bootstrap.md` - the standing implementation agent's poll-loop bootstrap.
- `templates/shipping-agent-bootstrap.md` - the standing shipping agent's commit/review/ship loop.
- `templates/design-review-task.md` - the optional read-only design-review lane prompt.
- `templates/fix-batch.md` - a `*-fix.md` batch.
- `templates/monitor.sh` - the background report monitor (terminal OR fix-batch).

## Pitfalls (each from a real run)

- Authoring the next task off `DONE, awaiting fix batch` (the implementer's state) instead of
  `DONE, shipped ... Next:` (the shipper's). Wait for the shipper.
- Treating the implementer's hand-off messages to the shipping agent as YOUR trigger. They are
  addressed to the shipper; hold.
- Under-scoping a task when the sequence-doc entry narrows an underlying decision. Cross-check the
  entry against the decision it cites and carry the broader load-bearing intent (or flag the gap).
- A duplicate tracker ticket because both the driver and a prior ship created one. Search first.
- Trusting a relayed status over the report file. Read the file.
- Letting a spawned subagent poll forever. A one-shot subagent implements and returns; the driver
  handles fix batches.
- zsh `grep` quirks in monitors. Use `/usr/bin/grep`; quote or `find` globs.
- Leaving stale "DROPPED"/"DEFERRED" markers in the sequence doc when a task is re-opened - the
  shipping agent reads those docs; correct them.

## Related skills

Use this to drive a build; the security skills are what it builds and reviews. `ship-check` is the
natural shipping-agent review lens for an agent-built app; `authz-review` and `chain-attacks` make
good read-only review lanes or discrete tasks; `app-security-scan` runs a scan as a task; and
`ci-cd-integration` sets up the gate that keeps the shipped branch honest after the relay ends.
