---
name: product-detail-page
description: Research the current requirements of a named ecommerce marketplace, then create one coherent modular product-detail image set from supplied product assets and verified facts, delivering separate upload-ready modules plus an optional stitched long-page preview. Use for Amazon A+ content, Shopify or DTC product pages, and marketplace detail pages that need hero, feature, detail, scenario, usage, specification, comparison, trust, or closing modules; do not use for a single listing main image, a generic poster, an unverified sales-claim page, or one monolithic AI-generated long image.
---

# Product Detail Page

Create one product-detail deliverable as a set of independent modules. Treat a long page as an ordered assembly of those modules, never as one model-generated canvas.

## Catalog

- Kind: Atom
- Display name: Product Detail Page
- Categories: Commercial Production, Layout & Design
- Status: Ready
- Route label: Researched modular PDP production
- Tone: teal
- Short description: Build modular ecommerce detail-page image sets.
- Similar skills: ai-banner-design, make-thumbnail, poster-design
## What this skill does

- Researches the target platform and locale before choosing dimensions, module types, upload form, copy placement, file limits, or synthetic-media requirements.
- Converts verified product facts into a buyer-decision sequence rather than a stack of unrelated promotional images.
- Produces each hero, feature, detail, scenario, instruction, specification, comparison, trust, or closing section as an independent module.
- Calls existing Atom Skills when they own a required asset, then keeps product identity and the page visual system consistent across every module.
- Delivers separate modules as the source of truth and optionally stitches them into a long-page preview or upload asset.

## How to use

Provide the target platform and locale, real product images, product name/category, verified facts, required copy, brand assets, and preferred delivery form. If the platform is omitted, research the likely destinations and ask only when their delivery structures materially conflict.

#### Create a marketplace detail page

```text
Research the current requirements for Amazon US A+ Content, then create a modular detail page for this portable blender from the supplied product images and verified specifications.
```

#### Create modules and a stitched long page

```text
Create a Chinese ecommerce product detail page for this shoe. Deliver every section separately and also stitch the accepted sections into one long-page preview.
```

#### Adapt one asset set to two destinations

```text
Use these verified product assets to prepare one Shopify product-page image set and one marketplace long-detail version without inventing claims.
```

## Workflow

### 1. Research the destination first

Read [references/platform-research.md](references/platform-research.md), then search current official documentation for the named platform, country, account/content tier, and upload surface. Record:

```yaml
platform: name, locale, seller surface
retrieved_at: current date
official_sources: direct URLs
delivery_model: fixed modules | independent media | long image | mixed
module_or_slot_limits: verified values or seller-backend-confirmation
image_rules: dimensions, ratio, format, size, text restrictions
mobile_behavior: stacking, crop, safe area, minimum readability
required_metadata: alt text, synthetic-media label, locale fields
prohibited_content: claims, badges, prices, contacts, reviews, guarantees
```

Do not rely on memorized platform numbers. Prefer the platform's official seller/help documentation. Mark anything visible only inside a seller dashboard as `seller-backend-confirmation`; never invent a precise specification.

When account tier changes the available modules or dimensions, request the tier or a current seller-dashboard screenshot before final export. You may plan a tier-neutral module sequence first, but do not label guessed dimensions upload-ready.

### 2. Build a fact and asset ledger

Classify every possible statement:

- `provided`: explicitly supplied by the user or verified source document;
- `visible`: directly observable in supplied product imagery;
- `unconfirmed`: inferred, promotional, medical, technical, comparative, environmental, certification, review, sales, origin, or performance claim without evidence.

Publish only `provided` and safely worded `visible` facts. Never infer an unseen back, interior, accessory, ingredient, dimension, certification, performance result, or comparison outcome.

Do not convert units, translate regulated terminology, or derive secondary metrics unless the user approves the conversion and its precision. Preserve the supplied unit when uncertain.

Number every source image and assign its role: hero, angle, detail, packaging, scale, usage, instruction, specification evidence, logo, or style reference. Record protected product traits: silhouette, proportions, material, color, texture, openings, controls, labels, logo position, included parts, and known unknown surfaces.

### 3. Plan the decision sequence

Read [references/module-system.md](references/module-system.md). Select only modules that answer a real buyer question:

1. Is this the product I need?
2. What value does it provide?
3. What visible or verified evidence supports that value?
4. How is it used, sized, maintained, or selected?
5. What could cause a mistaken purchase?

