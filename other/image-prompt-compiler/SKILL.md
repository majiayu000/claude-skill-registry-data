---
name: dircreative-image-prompt-compiler
description: Compile JSON-first reference image prompts from visual bible, reference pack, and prompt pattern registry.
---

# Image Prompt Compiler

## Required Knowledge

Read only the reference needed for the active task, not this entire list.
The root v2 route owns scope and authorization; legacy records do not add gates.

- `docs/film-preproduction/schemas/prompt-ir.schema.json`
- `docs/film-preproduction/schemas/prompt-ir.yaml`
- `docs/film-preproduction/prompt-authoring-standard-v1.md`
- `docs/film-preproduction/asset-intake-and-state-standard-v1.md`
- `docs/film-preproduction/prompt-qa-and-incident-runbook-v1.md`
- `docs/film-preproduction/chat-co-creation-interface.md`
- `docs/film-preproduction/chat-inline-visualization-interface.md`
- `docs/film-preproduction/ad-reference-pack-generation-gate.md`
- `docs/film-preproduction/schemas/image-prompt-manifest.yaml`
- `docs/film-preproduction/schemas/image-prompt-style-config.schema.json`
- `docs/film-preproduction/templates/image-prompt-style-config.template.json`
- `docs/film-preproduction/prompt-pattern-registry.json`
- `docs/film-preproduction/research/image-prompt-style-system.md`
- `docs/film-preproduction/co-creation-gate-policy.md`
- `docs/film-preproduction/capability-aware-generation-policy.md`
- `docs/film-preproduction/longform-decomposition-policy.md`
- `docs/film-preproduction/clean-frame-export-policy.md`
- `docs/film-preproduction/reference-consistency-gate.md`
- `docs/film-preproduction/film-commercial-quality-standard.md`
- `docs/film-preproduction/creative-production-integration.md`
- `docs/film-preproduction/production-prompt-discipline.md`
- `docs/film-preproduction/research/ai-video-prompt-community-lessons.md`
- `docs/film-preproduction/sources/model-sources.yaml`
- `docs/film-preproduction/sources/prompt-sources.yaml`
- `skills/dircreative/references/storyboard-frame-to-jingzao.md` only when the
  selected Skill Stack scenario is `cinematic_storyboard_frames`

## Inputs

- visual bible
- reference pack plan
- image layout spec

## Outputs

- image prompt manifest
- image prompt files
- visible pre-generation contract inside every exported image prompt
- machine-readable pre-generation contract for every assisted-generation image
- external generation instructions when `visual_output_mode` is `prompt_only` or `external_generation`
- exact capability-card, rights, and preserve/change receipts

## Chat Surface

When the user requests prompts, return the complete copyable prompt for the
selected asset, plus the reference binding and only necessary instructions.
Keep hashes, internal IDs and machine contracts in the manifest. When image
production is requested, prepare the exact prompt and pass it to the authorized
Delivery executor without asking the user to select the same material again.
State actual media status and preserve the distinction between planning boards
and clean model inputs. No prompt request authorizes a media call by itself.

## Visual Decision Contract

When visualization adds clarity, use `skills/dircreative/assets/visualizations/stage-surface-registry.json#image-prompt-handoff-summary`. Show prompt intent, inherited references, selected model, generation boundary, and QA target without exposing raw prompt bodies; prompt-only and generation requests remain separate conversation intents with a Markdown fallback.

## Rules

- Use JSON-first configs for formal reusable manifests. For a bounded prompt request, deliver the complete copyable prompt without first creating a project schema.
- For cinematic storyboard or clean narrative frames, DIR may hand frame-level
  craft ownership to `jingzao-image-forge` through
  `storyboard_frame_to_jingzao_v1`. Pass the complete shot-tension contract and
  ordered canonical references; consume the compiled spec/prompt back into the
  DIR manifest. Do not paraphrase Jingzao's craft rules, claim it was used
  without an isolated full-body read, or let asset identity sheets choose a
  neutral catalog composition.
