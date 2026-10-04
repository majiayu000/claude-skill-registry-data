---
name: icaire-whats-next
version: 1.0.0
description: |
  Provide a concise snapshot of what should be done next from in-progress and
  open ICAIRE task pages exposed through the ICAIRE Cortex MCP task tools. Use when the user
  asks what's next, wants a short task snapshot, or wants to decide what to
  work on before optionally fanning out Codex threads with full handoff prompts.
triggers:
  - "what's next"
  - "what is next"
  - "what should I do next"
  - "next ICAIRE tasks"
  - "snapshot of what needs to be done"
  - "what needs to be done next"
tools:
  - mcp
mutating: false
---

# ICAIRE: What's Next

Use this skill when the user wants a short, decision-ready snapshot of active
and ready ICAIRE task pages. ICAIRE tasks are page-backed records under
`tasks/*.md`; do not read or reconstruct old `ops/tasks.md` task lists.

This skill is related to `icaire-fanout-tasks`, but it does not create
handoff threads by default. It summarizes the next work first, then offers to
fan out Codex threads if the user wants to start the work.

If the user answers questions from the input-needed section or provides
additional task context after a snapshot, treat that as task-enrichment input.
Do not start executing the task in the same thread unless the user explicitly
asks you to work on it here. Working on tasks in the same thread where
`What's Next` ran is an anti-pattern by default; enrich or clarify the task
record, then wait for an explicit fanout or execution request.

## Workflow

Use the ICAIRE Cortex MCP task endpoint as the source of truth:

1. Call `tasks/list` twice by default, scoped to the authenticated member:
   first with `status: "in_progress", assignee: "me"`, then with
   `status: "open", assignee: "me"`.
2. If `tasks/list` is not visible, use targeted Codex tool discovery for the
   ICAIRE `tasks/list` tool before falling back to runtime or code inspection.
3. Resolve assignee scope before listing tasks:
   - For a generic request such as "what's next", and for "my tasks" or
     "assigned to me", pass `assignee: "me"`.
   - For "for people/name" or "assigned to people/name", pass that assignee
     slug.
   - Omit `assignee` only when the user explicitly asks for all-team,
     everyone's, or unassigned-across-the-team work.
   - For a named priority such as `p0`, `p1`, `p2`, or `p3`, pass `priority`.
   - For a named status, pass that `status`; otherwise use both default calls.
4. Use the returned task title, body, priority, assignees, source, and slug to
   identify the most useful next work. Use slugs internally for lookup and
   continuity, but do not normally show them in the snapshot output.
5. Within the resolved assignee scope, prefer `in_progress` tasks first, then
   high-priority `open` tasks. Keep `waiting` tasks separate unless the user
   asks for them.
6. Treat `readiness` and `execution_mode` as useful hints, then read the task
   body. If `## Open Questions` contains substantive questions, put the task in
   the input-needed section even when frontmatter says `readiness: "ready"`,
   unless the task is clearly an interactive guided session whose purpose is to
   answer those questions with the user.
7. Classify the remaining tasks with `readiness` and `execution_mode`:
   - `readiness: "ready"` plus `execution_mode: "agent"` means the task can
     appear in the normal next-work numbered list and can be fanned out as an
     autonomous prompt.
   - `execution_mode: "user"` means the user must personally do the work, even
     if the task is otherwise ready. Keep these in a separate user-action
     section.
   - `execution_mode: "interactive"` means an agent can help only by walking
     the user through input, review, or decisions. These still belong in the
     main next-work numbered list and can be fanned out as guided step-by-step
     prompts.
   - `readiness: "underspecified"` means the task needs user input before it
     should be fanned out or treated as an executable handoff.

Respond in chat with the snapshot. Do not write the result to a file, do not
return only a file link, and do not make the user open an artifact to see what
is next.

## Output Requirements

Default output is capped at 8 numbered items. Keep the snapshot short:

- Show a `What's Next` section first.
- This section should contain only tasks with `readiness: "ready"` and
  `execution_mode: "agent"` or `execution_mode: "interactive"` after the open
  questions override above.
- Format ready tasks as a numbered list, not bullets.
- Each numbered item should lead with a human-readable task title or action, not the
  task slug. Include priority only when it helps ranking or urgency.
- Do not include task slugs in the `What's Next` numbered list unless the user
  explicitly asks for paths/slugs or two tasks would otherwise be ambiguous.
- Do not format the numbered list as copyable prompt blocks.
- Do not include boilerplate about reading files, preserving changes,
  verification, or commits.
- Only when there are matching `execution_mode: "user"` tasks, append exactly:
  `There are a few things I can't physically help with:`
- Under that line, show a numbered list of user-only tasks with the concrete
  real-world user action required.
- If there are no matching user-only tasks, omit this heading entirely and do
  not mention that no such tasks were found.
- Only when there are matching `readiness: "underspecified"` tasks, or tasks
  whose body contains substantive open questions, append
  exactly:
  `I also need your input on a few tasks:`
- Under that line, show a numbered list of input-needed tasks. For each task,
  include indented bullet questions or the missing context required.
- Make clear that answers to these questions are for clarifying or enriching
  the task, not for starting execution in this `What's Next` thread.
- If there are no matching input-needed tasks, omit the input-needed heading
  entirely and do not mention that no such tasks were found.
- Name input-needed tasks by human-readable title or action, not slug, unless
  the user explicitly asks for paths/slugs.
- Prefer questions from the task page's `## Open Questions` section. If that
  section is absent or incomplete, add a small number of inferred blocking
  questions on the spot.
- Do not include input-needed or user-only tasks in the main `What's Next`
  numbered list.
- End by asking whether the user wants Codex threads launched with handoff
  prompts for the ready agent-executable or interactive tasks.

If the user agrees to launch threads or receive prompts, immediately use the
ICAIRE Fanout Tasks workflow on the same task scope and filters, preserving
the resolved assignee filter. Do not ask the user to repeat the scope.

If no actionable ICAIRE task pages match the requested filters, say that
directly and offer to run ICAIRE: Roadmap Tasks only if the user wants new
tasks proposed from current brain evidence.

## Quality Rules

- Treat MCP task data as authoritative for task status and assignees.
- Never issue an unscoped `tasks/list` call by default. Omit `assignee` only
  when the user explicitly requests an all-team view.
- Do not use local `TODO.md` discovery for this skill.
- Do not mutate tasks while producing the snapshot.
- If the user follows up with answers or additional context, use that context
  to enrich the relevant task record when an update workflow is available; do
  not treat the answer as permission to start working on the task.
- Do not create summaries for tasks with `status: "done"` or
  `status: "archived"` unless the user explicitly asks for those statuses.
- Do not promote an underspecified task to the ready list just because it sounds
  important.
- Keep each numbered item scoped to one task; put multi-task or ambiguous records in
  the input-needed list rather than guessing hidden subtasks.