Default to 6–10 modules only when the product has enough verified evidence. Use fewer for simple products. Do not pad the page with duplicate hero shots, generic lifestyle scenes, unsupported superlatives, or decorative brand filler.

If available facts support only three to five distinct buyer questions, build only three to five modules. Do not create a recap or specification module that merely repeats the preceding modules.

Create a module manifest before generation:

```yaml
id: stable ordered identifier
type: hero | feature | detail | scenario | steps | specs | comparison | trust | closing
buyer_question: one question
claim: one verified message
evidence: fact IDs and source-image IDs
visual_job: what the image must demonstrate
copy: exact approved headline, body, labels
asset_route: existing source | named Atom | image model | deterministic graphics
delivery_size: researched platform value
```

### 4. Define one visual system

Set one palette, type hierarchy, spacing scale, corner/border treatment, product scale rule, lighting family, background family, and annotation style for the entire set. Vary composition by module purpose while preserving product identity and visual continuity.

Keep text separate from generative imagery. Generate or edit text-free visual bases with intentional negative space, then add approved copy deterministically. Use an image model for short integrated display text only when exact typography is not required and the target platform permits embedded text.

### 5. Produce modules independently

Use the narrowest installed Atom for each required visual:

- `$ai-product` for a product-faithful scene;
- `$create-white-background-product-mockup` for a clean isolated product asset;
- `$remove-background` for a transparent product cutout;
- `$image-combiner` for a coherent multi-source scene;
- `$photo-collage` only when visible photo panels are the requested module treatment;
- `$expand-image` only after a content-accepted module misses its target geometry.

Generate each named module as a separate run. Repeat the product lock and relevant source IDs in every run. Do not generate the entire page in one prompt: one failure must require replacing only one module.

For steps, specifications, comparison tables, dimensions, icons, badges, and longer copy, prefer deterministic layout over generated text. Do not create a comparison module without verified competitor or variant facts.

### 6. Export separate modules first

The canonical deliverable is the ordered set of accepted module images plus a manifest. Use platform-native modules when the destination expects modules. Use independent product media when the storefront theme owns the page layout.

When the destination accepts or requests a long image, stitch the same accepted modules in order. Run:

```text
python3 scripts/assemble_detail_page.py manifest.json --output-dir /absolute/output/path
```

Read [references/assembly-manifest.md](references/assembly-manifest.md) before preparing the manifest. The script creates normalized module files, one stitched preview, and a machine-readable delivery manifest. Never treat the stitched preview as the only editable source.

If the user explicitly asks for only one long image but the researched platform uploads modules, explain the mismatch and deliver both the requested long derivative and the platform-native modules. Do not refuse the long image, and do not mislabel it as the platform upload source. For a destination that truly accepts one long image, the long image may be upload-ready while the separate modules remain the editable source.

### 7. Accept the deliverable

Accept only when:

1. Every module satisfies a distinct buyer question and appears once in the intended sequence.
2. Every claim maps to supplied or visible evidence; no certification, metric, review, ranking, price, guarantee, medical result, or comparison is invented.
3. Product shape, color, material, controls, labels, logo, packaging, and included parts remain consistent across modules.
4. Copy is exact, readable on mobile, within safe areas, and not baked into imagery when the platform expects text fields.
5. Modules share one visual system but do not repeat the same crop and composition.
6. Separate exports satisfy the researched dimensions, formats, file limits, metadata, and content restrictions.
7. The stitched output, when requested, follows module order without gaps, stretching, clipped copy, scaling mismatch, or hidden module boundaries.
8. The delivery includes research notes, fact ledger, module manifest, separate module images, optional long preview, alt text, and an acceptance record.

Retry only the failed module or deterministic layout property. Do not regenerate accepted modules or change the visual system because one section failed.

## User-facing output

- Media type: An ordered product-detail module image set, manifest, research record, and optional stitched long-page image
- Default quantity: 6–10 separate modules when evidence supports them; otherwise the minimum complete set
- Content per image: One buyer question, one verified message, and one purposeful visual job
- Default layout: Researched platform-native modules; separate modules remain canonical even when a long page is delivered
- Video output: No; record video opportunities separately without creating them
- Model policy: Call the narrowest installed product/layout Atom or current reference-aware image model, then use deterministic typography and assembly
- Downstream use: Amazon A+ content, marketplace detail images, Shopify/DTC product sections, seller review, localization, and campaign adaptation
