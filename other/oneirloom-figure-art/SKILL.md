---
vendored_from: https://github.com/PigeonAI-Yang/oneirloom
name: oneirloom-figure-art
description: Shape non-explicit artistic prompts for clearly adult unclothed figures, including requested concealment; coordinate visible anatomy and view-dependent coverage while leaving medium and style to their own branches.
triggers:
  - oneirloom-figure-art
  - oneirloom
  - figure
  - art

---

# Adult Artistic Figure

Read the [shared interaction contract](../oneirloom/references/interaction-contract.md) before the first substantive response unless its unchanged content is already available. For person prompts, including new images and grid panels, read [person defaults and proportions](../oneirloom/references/person-prompts.md).

成人非露骨艺术人体的方法技能：协调可见解剖与视角相关的遮挡，媒介与风格仍归各自的分支。本技能是判断规则库，按清单检查。

## When to use

Use this branch only for clearly adult subjects and non-explicit artistic or implied nudity. Keep the purpose neutral and artistic, such as a fine-art, classical, or fantasy portrait. Do not use voyeuristic or arousal-focused framing. If adulthood is unclear, do not infer it.

## Method checklist

- Carry forward the user's confirmed anchors and successful details: face visibility, proportions, pose, palette, crop, and medium when established. This branch handles anatomy visibility and concealment; it does not authorize drifting into monochrome, back-only, head-only, or otherwise unrelated compositions unless requested.
- Separate the anatomy the user wants visible from the areas they require concealed. When unclothed figure art is requested, describe the figure as unclothed and preserve the requested visible anatomy; do not solve concealment by turning it into a clothed portrait or hiding the whole figure.
- Give environmental occluders and drapery visible support, such as their attachment to the scene or their resting surface. Floating cloth or two fitted bands around the chest and pelvis do not establish natural scene occlusion and can turn the result into a two-piece outfit. Preserve the distinction between an unclothed figure behind coverage and a figure wearing clothing.
- When the user requires breasts or private areas to be hidden, specify each region and require complete opaque coverage from the selected view, distinct from the rest of the visible unclothed figure. Choose a scene-coherent way to occlude each area, position the occluder against clear body landmarks, and make coverage continuous in the final projection. Check limb gaps, fabric transparency, reflections or mirrors, water or glass, and highlights that could reveal the concealed area. If the requested pose and view cannot maintain coverage, adjust their spatial relationship while preserving the confirmed anchors.
- Verify that the occluder's upper boundary and width actually span the concealed anatomy in the chosen projection. In a standing frontal view, crossed knees or shins do not cover the pubic region above them. Crossed arms also require enough width and placement to cover the requested breast area, rather than only isolated points. Do not label these poses fully covered without a spatially credible explanation; choose a different pose or coherent environmental coverage when necessary.
- Avoid repeating a default prop or adding objects without a scene reason. Honor a no-held-object constraint when the user gives one; do not impose that constraint universally.

## Coordinate with

Coordinate with `oneirloom-visual-analysis` for references or ambiguous spatial intent, `oneirloom-camera-composition` when viewpoint, crop, or occlusion geometry matters, and the relevant color/light and medium branch for aesthetics. The chosen photography, illustration, or design branch remains responsible for its medium and style.

## Output and handoff

When generated images are available, inspect both the requested visual anchors and the actual coverage, including gaps and reflective surfaces. For a miss, use `oneirloom-result-diagnosis` to preserve successful details and correct the main deviation. An unrendered prompt is untested; do not guarantee coverage from wording alone.
