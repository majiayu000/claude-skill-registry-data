---
name: codex-slides-known-errors
description: Diagnose and recover from Codex Slides plugin, MCP, Browser handoff, local runtime, durable run, project resume, rendering, Design Files, export, and version-contract failures. Use when a tool fails, a run stalls, a project appears stale, or Codex and the Browser disagree.
---

# Codex Slides Known Errors

Classify the failure before retrying. Preserve the same project id and run id;
do not recreate a deck merely because a Browser tab closed or a wait timed out.

## Runtime and installation

- **Plugin version contract fails:** `.codex-plugin/plugin.json` must start with
  the exact root `package.json` version plus `+codex.`. The desktop package must
  use the same product version.
- **App is unreachable:** inspect `CODEX_SLIDES_URL` and `CODEX_SLIDES_LOG`.
  The local MCP launcher may need to prepare dependencies or a standalone build.
- **Installed skill or tool inventory looks stale:** reinstall/upgrade the
  plugin and start a new Codex task so the versioned plugin cache is refreshed.

## Durable runs

- **Another run is active:** inspect it with `get_project_run`. Wait, cancel it
  explicitly, or allow a Deck Agent request to remain in the visible queue.
- **Wait timed out:** the run was not cancelled. Continue with
  `wait_project_run` or reopen its `browserHandoff`.
- **Run id is missing after completion:** this indicates an old runtime without
  terminal `runHistory`; refresh the plugin/runtime before retrying the task.
- **Run is stopping:** do not start a conflicting render. Poll until it becomes
  `cancelled`, then continue.

## Browser handoff and project resume

- Use the exact returned `browserHandoff.url`; do not reconstruct a project URL.
- Keep all focus parameters: `slide`, `panel`, `version`, `mode`, `checkpoint`,
  `conversation`, and `run`.
- A clarify/research project may route through `/?resume=<id>`. The continuation
  query must survive that redirect.
- Presenter mode needs a user gesture for its second window. A presenter deep
  link opens the Play menu at the correct slide instead of bypassing popup
  protection.

## Rendering and project state

- A partially rendered or paused deck is resumable. Read the project and start
  a durable `render` run for the existing project.
- If Codex state and Browser state differ, read `/runs`/`get_project` as the
  canonical snapshot, then reload the same Browser handoff.
- Do not report success for slides whose status is `error` or whose persisted
  image cannot be loaded.

## Design Files and export

- Resolve Design Files through `list_design_files`; never guess an absolute path.
- Keep project files distinct from staged materials.
- Export the current or explicitly selected immutable version only after visual
  verification. Speaker notes are off-canvas but must remain present in PPTX.
