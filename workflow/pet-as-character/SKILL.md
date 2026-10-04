---
name: pet-as-character
description: Generate a cute desktop-pet animal character as transparent-background PNG frames - one consistent creature redrawn in several poses and expressions for an always-on-top desktop companion. Use when creating or replacing the briffy pet, or any animated desktop mascot sprite set. Not for icons, logos or app marks.
---

# Pet as Character

Adapted from [ip-as-logo](https://github.com/s1dashu/ip-as-logo-skill) (MIT). The taste is the same - extremely simplified, rounded, heavy, cute, barely-there dimensionality. The output is not: this skill draws a **living creature that stands on the user's desktop**, not a square mark on a coloured tile.

## What differs from ip-as-logo

| ip-as-logo | this skill |
| --- | --- |
| one solid named background colour, part of the design | **flat key colour that gets removed** - the delivered asset is a hard cutout with alpha |
| character emerges from the lower-left or lower-right corner, cropped | **centred, upright, complete body**, nothing cropped, even margin on all four sides |
| must read at `32 x 32` | must read at about `110 px` tall - its real size on screen |
| `4-7` shapes, exactly 2 IP colours + background | `5-9` shapes, 2 base colours + 1 small warm accent |
| one-pass batch, never use a previous candidate as a reference | after the character is chosen, **every later frame uses it as an image reference** - identity consistency outranks reproducibility |
| one image is the deliverable | **a frame set** is the deliverable: one creature, many expressions |
| square `1:1`, `1536 x 1536` | square `1:1`, `1024 x 1024` is enough (the pet window is `120 px`) |

Everything not listed here is inherited from ip-as-logo unchanged.

## Workflow

1. Parse the request for an explicit animal subject and available product context. Do not ask the user to choose a colour mode.
2. When no subject is given and the workspace is a product repository, read the README, product docs, package metadata and existing pet code before asking anything. An existing pet in the code is strong evidence of the intended species - keep it unless the user asks for a change.
3. When product context is insufficient, ask one consolidated round of questions covering what the product does, who it serves, and how the pet should feel. Do not start a second questionnaire.
4. Present three concise directions before generating, one compact line each: `<animal> - <product connection> - <defining silhouette>`. Then propose the identity batch: **six centred candidates**. Do not generate until the user agrees, unless the request already authorises it.
5. Choose the three directions deliberately. Prefer familiar, broadly lovable animals. Tie each one to a different product attribute or promise; do not return three arbitrary animals with no rationale.
6. **Identity batch.** On approval, generate six independent candidates labelled `A1`, `A2`, `B1`, `B2`, `C1`, `C2` - two per direction. There is no corner assignment: every candidate is centred and upright. Vary silhouette, ear and muzzle proportion, colour strategy and expression between the two variants of a direction.
7. **Frame set.** The user picks exactly one candidate. That file becomes the identity reference. Generate every pose in the frame set below by passing the chosen image to the model as a reference and asking for the same creature in a new pose. Never re-describe the creature from scratch for a frame - identity drift is the one failure mode that ruins a desktop pet.
8. Require a top-tier image model: prefer GPT Image 2 (it can return real transparency directly); also support Nano Banana Pro (Gemini Image Pro), Nano Banana 2, or Seedance 5.0 Pro. Never fall back to SVG or to drawing the creature by hand in code. Use another model only with the user's explicit consent.
9. Run the cutout step on every returned image. This skill *does* post-process: alpha is not decoration here, it is the deliverable. This is a deliberate departure from ip-as-logo's deliver-as-is rule, and it is the only inspection allowed - never filter, rank or silently retry a draw for its colours, composition, shading or dimensionality.
10. Report every label, direction and rationale, saved path, prompt, and dimensions. Present all results together; generate replacements only when the user explicitly asks for another draw.

## Frame set

One creature, redrawn. Each frame is a separate full-resolution square asset - never a sprite sheet, grid or contact sheet, because the cutout step needs clean margins around a single body.

| frame | app state | pose |
| --- | --- | --- |
| `idle` | resting | calm, upright, eyes open, faint friendly smile - the canonical pose |
| `blink` | resting | identical to `idle` except both eyes are closed as two soft downward arcs |
| `capture` | screenshot taken | eyes wide and round with surprise, small open mouth, body straight and alert |
| `think` | processing | eyes looking up and to one side, head tilted a little, one front paw touching the cheek |
| `listen` | recording | ears perked high and forward, head tilted toward the listener, mouth slightly open, attentive |
| `happy` | success | eyes as two upward happy arcs, wide smile, body leaning back in a small delighted hop |
| `sad` | error | ears drooping, eyes looking down, flat small mouth, shoulders lowered |
| `sleep` | hidden / long idle | sitting curled, eyes closed, head tipped to one side, completely relaxed |

`idle` and `blink` must be pixel-comparable: same body, same position, same scale, only the eyes differ. Ask for that explicitly.

Overlays the app draws itself in the DOM - the recording ring, thinking dots, capture flash, unread badge, mic bubble - must **not** appear in any frame. Do not draw props, tools, cameras, microphones, notebooks or speech bubbles.

## Complexity budget

- One dominant continuous outer silhouette from roughly `5-9` large basic geometric shapes. Merge or delete any shape that does not carry identity, expression or recognition.
- At most one species-defining feature: one bushy tail, one pair of round ears, one broad muzzle.
- At most two broad internal colour regions from the two base colours, plus one small warm accent (cheeks, inner ears, nose or paw pads).
- Face is two eyes plus one small mouth. Omit eyebrows, nostrils, whisker texture, fur strands, outlines and decorative marks unless essential for recognition.
- Show a **complete body**: head, torso, both front limbs, both feet, and the tail or its equivalent. A logo can be a floating head; a desktop pet cannot.
- Simplification, cuteness and an endearing baby-like personality are decisive. Large head, compact body, short limbs, soft cheeks, widely spaced simple eyes.
- Require a readable black silhouette and recognisability at about `110 px` tall. If a feature turns to noise at that size, enlarge, merge or remove it.

## Shape language and composition

- Thick, rounded, weighty contours and broad colour masses. No outline stroke around the body.
- Forbid sharp corners, pointed ears, needle tails, thin antennae, thin smiles, narrow gaps and acute tips. Every necessary tip ends visibly blunt and rounded.
- Show both members of every paired feature - ears, arms, feet.
- **Centre the creature horizontally, upright, facing the viewer.** The whole body sits inside the square with a clear even margin on all four sides. Nothing is cropped; nothing touches an edge. The cutout step needs that margin, and the app applies its own CSS drop shadow into it.
- The creature fills about `75-85%` of the square height and rests on an invisible floor a little above the bottom edge.
- Never place the creature in a corner, never crop it, never rotate or tilt the canvas.
- No ground shadow, platform, pedestal, podium or reflection - the pet stands on the user's wallpaper, and a baked-in shadow reads as a sticker.

## Colour and canvas

- Two base colours organised into broad purposeful masses, plus one small warm accent. Reuse the base colours for facial marks rather than adding semantic colours.
- Choose the colours from the product context, subject identity and intended personality. Favour clear, lively, warm colours - the pet sits on an unknown wallpaper and must stay legible on both light and dark desktops.
- Avoid a body that is mostly white, mostly black or mostly mid-grey: it disappears against one desktop theme or the other.
- **The background is a disposable key colour, not a design element.** Name one flat uniform key colour and require it to be absent from the creature. Default `#00B140` chroma green; use `#FF00FF` magenta when the creature is green, or any strongly saturated colour far from every colour in the creature.
- Never use the words `transparent`, `alpha`, `opaque`, `PNG` or `cutout` in the generation prompt for a model without a real transparency parameter - they distract it. Ask for a flat solid key colour instead and remove it afterwards.
- When the model exposes a real transparency parameter (GPT Image 2 `background: transparent`), use it and skip the key colour: set the background instruction to plain transparency and let the cutout step trim only.
- Generate a direct `1:1` square, `1024 x 1024`, with square outer corners. Accept and preserve a different native size when that is the service limit; never resample merely to reach the requested number.

## Prompt skeleton - identity draw

Describe the requested visual as an image only. Never tell the image generator that the result is a `logo`, `brand mark`, `app icon`, `icon asset`, `sprite`, `game asset` or `desktop pet`. This rule applies only to the generation prompt; the conversation and the skill name may describe the project freely.

For modern instruction-following models keep the exclusions inside the `Constraints:` line. For an older runtime exposing a dedicated `negative_prompt` parameter, move that line into the parameter and drop it from the main prompt.

```text
Create one complete full-bleed 1:1 square image.
Background: fill the entire square with a completely flat, uniform <keycolor>. Keep it perfectly even everywhere, with no gradient, texture, shadow, vignette or lighting variation. No colour in the creature may be <keycolor> or a near shade of it.
Subject: place one extremely simplified, cute, endearing <subject> on the background, drawn as a complete standing body - head, torso, both front limbs, both feet and <defining feature> - reduced to one soft rounded continuous silhouette.
Placement: centre the creature horizontally, upright, facing the viewer. Fit the whole body inside the square with a clear even margin on all four sides so nothing is cropped and nothing touches an edge. The creature fills about 80% of the square height and rests on an invisible floor a little above the bottom edge.
Complexity: use only 5-9 large basic shapes, at most two broad internal colour regions and one small accent. Use two simple eyes and one small mouth. Remove every nonessential line, outline, anatomical detail, texture and decoration. Keep the creature readable when it is only 110 pixels tall.
Colour behaviour: use two base colours organised into broad purposeful masses, plus one small warm accent for the cheeks, inner ears or nose. Reuse the base colours for the facial marks. Favour clear, lively, warm colours, and keep the creature clearly separated from the background. Do not make the body mostly white, mostly black or mostly grey.
Expression: <expression>.
Style: make simplification, cuteness and lovable baby-like appeal the strongest qualities. Use a large head, a compact body, short limbs, soft cheeks, widely spaced simple eyes, thick rounded contours and an ultra-clean graphic treatment. Prefer one clear shape over several explanatory details. Add an extremely, extremely subtle, almost imperceptible sense of depth.
Finish: show only the creature on the flat background, with clean surfaces and normal square outer corners.
Constraints: Use no text or watermark. Add no borders, frames, cards or presentation masks. Include one creature only, with no extra subjects, props, scenery, ground shadow, platform or pedestal. Use no fragile lines, sharp tips, unnecessary outlines, tiny details or decorative marks. Add no photorealistic material, dramatic bevel, glossy hotspot, deep occlusion, extrusion, strong three-dimensional rendering or external cast shadow. Keep the background solid and uniform, with no texture, vignette or lighting variation.
```

## Prompt skeleton - frame draw

Always send the chosen identity image as a reference alongside this prompt.

```text
Redraw the creature in the attached image exactly as it is - identical species, silhouette, proportions, colours, level of simplification and drawing style - in one new pose.
New pose: <pose>.
Keep everything else unchanged: the same two base colours and the same accent, the same head-to-body ratio, the same eye spacing and shape language, the same flat uniform <keycolor> background filling the whole square.
Placement: centre the creature horizontally, upright, complete, with a clear even margin on all four sides so nothing is cropped and nothing touches an edge. Keep the creature the same size as in the reference, filling about 80% of the square height.
Constraints: Change nothing except the pose and expression. Use no text or watermark, no props, no extra subjects, no scenery, no ground shadow, no platform, no borders or frames. Add no new colours, outlines, details or decorations. Keep the background solid and uniform.
```

## Post-processing

Run `node scripts/pet-cutout.js` after every draw. It:

1. detects real alpha and skips keying when the model already returned transparency;
2. otherwise flood-fills the key colour inward from the four edges, so a same-coloured region enclosed by the body is never punched out by mistake;
3. ramps alpha across the antialiased rim by colour distance and de-spills the key colour from the remaining fringe;
4. trims to the alpha bounding box, re-squares, pads for the CSS drop shadow, and writes `240 x 240` (`@2x`) and `120 x 120` frames into `assets/pet/`.

Reject a draw only when the cutout reports an unrecoverable background - a gradient, a shadow under the feet, or the creature touching an edge. That is a mechanical failure, not an aesthetic judgement.

## Delivery behavior

- Treat each batch as a one-pass creative draw. Generate every requested candidate once and deliver every returned image, cut out.
- Do not rank candidates as recommended or non-recommended, and do not automatically retry a result because of its colours, detail, composition, gradient, shading or dimensionality.
- Report the model, the constraint-delivery mode, the key colour, and the cutout result for every frame.
