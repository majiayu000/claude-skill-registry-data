---
vendored_from: https://github.com/PigeonAI-Yang/oneirloom
name: oneirloom
description: "Oneirloom (织梦师), also called 织梦师Skill or Oneirloom Skill. Explore visual directions across media, then turn visual requests and references into complete image prompts, graphic designs, craft constructions, digital forms, spatial concepts, sticker packs, icon assets, or brand identities. Diagnose results, route illustrated tutorial writing, or package an image and prompt into a 3:4 card. Select only the methods and templates the task needs."
triggers:
  - oneirloom
  - oneirloom

---

# Oneirloom

Oneirloom is the public name of this collection. Treat "织梦师", "织梦师Skill", "Oneirloom", and "Oneirloom Skill" as aliases for this entry. The main technical invocation is `$oneirloom`; capabilities retain the `oneirloom-` namespace.

## Coordinate the current request

1. Read the [shared interaction contract](references/interaction-contract.md) before the first substantive response unless its unchanged content is already available. Identify the actual deliverable and carry confirmed conversation choices. Distinguish prompts, concepts, specifications, and finished usable files. In prompt-only collaboration, approval of a scene or a request to try it continues prompt drafting; it does not change the requested deliverable to image generation.
2. Select only the capabilities the current task needs. When an emotional, memory, or fragmentary idea has no formed drawable scene, read [dream weaving](../oneirloom-dream-weaving/SKILL.md) before choosing a medium. Resolve each exact name through the host catalog, with `../<name>/SKILL.md` as the repository fallback, and read it explicitly. A link does not invoke a skill. Reuse unchanged instructions already read. An unavailable branch blocks only dependent work.
3. Resolve visual intent before model adaptation. For real products, begin with product evidence and the current concept; read product art direction before proposing a creative transformation. For a formed scene whose medium or visual direction remains open, use the optional visual-family index to compare relevant mechanisms. A settled medium goes directly to its method. For reconstruction, read visual analysis and its reconstruction workflow before drafting. Other image prompts lead with 3–5 checkable anchors while preserving all required relations.
4. Add the requested model adapter only when image prompting or generation needs it, after the visual specification. Multiple models share that intent. Unknown models or entries receive portable visual text until capabilities are established. Native vector and document work needs no image-model adapter. Use the selected capability's delivery and inspection procedure.

## Select capabilities by task

| Current task | Read |
| --- | --- |
| Existing image and prompt card | `oneirloom-prompt-card` |
| Illustrated tutorial or article edit | `oneirloom-image-tutorial` |
| Real-product depiction, clear or vague selling brief, or product revision | `oneirloom-product-art-direction` |
| Unformed feelings, memories, fragments, or an unsatisfying concept needing collaborative scene development | `oneirloom-dream-weaving`, then the formed scene's relevant capability |
| Full VI or defined identity extension | `oneirloom-brand-identity`, which coordinates only the requested components |
| Individually usable chat reactions | `oneirloom-expression-stickers` |
| UI icon family, app symbol, or product identifier | `oneirloom-icon-design` |
| Character, wardrobe, multi-view, or expression reference sheet | `oneirloom-character-sheet`; add visual analysis for supplied references |
| Reference reconstruction, unclear relations in a formed scene, or translation of an abstract aesthetic effect | `oneirloom-visual-analysis` |
| Decisive viewpoint, perspective, pose, crop, scale, or occlusion | `oneirloom-camera-composition` |
| Decisive regional color, transparent material, illumination, or atmosphere | `oneirloom-color-light` |
| Photography, lifestyle portrait, or film still | `oneirloom-style-photography` |
| Drawing, painting, print, animation illustration, or collage | `oneirloom-style-illustration` |
| Composed graphic or packaging graphics | `oneirloom-style-design` |
| Physical craft construction such as fuse-bead art or layered paper relief | `oneirloom-craft-construction`; add graphic design only when the deliverable also has a composed layout |
| Digital form, 3D concept render, or identity-to-volume transformation | `oneirloom-digital-form`; add graphic design for a composed layout |
| Fictional product shape or object-form concept | `oneirloom-digital-form`; for a real product, read product art direction first and preserve its supported facts |
| Room, set, or environment whose spatial arrangement is the main decision | `oneirloom-space-conception`, then camera composition for the chosen view |
| Isolated real-product study or product scene | `oneirloom-product-art-direction` and the requested photographic or graphic method |
| Fashion image or outfit series | The requested photographic or illustration method; read fashion styling when outfit coordination or continuity needs it. A wardrobe sheet is optional |
| Clearly adult non-explicit figure art or requested concealment | `oneirloom-figure-art` and the relevant medium |
| Requested Krea 2 or Qwen-Image-2.1 adaptation | `oneirloom-model-krea-2` or `oneirloom-model-qwen-image-2-1` respectively |
| Actual or user-reported result miss | `oneirloom-result-diagnosis`; a routine edit with no reported miss uses the current confirmed prompt and choices |

Use the primary deliverable capability plus its needed medium and conditional analysis, spatial, or lighting support. Let the owner select an optional recipe; no match means composing from the method. Do not reopen settled choices or load an unchanged medium for a local edit. Unformed feelings or fragments go to dream weaving; a formed scene with an open visual direction may use the optional family index. A clear watercolor request goes directly to illustration, and a settled local edit does not restart exploration.

For a formed scene with an open visual direction, cross-medium style exploration, family disambiguation, or an explicit family-level request, the [visual-family index](references/visual-families/index.md) is optional. Read only notes that help compare mechanisms. The ten overlapping lenses do not replace the deliverable owner or choose a medium for the user. A settled treatment proceeds through its owner without an automatic index read.

For person prompts, including new images and grid panels, read [person defaults and proportions](references/person-prompts.md). For requested Oneirloom watermarks, use the approved signature guidance in [prompt cards](../oneirloom-prompt-card/SKILL.md); the icon capability retains its no-automatic-watermark rule.
