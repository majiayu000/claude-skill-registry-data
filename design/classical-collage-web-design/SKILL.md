---
name: classical-collage-web-design
description: Use when designing or building a website, landing page, Framer template, pitch visual or brand system in the "classical painting × modern tech" art direction (Renaissance / neoclassical oil paintings and marble ruins combined with laptops, phones, coins and quiet product UI, as on the Aureon fintech page and contralabs.com). Covers art direction, metaphor selection, image sourcing and AI prompts, halftone and texture techniques, exact design tokens, components, page blueprints, motion, copy voice, and Figma / Framer / Next.js build steps.
---

# Classical Collage × Modern Tech

An editorial web art direction. **Old Master paintings, Greco-Roman ruins and marble** are combined with **modern objects and product UI**: laptops, phones, gold coins, dashboards. The art carries the emotion and brand. The interface stays almost invisible: off-white paper, near-black ink, one accent and a light serif.

Two reference implementations define the two official variants:

| Variant | Reference | Mood | Best for |
|---|---|---|---|
| **Warm / "Aureon"** | Aureon fintech landing page (Figma concept) | Sepia, ochre, antique gold, marble cream | Fintech, payments, wealth, legal, real estate, luxury, hospitality |
| **Cool / "Contra"** | contralabs.com (built in Framer) | Deep teal + mint with saturated reds/golds in the paintings | AI, research, creative tools, dev tools, agencies, education |

---

## How to use this skill

Work through these steps in order. Each one has a detailed reference file.

1. **Brief.** Collect the product, audience, 3–6 key messages and the CTA. Pick the variant (warm or cool) with the decision table in `references/01-art-direction.md`.
2. **Metaphors.** Give every section exactly one literal visual metaphor that *acts out* its headline. Use the metaphor bank in `references/02-metaphor-bank.md`.
3. **Art.** Source or generate the images, cut them out, grade them to one palette and apply the halftone / texture treatments. See `references/03-imagery-and-prompts.md` and `references/04-techniques.md`.
4. **Tokens.** Apply the colour, type, spacing, radius and shadow tokens from `references/05-design-tokens.md`. Ready-made files are in `assets/tokens.css` and `assets/tailwind.preset.js`.
5. **Components.** Build from the specs in `references/06-components.md`. React/Tailwind versions are in `assets/components/`.
6. **Page.** Assemble one of the blueprints in `references/07-page-blueprints.md` (fintech, AI/SaaS, agency/portfolio, D2C/product).
7. **Motion.** Follow `references/08-motion.md`: slow, weighty, scroll-led.
8. **Copy.** Write in the voice from `references/09-copywriting.md`.
9. **Build.** Use `references/10-build-figma.md`, `references/11-build-framer.md` or `references/12-build-nextjs.md`. `examples/landing.html` is a working single-file demo.
10. **QA.** Run every item in `references/13-qa-checklist.md` before handing anything over.

If the user only wants a quick concept (moodboard, single hero, art brief), do steps 1–3 and show the result. Don't build the whole system.

---

## The ten rules (memorise these)

1. **One metaphor per section, and it must be literal.** Scales mean evaluation, a keystone coin means foundation, a key means access. If the image could swap with another section's image and still work, it is decoration. Replace it.
2. **Anachronism is the hook.** Classical figures use modern objects calmly, as if they always had them. Never make it a joke: no sunglasses on statues and no memes.
3. **Loud art, quiet UI.** All saturation lives in the imagery. The UI uses neutrals plus at most one accent.
4. **Never tint the UI to match a painting.** Paintings change from section to section; the UI palette does not.
5. **Light serif, tight leading.** Display serif at weight 300–400, line-height 1.0, tracking −0.03 to −0.05em. Never bold a headline.
6. **Grotesk for function, mono for labels.** Body, buttons and nav use a neutral grotesk. Eyebrows and data use mono or tracked small caps.
7. **Space is the luxury signal.** At most two ideas per viewport. Section padding is 120–200px on desktop.
8. **One grade for every image.** Colour-grade every painting to the variant's palette so the collage reads as one world.
9. **Modern objects must look modern.** Render tech crisply (dark UI) or as black-and-white halftone. Never paint it in the oil style. The contrast is the point.
10. **Legally clean art only.** Use public-domain paintings or original generated images. Never lift images from the reference sites or from living artists.

---

## Fast defaults (when the user gives no constraints)

- **Variant:** cool for AI/SaaS/creative, warm for money/luxury/physical.
- **Fonts:** Source Serif 4 (display), Inter (body/UI) and JetBrains Mono (labels). All are free on Google Fonts.
- **Hero:** eyebrow `// CATEGORY`, a two-beat headline ending in a full stop, one-sentence sub, a dark pill CTA plus an outline pill, and one hero artwork.
- **Sections:** Hero → logo strip → intro + product shot on a painting → 4 stacked feature cards → scroll story → stats → testimonial → closing CTA → dark footer.
- **Motion:** 700ms, `cubic-bezier(0.22, 1, 0.36, 1)`, fade-up 16px, sticky stacking cards and parallax thumbnails.

---

## Anti-patterns (reject these)

- Blue/purple gradients, glassmorphism, neon glows, 3D blobs and emoji icons
- Bold or condensed serif headlines, or more than two typefaces plus a mono
- Mixing the warm and cool variants on one site
- Statues or paintings with no link to the copy ("classical vibe" filler)
- Dense, multi-panel dashboard screenshots. Show one focused widget at a time.
- Cartoonish AI art, plastic skin, or text and garbled letters inside generated images
- Stock-photo people alongside the paintings
- Fast, springy or bouncy animation

---

## File map

```
SKILL.md                         ← you are here
references/
  01-art-direction.md            concept, variant decision, mood, art direction brief template
  02-metaphor-bank.md            80+ headline→image metaphors by industry
  03-imagery-and-prompts.md      sourcing, licensing, AI prompt system, grading recipes
  04-techniques.md               halftone, data-text texture, dot grid, cut-out collage, floating UI
  05-design-tokens.md            colour, type scale, spacing, radius, shadow, grid (measured values)
  06-components.md               every component with exact specs and states
  07-page-blueprints.md          4 full page blueprints, section by section
  08-motion.md                   timing, easing, scroll choreography, reduced motion
  09-copywriting.md              voice, headline formulas, label system, examples
  10-build-figma.md              Figma file setup, styles, layers, export
  11-build-framer.md             Framer setup, effects, scroll transforms, CMS, template packaging
  12-build-nextjs.md             Next.js + Tailwind + Framer Motion implementation
  13-qa-checklist.md             pre-ship checklist
assets/
  tokens.css                     CSS variables for both variants
  tailwind.preset.js             Tailwind preset
  halftone.css                   halftone + paper + data-texture utilities
  components/                    React + Tailwind components
examples/
  landing.html                   single-file demo page (no external images needed)
```
