---
vendored_from: https://github.com/PigeonAI-Yang/oneirloom
name: oneirloom-icon-design
description: Design coherent functional UI icon families and distinctive app or product symbols. Adapt existing icon languages, create editable vector assets or requested illustrative icon prompts, and inspect meaning and legibility at the intended size. Reaction stickers use oneirloom-expression-stickers.
triggers:
  - oneirloom-icon-design
  - oneirloom
  - icon
  - design

---

# Design icons for their actual use

Read the [shared interaction contract](../oneirloom/references/interaction-contract.md) before the first substantive response unless its unchanged content is already available. For person prompts, including new images and grid panels, read [person defaults and proportions](../oneirloom/references/person-prompts.md).

Use this method for functional interface icons, icon families, and app or product identifiers. Read the [graphic-design process](../oneirloom-style-design/SKILL.md) for the shared process. The guidance below adds icon decisions within Understand, Observe, Design, production, and review. It does not define another design workflow.

## Establish the icon's job

During Understand, distinguish the requested use before selecting a style or tool.

- A functional UI icon represents an action, object, or state in a small interface context. Resolve each semantic label and the intended placement.
- An app or product symbol identifies one product or service. Resolve the recognizable idea and fixed brand assets before choosing the container or finish.
- A pictogram explains a larger concept and can carry more detail. Use [illustration](../oneirloom-style-illustration/SKILL.md) when that is the actual task. A pictogram is not automatically a suitable small UI icon.
- A reaction sticker communicates a response through character expression, pose, or short copy. Route that task to [oneirloom-expression-stickers](../oneirloom-expression-stickers/SKILL.md).

Carry the requested icon names, meanings, output count, target display sizes, backgrounds, and file requirements from the brief. Resolve states or exact labels only when the task needs them. A request for a downloadable icon set requires individual assets. A contact sheet can accompany the set but cannot replace it.

Preserve supplied logos and brand assets unless the user authorizes their modification. For requested lettering or a lettermark, preserve the literal characters. Add no marketing copy or automatic watermark to the icons.

## Observe the actual family

Inspect supplied family examples at a useful enlargement and at the intended viewing size when available. Record the relations that affect this task: stroke weight, caps and joins, corner language, key shapes, optical mass, centering, fill and negative counters, gaps, viewpoint, and color roles. Confirm which visible features carry the intended meaning. Do not infer hidden geometry or exact dimensions from a low-resolution sample.

An existing family takes precedence over a starter template. With no visual reference, describe a proposed visual language as a design choice. The starter templates contain no inspected image examples. Do not claim that their recipes reproduce an observed reference.

## Design the family and each meaning

Resolve a common construction language and each icon's metaphor together. Keep comparable visual weight and perspective across the family, while allowing different shapes to occupy different bounds. Use guides and key shapes to support consistency. Do not warp the metaphor or cut off meaningful parts to fill a placeholder.

Set dimensions and stroke rules for the current brief. A 24-unit or 32-unit canvas can be appropriate, but neither is a universal default. Likewise, IBM's documented grid and stroke settings apply to IBM's family. Optical correction and pixel alignment depend on the actual target size and renderer.

Read [digital form](../oneirloom-digital-form/SKILL.md) only when the requested icon uses a volume transformation or connected geometry that needs that method. Read [craft construction](../oneirloom-craft-construction/SKILL.md) only for a requested physical craft treatment. Neither replaces the icon's semantic, family, or vector-delivery requirements.

Keep the details that distinguish meaning and remove decoration that disappears at the target size. A filled icon needs readable internal openings as well as a recognizable outer contour. Do not close those openings to gain density. If states are requested, design their differences in the same native language and preserve the base meaning. Do not invent state variants for every asset.

For an app symbol, choose one focused product or brand idea and preserve its recognition through the requested treatment. Separate a container or mask preview from an actual platform export. When platform delivery is requested, verify the current official platform requirements before choosing export sizes, layers, masks, or packaging. The [source notes](references/sources.md) do not establish current platform specifications.

## Select a template and produce

Read the [template index](templates/index.md) only when a recipe helps. Select one template and resolve its relevant slots for the current brief. Use the method directly if none fits.

For original geometric icons that must scale or remain editable, prefer actual vector construction through code or a suitable native design tool. Honor an explicit SVG or code request with SVG code or files and a rendered preview. Construct meaningful paths and shapes. An SVG wrapper around a raster image does not make that image a vector icon.

Raster generation is valid for a requested illustrative app icon, material study, or image prompt. Use confirmed generation capabilities and the requested model adapter when applicable. Do not send every icon task to image generation. A generated raster may be a useful concept but does not satisfy a requested editable vector asset.

Choose `currentColor`, fixed brand colors, or another color arrangement from the actual interface and delivery brief. Keep naming consistent with the requested semantic labels. Deliver the agreed individual files and a concise label-to-file mapping when a set needs one. Do not add scripts, export bundles, or integration code unless the task calls for them.

## Inspect and hand off

Review meaning first, then family consistency at normal viewing size. Inspect requested light and dark contexts, and relevant state variants, when they are part of the intended use. Check optical weight, alignment, open counters, stroke appearance, color roles, and small-size legibility. Enlargement helps diagnose construction but cannot prove normal-size readability.

Open or render actual outputs with available tools. Verify the delivered SVG contains the intended vector geometry when vector output was requested. Check that the number and names of individual files match the brief. A new extension, export receipt, or overview board alone does not prove usable assets.

For prompt-only work, follow the [shared interaction contract](../oneirloom/references/interaction-contract.md): complete Chinese and English prompts for the chosen path, unless another language scope was requested. Keep controls and critique outside the copyable prompt. For a vector production request, deliver actual source and preview rather than only prompts.

State which files and sizes were inspected, and identify unrendered concepts or unverified platform exports. If a tool is unavailable, preserve completed work and report only the dependent gap. Use [result diagnosis](../oneirloom-result-diagnosis/SKILL.md) for a persistent miss, with meaning and the family reference as the acceptance basis.
