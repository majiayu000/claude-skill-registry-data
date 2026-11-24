---
name: draw-and-paint-art
description: "Draw and paint figures, characters, light and colour in any style with Krita, Blender Grease Pencil or code, and check a figure or character sheet for anatomy and pose errors. Use for gesture, construction, anatomy, foreshortening, painting light and form, hand-painted textures and turnaround sheets (\"anatomy\", \"Krita\")."
license: MIT
---

# Draw and Paint Art

This craft skill owns 2D drawing and digital painting: gesture, construction, anatomy, light, colour, Krita and Grease Pencil.
`2d-generalist`, `3d-generalist`, `model-characters` and `use-3d-software` call it. They keep the look and the order of work.

Read `local.md` next to this file first when it exists (machine paths and local rules).

## When to use

- You draw or paint a figure, a character, a prop or a painted texture.
- You build a turnaround, pose sheet or style sheet that a 3D artist will model from.
- You review a figure or sheet for anatomy, proportion, pose and silhouette errors.
- You set up Krita or Blender Grease Pencil for drawing.

## Ask first

When the user calls this skill directly for a new piece, find out what they want before you make anything. Read the
request, attachments and project files, then ask only about what is still unclear and would change the result:
purpose and platform, format (aspect, length, file type), subject details, look (style, references) and constraints.
Ask at most 4 questions in one round, each with 2 to 4 concrete options and your recommended option first (Claude Code:
`AskUserQuestion`; elsewhere a numbered list where "ok" takes the first options). Restate the goal in 2 or 3 lines,
show the cheapest preview of the look before the expensive step, and compare the result with the goal before you hand
it over. When a generalist skill called this one with a brief, use that brief and do not ask again.

## Core rules

1. Start with flow. Draw one line of action (a long S or C curve through neck and spine) before any shape.
2. Build every form from simple volumes. Use two blocks for ribcage and pelvis, cylinders for limbs, a circle at each joint and a box or ellipse for the head.
3. Draw through the forms. Draw the hidden edges so the parts do not contradict each other.
4. Work rough to clean. Lower the sketch layer opacity, trace once or twice with a darker line, and ink last.
5. Tilt the ribcage and pelvis against each other for contrapposto. Check head size against the ribcage.
6. Parts that come toward the viewer get bigger. A limb that tapers toward a joint can shrink as it comes forward.
7. Light has one direction. Paint in order: core shadow, light side, highlight, reflected light (lighter than the core shadow, darker than the lit side), cast shadow.
8. Paint values first in grayscale. Add colour with Color layers, Overlay and a Gradient Map, and keep the colours in value order.
9. Make the front line thicker where two shapes overlap, and avoid tangents between outlines.
10. Check the silhouette and the negative space. A strong silhouette is the goal in any style.
11. Shape language sets the feeling: circle is friendly, square is solid, triangle is aggressive. This holds for any style.
12. Flip the canvas often. A mirrored view shows errors that you stopped seeing.

## Workflow

1. Name the style and the use (concept, texture, sheet, final art). Pick the reference (3D pose viewer, photo, source model).
2. Draw the gesture and line of action, then the block-in (two blocks, limbs, joints, head).
3. Check proportion and pose on the block-in before adding anatomy or detail.
4. Add anatomy and surface forms, then the clean line pass with varied line weight.
5. Paint values in grayscale, then colour.
6. For 3D, export the sheet or texture and hand it to `model-characters` or `use-3d-software`.
7. Run the checks below.

## Routing

| The task is | Read |
| --- | --- |
| Gesture, line of action, construction, poses from reference, line weight | references/gesture-and-construction.md |
| Anatomy of torso, arm, leg, hand, foot, head, foreshortening, proportion checks | references/anatomy-and-foreshortening.md |
| Painting light on a form, colouring, painterly texture, portrait workflow | references/light-form-and-colour.md |
| Krita menus, dockers, brushes, layers, blending modes, Alpha Lock, transform | references/krita-and-tools.md |
| Grease Pencil v3 in Blender: drawing, layers, fills, Line Art, 2D over 3D | references/grease-pencil-drawing.md |
| Turnaround or style sheets, cut-out parts, painting textures for 3D | references/character-sheets-for-3d.md |
| Noticing, detail comparison, grayscale value check, final attack checklist, composition and colour variety | references/noticing-and-design-lessons.md |
| Paint over a Blender render, fake depth with paint | references/light-form-and-colour.md |
| Illustration stage order: sketch, sculpt, pose, props, light, paint-over | references/illustration-process-2d-3d.md |

For UV unwrap, seams, Texture Paint and rigging steps, use `model-characters` and `use-3d-software`. Do not copy those steps here.

## Checks

- Hide the sketch layer. The pose must still read from the silhouette alone.
- Flip the canvas horizontally and squint. Fix any lean, wrong head size or uneven shoulders.
- Compare head size with the ribcage, and compare limb lengths on both sides.
- Make a grayscale copy. The value order (dark, mid, light) must show the form and the light direction.
- Check each overlap and tangent in the line art.
- For a character sheet, overlay the views at the same scale. Heights, joints and key landmarks must line up across front, side and back.
- Save the file with layers (.kra) next to the flat export.
- Run the final attack checklist in `references/noticing-and-design-lessons.md` before you hand a piece over.
