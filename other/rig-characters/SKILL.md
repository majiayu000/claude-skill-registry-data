---
name: rig-characters
description: "Rig characters and props for animation in 2D and 3D: bone naming, Rigify, weights, IK with pole targets, IK/FK switching, face rigs, mechanical rigs, 2D cut-out rigs and export to game engines. Use for rigging a biped, prop or puppet, fixing bad deformation, a face or mouth rig, or exporting a rig to Unity, Godot, three.js or glTF (\"weight paint\", \"rig 2D cut-out\")."
license: MIT
---

# Rig Characters

This skill owns the rigging method: skeleton, skinning, controls, face rigs and engine export. `3d-generalist`, `2d-generalist`,
`model-characters` and `use-3d-software` call it. They own the look and the order of work.

## When to use

- A mesh or a set of drawn parts must move under control, and the rig is not built yet.
- A rig deforms badly: pinched joints, a reversed elbow, a hand that follows the wrong bone.
- A face needs expressions: bones, shape keys or a texture atlas.
- A rigid machine needs joints without a skeleton.
- A rig must work in Unity (Mecanim), Godot, three.js, Crucible or glTF.

Exact Blender button recipes are in `use-3d-software/references/rigging-and-weights.md`. Read it for those steps.
This skill adds the method around them and the other tools.

## Ask first

When the user calls this skill directly for a new piece, find out what they want before you make anything. Read the
request, attachments and project files, then ask only about what is still unclear and would change the result:
purpose and platform, format (aspect, length, file type), subject details, look (style, references) and constraints.
Ask at most 4 questions in one round, each with 2 to 4 concrete options and your recommended option first (Claude Code:
`AskUserQuestion`; elsewhere a numbered list where "ok" takes the first options). Restate the goal in 2 or 3 lines,
show the cheapest preview of the look before the expensive step, and compare the result with the goal before you hand
it over. When a generalist skill called this one with a brief, use that brief and do not ask again.

## Core rules

1. Apply the Mirror modifier and the object scale before you rig. Both sides need real geometry and scale must be 1.
2. Put every joint where the character really bends, inside the mesh. A wrong joint is the main cause of bad deformation.
3. Keep a slight bend in elbows and knees (knees forward, elbows back). IK reads the bend direction from it.
4. Name left bones with a `.L` suffix, build one side, then Symmetrize. Put `IK` in control bone names so search finds them.
5. Test bone roll with a local X rotation on every limb and finger. Do it before IK or Generate.
6. Turn Deform off on every control, IK, pole and root bone before you skin. Only the real skeleton deforms.
7. Clear the parent of IK and pole bones. A leftover parent link breaks the IK chain.
8. Skin with automatic weights first, then fix by hand with low strength. Test by rotating bones, not by reading colours.
9. Never add or delete geometry after shape keys exist. Change the Basis first.
10. Parent rigid accessories (shoes, hair, teeth) to a deform bone, never to a control bone.
11. Use IK for planted contacts and FK for loose drag. Keep both on one rig with a switch.
12. Test a rig that leaves Blender in the target engine with one stock clip before you call it done.

## Workflow

1. Pick the rig type: Rigify biped, custom armature, mechanical (no bones), shape keys only, or 2D cut-out.
2. Prepare the mesh: apply Mirror and scale, put the feet on the ground at the world origin, centre the character.
3. Build the skeleton and fit it. Check roll and left/right names.
4. Add controls: root, IK with pole targets, IK/FK switch, foot roll, and bone collections that hide helpers.
5. Skin: automatic weights, then hard weights for rigid parts, then paint fixes.
6. Add the face rig if the shot needs one.
7. Pose a stress test: a run pose, a fist, arms overhead, a deep knee bend. Fix pinching.
8. Export or hand off. Test in the target engine.

## Routing

| The task is | Read |
| --- | --- |
| Bone naming, meta-rig fitting, Rigify generation, roll, automatic and hard weights, weight fixes | `references/bones-and-weights.md` |
| IK with pole targets, IK/FK choice and switching, snapping, bone collections, ready rigs | `references/ik-fk-and-controls.md` |
| Shape keys, eye and mouth bones, 2D face atlas driven by a bone, blinking | `references/face-rigs.md` |
| A robot arm or machine without bones, a 2D cut-out puppet from Krita layers | `references/mechanical-and-cutout.md` |
| Rig to Unity Mecanim, Godot, three.js, Crucible, glTF | `references/export-to-engines.md` |
| A creature spine with controller bones, bendy bones, IK legs, Damped Track tails, Rigify frog or custom face, wind on bones, Bake Action | `references/creature-and-stylized-rigs.md` |
| Stylized recipes: image-sequence faces, Rigify samples for non-humanoids, rubber-hose and squash rigs, hard-weight toy rigs, ragdoll proxies, eye rigs | `references/stylized-rig-recipes.md` |
| A character holds, picks up, carries, hands over or puts down a prop; two-handed props; grip, weight, fingers; any software | `references/props-grip-and-contact.md` |
| Exact Blender menu steps for any of the above | `use-3d-software/references/rigging-and-weights.md` |

## Checks

- Rotate every limb and finger by 90 degrees. No candy-wrapper twist, no pinched elbow, no mesh left behind.
- Reset the pose (Alt+G, Alt+R, Alt+S in Blender). The mesh returns to the rest shape.
- Mirror a pose. The other side matches, and the pole angles on `.R` are right.
- Move the root and the hips. The whole rig and the legs follow.
- In Weight Paint, only deform bones show weights. Control bones show the mesh pink.
- Shape-key face: set every key to 1 once and nothing explodes. Set all to 0 and the Basis returns.
- Export: load the file in the target engine and play one clip. Watch the feet, the hands and the scale.
