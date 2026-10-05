---
name: 9image-design
description: Create the design stage of the 9Designer pipeline from a single reference image, starting with only the first landing page and continuing to the full multi-page prototype system after the user approves it. Use when the user provides an image or artwork and asks to turn it into a website, landing page, prototype, brand system, UI kit, responsive preview, or says "9image-design", "image to web prototype", "make this into a site", "build the whole prototype", "use this image as reference", or similar image-first web design requests.
---

# 9Image Design

## Core Rule

Use each newly provided image as the only source of truth for that prototype. Build a fresh custom web direction around that image's composition, mood, colors, lighting, motifs, typography, and atmosphere. Do not reuse the brand, copy, colors, layout, or motifs from prior unrelated reference images.

Do not make a generic SaaS, startup, dashboard, or template layout unless the image clearly calls for that style.

When the user asks for generated design images, use the image generation tool. Generate separate images one at a time or as separate tool calls. Do not combine the full system into one giant image.

## Frontend Design Bar

Before generating Image 1, define internally:

- Visual thesis: one sentence for mood, material, and energy.
- Content plan: hero, support/story, detail/showcase, final CTA.
- Interaction thesis: 2-3 motion or interaction ideas the future website should support.

Design with these rules:

- Start with composition, not component count.
- Make the brand/product name the loudest signal in the first viewport.
- Prefer a full-bleed or image-led hero with text placed on a calm area of the artwork.
- Preserve the reference image's native composition, focal path, horizon, and empty-space logic before choosing any web layout pattern.
- Keep copy short, specific, and scannable.
- Use cardless layouts by default; use cards only when the reference image or page concept needs them.
- Avoid hero cards, generic stat strips, logo clouds, pill clutter, fake dashboards, and generic SaaS grids unless the image clearly implies them.
- Avoid generic social icons, utility icons, arrows, and feature icons. Match glyph shape, fill/outline mode, optical weight, color, size, and container treatment to the reference world.
- Do not add hero eyebrows, kickers, badges, or decorative pills unless the reference already contains that structure or the user explicitly asks.
- Use at most two typeface directions and one dominant accent color unless the reference image has a stronger system.
- Use motion cues to support hierarchy and atmosphere, not noise.

Reject or regenerate concepts that are header-only for a full website, too blurry to implement, generic, crowded, repetitive, tiny, unreadable, or not faithful to the reference image.

## Reference Analysis

Before generating or designing, internally inspect the image for:

- Main subject and natural focal point
- Empty space and best text placement
- Movement direction and horizon line
- Foreground, midground, and background depth
- Lighting direction, glow, particles, shadows, and atmosphere
- Mood and emotional tone
- Color palette and contrast range, including primary, secondary, accent, background, surface, text, and glow/shadow color candidates in hex-style notes when practical
- Symbols, creatures, objects, landscape elements, textures, and patterns
- Illustration, photo, 3D, cinematic, editorial, or hand-drawn style
- Existing title text, logo, lettering, brand mark, or typography, including serif/sans/script/display category, x-height, contrast, weight, width, spacing, and distinctive letterform personality
- Which elements should later become transparent assets
- Which text should remain real HTML/CSS and which text is decorative logo, wordmark, or hand-lettering
- Which social, navigation, CTA, feature, gallery, and footer icons must later become exact generated or vector-quality assets
- Which motifs should become design tokens, reusable assets, icons, masks, section dividers, background textures, visual effects, or motion cues

Preserve strong existing identity. If the image contains a polished wordmark, logo, title, or lettering, keep it as the brand foundation. If it does not, create a short brand name that feels native to the image.

## Visual Translation

Turn image motifs into the design language:

- Clouds: soft masks, mist dividers, floating panels, cloud-like section edges
- Birds or wings: icons, motion cues, navigation marks, ornamental dividers
- Forests, leaves, vines, flowers: borders, organic frames, background patterns, icons
- Magic, mist, light, particles: atmospheric overlays, glow treatments, subtle gradients
- Mountains, hills, cliffs, horizons: section anchors, diagonal cuts, layered depth
- Vehicles, creatures, masks, symbols, artifacts: logo marks, cards, badges, icons
- Water, waves, ice, fire, metal, stone: texture, stroke, border, and button treatments

Choose typography to match the image:

- Whimsical or storybook images: playful hand-drawn or warm serif display
- Poetic, calm, cinematic images: elegant serif plus restrained editorial sans
- Adventure or action images: bold display type with strong rhythm
- Futuristic or abstract images: geometric sans and precise spacing
- Fantasy or atmospheric images: cinematic editorial type with luminous restraint

Keep all visible copy short, readable, intentional, and aligned to the image's tone.

