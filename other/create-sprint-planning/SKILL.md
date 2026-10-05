---
name: create-sprint-planning
description: >
  Assemble refined, sized stories into an iteration and order them by dependency
  and value so the build phase starts with a clear, unblocked queue. Use when the
  user says "plan the sprint", "what should we pick up next", "fill the iteration",
  "sequence these stories", "order the backlog for the next sprint", or "assign
  these to the sprint". This is a light coordination step, not a
  document-producing one. Do NOT use to create or refine a story (that is
  elaboration-upsert-user-story), to write acceptance criteria (that is
  elaboration-upsert-user-story-acceptance-criteria), to take a single story through build (that
  is create-code-generation), or to report the next step on a single work item
  (that is run-sdlc).
---

# Create Sprint Planning

Owned by the **Scrum Master** persona (the create-sprint-planning step). Invoked as `/create-sprint-planning`.

Assemble the stories that are ready for build into an iteration and order them so the queue
is unblocked. This is a **light coordination step, not an artifact-producing one**: it
sequences existing work. The iteration plan is recorded as a sprint file under
`docs/discovery/sprints/` or as a section in `docs/discovery/backlog.md`.

A story is build-ready when it carries `status: refined` and a `points:` value in its
front-matter. If a candidate is missing either, route it back to the right step.

## Where work items live

All work items are local markdown files under `docs/discovery/`:
- Stories: `docs/discovery/stories/<epic-slug>/<story-slug>.md`
- Epics: `docs/discovery/epics/<epic-slug>.md`
- Backlog: `docs/discovery/backlog.md`

## Workflow

1. **Gather candidates.** Scan `docs/discovery/stories/` for items with `status: refined` and
   a `points:` value. Read their front-matter (key, points, epic, relates, priority).
2. **Check dependencies.** Read `relates:` edges to identify blockers. A story that depends on
   an unfinished item cannot start until that item ships.
3. **Order by value and dependency.** Place unblocked items first, ordered by priority then
   value (highest value, fewest dependencies first). Group by epic where it makes sense.
4. **Capacity check.** Sum points of the proposed sprint and compare to the team's velocity
   (ask if unknown). Do not overload.
5. **Present the plan.** Show the ordered list with key, title, points, and any dependency
   note. Get confirmation.
6. **Record.** Update `status: in-progress` on selected items. Optionally create a sprint file
   at `docs/discovery/sprints/<sprint-name>.md` listing the selected items in order. Update
   `docs/discovery/backlog.md` to reflect the sprint assignment.

## Guardrails

- **Do not create or refine stories here.** Route unready items to the right skill.
- **Respect dependencies.** Do not sequence a blocked story before its blocker.
- **Confirm before writing.** Present the plan, then write on approval.
- **No em-dashes.**

## Next steps

- `/create-code-generation` (Developer) - take the first story in the sprint through build.
- `/elaboration-upsert-user-story-acceptance-criteria` (PM/QA) - sharpen a story that lacks testable ACs.
- `/elaboration-upsert-user-story` (PM) - create a missing story surfaced during planning.
