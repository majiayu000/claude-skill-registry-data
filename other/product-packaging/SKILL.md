---
name: product-packaging
description: Create a structured product packaging concept board from supplied product, brand, logo, color, or structural references. Use for early packaging directions that show conceptual front/back packs, a simplified dieline view, structure details, palette, materials, and finish ideas in one 3:4 presentation image; do not use for manufacturing-ready dielines, engineering dimensions, regulatory copy, or candle mockups.
---

# Product Packaging

Turn product and brand references into one coherent packaging concept board. The durable capability is a selected image model plus a compiled Prompt, not a named packaging endpoint.

## Catalog

- Display name: Product Packaging
- Categories: Commercial Production, Layout & Design
- Status: Ready
- Route label: Model-routed packaging concept
- Tone: lilac
- Short description: Turn product references into a structured packaging concept board.
- Similar skills: ai-product, create-white-background-product-mockup
## What this skill does

- Maps product, logo, color, structure, and style references to explicit roles before generation.
- Starts from the cleaned WeShop Product Packaging default Prompt and compiles only the supplied product facts.
- Routes the best current image model for layout, reference following, and text handling instead of depending on a temporary tool endpoint.
- Produces one presentation board and rejects invented specifications, regulatory copy, or claims that look production-approved.

## How to use

Attach the product and any logo, brand, color, or packaging references, then describe the packaging direction in one sentence.

#### Create a packaging concept

```text
Create a clean packaging concept board for this serum using its amber-and-ivory color palette.
```

#### Use brand references

```text
Use these product and brand references to create a gentle, minimal packaging concept with front, back, structure, palette, and material views.
```

## Workflow

### 1. Compile the brief

```yaml
product_type: supplied or inferred from the product image
reference_roles: product | logo | brand | palette | structure | style
packaging_format: supplied | requested | conceptual recommendation
required_views: front, back, simplified dieline, structure detail, finished mockup
verified_content: exact logo, copy, dimensions, materials, finishes
direction: visual tone, palette, illustration language
ratio: default 3:4
```

Ask only when a missing packaging format, exact copy, or source role would materially change the result. Treat inferred formats, dimensions, materials, and finishes as concepts, never verified production facts.

### 2. Select the model

- Apply the shared [model-selection policy](../../shared/model-selection.md). Packaging with any readable brand, product, regulatory, or promotional copy routes to GPT Image 2 Medium.
- Use an editing model when the task is primarily a controlled update to supplied packaging artwork rather than a new concept board.
- Use a specialized packaging agent only if its current API contract is available, verified, and materially better. The Skill must remain executable through a foundation model if that agent disappears.
- Default a normal packaging concept deliverable to one `3:4`, `2K`, GPT Image 2 Medium result with `batchCount: 1`. Use Low only for an explicitly named structure/layout draft; if text still fails, hand exact copy to deterministic layout rather than switching models.

### 3. Compile the Prompt

Start from the cleaned default Prompt supplied for Product Packaging. Do not search the API for another baseline unless the cleaned document has no default.

Normalize it into this order:

```text
Output: one clean 3:4 professional product-packaging concept board based on the supplied references.
Reference roles: Image 1 is [product]; Image 2 is [logo/brand]; Image 3 is [structure/style], when supplied.
Direction: choose a packaging format appropriate to [product type], or use the exact supplied/requested format. Derive the main palette from the product and pair it with restrained low-saturation supporting colors. Use a [requested or product-appropriate] visual language.
Layout: simplified unfolded dieline on the left; conceptual front and back pack views on the right; structure or closure details below; compact palette, material, and finish swatches alongside; ample white space and clear hierarchy.
Fidelity: preserve the supplied product identity, exact logo artwork, verified colors, and supplied copy. Use neutral placeholders for missing copy.
Truthfulness: show dimensions, materials, finishes, closure mechanics, and printing notes only when supplied; otherwise label them as conceptual or omit exact values.
Exclude: no invented claims, certifications, ingredients, legal copy, barcode, measurements, manufacturing tolerances, fake logo, garbled microtext, unrelated products, or multi-page collage.
```

The board may resemble a professional packaging portfolio presentation, but it is not a production dieline or engineering document.

### 4. Generate and accept

Execute through WeShop OpenAPI, poll to terminal state, and read the returned image result.

Accept only when:

1. One 3:4 board clearly presents the requested packaging direction.
2. Product identity, supplied logo, verified colors, and exact supplied copy remain recognizable.
3. Front, back, simplified dieline, structural detail, palette, and material/finish ideas form a coherent system rather than unrelated variants.
4. The hierarchy is legible and the board has useful white space.
5. No unsupported specification, claim, certification, ingredient, barcode, dimension, or production guarantee appears as fact.
6. The result reads as a concept board, not a manufacturing-ready deliverable.

### 5. Retry a failed result

Retry once on the same model with a non-identical Prompt naming only the failed property. Remove optional illustration and microcopy first when the board is crowded or text is garbled. Reassert reference roles when product or brand identity drifts. Change models only for a demonstrated capability mismatch, and use a specialized packaging agent only while its current contract remains verified. Record model, optional agent, parameters, Prompt revision, execution ID, error, retryability, refund state, and acceptance failure.

When this Skill selects GPT Image 2, use `quality: "medium"` and `imageSize: "2K"` by default; change either only when the user explicitly requests another tier.

Every GPT Image 2 call in this Skill defaults to Medium at 2K; use another tier only when the user explicitly requests it.

## User-facing output

- Media type: One product-packaging concept board and a compact acceptance record
- Default quantity: 1 separate image
- Content per image: One coherent packaging direction with conceptual front, back, dieline, structure, palette, and material views
- Default layout: 3:4 presentation board with ample white space
- Video output: No
- Model policy: Route the best current layout- and reference-capable image model; specialized packaging endpoints are optional
- Downstream use: Packaging exploration, design reviews, brand direction, and briefing a packaging designer