## Generation Workflow

Default to an approval-gated workflow:

1. Generate only Image 1.
2. Treat Image 1 as the prototype direction for that specific reference image.
3. Stop after generating Image 1. Wait for the user to approve it, request changes, or say to continue.
4. If the user requests changes, revise Image 1 first. Do not build the remaining pages from an unapproved direction.
5. After explicit approval, generate the remaining pages as separate image-generation calls in order, preserving the approved brand identity from Image 1.

Even if the user initially asks for the whole prototype, create only the first landing page first unless they explicitly override the approval gate in the same request.

Within one approved prototype, maintain the same brand name, logo style, color palette, typography, icon style, button style, copy tone, and atmospheric visual system across every image.

After approval, generate section/detail concepts when the full-page image is too small to read precisely. For multi-section websites, prefer coordinated section-level images for complex areas over relying on one compressed full-page board. Keep the same design system; do not crop or zoom an old image as the main source of truth.

## Standard 10-Image System

Use this sequence unless the user gives a different scope:

1. **Full Landing Page Design**: navigation, 16:9 hero using the reference artwork as dominant visual, intro/story, highlight, features, visual showcase, CTA, minimal footer.
2. **About / Story Page**: inner hero, origin story, editorial text-image section, timeline or journey, values/philosophy, closing CTA.
3. **World / Gallery Page**: full-width visual hero, tabs/filters, varied gallery grid, featured scene, immersive detail block, small CTA.
4. **Feature / Experience Page**: feature hero, benefits/highlights, deep-dive blocks, icon feature list, visual journey, CTA.
5. **Detail Page**: choose the best detail type for the image, such as character, artwork, chapter, product, journal, destination, or experience; include hero, metadata, content, supporting visuals, related items, CTA.
6. **Contact / Join / Signup Page**: emotional headline, short copy, form, supporting artwork, trust/community note, CTA, compact footer.
7. **Brand Kit / Design System Board**: logo system, extracted palette with hex-style swatches, typography system, 6-8 motif icons, visual style rules.
8. **UI Component Library Board**: buttons, links, nav, mobile nav, cards, image frames, inputs, search, dropdown/filter, tags, CTA banner, quote block, feature card, gallery card, footer module.
9. **Copy and Content System Board**: tagline, hero copy, CTAs, intro, features, gallery labels, CTA/footer text, inner page headlines, contact/signup copy.
10. **Responsive Website Preview Board**: desktop, tablet, mobile, mobile menu, mobile section examples, CTA and footer on mobile.

## Layout Rules

For the landing page and inner pages:

- Base hero text placement on the image composition: top center, bottom left, bottom center, right side, horizon-aligned, floating overlay, vertical stack, or integrated with existing title text.
- Keep the artwork as the focus. Use overlays, gradients, glass panels, or minimal buttons only where they improve readability.
- Use varied section structures: asymmetrical editorial blocks, overlapping image cards, circular masks, horizontal story strips, diagonal transitions, immersive banners, timeline sections, layered depth, icon highlights, framed artwork moments, and organic dividers.
- Avoid the default left-text/right-image hero plus four-card grid unless the artwork naturally demands it.
- Keep the result premium, spacious, cinematic, visually rich, and uncluttered.

## Prompting Pattern

For Image 1, include:

- The provided reference image as the dominant creative source
- A full landing page only
- Navigation bar, hero, intro/story, highlight, feature, visual showcase, CTA, and minimal footer
- Hero composition based on the reference image's focal point, empty space, horizon, and movement
- A fresh brand direction derived only from the current image
- Clear instruction to stop after Image 1 and wait for approval
- Implementation clarity: readable text, stable section dimensions, clear button/card/form details, and extractable spacing/type/color decisions
- Clear distinction between normal HTML text and decorative image-based lettering or logo marks

For later images after approval, include:

- The page number and page type
- The approved brand identity and motifs from Image 1
- Specific layout requirements for that page
- Text/copy examples that should be readable
- Explicit instruction to keep consistency with previous generated images
- Explicit instruction to avoid generic SaaS/corporate styling and overcrowded text
- Explicit instruction that each page/section must be practical for HTML/CSS implementation and later screenshot comparison

Example framing:

```text
Create IMAGE 1 - Full Landing Page Design from the attached reference image only. First infer a fresh brand direction from the image's subject, empty space, movement, lighting, palette, motifs, typography, and mood. Design a complete premium landing page with navigation, hero, intro/story, highlight, features, visual showcase, CTA, and minimal footer. Use the artwork as the dominant hero visual, choose hero text placement based on the image composition, avoid generic SaaS styling, and stop after this landing page for approval.
```
