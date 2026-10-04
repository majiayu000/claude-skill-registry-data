---
name: build-ai-short-drama-prompts
description: Build and validate commercial-ready AI short-drama production packages after story and visual direction are locked. Use when the user provides an approved brief, continuity bible, or ProductionHandoff; explicitly requests A1/A2/A3, 95-point commercial QC, TapNow orchestration, model verification, shot-package standardization, or continuity-critical image-to-video, first/last-frame, or tail-continuation work. Do not trigger for ordinary image generation, early ideation, or style exploration.
---

# Build AI Short Drama Prompts

Operate as a commercial screenwriter-director production system, not a prompt thesaurus. Turn the user's story into an evidence-aware, original, executable production package.

## Accept ProductionHandoff JSON

Accept a JSON `ProductionHandoff` from `create-ai-short-drama-and-images` as an approved upstream input. JSON is the canonical runtime format; YAML assets are human-readable worksheets only.

Map handoff fields without discarding locks:

- `approved_visual_brief` -> normalized project intent and visual baseline;
- `character_and_scene_locks` -> character/scene/prop continuity Bibles;
- `selected_assets` -> reference registry with explicit roles and approval states;
- `target_platform` -> platform route;
- `continuity_level` -> validation strictness;
- `production_requirements.target_model` -> `project.target_model`.

For `high` or `locked` continuity, every lock must name concrete `locked_fields` and `approved_asset_ids`; every referenced asset must carry those same locked fields. A concrete target model is accepted only with fresh first-party availability and prompt-syntax claims. `production_requirements.generate_video` must be `false`; this Skill prepares video production prompts but does not execute video generation.

For any `local_file` character reference, the runtime—not the JSON package—must set `AI_VISUAL_PROJECT_ROOT` to the actual project root. Local assets must be under that root, bounded to 50 MB, non-symlinked, SHA-matched, and decodable. This check uses Pillow already bundled with Codex; if Pillow is unavailable, validation fails closed with `LOCAL_CHARACTER_ASSET_INVALID` and the operator must install/restore Pillow before using local-file references.

Run the existing validator after import. A handoff does not bypass A1 evidence checks, A2 package construction, preflight, or A3 approval.

## Run The Production Loop

Use three independent passes. Spawn subagents when available; otherwise run the passes sequentially and keep their artifacts separate.

1. **A1 Research Producer**
   - Verify current platform/model capabilities from official sources.
   - Record `verified_at`, model/version, real parameters, unsupported controls, commercial terms, known failure modes, and sources.
   - Separate official facts, professional film principles, and community observations.
2. **A2 Prompt Architect**
   - Normalize the brief.
   - Build character, scene, prop, lighting/color, and sound Bibles.
   - Route the task by workflow, platform, style, emotion, continuity risk, and delivery type.
   - Compose new shot design from the user's facts. Never reuse source examples' characters, dialogue, settings, or distinctive creative combinations.
3. **A3 Commercial Screenwriter-Director**
   - Review as screenwriter, director, cinematographer, script supervisor, editor, sound supervisor, platform operator, and client-delivery owner.
   - Apply every gate in `references/07-quality-gates.md`.
   - Return failures to A1 for missing/uncertain evidence or A2 for creative, continuity, execution, or delivery defects.

Repeat until `PASS`, or mark `STALLED` after the same root defect survives three consecutive revisions. Never lower the threshold to force approval.

## Required Threshold

- Score at least `95/100`.
- `Critical = 0`.
- `High = 0`.
- Every required field is present.
- Every platform claim is dated and verified.
- Every protagonist shot explicitly calls the approved final character reference.

## Choose The Workflow

Read `references/02-workflows-and-handoff.md`.

Default routing:

- Use built-in image generation first for character masters, multi-angle plates, nine-grids, scene Bibles, prop sheets, lighting palettes, storyboards, approved first/last frames, and continuity repair frames.
- Use TapNow to orchestrate assets and generate motion, acting, camera movement, dialogue, native audio, extensions, and assembly.
- Use direct text-to-video only for non-recurring empty shots, abstract imagery, exploratory concepts, or low-continuity inserts.
- Use image-to-video for approved characters, recurring scenes, products, props, or precise starting compositions.
- Use first/last-frame generation when both the opening and landing composition matter.
- Use an actual exported video tail frame only when continuing the same shot or action. Do not use tail-to-head continuity across a deliberate hard cut or major angle change.

## Build In This Order

