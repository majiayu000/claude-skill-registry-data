---
name: build-schematic-models
description: Design and approve complete dimensioned mechanical schematics, construct independent parts, then assemble and review editable and portable articulated models. Use for vehicles, devices, vessels or similar objects with separately addressable rigid and flexible components; finished animation and engine integration remain separate.
engines: [AGNOSTIC]
---

# Build Schematic Models

## When to use

Use for dimension-driven mechanical objects whose components must remain separately modeled and articulated. Route buildings to `build-floor-plan-models`; finished clips and game-engine behavior follow their own workflows.

## Workflow

1. Resolve this skill and the selected `SCHEMATIC_TO_MODEL` pipeline. Read `STYLE.md` and `.styles/.pipelines/schematic-to-model/PIPELINE.md` from the Hephaera installation. Preserve engine/default selection; a prompt override stays task-local. Read `MEDIA.md` only for generated reference media actually in scope. Inspect configured external libraries before replacement work, using only project-local copies with rights evidence.
2. Capture purpose, dimensions, materials/appearance, internal systems, moving parts, inspection needs, detail, tolerances and finite budgets. Author the pinned Bubo assembly design/profile with stable definitions, physical instances, subassemblies, local frames, interfaces, joints, mechanisms, terminals and routes. Declare observations, assumptions, unresolved or simplified systems before approval; references do not supply dimensions automatically.
3. Use `schematic-to-model.sh init` with exact design rights and process limits, then `validate` and `preview`. Show the complete dimensioned orthographic/section/exploded package, BOM, connections and part/assembly/flexible-rig sheets together. Record actual whole-package human approval with `record --kind whole-assembly-design`. Revisions create a new version with retained parent ancestry and invalidate dependent approval/evidence.
4. Use `doctor`, explicitly select an existing supported Blender, then `build-parts`, `assemble` and `prove-motion` in order. Require an approved v2 design/profile and independently verified parts. Retain every physical occurrence separately, even when identical definitions share geometry. Verify supported joints/coupled mechanisms and real owned wire/hose/spring/belt deformation against approved interfaces, sampling, clearances and limits. Use only Bubo's audited fixed bundle; report unavailable tool/host enforcement without installation, arbitrary scripts or fallback.
5. `export --author ID`, then `review`. Compare actual rest/diagnostic raw and independently re-imported GLBs with approved geometry, quantities, materials, hierarchy, local precision, pivots, skins and channels. Review every exterior/internal/exploded view and every diagnostic sample. Record independent model review, then separate actual `human-model` acceptance using exact current artifact identities. `status` inspects freshness and retained failures; synthetic tests never supply human acceptance.

## Output

Deliver editable source, animation-free assembled GLB, approved schematics/BOM, component/mechanism metadata and a separately labeled diagnostic-motion package in non-runtime staging. Every component stays separately addressable. Sampled readiness is not manufacturing, circuit/physics or continuous-collision certification, finished animation, engine behavior or asset promotion.

For later animation, resolve `build-model-animations` and explicitly use the current preserve-only `mechanical-assembly` handoff. Preserve mixed rigid/flexible identities and rig ownership; source-state changes invalidate the descriptor. Existing motion profiles and separate motion/human runtime reviews remain in force. No operation here copies a model into a game.

Read `commands/BUBO_ARGUMENTS.md` (Schematic to model) in the installation for host flags and policy receipts. As each native stage becomes relevant, read its maintained contract under `runtime/bubo/resources/schematic-to-model/`: `README.md` for design, `PARTS.md` for independent construction, `ASSEMBLY.md` for articulation and `EXPORT.md` for portable verification/review/handoff. Do not duplicate their schemas in task instructions.
