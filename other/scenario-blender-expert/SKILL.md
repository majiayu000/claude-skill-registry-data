---
name: scenario-blender-expert
description: "Use when doing any 3D work in Blender through Python or an MCP bridge, headless or in a live session: modeling, sculpting a character or head, retopology, UV unwrapping, baking, texturing, rigging, animating, previs, geometry nodes, lighting and rendering, grease pencil, or finishing an AI-generated mesh into a production asset. Also when a bpy script fails on Blender 5.x API changes, a brush or sculpt operator fails or crashes headless, or a result has to be judged like a professional 3D artist would."
license: MIT
---

# Blender expert (router and agent protocol)

Expert-level Blender work is a loop, not a script: build big to small, and at every stage turn the model, measure it and fix it before adding detail. This skill is the protocol every Blender task follows and the map to the domain skills distilled from Blender Studio artists, Blender Conference talks and top instructors (sources in each skill). If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## 1. Execution channel

| Channel                                                                                    | Use for                                                                                | Rules                                                                                                                                                                                                                              |
| ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Live GUI Blender (user's session over the MCP bridge)                                      | anything interactive: real sculpt/paint brushes, weight painting, viewport screenshots | One short, idempotent script per call returning a compact result dict. Get-or-create by name. Never touch objects you did not create. Save a stage backup `bpy.ops.wm.save_as_mainfile(filepath=..., copy=True)` after each stage. |
| Headless helper `blender -b [file] --factory-startup --python-exit-code 1 -P x.py -- args` | renders, audits, batch ops, anything when no bridge is up                              | Always `--factory-startup`: without it the user's add-ons load (on this machine one of them makes network API calls). Without `--python-exit-code` a failing script still exits 0. Print a final machine-readable result line.     |

Never open your own GUI Blender window to test things on the user's machine: windows steal focus and pile up. Live work goes through the user's already-running Blender; everything else runs headless, one Blender process at a time per agent (other sessions may be rendering on the same machine).

Check `bpy.app.version` first; this skill set targets 5.2 LTS. Many tutorials the experts recorded use 2.8x to 4.2 UI: read [`references/blender-5.2-deltas.md`](references/blender-5.2-deltas.md) before trusting any remembered operator, brush name or API.

**Verified capability matrix (Blender 5.2.1):**

| Action                                                                                                                                | Headless                                               | GUI session                                       |
| ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------- |
| Voxel remesh, QuadriFlow, multires subdivide, modifiers, bmesh, UV ops with edit-mode context, Cycles/EEVEE/Workbench renders, baking | yes                                                    | yes                                               |
| `bpy.ops.brush.asset_activate`, dyntopo toggle                                                                                        | yes                                                    | yes                                               |
| Brush strokes (`sculpt.brush_stroke`, `paint.image_paint`, `paint.weight_paint`)                                                      | no (poll fails)                                        | yes, via [`scripts/bx_gui.py`](scripts/bx_gui.py) |
| `paint.mask_flood_fill`, `sculpt.mesh_filter`                                                                                         | CRASHES Blender                                        | yes, via `bx_gui.run()`                           |
| Programmatic sculpting on mesh data                                                                                                   | yes, `scenario-blender-sculpting/scripts/bx_sculpt.py` | yes                                               |

## 2. The expert loop (every domain)

1. **Establish the brief** in numbers: purpose (film, game engine, still, animation), budgets (tris, texture size, frame range), style (stylized or realistic), references. When the brief is silent, choose a documented default from the domain skill and write it down.
2. **Plan the stages** the domain skill defines. Never start with detail.
3. **Build one stage** with the smallest scripts that do it.
4. **Gate the stage:** run the measurable checks ([`scripts/bx_audit.py`](scripts/bx_audit.py) for meshes, the domain's own checks) AND render a review sheet ([`scripts/bx_review.py`](scripts/bx_review.py): silhouette, matcap, wire from front/side/three-quarter/low) and open it with the image reader. Experts orbit constantly; the review sheet is the agent's orbit. Judge with the domain's `references/critique.md`.
5. **Fix before advancing.** A problem found at blockout costs one script; found after texturing it costs the stage.
6. **Deliver with evidence:** final renders, audit numbers, and what was not verified.

Never report a model, rig, animation or render as done without having looked at a render of it.

## 3. Persona pipelines

| Persona / brief                                     | Skill chain                                                                                                                                                                                                | Deliverable                                                  |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| Character artist, stylized or realistic             | scenario-blender-sculpting, scenario-blender-retopology, scenario-blender-uv-baking, scenario-blender-texturing-shading, scenario-blender-hair                                                             | sculpt, animation-ready low poly, UVs, baked maps, materials |
| AI-mesh finisher (Scenario 3D output to production) | audit the generated mesh, scenario-blender-retopology (or cleanup + remesh), scenario-blender-uv-baking (bake FROM the generated high), scenario-blender-texturing-shading; generation itself: scenario-3d | clean, UV'd, baked asset at a stated budget                  |
| Game asset artist                                   | scenario-blender-hard-surface or scenario-blender-sculpting, scenario-blender-retopology (game budget), scenario-blender-uv-baking, scenario-blender-texturing-shading                                     | low poly + PBR set, exported glTF/FBX                        |
| Rigger / character TD                               | scenario-blender-rigging                                                                                                                                                                                   | rig with controls, weights, deformation tests                |
| Animator                                            | scenario-blender-previs-storyboard (shot planning), scenario-blender-animation                                                                                                                             | blocked, splined, polished shot + playblast                  |
| Story / previs artist                               | scenario-blender-previs-storyboard, scenario-blender-grease-pencil                                                                                                                                         | shots, cameras, animatic                                     |
| Look-dev and lighting artist                        | scenario-blender-texturing-shading, scenario-blender-lighting-rendering                                                                                                                                    | lit, color-managed, composited renders                       |
| Technical artist / procedural                       | scenario-blender-geometry-nodes                                                                                                                                                                            | node-group assets, procedural systems                        |
| 2D / 2.5D animator                                  | scenario-blender-grease-pencil                                                                                                                                                                             | GP animation                                                 |

Related skills outside this set: scenario-3d (generate meshes to finish here), scenario-textures (AI textures), text-image-to-blender-blockout (camera-locked blockouts for render-to-real video).

## 4. Shared toolkit (`scripts/`, all tested on 5.2.1)

- `bx_audit.py`: `audit(obj, high=None)` returns quads %, n-gons, poles (valence 3 / 5+ / 6+), non-manifold, loose, duplicates, flipped faces, self-intersections, boundary loops, symmetry %, edge-length CV, and fidelity to a high poly; `verdict(report)` lists problems. CLI: `blender -b f.blend --python bx_audit.py -- --object Name [--high Sculpt] [--json out.json]`.
- `bx_review.py`: `review(objs, out_dir, views, modes)` writes one contact sheet (rows = modes, cols = views) in a temporary scene, user settings untouched; `playblast(path)`; `turntable(obj, path)`.
- `bx_gui.py`: real brushes in a live session: `set_view`, `activate_brush(mode, name)`, `stroke(mode, world_points, size, strength)`, `run(op, **kw)`, `set_paint_color`, `screenshot`.

Import pattern: `import sys; sys.path.append("<this skill>/scripts"); import bx_audit, bx_review`.

## 5. Version traps that break most remembered code

- Brushes are assets (4.3): `bpy.ops.brush.asset_activate(asset_library_type='ESSENTIALS', asset_library_identifier="", relative_asset_identifier="brushes/essentials_brushes-mesh_sculpt.blend/Brush/Clay Strips")`; brush size is a diameter (5.0); Flatten/Fill/Scrape merged into the Plane type.
- Auto Smooth removed (4.1): `mesh.shade_smooth()` / Smooth by Angle modifier; voxel remesh output is flat-shaded until you call `shade_smooth()`.
- Principled BSDF v2 (4.0): address sockets by name; Emission strength defaults to 0.
- `BLENDER_EEVEE` is the EEVEE Next identifier in 5.x (`BLENDER_EEVEE_NEXT` fails).
- Compositor is a node group (5.0): `scene.compositing_node_group`, not `scene.node_tree`.
- Video output: set `image_settings.media_type = 'VIDEO'` before `file_format = 'FFMPEG'` (5.0).
- Slotted actions (4.4), `action.fcurves` removed (5.0): use `bpy_extras.anim_utils.action_get_channelbag_for_slot(action, slot)`.
- Bone collections replace armature layers (4.0); Grease Pencil v3 is `GREASEPENCIL` with `bpy.ops.grease_pencil.*` (4.3).
- Positional context dicts for operators are gone: `with bpy.context.temp_override(...)`.
- `obj.matrix_world` is stale right after setting location/scale until `view_layer.update()`.

## References

- [`references/bpy-reliability.md`](references/bpy-reliability.md): checklist and tested procedures for reliable bpy (operators vs data API, stale references, evaluated vs original data, idempotent headless jobs, numpy bulk access, node trees, persistence). Load before writing any non-trivial script.
- `references/blender-5.2-deltas.md`: full, cited list of what changed from 2.8x to 5.2 per domain (load before writing code from memory or following an old tutorial).
