---
name: orchestrate-tickets
description: "Coordinate approved MAGA Tickets across Codex tasks: dispatch, recover, integrate, and archive. Use for bounded cross-task execution; exclude unapproved plans and product discovery."
---

# Orchestrate Tickets

Run approved Ticket contracts through fresh Codex project tasks. A Ticket may
produce a finding, prototype, diagnosis, review, delivery, or release result; it
does not have to be source-code implementation. This is an internal execution
capability, not the normal product-facing entry. Keep product decisions visible
and keep skill names, Git mechanics, validation tools, and task routing internal
unless the user asks.

## Preconditions

Proceed only when:

- The Product Owner approved the currently described Ticket set and every selected Ticket records `authorization: approved`.
- For every task that does not already exist, either the Product Owner explicitly
  approved its deterministic title or the project Autonomy Policy authorizes
  dispatch inside this already approved Ticket and its active-worker limit. Record
  `Task opening: approved` or `Task opening: standing-policy` for the exact title
  and attempt before dispatch.
- Each Ticket is a durable work contract with a user-visible outcome, acceptance criteria, blockers, authorization, and status.
- The contract is reachable from the worker's starting repository state or issue tracker.
- Codex task coordination tools are available.
- The project's Autonomy Policy has been read; it does not authorize new Tickets,
  expanded outcomes, or external/irreversible side effects.
- Short-lived read-only investigation may use a native subagent only when the
  project's `Delegate` policy has capacity. A subagent cannot write, commit,
  create another task, approve a request, or expand the Ticket.
- A thread Goal, when available, is only a bounded continuation aid. It never
  authorizes a Ticket, permission, release, or expanded outcome.

If task tools are unavailable, say automatic dispatch is unavailable and provide the next ticket pointer. Do not pretend a task was created.

Follow `AGENTS.md` and narrower ticket instructions. Never persist machine paths, usernames, `threadId`, `hostId`, `clientThreadId`, or wait cursors in tracked files.

## Name Tasks Deterministically

Use the project's language and these title shapes:

```text
Coordinator: <project> · <localized "project lead">
Manager:     <project> · <role> · <localized "management">
Worker:      <project> · <localized workspace or role> · <ticket-key> <user-visible outcome>
Replacement:<worker title> · <localized "retry N">
```

For example: `Inventory · Prototype · T002 Mobile stock adjustment flow`.

- Derive the project, workspace or role, Ticket key, and outcome from durable contracts. Prefer the Ticket's optional `workspace` value for bounded capability work; otherwise use its role. Name roles by responsibility, not generic code layers.
- Keep the stable ticket key. Do not put status, branch, worktree, thread IDs, or commit hashes in a title.
- Keep one active task per ticket. Increment the retry suffix only when replacing an unusable task.
- Do not rename workers as their status changes.
- Rename the current task with `codex_app__set_thread_title` when it is the coordinator and still has a generic title.
- Never create or keep a worker titled only with a generic capability such as `Research`, `Prototype`, or `Implementation`; the Ticket key and specific outcome are required.

## Manage Durable Roles

For a role whose contract says `Session shape: managed queue`:

1. Reuse an active same-project task with the deterministic manager title.
2. If none exists, propose its deterministic manager title and create it only when
   the project's Autonomy Policy covers that role queue or the Product Owner has
   approved the exact title; then pin it using the current host's sidebar tool and
   give it the role contract plus current project index as its only durable entrypoints.
3. Send newly approved Ticket pointers to that manager instead of creating another manager.
4. Let the manager apply this worker lifecycle within its role boundary; it must return product decisions and cross-role conflicts to the Project Lead.
5. Keep the role in repository state. Archive its manager task only when the role is retired or replaced, and record that durable fact first.

### Pin Through The Available Host Tool

Inspect the tools available in this session before pinning. The current desktop
mapping is `codex_app__move_thread_to_sidebar_section` with the existing task's
ID and `sectionId: "pinned"`. Report success only after the host confirms it.
If the tool is unavailable or fails, keep the existing task and return its exact
title with the uncompleted pin status; do not create a replacement. This desktop
mapping does not rename the bridge's separate task-metadata protocol.

Use this manager prompt:

```text
Carry the durable role at: <repository-relative role contract>

Read AGENTS.md, .ai-workflow/PROJECT.md, and that role contract. Coordinate only
approved Tickets owned by this role. Apply the installed task-orchestration
capability internally. Do not broaden product scope, store task identifiers in the
repository, or implement every Ticket in this management context. Return product
decisions and cross-role conflicts to the Project Lead.
```

Do not create a management task for `direct execution` roles. Dispatch their approved fresh Tickets directly from the Project Lead.

## Choose The Smallest Execution Shape

1. Keep a small, self-contained Ticket in the current task when it has no
   specialist `workspace` and remains Project Lead work.
2. Use the native `CodexBridge` subagent adapter before opening a worker when
   the question is short, read-only, inside the approved Ticket, and its result
   can return to the parent without durable integration. Check `Delegate`
   capacity and the selected model's native capability first.
3. Propose a fresh project task for a Ticket whose workspace is `research`,
   `prototype`, `delivery`, `diagnosis`, `review`, or `release` when the outcome
   needs a durable artifact, source change, commit, independent acceptance,
   distinct permission boundary, or user-visible follow-up. Create it when the
   project's confirmed `Dispatch` policy covers the approved Ticket and has
   capacity, or after explicit approval; the fresh task is required for its
   responsibility model and reasoning depth to take effect.
4. Run Tickets sequentially by default.
5. Run Tickets in parallel only when their blockers are complete, their write
   scopes do not conflict, and each task has an isolated worktree.

### Native subagent boundary

Give a subagent the smallest repository-relative pointers and one question. The
bridge supplies `experimentalApi`, `collaborationMode`, a read-only sandbox, and
the finite admission limit; the parent remains responsible for the Ticket.
It
returns a finding, uncertainty, or blocker to its parent. Do not give it a
commit requirement, a task-creation instruction, an external connector, or a
permission escalation. If the question grows into a durable artifact, source
change, or independent acceptance result, stop the subagent and dispatch a
named worker through the normal Ticket lifecycle.

Do not create tasks merely because the plan contains several bullets. Split on attention and ownership boundaries. Do not dispatch more live tasks than can be tracked in one `codex_app__wait_threads` batch.

## Find The Frontier

Select Tickets with `authorization: approved` that are `ready`, unclaimed, unblocked, and small enough for one fresh context. Read the index first, then open only the selected Ticket and its explicit references. A new, split, derived, materially expanded, resumed-deferred, or reauthorized-revoked Ticket is not executable until its own authorization is current; do not inherit approval from another Ticket or the legacy `task_creation` field.

If no ticket is ready, report the blocking product decision, dependency, permission, or external condition. Downstream tickets become ready only after every blocker is `integrated`, not merely `completed`.

## Execute And Close

Before recovering state or creating a worker, read
[dispatch and recovery](references/dispatch.md). Follow the host's explicit
new-task requirements even when a project Dispatch policy is approved.
While work is active or a result arrives, read
[observation and closure](references/closure.md). Integration requires the
returned result in project history, then a durable status update and archival.

## Keep The Product Conversation Clean

Report what behavior is being built, what is ready to try, and what decision is blocked. Do not ask the user to choose skills, testing styles, ticket order, branches, worktrees, retry mechanics, or review modes unless one materially changes product behavior or risk.
