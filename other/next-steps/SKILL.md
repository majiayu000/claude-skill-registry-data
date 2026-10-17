---
name: next-steps
description: Status overview of an .aiwork/ task folder — what is done, what is awaiting the human, what is blocked, and the one next action. Auto-detects the most recent task folder when no argument is given.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep
argument-hint: [spec-or-task-folder-path]
---

# Next Steps

Read-only status report for one `.aiwork/` task folder. Follows the `aiwork-protocol` skill; changes nothing.

## 1. Resolve input

`$ARGUMENTS` is a spec, plan, ticket, or task folder path. A file path resolves to its task folder (a ticket's is the folder above `tickets/`). With no args, find the most recently modified task folder per `aiwork-protocol` conventions. Nothing found → say so and stop.

## 2. Gather

Read frontmatter first, prose only where needed.

- **`intent.md`**: `status` (`proposed` / `accepted` / `declined`).
- **`spec.md`** (or the current `plan*.md` when there is no spec, skipping any with `superseded_by`): `status`, `blocked_by`, `verified`. Note whether the spec still has open questions, TBDs, or a non-empty Open Concerns section.
- **`tickets/`**, if present: for each ticket its number, title, `status` (`ready` / `in-progress` / `done`), `blocked_by`, `verified`, and the count of ticked vs unticked acceptance criteria. The **frontier** is every `ready` ticket whose blockers are all `done`.
- **`review*.md`**: present or not, and its `reviewed_sha`.
- **`implementation-notes*.md`**: any entries the human must act on.

Read the vocabulary as the protocol defines it:

- Ticket folders carry the truth in ticket statuses; the spec's own `status` is optional there.
- Without tickets, an absent spec `status` means unknown, not not-started.
- `agent-done` means the agent finished and handed over; report it as awaiting the human's check, never as finished. `done` on a spec is the human's call.
- Older folders may use `draft` / `active` / `complete` / `superseded`; map them to the nearest current value and say so.

## 3. Report

Brief. Print, in order:

1. **Headline**: task folder, then one line — intent status, spec status (or "tickets: N done / M in progress / K ready / J blocked").
2. **Tickets table** when `tickets/` exists: number, title, status, blockers, criteria ticked, `verified` passes. Skip the table for folders without tickets.
3. **Next action**, exactly one line, first match wins:
   - intent not `accepted` → decide the intent (`/aiwork:to-spec` waits on it)
   - no spec and no tickets → `/aiwork:to-spec`
   - spec with open questions / Open Concerns → resolve them; `/aiwork:implement-spec` stops on them
   - spec, no tickets, not small → `/aiwork:to-tickets`; small → `/aiwork:implement <spec>`
   - frontier non-empty → `/aiwork:implement-spec`, or `/aiwork:implement tickets/<NN>` naming the first frontier ticket
   - a ticket `in-progress` → resume it
   - all tickets `done`, no `review*.md` → `/aiwork:implement-spec` runs the wrap-up review
   - spec `agent-done` → the human exercises the feature and reads the code, then sets `done`
   - spec `done` → all done
   - spec `blocked` or every remaining ticket blocked → name the blocker
4. **Needs a human**: only if any exist — `blocked_by` causes, unresolved implementation notes, `done` tickets with unticked criteria or without an on-app `verified` pass (`behaviour` / `ux` / `human`), a review whose `reviewed_sha` is missing.
