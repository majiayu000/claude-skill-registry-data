---
name: codex-slides-deck
description: Compatibility entry point for scenario-led creation, Design Files, brand systems, inspecting, revising, restyling, and exporting Codex Slides slide decks. Use when a user asks Codex to make a presentation, use project files, edit an existing deck, manage slide structure, apply brand or template rules, or export PDF/PPTX.
---

# Codex Slides Deck

The canonical `codex-slides` sibling skill owns the complete workflow. Use the
`codex_slides` MCP tools when available; otherwise run its self-contained CLI
at `../codex-slides/scripts/codex-slides.mjs`. Keep the live workspace available
in the in-editor Browser whenever visual review helps.

## Choose the flow

- Default to the live Browser workflow: open the Codex Slides home screen,
  submit the request there, then operate the created project through clarify,
  outline confirmation, style selection, rendering, and review. Keep the
  Browser visible throughout.
- If Browser UI submission fails, use `start_project` / CLI `start-project` to
  create the durable project shell, immediately open its returned URL, and
  continue in the UI.

- Use `list_scenarios` / CLI `scenarios` when a named workflow such as business
  report, document-to-deck, data insights, brand application, localization, or
  batch generation fits. Upload required slot files and pass `scenarioId`,
  `materialIds`, and `materialContexts` into creation.
- Only when the user explicitly requests an unattended/headless one-call
  result, call `create_deck` or CLI command `create`.
- For CLI automation or recovery, call `create_outline`, optionally
  `revise_outline` and `rank_inspiration`, then `render_deck`; the CLI commands
  are `outline`, `revise-outline`, `inspiration`, and `render`.
- For an existing deck, use `list_projects` or `get_project`, then choose the
  smallest mutation tool.

## Edit with the right tool

- Use `edit_deck` for natural-language add/rewrite/redraw/optimize requests.
- Use `manage_slide` for deterministic add, duplicate, delete, or transition.
- Use `regenerate_slide` for one slide.
- Use `restyle_deck` for a whole-deck template/style change.
- Use `upload_material` before creation, editing, or restyling when a local
  reference file matters.
- Use `upload_slide_image` for a finished PNG.
- Use `mark_edit_slide` when the user supplies an annotated PNG and wants a
  clean revised slide.
- Use `get_speaker_notes`, `update_speaker_notes`, and
  `generate_speaker_notes` (CLI `speaker-notes` with `get`, `set`, or
  `generate`) for presenter-only talk tracks. These notes persist per slide,
  appear in the speaker window, and are embedded in PPTX export.
- Use `list_design_files`, `read_design_file`, `write_design_file`, and
  `upload_design_file` for the project file workspace. Pass selected paths as
  `designFilePaths` when revising an outline or editing a deck.
- Use `get_brand_design_system` then `update_brand_design_system` for persistent
  project-wide brand/style rules. Redraw only when requested.
- Use `start_project_run` for navigation-independent chat, outline, or render
  work; retain the returned `runId` and track or cancel it explicitly.

## Show and verify

Open `open_codex_slides` / CLI `open` before a new creation and keep the live
workspace visible. After a programmatic mutation, navigate or reload its
resource link and inspect the changed slide or flow; do not make the user open
the URL manually.

Follow the exact `browserHandoff.url`; it can focus the changed slide, speaker
notes, export, versions, Design Files, brand system, Play menu, or durable run.

Use `export_deck` only after the requested visual result is ready. Browser-only
controls such as Play from current/beginning, the synchronized audience and
presenter windows, notes editing, slide navigation, and direct on-canvas marking
remain available through the live workspace.
