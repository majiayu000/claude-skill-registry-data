---
name: imagegen-frontend
description: Generate premium frontend design reference images for mobile apps and websites. Use for mobile screen concepts, app flows, landing pages, marketing sites, product pages, portfolios, or redesign comps when output should be images rather than code. Mobile output uses readable platform-aware phone screens; web output uses one separate horizontal image per section. Not for frontend implementation or image-to-code work.
---

# Frontend Image Direction

Generate polished, buildable frontend reference images. Do not write code or return text-only design advice. User brief overrides style defaults; output contract below does not.

## Route

Choose one mode before generating:

- **Mobile**: native or cross-platform app screens and flows.
- **Web**: landing pages, marketing sites, product pages, portfolios, and desktop web comps.

If request mixes both, keep separate mobile and web image sets under one shared brand system.

## Shared Direction

Lock a small design bible before first image:

- product goal and audience
- palette: primary, secondary, sparse accent, neutral scale
- typography mood and scale
- spacing, radius, shadow, icon, and image language
- signature visual idea

Keep bible consistent across every image. Vary composition and density, not product identity.

Design for:

- immediate hierarchy and readable text
- controlled palette and generous spacing
- intentional imagery, crops, texture, and material
- believable content and interaction structure
- enough detail for developer to recreate layout
- one memorable visual idea instead of many decorative tricks

Avoid default AI tells:

- purple-blue glow, rainbow mesh, meaningless blobs, or gratuitous glass
- repeated card grids, pills, badges, fake stats, and dashboard clutter
- generic startup copy or nonsense brands
- tiny text, awkward wrapping, random icon styles, or weak contrast
- visual novelty that hides hierarchy or product purpose

Prefer restrained gradients, texture, and image overlays only when palette-matched and legible. Match industry tone rather than forcing generic startup aesthetics.

## Mobile Mode

### Output Contract

- Generate one fresh image per requested screen. `N` screens means `N` images.
- For unspecified app concept, choose enough screens to show one useful flow; do not pad it.
- Never replace screens with one collage containing unreadable miniatures.
- Never crop an old board to fake a dedicated screen; generate a fresh screen-specific image.
- Show each screen in a subtle, consistent phone frame by default. Omit frame only when user asks for raw screens or assets.

### Platform

Choose and maintain one dominant mode:

- **iOS**: restrained chrome, safe areas, tab bars, sheets, elegant spacing.
- **Android**: clear app bars, navigation, sheets, component rhythm, explicit states.
- **Cross-platform**: universal navigation, safe areas, neutral premium language.

Do not mix platform patterns carelessly. Respect status bar, gesture, home indicator, and navigation regions.

### Flow And Layout

- Order screens as believable transitions: onboarding -> auth -> home; browse -> detail -> checkout; dashboard -> activity -> detail.
- Carry state forward and keep navigation model stable.
- Make first screen calm: one focal point, short headline, concise support, clear next action.
- Prefer direct hierarchy and fewer containers over nested cards and phone-sized website layouts.
- Keep device scale, bezel, margins, and shadow consistent. Device supports content; it does not dominate.
- On onboarding, vary composition and purpose instead of cloning one template.

Use imagery, texture, custom-feeling icons, and decorative assets when they serve product category. Keep text comfortably readable at normal image size.

## Web Mode

### Output Contract

- Generate one separate horizontal image per section. `N` sections means `N` images.
- Never combine sections into a tall page, collage, or single best frame.
- Defaults when count is absent: hero `1`; landing page, product page, or portfolio `6`; full website or marketing site `8`.
- Use 16:9, 16:10, or 21:9 based on section density.
- If tool renders one image per call, generate sections sequentially until count matches.

### Page System

Give every section one job: hook, proof, explain, compare, or convert. Typical six-section flow:

1. Hero
2. Trust or proof
3. Features
4. Product or use-case story
5. Testimonial or pricing
6. Final CTA

Adapt structure to product. Do not add irrelevant trust bars, pricing, KPIs, or dashboards.

Across sections:

- keep one palette, type system, CTA family, radius language, and image grade
- use at least three composition anchors when page has four or more sections
- vary density, background intensity, image-to-text ratio, and scale
- keep one clear conversion path and primary action
- mix image crops where imagery is central; do not repeat one stock silhouette

### Composition

Do not default hero to text-left/image-right. Consider centered over image, bottom-aligned over image, stacked minimalist, image-as-canvas, inverted split, or off-grid editorial. Use classic split only when brief supports it.

Choose hero scale decisively:

- **Giant statement** for cinematic, luxury, agency, or bold briefs.
- **Mid editorial** for product, SaaS, commerce, and balanced storytelling.
- **Mini minimalist** for Swiss, typography-led, or restrained briefs.

Keep headline short, support concise, and first viewport uncluttered. Website comps must expose layout, spacing, type scale, CTA priority, components, and media treatment clearly enough to implement.

## Generation Workflow

1. Parse mode, count, audience, platform, brand mood, and required states or sections.
2. Lock design bible and logical sequence.
3. Assign each image a purpose, composition, and content state.
4. Generate exact image count in order.
5. Check consistency, legibility, hierarchy, and count. Regenerate weak or missing images rather than explaining them away.

## Final Check

Before completion, verify:

- output is images, not code or a prose substitute
- image count exactly matches contract
- text remains readable at normal viewing size
- all images belong to one product system
- mobile flow and navigation are believable, or web sections form coherent funnel
- composition avoids reflexive AI defaults
- imagery and decoration support structure
- each image is clean enough to serve as frontend reference

After image generation, follow image tool response rules. Do not add a summary or ask follow-up questions.
