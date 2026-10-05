---
name: poster-design
description: Create one distinctive, production-ready poster or promotional flyer from a theme, campaign brief, exact copy, product, person, photo, or visual references. Use for commercial, editorial, cultural, event, retail, fashion, music, art, typography-led, photo-led, zine, bitmap, collage, experimental posters, or single-page flyers that need deliberate hierarchy and broad visual variation; do not use for multipage layouts, manufacturing artwork, generic banners, thumbnails, infographics, or simple photo filters.
---

# Poster Design

Turn a communication idea into one poster with a clear focal point, intentional typography, and a deliberately selected art direction. Treat the capability as model routing plus a compiled Prompt; never depend on a temporary poster endpoint.

## Catalog

- Display name: Poster Design
- Categories: Layout & Design
- Status: Ready
- Featured: yes
- Route label: Model-routed poster generation
- Tone: coral
- Short description: Create distinctive posters across varied art directions.

- Similar skills: ai-banner-design, make-thumbnail, product-detail-page
## What this skill does

- Distills a theme or campaign into one message, one focal subject, one visual metaphor, and a readable copy hierarchy.
- Handles promotional flyers as an information-richer poster mode with explicit offer, event, CTA, contact, and print-format checks.
- Selects an art direction from independent composition, image-language, typography, color, and material axes instead of imposing one house style.
- Routes the current image model before considering an optional specialist endpoint.
- Generates one poster, checks communication and visual quality, and retries only the failed property.

## How to use

Provide a theme, exact copy, intended format, and any product, person, brand, or visual references you want preserved.

#### Create a campaign poster

```text
Create a bold Chinese campaign poster for these sneakers titled “舒适每一步”.
```

#### Create from a reference photo

```text
Turn this street photo into an expressive cultural poster titled "CITY IN MOTION".
```

#### Explore an art direction

```text
Create an experimental poster about artificial memory with an unexpected visual style.
```

#### Create a promotional flyer

```text
Create an A5 launch flyer from these product images using the headline “SUMMER DROP” and the supplied event details.
```

## Workflow

### 1. Compile the poster brief

Resolve only fields that change the result:

```yaml
purpose: sell | announce | invite | inform | express
format: poster | promotional flyer
audience_and_placement: supplied or inferred
message: the one idea viewers should retain
exact_copy: title, subtitle, details, CTA
focal_subject: product | person | object | scene | type | symbol
reference_roles: identity | product | logo | brand | composition | style
preservation: elements that must remain unchanged
ratio: supplied; otherwise 4:5 for social or 3:4 for general poster use
direction: supplied | inferred | explore
```

Do not invent factual claims, event details, prices, credits, logos, or long copy. Ask only when missing exact copy, asset roles, or format would materially change the output.

For `promotional flyer`, also resolve the real delivery size, portrait/landscape orientation, digital versus print use, required offer/event details, CTA/contact path, and whether deterministic typesetting or prepress finishing is available. Treat an image-model result as artwork, not automatically print-ready: verify final pixels, bleed, trim, safe margin, color profile, and export format in the finishing step.

### 2. Choose a genuinely different direction

Read [references/style-recipes.md](references/style-recipes.md). Honor an explicit direction. Otherwise construct one direction by selecting compatible values across these axes:

- composition: monumental, asymmetric editorial, centered icon, full-bleed, modular, collage, or radical negative space;
- image language: photography, illustration, graphic abstraction, type-as-image, bitmap, printmaking, or mixed media;
- typography: display-led, integrated, restrained, vernacular, or microtype;
- color: monochrome, duotone, restrained accent, tonal, high-chroma, or brand-led;
- material: clean digital, paper, risograph, halftone, xerox, screen print, painted, or tactile collage.

Do not randomly combine incompatible traits. Make the direction serve the message. For an open exploration request, choose one non-generic direction with a brief internal rationale; offer multiple concepts only when the user explicitly asks for options.

### 3. Select the model

