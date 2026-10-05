---
name: dircreative-edit-assembly-planner
description: Convert sequence plans and generated clip receipts into edit assembly, continuity, audio, and retry guidance.
---

# Edit Assembly Planner

## Required Knowledge

Read only the reference needed for the active task, not this entire list.
The root v2 route owns scope and authorization; legacy records do not add gates.

- `docs/film-preproduction/longform-decomposition-policy.md`
- `docs/film-preproduction/capability-aware-generation-policy.md`
- `docs/film-preproduction/schemas/sequence-plan.yaml`
- `docs/film-preproduction/schemas/longform-reference-pack.yaml`
- `docs/film-preproduction/research/audio-design-notes.md`

## Inputs

- sequence plan
- longform reference pack
- video prompt manifest
- generation QA report or external clip list

## Outputs

- edit assembly plan
- sequence order
- transition notes
- audio spine
- continuity check list
- retry priority list

## Rules

- Keep generated clip order tied to sequence IDs.
- State incoming and outgoing transition intent for each sequence.
- Keep audio policy separate from image prompts.
- Do not assume generated clips exist in `prompt_only` mode.
- If clips are missing, output an external generation checklist instead of pretending the edit is ready.
- Do not generate or edit videos.

## skill_run_receipt

Persist the following only for a requested formal handoff, pause/resume or actual
execution record. Ordinary work returns its result without a separate receipt.
The next skill is advisory; the controller continues only the requested scope.

Record clip availability, edit order, audio handoff, continuity risks, missing assets, retry priorities, QA status, and `next_recommended_skill: generation-qa`.
