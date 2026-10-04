---
name: roadborne-game-assets
description: Plan, source, author, integrate, and verify Roadborne visual assets through its Godot Mono world-preview and UI pipelines. Use only in the Roadborne repository for environment art, models, materials, textures, animation, VFX, icons, UI art, concept references, asset provenance, or visual-quality evidence. Do not use for unrelated games or to decide unresolved Roadborne art rules.
---

# Roadborne Game Assets

Produce the smallest owner-authorized visual slice and prove it in the actual Godot client. This
skill does not turn a concept, imported file, successful build, or attractive screenshot into
approved production art.

## Establish authority

1. Confirm the workspace is Roadborne by reading AGENTS.md.
2. Read outstanding_questions.md and the owning document:
   - WORLD_PREVIEW.md and WorldDesign.md for opening-region environment work;
   - ICE_BIOME_DESIGN.md for Rimefall work;
   - UI_DESIGN.md and GAMEPLAY_DESIGN.md for UI, feedback, and accessibility;
   - TECHNICAL_DIRECTION.md for the engine and asset-pipeline boundary.
3. Preserve the exact statuses Decided, Unresolved, Delegated, Deferred, Paused, Rejected,
   Reference, and Candidate. Only the owner promotes a proposal or asset to Decided.
4. Inspect git status before writing. Preserve unrelated dirty files, worktrees, generated
   evidence, and running processes.

Determine the effective Godot version from src/Roadborne.Client/Roadborne.Client.csproj and the
actual Godot executable used by the repository scripts. Never assume the newest installed version
or silently migrate the project.

## Route the task

- Environment composition, materials, terrain, ecology, lighting, time of day, or visual parity:
  follow the world-preview loop below.
- A model, rig, animation, collision mesh, LOD, or GLB/glTF export: read
  references/three-d-pipeline.md. Use roadborne-blender-assets only after ART-Q03 is active and its
  missing conventions are selected.
- UI art, icons, raster textures, or image normalization: read references/raster-pipeline.md and
  retain the accessibility rules in UI_DESIGN.md.
- A new or revised visual language: read references/art-direction.md, but stop at Candidate until
  the owner approves it.
- Licensing, generated media, CC0, commissioned work, or source acquisition: read
  references/provenance.md before downloading or generating anything.
- Performance measurement or optimization: also use performance-optimization, while treating
  every unselected hardware or asset budget as Unknown rather than inventing a target.
- Concept-image generation or editing: use imagegen for the media operation. Its result remains a
  concept/reference until separately authored and accepted as an engine asset.

## World-preview production loop

1. Define one visible acceptance slice already authorized by the owning document. If the needed
   art rule, source policy, Blender convention, or acceptance target is unresolved, expose that
   dependency rather than choosing it.
2. Inspect the current source asset, import sidecars, ASSET_PROVENANCE.md, checksums, runtime code,
   fixed review anchor, and latest comparable raw capture.
3. Capture or identify an append-only baseline with the repository's Run-WorldPreview.ps1 path.
   Record worktree/commit identity, client DLL hash, Godot version, renderer, viewport, camera FOV,
   anchor, Beauty/HUD state, capture hash, and log path.
4. Change the fewest authoritative source files. Prefer existing Roadborne modules and retained
   source assets; do not add a parallel asset manifest, art bible, scene, camera, or renderer.
5. Run a non-skipped Godot import before relying on a new or changed asset. Build success proves
   compilation only; import success proves only that Godot accepted the tested input.
6. Capture the same anchor and camera conditions after the change. Inspect the raw images directly
   and report the specific visible improvement, regression, or unchanged result.
7. When performance is in scope, measure the same scene and hardware before and after. Report
   frame time, CPU/GPU evidence, draw calls, visible instances, primitives, memory, and loading
   separately when available. Do not infer a shipping target from the current RTX 3080.
8. Update the existing provenance/checksum record and every affected durable Roadborne document.
   If no durable document changes, record why the existing claims remain accurate.

## Acceptance boundaries

- Original or CC0 source with recorded provenance is the current initial-asset rule.
- Generated images may guide composition, materials, or modeling; they do not substitute for
  meshes, UVs, rigs, animation, collision, navigation, or engine validation.
- The rejected engineering foreground gate and rejected population candidates remain rejected.
  Do not polish, republish, or propagate them as production art.
- Compare visual-quality evidence at equivalent camera distance, FOV, renderer, resolution,
  density, and debug state. Edited comparison boards and Remotion videos are presentation
  artifacts; preserve the raw Godot captures and logs as evidence.
- Accessibility cues cannot rely on color alone.
- No asset may copy protected Silkroad Online art, maps, names, audio, or other source material.
- Do not commit, push, deploy, install a DCC, change the selected Godot version, or operate live
  services unless the current owner instruction explicitly authorizes it.

## Evidence report

Report source/provenance evidence, source/build/import evidence, local runtime/capture evidence,
visual acceptance, performance evidence, and remaining unproven claims as separate lanes. Include
exact changed paths and checks run. Never collapse those lanes into "production-ready" or
"parity" without the owning acceptance matrix passing.

## References

- Read references/art-direction.md only for a visual-language task.
- Read references/raster-pipeline.md only for raster, UI-art, icon, or texture normalization.
- Read references/three-d-pipeline.md for models, materials, rigs, animation, collision, LOD, or
  GLB/glTF work.
- Read references/provenance.md before acquiring, generating, or changing asset rights records.
- UPSTREAM.md records the adapted source and license.
