---
name: ai-product
description: Place one supplied real product into a new commercial studio, material, lifestyle, or campaign-ready scene while preserving product silhouette, proportions, construction, materials, colors, packaging, labels, logos, controls, and product count. Use for AI product photography, product background replacement, still-life scenes, lifestyle product images, material backdrops, and copy-space variants; do not use for white-background mockups, inventing a new product, packaging design, posters, product-detail layouts, collages, or background removal.
---

# AI Product

Create one product-faithful commercial scene from one real product image. Keep the Atom focused on product plus environment; downstream layout Skills own copy and graphic design.

## Catalog

- Display name: AI Product
- Categories: Commercial Production
- Status: Ready
- Route label: WeShop AI Product or GPT Image 2
- Tone: sage
- Short description: Place a real product into a new commercial scene.
- Similar skills: create-white-background-product-mockup, product-packaging
## What this skill does

- Preserves one supplied product while changing its background, surface, lighting, and commercial context.
- Creates simple studio, material, lifestyle, or copy-space product scenes.
- Generates or accepts an ideal empty background, turns it into an AI Product custom Location, then places the protected product into it.
- Checks product fidelity, segmentation edges, grounding, lighting, scene adherence, and output count.
- Retries only the failed property and never treats a long-running accepted job as failed.

## How to use

Provide one clear product image and describe the setting or commercial use.

#### Create a material studio scene

```text
Place these headphones on a pale oak surface with warm side light and a cream plaster background.
```

#### Create a lifestyle scene

```text
Place this coffee maker in a bright modern kitchen while keeping the exact machine unchanged.
```

#### Reserve copy space

```text
Create a clean campaign-ready product image with the product low-left and empty space above.
```

## Workflow

### 1. Bind one real product

Require one product image. Record:

```yaml
product_locks: silhouette | proportions | construction | components | materials | colors | packaging | label/logo positions | controls | product count
scene_change: background | surface | lighting | shadow | reflections | props | negative space
delivery: count | requested ratio | downstream use
```

Read [references/input-and-acceptance.md](references/input-and-acceptance.md) for transparent, reflective, low-contrast, cropped, multi-product, or heavily occluded sources.

Route a white background to White Background Product Mockup, a new package to Product Packaging, typography to Poster Design or Layout Composition, multiple arranged images to Photo Collage, and a transparent cutout to Background Removal.

### 2. Select the route before writing the Prompt

- **User supplies a background:** accept it as the intended scene and skip background generation.
- **User describes a scene without supplying one:** apply the shared model policy. Use GPT Image 2 Medium/2K normally; use Seedream only for an empty scene whose primary requirement is demanding lighting/material rendering or Asian commercial aesthetics and which contains no readable text. Generate one result with clear product-placement space and do not render the product in this step.
- **Primary placement route:** register the accepted background as an `aiproduct` custom Location, wait until it is complete, then execute `aiproduct` v1.0 with its `locationId`, `generatedContent: "freeCreation"`, `maskType: "autoSubjectSegment"`, and `batchCount: 1`.
- **Exact background pixels or mandatory scene objects:** use GPT Image 2 with numbered product/background roles. A custom Location preserves scene semantics and style but may recompose or omit background objects.
- **Verified caller-supplied product mask:** use `maskType: "custom"` with `customMaskUrl`.
- **Custom Location unavailable or placement fails after one targeted retry:** use GPT Image 2 with numbered product/background roles, `quality: "medium"`, `imageSize: "2K"`, and one result per run.
- **No real product reference:** do not use `aiproduct`; route product concept generation to GPT Image 2 or the appropriate Product Mockup Skill.
- **Exact aspect ratio:** `aiproduct` exposes no ratio field and may retain the source ratio even when ratio language appears in the Prompt. Generate and accept the scene first, then use Expand Image or deterministic cropping when safe; do not promise a Prompt-only ratio.

`generatedContent` is an algorithm preference, not an aspect-ratio field. `freeCreation` releases the source background style while the mask protects the product. Do not expose the WeShop location library when users cannot preview it; create a Location from the user's visible background instead. Read [references/api-and-routing.md](references/api-and-routing.md) before execution.

### 3. Compile two concise Prompts

For background generation, describe one empty environment, surface, light direction, camera, composition, and clear placement area. Explicitly exclude the product and all copy.

```text
Create one empty [ratio] commercial product-photography background: [scene and surface], [light], and a clear empty placement area at [position]. No product, packaging, person, readable text, logo, watermark, or collage.
```

For placement, write product locks first, then bind the accepted Location, grounding, and composition.

```text
Preserve the supplied [product] exactly, including [recognition anchors]. Place this single product in the clear [position] area of the supplied location. Match its perspective and light; add only a realistic contact shadow. Keep the product sharp and dominant.
```

Use the supported negative field:

```text
No changed product geometry, color, material, components, label, logo, controls, or count. No extra product, person, hand, invented accessory, text, watermark, floating object, halo, collage, or clutter.
```

Do not ask the image model to render prices, claims, specifications, badges, or final campaign copy.

### 4. Execute and accept

Visually accept the empty background before creating its custom Location. Poll the Location until `complete`, then submit one product-placement result with `batchCount: 1`. Poll to terminal state. A progress value of `0.99`, long Running state, or early result URL is not failure or completion by itself.

Apply every check in [references/input-and-acceptance.md](references/input-and-acceptance.md). API success is not visual acceptance.

### 5. Retry one failed property

- product drift: shorten scene language and restate only lost product anchors;
- weak or missing scene: verify the intended background was registered and the returned `locationId` was passed; then simplify only the placement instruction;
- invented prop or accessory: name that object in `negTextDescription` and retry once;
- edge halo or old-background residue: use a verified custom mask or cleaner source;
- unrealistic grounding: request one contact surface, one light direction, and a grounded shadow;
- exact ratio mismatch: do not repeat the same `aiproduct` request; route to Expand Image or a safe crop;
- custom Location rejected, a mandatory background object disappears, or the scene is still ignored after a targeted retry: switch to GPT Image 2 with explicit product/background source roles because the failure demonstrates a scene-control mismatch.

Never resend an identical request. Record route, parameters, Prompt revision, execution ID, terminal state, failed acceptance item, and fallback reason.

## User-facing output

- Media type: One product-scene image plus original and acceptance record
- Default quantity: 1 separate image
- Content per image: One preserved product in one coherent commercial environment
- Default layout: One image; no typography, grid, collage, or extra product
- Model policy: GPT Image 2 medium/2K for empty background generation, then AI Product with a custom Location for product placement; GPT Image 2 composition is the fallback
- Downstream use: Product pages, posters, banners, detail layouts, social graphics, and collages
