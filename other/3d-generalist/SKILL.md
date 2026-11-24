---
name: 3d-generalist
description: "3D generalist studio for creators: source and kitbash scanned assets, build or rig characters, dress worlds and perspective cutaways, animate character acting, light and shoot, sync narration and foley, and pass automated QA gates across Blender, three.js and Crucible. Use for 3D Shorts, explainers, story animations, cutaway builds, 3D worlds or character animation (\"3d generalist\", \"3D shorts\", \"cutaway 3D\")."
license: MIT
---

# 3D Generalist

Act as a complete 3D creative studio for content creators. Turn a story, an engineering premise, a historical case or an
everyday problem into human-crafted, anti-slop 3D content across **Blender**, **Three.js** and **Crucible**: vertical Shorts,
cutaway build films, 3D storytelling videos, interactive scenes and hero renders.

Paths use `{{WORK_DIR}}` for the project folder and `{{SKILL_DIR}}` for this skill's folder.

## Choose the mode and load only the references it needs

| Mode | What it makes | Read first |
|---|---|---|
| `cutaway` | A 60 s 3D perspective cutaway Short where one simple thing is built piece by piece through problem-and-fix rounds | `references/shorts-storytelling.md`, `references/worlds-and-cutaways.md`, `references/acting-and-motion.md`, `references/qa-and-gates.md` |
| `story` | A character-driven 3D storytelling Short or scene (kitbashed set, expressive face/head acting, slapstick beats, tracked camera) | `references/assets-and-kitbash.md`, `references/characters-and-rigs.md`, `references/acting-and-motion.md`, `references/camera-and-lighting.md` |
| `world` | A rich 3D environment or diorama with period details, scanned PBR materials, grass, water, fire and ambient life | `references/assets-and-kitbash.md`, `references/worlds-and-cutaways.md`, `references/camera-and-lighting.md`; shown as render, then clay model, then render: `references/clay-reveal.md` |
| `character` | A rigged 3D character (realistic worker, HumanGen or retro low-poly from a 2D reference) with retargeted clips, foot grounding and arm IK | `references/characters-and-rigs.md`, `references/acting-and-motion.md`, `../model-characters/SKILL.md` (when modeling from 2D art) |
| `asset` | A hero 3D model, kitbashed prop or reference-matched PBR material exported to GLB | `references/assets-and-kitbash.md` |

For any step done in Blender (geometry nodes, shaders, rigging, weight paint, NLA, bpy), load the `use-3d-software` skill for the exact nodes and current 5.x names. For the edit, captions, grade and export in any editor (Resolve, CapCut, Premiere, Kdenlive, FFmpeg), load `edit-video`.
Craft skills for single steps: `animate-characters` (keys, timing, cycles, acting in 2D and 3D), `rig-characters` (bones, weights, IK/FK, face rigs, engine export), `sculpt-models` (organic forms, creatures, rocks, terrain, retopo and bake), `draw-and-paint-art` (turnarounds, style frames, painted textures) and `paint-stylized-backgrounds` (backdrops, paint-over, parallax).
**Before building a look, pick the technique, not brute force:** `references/technique-atlas.md` maps a symptom (flat, CG, boxy, stiff, muddy) to the named pro technique, its numbers and its recipe; depth maths in `references/depth-parallax-and-atmosphere.md`. Machine paths (Krita, OpenToonz, Blender): `local.md` next to this file when it exists.

## Order of work: the production spine

Run the eight steps of `references/pipeline-spine.md` in order, in every mode. Each step writes its file into
`{{WORK_DIR}}` and its line under `## Progress` in `brief.md`; start a step only from the files of the one above it.
The user sees the work three times: the choice at step 4 (prep sheet, sketch and options), a WIP demo of the
first finished shot at step 6 (sent without waiting), and the preview at step 8. After the preview the user's
answer picks the next round: fix, continue in a direction, or "you decide" free creative mode (spine, last section). The spine says
which steps shrink per mode.

