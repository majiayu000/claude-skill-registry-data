---
name: project-local-skill-generator
description: Generate thin project-local .codex/skills from a scaffolded repo's actual harness artifacts. Use after scaffold or harness setup when a repo should have local Codex workflows for feature state, session handoff, Definition of Done, runtime debugging, UI work, or review protocol without copying plugin skills.
---

# Project Local Skill Generator

## Purpose

Create short repo-specific `.codex/skills` that teach Codex how to operate in this project day to day, while keeping reusable harness authoring skills in the plugin.

## Inspect First

- existing `.codex/skills`
- `AGENTS.md`, nested `AGENTS.md`, docs, scripts, feature state, progress, decisions, runtime docs, UI docs, review docs, and validation commands
- whether each proposed local skill has real repo artifacts to link to

## Procedure

1. Suggest local skills from evidence.
   - Use `scripts/suggest_project_local_skills.py` from this plugin.
   - Recommend only skills backed by existing repo files.
   - Classify suggestions as `daily`, `on_demand`, or `library` so high-frequency workflows stay easy to find without bloating root instructions.
   - Skip skills whose artifacts are missing instead of inventing local policy.

2. Generate thin local wrappers.
   - Use `scripts/generate_project_local_skills.py`.
   - Write to `.codex/skills/<local-skill-name>/SKILL.md`.
   - Default local skills are `project-feature-workflow`, `project-session-handoff`, `project-definition-of-done`, `project-runtime-debugging`, `project-ui-workflow`, and `project-review-protocol`.
   - Stack-specific local skills may include `project-bun-workflow`, `project-frontend-workflow`, `project-browser-qa`, `project-api-workflow`, `project-data-workflow`, `project-docker-runtime`, and `project-decision-log` when matching artifacts exist.
   - Trajectory local skills may include `project-trajectory-supervisor` when task traces, trajectory policy, or `scripts/check-trajectory-risk` exists.

3. Preserve local edits.
   - Inspect existing local skill files before generation.
   - Do not overwrite existing local skills unless the task explicitly requests refresh or overwrite behavior.
   - Prefer adding missing skills over regenerating edited ones.

4. Keep plugin and project roles separate.
   - Local skills name exact repo files and commands.
   - Local skills route heavy harness authoring back to plugin skills.
   - Do not copy full plugin skills into `.codex/skills`.

5. Validate local skills.
   - Use `scripts/check_project_local_skills.py`.
   - Confirm links point to real files and commands.
   - Confirm local skill bodies are short and repo-specific.
   - Use `$subagent-review-orchestrator` separately for `.codex/agents` generation; do not mix local skills and subagent files.

## Validation

- Run `scripts/suggest_project_local_skills.py <repo> --json` before generating.
- Run `scripts/generate_project_local_skills.py <repo>` when generation is requested.
- Run `scripts/check_project_local_skills.py <repo>` after generation.
- Confirm existing local skills were preserved unless overwrite was explicitly requested.

## Completion Criteria

- The repo has only useful project-local skills backed by actual artifacts.
- Generated skills point to repo-local docs/scripts and avoid generic plugin-scale instructions.
- Reusable harness logic remains in the plugin.
