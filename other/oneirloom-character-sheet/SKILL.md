---
vendored_from: https://github.com/PigeonAI-Yang/oneirloom
name: oneirloom-character-sheet
description: Design character sheets, wardrobe sheets, multi-view identity anchors, and production or expression cards. Select indexed wardrobe, four-view plus four-expression, or three-view templates when their layout fits; ordinary single-image reconstruction belongs to visual analysis.
triggers:
  - oneirloom-character-sheet
  - oneirloom
  - character
  - sheet

---

# Character sheets

Read the [shared interaction contract](../oneirloom/references/interaction-contract.md) before the first substantive response unless its unchanged content is already available. For person prompts, including new images and grid panels, read [person defaults and proportions](../oneirloom/references/person-prompts.md).

角色设定类提示词的方法技能：身份锚点、版式选择与跨视角一致性。具体版式配方在 templates。

## When to use

- Character sheets, wardrobe sheets, multi-view identity anchors, and production or expression cards
- A requested wardrobe sheet, 4+4 card, or three-view card whose layout matches an indexed template
- Ordinary single-image reconstruction belongs to `oneirloom-visual-analysis`, not here
- An expression reference card records identity and expression range for production. For individually usable chat reactions or a sticker pack, use [expression stickers](../oneirloom-expression-stickers/SKILL.md). Reuse an existing identity reference; a sticker request does not require a new character sheet.

## Workflow

1. Establish identity. Separate user settings, visible reference facts, and necessary design inferences. Use `oneirloom-visual-analysis` when a reference is supplied. Unseen features are not observed facts; add backstory or inferred props only when requested. Choose a small set of stable identity anchors, such as silhouette, face structure, hairstyle, regional colors, or distinctive clothing. An occupation or accessory does not establish additional props. Across views, keep those anchors stable while changing only the intended pose, expression, and angle. Identify any necessary inference that materially changes the character.
2. Choose the layout. Let the main image establish identity before adding supporting information. Select views and details for the intended drawing, modeling, animation, or presentation task. Keep structural views in the same base outfit unless variation is requested. Expressions, gestures, silhouettes, palettes, material details, and labels belong only when useful. Names, age, and personality come from the user or authorized design work.
   For a requested wardrobe sheet, 4+4 card, or three-view card, read the [template index](templates/index.md), then the matching template. Match its panel count, hierarchy, and purpose; otherwise design the layout from the method above. Template-specific equal panels take precedence over the general main-image hierarchy when explicitly selected. For a realistic wardrobe conversion, add the photography method and preserve clothing construction while translating drawn faces and materials into natural photographic proportions.
   When outfit coordination or garment continuity needs reusable guidance, read [fashion styling](references/fashion-styling.md). It can support a single fashion image without requiring a sheet; observed garment facts in reconstruction remain with visual analysis.
   Resolve every delivered slot from user settings, visible facts, or an applicable router default. Omit optional unknown details; ask only if a missing detail changes the requested design. Retain a panel-specific prop only when specified or visible, otherwise remove its whole sentence. Keep unknown structure open rather than inventing it to complete a template.
3. Compose. Describe identity anchors, required views, shared clothing, medium, lighting, and layout as positive visible relations. Keep one character consistent across views. Load medium, camera, lighting, and model methods only as needed.

## Output and handoff

Follow the shared interaction contract and keep controls and reference-image inputs outside the prompt. Text alone does not guarantee cross-view identity. For strict continuity, use character references, editing, or iteration only through a confirmed entry. Keep production guidance outside the prompt; if exact labels matter, propose editable typesetting after generation. Explain inference or uncertainty when the user needs it; otherwise deliver the requested prompt. When a generated result misses identity or layout, hand off to `oneirloom-result-diagnosis`.

Method inspiration: <https://x.com/leo_xiaolei/status/2102013053084545433>. The identity and layout method was independently organized rather than copied from the source template.
