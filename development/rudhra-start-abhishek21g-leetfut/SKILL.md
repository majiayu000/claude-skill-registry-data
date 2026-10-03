---
name: rudhra-start
description: Start or bootstrap a project using Abhishek's full agent operating system. Use when the user says "rudhra start", "rudra start", "Rudhra start this project", "start this project as Rudhra", or asks to load the standard Claude/Codex template, context files, tool registry, skills, hooks, evals, and promotion loop into a new or existing project.
---

# Rudhra Start

Use this skill as the named startup ritual for Abhishek's projects.

## Steps

1. Identify the target project:
   - If the user gives a path, use that.
   - If the user gives a GitHub repo link, clone it first, then use the cloned folder.
   - If the user is already inside a project, use the current directory.
2. Ensure the master template is available:
   ```sh
   test -d ~/.agent-project-template/.git || gh repo clone Abhishek21g/agent-project-template ~/.agent-project-template
   git -C ~/.agent-project-template pull --ff-only
   ```
3. Bootstrap the project:
   ```sh
   ~/.agent-project-template/bootstrap-agent-project.sh <target-directory>
   ```
4. Fill `agent/PROJECT_CONTEXT.md` by interviewing the user for project name, goal, stack, commands, constraints, and definition of done.
5. Copy the install/dev/test/lint/build commands into `AGENTS.md` and `CLAUDE.md`.
6. End by telling the user exactly what was installed and what still needs real project detail.

## Rules

- Do not overwrite existing project files.
- Do not invent project commands; inspect package/config files or ask.
- For GitHub template creation from scratch, use:
  ```sh
  gh repo create <repo-name> --private --template Abhishek21g/agent-project-template --clone
  ```
- Log reusable lessons in `agent/PROMOTE.md` during later project work so `harvest-template-lessons` can improve the master template.
