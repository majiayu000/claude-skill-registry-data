---
name: realsee-blender-reconstruction
description: Reconstruct an evidenced indoor space from local Realsee scan exports, point clouds, CAD, and panoramas as a separately editable native Blender scene. Use for scan-to-Blender space modeling, source-based geometry/material/light refinement, and requested walkthrough or physics exports. Argus panorama-to-depth inference is a separate capability.
---

# Realsee → editable Blender space

[简体中文](SKILL.zh-CN.md)

Deliver a convincing, usable whole-space model promptly, then refine the parts that matter to the user. Turn the user's captured space into a native scene they can change in Blender. Prioritize spatial layout, walls, floors, ceilings, openings, and fixed services; add furniture and small objects to the depth requested. Execute Blender, inspect its output, and refine it. A plan, a script, or a saved scan import alone is not the reconstruction.

## Default: whole space first, selective refinement

Use the user's intended views and edits to set detail, not the maximum detail visible when zooming into every source. Read [fast modeling and preview workflow](references/fast-workflow.md) when starting a whole-space reconstruction or choosing an iteration strategy; use [automation performance](references/automation-performance.md) when scripting many objects or diagnosing slow iterations.

- Build and preview all requested areas with the scan reference disabled before refining individual rooms. Prioritize scale, connectivity, openings, major finishes, and lighting; a blockout is a checkpoint, not the final handoff.
- Use the simplest editable construction that meets the requested use. Inspect sources and add detail when they resolve a visible or functional defect; follow the linked workflow for batching, previews, and stopping criteria.
- Verify representative real edits and deliver once the requested result is achieved. User-specified exhaustive reconstruction or engineering checks take precedence.

For a narrow edit to an existing scene, inspect the target and its dependencies, patch a preserved copy, and verify the changed result. A wall-color change needs the actual shader result, data-sharing check, saved persistence, and unaffected neighbors; it does not initiate source registration or reconstruction-wide geometry tests. Reuse prior acceptance evidence and rerun only invalidated checks. If earlier checks are unavailable, report the scope actually verified instead of claiming a new full-scene certification.

## Establish the project and scope

Use the selected project directory as `PROJECT_ROOT`, never the installed skill directory. Resolve input and output paths against it. Use the user's paths; otherwise inspect `data/` and deliver `output/reconstruction_native.blend`. If inputs are absent, explain exactly what is missing; do not create an empty folder and treat it as evidence. Preserve original inputs and existing user models.

Read an existing project brief or acceptance requirements if provided. The user's requested scope and tolerances take precedence over this workflow. Do not inherit a reference case's scope, dimensions, tolerances, or execution settings.

Discover Blender from PATH, the user's executable setting, or the available local integration, then verify its version. Resolve an executable symlink before launch. Background `bpy` execution works without MCP. Inspect APIs in the installed Blender before writing version-sensitive import, material, render-device, or export calls. Store project scripts, checkpoints, and previews in the project, not in this skill.

## Reconstruct from evidence

Read [source registration and native modeling](references/reconstruction.md) when beginning or correcting the scene.

1. Briefly inventory substantive inputs and their purposes, duplicates, dependencies, and inspection status; deepen the record only when useful to the task. Preserve texture paths. Several exported formats of one scan do not represent several physical spaces.
2. Establish units, up axis, handedness, origin, floor datum, source-to-scene transforms, and trustworthy correspondences before detailed modeling. Use drawings for annotated dimensions, cloud/mesh for 3D surfaces, and photographs for appearance. Expose material conflicts between sources instead of tuning scale to hide them.
3. Map evidenced areas and connections. Maintain a small coverage record from source features to actual object IDs, with measured, inferred, or unresolved status. Panorama stations are viewpoints, not room counts; reflections are not extra rooms.
4. Build the entire requested structure before decorating individual rooms. Use native Mesh/Curve data, material nodes, and meaningful editable modifiers. Separate door leaves from frames, place hinges correctly, and keep independently editable surfaces and components separate. Do not rely on a monolithic triangulated scan or billboards to stand in for structure.
5. Keep the registered original scan and its textures in a clearly named reference collection, hidden from final renders, or an accompanying reference file. The reconstructed space must still exist when the reference is disabled. Retain an untouched original and record registration separately.
6. Compare plan/elevation and neutral solid views, then each area's interior against rectified photos or registered cameras. Refine shapes, finishes, and physical light locations from those comparisons. Show concise previews at useful milestones and incorporate user corrections.

If delegating area or asset work, give each worker the shared coordinate frame and stable object IDs, use separate output files, and keep one owner responsible for integration. Do not let workers write the same `.blend` or control the same live Blender scene concurrently.

Complete authorized reconstruction and correction work rather than stopping at a blockout. If evidence or tools prevent a requested part, continue the independent work and identify the specific gap; do not describe inferred detail as a measured replica.

## Verify the saved deliverable

Read [acceptance and reopening tests](references/acceptance.md) before finalizing. For a reconstructed deliverable, run the fresh-process reopening and representative geometry/material edit-and-reopen checks once the final candidate is ready; repeat only when later changes invalidate them. They are essential for a claim of native editability. Moving an object alone is insufficient. Deliver the intended scene, never the edited test copy as the final model.

Cover requested spaces and structural connections, key source/model dimensions, resource loading, materials, and reference-disabled renders. Keep uncertainty and unperformed checks visible. Scale the report to the task; a short list of meaningful discrepancies is more useful than invented precision or a large audit for its own sake.

Deliver the `.blend`, required packed or relatively linked resources, useful comparisons, scripts actually used, and concise editing notes. Distinguish a verified editable reconstruction from photorealistic or dimensional equivalence; each needs its own evidence.

## Requested extensions

Read [walkthroughs, physics, generated assets, and web previews](references/extensions.md) only for those requests. A generated asset, a video, or a web GLB does not replace the editable native scene. Do not automatically upload scans, buy generation credits, publish files, or change global GPU/proxy settings as part of local modeling; follow the user's actual authorization for those actions.
