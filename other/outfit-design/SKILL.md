---
name: outfit-design
description: Invent or intentionally redesign the clothing and coordinated accessories worn by one supplied person while preserving their identity, body, pose, and locked scene. Use for complete outfit concepts, fashion restyling, capsule looks, coordinated separates, costume concepts, targeted garment redesign, footwear or accessory design, and style-led wardrobe changes; do not use to place a supplied real garment on a person, preserve an existing outfit while changing the model or pose, create flat product-only garment images, or make ordinary image style filters.
---

# Outfit Design

Create one finished image of the supplied person wearing an intentionally new outfit. Treat the outfit as a designed system of silhouette, pieces, layering, materials, construction, palette, and accessories.

## Catalog

- Display name: Outfit Design
- Kind: Atom
- Categories: Fashion, Layout & Design
- Status: Ready
- Route label: Outfit Generator with GPT Image 2 reference-aware route
- Tone: violet
- Short description: Invent or redesign a coordinated outfit.
## What this skill does

- Designs a complete new look or changes named clothing/accessory slots on one person.
- Separates the high-level fashion concept from concrete garment construction before prompting.
- Preserves the supplied person's identity, body, pose, hands, and locked background.
- Routes supplied real garments to Virtual Try-On instead of redesigning them.
- Returns one finished fashion image per named design direction, never a component board or collage unless explicitly requested elsewhere.

## How to use

#### Design a complete look

```text
Redesign this person’s outfit as modern coastal tailoring in cream and navy.
```

#### Keep one existing piece

```text
Create a new evening outfit around this jacket and leave the jacket unchanged.
```

#### Change one wardrobe slot

```text
Replace only the trousers with a sculptural wide-leg design in charcoal wool.
```

## Workflow

### 1. Bind source roles and boundaries

Require one clear image containing one adult person. Record the target clothing slots, protected existing pieces, allowed accessories, identity/body/pose locks, background policy, framing, and number of named directions.

- Supplied real garment that must remain exact: route to Virtual Try-On or Clothes Changer.
- Same outfit with a different person: route to Fashion Model Replacement.
- Same outfit with a different pose: route to Change Pose.
- Product-only flat lay, ghost mannequin, or sketch-to-garment: route to White Background Product Mockup.
- Multi-image campaign: generate accepted looks separately, then hand them to the relevant social-photo, lookbook, or product-detail Atom when installed.

Read [references/routing-and-api.md](references/routing-and-api.md) before execution and [references/acceptance.md](references/acceptance.md) before accepting a result.

### 2. Resolve the design in two layers

First bind the concept: occasion, audience, climate/season, style tension, silhouette family, coverage, mobility, palette, and formality. Then resolve observable garment attributes: piece list, lengths, volume, neckline, sleeves, waist, closures, seams/panels, layering order, materials, surface treatment, footwear, and accessories.

Do not infer sensitive personality, occupation, gender identity, ethnicity, or body goals from appearance. Use visible fit and the user's brief only. Treat fit as a visual concept, not a physical sizing guarantee.

### 3. Select the route

- **One person + text-described redesign:** prefer `outfit-generator` v1.0 with one concise `textDescription` and `batchCount: 1`.
- **Supplied style/garment references, several protected pieces, exact local change, or dedicated-agent mismatch:** use GPT Image 2 Medium/2K with indexed references and one result.
- **Demanding lighting/material rendering or Asian commercial fashion aesthetics:** consider the current Seedream adapter only when it supports every required reference and no readable text is required.
- **Readable clothing text or multilingual design:** use GPT Image 2 Medium. Render exact supplied copy only; otherwise prohibit invented labels.

Apply the package [model-selection policy](../../shared/model-selection.md). Never run several models merely to compare quality. Choose from the input contract and retry only the failed property.

### 4. Compile one concise Prompt

Start from the cleaned API default, but remove its contradictory request for a composite diagram. Submit one finished-image instruction:

```text
Redesign only the clothing worn by the person as [design direction]. Build the look from [piece list], with [silhouette/layering], [materials/construction], and [palette/accessories]. Preserve the exact face, hair, body proportions, pose, hands, background, lighting, camera, crop, and composition; keep [protected pieces] unchanged. Show one person in one finished image with believable fit, closures, occlusion, and fabric behavior. No component board, annotations, collage, duplicate person, invented branding, or extra garments.
```

Name only high-risk construction details. Avoid long adjective lists, inferred personality analysis, or vague “fashionable” language.

### 5. Execute and verify

Run each named direction independently with `batchCount: 1`. Verify identity, body, pose, hands, scene, target-slot change, protected pieces, coherent outfit construction, anatomy, fabric behavior, and absence of extra people or layout artifacts.

Retry once only when one property fails:

- identity/body drift: shorten the concept and strengthen source locks;
- wrong clothing slot: name replaced and protected pieces explicitly;
- incoherent layers/closures: simplify the piece list and state the wearing order;
- background drift: use the reference-aware GPT Image 2 route and lock the scene;
- missing requested detail: add only that observable construction property.

Do not resend an identical request. Do not turn the correction into Virtual Try-On unless a supplied real garment must be preserved.

## User-facing output

- Media type: One finished fashion image per named direction
- Default quantity: 1
- Default route: `outfit-generator` v1.0 for one-person text redesign
- Reference-aware route: GPT Image 2 Medium/2K
- Required preservation: Identity, body proportions, pose, hands, background, camera, crop, and protected pieces
- Downstream use: Fashion Photoshoot, Change Pose, Poster Design, AI Banner Design, Photo Collage, and lookbook workflows
