---
vendored_from: https://github.com/PigeonAI-Yang/oneirloom
name: oneirloom-digital-form
description: Shape or transform a digital visual subject when silhouette, volume, repetition, deformation, connections, or composite layers define the result. Use for digital-native forms and 3D concept renders.
triggers:
  - oneirloom-digital-form
  - oneirloom
  - digital
  - form

---

# Digital form (数字造型)

Read the [shared interaction contract](../oneirloom/references/interaction-contract.md) before the first substantive response unless its unchanged content is already available. For person-based subjects, including a person transformed into a figure, read [person defaults and proportions](../oneirloom/references/person-prompts.md).

Use this method when a digital shape or its transformation is the main decision. It covers visual descriptions and concept renders. A render is not an editable 3D model. For a native model request, confirm that actual modeling tools and files are available before promising the artifact.

## Shape the form

1. Identify the subject, its fixed identity or product facts, the requested transformation, and the requested output type. Assign each supplied reference a role supported by the chosen entry.
2. Resolve the silhouette and overall scale before surface detail. Choose a discrete form, a continuous form, or a clear transition between them.
3. Define how repeated parts align and vary, how connected parts meet, and which layers sit in front. Bound deformation with the features or proportions that must survive.
4. Read [form and transformation mechanisms](references/form-and-transformation.md) for 3D structure and identity-to-volume examples. Use [material response](../oneirloom-color-light/references/material-response.md) for roughness, transparency, light, and reflection. [Camera composition](../oneirloom-camera-composition/SKILL.md) owns viewpoint and projection. [Graphic design](../oneirloom-style-design/SKILL.md) owns type and page layout.

For a requested sculptural product variant, optionally consult the [template index](templates/index.md).

For an existing product, preserve its known geometry and facts. A fictional product concept may introduce visual choices, but label them as concept choices rather than product specifications.

## Correct a form miss

If a form looks flat or a transformation loses identity, revise the silhouette and one defining volume or connection first. Keep the accepted material, composition, and other constraints fixed.

## Deliver the requested result

For a prompt request, return a complete prompt under the shared contract. For a concept brief, identify the visible form, transformation rule, part relationships, and output limit. State whether you produced a render or an actual editable file, and what remains unverified.
