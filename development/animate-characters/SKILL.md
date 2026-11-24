---
name: animate-characters
description: "Animate characters, creatures and props in 2D and 3D in any style: the 12 principles, timing and spacing, keys and breakdowns, graph editor curves, cycles, IK or FK, face swaps, frame by frame, cut-out and playblast checks. Use for character animation, walk, run and idle cycles, squash and stretch, Grease Pencil or Krita animation (\"walk cycle\")."
license: MIT
---

# Animate Characters in 2D and 3D

This craft skill owns the motion of a character, creature or prop: poses, timing, curves, cycles and face swaps.
`3d-generalist`, `2d-generalist`, `model-characters` and `use-3d-software` call it.
They keep the look and the order of the whole job. For building the rig, use the `rig-characters` skill.
Read `local.md` next to this file when it exists (machine paths for Krita and OpenToonz).

## When to use

- A character, creature or prop must move with weight, acting or a loop.
- A motion looks stiff, floaty, robotic or "on rails", and you must fix the cause.
- You need a walk, run or idle cycle, a face swap, or a hand-drawn sequence.
- Not for camera moves, NLA layering or Blender recipes: see
  [use-3d-software animation-and-nla](../use-3d-software/references/animation-and-nla.md).

## Ask first

When the user calls this skill directly for a new piece, find out what they want before you make anything. Read the
request, attachments and project files, then ask only about what is still unclear and would change the result:
purpose and platform, format (aspect, length, file type), subject details, look (style, references) and constraints.
Ask at most 4 questions in one round, each with 2 to 4 concrete options and your recommended option first (Claude Code:
`AskUserQuestion`; elsewhere a numbered list where "ok" takes the first options). Restate the goal in 2 or 3 lines,
show the cheapest preview of the look before the expensive step, and compare the result with the goal before you hand
it over. When a generalist skill called this one with a brief, use that brief and do not ask again.

## Core rules

1. Work pose to pose. Block the key poses first, then breakdowns, then in-betweens. Use straight ahead only for fire, smoke and loose masses.
2. Block on Constant (stepped) in 3D and on holds in 2D. Switch to Bezier only after the timing reads.
3. Every action gets an anticipation, a small opposite move 3 to 6 frames before it. Realistic styles keep it small, cartoon styles push it.
4. The head leads every turn and notice by 4 to 6 frames. Never stop all joints on one frame: stagger the stops 3 to 6 frames apart.
5. Attached parts (hair, tail, cloth, ears) lag the main mass by 1 to 3 frames. They overshoot at the stop, about 3 frames later.
6. Spacing makes weight. Put the keys close together near the poses (slow in, slow out) and far apart in the fast middle. A fall is faster than a rise.
7. Limbs travel on arcs. Check them with motion paths in 3D and with a drawn path line in 2D. IK paths need breakdown keys to bend.
8. Squash and stretch conserve volume: stretch along the force, squash across it, and keep the contact frame for 2 frames.
9. Pick the pose by silhouette. Hide the interior and check that the pose still reads. Avoid tangents between outlines.
10. Retime with `S` then `X` (timing only). Plain `S` in the Graph Editor scales the values and warps the pose.
11. A loop needs an identical first and last pose, and the last frame is the one before the first. Otherwise the loop pops.
12. Judge timing only at real speed (Sync to Audio, 24 fps with motion blur or on twos). Play it many times between edits.

## Workflow

1. Plan the action in words: beats, the idea of each pose, the length in seconds. Gather a reference clip when the action is real.
2. Choose the tool and the frame rate. 24 fps with motion blur, 30 fps for games, on twos for hand-drawn or stylized work.
3. Pick IK or FK per shot (see the `cycles-and-locomotion.md` entry). Hide the controls you do not need.
4. Block the key poses on Constant. Check each from front and side in orthographic view.
5. Set the timing: hold frames, anticipation and the spacing. Preview the range (`P`) at real speed.
6. Add breakdowns. Fix arcs and weight shift. Then switch to Bezier or add in-betweens.
7. Add overlap, follow through and secondary action as a separate pass or layer.
8. Add face swaps and blinks, then procedural noise or wiggle on the loose parts.
9. Playblast with overlays, run the checks below, then hand back to the calling skill.

## Routing

| The task is | Read |
| --- | --- |
| The 12 principles, how each works in 2D and 3D, silhouettes, exaggeration, worked jump example | [references/principles.md](references/principles.md) |
| Keys, holds, Dope Sheet, Graph Editor, handle types, interpolation, Stepped, Noise, motion paths, frame rate | [references/timing-and-graph-editor.md](references/timing-and-graph-editor.md) |
| Walk, run and idle cycles, Make Cyclic, foot slide, IK or FK per shot, copy and mirror poses, crowds | [references/cycles-and-locomotion.md](references/cycles-and-locomotion.md) |
| Shape keys, texture face swaps, blinks, mouth shapes, lip sync, wiggle and wind on loose parts | [references/acting-and-faces.md](references/acting-and-faces.md) |
| Frame by frame in Grease Pencil v3 or Krita, onion skin, cut-out rigs, FX frames, export | [references/2d-frame-by-frame-and-cutout.md](references/2d-frame-by-frame-and-cutout.md) |
| 2D-style timing in 3D: twos, threes and fours, stepped `floor(#frame / n)` shaders, line boil, Sketchify, linear loops | [references/stepped-2d-look-in-3d.md](references/stepped-2d-look-in-3d.md) |
| Smears and VFX planes: stepped noise streaks, rain on twos, Grease Pencil splash, shape-key smoke and puffs, flames | [references/smears-and-vfx-planes.md](references/smears-and-vfx-planes.md) |
| Overlap on hair and tails, wind on bones, acting from reference, shot planning, cinematic shot lessons | [references/overlap-acting-and-shot-planning.md](references/overlap-acting-and-shot-planning.md) |
| 2D motion design (After Effects style): hold blocking, easing recipes, overshoot, shape morphs, shape-layer rigs, eye blinks, free-tool routes | [references/motion-design-2d.md](references/motion-design-2d.md) |
| Stylized recipes: ball bounce squash, blocking to Bezier, keying sets, Stop-Mo stepping, clay boil, slotted actions and NLA mixing, mocap retarget, soft body and cloth jiggle, ragdolls, audio-driven keys, Mograph Array motion | [references/stylized-animation-recipes.md](references/stylized-animation-recipes.md) |
| Hands, grip and props: pick up, carry, put down, two-handed holds, weight of a lift, finger posing, grip checklist | `rig-characters` `references/props-grip-and-contact.md` |
| NPR shading, outlines and painted textures for the look | `model-characters` `references/npr-shading-and-painted-look.md` |
| Blender NLA, camera moves, seamless loops, Global Transform, Bake Action | [use-3d-software animation-and-nla](../use-3d-software/references/animation-and-nla.md) |

## Checks

- Scrub frame by frame. Look for pops at cut points, foot slide and joints that freeze on the same frame.
- Turn on motion paths and look at the wrists, feet and head. Fix any straight or kinked path.
- Play the loop twice in a row. The seam must not show.
- Hide the mesh or fill the shape black. The silhouette must show the action.
- Play at real speed with sound. If it feels floaty, shorten the in-betweens. If it feels robotic, offset the stops.
- For a face swap, step through the frames. Each face must change in one frame, with no blend.
- Render a low resolution playblast of the whole shot before any full render.
- Stepped style: the character, shaders, outline boil and effects all use one step size. Check the Dope Sheet for keys on
  every 2 or 3 frames.