- Resolve the exact image capability card, version, status, provider surface, source tier, and accessed date before naming generation/edit/reference/output behavior. Reject family aliases, `latest`, stale cards, S4-only evidence, workflow-only cards, and deprecated defaults.
- Select `operation: generate | edit | retry`. `edit` requires a real input image plus non-overlapping `preserve` and `change` sets; `retry` changes one production variable and records the observed failure.
- Run the rights gate for every input/reference image, likeness, brand, character, logo, and exact text asset. Unverified/blocked rights force prompt-only and block external upload as well as assisted generation.
- Apply the production prompt discipline pre-delivery harness to the active prompt and its actual dependencies: reference roles, model constraints, prompt-window hygiene and falsifiable success criteria. A bounded edit uses the relevant checks directly; full audits are source-maintenance or formal-contract tests.
- A shot-derived client-film image prompt comes from its current shot and asset/reference contract; initial character/product/scene studies use their design contract without an invented shot. For shot-derived prompts, bind the current shot ID, character or role identity, prop, action, shot size, camera angle or position, vertical/horizontal composition, and usage page.
- A shot-derived clean image inherits its existing shot and asset truth. Initial character/product/scene asset design follows the role-specific design contract; it does not require its own future image or a whole-film shot gate. Missing media stays prompt_only with its actual use and unresolved binding named.
- For complex image assets, include `evidence_policy`, `visual_decomposition`, `prompt_layers`, `type_treatment`, and `style_tags` in the style config.
- `visual_decomposition` must cover subject, action/pose or blocking, details/appearance, environment/background, lighting/atmosphere, composition/framing, style/camera, colors/palette, materials/texture, proportion/scale, and generation intent.
- Map decomposition fields into director language: blocking, foreground/midground/background, readable zone, shot size, angle, lens feel, camera support, movement, focus, palette, material behavior, continuity locks, and downstream video-model use.
- `prompt_layers.director_recreation_prompt` is the production prompt for the exact asset. `prompt_layers.prompt_core` is the reusable lock. `prompt_layers.negative_prompt` is optional/empty unless a concrete known risk or observed failure needs a targeted avoid-list; never carry a growing history of failed attempts into a new image.
- Do not use standalone filler quality words such as `high detail`, `masterpiece`, `best quality`, `cinematic`, `beautiful`, or `premium`. Replace them with concrete surface, lens, lighting, composition, readability, and continuity constraints.
- Image prompt model constraints must be explicit when relevant: aspect ratio, output mode, direct-input policy, text policy, reference role, and whether generated files are expected to exist.
- Keep `desired_audio` as downstream metadata only and `generation_audio_route: not_applicable` in an image manifest. Never ask an image model to generate dialogue, voiceover, music, ambience, or sound effects.
- Do not write plausible platform or model facts as verified facts. Aspect ratios, output controls, direct-input policy, and current tool availability must come from local policy, source docs, or tool schema evidence.
- Use only locked upstream facts and visible generated/imported evidence. If a detail is uncertain, write a broader production-safe description instead of inventing brands, logos, exact text, locations, camera bodies, lens models, hidden objects, or offscreen props.
- Default to the project working language plus exact displayed labels. Add multilingual prompt fields only when the client handoff, UI, or external generation target requires them.
- Add 3-5 short style tags only as routing and QA metadata; do not treat tags as a substitute for the visual decomposition.
- Apply type treatment before writing the final prompt: portrait, product, poster/ad, UI, illustration, 3D, and photography each require different visible facts and failure checks.
- For brand/product films where product identity is not locked, the first assisted-generation image must be a clean single-product `PRODUCT IDENTITY REFERENCE`.
- Before product identity generation, freeze product silhouette, scale, material, diffusion/opening method, logo/text policy, desk/car use readability, and forbidden style drift.
- The first product identity image must not include the protagonist, full ad scene, storyboard panels, labels, captions, detail insets, product-sheet collage panels, strong category-rewriting background props, large slogan text, ancient/fantasy symbols, or luxury perfume ad cliches unless explicitly requested.
- Material macro views, vent details, packaging, and usage-context views must be separate later assets, not insets inside the first product identity candidate.
- Product identity QA must check for video-model misread risks: speaker, power bank, air purifier, car control knob, perfume bottle, incense burner, and ancient ornament.
- For abstract pebble, pod, stone, or capsule products, also check mouse, soap, jewelry box, stone decor, charging case, and generic electronic accessory risks.
- Do not mark an abstract product identity as locked from a beauty shot alone. Compile follow-up `FUNCTION DETAIL REFERENCE` and, for multi-mode products, `USAGE POSITION REFERENCE` prompts before final identity lock.
- If a base, coaster, tray, dock, magnet, stand, or holder appears, write whether it is product hardware or environment/support hardware in the pre-generation contract.
- Before assisted generation, the exact asset needs a validated pre_generation_contract and execution packet. Keep asset IDs, hashes, source provenance, authorization and direct-input policy in those records; they are not image content.
- The prompt must express the visual role, actual reference responsibilities and preserve/change constraints. Human planning boards may show their role as the dominant title; only a supplied display title may be smaller metadata. Never print an internal project ID or hash as a title.
- Character masters follow the canonical no-text character-master-sheet contract. Clean frames have no visible title, label, border or planning overlay. Their role is bound in the manifest; no generic visible-contract prefix may override it.
- Legacy v1 prompt-only exports used Pre-generation contract, Largest title on the page, Smaller metadata only and Direct video input policy headers. Preserve them when reading those old fixtures; new terminal prompts contain only visual instructions and actual attachment roles.
- Prompts must preserve the lock order: character identity first, scene geography/camera FOV second, professional storyboard/motion page third, clean frames last.
- Resolve the material role from the active plan and conversation. Ask one focused question only if multiple remaining roles would materially change the output.
- Visual exploration produces draft candidates. Formal assets require the appropriate design/shot source, scoped execution and actual review; legacy story/script/shot approvals are not current gates.
- Later prompts must inherit locked character and scene anchors instead of redesigning them.
- Do not repeat the same character or scene across multiple boards unless the prompt explicitly says which locked source is being reused and what new job the image performs.
- Every board prompt must include a clear role label: `CHARACTER IDENTITY REFERENCE`, `SCENE GEOGRAPHY + CAMERA FOV REFERENCE`, `PROFESSIONAL STORYBOARD + MOTION MAP`, or the matching Chinese label.
- For titled human planning boards the role is the dominant title and any supplied film title is smaller. No-text character masters, standalone asset studies and clean frames keep labels in the manifest.
- Product identity boards may include clear packaging text; do not apply `no readable text` to identity boards that need brand or product recognition.
- Clean frames must be no-text, no-label, no-arrow, no-panel direct I2V frames.
- Professional storyboard/motion maps default to planning-only; a clean frame is a separate prompt/asset and must never be an implied crop from a board.
- Clean frame prompts must be individual image prompts, not only a note saying to crop/export from a board.
- If a reference pack includes a clean frame set, compile one prompt per required clean frame and mark each as `text_policy: no_text`.
- Storyboard/motion overview pages receive duration, movement and transition text from the shot cards during deterministic assembly, not by asking an image model to redraw the sequence.
- Professional storyboard/motion page prompts must include one shot cell per approved shot with timecode, duration, shot image region, detailed frame description, character design locks, scene layout locks, prop continuity, shot size, focal length, camera position, camera movement, subject movement path, subject blocking, emotional beat, sound, transition, and model risk.
- Professional storyboard/motion page prompts must require compact professional shot-card text inside each cell. The text may be short, but it must name narrative purpose, lens/support/movement, subject blocking/path, continuity lock, sound or edit cue, and model risk. Reject thin labels such as only `wide`, `close-up`, `slow push`, `conversation`, or `emotional ending`.
- The visible text inside each storyboard cell must follow this structure: `S03 00:18-00:24 | Narrative purpose: ... | Lens/support/movement: ... | Blocking/path: ... | Continuity: ... | Sound/edit: ... | Model risk: ...`.
- When adapting external/community prompt examples, keep only the reusable structure. Do not copy a Reddit, X, or prompt-library recipe into an image prompt unless it has been converted into DIRcreative source truth, material role, prompt contract, targeted negative constraints, and falsifiable success criteria.
- Record `visual_output_mode`, `execution_capabilities`, and `asset_output` for every image.
- Use `scripts/dircreative_prompt_compiler.py` as the executable compiler; the
  media gate only revalidates its content-addressed output and never rewrites it.
