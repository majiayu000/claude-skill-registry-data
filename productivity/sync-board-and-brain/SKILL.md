---
name: sync-board-and-brain
description: Reconcile ICAIRE Board tasks and initiatives with the remote ICAIRE brain. Use when a team member asks to sync the board and brain, update the ICAIRE board from recent work, reconcile board tasks with brain tasks, or review board/brain drift.
---

# Sync Board And Brain

Reconcile the ICAIRE Board execution view with the remote ICAIRE brain.

## Contract

- Use ICAIRE-specific skills and automations as the adapter layer. Do not add
  ICAIRE Board logic to BigBrain core.
- Treat the ICAIRE brain as the superset and richer source of context.
- Treat ICAIRE Board as the focused execution view for active Board initiatives.
- Use ICAIRE Cortex MCP for brain reads/writes: `filing_rules`, `me`,
  `members/list`, `tasks/list`, `tasks/create`, `tasks/update`, `read`,
  `create_page`, and `update_page` where available.
- Use ICAIRE Board MCP for board reads/writes. Start with `board_snapshot`; use
  `initiative_*`, `task_*`, and `step_*` tools for reviewed Board writes.
- Start every run with `filing_rules`, `me`, active `members/list`, Board MCP
  health or `initialize`, `tools/list`, and `board_snapshot`.
- Scan recent Codex threads available to this agent runtime, not only the
  current thread. Include only ICAIRE-relevant progress, decisions, blockers,
  open questions, and concrete next actions.
- Do not call Granola from this workflow. Granola discovery belongs to the
  single machine-wide BigBrain router; this workbench owns ICAIRE destination
  policy, not another scheduler.
- Use review-then-apply. Present proposed brain and Board changes first, then
  apply only after the user confirms or the invoking automation explicitly
  provides approval.
- Treat Board task content as user-facing execution content, not an audit log.
  Do not write sync metadata, brain slugs, mirror IDs, or phrases such as
  "brain sync", "brain mirror", "synced from brain", or "during sync" into
  Board initiative, milestone, task, step, or description fields.

## Identity And Scope

- Every Board initiative should have a matching ICAIRE brain initiative page.
- Every Board task should have a matching ICAIRE brain task page.
- Store stable cross-system identity in synced brain pages:
  - Board initiative ID or Board task ID
  - Board title
  - linked brain slug
  - last sync timestamp
- Prefer stable IDs over fuzzy title matching. Use title matching only to
  propose possible links for user review.
- Keep Board promotion selective. Push a brain task to the Board only when it
  clearly belongs to an existing Board initiative, is already linked to a Board
  mirror, or the user explicitly accepts it during review.
- Do not push minor unrelated admin tasks, loose meeting follow-ups, personal
  material, commercial/client work, or tasks unrelated to Board initiatives to
  the Board.

## Reconciliation Rules

- Brain context wins for richer details:
  - meeting-derived context
  - acceptance criteria
  - blockers and open questions
  - source links
  - clarifying notes
- Board state wins for execution placement:
  - current Board initiative and milestone
  - column, group, archive state, completion state
  - Board assignee and due date when they are actively maintained there
- If Board and brain conflict ambiguously, surface it in the review step. Do not
  silently choose a side.
- Board descriptions are not update journals. Use Board writes primarily to:
  - create new Board tasks from new information when they clearly belong on the
    active Board
  - update task status, completion, archive state, assignee, due date, milestone,
    or steps when execution state changed
  - clarify or rename a task title only when the current title is misleading or
    incomplete
  - edit a description only when it materially improves the task itself, such as
    acceptance criteria, blocker context, or a concise scope clarification
- Never add a timestamped run note, sync summary, brain mirror reference, brain
  slug, or machine provenance to Board descriptions or steps.
- Never delete brain pages. When a Board task is archived or removed, update the
  brain task to `archived` and include:
  `No successor task needed: state mirrored from ICAIRE Board task <id>.`
- Before marking any brain task `done` or `archived`, include either
  `Next task: tasks/<slug>` or `No successor task needed: <reason>`.
- Preserve brain-only notes where possible. When updating task bodies, keep
  Board-generated sync text in a clearly marked section and do not overwrite
  teammate-authored context outside that section.

## Workflow

1. Confirm access:
   - Call ICAIRE MCP `me`; stop if no active ICAIRE member is resolved.
   - Call ICAIRE MCP `filing_rules` and follow the live task and initiative
     filing contract.
   - Call ICAIRE MCP `members/list` with active members.
   - Call Board MCP `initialize`, `tools/list`, and `board_snapshot`.