1. Normalize the project brief using `assets/project-brief.yaml`.
2. Verify platform facts with `references/06-platform-registry.md` and live official documentation.
3. Select workflow and image/video handoff.
4. Select one primary style and at most one secondary style from `references/03-style-packs.md`.
5. Build continuity Bibles.
6. Break scenes into beats and coverage.
7. Generate reference-asset prompts before video prompts when continuity is medium, high, or serialized.
8. Write each shot with `references/01-prompt-schema.md`.
9. Write dialogue, ambience, Foley, effects, music, silence, and transitions using `references/05-audio.md`.
10. Add platform-specific syntax only after the platform adapter is verified.
11. Run `scripts/prompt_standardizer.py validate`.
12. Hash the exact reviewed package and signed evidence snapshot, set separate 32+ character `LOOP_STATE_KEY`, `A3_APPROVAL_KEY`, `AI_VISUAL_EVIDENCE_KEY`, and `AI_VISUAL_RIGHTS_KEY` secrets. Before `init`, run from the actual project root, set operator-controlled `AI_VISUAL_PROJECT_ROOT` to that same current directory, and pre-create `AI_VISUAL_LOOP_CHECKPOINT_ROOT` outside the project; the controller rejects an internal or falsely declared project path, signs `checkpoint_required=true`, serializes checkpoint compare-and-swap with a file lock, and fails closed if the environment is later removed. Initialize with `--package-sha256` and `--evidence-snapshot-sha256`, then feed the preflight result into `scripts/loop_controller.py advance`. If A1/A2 changes either artifact, use `scripts/loop_controller.py refresh` to audit the new hashes and invalidate the prior A3 challenge. A final A3 pass requires the current challenge, the complete signed evidence snapshot, and an HMAC signature over the full review conclusion.
13. Run the routed A1, A2, or A3 pass and record its structured result.
14. Repeat the controller step until A3 approves or the loop reports `STALLED`.
15. Deliver in the order defined below.

The validator performs structural and consistency preflight only. Its highest result is
`READY_FOR_A3`; it must never be treated as final client approval. Only a completed A3
review with a dated evidence record may issue `PASS`.

The loop controller routes work but does not generate or approve creative content. Its
highest authority is to select `A1`, `A2`, or `A3`, record defects, detect repeated root
causes, and preserve the audit trail.

## Mandatory Shot Content

Every shot prompt must include:

- final character/reference lock, even for a partial face, hand, shoulder, silhouette, or back view;
- narrative purpose and emotional change;
- shot size, camera height, angle, composition, lens appearance, focus, and motivated movement;
- one primary action and no more than two causal secondary motions;
- opening and ending state;
- foreground, midground, background, hero element, material texture, and environmental motion;
- motivated light source, direction, softness, temperature relationship, exposure anchor, shadow direction, palette, and continuity reference;
- dialogue and complete audio intent;
- continuity state, edit relationship, and frame handoff;
- positive invariants plus model-appropriate restrictions;
- expected visual result and likely failure mode.

## Use The Three Visual-Control Modules

Use them when motivated, not as decorative keyword stuffing.

- **Light-source module:** name source, direction, size/softness, color relationship, falloff, shadow direction, and exposure anchor.
- **Facial-detail module:** use three to five stable anchors: skin texture, eye condition, micro-expression, fatigue/age marker, and tension in mouth or brow.
- **Foreground-occlusion module:** name the object, frame share, blur level, movement, and what it must not cover.

Also consider the original modules in `references/04-cinematography-and-continuity.md`: attention path, causal secondary motion, material age, silence beat, focus narrative, and end-frame editability.

## Separate Real Parameters From Visual Language

Never claim that a simulated camera, lens, aperture, film stock, shutter, or color science is a real platform setting unless official documentation confirms it.

Output two blocks:

```yaml
platform_real_parameters:
  model:
  verified_at:
  resolution:
  aspect_ratio:
  fps:
  duration:
  reference_modes:
  native_audio:

visual_language:
  camera_emulation:
  lens_appearance:
  depth_of_field:
  shutter_motion_appearance:
  film_texture:
  dynamic_range:
  color_pipeline:
```

## Read References Selectively

- Always read `references/00-loop-and-routing.md`, `references/01-prompt-schema.md`, and `references/07-quality-gates.md`.
- Read `references/02-workflows-and-handoff.md` for any image/video generation or TapNow task.
- Read `references/03-style-packs.md` when choosing or translating a style.
- Read `references/04-cinematography-and-continuity.md` for shot design, lighting, color, blocking, continuity, or editing.
- Read `references/05-audio.md` whenever dialogue, sound, music, silence, or commercial delivery is involved.
- Read `references/06-platform-registry.md` and refresh official documentation for platform-specific work.
- Read `references/08-template-library.md` to produce copy-ready prompts.
- Read `references/09-evidence-sources.md` when source provenance or research refresh is required.

## Deliver The Commercial Package

Return:

1. creative and story intent;
2. platform/model route with verification date;
3. base technical and visual tone;
4. approved character lock sheet;
5. scene, prop, lighting/color, and sound Bibles;
6. image-generation asset plan;
7. nine-grid and multi-angle prompts;
8. storyboard and shot list;
9. one copy-ready prompt per shot;
10. first/last/tail-frame dependency map;
11. audio cue sheet and stem plan;
12. global invariants and restrictions;
13. expected result and retry strategy per workflow;
14. client delivery manifest;
15. A3 review report, score, and evidence/version record.

Do not expose intermediary failed drafts unless the user asks. The user should see the approved result plus any genuinely unresolved limitation.
