---
name: project-directories
type: reference
description: Reference for the user's local project directory layout. Read when locating repositories, workspaces, or ad-hoc project directories.
---

## Layout

- `~/Dev/src/<host>/<repo>`: Cloned source repositories.
  - Example: `~/Dev/src/github.com/sirn/example` corresponds to `github.com/sirn/example`.
- `~/Dev/workspace/<name>/<repo>`: Named workspaces containing one or more repositories.
  - Example: `~/Dev/workspace/foo-implementation/example` is the `example` repo inside the `foo-implementation` workspace.
- `~/Dev/adhoc/<name>`: Ad-hoc scripts, experiments, and one-off projects.

## Policy

- Stay inside the current project or workspace unless the user explicitly asks otherwise.
- In `~/Dev/workspace/<name>/...`, treat `~/Dev/workspace/<name>` as the workspace boundary.
- If a required file is outside the current project/workspace, ask before accessing it.
- Use the project `tmp/` directory for temporary files when possible.
