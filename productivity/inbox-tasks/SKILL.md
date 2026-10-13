---
name: inbox-tasks
description: "Use when a task needs a tracking file and you must decide where it lives: check whether its subject belongs to a project first, else file it in {agency-root}/tasks/inbox/. On-demand; moved out of CLAUDE.md."
---
# Inbox task management (ownerless tasks only)

Before filing any task tracker, check `{agency-root}/memory/medium-term.md`: does the task's SUBJECT match an existing project? If yes, its tracking file goes in that project's `memory/tasks/` (see `{agency-root}/skills/pd-spawn/SKILL.md` for the delegation-file convention when a PD is spawned), even when the session that filed it has no project of its own. Only genuinely ownerless tasks go to `{agency-root}/tasks/inbox/{ongoing|completed|archived}/{slug}/TASK.md`; format and lifecycle: `{agency-root}/tasks/inbox/index.md`. A task's file follows what it is ABOUT, never the session that filed it.
