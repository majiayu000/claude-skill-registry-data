---
type: Skill
name: design-product-photography
description: Define product photography standards for e-commerce — shot types, composition, lighting, consistency rules, AI-assisted generation, and platform-specific variants. Covers the full product imagery pipeline from concept to published asset. Use when you need to plan product photoshoots, create photography briefs, set image standards for an e-commerce catalog, generate AI product lifestyle shots, or ensure visual consistency across hundreds of products.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# Product Photography

Use this skill when planning, creating, or reviewing product images for e-commerce — whether real photography or AI-generated visuals.

## MCP Tool Discovery

| Photography Task | Tool |
|---|---|
| Generate product images (AI — Gemini) | `generate_gemini_image_validated` (agent-prefixed or bare) |
| Generate product images (AI — DALL·E/OpenAI) | `generate_openai_image` |
| Edit/retouch images (AI) | `edit_gemini_image_validated` |
| Background removal | `remove_background` |
| Resize for platforms | `resize_image` |
| Generate scene backgrounds | `product_actualization` (place product in generated scene) |
| Alt text generation | `generate_image_alt_text_validated` |
| Image analysis (quality check) | `analyze_image` |

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for photography workflows. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai health` | Verify image generation/editing tools |
| `wp mcp-ai provider` | Check configured AI providers (Gemini, etc.) |
| `wp mcp-ai bulk` | Batch process product images |

## When to use this skill

Trigger when ANY of the following is true:

- Planning product photography for new arrivals or catalog updates.
- The task asks to "create product images", "shoot products", or "generate product visuals".
- Setting image standards for an e-commerce store.
- Creating photography briefs for a photographer or AI generation session.
- Ensuring image consistency across 100+ products.
- The task mentions "product shot", "hero image", "product photography", or "lifestyle image".
- Generating platform-specific product visuals (Instagram, website, ads).

## The Product Image Stack

Every product needs these image types:

```
┌──────────────────────────────────────────────┐
│              LIFESTYLE / CONTEXT              │  ← Social media, ads, hero banners
│    "The product in someone's life"            │
├──────────────────────────────────────────────┤
│              ANGLED / DETAIL                   │  ← Secondary gallery images
│    "What it looks like from every side"       │
├──────────────────────────────────────────────┤
│              WHITE BACKGROUND                 │  ← Primary product page image
│    "Clean, consistent, shoppable"            │
└──────────────────────────────────────────────┘
```

### Image Inventory Per Product

| # | Type | Purpose | How to Create |
|---|---|---|---|
| 1 | **White background — Front** | Primary product image | Photography or AI + `remove_background` |
| 2 | **White background — Back** | Show reverse side, label, details | Photography or AI |
| 3 | **White background — Angle** | 3/4 view showing depth and shape | Photography or AI |
| 4 | **Detail / Macro** | Texture, cap, engraving, ingredients | Photography (macro) or AI detail crop |
| 5 | **Packaging / Box** | Unboxing appeal, gift-ready presentation | Photography or AI |
| 6 | **Lifestyle — In Use** | Person holding/using the product | AI generation (`product_actualization`) |
| 7 | **Lifestyle — Scene** | Product in aspirational setting | AI generation or styled photoshoot |
| 8 | **Size Reference** | Product next to common object for scale | Photography or simple composition |

## White Background Standards

The primary product image — the first thing customers see — must be consistent across your entire catalog.

### Technical Specs

```
Format:      WebP or JPEG (PNG if transparency needed)
Resolution:  2000px minimum on longest side (4K-ready, good for zoom)
Color space: sRGB
Background:  Pure white (#FFFFFF) or transparent
Lighting:    Even, no harsh shadows, no blown highlights
Composition: Product centered, filling 80–90% of frame
Angle:       Slight 3/4 turn (not perfectly flat — show depth)
```

### Consistency Rules

```
✓ ALL products on white background
✓ ALL products at similar scale (a 30ml bottle and 100ml bottle
  should look proportionally different, not randomly zoomed)
✓ ALL products with the same lighting temperature
  (don't mix cool/clinical with warm/lifestyle whites)
✓ ALL products with the same shadow treatment
  (natural drop shadow OR no shadow — pick one, apply to all)

✗ Mixed backgrounds (some white, some gray, some beige)
✗ Different lighting across products in the same category
✗ Products at wildly different scales
✗ Visible floor/wall seams or backdrop edges
✗ Reflections of the photographer/studio in glass bottles
```

### By Product Category

**Fragrance Bottles:**
- Glass is tricky — use diffused lighting, avoid hard reflections
- Show the bottle shape clearly (silhouette matters for recognition)
- Include the cap ON and OFF if the cap is a design feature
- Spray mechanism visible in at least one shot

**Jewelry:**
- Macro lens or close crop (small details matter)
- Velvet or neutral surface — no distracting textures
- Show clasp/closure in detail shot
- Include wearing shot (on skin, not just on surface)
- Scale reference critical (ring on finger, bracelet on wrist)

**Skincare:**
- Clean, clinical lighting (suggests purity and hygiene)
- Show texture — pump dispenser, dropper, jar opening
- Ingredients list visible on back label if space allows
- Include "amount dispensed" shot (dollop of cream, drop of serum)

## AI-Generated Product Images

### When to Use AI vs Photography

| Use Case | Best Approach |
|---|---|
| White background product shots | Photography preferred (accuracy). AI if photo unavailable. |
| Lifestyle / scene images | **AI excels here** — use `product_actualization` or `generate_gemini_image_validated` |
| Social media creative variants | AI (fast, infinite variations) |
| Seasonal or themed versions | AI (add holiday props, change background season) |
| Color variants of same product | AI editing (`edit_gemini_image_validated`) |

### Product Actualization (AI Scene Generation)

Use `product_actualization` to place a real product image into an AI-generated scene:

```
product_actualization {
  product_attachment_id: [your product photo]
  mode: "image"
  scene_prompt: "Elegant marble bathroom vanity, morning sunlight streaming
                 through frosted glass, fresh flowers, spa-like atmosphere,
                 shallow depth of field, luxury aesthetic"
  aspect_ratio: "3:2"
  integration_mode: "ai"
}
```

This naturally embeds the product with matching lighting, shadows, and reflections — far better than manual compositing.

### Prompt Structure for Fragrance Photography

```
[Product type] + [Setting] + [Lighting] + [Mood] + [Camera details]

"An 80ml Carolina Herrera Good Girl stiletto-shaped perfume bottle on a
black marble surface, dramatic side lighting creating long shadows, gold
accents catching the light, luxury editorial photography, shallow depth
of field, bokeh background, 85mm lens, high-end fragrance campaign"
```

### Prompt Structure for Jewelry Photography

```
[Jewelry piece] + [Surface] + [Lighting] + [Detail] + [Style]

"Swarovski crystal bracelet draped over a dark velvet jewelry display,
soft diffused light catching every facet, macro photography showing
crystal clarity and cut precision, elegant and minimal composition,
no distracting elements, luxury catalog style"
```

### Prompt Structure for Skincare Photography

```
[Product] + [Props] + [Lighting] + [Vibe] + [Style]

"Conatural face wash bottle surrounded by fresh lavender sprigs and
chamomile flowers, natural window light, soft shadows, clean white
marble surface, spa aesthetic, bright and airy, wellness photography,
minimal and fresh composition"
```

## Social Media Image Variants

### Platform-Specific Crops from One Hero Image

```
Source: 2000×2000px product hero (1:1 square)

Instagram Feed:  1080×1080px (1:1) — crop from center
Instagram Story: 1080×1920px (9:16) — product bottom-third, text space top
Facebook Feed:   1200×630px (1.91:1) — product left-third, text space right
Pinterest:       1000×1500px (2:3) — full product, clean background
Website Hero:    1920×800px — product right-third, text space left
```

Use `resize_image` for each variant — never upload the full-resolution original to social media.

### Adding Text Overlay Space

When shooting or generating images intended for social posts with text overlay:

```
Rule of thirds:
  ┌──────────┬──────────┬──────────┐
  │          │          │          │
  │  TEXT    │  TEXT    │          │
  │  ZONE    │  ZONE    │  PRODUCT │
  │          │          │          │
  │          │          │          │
  └──────────┴──────────┴──────────┘

Product should occupy 1/3 of frame (right or bottom)
Empty space on the remaining 2/3 for headline, caption, or CTA
```

## Photography Brief Template

When briefing a photographer or planning an AI generation session:

```
PRODUCT PHOTOGRAPHY BRIEF
─────────────────────────
Product: [Name, SKU, size]
Brand: [Brand name]

SHOT LIST:
  □ White background — Front (primary)
  □ White background — Back
  □ White background — 45° angle
  □ Detail — [specific feature to highlight]
  □ Detail — [second feature]
  □ Packaging — Box/tin unopened
  □ Packaging — Box/tin open with product
  □ Lifestyle — [scene description]
  □ Lifestyle — [alternate scene]
  □ Size reference — [comparison object]

TECHNICAL:
  Format: WebP or JPEG
  Resolution: 2000px minimum
  Color space: sRGB
  Background: #FFFFFF (white background shots)

STYLE REFERENCES:
  [2–3 links or descriptions of images with the desired aesthetic]

NOTES:
  [Any special handling — reflective surfaces, fragile items,
   specific angles needed, text that must be readable, etc.]
```

## Image Quality Checklist

Before publishing any product image:

```
□ Background is clean (white = pure white, not off-white or gray)
□ Product is in focus (crisp edges, no softness)
□ Lighting is even (no harsh shadows except intentional creative choices)
□ Colors are accurate (matches the real product — check against reference)
□ No dust, fingerprints, or smudges on the product
□ Labels and text are readable and correctly oriented
□ Image is properly cropped (product fills 80–90% of frame)
□ File is optimized (WebP, properly compressed — see design-image-optimization)
□ Alt text is written via generate_image_alt_text_validated
□ Filename is descriptive (brand-product-view.format), not IMG_4829.jpg
```

## Batch Consistency Across a Catalog

When you have 100+ products, consistency is the hardest thing to achieve and the most valuable:

### Consistency Checklist

```
□ All primary images use the same background color
□ All products at consistent scale within their category
  (a 30ml fragrance should look smaller than an 80ml — consistently)
□ Same angle for all primary shots (all slightly 3/4, all front-facing, etc.)
□ Same lighting temperature across the entire catalog
□ Same shadow treatment (drop shadow style, opacity, direction)
□ Same file format and approximate file size per image
□ Same naming convention across all files
```

### AI Consistency

When generating images with AI for a catalog:

```
Use consistent prompt templates:
  "Product photography of [PRODUCT NAME], [FIXED LIGHTING],
   [FIXED BACKGROUND], [FIXED STYLE], luxury e-commerce catalog,
   [FIXED COLOR PALETTE], [FIXED COMPOSITION]"

Keep these elements IDENTICAL across all prompts:
  ● Background description
  ● Lighting description
  ● Style keywords
  ● Composition instructions

Only vary:
  ● Product name and description
  ● Any category-specific details (glass for fragrance, velvet for jewelry)
```

## Common Mistakes

```
WRONG:
  ✗ Mixed backgrounds — some white, some gray, some lifestyle
  ✗ Inconsistent scale — one bottle fills the frame, another is tiny
  ✗ Using lifestyle images as primary product images (confusing)
  ✗ Blown highlights on glass bottles (no detail in the brightest areas)
  ✗ 500KB+ images slowing down product pages
  ✗ Same image used for every variant (color, size — looks lazy)
  ✗ No detail shots — just one front-facing image
  ✗ Watermarked or manufacturer-supplied images (looks dropshipped)

RIGHT:
  ✓ Every primary image: white background, consistent lighting, clean
  ✓ Products shown to scale — a 30ml looks smaller than an 80ml
  ✓ 6–8 images per product: front, back, angle, detail×2, packaging, lifestyle
  ✓ Proper exposure: highlights preserved, shadows open, details visible
  ✓ Optimized files (WebP, < 200KB for primary image)
  ✓ Unique image per variant (different size shown, different color shown)
  ✓ at least one in-use or lifestyle shot per product
  ✓ Original or AI-generated — never use supplier shots alone
```

## Critical Rules

- **White background consistency is non-negotiable** — if your catalog has 100 products, all 100 primary images need the same background, lighting, and scale.
- **6 images minimum per product** — front, back, angle, 2× detail, packaging. Lifestyle is bonus.
- **AI excels at lifestyle** — use `product_actualization` or `generate_gemini_image_validated` for scene imagery.
- **Optimize before uploading** — `resize_image` to platform dimensions, convert to WebP via media worker.
- **Consistent naming** — `[brand]-[product]-[view].webp`. Never `IMG_4829.jpg`.
- **Alt text on every image** — use `generate_image_alt_text_validated` before publishing.
- **No supplier images as primary** — they look generic and destroy brand trust. Use only as reference.

## What This Skill Does NOT Cover

- **Image generation techniques** — use `design-image-generation` for prompt engineering, model selection, and AI provider configuration.
- **Image optimization** — use `design-image-optimization` for format conversion, compression, responsive sizing, and alt text generation.
- **Social media publishing** — use `design-social-publishing` to post product images to Instagram, Facebook, and other platforms.
- **Brand identity creation** — use `design-brand-kit` for logo design, color palettes, and typography that define the visual brand context.
- **Product copywriting** — use `design-product-research` for product descriptions and marketing copy that accompanies product images.
- **Video product showcases** — use `design-video-creation` for product video content (unboxing, demos, short-form Reels).

## Cross-references

- Run **`design-image-generation`** for AI generation techniques — check your tool list for the Gemini image tool.
- Run **`design-image-optimization`** to resize, compress, and convert images — use `resize_image` (MCP).
- Run **`design-brand-kit`** to align product imagery with brand visual identity.
- Run **`design-product-research`** to understand the product before creating its visual story.
- Run **`design-seo-content`** for image SEO — filenames, alt text, and product page optimization.
