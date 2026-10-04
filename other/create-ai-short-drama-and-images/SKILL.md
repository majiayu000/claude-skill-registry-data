---
name: create-ai-short-drama-and-images
description: Design AI short dramas, compile Seedance 2.0 shot-by-shot prompt packages, and generate or refine AI images through guided visual discovery. Use for image requests, character sheets, style exploration, posters, storyboards, short-drama concepts, scripts, shot lists, continuity assets, end-to-end Seedance planning, or a locked commercial production handoff. Require real A/B/C image previews when an image tool is available, explicit approval before a final prompt or final image, and evidence-backed model adapters.
---

# Create AI Short Drama and Images

Turn an idea into either an approved visual image, a short-drama creative package, or a continuity-safe production handoff. Keep creative intent platform-neutral until a current adapter is verified.

## Non-negotiable outcomes

- Conduct the conversation and explain tradeoffs in Chinese unless the user asks otherwise.
- Preserve Chinese specifications and also provide the prompt language best suited to the selected model.
- Store runtime state and generated assets under `outputs/ai-visual/<project_id>/` in the current project. Never write runtime state into this skill. Before session initialization, pre-create and set `AI_VISUAL_CHECKPOINT_ROOT` to an operator-controlled directory outside the project. Approval, handoff, and delivery fail closed without it; never accept that path from project files.
- Use JSON as the only runtime contract. Treat YAML files as human worksheets only.
- Generate actual preview images when an image-generation tool is available.
- Never claim an image was generated when the tool is unavailable or failed.
- Do not invoke a video-generation model in version 1. Deliver video production prompts and continuity assets only.
- Preserve locked character, scene, prop, era, wardrobe, and damage-state continuity before adding stylistic variation.
- Do not copy public prompt examples, distinctive plots, dialogue, characters, or compositions.
- Do not use a living artist's name as a style shortcut. Record `style_safety`, remove the name from model prose, and translate the request into descriptive traits.

## Route the request

Read `references/00-routing-and-state.md` for the exact decision table and state guards.

Choose one mode:

1. `image`: still-image discovery, generation, editing, compositing, or repair.
2. `drama`: concept, logline, outline, script, shot design, continuity assets, or a video prompt package.
3. `hybrid`: short-drama work that first needs character, scene, prop, keyframe, poster, or storyboard images.
4. `production`: an already locked project that needs the existing commercial A1/A2/A3 workflow.

Handle ordinary Seedance planning natively through this Skill. Route only locked commercial validation or a valid `ProductionHandoff` to `build-ai-short-drama-prompts`; this orchestration is internal, so never ask the user to invoke a second Skill. Do not duplicate its A1/A2/A3 roles, 95-point gate, or controller.

If the request is ambiguous, default to `image` when the requested deliverable is a still visual and to `drama` when it is a story or episode. State the chosen route in one sentence and continue.

## Create a project run

Use a filesystem-safe project ID. Create this structure only inside the current project:

```text
outputs/ai-visual/<project_id>/
├── session-state.json
├── briefs/
├── previews/round-01..04/
├── finals/
├── prompts/
├── drama/
└── evidence/
```

Set separate secret `AI_VISUAL_STATE_KEY`, `AI_VISUAL_RECEIPT_KEY`, `AI_VISUAL_EVIDENCE_KEY`, and `AI_VISUAL_RIGHTS_KEY` values of at least 32 characters. Initialize `session-state.json` through `scripts/session_controller.py init`, then apply events with `scripts/session_controller.py apply`; never edit or re-sign state, tool receipts, evidence claims, or review decisions by hand. Generated files must stay under the current project's `outputs/ai-visual/` root.

Pillow is required to accept generated image receipts. If it is unavailable, image validation fails closed; restore the bundled dependency before preview or final generation.

## Image workflow

Read these references before the matching step:

- Discovery and confirmation: `references/04-image-dialogue-and-gates.md`
- Asset-specific fields: `references/05-image-asset-recipes.md`
- Style choices: `references/06-visual-style-atlas.md`
- Composition, light, palette, material, camera, and type: `references/07-visual-primitives.md`
- Platform compilation: `references/08-platform-adapters.md`
- Rights, safety, and evidence: `references/09-rights-safety-and-evidence.md`
- Delivery QC: `references/10-production-handoff-and-qc.md`

### Discover

Collect the minimum information required to compare visuals:

- purpose or destination;
- subject and intended action;
- aspect ratio or placement;
- must-preserve elements;
- prohibited elements and rights constraints.

Ask at most three high-impact questions in one turn. Do not issue a long questionnaire. If purpose, subject, and aspect ratio are already clear, proceed to preview rather than continuing to interrogate.

