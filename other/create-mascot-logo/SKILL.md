---
name: create-mascot-logo
description: Create a highly simplified square IP mascot logo through three product-relevant directions and separately generated candidates. Use for cute rounded animal, creature, robot, plant, or object mascots meant to work as a compact brand symbol; do not use for wordmarks, monograms, general logo lockups, detailed character illustrations, avatars, or character reference sheets.
---
# Create Mascot Logo

## Catalog

- Display name: Create Mascot Logo
- Categories: Character, Commercial Production
- Status: Ready
- Route label: GPT Image 2 mascot-logo generation
- Tone: purple
- Short description: Create a compact, cute mascot mark with controlled silhouette, color, and separately labeled directions.
- Similar skills: create-logo
## What this skill does

- Converts product purpose and personality into three concise mascot directions before generation.
- Generates simple square candidates with a rounded small-size silhouette and a controlled three-color contract.
- Keeps each candidate as a separate asset with its own prompt, operation record, and label.

## How to use

Provide the product or brand purpose, audience, personality, mascot subject if known, palette constraints, and desired candidate count.

#### Example

```text
Create six simple mascot-logo candidates for a calm privacy app: use a friendly rounded ghost, a deep navy background, and no text.
```

## Direction gate

1. Read only relevant product context when it is already available. Otherwise ask once for the product purpose, audience, and intended personality.
2. Propose three directions in the form `<subject> — <product connection> — <defining silhouette>`. If the user named a subject, vary its treatment rather than replacing it.
3. Default to six candidates: two variants per accepted direction, labeled `A1`, `A2`, `B1`, `B2`, `C1`, and `C2`. When one direction is selected, label six variants `A1`–`A6`. Honor a different requested count or distribution.
4. Do not spend a generation run until the user has approved the directions and quantity, unless the current request already explicitly authorizes them.

## Visual contract

- Build one dominant, readable silhouette from roughly 4–7 large shapes. Use one species-defining feature at most and keep both members of paired features visible.
- Favor a compact head or upper-body crop, thick rounded forms, blunt ends, simple eyes, and a friendly expression. Remove outlines, texture, anatomy, costume, repeated details, and tiny decoration unless essential for recognition.
- Make the mascot recognizable at small size. Treat the 32 px check as an acceptance review, not a model guarantee.
- Place it upright, emerging from the lower-left or lower-right and filling about 75–85% of the square without cropping an identifying paired feature.
- Default to exactly three semantic color families: two for the mascot and one clearly separated solid background. Incidental shading within a family is acceptable. Follow explicit palette or color-count requests.
- Generate the image only: no text, watermark, border, mockup, card, scenery, extra character, photorealistic material, strong extrusion, or external cast shadow.
- Do not call the asset a logo, brand mark, app icon, or icon inside the generation Prompt; keep that use-case context outside `textDescription`.

## Route and execution

Use `gpt-image` v1.0 / GPT Image 2 with `quality: "medium"`, `imageSize: "2K"`, `aspectRatio: "1:1"`, and `batchCount: 1` for every candidate. Compile one complete semantic `textDescription` from the accepted direction and visual contract. Do not invent a negative-prompt parameter.

Run candidates independently. Persist a unique stable `operationKey` before each submission, require a non-empty `executionId`, and poll every accepted run to terminal state. Do not create a contact sheet or ask one generation to contain several candidates.

Inspect each returned asset for the declared shape, subject count, crop, paired-feature, text, and background invariants. Preserve and report every terminal result, including a result that misses an aesthetic invariant; do not silently filter it. Retry only when the user requests a replacement or a terminal run fails. A replacement uses a new linked operation key and a prompt revised for the observed failure; never blindly resubmit an identical request.


## User-facing output

- Media type: Separate square mascot-logo images plus a labeled receipt
- Default quantity: 6 after direction approval
- Content per image: One simplified mascot on one solid full-canvas background
- Default layout: Independent 1:1 assets, never a grid or contact sheet
- Model policy: GPT Image 2 Medium/2K, one candidate per run
- Downstream use: Mascot selection, brand-system refinement, and small-size application testing
