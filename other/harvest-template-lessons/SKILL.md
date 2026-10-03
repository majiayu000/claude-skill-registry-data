---
name: harvest-template-lessons
description: Pull reusable lessons from agent/PROMOTE.md across all projects registered in PROJECTS.md and propose them as additions to this master template.
---

# Harvest Template Lessons (Codex)

Mirrors the Claude version. Run from within the master template directory:

1. Read `PROJECTS.md` for registered project paths.
2. For each existing project, read `agent/PROMOTE.md`, collect entries newer than that project's "Last Harvested" date.
3. Group by target file (CLAUDE.md / AGENTS.md / TOOL_REGISTRY.md / a skill / a hook / WORKFLOW.md / EVALS.md), merge duplicates across projects.
4. Present proposed changes — do not apply automatically.
5. On approval, edit the template files, then update `PROJECTS.md`'s "Last Harvested" column for the projects you pulled from.
6. Never edit the source project's `PROMOTE.md`.
