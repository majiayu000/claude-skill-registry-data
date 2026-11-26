---
vendored_from: https://github.com/PigeonAI-Yang/oneirloom
name: oneirloom-style-illustration
description: Compose watercolor, print, comic, animation, concept-art, folkloric narrative, and paper-collage prompts through visible linework, color layers, texture, and spatial structure. Select indexed presets for decorative rainy-night prints, halftone portrait cutouts, or zhiguai narrative illustrations.
triggers:
  - oneirloom-style-illustration
  - oneirloom
  - style
  - illustration

---

# Illustration and painting

Read the [shared interaction contract](../oneirloom/references/interaction-contract.md) before the first substantive response unless its unchanged content is already available. For person prompts, including new images and grid panels, read [person defaults and proportions](../oneirloom/references/person-prompts.md).

绘画与插画类提示词的方法技能：先定媒介与画面结构，再写线、纹理、色彩层与主体背景关系。本技能是判断规则库，按清单检查；具体风格配方在 templates。

## When to use

- Watercolor, print, comic, animation, concept-art, folkloric narrative, or paper-collage prompts
- A specific preset with an indexed template, such as a decorative rainy-night print, halftone portrait cutout, or zhiguai narrative illustration

## Method checklist

When illustration is used in a poster, cover, editorial layout, infographic, or composed ad, read the [graphic-design process](../oneirloom-style-design/SKILL.md) before adapting a recipe. It owns the brief, layout, mechanism transfer, and review order; this method supplies linework, medium, texture, and color-layer decisions. Preserve the intended crop, relative areas, and overlap when changing medium. Illustration without a graphic-layout task keeps the checklist below.

- Establish the medium and image structure, then specify lines and edges, marks and texture, color layers, the role of paper or canvas, and subject/background relationships.
- The same style name can describe different techniques; specify the visible result.
- For watercolor streets, describe light pencil structure, transparent washes spreading into damp paper, and paper-white window edges.
- For comics, prioritize gaze, action direction, framing continuity, and panel reading order.
- For concept art, prioritize shape language, scale references, and atmosphere.
- Introduce photographic imaging terms only for an expressly mixed medium.

## Templates and references

- Read the [illustration styles](references/styles.md) only to select an unresolved medium or distinguish a needed technique. A fully specified medium uses the checklist without an automatic catalogue read.
- For cross-medium style exploration, family disambiguation, or an explicit family-level request, consult the [visual-family index](../oneirloom/references/visual-families/index.md) and only the relevant family note; use this method for the illustrative treatment.
- A clear watercolor or other settled medium goes directly through this checklist. Read [craft construction](../oneirloom-craft-construction/SKILL.md) only when physical paper layers, joins, or supports define the requested object. Read [digital form](../oneirloom-digital-form/SKILL.md) only when a digital shape transformation is a main decision. For a still image whose event staging needs separate planning, use the [still-frame staging reference](../oneirloom-style-photography/references/still-frame-staging.md); keep illustration responsible for its marks and medium.
- For a specific preset, read the [template index](templates/index.md), then the matching template only. Match defining visual relations rather than one color or weather word. Use the method above if nothing fits.
- Preserve user and source-image details when adapting slots, and inspect example images before describing their results. A sample image is not automatically a generation input.

## Output and handoff

Deliver the illustration description integrated into the active task's complete prompt. Composition and color relations follow `oneirloom-camera-composition` and `oneirloom-color-light` when they are loaded; reference inspection follows `oneirloom-visual-analysis`. When a generated result misses the intended illustration, hand off to `oneirloom-result-diagnosis`.
