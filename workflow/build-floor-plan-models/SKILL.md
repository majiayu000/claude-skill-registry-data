---
name: build-floor-plan-models
description: Design dimensioned floor plans and turn one approved architectural package into detailed unfurnished building models. Use for single-storey, multi-storey or courtyard architecture with editable source and portable visual/collision exports.
engines: [AGNOSTIC]
---

# Build Floor Plan Models

## When to use

Use for dimensioned building architecture, including individual floors, connected storeys and courtyards. For engineered vehicles, devices or vessels with independently modeled components, use `build-schematic-models`.

## Workflow

1. Resolve this skill and the selected `FLOOR_PLAN_TO_MODEL` visual pipeline. Read `STYLE.md` and `.styles/.pipelines/floor-plan-to-model/PIPELINE.md` from the Hephaera installation. Preserve the current engine and default pipeline; a prompt override belongs only to this task. Read `MEDIA.md` only when generated reference images are actually in scope.
2. Capture purpose, floor count, dimensions, architectural style/materials, circulation, player-clearance envelope, detail profile, tolerances and budgets. Inspect configured external libraries first and use only project-local copies with rights evidence. Reference images guide the design; author dimensions explicitly.
3. Author the versioned plan from the pinned Bubo construction schema/examples. Keep stable semantic IDs, one shared coordinate datum, explicit room connectivity, openings, stair/slab connections and courtyard voids. Read the design/construction contracts linked from the pipeline rather than inventing a second schema.
4. Initialize with `floor-plan-to-model.sh init`, explicit plan rights and finite process budget. Run `validate` and `preview`, then show the user the complete dimensioned design: every floor, roof, exterior elevation and vertical-connection section. Record approval of the exact whole package using actual user evidence. Revise through a new version with retained parent ancestry; earlier approval never transfers automatically.
5. Inspect prerequisites with `doctor`, select an existing supported Blender explicitly, then `build`, `export --author ID` and `review`. All geometry/drawing/export algorithms and fixed audited authoring scripts stay in Bubo. Report unavailable tool/host enforcement explicitly without installation or fallback.
6. Review every exported floor, elevation, roof and required section, then compare the independent visual/collision imports with approved dimensions, openings, materials, semantic hierarchy, door pivots and clearances. Record an independent review and separate human model acceptance against the current package and complete views. Use `status` to inspect current evidence and retained failures.

## Handoff

Deliver editable Blender source, separate visual/collision GLBs, semantic metadata, approved drawings and provenance in non-runtime staging. These are unfurnished architectural model packages. Engine adapters, runtime collision/movement tests, gameplay, asset promotion, curved forms and automatic CAD/raster conversion remain separate work. No command here grants runtime acceptance or copies a model into a game.

Read `commands/BUBO_ARGUMENTS.md` (Floor plan to model) in the Hephaera installation for command arguments and policy receipts.
