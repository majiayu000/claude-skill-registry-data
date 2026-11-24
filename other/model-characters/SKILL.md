---
name: model-characters
description: "Model 3D characters from a 2D image, turnaround, sketch or idea in any style: low-poly (PS1, chibi, anime), stylized sculpt, clean quad base mesh, and realistic humans from generators and scans, then hand off to rigging, texturing and animation. Works in Blender, three.js, Crucible, Godot, Unity and Unreal. Use for \"model a character\", \"3D character from this drawing\", \"low poly character\", \"base mesh\"."
license: MIT
---

# Model 3D Characters
Paths use `{{WORK_DIR}}` for the project folder and `{{SKILL_DIR}}` for this skill's folder.

If `local.md` or `references/local.md` exists, read it first for local paths and machine rules.

A craft skill. It turns a reference (drawing, turnaround, photo, text idea) into a 3D character in the style the user
wants. Low poly is one route, not the default. The generalist skills (`3d-generalist`, `2d-generalist`) decide the
story and the shot. This skill decides how the character is built. Tool-specific steps live in `use-3d-software`.

## Ask first

When the user calls this skill directly for a new piece, find out what they want before you make anything. Read the
request, attachments and project files, then ask only about what is still unclear and would change the result:
purpose and platform, format (game asset, film, still, print), subject details, look (style, references) and
constraints (triangle budget, engine, deadline). Ask at most 4 questions in one round, each with 2 to 4 concrete
options and your recommended option first (Claude Code: `AskUserQuestion`; elsewhere a numbered list where "ok" takes
the first options). Restate the goal in 2 or 3 lines, show the cheapest preview of the look (a blockout still or a
turnaround grey render) before the expensive step, and compare the result with the goal before you hand it over.
When a generalist skill called this one with a brief, use that brief and do not ask again.

## Pick the route

| The character should be | Route | Read |
|---|---|---|
| Low poly: PS1, N64, chibi, anime, mascot, painterly, under about 2k triangles | Low-poly | `references/style-presets.md`, then `references/low-poly-route.md` |
| Stylized and smooth: cartoon, Pixar-like, figurine, toy, collectible | Sculpt | `references/sculpt-stylized.md`, then retopo by the base-mesh route; anatomy, creatures, surface detail, bake and the silhouette check: the `sculpt-models` skill |
| Clean quads for subdivision, a game LOD or a sculpt base | Base mesh | `references/base-mesh-and-box-modeling.md` |
| Realistic human or creature | Generate or source, then adapt | `3d-generalist` `references/characters-and-rigs.md` (generators, scans, Mixamo, retargeting); for close-ups generate in parts and bake: `sculpt-models` `references/ai-mesh-to-game-ready.md` |
| Anime-semireal, painted or manga character, finished by painting and rendered in EEVEE | Painted | `references/stylized-character-process.md` (build order, head, body, hair), then `references/npr-shading-and-painted-look.md` |
| Toon shader, key and rim light, Solidify outline, painted mask layers or hatching on any model | Shading | `references/npr-shading-and-painted-look.md` (shared with the background and animation skills) |
| An existing model to restyle | Adapt | Keep the rig if it has one. Repaint by `uv-and-texturing.md`, reshape by the sculpt route |

Prefer a licence-clear base (CC0 or CC BY scans, generator output, an open base mesh) over modelling a realistic
human from nothing. Credit it.

## Steps for every route

1. **Measure the reference.** For a turnaround or front view, run
   `uv run --no-project {{SKILL_DIR}}/scripts/read_character_ref.py ref.png --height 1.70 --out cal`.
   It gives head count, joint heights, width and depth profiles and a colour palette. For a single sketch, set the
   height and the head count by hand and write them down.
2. **Block out** the silhouette in large parts at the measured heights. Check front, side and three-quarter views
   against the reference before any detail. Read `references/head-and-face.md` before the head.
3. **Build the route.** Follow the route file. Keep scale applied, mirror on the centre line, and parts separate
   where clothing or hair makes a step in the silhouette.
4. **Topology for motion.** Add loops at the knees, elbows, shoulders, mouth and eyes when the character will bend.
   A sculpt that must animate is retopologized or decimated first.
5. **UV and texture.** `references/uv-and-texturing.md` for atlases, unlit colour and ramps. Hand-painted and
   stylized painting craft is in `draw-and-paint-art`.
6. **Rig and animate.** Hand off to `rig-characters` and `animate-characters`. The short low-poly rig notes are in
   `references/rigging-and-animation.md`.
7. **Check.** Run `uv run --no-project {{SKILL_DIR}}/scripts/check_character.py character.glb --max-tris <budget>`
   on the export, then render a turnaround still and compare it with the reference side by side. A static mesh
   that was repaired, remeshed or decimated also passes `use-3d-software` `scripts/mesh_prep.py compare` against its source.

## More references

- `references/modeling-and-topology.md`: part-by-part low-poly recipes in Blender, three.js and Crucible.
- `references/more-build-methods.md`: Wind Waker style head, cylinder bodies, clothes as shells, hats, face atlas.
- `references/npr-shading-and-painted-look.md`: toon shader, two-sun rim rig, outlines, painted layers, bake.
- `references/stylized-character-process.md`: painted character build order, head, hands, hair, design lessons.
- `references/stylized-modeling-and-texture-painting.md`: cute cartoon builds from a subdivided cube or round cube, clothes as shells, curve tubes, metaball hair, face discs, round chibi bodies and loose-edge faces, carved Boolean faces, topology fixes, texture-paint layers, VDM brushes.
- `references/faults.md`: geometry, UV, rig and animation faults and their fixes.
- `use-3d-software`: the exact steps per tool (Blender sculpt and modifiers, export to three.js, Godot, Unity, Unreal).

## Hard rules

- No box head and no flat face plate. The face has a nose, brow and cheek steps in the side view.
- UV before texture. Never project at a harsh camera angle.
- No internal or coplanar faces. Delete caps inside open cylinders and along mirror seams.
- Skinned vertices have normalized weights (sum 1.0, at most 4 influences for engines).
- Bend knees and elbows slightly in the rest pose when the rig uses IK.
- Stepped (`Constant`) keys on UV-offset face controllers.
- Run `uv run --no-project {{SKILL_DIR}}/scripts/test_character_skill.py` after changing any script in `scripts/`.

