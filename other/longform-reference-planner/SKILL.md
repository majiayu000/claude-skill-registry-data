---
name: dircreative-longform-reference-planner
description: Build global and per-sequence reference pack contracts for longform AI video workflows.
---

# Longform Reference Planner

## Required Knowledge

Read only the reference needed for the active task, not this entire list.
The root v2 route owns scope and authorization; legacy records do not add gates.

- `docs/film-preproduction/longform-decomposition-policy.md`
- `docs/film-preproduction/capability-aware-generation-policy.md`
- `docs/film-preproduction/reference-locking-policy.md`
- `docs/film-preproduction/schemas/longform-reference-pack.yaml`
- `docs/film-preproduction/schemas/reference-pack-manifest.yaml`
- `docs/film-preproduction/research/model-reference-behavior.md`

## Inputs

- sequence plan
- visual bible
- reference pack manifest
- image prompt manifest
- target model list

## Outputs

- longform reference pack
- global reference pack
- per-sequence reference pack plan
- clean start/end frame requirements
- external generation instructions

## Rules

- Separate global identity/style assets from sequence assets.
- Use sequence packs as the normal unit for 180s work.
- Do not make one clean image per shot unless QA or model constraints require it.
- Every asset must have one primary job and one `asset_output.status`.
- `prompt_only` must remain fully useful without generated files.
- `assisted_generation` requires recorded user authorization.
- `external_generation` must include upload/import instructions.
- Resolve every target through `capability_card_id + version + provider_surface`; never emit family aliases or family-keyed policy maps.
- Copy no numeric reference limit into the pack; validate limits from the exact current card at audit time.
- Keep dense boards out of direct frame slots whenever the exact card requires a clean image input.
- Use clean first/end frames only for exact cards whose reference modes authorize those inputs.
- Do not generate images or videos.

## skill_run_receipt

Persist the following only for a requested formal handoff, pause/resume or actual
execution record. Ordinary work returns its result without a separate receipt.
The next skill is advisory; the controller continues only the requested scope.

Record global packs, sequence packs, output statuses, user gates, exact-card direct input policy, QA status, and `next_recommended_skill: image-prompt-compiler`.
