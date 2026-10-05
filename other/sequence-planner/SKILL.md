---
name: dircreative-sequence-planner
description: Split the requested film into performance-sized model units with continuity and edit handoffs.
---

# Sequence Planner

## Required Knowledge

Read only the reference needed for the active task, not this entire list.
The root v2 route owns scope and authorization; legacy records do not add gates.

- `docs/film-preproduction/longform-decomposition-policy.md`
- `docs/film-preproduction/capability-aware-generation-policy.md`
- `docs/film-preproduction/schemas/sequence-plan.yaml`
- `docs/film-preproduction/schemas/shot-list.yaml`
- `docs/film-preproduction/research/channel-playbooks.md`

## Inputs

- selected concept
- treatment or script
- shot list
- target duration
- channel and model targets

## Outputs

- sequence plan
- generation unit policy
- user gate map
- edit handoff skeleton

## Rules

- Default 180s work to `longform_generation_mode: hybrid`.
- Default `visual_output_mode` to `prompt_only` unless the user authorizes generation.
- Plan the whole film before any per-sequence reference prompts.
- Resolve the actual selected capability card before setting a generation-unit ceiling; it is separate from story duration.
- If the user names a model limit, preserve that value as a production constraint without inventing the story duration.
- Size units from performance capacity and the exact supported range. Avoid arbitrary durations and preserve adjacent visual/audio states.
- Keep each sequence's dramatic function distinct.
- Do not create images or videos.
- Mark batch mode with accepted continuity and rework risks.
- Preserve global continuity anchors for identity, product, wardrobe, location, lens, light, and audio.

## skill_run_receipt

Persist the following only for a requested formal handoff, pause/resume or actual
execution record. Ordinary work returns its result without a separate receipt.
The next skill is advisory; the controller continues only the requested scope.

Record duration split, mode choice, user gates, unresolved continuity questions, QA status, and `next_recommended_skill: longform-reference-planner`.