- Apply the shared [model-selection policy](../../shared/model-selection.md). Any readable title, copy, Chinese, or multilingual content routes to GPT Image 2 Medium; do not fall back across models for text accuracy.
- Keep reference images on the same route when GPT Image can preserve the required product, person, or brand assets.
- Prefer a reference-aware editing model when the work is primarily a controlled transformation of an existing poster or when reference fidelity demonstrably exceeds GPT Image.
- Use Midjourney only for pure text-to-image artistic poster exploration with no readable copy or reference assets; receive all four results. Use Z-Image only for text-free photorealistic directions or Chinese cultural elements.
- Use `ai-poster` or `ai-poster-from-images` only when its current contract is verified and materially improves the requested result. It is an accelerator, not the Skill identity.
- Default a normal poster deliverable to one GPT Image 2 Medium, 2K image with `batchCount: 1`. Use Low only for an explicitly requested layout draft; use High only after a recorded Medium acceptance failure or explicit premium delivery.

### 4. Compile the Prompt

Read [references/prompt-compiler.md](references/prompt-compiler.md), then load only the selected recipe from [references/style-recipes.md](references/style-recipes.md). Begin with the cleaned WeShop Poster default only for the `fashion-commerce` recipe. Begin with the cleaned AI Flyer Maker seed only for `promotional-flyer`, retaining its reference-preservation and hierarchy intent while replacing generic style language with the actual brief. Neither is the universal baseline.

Keep three contracts distinct:

- `must preserve`: supplied identity, product, logo, color, geometry, or recognisable scene evidence;
- `must render exactly`: approved title, subtitle, date, price, CTA, and other supplied copy;
- `may reinterpret`: composition, background, metaphor, lighting, texture, and supporting graphics.

Use the compiler to decide these fields internally, then compress them into short natural prose. Do not send field labels or repeat the same constraint across sections. The submitted Prompt should normally contain: the poster and exact copy; one concrete visual concept; the essential reference lock; composition/type relationship; material/color direction; and a short exclusion clause.

Keep the submitted Prompt near 60–120 English words or equivalent unless complex source-role mapping genuinely requires more. Internal reasoning may be structured; model instructions should read like a concise art director's brief.

### 5. Generate and accept

Execute through WeShop OpenAPI, poll to a terminal state, and read the returned image result. Accept only when:

1. One poster communicates one dominant message and has one unmistakable first-read focal point.
2. Title, subtitle, details, and CTA follow the requested hierarchy; required copy is correct and unintended readable text is absent.
3. Supplied product, person, logo, and brand assets meet their declared preservation level.
4. The selected art direction is visible in composition, typography, color, and material—not merely named in the Prompt.
5. The result remains legible at thumbnail size, maintains safe margins, and matches the requested ratio.
6. No invented claim, date, price, logo, credit block, duplicate subject, collage panel, or generic AI decoration appears unless requested.

For a flyer, additionally require every approved offer, date, venue, CTA, and contact item to be present exactly once and readable at delivery size. Do not claim print readiness until deterministic finishing verifies trim, bleed, safe margin, resolution, color profile, and export format.

### 6. Retry a failed result

Retry once with a non-identical Prompt that names only the failed property:

- copy error: remove optional text and reassert exact approved copy;
- weak hierarchy: enlarge or isolate the focal subject and dominant title;
- generic style: change the visual metaphor or recipe, not only the palette;
- reference drift: strengthen the relevant preservation clause and remove competing transformations;
- clutter: remove secondary graphics, microcopy, and texture layers;
- wrong ratio or crop: preserve the concept and rebuild only the attention geometry.

Use deterministic typography after generation when exact or longer copy remains unreliable and the user accepts a composited result. Change models only for a demonstrated capability mismatch. Record model, optional agent, parameters, Prompt revision, execution ID, error, retryability, refund state, and failed acceptance item.

When this Skill selects GPT Image 2, use `quality: "medium"` and `imageSize: "2K"` by default; change either only when the user explicitly requests another tier.

Every GPT Image 2 call in this Skill defaults to Medium at 2K; use another tier only when the user explicitly requests it.

## User-facing output

- Media type: One finished poster or promotional-flyer image and a compact acceptance record
- Default quantity: 1 separate image
- Content per image: One communication objective, one focal system, and one deliberate copy hierarchy
- Default layout: 4:5 for social or 3:4 for general use unless specified
- Video output: No
- Model policy: Route the best current typography- and composition-capable image model; specialist poster endpoints are optional
- Downstream use: Campaigns, launches, retail offers, event flyers, editorial stories, cultural communication, music, fashion, art, print, and social promotion
