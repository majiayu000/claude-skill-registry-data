---
name: use-3d-software
description: "Exact steps in the 3D tool the job needs: Blender (geometry nodes, shaders, modeling, rigging, animation, bpy), three.js and Crucible, Godot, Unity and Unreal, and moving assets between them (GLB, FBX, USD, scale, axes). Maps Cinema 4D, Houdini, Maya and 3ds Max habits to free tools. Use for any step inside a 3D app or engine, \"geometry nodes\", \"bpy script\", \"import to Unity\", \"export GLB to three.js\" (\"node Blender\")."
license: MIT
---

# Use 3D Software

A tool skill. The generalist and craft skills decide what to make. This one says how to do it in the tool the user
has or the target needs, by script or by the exact UI path, with current names.

Read `local.md` next to this file first when it exists (machine paths and local rules).

## When to use

- Any step inside a 3D app or engine: a node tree, a material, a rig, a modifier stack, a bake, a headless render,
  an import, a scene in an engine, an export to another tool.
- Called from `3d-generalist`, `2d-generalist`, `model-characters`, `rig-characters`, `animate-characters`,
  `draw-and-paint-art` and `paint-stylized-backgrounds`. They own the workflow and the look. Do not restate their steps.
- Not for hard-surface CAD with exact dimensions (use a CAD tool such as build123d or FreeCAD).

## Pick the tool

Use the tool the user already has or the delivery needs. When nothing decides it: Blender for modeling, rigging,
offline renders and film; three.js for a page people open in a browser; Godot for a free, light game; Unity for a
mobile or cross-platform game with a big asset store; Unreal for a photoreal real-time scene or game.

## Routing

| The task is | Read |
|---|---|
| Any Blender step: headless runs, priority, version names | `references/blender-headless-and-versions.md` first |
| Blender node trees, instancing, scattering, curves, volumes, Grease Pencil in nodes | `references/geometry-nodes.md` |
| Blender materials, procedural textures, world, toon, baking, lighting, compositor, depth of field | `references/shading-and-textures.md` |
| Stylized Blender looks: clay, painterly and Paint Filter, comic toon shader (cell shade, screen tone, outline, rim light, glow), line art, pixel, wear and grime masks, glass, skin and thickness, toon water, hologram, curve hair and fur | `references/stylized-shading-recipes.md` |
| Blender lighting roles and ratios, light linking, IES and gobos, cheap fog, Cycles and EEVEE speed, 2.5D backgrounds, scatter and LOD in geometry nodes, hotkeys | `references/lighting-render-and-gn-recipes.md` |
| Blender meshes, modifiers, skin modifier, props, sculpt notes, particles | `references/modeling.md` |
| Blender environments: terrain, scattering, grass and trees, wind, fog and god rays, rain, buildings from photos, HDRI worlds | `references/environments.md` |
| Rain, wind, storms, sun and sky, snow and fog in Unity, Godot, Unreal, three.js or Blender: where to learn and what to start from | `references/weather-across-engines.md` |
| Quick Blender recipes: bevel and extrude keys, holes, bridges, lathe, array, lattice, shrinkwrap decals, pipes, gears, stairs, fences, rails, bookshelves, food | `references/quick-modeling-recipes.md` |
| Blender armatures, Rigify, IK, binding, weight paint, face rigs | `references/rigging-and-weights.md` |
| Blender keyframes, walk cycles, NLA, camera rigs, loops | `references/animation-and-nla.md` |
| Blender fire, explosions from VDB, lightning, liquid, cloth drapes, ocean, hair and fur, glitch | `references/effects-fx.md` |
| Blender hotkeys, bpy recipes, add-ons, free vs paid | `references/workflow-and-addons.md` |
| Fix a broken mesh, clean quads, UVs, LODs, meshopt or KTX2, and proof it still looks the same (`scripts/mesh_prep.py`) | `references/mesh-prep.md` |
| A web page: GLB loading, compression, animation, lights, colour, export from Blender | `references/threejs.md` |
| A photoreal room from code in three.js: baked per-vertex light, code textures, filmic grade, film; porting it to a path tracer | `references/threejs-baked-interior.md` |
| Godot 4: import, materials, AnimationTree, controller, camera, build | `references/godot.md` |
| Unity 6: FBX import, Humanoid rigs, Animator, terrain, Timeline, build | `references/unity.md` |
| Unreal Engine 5: Blueprints and C++, Enhanced Input, animation blueprint, UI, import from Blender | `references/unreal.md` |
| The user thinks in Cinema 4D, Houdini, Maya or 3ds Max terms | `references/paid-to-blender.md` (mapping, not tested) |

Read the reading map at the top of a reference, then the full entry you use. Entries keep exact steps and a source
link. Open the source link only when an entry is thin.

## Move assets between tools

- GLB (glTF 2.0) is the default between Blender, three.js, Crucible and Godot. FBX is the default into Unity and Unreal.
  USD for big scenes and Omniverse or SimReady assets.
- Apply scale and rotation before export. Blender is Z up. glTF, three.js, Godot and Unity are Y up. Unreal is Z up
  in centimetres. Check the forward axis on the first import with a test cube and an arrow.
- Bake procedural materials and modifiers that the target cannot read. Keep textures power of two.
- Name armature bones consistently. Export one action per clip, or split clips on import.
- Re-import into the target and look at it there before calling it done.

## How to work

1. Find the entry. If several fit, take the one closest to the installed version and note any renamed item.
2. Prefer a script for anything repeatable. Use the UI path when the user wants to learn or edit by hand.
3. Build in the smallest scene that shows the technique, then swap in the real asset.
4. Prefer a real asset from a licence-clear source (Poly Haven, ambientCG, Kenney, Quaternius) and credit it. For a
   restricted or unknown licence, ask the user once: use it at their responsibility, or skip it.
5. Name nodes, groups and objects. Expose inputs the user will tune.

## Checks before handing off

- Render or run one frame in the target tool and read the picture, not the node tree or the code.
- Look for stretched textures (unapplied scale), flipped normals, z-fighting, wrong axis, missing textures,
  black or grey colour from a wrong colour space, and popping at a loop point.
- For a rig, pose the extremes. For a loop, compare the first and last frames. For a script, run it twice.
- Paid add-ons and packs in the references are sources of ideas. Never buy or add one without the user's say.
- Report which entries and renamed items you used, and what you saw in the frame.
