---
name: roadborne-blender-assets
description: >
  Inspect, author, repair, audit, render, and export Blender assets for Roadborne's Godot Mono
  pipeline. Use only in the Roadborne repository for Blender source scenes, bpy automation,
  evaluated topology, UV/PBR work, rigs, animation, LODs, collision or navigation meshes, and
  GLB/glTF handoff. Respect ART-Q03: when its Blender/version/units/axes/export contract is Paused
  or Unresolved, limit work to explicitly authorized research or inspection and do not claim a
  production export pipeline.
---

# Roadborne Blender Assets

Treat every Blender result as one input to the Roadborne Godot pipeline, not as production proof.
Preserve editable source, measure evaluated geometry, verify export/import, and inspect the result
through the actual gameplay or review camera.

## Authority and stop gate

1. Confirm the workspace is Roadborne and read AGENTS.md, outstanding_questions.md, and the owning
   world, character, UI, or technical document.
2. Read ART-Q01 through ART-Q05. ART-Q03 owns the Blender version, units, axes, editable source,
   deterministic GLB, collision, and navigation conventions.
3. If ART-Q03 is Paused or Unresolved, do not install or upgrade Blender, select those conventions,
   author a production export, or integrate a new production asset unless the owner's current
   instruction explicitly resumes and bounds that work. Inspection, audit-script maintenance, and
   rejected-evidence review may proceed only within the current instruction.
4. Derive the effective Godot version from src/Roadborne.Client/Roadborne.Client.csproj and verify
   the exact Blender executable used. Do not assume either version.
5. Inspect git status and the active .blend path before mutation. Preserve unrelated dirty files,
   other Blender scenes, ignored evidence, and running processes.

## Establish the asset contract

Use recorded owner decisions only. Record or mark Unknown:

- gameplay role, camera distance, silhouette and accessibility requirements;
- source and rights status under the original-or-CC0 initial-asset rule;
- deliverables: editable .blend, GLB/glTF, textures, rigs/actions, collision, navigation, LODs,
  sockets, and review captures;
- selected units, axes, origin/pivot, names, folders, and export/import settings;
- selected triangle, material, texture-memory, bone, and animation budgets;
- exact Godot scene, review anchor, renderer, FOV, resolution, and acceptance condition.

Do not reasonably default an unresolved Roadborne product or pipeline decision.

Read references/game-ready-assets.md for asset-quality gates and references/blender-core.md before
non-trivial bpy data manipulation.

## Control path

1. Prefer direct bpy data access for deterministic construction, inspection, and batch edits.
2. Use bpy.ops only when its context is deliberately established and the operator is appropriate.
3. Prefer Blender background mode for repeatable audits, previews, and exports.
4. Use a Blender MCP bridge only when the owner authorized live editor mutation, its tools were
   discovered, and the exact running Blender instance and file were confirmed.
5. Use interactive UI work only when visual judgment or a UI-only operation requires it.

Never overwrite the only source .blend or claim an editor/MCP change without direct confirmation.

## Asset loop

1. Inspect Blender version, units, render engine, collections, linked libraries, evaluated
   modifiers/Geometry Nodes, materials, images, armatures, actions, transforms, origins, UVs,
   normals, dependencies, and provenance.
2. Solve gameplay-scale silhouette, proportion, negative space, origin, and collision role before
   high-frequency detail. Judge from the selected Roadborne camera.
3. Build reversible geometry that supports shading, baking, deformation, LOD, and the target
   silhouette. Keep semantic pieces separate while proportions change.
4. Author UVs and PBR materials for the effective Godot importer. Reuse Roadborne's recorded
   channel-packing and color-space conventions; do not invent a parallel material standard.
5. For rigs/animation, verify rest transforms, weights at extreme poses, stable bone/action names,
   clip ranges, loops, and the selected root-motion policy.
6. Create LODs from measured screen coverage and separate render geometry, collision/navigation
   proxies, sockets, and triggers according to their gameplay roles.
7. Run scripts/audit_blender_asset.py inside Blender. Its evaluated triangle/topology result is a
   mechanical gate only, not visual acceptance.
8. Export to a new artifact path using the selected ART-Q03 contract. Re-import into a clean
   Blender scene when useful, then run a non-skipped import in the exact Roadborne Godot checkout.
9. Verify scale, axes, hierarchy, names, materials, textures, normals/tangents, bounds, actions,
   deformation, LODs, collision/navigation correspondence, and missing dependencies in Godot.
10. Capture the raw asset in representative Roadborne gameplay/review conditions and compare it
    with the fixed baseline. Record performance separately when it is in scope.

Read references/automation-and-qa.md before scripting, background execution, export, or delivery.

## Roadborne boundaries

- Do not reuse the rejected traveler, foreground-gate fixture, or another rejected source as
  production art.
- No procedural or generated output bypasses topology, UV, rig, license, import, runtime, or visual
  gates.
- Do not copy protected Silkroad Online assets or use them as extraction inputs.
- Do not infer production quality, current-Silkroad parity, collision, navigation, or animation
  success from a Blender beauty render.
- Do not invent asset budgets or a target hardware floor. Report counts and measured costs until
  the owner records a target.
- Update the existing Roadborne ASSET_PROVENANCE.md and checksums; do not create a competing
  manifest.
- Do not commit, push, deploy, change Godot/Blender versions, or modify live services without
  explicit current authorization.

## Evidence report

Report source and rights, Blender source/audit, exported artifact, clean re-import, Godot import,
raw runtime capture, measured performance, visual acceptance, and remaining unknowns separately.
Include exact paths, executable versions, settings, counts, hashes, and checks actually observed.

Use references/official-blender-sources.md for version-sensitive API/export claims. UPSTREAM.md
records the adapted source and license.