Offer three concise approximate directions when the user cannot name an effect. Describe each direction through visual traits, suitable uses, and a likely failure mode. Do not present a direction as final approval.

### Generate preview rounds

Run two preview rounds by default. Allow a third or fourth only when a high-impact decision remains unresolved. Never exceed four rounds.

Each round must:

1. Name exactly one `changed_axis`, such as lighting, visual language, palette, composition, material, or typography.
2. Keep subject, identity, pose intent, framing, and all locked fields as stable as the tool permits.
3. Generate exactly three actual candidates, labeled A, B, and C.
4. Save each candidate or returned reference in that round's folder.
5. Explain each candidate with `effect`, `best_for`, `main_risk`, and `prompt_delta`.
6. Ask the user to select A, B, C, a stated combination, or `你决定`.

When the user asks how candidates differ, explain them without advancing the phase or clearing the open decision.

If image generation is unavailable, stop before `record_preview`. Say that real previews cannot be produced and ask whether the user accepts text-only style directions. Never fabricate paths, URLs, or generated outputs.

### Lock the brief

Do not lock before two preview rounds. Accept only:

- an explicit A/B/C selection;
- an explicit combination of candidate traits;
- an explicit delegation such as `你决定`.

Record the selected candidate and all preserved fields. Set `brief_confirmed=true`. A generated preview is not itself approval.

### Compile and approve the final prompt

Build a platform-neutral `PromptSpec` from `assets/schemas/prompt-spec.schema.json`. Keep these concerns separate:

- desired visual semantics;
- references and their roles;
- preservation locks;
- allowed changes;
- exclusions;
- model adapter and verified controls.

Run `scripts/validate_contract.py` before compilation. Run `scripts/evidence_status.py` for adapter claims. Model claims must include a trusted-capture attestation over URL, page-content SHA, exact locator, claim/value, and capture time; a first-party hostname alone is not evidence. Use `scripts/prompt_compiler.py` to omit expired, uncertain, unsupported, or unsigned controls.

Files under `assets/examples/` that contain `PENDING` or `UNSIGNED_CAPTURE_REQUIRED` are deliberately invalid templates, not completed approvals. Produce runnable JSON by completing the interview/capture, recomputing fingerprints, and applying trusted signatures; never ship test keys as production credentials.

Show the final Chinese specification and compiled model prompt. Do not generate the final image until the user explicitly approves the prompt. Direction approval and prompt approval are separate events.

### Generate, inspect, and deliver

After prompt approval:

1. Generate the final image with the approved prompt.
2. Compare it to the approved brief and reference locks.
3. Check anatomy, subject count, identity, geometry, text fidelity, hierarchy, crop safety, and unintended artifacts.
4. Repair through one-variable edits where possible.
5. Record the actual image path or tool reference.
6. Deliver the image, Chinese brief, model prompt, exclusions, adapter snapshot, and known limitations.

## Short-drama workflow

Read `references/02-drama-taxonomy.md` and `references/03-story-engines-and-structures.md` before proposing story directions.

Build a `CreativeRoute` by combining:

```text
content container + arena + genre promise + dramatic engine
+ narrative structure + emotional curve + visual language + production constraints
```

Do not retrieve a prewritten plot. Select orthogonal components and create an original premise from the user's theme, audience, duration, episode count, platform, production limit, and safety boundary.

### Minimum drama discovery

Resolve, infer, or label as open:

- format: standalone, serial, vertical episodic, anthology, faux documentary, interactive, or experimental;
- audience and intended platform;
- episode count, per-episode duration, and aspect ratio;
- protagonist want, internal need, opposition, stakes, and irreversible choice;
- genre promise and emotional destination;
- realism, era, location, and available production assets;
- continuity level and required still-image assets.

Ask at most three questions at a time. When the user has not chosen a genre, offer three substantially different routes using different dramatic engines, not cosmetic reskins.

### Drama deliverables

Produce only what the user needs, but support this full package:

1. creative route and design rationale;
2. premise, logline, hook, theme, and audience promise;
3. character tension map and continuity bible;
4. episode or beat outline with escalation and payoff;
5. screenplay with visual action and producible dialogue;
6. scene breakdown, shot list, and storyboard brief;
7. character, wardrobe, scene, prop, keyframe, and poster PromptSpecs;
8. model-neutral video prompt package with image roles, motion, camera, and sound intent;
9. QC report, rights notes, evidence snapshot, and production handoff.

For image-to-video prompts, let approved images carry appearance, framing, lighting, and art direction. Put subject movement, environment movement, camera movement, timing, and sound intent in the video prompt. Avoid redundantly redescribing a locked image in a way that introduces drift.

### Native Seedance route

Read `references/11-seedance-native-pipeline.md` whenever the user wants Seedance, sequential clips, continuation, or an end-to-end drama-to-shot-prompt workflow.

