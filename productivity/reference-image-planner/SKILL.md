---
name: dircreative-reference-image-planner
description: Plan reference image pack roles, board types, and layout specs before prompt compilation.
---

# Reference Image Planner

## Required Knowledge

Read only the reference needed for the active task, not this entire list.
The root v2 route owns scope and authorization; legacy records do not add gates.

- `docs/film-preproduction/schemas/prompt-ir.schema.json`
- `docs/film-preproduction/asset-intake-and-state-standard-v1.md`
- `docs/film-preproduction/prompt-authoring-standard-v1.md`
- `docs/film-preproduction/chat-co-creation-interface.md`
- `docs/film-preproduction/chat-inline-visualization-interface.md`
- `docs/film-preproduction/ad-reference-pack-generation-gate.md`
- `docs/film-preproduction/research/storyboard-reference-analysis.md`
- `docs/film-preproduction/research/image-prompt-style-system.md`
- `docs/film-preproduction/research/model-reference-behavior.md`
- `docs/film-preproduction/research/tapnow-agentic-canvas-lessons.md`
- `docs/film-preproduction/reference-locking-policy.md`
- `docs/film-preproduction/reference-consistency-gate.md`
- `docs/film-preproduction/co-creation-gate-policy.md`
- `docs/film-preproduction/longform-decomposition-policy.md`
- `docs/film-preproduction/capability-aware-generation-policy.md`
- `docs/film-preproduction/clean-frame-export-policy.md`
- `docs/film-preproduction/sources/model-sources.yaml`
- `docs/film-preproduction/schemas/visual-bible.yaml`
- `docs/film-preproduction/schemas/reference-pack-manifest.yaml`
- `docs/film-preproduction/schemas/longform-reference-pack.yaml`

## Inputs

- visual bible
- shot list
- asset requirements

## Outputs

- reference pack plan
- reference pack manifest
- image layout spec
- board role map
- model-specific direct input policy
- exact capability-card resolution receipt
- reference rights gate
- asset output status map
- longform sequence pack requirements when target duration exceeds one generation unit

## Chat Surface

Return the usable asset plan: each asset's purpose, source/reuse/derive/generate
choice, reference role, dependent shots and necessary input policy. Explain the
few choices that change quality or effort. Preserve the selected model and
strategy; do not reopen either because several options exist. Separate planning
boards from direct clean inputs. Reuse existing image authorization; ask only if
an actual new side effect lacks it.

## Visual Decision Contract

When visualization adds clarity, use `skills/dircreative/assets/visualizations/stage-surface-registry.json#reference-asset-role-graph`. Bind every asset node to ID, role, status, shot binding, and current hash-bound source; visually distinguish planning-only from direct-video-input roles and preserve the Mermaid fallback.

## Rules

- Plan the fewest reference assets that still preserve readability and model safety.
- Resolve `capability_card_id + version + provider_surface` from `model-sources.yaml` before naming duration, reference modes, audio, edit, extension, or upload slots. A family alias, `latest`, stale card, S4-only evidence, workflow-only card, or deprecated card cannot authorize generation.
- Preserve source tier and `accessed_on` evidence in the manifest. If official sources conflict, keep the conflict visible and fail closed when the exact execution route remains ambiguous.
- Run the rights gate before proposing any direct image, video, audio, character, element, likeness, voice, brand, character, or music input. Unverified/blocked assets remain planning-only.
- Before any prompt or generation step for a client-facing film, create a per-shot asset/reference contract. Each shot must name source decision, source status, usage page or shot, planning/direct-input role, and blocker status.
- If the user says existing browser, Grok, ChatGPT, ImageGen, downloaded, or local images exist, complete browser/local intake before declaring missing assets or writing replacement prompts. If intake tooling is unavailable, record `TOOL_BLOCKED` and the manual intake needed.
- A supplied or generated storyboard sequence without bound source assets is
  `planning_only`, even when faces, vehicles, props, or locations look similar.
  Audit recoverable visible facts, then derive missing identity, production-
  design, geography/FOV, and critical-prop references before clean frames.
- Use the `asset_foundation` Skill Stack scenario for that planning pass. Keep
  character continuity, production design, camera geography, constraint-input,
  material, and post-generation consistency responsibilities distinct; do not
  load every provider into one stage.
- New recurring clothed-human work routes to the v3 contract in
  `skills/dircreative/references/character-master-sheet.md`. Separate identity
  and wardrobe/body files are allowed as hash-bound `planning_only` generation
  provenance, but the planner must produce one unified master and must never
  submit those inputs as co-active downstream identity references. This planner
  records roles and shot need; the canonical reference owns layout, headless and
  conditional-detail rules.
- Run its stable passes in the order defined by
  `skills/dircreative/references/asset-foundation-pass.md`. Bind each output hash
  only where it is a real next input. A failed or incomplete pass blocks only
  the asset, shot or sequence that consumes it; continue independent planning
  and authorized production batches before returning to the failed dependency.
- Before repeated/multi-shot assets become compile inputs, route the final pass
  through `ai-film-asset-stress-test`. `conditional` must enumerate allowed and
  blocked shot scope; missing real evidence remains `unverified`.
- Split human planning boards from model layout references. A narrative frame
  or labeled board cannot become an identity source, clean frame, or model
  reference without an explicit promotion receipt, narrower role, and
  independent QA. Composition evidence never outranks identity or vehicle
  topology.
- Resolve the selected provider's current `max_references` before prompt-ready
  status. If a unit exceeds it, preserve explicit reference sovereignty and
  merge only assets that already bind the same identity/state contract; never
  discover the limit at generation time or silently drop a reference.
