---
name: folder-studio
description: Build, run, troubleshoot, or extend a Folder Studio macOS menu bar app that reads folder context, suggests engravings, colors folders, previews Finder-style skins, and applies custom icons. Use when Codex needs to work on a workspace containing `FolderStudioApp`, keep Folder Studio separate from Cursor Studio, regenerate the Xcode project, or validate the `FolderStudio` scheme and tests.
---

# Folder Studio

Use this skill for a Folder Studio workspace. If the current repo contains `FolderStudioApp` and `project.yml`, use that workspace by default. Otherwise, pass `--workspace /path/to/workspace` to the runner script.

## Quick Start

1. Read `references/project-map.md` for the split target layout and the main folder-skin files.
2. Run `bash scripts/run_folder_studio.sh doctor`.
3. Run `bash scripts/run_folder_studio.sh inspect`.
4. Use `bash scripts/run_folder_studio.sh test` after analysis, rendering, or UI changes.
5. Use `bash scripts/run_folder_studio.sh build` when you need the app product.
6. Use `bash scripts/run_folder_studio.sh open` to jump into Xcode.

## Workflow

### Product Boundary

- Keep `FolderStudio` focused on context-aware folder skins, not cursor packs.
- Folder Studio owns:
  - folder analysis
  - dominant category detection
  - engraving suggestions
  - color palette and finish controls
  - Finder icon preview and apply/reset behavior
- Do not blend cursor-pack planning back into this target. That belongs to `CursorStudio`.

### UI Guidance

- Keep the menu bar panel compact and professional.
- The app should make these signals visible immediately:
  - folder name and dominant category
  - key content counts
  - current engraving, badge, and palette choices
  - whether the icon is ready to apply or reset

### Editing Guidance

- Read `project.yml` before changing targets or schemes.
- Folder analysis and icon rendering belong in `FolderStudioApp/Sources/Services/`.
- Panel state and persistence belong in `FolderStudioApp/Sources/App/`.
- Compact panel UI belongs in `FolderStudioApp/Sources/Views/`.
- If category heuristics or palette behavior change, update the tests too.

### Validation

- Run `doctor` if the workspace or tools are uncertain.
- Run `test` after changing analysis, builders, render logic, or panel behavior.
- Run `build` after target or view changes.
- Preserve Finder icon behavior:
  - preview should match the generated icon payload
  - apply should set a custom folder icon
  - reset should clear it back to Finder defaults

## Resources

- `scripts/run_folder_studio.sh`: workspace detection and local `doctor`, `inspect`, `generate`, `open`, `build`, and `test` commands.
- `references/project-map.md`: target map, main files, analysis and icon contract, and validation notes.
