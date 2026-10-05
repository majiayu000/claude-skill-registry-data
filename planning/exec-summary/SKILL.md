---
name: exec-summary
description: Produce a short executive summary for the current rolling-wave project. Use when the user wants a concise status update, investor/team-friendly summary, leadership summary, project progress snapshot, or TL;DR of completed slices, the current slice plan, and upcoming slices.
---

# Exec Summary

Create a short executive summary of the current rolling-wave project.

## Core Invariants

- Work under `docs/rolling-wave/{project}/`.
- Read project-level state from `project.md`; read slices from `slices/NNN-slug.md`.
- Use slice statuses: `pending`, `ready`, `in progress`, `ready for review`, `in review`, `done`.
- Treat the roadmap in `project.md` as the planned sequence.
- This is read-only. Do not edit project or slice files.
- Keep output concise and executive-friendly. Do not include planning-process caveats, file visibility notes, or test warnings unless directly relevant to the status.

## Workflow

1. Resolve the project.
   - If the user names a project, use `docs/rolling-wave/{project}/`.
   - If only one project exists under `docs/rolling-wave/`, use it.
   - If multiple projects exist and no project is named, ask which project to summarize.
   - If no rolling-wave project exists, say so plainly.

2. Read status.
   - Read `project.md`.
   - Read slice files under `slices/`.
   - If a slice references a child rolling-wave project, read the child `project.md` only enough to summarize child status and current child slice.
   - Prefer slice file frontmatter for status when present.
   - Use the roadmap table in `project.md` for ordering and one-line purpose.

3. Identify the current slice.
   - Prefer a slice with status `in progress`.
   - Else use `in review`.
   - Else use `ready for review`.
   - Else use `ready`.
   - Else use the first non-`done` roadmap slice.
   - If no unfinished slices remain, say the roadmap appears complete.

4. Summarize.
   - Slices overview: use a markdown table with `status` and `name` columns in roadmap order.
     - Show each slice's exact status; do not reduce status to completed or incomplete.
     - For child-project-backed slices, append `-> {child-project}: {child-status}` or a similarly terse child-project marker to the `name` cell.
     - Include slice id/name and a short outcome- or purpose-oriented phrase in the `name` cell.
   - Current slice TL;DR: summarize the current slice plan in one to three bullets from its purpose, behavior, acceptance criteria, expected intermediate state, risks, and implementation notes.
   - Upcoming: include upcoming slices in the same table rather than a separate plain bullet list.
   - Include material project-level risks or review notes only if they affect leadership understanding of progress or next steps.

## Output

Use this shape:

```markdown
- Slices:
  
  | status | name |
  | --- | --- |
  | done | 001-...: ... |
  | in progress | 002-...: ... |
  | pending | 003-...: ... |
- Current slice:
  - ...
```

Keep the whole answer short. If there is nothing in a section, write `none` for that section.