| Step | Writes | 3D rules for the step |
|---|---|---|
| 1. Brief | `brief.md` | `references/intent-brief.md`: five slots, at most 4 questions, then go |
| 2. Reference | `refs/`, `refs/NOTES.md` | two views per hero subject, real footage for place, light and weather; real CC0 / CC BY assets before primitives: `references/assets-and-kitbash.md` |
| 3. Script and beats | `script.md`, beat table, scratch voice, cue list | hook at 0 to 3 s with the picture already moving, 5 to 7 `But <failure> -> So <fix>` rounds, a flip, a stress test, a closer, sources on top: `references/shorts-storytelling.md` |
| 4. Prep and look gate | `plan.md` (sketch, tools checked, resources downloaded), style frames A/B/C, grey blockout or animatic with real cameras, then `LOOK.md`, `cameras.json` | the user picks; `references/technique-atlas.md` picks the technique, `references/camera-and-lighting.md` the light, `references/clay-reveal.md` the clay pass |
| 5. Assets and check | `assets/`, `CREDITS.md`, measured bounds | fit on real vertex bounds (`Box3.setFromObject(model, true)`), scale the world to the character, no clipping at shot distance: `references/assets-and-kitbash.md`, `references/characters-and-rigs.md`; broken, heavy or UV-less meshes: `use-3d-software` `scripts/mesh_prep.py` (repair, LOD, gate) |
| 6. Build and animate | shots, WIP demo after the first, `checks.md` | sub-phases 6a layout to 6i grade, each closed by its gate (`references/pipeline-spine.md` step 6); one continuous dressed set with ambient life, cutaway by section plane: `references/worlds-and-cutaways.md`; head leads turns 4 to 6 frames, staggered stops, anticipation, physics baked so every frame is `f(t)`: `references/acting-and-motion.md`; under 1 hard cut per 10 s, camera keys 5 to 8 frames apart, spine fill light, DoF on the subject, 6-subframe 180-degree blur, then bloom, vignette and grain as `LOOK.md` sets them: `references/camera-and-lighting.md`; drawn FX: `references/hybrid-2d-3d-fx.md` |
| 7. Sound | final voice, SFX, music, mix | `design-sound`: tail silences over 0.12 s trimmed, one-word captions within ±0.05 s, a soft real SFX for every visible event, -14 LUFS |
| 8. QA, preview, final | gate report, 540p preview with sound | every gate in `references/qa-and-gates.md` (contact and slip: `scripts/check_contact_and_slip.mjs`; Blender frame fill and floating props: `scripts/blender_frame_audit.py`; Crucible sets: gate 15 base review; look match: `scripts/compare_look.py`; sheets: `scripts/contact-sheet.sh`), then the user approves the preview before the full render |

## Hard anti-slop rules

- **Nothing floats, ever:** every foot, knee, stone, prop and structure sits within 1 to 2 cm of the real mesh surface
  under it, with visible support in day or night shots.
- **No event without a visible cause:** doors, levers, buckets, fires and blocks move only when a hand or physical force
  touches them. Hands sit within 3 cm of the gripped surface with low, natural elbows.
- **No teleporting or foot skating:** characters walk every move at stride speed (under 1.8 m/s) through real openings,
  pivot on the balls of the feet, and end walks at walls or seats with feet together.
- **Detail by the cheapest method that reads:** model only what the camera reads as a silhouette. Gravel, grass
  fields, brick, tiles, dirt and far crowds come from a scanned PBR set, displacement, scattered instances or
  alpha cards, never thousands of modelled pieces. Ladder and examples:
  `references/assets-and-kitbash.md`, "Detail ladder".
- **Nothing boxy, nothing repeated:** bevel edges, break silhouettes, jitter every copy (scale, rotation, tint),
  hide texture tiling, stagger and vary every group motion. Rules:
  `references/assets-and-kitbash.md`, "Variation and imperfection".
- **Clean enters and exits:** nothing pops on or vanishes in 1 frame. Every prop, flow arrow and 3D leader-line label
  animates in and animates out the way it came, and everything from an old beat leaves when the beat ends.
