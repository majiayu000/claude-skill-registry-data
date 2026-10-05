---
name: fashion-model-replacement
description: Replace the person or mannequin in an already-dressed fashion image while preserving the complete outfit, garment construction, fit cues, branding, pose, crop, and requested scene. Use when a user asks for a different fashion model, mannequin-to-human conversion, market-specific adult model, text-described model, or supplied target-person reference; do not use for putting a separate garment on a person, changing only pose, inventing an outfit, face-only entertainment swaps, or general photoshoots.
---

# Fashion Model Replacement

Produce one dressed-model image. Define the Skill by the replacement job and preservation contract, not by `aimodel`, a model library, or any single engine.

## Catalog

- Display name: Fashion Model Replacement
- Categories: Fashion, Commercial Production
- Status: Ready
- Route label: WeShop AI Model or GPT Image 2
- Tone: coral
- Short description: Replace a fashion model while keeping the outfit intact.
- Similar skills: change-pose, virtual-try-on
## What this skill does

- Replaces a person or mannequin already wearing the product.
- Generates a suitable adult model from a concise description when no target-model image is supplied.
- Routes between the currently verified WeShop AI Model contract, newer verified WeShop replacement routes, and GPT Image 2 according to inputs.
- Verifies outfit, anatomy, identity/reference, pose, crop, and scene continuity.

## How to use

Provide one already-dressed fashion image, then describe the new model or attach a supplied target-model reference.

#### Describe a new model

```text
Replace the model with an adult Black woman with short natural curls and keep the complete outfit, pose, and studio unchanged.
```

#### Use a model reference

```text
Replace the person in this fashion image with the supplied model reference while preserving the outfit and composition.
```

#### Replace a mannequin

```text
Turn this dressed mannequin image into a natural adult fashion-model photo without changing the clothing.
```

## Workflow

### 1. Confirm the replacement job

Require an already-dressed person or mannequin source. Compile:

```yaml
source: dressed-person | dressed-mannequin
target_model: supplied-reference | text-description | minimally-generated-adult
replace: whole model | mannequin-to-human
outfit_locks: garments | fit cues | accessories | footwear | branding
image_locks: pose | crop | camera | background | lighting | composition
delivery: count | ratio | resolution
```

Do not route a separate garment plus person here; use Virtual Try-On. Do not route pose-only work, outfit invention, or a general campaign reshoot here.

### 2. Build the model brief

Read [references/model-brief-and-acceptance.md](references/model-brief-and-acceptance.md). When no target reference is supplied:

- use the user's explicit adult model description;
- ask one short question only when target audience or model presentation materially changes the commercial result;
- otherwise generate a neutral adult commercial fashion model with natural features and expression;
- do not browse or expose WeShop model/location libraries without a preview surface;
- pass an existing user-supplied `fashionModelId` only when the user explicitly provides it.

### 3. Select the route and mask before spending a run

- **Supplied target-model reference:** prefer `gpt-image` v1.0 / GPT Image 2 because it accepts the dressed source and target-person reference together. Default to `quality: "medium"`, `imageSize: "2K"`, requested/auto ratio, and `batchCount: 1`.
- **Text-described identity/head replacement with background locked:** use the best currently documented WeShop AI Model route. The verified route is `aimodel` v1.0 with `generatedContent: "freeCreation"`, `maskType: "autoHumanSegment"`, `pose: "originalImagePose"`, no `locationId`, and a concise model description. This preserves body and background while replacing face/head.
- **Whole-model or body-type replacement:** prefer GPT Image 2 or a verified `customMaskUrl` workflow. Do not use `autoHumanSegment` when the requested body itself must change.
- **Whole model may be regenerated and background is released:** `autoApparelSegment` may be used to lock only the complete outfit. Never select it when the background must stay unchanged.
- **Exact target appearance:** prefer GPT Image 2 with a supplied target-model reference. Without a target reference, treat fine hair and facial language as guidance rather than an identity guarantee.
- **Mannequin-to-human or difficult free-form replacement:** choose between the current WeShop route and GPT Image 2 based on garment segmentation versus multi-reference/prompt control.
- **Swap Model & BG / `changemodelbg`:** use only after its full execution contract is available and verified; do not infer parameters from the marketing page.

Read [references/api-parameters.md](references/api-parameters.md) before constructing an `aimodel` request. Never use a mask whose protected region conflicts with the user's invariants.

Do not step through WeShop 1.0, WeShop 2.0, and GPT Image 2 as a quality ladder. Choose once from the inputs. Record the reason for every fallback.

### 4. Compile one concise Prompt

Text-described WeShop route:

```text
Replace the current model identity with [short adult model brief]. Preserve the original body, complete outfit, pose, hands, crop, background, lighting, shadows, camera, and composition unchanged.
```

GPT Image 2 with reference:

```text
Replace the person in Image 1 with the adult person from Image 2. Preserve Image 1's complete outfit, [recognition anchors], fit cues, pose, crop, background, lighting, and composition. Integrate the new head and body naturally. One person only; no outfit redesign, extra accessory, text, duplicate, or collage.
```

Use negative Prompt fields only when the selected route supports them. Do not submit demographic checklists, beauty scoring, or generic fashion adjectives that do not affect the requested result.

### 5. Execute and accept

Upload real originals, submit one result, poll to terminal state, and inspect the image. Keep the dressed source and any target-person reference as separate Original assets.

Apply the six checks in [references/model-brief-and-acceptance.md](references/model-brief-and-acceptance.md). API success is not acceptance.

### 6. Retry one failed property

- outfit drift: reduce model/scene language and reassert only lost garment anchors;
- incorrect target appearance: restate two or three observable model attributes or strengthen the supplied reference role;
- anatomy or neck seam: target that junction without changing outfit or scene;
- scene/pose drift: reassert the original pose, crop, background, lighting, and composition;
- target-reference mismatch on WeShop route: switch to GPT Image 2 with both originals;
- segmentation failure on GPT Image 2: switch to the verified WeShop apparel-mask route.

Never resend an identical request. Record route, model version, parameters, Prompt, execution ID, terminal status, error/refund state, failed acceptance item, and fallback reason.

## User-facing output

- Media type: One fashion model replacement image plus a compact source and acceptance record
- Default quantity: 1 separate image
- Content per image: One replacement model wearing the preserved source outfit
- Default layout: Preserve source pose, crop, camera, scene, lighting, and composition
- Video output: No
- Model policy: Text-described replacement uses the best verified WeShop AI Model route; supplied model references prefer GPT Image 2 medium/2K
- Downstream use: Pose variants, fashion photoshoots, lookbooks, product pages, posters, banners, and collages
