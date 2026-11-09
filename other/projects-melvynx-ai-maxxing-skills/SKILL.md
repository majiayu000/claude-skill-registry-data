---
name: projects
description: Load, list or archive a project of the user's brain, and find where a piece of work belongs. Use when the user says "load project X", "charge le projet X", "on bosse sur X", "where is X", "list my projects" or "archive X".
argument-hint: "<load|list|archive> <name>"
metadata:
  internal: true
---

Work with the projects of the user's brain, following the Projects and Hygiene sections of its `AGENTS.md`. The brain is the folder named in the `## Brain` section of `~/.claude/CLAUDE.md` (default `~/brain`). Talk to the user in their language, without jargon.

- `load <name>`: find the folder (search `projects/**/About.md` by folder name and title, ask in one line when two match), read `About.md` and `Roadmap.md` first, then only the files the task needs. Say in two lines where the project stands and the next step. Update `About.md` and `updated:` when something important changes.
- `list [status]`: read the status of every `projects/**/About.md` and show name, status, updated and a one-line summary, grouped by hub. Flag projects not updated for 60 days or more, and point to `/cleanup` to tidy them.
- `archive <name>`: fold the final outcome into `About.md`, set `status: done`, trash scratch files, keep deliverables, move the folder to `archives/<slug>/` (keep it intact), fix the paths that pointed to it, and commit `projects: archive <name>`.
- A new project goes through the `create-project` skill.
