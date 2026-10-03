---
name: new-project
description: Scaffold the full agent-project template (AGENTS.md, CLAUDE.md, agent/ context files, skills, hooks) into a new or existing project directory. Use when the user says things like "start a new project", "set up agent files for this repo", "bootstrap this project", or "scaffold this the way we always do".
---

# New Project Scaffold

This skill installs Abhishek's standard agent-project template into the current working directory, so every new project starts with the same durable scaffolding instead of being rebuilt from scratch.

## Steps

1. Confirm the target directory with the user if it's ambiguous (current directory vs. a path they named).
2. Run the bootstrap script, pointing at the target directory:
   ```sh
   ~/.agent-project-template/bootstrap-agent-project.sh <target-directory>
   ```
   This copies (without overwriting anything that already exists): `AGENTS.md`, `CLAUDE.md`, `agent/PROJECT_CONTEXT.md`, `agent/TOOL_REGISTRY.md`, `agent/WORKFLOW.md`, `agent/EVALS.md`, `agent/AUTO_UPDATE.md`, `.claude/skills/`, `.codex/skills/`, and `hooks/`.
3. Immediately after scaffolding, interview the user briefly to fill in `agent/PROJECT_CONTEXT.md` for real. Ask at minimum: project name, one-sentence goal, tech stack, and the install/dev/test/lint/build commands. Write the answers directly into the file.
4. Fill in the same install/dev/test/lint/build commands into the "Commands" sections of the newly-copied `AGENTS.md` and `CLAUDE.md`.
5. Tell the user what was created and what's still a placeholder.

## Notes

- This only ever copies files that don't already exist (`copy_if_missing` behavior), so it is safe to run on a partially-set-up project without clobbering existing work.
- If `~/.agent-project-template` is missing, clone it first:
  ```sh
  gh repo clone Abhishek21g/agent-project-template ~/.agent-project-template
  ```
- Global standing preferences belong in `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`, not here.
