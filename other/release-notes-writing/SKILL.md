---
name: release-notes-writing
category: pm
description: Use when the stakeholder asks for release notes or a changelog - group done/released work into Added, Changed, Deprecated, Removed, Fixed and Security, in outcome language, with task references
source: olivierlacan/keep-a-changelog 1.1.0 (MIT), phuryn/pm-skills release-notes (MIT), adapted
---
# Release Notes Writing

## Overview

Release notes tell users what changed for THEM, not what the team did. The failure mode is internal jargon and a flat list of task titles that mean nothing to a user. Changelogs are for humans, not machines — don't dump git log or task titles verbatim.

**Core principle:** User-visible outcomes, grouped by Keep a Changelog's categories, in plain language.

## Where the material comes from

- `list_board_tasks` filtered to `done`/`released` for the period asked about.
- `get_task_pull_request` on each one for detail (what actually shipped, not just the title).
- TaskTrooper has no epic/parent task — deliver the notes in chat, or as a document (`add_task_document`) on whichever task the stakeholder names, never a phantom "release epic".
- The system's own batch release cut auto-generates `### Features` / `### Fixes` sections from `KEY Title`. Writing implementation-task-spec titles as action + user-visible object (not an internal component name) makes that auto-generated text usable on its own — keep that in mind even when you're not the one writing this document.

## Structure

- **Added** — new user-visible capability.
- **Changed** — behavior changes users must know about (a moved button, a changed default).
- **Deprecated** — soon-to-be-removed, still working.
- **Removed** — gone.
- **Fixed** — defects resolved, described by the symptom the user saw, not the internal cause.
- **Security** — a vulnerability closed; state impact, not exploit detail.
- **Action required** — anything in Changed/Removed that is breaking: what the user must do and by when.

Write user-facing language, no internal jargon. Put task keys in parentheses for traceability.

## Worked Example

```markdown
## Release 2026-07-16

### Added
- Export a project's tasks to CSV from the board (LLM-142).

### Fixed
- Deleting a task with subtasks no longer shows an error (LLM-150).

### Changed
- Task titles are now capped at 200 characters (LLM-138).

### Action required
- None this release.
```

Contrast the bad version: *"LLM-142 TaskExporter service; LLM-150 fix nil deref in cascade."* — accurate to the team, meaningless to a user.

## Common Mistakes

- Internal jargon ("nil deref", "N+1").
- Task titles pasted verbatim instead of user outcomes.
- Omitting "Changed" → users surprised by a moved feature.
- A breaking change with no "Action required" line.
- Attaching the document to an invented "release epic" task.

## Red Flags

- A note a user couldn't understand.
- No task key for traceability.
- A Removed/Changed entry with nothing telling the user what to do about it.
