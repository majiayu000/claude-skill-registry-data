---
name: ecommerce-detail-page-generator
description: Turn product photos and a minimal brief into verified, platform-adapted e-commerce detail-page systems, including product fact review, visual analysis, localized copy, 6-10 module story planning, policy-aware text-free image generation or real-photo routing, deterministic Pillow typography, platform-sized slices, long-page previews, manifests, and automated validation. Supports 淘宝/天猫/京东/拼多多/抖音/小红书/Amazon/AliExpress/Temu/TikTok Shop/eBay/Etsy/Shopify. Use when a user asks for 电商详情页, 商品详情图, 商详设计, A+ content, listing galleries, or a short-input workflow that turns product photos into ready-to-review commerce assets without inventing unsupported claims.
---

# E-commerce Detail Page Generator

Create a platform-adapted product story from a minimal brief while preserving product truth. Use image generation for visual bases only where the platform permits synthetic imagery; use Pillow composition for exact copy, dimensions, slicing, and manifests.

## Required Input Gate

Require exactly these three inputs before planning or generating:

1. Target platform, including country/site when relevant.
2. At least one clear product image.
3. Product name or category.

Do not call `image_gen` before this gate passes.

If one required input is missing, ask only for the single most important missing item. Do not present a long form.

After the gate passes, distinguish every fact as:

- `user`: explicitly supplied by the user.
- `visible`: directly observable in an uploaded image.
- `unconfirmed`: plausible but not verified.

Never publish an `unconfirmed` fact. Do not infer hidden materials, dimensions, capacity, performance, certification, compatibility, ingredients, medical effects, price, discount, sales, reviews, warranty, package contents, or unseen product surfaces.

If the proposed page needs one of those facts, ask one concise question and stop generation until answered. If several facts are missing, ask first for the one that changes the primary selling proposition or compliance status.

## Platform Routing

1. Read `references/platform-profiles.json`.
2. Resolve the user's platform through `aliases`.
3. Read the matching section of `references/platform-style-guide.md`.
4. Reverify rules on the web before generation when:
   - the profile is older than its `reverify_after_days`;
   - a rule is marked `seller_backend_confirmation`;
   - the platform/site is not covered;
   - the product is regulated, health-related, for children, battery-powered, ingestible, cosmetic, or safety-sensitive.
5. Prefer official seller documentation. Treat dimensions from non-official sources as a working canvas, not a platform guarantee.

Platform rules modify export shape, information density, module order, typography, and sales rhythm. They must not erase the product's own visual identity.

## Product Analysis

Inspect all product images and create `brief.json` with:

- product name, platform, locale, category, and supplied image paths;
- a visual fingerprint: dominant colors, geometry, finish, material appearance, visual temperature, perceived price tier, likely audience, and photographic cues;
- facts grouped by `user`, `visible`, and `unconfirmed`;
- prohibited claims and open questions;
- a short design direction derived from the product rather than from a generic template.

For local images, load them with `view_image` before analysis. When multiple images exist, label each as front, back, side, detail, packaging, scale, or unknown.

## Page Architecture

Read `references/category-playbooks.md`, then select 6-10 modules. Use only modules supported by verified facts.

Default story arc:

1. Product-led hero and primary promise.
2. Customer problem or desired outcome.
3. Primary differentiator.
4. Supporting features or details.
5. Real use context.
6. Operation, fit, or sizing guidance.
7. Verified specifications or package contents.
8. Trust, care, compatibility, or closing summary.

Omit comparison, certification, review, guarantee, discount, and before/after modules unless the user provides evidence.

Write concise copy. Prefer one headline, one support line, and up to three proof points per module. Localize for the target market instead of translating literally.

Represent the complete plan as `page-spec.json` conforming to `references/page-spec.schema.json`.

## Visual Generation

Load the system `imagegen` skill before using `image_gen`. Read `references/prompt-recipes.md`.

Generate one text-free visual base per module that needs new imagery. Repeat these invariants in every prompt:

- preserve product geometry, color, proportions, controls, openings, labels, and logo placement from the references;
- do not invent unseen product sides, accessories, packaging, or usage outcomes;
- no text, letters, numbers, badges, watermarks, UI, or fake certification marks;
- leave intentional negative space matching the module layout.

Use separate calls for separate modules. Do not ask one generation to create a full long page.

Platform exceptions:

- `tiktok-shop`: official listing rules prohibit digital renderings and added text in product images. Build listing modules from the user's real photos with deterministic crops only; keep copy in `copy.md`.
- `etsy`: use the seller's original photos of the actual item. Do not replace them with generated product renderings. Generated moodboards are concept-only and must not be labeled upload-ready.
- When a platform profile sets `image_text_policy` to `forbidden`, set each module's `text_mode` to `none`.

## Composition and Export

Save generated or selected module bases inside the project output directory, then run:

```bash
python3 scripts/compose_detail_page.py \
  --spec <path/to/page-spec.json> \
  --brief <path/to/brief.json> \
  --output <path/to/ecommerce-detail-output/product-slug>
```

The composer must create:

- `brief.json`
- `page-spec.json`
- `copy.md`
- `modules/01-*.jpg` or `.png`
- `detail-page-long.jpg`
- `manifest.json`

For Amazon A+, TikTok Shop, Etsy, and eBay, treat module files as the primary deliverable and the long image as review-only. For domestic long-detail platforms, both slices and the long preview are deliverables.

Run validation:

```bash
python3 scripts/validate_output.py \
  --spec <path/to/page-spec.json> \
  --output <path/to/ecommerce-detail-output/product-slug>
```

Fix errors before delivery. Warnings about seller-backend confirmation must remain visible in `manifest.json`.

## Quality Bar

Reject or regenerate a module when:

- the product shape, color, logo, controls, or included parts drift;
- text overflows, becomes too small, or falls outside safe margins;
- two adjacent modules repeat the same composition;
- the page looks like a generic template rather than the supplied product;
- a claim lacks a `user` or `visible` source;
- the output violates the selected platform's image or AI-content policy.

Deliver the final paths, platform profile used, unresolved backend checks, and any modules restricted to preview-only use.

## Resources

- `references/platform-profiles.json`: machine-readable platform rules and evidence metadata.
- `references/platform-style-guide.md`: platform visual and conversion systems.
- `references/category-playbooks.md`: category-specific module choices.
- `references/prompt-recipes.md`: reusable image-generation prompt patterns.
- `references/page-spec.schema.json`: composition contract.
- `scripts/compose_detail_page.py`: exact text layout, slicing, long preview, and manifest generation.
- `scripts/validate_output.py`: structural and rendered-output checks.
- `scripts/test_pipeline.py`: isolated four-platform regression test.
