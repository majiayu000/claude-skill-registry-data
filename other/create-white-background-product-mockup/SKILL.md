---
name: create-white-background-product-mockup
description: Create one clean, product-faithful mockup on a plain white background from a description or supplied reference image. Use for catalog packshots, apparel flat lays, ghost-mannequin presentations, sketch-to-garment mockups, or handbag, shoe, apparel, packaging, and object mockups where geometry, material, color, branding, and visible text must not drift; do not use for lifestyle scenes, decorative commercial backgrounds, transparent cutouts, packaging concept design, or posters.
---

# Product Mockup

Turn one product brief or reference image into one commercial mockup. Treat named tool endpoints as replaceable routes; the durable capability is a selected image model plus a mode-specific Prompt.

## Catalog

- Display name: White Background Product Mockup
- Categories: Commercial Production, Layout & Design
- Status: Ready
- Route label: Model-routed product mockups
- Tone: peach
- Short description: Create product, flat-lay, and ghost-mannequin mockups without identity drift.
- Similar skills: ai-product, product-packaging
## What this skill does

- Extracts only the mockup mode, product, output, framing, and fidelity constraints that change generation.
- Routes an available foundation image model first; treats `flat-lay`, `ai-ghost-mannequin-generator`, and other specialized agents as optional, replaceable accelerators.
- Compiles a photography brief from the user-supplied default Prompt, falling back to a documented API default only when the user has not supplied one.
- Generates one product image per run, checks identity and white-background requirements, and retries only the failed property.

## How to use

Tell the agent whether you want a product mockup, flat lay, ghost mannequin, or sketch-to-garment result, then attach a reference or briefly describe the product.

#### Create from a description

```text
Create a clean white-background mockup of a warm camel-brown square-toe loafer.
```

#### Create from a product reference

```text
Turn this serum bottle photo into a white-background product mockup while keeping the bottle, cap, and label unchanged.
```

#### Create an apparel flat lay

```text
Create a clean white-background flat lay of this garment with no model or hanger.
```

#### Create a ghost-mannequin mockup

```text
Turn this garment photo into a white-background ghost-mannequin image while preserving its shape and details.
```

#### Turn a clothing sketch into a product mockup

```text
Turn this clothing sketch into a realistic white-background garment mockup without changing the design.
```

## Workflow

### 1. Compile the brief

Resolve without unnecessary questions:

```yaml
input: description | one product/garment/sketch reference
mode: product | flat_lay | ghost_mannequin | sketch_to_garment
product: category, count, geometry, material, color, construction
protected: logo, label placement, visible text, distinctive details
view: front | three-quarter | side | user-specified
background: plain white | pure white
ratio: default 1:1
```

Use one product or one pair/set only when the category naturally requires it. Do not infer marketplace compliance when no current channel rules were researched.

### 2. Select the model and route

- Apply the shared [model-selection policy](../../shared/model-selection.md). For a normal product-faithful deliverable, prefer GPT Image 2 Medium at `1:1`, `2K`, and `batchCount: 1`. When demanding studio lighting/material rendering or Asian e-commerce aesthetics are the primary requirement and no readable text must be rendered, consider the current Seedream adapter. Attach every real product reference and never use Midjourney or Z-Image for reference-led work.
- Treat `aiproduct`, `flat-lay`, `ai-ghost-mannequin-generator`, and sketch-to-garment agents as optional routes, not permanent dependencies. Use one only when its current API contract is available, verified, and materially improves the selected mode.
- If a named agent disappears or changes, keep the mode and recompile its Prompt for the best current foundation model instead of removing the Skill capability.
- Do not switch models merely because a run is slow or one output fails acceptance.

### 3. Compile the prompt

Choose the Prompt baseline in this order:

1. The default Prompt supplied in the cleaned tool document.
2. The current API default Prompt, only when the cleaned document has no default.
3. A minimal self-authored baseline, clearly marked as authored rather than sourced, only when neither exists.

For ordinary products, start from: `Generate a mock-up image of [product] in a plain white background. [color: ...], [design: ...].`

For flat lay and ghost mannequin, start from their cleaned default Prompts, then normalize them into the packet below. Do not require their named agents to preserve the capability.

Expand it into this ordered packet, omitting unknown fields rather than inventing them:

```text
Output: one professional catalog mockup of [one product / one natural pair] on a [plain/pure] white seamless background.
Product: [category, count, color, geometry, materials, construction, distinctive details].
View: [front/three-quarter/side], centered, fully visible, realistic scale, clean margins.
Lighting: soft neutral studio lighting, accurate material response, subtle natural contact shadow.
Fidelity lock: preserve exactly [source-backed geometry, proportions, color, material, construction, logo/label placement, visible text]. Do not redesign, simplify, add, remove, mirror, or substitute these details.
Exclude: no props, people, hands, mannequin, packaging, scenery, decorative surface, duplicate product, collage, grid, split screen, watermark, invented logo, or invented text.
```

For description-only generation, replace “preserve exactly” with “render exactly as specified.” Do not claim source fidelity for details that were never supplied.

### 4. Generate and accept

Execute through the WeShop OpenAPI contract. Poll to a terminal state and read the image result, not merely the accepted run.

Accept only when all are true:

1. One separate image contains the requested product count and view.
2. The background is uniform white with no horizon, set, or colored cast.
3. Listed geometry, color, materials, construction, branding, and visible text match the brief/reference.
4. The product is fully visible, centered, sharp, and grounded by at most a subtle natural contact shadow.
5. No unrequested prop, person, package, duplicate, layout, watermark, or fabricated text appears.

Add mode-specific checks:

- `flat_lay`: the complete garment is visible; its construction is preserved; no person, mannequin, hanger, or unintended 3D worn form remains.
- `ghost_mannequin`: no body or mannequin remains; the garment retains believable worn volume; neck, cuff, and hem openings reconstruct naturally without structural drift.
- `sketch_to_garment`: silhouette, panels, seams, openings, pockets, and construction match the source drawing; no redesign or invented feature appears.

### 5. Retry a failed result

Retry once on the same model with a non-identical Prompt that names only the failed property plus the full fidelity lock. Remove secondary styling before changing the model or route. Use a specialized agent only when its current verified contract addresses the failed property; otherwise keep the capability on the best available foundation model. Record the model, optional agent, parameters, Prompt revision, execution ID, terminal error, retryability, refund state, and acceptance failure. Never resubmit an identical failed request.

When this Skill selects GPT Image 2, use `quality: "medium"` and `imageSize: "2K"` by default; change either only when the user explicitly requests another tier.

Every GPT Image 2 call in this Skill defaults to Medium at 2K; use another tier only when the user explicitly requests it.

## User-facing output

- Media type: One product mockup image and a compact acceptance record
- Default quantity: 1 separate image
- Content per image: One product or one natural pair/set at one view
- Default layout: Centered 1:1 catalog composition on white
- Video output: No
- Model policy: Route the best current foundation image model first; use specialized product/flat-lay/ghost agents only while verified and useful
- Downstream use: Catalogs, product pages, marketplace-main-image drafts, and commercial layout handoff
