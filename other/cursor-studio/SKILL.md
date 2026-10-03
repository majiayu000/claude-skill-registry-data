---
name: cursor-studio
description: Build, run, troubleshoot, or extend a Cursor Studio macOS menu bar app that plans custom cursor packs from presets, prompt notes, slot lists, hotspot guidance, and exportable briefs. Use when Codex needs to work on a workspace containing `CursorStudioApp`, keep Cursor Studio separate from Folder Studio, regenerate the Xcode project, or validate the `CursorStudio` scheme and tests.
---

# Cursor Studio

Use this skill for a Cursor Studio workspace. If the current repo contains `CursorStudioApp` and `project.yml`, use that workspace by default. Otherwise, pass `--workspace /path/to/workspace` to the runner script.

## Quick Start

1. Read `references/project-map.md` for the split target layout and the main cursor files.
2. Run `bash scripts/run_cursor_studio.sh doctor`.
3. Run `bash scripts/run_cursor_studio.sh inspect`.
4. Use `bash scripts/run_cursor_studio.sh test` after preset, role, export, or UI changes.
5. Use `bash scripts/run_cursor_studio.sh build` when you need the app product.
6. Use `bash scripts/run_cursor_studio.sh open` to jump into Xcode.

## Workflow

### Product Boundary

- Keep `CursorStudio` focused on cursor-pack planning, not folder icons.
- Cursor Studio owns:
  - cursor presets
  - accent palettes
  - pack scope and slot selection
  - hotspot notes
  - prompt-template and brief export
- Do not fold folder-skin logic back into this target. That belongs to `FolderStudio`.

### UI Guidance

- Keep the menu bar panel compact, professional, and high-signal.
- Prefer native-feeling controls over decorative chrome.
- The main surface should answer three questions quickly:
  - what preset is active
  - which cursor roles are included
  - what export will be produced

### Editing Guidance

- Read `project.yml` before changing targets or schemes.
- Cursor models and export logic belong in `CursorStudioApp/Sources/App/`.
- The compact menu bar surface belongs in `CursorStudioApp/Sources/Views/`.
- If presets, accents, or role metadata change, update the tests too.

### Validation

- Run `doctor` if the workspace or tooling is uncertain.
- Run `test` after changing slot logic, builders, or the app model.
- Run `build` after panel or target changes.
- Keep output exports deterministic:
  - markdown should stay readable
  - json should stay machine-friendly
  - hotspot notes should match the selected roles exactly

## Resources

- `scripts/run_cursor_studio.sh`: workspace detection and local `doctor`, `inspect`, `generate`, `open`, `build`, and `test` commands.
- `references/project-map.md`: target map, main files, role and export contract, and validation notes.
