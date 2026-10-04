---
name: readme
description: >
  How to write and update frename's README.md and version.md entries for users. Use whenever a
  change is visible to the user, when editing README.md, or when reviewing user-facing text.
---

# README for users

The README is for video editors deciding whether to use frename and learning how. Not for developers.

## Rules

- Plain language, short sentences, second person ("Press `[` to mark…"). No crate names, no
  internal types, no implementation details. Build instructions stay in one short section at the end.
- Organised by what the editor does (open a folder, tag, mark moments, prepare for Premiere),
  not by code modules.
- Every shortcut the app has is in the shortcut tables; nothing is listed that the app lacks.
- A new feature gets one or two sentences in the section where an editor would look for it.
  A bigger feature may get its own short section with at most one screenshot.
- Keep it compact: when adding, check whether an older paragraph can be shortened or removed.
  Target: README stays under ~250 lines.
- Technical details that are still worth keeping go to `docs/`.
- English only (see `AGENTS.md`).

## version.md

Follow `.claude/skills/create-release-version/SKILL.md`. One line per user-visible change, written
as what the user can now do or what now behaves differently.
