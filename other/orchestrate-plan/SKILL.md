---
name: orchestrate-plan
description: "Use whenever execute-plan runs, as the plan's orchestrator: settling the mandate, running the plan phase by phase on the swarm board, dispatching the plan's workers once, posting each phase's tasks to them, watching the board, verifying merges, and handling the branch and pull request. Not for keeping the tracker or deciding when to pause (execute-plan), and not for doing a task (the swarm-worker agent)."
---

# Orchestrate a plan

**Load the `orchestrate` skill and the `swarm-board` skill's orchestrator side with this one.** The first holds the charter protocol, dispatch, briefs and findings; the second everything said on the board, and replaces the `orchestrate` skill's *Watching*. Here the charter is the plan's *Mandate*; a member is a seat's worker for the whole run, given one task per phase. The phases, seats and roles are the plan's; the cut is the `write-plan` skill's `references/phases.md`.

## The mandate

Read the plan's *Mandate* section. Ask what it leaves open before the first phase, with the questions of `references/mandate.md`, and write the answers there and in the line under the tracker.

## The run

- **Every phase runs on the board, from the first to the close, whatever its width.** The board is the run's record, the person's view and the next phase's memory. Running a phase off it, or merging a seat's work yourself, changes the mandate, which is the person's.
- **One board run for the plan**, opened before the first phase (`--kind task`, the plan's URL as `--link`, `--protocol build-verify` when `verify:` is on), one row per seat for the whole run: the builders `w1` … `w<N>`, each `role` naming its area, and the verifiers.
- **Leave the plan's branch checked out nowhere** while the run is open (detach the main checkout): a worker fast-forwards it from its worktree. Re-run each done-when in a detached worktree of your own.
- **Every seat is dispatched once, at the run's open**, all at once: builders on the plugin's `swarm-worker` agent in their own worktrees, verifiers on `verifier`, with the briefs of `references/brief.md`, read before the first dispatch. A worker stays for the whole run; one whose context runs long is replaced in the same seat.

## A phase

1. **Write its tasks now**, at most one per seat, as the `orchestrate` skill's `references/tasks.md` says, from the phase's goal, every seat's role and area, and what the run taught so far. The tracker's placeholder becomes the phase's seats, each a subgraph whose steps are its task's done-when.
2. **Open it**: `phase <name> "<text>"`, the text naming every seat's part, then post each task to its worker. A seat with no task in this phase is told `done <name>` now.
3. **Watch the board**: it replaces the periodic check and the digest. Each seat's state, and the `stalled`, `gone`, `idle` and `liveness` events, are read and answered as the `swarm-board` skill's orchestrator side says; a drift is answered on the board, by its interrupt.
4. **A merge**: re-run the task's done-when on the merged branch, and what the testing prompt asked for; tick its steps.
5. **The phase closes** when every task is ticked and the full check is green on the merged branch: the board's `all-done`, then that check. Only then is the next phase's tasks written. A worker that stopped on a finding: fix the task (or the plan, for a decision) and post it again, or pause when the finding changes the phase.

**Two seats' agreements are theirs.** One that changes a decision the plan took becomes a row in the plan's decisions, as the `execute-plan` skill says.

## Verification: the build-verify protocol

**When the mandate's `verify:` is on, the plan runs the `orchestrate` skill's build-verify
protocol** (`references/protocols/build-verify/protocol.md`, read before the run opens): the
plan's phases are its builds, its seats its builders, the validator its verifier `v1` (one per
focus when the mandate names several), dispatched at the run's open with the builders, dormant
until a verify phase. **A verify phase is yours to open** after each phase or at the
end, as `verify:` says, its message the protocol's. **The verifiers' tables are judged** as the
`orchestrate` skill's `references/findings.md` says, and **the judged table decides the next
cut**: the next phase as planned, amended, a fix phase of the rows that stand, or a pause when a
finding breaks a decision. Write what changed into the plan before cutting. The mandate's `loop:`
bounds the fix phases a verify may add beyond the plan's own.

A verifier that ended (its context spent) is replaced by a fresh one in the same row. No
`verify-<app>-<focus>` skill and the person wants one: the `verification-skill-create` skill runs
before the first phase; else the verifier is `instructed`, its steps in each verify message.

## Branch and pull request

- **One branch for the plan, one pull request**, opened as a draft (`gh pr create --draft`) on the first push; give the person its URL and write its number into the state node. Marked ready where the pace merges or hands it to the person.
- **Never delete a branch**, and never pass the option that deletes one on merge.
- **Whatever merges leaves the branch green**: complete, or inert where it is not yet.

## The close

**Close the run on the board once the last phase closes**, before the plan's close. A step the person does (a walk, a trial) stays open in the tracker and never holds the run open.