2. Gather recent teammate context:
   - Use available Codex thread tools to list recent threads.
   - Read only threads that are plausibly ICAIRE-related by title, summary, or
     recent status.
   - Extract confirmed progress, decisions, blockers, and candidate tasks.
   - Skip unrelated personal, commercial, family/admin, deal, client, or
     non-ICAIRE material silently.
3. Build the current state model:
   - Board initiatives, milestones, profiles, columns, groups, and tasks from
     `board_snapshot`.
   - Brain initiatives and tasks from ICAIRE MCP list/search/read/task tools.
   - Existing Board/brain links from stable IDs recorded in brain pages.
4. Propose brain writes:
   - Missing brain initiative pages for Board initiatives.
   - Missing brain task pages for Board tasks.
   - Brain task updates from Board state and richer recent context.
   - Archive updates for brain mirrors whose Board task was archived or removed.
5. Propose Board writes:
   - New Board tasks only when the brain task belongs to an existing Board
     initiative or is already linked to Board work.
   - Board task updates when new information changes execution state or makes
     title, steps, due date, assignee, milestone, completion, archive state, or
     scope materially clearer.
   - Prefer adding or updating steps for concrete next actions. Use description
     edits sparingly and only for durable task context that a teammate should
     see while doing the work.
   - Board initiative updates only for direct initiative metadata changes.
6. Review before applying:
   - Show exactly three user-facing headings, in this order:
     `Things that I suggest updating in the brain`,
     `Things that I suggest updating in the board`, and `Questions`.
   - Put every proposed change under the relevant heading as a bullet. Use
     nested bullets for initiative, milestone, task, step, and field detail
     without introducing more headings.
   - Put only user-actionable ambiguities, conflicts, approval decisions, or
     blockers under `Questions`. Do not expose internal categories such as
     conflicts, skipped items, approvals, or verification as separate headings.
   - If a section has no items, include one bullet saying `Nothing suggested.`
     or `No questions.` as appropriate.
   - Include Board IDs and brain slugs outside the proposed Board content as
     parenthetical review metadata only when needed to identify an item. These
     identifiers must not be written into Board fields.
   - Stop after the review unless the user confirms apply.
7. Apply and verify:
   - Use ICAIRE MCP writes for brain pages and tasks.
   - Use Board MCP writes for Board initiatives, tasks, and steps.
   - Verify each changed brain page with `read` or `tasks/list`.
   - Verify each changed Board item with `board_snapshot` or targeted Board MCP
     list/read calls.
   - Record notable sync conflicts, schema issues, or auth issues in `ops/`
     only when they are durable operational information.

## Output

For every user-facing run, return exactly these three headings in this order,
with bullet points under each and no other headings:

```text
## Things that I suggest updating in the brain

- <proposed brain update>

## Things that I suggest updating in the board

- <initiative title>
  - <milestone title or "No milestone">
    - Task: <task title>
      - Status: <old> -> <new>
      - Assignee: <old> -> <new>
      - Due date: <old> -> <new>
      - Description: <old concise summary> -> <new user-facing description>
      - Steps:
        - Add: <step text>
        - Complete: <step text>

## Questions

- <question that requires the user>
```

Do not include "brain sync", "brain mirror", mirror slugs, brain slugs, task
paths, sync timestamps, or other provenance inside the proposed field values.
Do not add headings for conflicts, skipped items, approvals, or verification.
Fold a conflict or missing approval into a direct question only when the user
must resolve it; otherwise keep internal reconciliation details out of the
review.

For review-only runs, use proposal bullets as shown. After an approved apply,
keep the same headings, prefix completed changes with `Applied:`, and keep any
unresolved user decisions under `Questions`.

## Guardrails

- Do not modify BigBrain core for ICAIRE-specific sync behavior.
- Do not create Board tasks for every brain task. The Board stays focused on
  active Board initiatives.
- Do not invent owners, due dates, status, initiative links, or Board placement.
- Do not assign brain tasks to inactive members or arbitrary `people/*` pages.
- Do not claim a sync succeeded until both brain and Board verification have
  run.
- Do not expose or store Board MCP tokens in brain pages, skill files, logs, or
  final reports.
- Do not use Board descriptions as timeline entries. Durable sync summaries and
  operational notes belong in brain `ops/` pages when they are worth keeping,
  not in Board task content.
