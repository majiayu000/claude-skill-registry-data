---
name: world-content-pipeline
description: "Organizes world content from design source to validated runtime assets. Use when a game has biomes, props, NPCs, structures, items, audio, localization, or procedural templates."
---

# World Content Pipeline

## Use when
Content is copied manually between design, source assets, runtime registries, and documentation, producing drift and missing dependencies.

## Workflow
1. Define canonical IDs, editable source formats, derived outputs, ownership, localization keys, and compatibility constraints.
2. Build validation for missing references, duplicate IDs, invalid dimensions, broken asset links, unused entries, and dependency cycles.
3. Separate authored data from generated artifacts and make transformations deterministic with logged tool versions.
4. Create a small end-to-end content example that is edited once, rebuilt, loaded in the game, and verified by tests.

## Required output
A content data-flow map, schema/ID conventions, pipeline validation list, and one working vertical-slice example.

## Validation
- Runtime content is traceable to canonical source data.
- Build failures identify the offending ID/file and the dependent reference.
- Generated files can be recreated rather than hand-patched.

## Guardrails
Do not edit generated output as the permanent fix when the canonical source or generator is responsible.
