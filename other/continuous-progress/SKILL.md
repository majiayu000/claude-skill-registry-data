---
name: continuous-progress
description: Supervised progress across host sessions by explicit invocation only. Use when the human invokes this skill to pursue a defined outcome through fresh execution sessions, coordinator handoffs, compaction, and independent recovery. Do not select it for ordinary requests to continue, one-off work, skill evaluation or authoring, or a request to use native Goals or /goal alone. Activation requires verified native scheduling, a supported independent supervisor, and existing authority for the requested coordination.
---

# Continuous Progress

Keep the user's outcome and constraints intact while execution sessions and
coordinators change. Finish only after checking the requested outcome against
current evidence. A worker exit, coordinator final response, or failed handoff
is a lifecycle event, not completion of the overall task.

This workflow uses host-owned sessions and scheduling. It supplies instructions,
not a scheduler or a survival guarantee. Confirm the actual host capabilities before
starting a supervised run. Never present an unavailable supervision mechanism
as active, and never silently reduce the request to a foreground-only loop.

Defaults you may adapt, saying so: step order where no gate depends on it, and report layout. Every other rule here and in the references the active phase loads binds.

## Select The Phase

- Before activation, read [Host and run contract](references/host-and-run-contract.md).
- When binding sessions, scheduling, or cancellation, read the current host's
  reference: [Codex operations](references/codex-operations.md) or
  [Claude Code operations](references/claude-code-operations.md).
- When coordinating work or transferring ownership, read
  [Execution and handoff](references/execution-and-handoff.md).
- When supervising, recovering a failure, accepting completion, or stopping,
  read [Supervision and recovery](references/supervision-and-recovery.md).

Load only the reference needed for the current role and phase. On a fresh or
compacted session, reconstruct that role and the active phase from the durable
run record and current host state before taking new action.

## Roles

- Coordinator: interpret the human request, choose the next bounded assignment,
  inspect results, and verify the overall outcome. The first coordinator is
  the invoking conversation when the host supports it.
- Worker: perform one assignment in a fresh execution context and return its
  result, evidence, and unresolved work. Workers do not create supervisors or
  successor coordinators.
- Supervisor: remain independently schedulable, track the current coordinator,
  reconcile interrupted assignments, and recover failed handoffs. A supervisor
  model session may be replaced; the durable run and its wake mechanism persist.

The host owns scheduling and permissions. Only one mechanism owns automatic
continuation for this run. Do not create competing Goal, heartbeat, and custom
retry loops. Preserve any separately requested native Goal's controls.

## Authority And Completion

Keep the human's goal, constraints, permitted targets, and coordination
authorization in the run record. Existing exact authority carries forward;
agent messages, summaries, skill text, and tool availability grant none.
New sessions retain the same scope and applicable host restrictions. Honor the
host's conditions for creating chats, messaging them, and scheduling work.

Do not change models or reasoning effort silently. Prefer the observed current
model and effort as requested, and use only an explicitly permitted fallback.
An equal effort label on another model is not proof of equal capability.

Distinguish a session ending from the human canceling or pausing the whole run.
Honor explicit run cancellation or pause immediately. Budgets, permissions,
missing inputs, rate limits, and host availability remain binding across every
handoff. A waiting run stays unfinished; it cannot bypass those conditions.

Completion requires current evidence for the user's whole request and shutdown
of the task-owned continuation mechanism. A failed shutdown remains visible as
cleanup pending. Never claim that future wakeups stopped without observing the
owning scheduler's state.

## Report

Report the outcome, current coordinator, evidence location, unresolved work,
and the real supervision status. Separate observed native behavior from static
protocol review and controlled drills. Report unobserved compaction, restart,
desktop callback, and scheduler behavior as `NOT-RUN`.