- For `storyboard_frame` and clean-frame roles, the accepted prompt is the exact
  prompt read back from a production `storyboard_frame_to_jingzao_v1` manifest,
  bound to the installed Jingzao Skill and the active shot truth. A locally
  reconstructed DIR helper prompt is invalid. Assemble the professional
  storyboard/motion page deterministically from approved individual frames and
  shot-card text with `scripts/dircreative_storyboard_page_assembler.py`; never
  ask imagegen to redraw that overview page. Write the PNG and assembly receipt
  into the project, then bind and visually review them through the normal plan.
- Include selected pattern IDs, exact labels, art-directed layout policy, material truth, consistency locks, and surface integrity guard.
- Treat `surface_integrity_guard_v1` fixed wording as an optional internal QA macro, never a required Image2/GPT Image suffix. Default it off; activate it only for an observed matching failure or recorded A/B eval, preserve the control prompt, and never use its word `transparent` as evidence of alpha-background support.
- Retry prompts must change one variable at a time: subject/product identity, primary action, camera/framing, look/material/light, reference binding, or output control. Record the failure ID and smallest upstream artifact being corrected.
- In `prompt_only`, produce complete prompts and import instructions without generated files.
- In `external_generation`, name the target tool, upload role, and reference binding expected downstream.
- In `assisted_generation`, require explicit user authorization before calling any image tool.
- Creative Production may be used only as a deep generation and review adapter after upstream DIRcreative gates and `pre_generation_contract.status: pass`; use Mood boards, Scenes, Offers, Ads, Shots, or Generative Polish only through the mapping in `creative-production-integration.md`.
- When Creative Production is used, `render_moodboard_board_widget` is the review surface and is not the source of truth. Write the candidate, QA status, and user lock state back into `.dircreative/runs/` or the relevant manifest.
- A Creative Production candidate starts as `generated_candidate`; do not mark it `user_locked` until self-QA passes and the real user locks it.
- Do not compile locked image generation tasks from `simulated_fixture` decisions in a live run.
- In `prompt_only` and `external_generation`, do not call image tools. In an
  authorized `assisted_generation` handoff, return the validated prompt and
  packet to the Delivery executor; this compiler still does not perform the
  media call itself.
