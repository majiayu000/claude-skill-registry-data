---
name: codex-slides
description: Create, research, revise, restyle, present, inspect, and export Codex Slides slide decks from Codex, including scenario workflows, project Design Files, and always-on brand design systems. Use when the user asks for a presentation, PPT/PPTX, slide deck, research brief converted into slides, an existing deck edit, a marked-up slide revision, brand/style controls, project files, or to open and operate Codex Slides in the Codex in-editor Browser.
---

# Codex Slides

Run Codex Slides as an interactive product inside Codex. The live Browser
workspace is the primary experience; MCP and the bundled CLI are transports
for opening the workspace and performing deterministic operations, not a reason
to hide the presentation workflow in a long-running Codex turn.

## Browser-first default

For every new deck request, unless the user explicitly asks for a headless,
unattended, one-call, or CLI-only run:

1. Call `open_codex_slides` / CLI `open` **without** a project id, immediately
   navigate the returned URL in Codex's in-editor Browser, and verify that the
   Codex Slides home/create screen is visible.
2. Keep the Browser open. Enter the user's request in the home composer, attach
   or assign source files in the UI, and submit it there. This creates a durable
   project before clarification starts. If UI submission is not reliable, use
   `start_project` / CLI `start-project` only as a deterministic fallback, then
   navigate its returned project URL immediately.
3. Continue in the live project workspace. Let Codex Slides show and own each
   checkpoint: requirements/clarifying questions, research progress, editable
   outline confirmation, visual-inspiration or style selection, and rendering.
   Answer or manipulate each step in the Browser; when a choice materially
   changes the result and the user's prompt does not resolve it, leave that
   checkpoint visible and ask the user.
4. During research and rendering, keep the project workspace visible so the
   user sees progress and can steer. Do not leave Codex showing only a generic
   "working" message while a hidden tool completes the whole deck.
5. After rendering, inspect the deck in the same Browser workspace. Use its
   agent composer, slide controls, mark mode, Play, Design Files, and brand
   system for follow-up work. Export only after visual review.

Do not call `deep_research`, `create_outline`, `rank_inspiration`,
`render_deck`, or `create_deck` before opening the Browser for a normal deck
request. Do not default to `create_deck`; it is the explicit unattended fast
path. A user's request such as "make a six-slide deck and show me" still uses
the Browser-first guided flow unless they specifically ask Codex to finish it
in the background without checkpoints.

## Choose a transport

1. Use the `codex_slides` MCP tools when they are exposed in the current
   session and a structured tool call is convenient.
2. Otherwise run `scripts/codex-slides.mjs`. Pass inputs with `--json`,
   `--input-file`, or command flags. It installs, builds, and starts the local
   app when necessary.
3. Do not treat MCP as a prerequisite. Both transports use the same API and
   return the same project URLs.

Every Browser-capable response includes a `browserHandoff`. Follow its exact
URL instead of rebuilding one, because it can focus a slide, panel, version,
mode, checkpoint, conversation, or durable run.

Run this to discover the portable command surface:

```bash
node <skill-dir>/scripts/codex-slides.mjs capabilities
```

Read [references/COMMANDS.md](references/COMMANDS.md) when selecting commands,
constructing JSON inputs, or mapping a CLI command to an MCP tool.
Read [references/CAPABILITY_MATRIX.md](references/CAPABILITY_MATRIX.md) when
auditing a newly added product feature or changing the Browser/CLI/MCP contract.

## Build a deck

- Discover workflow presets with `scenarios` / `list_scenarios`. A scenario owns
  its default page count, aspect, research behavior, model instruction, and
  required/optional source slots. Pass its `scenarioId` to `onboard`,
  `research`, `create`, or `outline`; do not re-create the scenario prompt by
  hand.
- Upload slot files with `upload-material` / `upload_material`, then pass both
  `materialIds` and `materialContexts` (`id`, `name`, `role`). Required slots
  must be satisfied before creation. Keep content sources, datasets, brand
  assets, templates, and visual references in their declared roles.
- Use the Browser-first guided flow above by default. The Browser UI drives the
  staged `clarify -> outline -> inspire -> deck` state and persists the project
  before expensive work starts.
- Search the shared community style library with `templates` / `list_templates`
  (`query` and `communityGroup`), then use `inspiration` / `rank_inspiration`
  when the topic and outline should semantically rank those directions. A chosen
  community style is both prompt context and the first visual reference image.
- Use `start-project` / `start_project` only when Codex needs a deterministic
  fallback to create the same durable project shell before returning to the UI.
- Use `create` / `create_deck` only when the user explicitly requests an
  unattended one-call result or the current Codex surface has no Browser.
- The lower-level `onboard`, `research`, `outline`, `revise-outline`,
  `inspiration`, and `render` operations are for CLI automation, recovery, and
  deterministic mutations. Keep the corresponding Browser project open when
  using them interactively.
- For navigation-independent Deck Agent, outline, or render work, use
  `start_project_run` / CLI `run-start`. Retain its `runId`; use
  `get_project_run`, `wait_project_run`, or `cancel_project_run` (CLI
  `run-status`, `run-wait`, `run-cancel`) after navigation or reconnect.
- Preserve the Markdown research brief and its source links. Do not call a
  brief source-backed when it contains no source links.
