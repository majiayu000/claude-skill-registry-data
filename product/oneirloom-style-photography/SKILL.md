---
vendored_from: https://github.com/PigeonAI-Yang/oneirloom
name: oneirloom-style-photography
description: Compose realistic photography, lifestyle and fashion portraits, product photographs, and film-still prompts. Select indexed scene templates for requests such as crouching selfies or indoor full-length portraits.
triggers:
  - oneirloom-style-photography
  - oneirloom
  - style
  - photography

---

# Photography

Read the [shared interaction contract](../oneirloom/references/interaction-contract.md) before the first substantive response unless its unchanged content is already available. For person prompts, including new images and grid panels, read [person defaults and proportions](../oneirloom/references/person-prompts.md).

写实摄影类提示词的方法技能：组织主体与动作、空间关系、光色与成像质感。本技能是判断规则库，按清单检查；具体场景配方在 templates。

## When to use

- Realistic photography, lifestyle and fashion portraits, product photographs, or film-still prompts
- A concrete reusable scene or pose with an indexed template, such as a crouching selfie or an indoor full-length portrait

## Method checklist

- Establish the whole frame first: setting, camera position and distance, primary masses, subject placement and scale, crop, and depth. Then describe the subject and action, regional light and color, and visible materials and imaging texture.
- For environment-led scenes, give the room or landscape a concrete layout and define the complete subject silhouette relative to the frame. Keep camera distance and foreground scale compatible with that occupancy; low camera height does not require close subject distance or enlarged foreground limbs.
- For realistic or reference-based images, ground details in the brief: describe relevant objects, viewpoint and occlusion, the subject's action and contact with nearby objects, and garment drape or tension only when supported.
- Match depth of field and background clarity to the reference or intended photograph rather than adding generic blur.
- Describe coherent lighting through supported source direction, relative key and fill, and a few decisive highlights and shadows across the subject and surroundings.
- Describe the visual result rather than assumed equipment. Break cinematic style into narrative context, framing, light, and color.
- Use candid action and expression only when the brief calls for a candid image, and keep stage posing as posed.
- For portraits, control the relative positions of the face, shoulders, limbs, and background. For real products, read [product art direction](../oneirloom-product-art-direction/SKILL.md). Preserve supported materials and marks; complete silhouettes apply when the catalog brief calls for them, while agreed creative crops follow the current design.
- Express film texture through useful visible effects such as soft highlights, grain, or a subtle color cast. Do not impose shallow depth of field, film treatment, resolution claims, or camera gear on every request.
- For lifestyle and beauty selfies, default to loose, environment-dominant framing that keeps the setting recognizable around the subject. Follow a close-up or tight crop only when the user asks for it or the reference requires it.
- Before returning, check that framing, perspective, joint states, support, and object contacts can coexist in one view. Describe visible parts and occlusions consistently; a toe hidden inside a closed shoe is not a visible toe. Keep only the pose relations needed for the accepted action.

## Templates and references

- Read the [photography styles](references/styles.md) only to select an unresolved medium or distinguish a needed technique. A fully specified medium uses the checklist without an automatic catalogue read. Choose one primary style and add explicitly requested mixed features.
- For cross-medium style exploration, family disambiguation, or an explicit family-level request, consult the [visual-family index](../oneirloom/references/visual-families/index.md) and only the relevant family note; use this method for the photographic treatment.
- For a concrete reusable scene or pose, read the [template index](templates/index.md), then only the matching template. Keep the template's defining visual relations and replace its adjustable details from the brief. When none fits, compose from the method above.
- For a film-like still whose event, eyelines, staging, depth, or light narrative needs explicit planning, read [still-frame staging](references/still-frame-staging.md). This reference concerns a still image, not video production.
- For a single fashion image or outfit series with unresolved styling or identity-continuity choices, read the [fashion styling reference](../oneirloom-character-sheet/references/fashion-styling.md); a wardrobe sheet is optional. In reconstruction, observed garment facts remain with [visual analysis](../oneirloom-visual-analysis/SKILL.md).
- Example images illustrate their recorded prompts; inspect them before making visual claims, and use them as generation inputs only when that reference role is requested.

## Output and handoff

Deliver the photographic description integrated into the active task's complete prompt. Viewpoint, crop, and lighting relations follow `oneirloom-camera-composition` and `oneirloom-color-light` when they are loaded; reference inspection follows `oneirloom-visual-analysis`. When a generated result misses the photographic intent, hand off to `oneirloom-result-diagnosis`.
