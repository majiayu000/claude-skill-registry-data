---
name: game-concept-art
description:
  "Create or revise game concept art, the art direction document, consistent construction views, poses and visual
  targets from saved GameGen preferences before asset production. Changes to saved art preferences go through
  game-bootstrap."
---

# Create production concept art

Read [shared context](../../references/shared-context.md), then load ready project preferences with the shared reader.
Read [concept references](../../references/concept-references.md) and the chosen route in
[providers](../../references/providers.md).

Use `game.title`, `description`, `goal` and `scope` to establish the visual brief. Inspect supplied references and the
saved art direction before generating. Separate silhouette, proportion, palette, material response, lighting, camera and
detail density. Preserve the user's style and original character identity. Do not default every project to chibi
creatures or a particular franchise aesthetic.

This skill owns the document at `art.direction_doc`, the concept reference files and their manifest entries. It does not
edit preferences. When the user changes a saved `art` choice such as style, palette, references, lighting or required
views, the coordinating agent applies that change through `game-bootstrap` first; then regenerate or revise concepts
against the updated preferences.

## Generate a usable reference package

1. Resolve one canonical design using the selected review policy. Present the design at the intended gameplay scale as
   well as a readable close view.
2. Build the view list from `art.required_views`. Derive its neutral construction views, usually front, side and rear,
   from that exact identity. Keep consistent projection, ground line and scale. Add the other side for asymmetry and
   top/underside views when needed to model concealed forms.
3. Add the remaining required views, such as three-quarter and gameplay-camera views, then face/material details,
   expressions and relevant motion key poses. Add a view outside the saved list only when concealed forms need it, and
   record why. Favor individual readable images over crowded sheets. Effects must not hide anatomy.
4. Reconcile differences between generated views. Record the intended construction if a tool changes proportions or
   appendages. Use fixed-camera Blender blockout renders through the
   [local CLI workflow](../../references/blender-cli.md) as reference inputs when stronger view consistency is needed.
5. For 2D, derive only the required directions, pixel density, frame dimensions and grounded pivots. For environments,
   include a modular scale/grid reference and a small playable composition with readable paths and silhouettes.
6. Inspect identity, anatomy, repeated feature counts, negative space, color and camera readability. Correct a named
   mismatch with a targeted edit while preserving accepted details.

Follow the saved provider, actual available model options and budget. For GPT image work, use GPT Image 2.5 through the
existing imagegen skill when selected, and choose the flavor per operation with the
[shared flavor policy](../../references/providers.md#gpt-image-25).

Use SpriteCook for the selected sprite/tiles/UI purpose and its existing workflow skills. Higgsfield requires the
configured need and allowance. A higher-quality setting alone does not guarantee a faithful asset reference.

## Handoff

Save the selected reference files, prompt, input roles, intended model flavor and reason, actual reported model, output
hashes and approval revision in the project manifest. Store the concise visual rules in `art.direction_doc`. Keep images
and long prompts outside the preferences file. Hand asset production a coherent view set with known scale and
requirements. Clearly label these outputs as concepts; later Blender and engine reviews still need to happen.
