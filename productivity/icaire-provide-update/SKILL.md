---
name: icaire-provide-update
description: Capture ICAIRE progress updates into the remote ICAIRE brain. Use when the user dumps notes about progress, decisions, blockers, questions, initiative movement, people updates, or next actions and wants ICAIRE memory updated.
---

# ICAIRE Provide Update

Turn unstructured ICAIRE progress notes into durable remote brain updates.

## Contract

- Use the ICAIRE Cortex MCP connector as the source of truth and write target.
- Prefer direct remote writes. Do not only summarize in chat when the user is
  providing an update for the brain.
- Use paths relative to the remote brain root, such as `meetings/...`,
  `initiatives/...`, `people/...`, `inbox/...`, and `tasks/...`; do not prefix
  paths with `cortex/`.
- Before choosing target pages or task paths, call ICAIRE MCP `filing_rules`
  and follow the compiled `FILING.md` guidance it returns. If that tool is
  unavailable, list and read the relevant `FILING.md` files directly; do not
  expect a page named `filing_rules` to exist.
- Preserve uncertainty. Separate confirmed progress, inferred implications,
  blockers, open questions, and candidate tasks.
- Before marking any task `done` or `archived`, either create or link the
  successor task and use `Next task: tasks/<slug>` in the timeline entry, or
  state `No successor task needed: <reason>`.
- Verify every write by reading the changed page or listing the created task.

## Workflow

1. Identify the update source, date, people, initiatives, deliverables, and
   whether the notes include decisions, progress, blockers, questions, or tasks.
2. Retrieve filing rules and context with ICAIRE MCP `filing_rules`, `search`,
   `query`, `list`, and `read`.
3. Update stable pages when the note changes durable knowledge:
   - initiative progress, status, milestones, blockers, dependencies
   - people responsibilities or commitments
   - deliverable status
   - open questions or unresolved triage notes
4. Create or update task pages for concrete next actions:
   - Prefer MCP `tasks/create`; use `tasks_create` only if the client cannot
     call slash-named tools.
   - Assign only active members from `members/list`; use `me` for the current
     authenticated member only when the note clearly assigns the action to them.
   - When recording completion, create or identify the next concrete task first
     unless no successor is needed, then include the completion handoff in
     `tasks/update`.
   - If no active member can be identified, write the item to `inbox/` or report
     it as unassigned instead of assigning it to an arbitrary person page.
5. Verify persistence with `read`, `list`, or `tasks/list`.

## Output

Return:

- `Updated`: pages changed or created
- `Tasks`: task pages created or updated
- `Open Questions`: unresolved points
- `Unassigned Items`: concrete work without an active member
- `Verification`: read/list checks performed

## Guardrails

- Do not invent owners, dates, status, or initiative names.
- Do not assign tasks to external people or non-members.
- Do not create duplicate initiative, person, meeting, or task pages when an
  existing page should be updated.
- Do not claim the remote brain was updated until the write is verified.
- Do not bypass the MCP `filing_rules` tool by guessing from stale local
  conventions or by reading a nonexistent `filing_rules` page.
