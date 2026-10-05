---
name: dircreative-script-treatment
description: Turn approved treatment into script-ready scenes, action, dialogue, voiceover, and no-dialogue decisions.
---

# Script Treatment

## Required Knowledge

Read only the reference needed for the active task, not this entire list.
The root v2 route owns scope and authorization; legacy records do not add gates.

- `docs/film-preproduction/chat-co-creation-interface.md`
- `docs/film-preproduction/chat-inline-visualization-interface.md`
- `docs/film-preproduction/creative-copy-deck-capability.md`
- `docs/film-preproduction/professional-agent-voice-standard.md`
- `docs/film-preproduction/schemas/story-package.yaml`
- `docs/film-preproduction/research/audio-design-notes.md`
- `docs/film-preproduction/research/film-production-glossary.md`

## Inputs

- approved treatment
- story review
- audio intent
- approved claim register
- real copy samples and `VOICE PROFILE` when a client or brand voice is requested

## Outputs

- script
- dialogue or no-dialogue policy
- voiceover or no-voiceover policy
- copy-development receipt
- `deck_narrative_spec` when a deck handoff is requested; no PPT output

## Chat Surface

Return the requested script with readable action, dialogue, voiceover and sound.
Timing must support the actual performance capacity. For a script-and-shots
request, review the script internally and continue to shot design. Ask only about
a material unresolved direction or scope change.

## Copy Development Gate

Write with the supplied project/character voice and factual boundaries. When a
specific existing voice is requested, derive a VOICE PROFILE from representative
approved passages; new writing may use a project-register contract. Do not
require 5-20 samples for an original screenplay.

Read `skills/dircreative/references/copy-script.md` for direct language craft.
Use de-AI-writing, shuorenhua or layered Sepia only for an explicit request or a
remaining diagnosed defect; do not run a mandatory rewrite-plus-detector cascade.
`humanizer-zh` is diagnostic only. A phrase hit cannot prove authorship, override
intentional style or create a blocking verdict without actual craft evidence.

When a formal copy_execution handoff is requested, bind samples, protected spans,
findings, claim/evidence IDs and the providers actually applied to that schema.
Pending or unsupported claims block their affected line. Never label a planned
provider call or a self-filled status as executed.

## Deck Narrative Handoff

When the user requests a deck, create `deck_narrative_spec` only after the script direction is approved. The spec must define the communication job, opening tension, cumulative story beats, closing resolution, one narrative job and authoritative `primary_claim_id` per slide, claim/evidence bindings, layout family, composition, primary visual role, text-density budget, and recomputed QA statuses.

Routing rules:

- Editable PowerPoint defaults to `Presentations` with element-level editability.
- `codex-ppt` is allowed only after the user explicitly accepts full-slide images whose contents are not separately editable.
- `high-end-visual-design` may inform aesthetic references, but it is not a PPT construction, editability, or QA authority.
- Stop at the spec. Do not generate slides, slide images, or a `.pptx` in this skill.

## Visual Decision Contract

When visualization adds clarity, use `skills/dircreative/assets/visualizations/stage-surface-registry.json#script-timing-bands`. Bind time bands, dialogue, voiceover, audio, duration budget, and overrun to the current script artifact; approval and revision remain conversation intents with a table fallback.

## Rules

- Separate action, dialogue, voiceover, and sound notes.
- Preserve the approved facts, inferences, audience tension, business objective, proposition, avoid-cliches, concept dependencies, and claim boundaries.
- Write to the approved story duration, not automatically to 15s. If 15s is only the model generation-unit cap, write the full script/treatment first and hand longform splitting to sequence-planner.
- For 60-second client films, create a time budget and VO budget before shot design. Each VO line must include readable VO text, start/end seconds, covered shot IDs, and covered seconds. A VO line may cover multiple shots, but the mapping must be copyable and unambiguous.
- Do not write placeholders such as `VO marks this shot segment`, `VO标注本镜头句段`, or internal production instructions inside VO text.
- Each scene must identify what the character wants, what blocks it, what changes by the end of the scene, and which visible action proves that change.
- Each scene must fill a scene beat card: scene objective, opposing force, tactic change, subtext under dialogue, visible action beat, turn/reveal, and end-state change.
- Dialogue must create pressure, misdirection, reveal, refusal, concession, or choice. Do not use dialogue only to state the theme or decorate the mood.
- The script must preserve the approved story engine: external pressure, hidden relationship engine, irreversible choice/reveal, escalation, consequence, and visible ending action.
- If the script reads as atmosphere without causality, return to story-development instead of continuing to shot design.
- If there is no dialogue, state that explicitly.
- Do not hide an unapproved claim inside dialogue, voiceover, a slogan, a supers line, or a slide title.
- Do not write shot list or prompt files.

## skill_run_receipt

Persist the following only for a requested formal handoff, pause/resume or actual
execution record. Ordinary work returns its result without a separate receipt.
The next skill is advisory; the controller continues only the requested scope.

Record script scope, dialogue policy, copy source set and shortfalls, VOICE PROFILE coverage status, DIR judgment status, de-AI fidelity status, manual-craft status, humanizer review-only status, reconciled trace clusters, approved claim and evidence IDs used, deck claim/evidence/QA handoff status, and `next_recommended_skill: script-breakdown`.