- Validate Prompt IR v1.1 before compiling DIR-owned prompts. Treat `prompt-ir.yaml` as an authoring template, not as the executable schema; Jingzao-owned frame prompts use their validated production handoff and prompt manifest instead.
- Keep source locators, hashes, entity IDs, capability evidence, QA, retry, and post-production metadata inside Prompt IR/manifests. The image model receives only attached reference roles, observable visual instructions, preserve/change boundaries, and targeted current constraints.

## Prompt IR and look closure

Before compiling any image prompt, run asset intake against the supplied files or conversation media. Record source kind, locator, hash, role, authorization, inherits_from, preserve, may_change, do_not_copy_or_animate, reuse_action, lock state, and downstream use. If an existing image already resolves identity, material, scene, or composition, use direct_reference, edit, or derive; do not recreate it from prose.

Every complex image prompt must include a composition card with visual center, hierarchy, foreground/midground/background, negative space, movement room, leading lines or occlusion, perspective depth, crop safety, and narrative purpose. Do not default to rule of thirds, center framing, symmetry, or cinematic as a substitute for a reason.

Every complex image prompt must include a four-layer render look card:

~~~text
lighting -> optics -> atmosphere -> grade
condition -> effect -> intensity -> preserve -> exit/continuity
~~~

Separate physical lens/filter behavior from post effects. Write none by design when a layer is not needed. Image prompts never generate audio; audio intent remains downstream metadata.

After an image is generated or imported, perform self-QA before asking for lock. Return the artifact, current status, pass/fail findings, and next_action. A generated_candidate is not user_locked, and prompt_only is not generated.

## skill_run_receipt

Persist the following only for a requested formal handoff, pause/resume or actual
execution record. Ordinary work returns its result without a separate receipt.
The next skill is advisory; the controller continues only the requested scope.

Record selected patterns, exact capability card/version/surface and source evidence, source conflicts, rights status, operation, preserve/change contract, optional QA macro activation, visual output mode, execution capability, asset output statuses, storyboard/clean-frame separation, manifest QA, prompt files, and `next_recommended_skill: video-model-adapter`.
