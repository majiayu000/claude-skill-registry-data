---
name: dircreative-script-breakdown
description: Extract production assets, props, wardrobe, sound, VFX, and special requirements from script.
---

# Script Breakdown

## Required Knowledge

Read only the reference needed for the active task, not this entire list.
The root v2 route owns scope and authorization; legacy records do not add gates.

- `docs/film-preproduction/research/film-production-glossary.md`
- `docs/film-preproduction/research/audio-design-notes.md`
- `docs/film-preproduction/schemas/story-package.yaml`

## Inputs

- approved script

## Outputs

- script breakdown YAML
- asset requirements
- audio policy

## Rules

- Separate image prompt labels, video prompt audio, and post-production audio.
- List every story-critical character, location, prop, wardrobe item, VFX, SFX, and special requirement.
- Do not write shot list or prompt files.

## skill_run_receipt

Persist the following only for a requested formal handoff, pause/resume or actual
execution record. Ordinary work returns its result without a separate receipt.
The next skill is advisory; the controller continues only the requested scope.

Record extracted assets, missing decisions, QA status, and `next_recommended_skill: shot-design`.