- Upload logos, screenshots, PDFs, or other references with `upload-material`
  before creation, editing, or restyling, then pass the returned material ids.

## Operate Design Files

- Use `design-files` / `list_design_files` to inspect the generated and uploaded
  project file inventory. Use `read-design-file` / `read_design_file` for text
  and the returned Browser deep link for visual or binary files.
- In the Browser, every selected Design File exposes its absolute local path for
  copying and a direct download action. CLI/MCP file-list responses include the
  same `absolutePath` and a `downloadUrl` for automation.
- Use `write-design-file` / `write_design_file` only when the user asked to
  replace an existing editable file. Use `upload-design-file` /
  `upload_design_file` to add a local file to the project workspace.
- When an outline or deck edit should use project files as evidence, pass their
  returned paths as `designFilePaths` to `revise-outline` / `revise_outline` or
  `edit` / `edit_deck`. This is the Codex equivalent of selecting a Design File
  with `@` in the Browser composer.

## Reuse project templates

- Use `project-templates`, action `list`, or `list_project_templates` before
  creating with a reusable project template. Pass the returned id as
  `projectTemplateId`; do not substitute a built-in `template` id.
- Use `project-templates`, action `save`, or `save_project_as_template` only when
  the user wants to preserve an existing project's visual system. The snapshot
  includes its format, base template/style, brand system, brand assets, and up
  to six visual references, but not the source project's deck content.
- Deleting a saved template does not mutate projects already created from it,
  because assets and brand rules are copied into each new project.

## Maintain the brand design system

- Call `get-brand-system` / `get_brand_design_system` before changing an
  existing project's always-on rules. It returns normalized brand identity,
  style, colors, typography, effects, spacing, radii, and brand assets.
- Stage new logos or product images with `upload-material`, then merge a partial
  update with `set-brand-system` / `update_brand_design_system`. Brand updates
  preserve untouched sections. Redrawing existing slides is explicit; default
  to saving without redraw unless the user requested application to the current
  deck.
- A brand design system is project-wide context for outline generation, slide
  generation, chat planning, and later edits. Do not replace it with a one-off
  free-text style when the project already has one.

## Edit an existing deck

- Inspect with `list` and `get` before changing an unknown project.
- Use `edit` for natural-language add/rewrite/redraw/optimize requests.
- Use `slide` for deterministic add, duplicate, move, delete, or transition changes.
- Use `regenerate` for one slide and `restyle` for the whole deck.
- Use `upload-slide` for a finished local PNG.
- Use `mark-edit` when the user supplies an annotated PNG and wants a clean
  regenerated slide.
- Use `speaker-notes` / `get_speaker_notes` to inspect the talk track,
  `action:set` / `update_speaker_notes` to write or clear exact notes, and
  `action:generate` / `generate_speaker_notes` to ask the project's selected
  agent for one slide or a coherent full-deck talk track. Notes stay off-canvas,
  appear in presenter mode, and export as native PowerPoint speaker notes.
- In the Browser, use the project header's Version entry to inspect immutable
  deck snapshots and their originating prompts. Each version owns its slide
  images, transitions, and notes, so preview, Play, and PDF/PPTX export use that
  exact snapshot. Restoring never overwrites history; it creates a new current
  version linked to the selected source version. Every AI command or manual
  action that changes a rendered deck must create a version; one multi-step AI
  command may update one grouped version. Conversation-only turns, navigation,
  and saves whose deck content is unchanged do not create empty versions.

Keep durable edits scoped to the project the user named. If no project was
named and multiple projects exist, inspect the recent list before choosing.

## Route to focused workflow skills

- Use the `codex-slides-structured-intake` sibling for ambiguous or
  scenario-led new-deck requirements.
- Use the `codex-slides-verification` sibling after creation, rendering,
  editing, restyling, version restore, speaker-note changes, or export.
- Use the `codex-slides-known-errors` sibling when the runtime, MCP, durable
  run, Browser handoff, project resume, render, Design Files, or export fails.

## Open and verify in Codex Browser

Open the Browser **before** creating a new deck and keep it open throughout the
workflow. After any programmatic mutation, navigate or reload the project URL
and inspect the visible result. Do not stop after printing the URL when the
Browser capability is available.

Preserve exact handoff query parameters: `slide`, `panel`, `version`, `mode`,
`checkpoint`, `conversation`, and `run`. Presenter mode intentionally leaves
one visible user click because browsers require a gesture to open its second
window.

Use Browser view `scenarios` for the workflow catalog, `design-files` for the
file workspace, and `brand-system` for the visual-system editor. Use the normal
workspace for Play from current/beginning, dual-window presenter mode, speaker
notes editing or AI generation, slide navigation, direct on-canvas marking, and
layout inspection. If the current Codex surface has no in-app Browser session, return
the local URL and state that limitation instead of claiming it opened.

## Export only after review

Use `export` / `export_deck` with `pdf` or `pptx` after the requested visual
result is ready. Return the download URL and keep the project preview URL
available for follow-up edits.

## Runtime

Use Node.js 20 or newer. Override the default app URL with
`CODEX_SLIDES_URL`; override the source checkout with `CODEX_SLIDES_HOME`.