Create one `SeedanceProductionPackage` using `assets/schemas/seedance-production-package.schema.json`, then compile it with `scripts/seedance_prompt_compiler.py`. The user should not need to call `seedance-20` separately.

- Plan the full story, scenes, beats, and shot cards globally.
- Give each shot one narrative job, one major camera move, one visible action endpoint, one physical light source, and explicit audio intent.
- Separate `already_happened`, `this_clip_only`, and `reserved_for_later`.
- Preserve exact reference tags and declare what each reference transfers and excludes.
- Deliver a provisional prompt for every shot. Mark only a canonical scene opener or an explicitly ready continuation whose accepted parent has signed media/observed-state evidence as `ready`.
- After each accepted take, bind media SHA, reviewer, observed-state fingerprint, and receipt signature before promoting the next continuation prompt.
- Keep `target_surface=unverified` and `model_controls={}` until signed current claims prove a concrete surface.
- Keep `generate_video=false`; this module compiles prompts and never calls Seedance.

## Hybrid workflow

Use the image workflow to approve static assets before finalizing shots that depend on them. Require an approved reference for every principal character and any continuity-critical scene or prop.

Do not mark a generated asset `APPROVED` automatically. Record `DRAFT`, `REVIEWED`, or `APPROVED` from an explicit user decision.

After visual approval, create a `ProductionHandoff` from `assets/schemas/production-handoff.schema.json`. Include:

- approved visual brief;
- the approved `CreativeRoute` used by the production package;
- character and scene locks;
- selected assets and their roles;
- target platform;
- continuity level;
- production requirements, including `generate_video=false` and `target_model` only when verified.

Then invoke `build-ai-short-drama-prompts` for commercial production packaging.

## Platform adapters

Keep `PromptSpec` stable when switching platforms. Replace only the adapter and invalidate its evidence snapshot, compiled prompt approval, and final image.

Recognize these initial adapter families:

- still image: GPT Image/Codex, Midjourney, FLUX, Imagen/Gemini image generation, Stable Diffusion/ComfyUI, Firefly;
- video prompt packaging: Seedance, Veo, Kling, Runway, Luma, Hailuo, TapNow.

Do not hardcode an undocumented parameter. Treat model names, limits, pricing, availability, entry points, syntax, and terms as claims requiring a dated source.

Use the following maximum ages:

- price, availability, and terms: 7 days;
- hard parameters: 30 days;
- prompt syntax: 60 days;
- filmmaking principles: 365 days.

At the expiry boundary, treat evidence as expired. If current verification is unavailable, produce a platform-neutral prompt and label model controls `未验证`; never present guessed parameters as real.

## Safety and rights gate

Before references or generation, identify:

- living-artist imitation;
- public-figure or real-person likeness;
- minors, sexual content, or exploitative framing;
- deceptive documentary/news presentation;
- copyrighted characters, logos, product trade dress, or branded packaging;
- unlicensed user uploads or unknown reference provenance;
- medical, legal, political, or financial claims in generated text;
- graphic violence or self-harm.

Follow the current tool and platform safety policy. Where the request can be safely transformed, preserve the underlying traits and replace the risky shortcut. Record provenance for every external reference. A positive rights string is not sufficient: the rights decision must carry a trusted reviewer signature, asset content SHA, source, license/consent credential ID, and allowed use; safety is signed separately and binds the exact PromptSpec or handoff brief.

## Validation and commands

Run from the skill directory:

```bash
python3 -m unittest scripts/test_skill.py -v
python3 scripts/audit_prompt_corpus.py /path/to/public-prompts.json --sample-size 400
python3 scripts/evidence_status.py /path/to/evidence-records.json --now 2026-08-13T00:00:00Z
```

Validate runtime JSON with `scripts/validate_contract.py` or the schemas under `assets/schemas/`. Keep creative decisions human- or model-authored; use scripts only for deterministic validation, compilation, state transition, and evidence aging.

## Quality gates

Do not deliver until all applicable checks pass:

- the route and phase are correct;
- no preview round asks more than three questions;
- image rounds contain exactly three real candidates or honestly declare tool unavailability;
- no final prompt exists before brief confirmation;
- no final image exists before prompt approval;
- platform switching preserves the locked creative brief;
- adapter controls are fresh and verified;
- drama assets bind to continuity locks;
- text in images is checked character by character;
- references have provenance and rights status;
- runtime outputs are outside the skill directory;
- video execution has not been attempted.

## Research provenance

Use `assets/source-ledger.json` for the audited source list and `assets/research-audit.json` for the 4,633-record index and 400-record structural review. Read `references/01-research-ledger.md` before updating either file. Community galleries are discovery sources, never authority for model capability or a repository of reusable finished prompts.
