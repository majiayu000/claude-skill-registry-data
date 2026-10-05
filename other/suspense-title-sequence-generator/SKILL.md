---
name: suspense-title-sequence-generator
description: Create one suspense pop-art film title sequence from supplied title and credit facts, six approved graphic keyframes, a locked motion-graphics plan, exact-copy finishing, and final readability QC. Use when the six-anchor suspense package, supplied-credit discipline, and graphic transitions are the requested outcome. Unlike make-video-intro (relationship 0.61), this is a film-specific multi-shot title package rather than a reusable brand sting; unlike make-kinetic-typography (0.59), it owns visual narrative and keyframes, not type alone. Unlike a general cinematic title-sequence candidate (0.95), choose this when this suspense pop-art grammar is decisive. Do not use for invented credits, named-IP imitation, a generic opening, or a text-only title card.
---
# Suspense Title Sequence Generator

## Catalog

- Display name: Suspense Title Sequence Generator
- Categories: Film, Video
- Status: Ready
- Featured: yes
- Route label: Six-anchor graphic title composition
- Tone: purple
- Short description: Produce a suspense pop-art film title sequence with exact supplied credits and graphic-motion QC.
## What this skill does

- Locks title, credits, film cues, reference roles, and a six-keyframe structure before paid generation.
- Produces graphic keyframes as approved visual anchors, then animates a coherent title package around them.
- Keeps supplied English title/credit copy exact through deterministic finishing and checks every hold for readability.

## How to use

Provide film type, title, one-line logline, cast, only the credit roles/names that should appear, and supplied character/prop/scene/style references. State ratio, duration, language, and audio preference.

#### Example

```text
Create a 15-second 16:9 suspense title sequence for “GLASS SIGNAL.” Use the supplied cast and director credit only, six saturated red/yellow/blue graphic keyframes, vinyl and evidence-wall motifs, exact English credits, and no Chinese on-screen text.
```

## Workflow

1. Lock film type, exact title, supplied credit roles/names, logline, duration, ratio, language, reference roles, audio plan, and forbidden content. Never invent missing roles/names, turn a director into another credit, or use placeholder text.
2. Classify references as protagonist, supporting character, prop, scene, style, or shot reference. Preserve supplied identity cues while restaging them in an original graphic treatment; do not reproduce frames from an existing title sequence or IP.
3. Write six Chinese keyframe prompts and show them for approval. Each keyframe locks 16:9 composition, character placement, prop count, color blocks, title/credit placement, and the next transition. Use supplied English title/credits only; no story logline appears on screen.
4. Generate and inspect each approved keyframe with a current text-safe image route. Persist one `operationKey` per keyframe, require `executionId`, poll terminal state, and regenerate only a failing keyframe with a linked revised key. If text is unreliable, use deterministic supplied type instead of accepting garbling.
5. Compile one coherent 15-second motion-graphics sequence from the six accepted anchors. Select a current video route suited to the approved references; use one durable key, terminal polling, and no blind retry. Preserve graphic panels, masks, transitions, supplied credits, and final title hold.
6. Add exact title/credits deterministically where generation cannot preserve spelling. Inspect keyframes and final playback for copy, line breaks, readability, credit omission/invention, composition, transition continuity, duration, ratio, audio, and final freeze/hold. Do not add a client-side publication confirmation; follow the API result.


## User-facing output

- Media type: One final MP4 plus credit ledger, six keyframes, motion plan, and operation receipts
- Default quantity: 1 title sequence
- Content per video: Six graphic suspense beats with exact supplied title and credits
- Default layout: 15 seconds and 16:9 by default; use requested ratio/duration when the approved route supports it
- Model policy: Text-safe image route for anchors; current catalog video route for the approved motion plan; deterministic exact-copy finishing
- Downstream use: Human title, credit, creative, and publication review
