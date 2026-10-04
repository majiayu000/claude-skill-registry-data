---
name: reference-sheets
description: Plan character, location, and prop reference sheets including functional prop views without hardcoding one universal view count.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Reference Sheets

## Procedure

Read `../../references/REFERENCE_SHEETS.md`. Validate `reference_sheet_plans.json`. Before generation, use `generation-workflow-setup` to choose the complete character-sheet, location-orbit, prop-sheet, or orbit-sheet workflow from the numbered catalog. Bundled workflows under `comfyui_workflows/` are real editable workflow sources, not sanitized blueprints. Validate the selected workflow and its live dependencies before execution.

## Done

Durable project state and deterministic validation agree before downstream generation continues.
