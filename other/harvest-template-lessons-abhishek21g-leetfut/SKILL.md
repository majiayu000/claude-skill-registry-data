---
name: harvest-template-lessons
description: Pull reusable lessons from agent/PROMOTE.md across all projects registered in PROJECTS.md and propose them as additions to this master template (CLAUDE.md, AGENTS.md, TOOL_REGISTRY.md, skills). Use when the user says "harvest lessons", "update the template from my projects", "sync learnings back to the template", or similar.
---

# Harvest Template Lessons

This is the return half of the template loop: template → project (via bootstrap) → back into template (via this skill). Run this from within the master template directory (this repo).

## Steps

1. Read `PROJECTS.md` to get the list of registered project paths.
2. For each project path that still exists on disk:
   - Read `<project>/agent/PROMOTE.md`.
   - Skip rows already covered by "Last Harvested" in `PROJECTS.md` for that project (compare log entry dates against the last-harvested date).
   - Collect any new, real (non-example) rows.
3. If a project path no longer exists, note it and skip — don't fail the whole run.
4. Group the collected lessons by target (CLAUDE.md / AGENTS.md / a skill / a hook / TOOL_REGISTRY.md / WORKFLOW.md / EVALS.md). Where two projects logged near-identical lessons, merge them into one proposed change instead of duplicating.
5. Present the proposed changes to the user as a clear diff-style summary, grouped by target file — do not apply anything yet.
6. Wait for approval. Apply only what's approved, using the Edit tool on the actual template files in this repo.
7. After applying, update `PROJECTS.md`'s "Last Harvested" column for each project you pulled from to today's date, so the same lessons aren't re-proposed next time.
8. Do not clear or edit the source project's `agent/PROMOTE.md` — leave it as the project's own history. The "Last Harvested" date in `PROJECTS.md` is what prevents re-proposing the same rows.

## Guardrails

- Never auto-apply anything to CLAUDE.md/AGENTS.md/TOOL_REGISTRY.md without explicit approval in this run — same rule as the weekly external-tool check.
- Discard anything that's clearly project-specific despite being logged (use judgment — if in doubt, ask rather than silently dropping or silently applying).
- If a proposed lesson would make CLAUDE.md/AGENTS.md longer than ~200 lines, flag that explicitly and suggest what to prune, rather than just adding on top.