- Hero, acting, movement, or expression-critical shots must include a reference video, reference clip, or explicit motion note. Music/video sources must keep source, usage, and lock status so later versions cannot drop them.
- For assisted generation, lock visual truth in this order: character identity, scene geography/camera FOV, professional storyboard/motion page, then selected clean frames.
- Character consistency and scene consistency are mandatory. Establish shared identity and geography before dependent work; do not batch-generate boards that independently reinterpret an unanchored character or location. Once those inputs are ready, produce the batch continuously and review/select it together.
- Prefer a minimal V2 pack when drift risk is high: one character identity reference, one scene geography + camera FOV atlas, one professional storyboard/motion page, then optional clean first/end frames.
- Scene geography boards should be a single atlas when possible: panoramic or 360-degree environment, top-down route map, shot camera positions, FOV wedges, subject path, and vehicle path.
- Repeated character or scene content must inherit from the locked source asset; repetition must not introduce new face, wardrobe, prop, street, vehicle, or light-source facts.
- Model irreversible state families explicitly: damage, shield, core, door,
  helmet, prop, and vehicle states need legal transitions and cannot reset in a
  later clean frame.
- A clean frame is not an identity-board beauty shot. It must pass both asset
  truth and director-frame quality. When `jingzao-image-forge` is available,
  export the approved shot card, canonical asset roles, camera_action evidence,
  state, and target surface through `storyboard_frame_to_jingzao_v1`; do not
  replace that provider with a generic centered prompt.
- Shot count and image count are dynamic. Do not force three clean frames or one image per shot by default.
- Before planning frames, choose a reference strategy: `all_reference_sequence`, `hybrid`, `per_shot_i2v`, or `minimal_test`.
- For fast 15-second work, allow more shots and more clean frames when the edit rhythm needs them.
- For all-reference models or modes, dense boards can be the main guidance if the prompt manifest records anti-misread clauses and accepted risk.
- For complex ad films with unresolved visual truth, propose a complete reference pack: identity, scene/FOV, optional lighting/material/style, optional storyboard/motion, and only the clean frames required by the selected model route.
- Do not treat a complete pack as a universal prerequisite. If the user supplies locked character/product and scene assets, compile the prompt from those assets plus written composition, camera, action, audio, transition, and conditional Look fields.
- A style/material/lighting board is optional when the look can be expressed precisely in the prompt and no repeated cross-shot drift is observed.
- A storyboard/motion board is optional when the shot list and Prompt IR already express timing, blocking, camera path, sound, and transition; it is a human-review artifact, not a mandatory model input.
- Do not generate a clean frame unless the selected model workflow requires a direct start/end image or a clean visual anchor.
- Default `visual_output_mode` to `prompt_only` unless image generation is available and authorized.
- Record execution capabilities and `asset_output.status` for every planned asset.
- For 60s, 90s, and 180s targets, create global references once and sequence packs one at a time in hybrid mode.
- Every reference asset needs exactly one primary production role.
- Every planned board must have a visible role label or manifest role label, such as character reference, scene + camera movement reference, professional storyboard + motion map, or clean first/end frame.
- A professional storyboard/motion page is required for explicitly requested whole-film coverage; a bounded shot review can use its existing shot card. Each shot cell must include timecode, duration, shot image region, detailed frame description, shot size, focal length, camera position, camera movement, subject blocking, sound, transition, and model risk.
- A professional storyboard/motion page defaults to `planning_only`. A clean first/key/end frame is a separate, text-free asset; never imply a board crop is a clean frame.
- Use dense boards for human review, Seedance, and Veo only when the direct input policy allows it.
- Use clean first frames or start/end frame assets for Kling and Runway direct image-to-video inputs.
- For any direct first-frame/start-end-frame workflow, plan the required clean frames for that selected mode.
- Clean frames are separate assets or explicit clean-frame prompts, not hidden crops implied by a dense board.
- Do not mark direct I2V as ready when clean frames are only planned; keep `asset_output.status` as `prompt_ready`, `external_pending`, or `generated_candidate` until real images pass the required independent visual review and host dependency adoption. Record user acceptance separately, only when it actually occurs.
- Separate planning boards from direct model inputs when labels, arrows, floor plans, or panel borders could be misread.
- Only unresolved concept choices or unapproved real media actions need a v2 external gate. Preserve already granted scoped permissions.
- Separate controller design decisions, independent media review and actual user acceptance; never manufacture the last.
- Add `must_not_animate` rules for any board with labels, arrows, panel borders, floor plans, timing notes, or tables.
- Load the exact-card pack recipe for the selected model only. Keep Kling VIDEO 3.0 separate from its legacy 5/10-second card; keep Runway Gen-4.5 generation, Aleph 2.0 Web, Aleph 2.0 API, and deprecated Gen-4 Aleph separate; use stable Veo 3.1 `*-001` cards instead of preview aliases.
- Layout spec must protect readability and video-model safety.
- Represent the reference pack as asset nodes with explicit graph edges: planning-only, reference-only, or direct video input.
- Preserve prompt optimizer provenance if an optimized prompt is produced: keep the JSON-first source intent and the optimized text output.

## skill_run_receipt

Persist the following only for a requested formal handoff, pause/resume or actual
execution record. Ordinary work returns its result without a separate receipt.
The next skill is advisory; the controller continues only the requested scope.

Record reference pack decision, visual output mode, execution capability, exact capability cards, source tiers/dates/conflicts, rights status, asset output statuses, rejected layouts, storyboard/clean-frame separation, direct input policy, optional canvas graph receipt, user decision gate status, QA status, and `next_recommended_skill: image-prompt-compiler`.
