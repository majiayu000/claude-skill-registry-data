---
name: make-product-commercial
description: Direct and produce one short product commercial from a locked brief, claim ledger, timed treatment, continuity plan, and verified image/video operations. Use when the final result is a coherent 5–30 second advertisement in which a supplied product and its truthful benefit drive the story; do not use for one generic cinematic shot, standalone product photography, influencer talking portraits, editing only supplied footage, or long-form brand films.
---
# Make Product Commercial

## Catalog

- Display name: Make Product Commercial
- Categories: Commercial Production, Video
- Status: Ready
- Route label: Product-safe multi-shot video composition
- Tone: purple
- Short description: Produce one truthful, continuity-safe short commercial in which the supplied product drives the action.
- Similar skills: minimalist-product-ad-generator, product-launch-video
## What this skill does

- Locks product truth, audience promise, duration, CTA, and claim evidence before creative treatment.
- Converts one approved treatment into timed atomic shots with stable product, cast, space, light, and screen-direction anchors.
- Generates and assembles only the required shots, then inspects the complete commercial for product fidelity, timing, claims, sound, and CTA.

## How to use

Provide product images or a precise product brief, audience, market, truthful benefit, duration, ratio, placement, required/forbidden claims, brand rules, CTA, voiceover preference, and any cast or first/last-frame references.

#### Example

```text
Make a 15-second 9:16 commercial for this insulated bottle. Preserve its exact teal color and label, show the leakproof lid causing the bag-safe benefit, use natural sound plus a short English voiceover, and end on the supplied packshot with “Carry calm.”
```

## Workflow

1. Freeze a brief with product identity, exact supplied facts, audience tension, single promise, evidence, market, duration, ratio, placement, CTA, audio, required assets, and prohibited inventions. Do not infer certifications, performance numbers, ingredients, medical effects, comparisons, or trademarks.
2. Propose one concise treatment unless the user requests options: opening hook, product-caused progression, proof moment, emotional/functional payoff, and end card. Continue through the supported generation route without a client-side payment confirmation.
3. Build a timecoded shot manifest totaling the requested duration. Give every shot one observable product action, camera instruction, environment, lighting, cast state, product-state anchor, sound/voice beat, transition intent, and acceptance condition. Keep a single-shot commercial single-shot.
4. Select exactly one cataloged model per generated shot before submission: Kling 3.0 for supplied-product or precise one/two-frame control; Kling V3 Omni for several named product/cast/scene references or a motion-reference video; Seedance 2.5 for long multimodal, audio-visual, artistic, or talking-performance shots; Veo 3.1 for one-source-image premium synchronous dialogue/SFX at 16:9 or 9:16; Seedance 2.0 for routine image-led shots; MiniMax H3 for justified large-amplitude or natural human motion. Do not trial models in sequence or silently downgrade while the chosen route remains available.
5. Use the downstream route's native fields only. Persist a unique stable `operationKey` per shot, require an `executionId`, poll to terminal state, and download each terminal-success MP4. Generate missing still assets through a suitable image Atom; do not ask a video model to repair a source product image implicitly.
6. Inspect first, middle, and last frames of every shot for product geometry, label, color, action, cast identity, screen direction, camera, duration, ratio, audio, and forbidden additions. A failed or rejected shot gets one new linked key and an error-responsive prompt; accepted shots are not regenerated.
7. When multiple clips are required, pass only accepted clips in manifest order to `$combine-videos`. Add exact text, logo, CTA, captions, voiceover, music, or final mix through deterministic editing when generated media cannot guarantee them.
8. Inspect the assembled commercial end to end: exact duration/ratio, 0–3 second hook, causal product role, continuity, claim truth, intelligible audio, exact CTA/end card, no blank/corrupt frames, and no unintended watermark. Report every retained limitation and do not add a client-side publication confirmation; follow the API result.


## User-facing output

- Media type: One final MP4 plus treatment, shot manifest, claim ledger, and operation receipt
- Default quantity: 1 commercial; one cut only unless alternates are explicitly requested
- Content per video: Hook, product-caused proof/progression, payoff, and CTA within the requested duration
- Default layout: User-requested placement ratio; preserve a supplied end card when provided
- Model policy: Kling 3 precise product/frames; Kling Omni complex/motion references; Seedance 2.5 long audiovisual/artistic/performance; Veo source-image synchronous audio; Seedance 2.0 routine; H3 large/natural motion
- Downstream use: Human brand/legal review and manual campaign publishing
