---
name: dircreative-visual-bible
description: Define visual continuity for characters, environments, props, wardrobe, lighting, palette, and texture.
---

# Visual Bible

## Required Knowledge

Read only the reference needed for the active task, not this entire list.
The root v2 route owns scope and authorization; legacy records do not add gates.

- `docs/film-preproduction/chat-co-creation-interface.md`
- `docs/film-preproduction/chat-inline-visualization-interface.md`
- `docs/film-preproduction/schemas/visual-bible.yaml`
- `docs/film-preproduction/research/storyboard-reference-analysis.md`
- `docs/film-preproduction/research/image-prompt-style-system.md`

## Inputs

- shot list
- asset requirements
- blocking plan

## Outputs

- visual bible
- continuity locks
- drift risks

## Chat Surface

Return the recommended visual system and the identity, geography, material,
lighting and palette rules needed for this project. Reuse an already selected
style. Offer alternatives only when they produce materially different films and
the user must choose. Internal design locks permit the next authorized stage;
they do not imply user acceptance of media.

## Visual Decision Contract

When visualization adds clarity, use `skills/dircreative/assets/visualizations/stage-surface-registry.json#visual-lock-matrix`. Bind identity, environment, props, wardrobe, light, material, and drift risks to the visual-bible artifact; use fullscreen only when the continuity matrix cannot remain legible inline and preserve the table fallback.

## Rules

- Lock identity, environment, prop states, palette, lighting, and material behavior.
- Label any base, coaster, tray, dock, magnet, stand, or holder as
  `support/environment hardware` so it cannot be merged into the product body.
- Break visual direction into concrete fields before prompt work: subject, action/pose or blocking, details/appearance, environment/background, lighting/atmosphere, composition/framing, style/camera, colors/palette, materials/texture, proportion/scale, and generation intent.
- State which facts are locked from story/shot/reference evidence and which are still unresolved. Do not invent unseen brands, exact text, locations, camera bodies, lens models, or hidden objects.
- Define type-specific visual rules when relevant: portrait, product, poster/ad, UI, illustration, 3D, or photography.
- Use style tags only as compact routing labels. The visual bible still needs full visual rules.
- Decide whether the project needs one board or a multi-image reference pack.
- Do not write final image prompts.

## skill_run_receipt

Persist the following only for a requested formal handoff, pause/resume or actual
execution record. Ordinary work returns its result without a separate receipt.
The next skill is advisory; the controller continues only the requested scope.

Record visual bible gate status, missing assets, drift risks, and `next_recommended_skill: reference-image-planner`.
