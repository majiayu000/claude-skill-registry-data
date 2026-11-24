---
name: sculpt-models
description: "Sculpt characters, creatures, heads, rocks, cliffs, terrain and worn props in Blender 5.x, by hand or with bpy, or refine a Tripo mesh; multires, remesh, retopo, bake, silhouette check. Use for \"sculpt\"."
license: MIT
---

# Sculpt Models

This craft skill owns digital sculpting: form, anatomy, surface detail, environment sculpts and the Blender 5.x
sculpt toolset, through to a retopologised and baked asset. It is called by `3d-generalist` and `model-characters`.
Read `local.md` next to this file when it exists (machine paths).

## When to use

- A character, creature, head or bust that must read as organic, not blobby or symmetric.
- Rocks, cliffs, terrain, bark, ruins, worn and damaged props.
- Refining an AI base mesh (Tripo Studio) or a scanned mesh: re-cutting planes, eyelids, mouth corners, folds.
- A realistic close-up asset from AI: generate in parts, retopo, bake to a low poly (`references/ai-mesh-to-game-ready.md`).
- Turning one picture (AI image, render, figurine photo, drawing) into a sculpt measured against it.
- Baking sculpt detail onto a low-poly mesh for a game engine, three.js or Crucible.

Not this skill: stylised cartoon character sculpts step by step (`~/.claude/skills/model-characters/references/sculpt-stylized.md`),
machined parts at exact dimensions (`model-parts-in-cad`), drawing anatomy in 2D (`draw-and-paint-art`).

## Order of work

1. **Reference first.** Real photos or scans of the subject from several views (the `real resources first` rule):
   an animal, a rock type, a face type. Never sculpt a real thing from memory.
2. **Decide the end state.** Static (prop, environment, still) or deforming (rigged, animated); target face count and
   where it ships (`references/blender-sculpt-tools.md`, "Retopology and bake"). This decides every later step.
3. **Block out primary forms** from simple volumes at real scale, symmetry on, 5k to 20k faces, Voxel Remesh to unify.
   Run `scripts/check_sculpt.py` and read the silhouette sheet before any detail.
4. **Secondary forms:** planes, landmarks, muscle groups, folds, fracture planes (`references/form-and-anatomy.md`,
   `references/surfaces-environment-and-hard-surface.md`).
5. **Break symmetry** for anything alive, then **Multires** for tertiary detail in distinct layers by scale.
6. **Retopologise or decimate, then bake** normals (and displacement where detail changes the silhouette).
   Scripted route and the before/after numbers: `use-3d-software` `scripts/mesh_prep.py` (`references/mesh-prep.md`).
7. **Check again** (below) at the final camera distance, then hand the asset to `rig-characters` or the scene.

## Hard rules

- Big to small, always. No detail on a form whose silhouette has not passed.
- No global noise displace on a primitive as "sculpting": masses are built as volumes first.
- No perfect mirror on anything alive; no random vertex jitter as "asymmetry".
- Detail comes in distinct scales with rest areas between; one-frequency noise everywhere fails.
- Eyes, lids, lips, ears and nostrils have thickness and structure (`references/form-and-anatomy.md` §2).
- A sculpt that must deform is retopologised; a static one may be decimated. Never rig raw Dyntopo or voxel topology.
- Apply scale before sculpting; a scaled object stretches every stroke.

## Check gate (run before showing anyone)

```
blender -b <file.blend> --python scripts/check_sculpt.py -- [--object Name] [--out <folder>]
blender -b --python scripts/check_sculpt.py -- --import model.glb --out <folder>
```

It prints faces, scale, non-manifold edges, loose vertices, mirror error and surface busyness, and writes a
silhouette sheet (8 angles plus top and bottom) and a matcap and studio sheet. Exit 1 means a measured check failed.
Then look (more than about 5 pictures go through a frame-reading subagent):

1. The silhouette reads as the subject from every angle, at thumbnail size.
2. Under the raking studio light, forms are planes and landmarks, not mush; nothing is lumpy noise.
3. Squint: only primary and secondary forms remain, with a clear value pattern.
4. Flip the front view horizontally: proportion and tilt errors pop out.
5. At the final output size, delete detail nobody will see; keep what reads.

Tests: `bash tests/test_check_sculpt.sh` (a clean fixture passes, a broken one fails on scale and a loose vertex).
Worked procedural example: `blender -b --python scripts/procedural_rock.py -- --out rock.blend` (joint-set cuts, corner chips, masked layered displacement, QuadriFlow or Decimate low copy).

## References

| Need | Read |
| --- | --- |
| Blender 5.x brushes, remesh, Dyntopo, Multires, masks, face sets, bake, retopo, sculpting through bpy | `references/blender-sculpt-tools.md` |
| Form hierarchy, heads, bodies, creatures, asymmetry, stylisation, procedural and AI-mesh routes | `references/form-and-anatomy.md` |
| One image to a sculpt: views, registration, screening, staged fitting, IoU and normal-error targets | `references/image-to-sculpt.md` |
| AI high-poly in parts to a baked low poly: Tripo Studio steps, `scripts/bake_ai_mesh.py`, detail normal, roughness | `references/ai-mesh-to-game-ready.md` |
| Skin and surface layers, cloth folds, rocks, cliffs, terrain, bark, hard surface, stamps | `references/surfaces-environment-and-hard-surface.md` |
| Stylised cartoon character sculpt, step by step | `~/.claude/skills/model-characters/references/sculpt-stylized.md` |
| Which detail method is cheapest (texture, displacement, scatter, cards, model) | `~/.claude/skills/3d-generalist/references/assets-and-kitbash.md` |
