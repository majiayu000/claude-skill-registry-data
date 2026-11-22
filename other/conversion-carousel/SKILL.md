---
name: conversion-carousel
description: Plan, produce and place a conversion-focused product image carousel where each slide removes one buyer objection, every claim is evidenced, and text is composed in HTML. Use for PDP galleries, ad landing heroes and bundle pages.
---

# Conversion carousel images

Requires `/setup` context for the workspace, store and theme. Apply carousel
changes through `lexsis_pages.edit_context`, `lexsis_pages.source` and
`lexsis_drafts.page_update_section`, with hosted review. Publishing stays with
`/publish`.

A carousel is a sequence of arguments, one per slide. Each slide exists to remove one reason a shopper would hesitate to buy. Your job is to work out which hesitations matter for this buyer, put them in the order the buyer actually has them, and prove each answer with an image and a claim you can back up.

Work in four phases: **understand → plan → produce → ship and check**. Show the slide plan to the person before you spend money on image generation or rebuild a live page, unless they have told you to just go.

---

## Phase 1: Understand the buyer and the evidence

Collect these before planning. Look in project docs, brand context, the catalog, the live page and any ad the traffic comes from. Ask only for what you cannot find.

1. **Who is buying, and for whom.** Self-purchase and gift purchase are different jobs. A gift buyer worries about the recipient's taste, the presentation, the delivery date and looking thoughtful. A self-buyer worries about fit, quality and whether it suits them.
2. **Where they arrive from.** If the traffic comes from an ad, slide 1 must match the ad's promise and visual. If the first thing they see is unrelated to the ad, many leave immediately.
3. **The offer.** Price, bundle tiers, codes, shipping, returns.
4. **The claims ledger.** List every fact you might put on a slide, each with its source: product spec table, store policy page, merchant statement, lab report or real reviews. Anything without a source is not a claim; it is a risk.
5. **Real assets.** Product shots, on-body photos, packaging, unboxing, real customer photos, press and celebrity looks with usage rights. Real beats generated whenever both exist.

### The claim gate (non-negotiable)

Fabricated proof destroys trust faster than missing proof, and in many markets it is illegal. Before any text goes on a slide, check it against the ledger.

- **Never put on a slide without evidence:** review counts, star ratings, "X happy customers", "bestseller", "selling fast", certifications, material-safety claims (nickel-free, hypoallergenic, organic and similar), medical or efficacy claims, celebrity association without written rights, delivery-date promises.
- **Treat suspicious review libraries as unusable.** Signs include many reviews from one reviewer, bursts posted within minutes, or none marked as verified buyers. Tell the person; don't use them.
- **Treat AI-generated product imagery as a draft.** It must faithfully match the real product: same shape, stone colours, finish and proportions. Flag it for the merchant to sign off. Never generate fake customers, fake UGC or fake reviews.
- **Keep prices out of images by default.** They go stale and contradict the live offer. Put prices in live HTML next to the carousel. Bake prices in only if asked, and then only the current, verified ones.
- When a strong slide idea lacks evidence, swap it for a true fact that answers the same objection. For example, replace "9,000+ happy customers" with "Free shipping across India". Then tell the person what evidence would unlock the stronger version.

---

## Phase 2: Plan the slides (the psychology)

### How people actually consume carousels

- **Most people only see slide 1.** Swipe-through rates are low, so slide 1 must work alone: it shows what the product is, makes it look desirable, and states the core promise in a few words. Never open with a logo, a lifestyle mood shot with no product in it, or a trust grid.
- **First and last get remembered** (serial position effect). Put your strongest desire image first and your risk-removal or trust slide last, because that is what they carry to the buy button.
- **One idea per slide.** Each slide gets a short headline (≤ 8 words ideal, 12 max), one visual, and at most 3 supporting labels. Cognitive load kills swipes.
- **Mobile is the real canvas.** A 1080 px wide slide displays at about 360 px on a phone, roughly one third of its size. Size text for the phone (see the design rules below).

### Psychology levers and what they look like on a slide

| Lever | What it means | On a slide |
|---|---|---|
| Processing fluency | Easy to understand feels true and good | One message, big clear product, generous space |
| Concreteness and specificity | Specific details are believed more | "Kundan set by hand" with an arrow to the stone, not "premium quality" |
| Mental simulation | Seeing it on a body lets them imagine owning it | On-ear, on-wrist or in-hand shots; scale reference |
| Quality inference from detail | Close-ups signal craftsmanship and justify price | Extreme macro shots with callout lines to materials |
| Jobs-to-be-done and occasions | People buy for a moment, not a SKU | "One pair for every day of Diwali", "Desk to dinner" |
| Risk reversal and loss aversion | Fear of a bad purchase outweighs desire | Returns, delivery speed, secure payment, gift box |
| Effort signalling (gifts) | Givers want to look thoughtful with low effort | "Arrives gift-boxed, no wrapping needed" |
| Anchoring and value framing | Price is judged against a reference | Per-unit maths, bundle saving, cost per wear (live HTML preferred) |
| Choice architecture | Too many options stall decisions | Variant lineup with names; highlight one default or best value |
| Social proof and authority | Others' choices reduce uncertainty | Only real: verified reviews, real UGC, press, celebrities with rights |
| Self-referencing | "This is for someone like me" | Model, styling and setting matched to the target customer |
| Novelty versus familiarity | Too traditional or too odd both repel | Mix the familiar product with a fresh styling context (e.g. designer styling for traditional jewellery) |

### Slide archetypes (pick 4 to 6)

Map each slide to the objection it answers. For every slide, write down: **job → objection → lever → headline → visual → evidence**.

1. **Identity and desire** (almost always slide 1). The product or range, beautifully lit, with a short promise. A collage works for multi-variant offers: each variant in a grid tile with its name.
2. **Up close and quality proof.** An extreme macro with 2 or 3 callout labels connected by thin lines, each label pointing at the actual feature. Answers "will it look cheap?"
3. **On-body and scale.** Shows the real size and how it is worn. Answers "how big is it, will it suit me?" A real photo is strongly preferred; generated only as a stand-in, flagged.
4. **Occasion or use story.** Variants mapped to moments (days of a festival, outfits, routines). Answers "why do I need more than one?" and lifts bundle size.
5. **Variant lineup or choice helper.** Names, one visible difference each, best-value marker.
6. **What's in the box or gift-ready.** Real packaging. Answers "do I have to wrap it, is it presentable?"
7. **How it's made or materials.** 3 steps or a materials stack, only from the spec sheet.
8. **Comparison.** Against the realistic alternative (marketplace knock-off, sweets box, generic gift). Only verifiable differences.
9. **Social proof.** Real reviews, UGC, press or celebrity looks. Skip the slide entirely if none qualify.
10. **Trust and risk reversal** (often the last slide). An icon grid of 4 or 5 facts: shipping, dispatch time, returns, payment methods, gift box, warranty. Each must be in the ledger.

**Default sequences**

- **Ad landing page (cold traffic, gifting):** Identity → Up close → Gift-ready → Occasion story → Trust.
- **PDP gallery (one SKU):** Identity → On-body/scale → Up close → In the box → Materials/how made → Trust or proof.
- **Bundle page:** Identity collage of all variants → Up close → Occasion map → Value framing (HTML) → Trust.

### Category notes

- **Jewellery.** The macro detail and the on-body scale shot are the two biggest levers. State plating and base metal precisely ("22K gold plated over brass", not "gold"). Show the packaging for gifting.
- **Beauty and skincare.** Texture swatch, before/after only if real and compliant, ingredient callouts from the INCI list, no efficacy numbers without studies.
- **Apparel.** Fit on multiple body types, fabric macro, size guidance, styling outfits.
- **Supplements and food.** Ingredients and sourcing facts only; no health claims beyond the approved label.
- **Home.** Scale in a room, materials macro, dimensions slide.

---

## Phase 3: Produce the slides

### Asset rules

- Use real assets first: `lexsis_asset_library.search` and `lexsis_catalog.get`, then `lexsis_assets.view` on each candidate.
- Generate only after the plan is approved and `lexsis_workspace.credits` is confirmed, with `lexsis_drafts.asset_generate` and the real product photo as reference, following the asset generation policy. Describe the shot type, ask for the exact product "reproduced precisely, no changes", and ask for no text or watermark.
- View every generated image against the real product with `lexsis_assets.view`, and regenerate any that drift.
- **Text and layout:** compose the slides in HTML, never inside the image model. You get crisp, correct type, brand fonts, exact claims and fast edits.

### Design rules for a 1080×1350 (4:5) slide

- Use brand colours and fonts.
  - Use the fonts from the selected theme.
- Minimum sizes so text survives the phone downscale (about 0.33×):

  | Element | Minimum size at 1080 px |
  |---|---|
  | Headline | 70–80 px |
  | Eyebrow | 28–30 px |
  | Body | 34–38 px |
  | Labels and pills | 30–36 px |
  | Tile titles | 40–44 px |
  | Tile body | 28–30 px |

- Keep a 70 px safe margin. Put the headline in the top third and keep the product clear of the text.
- Callout labels are solid pills with a 2 px line ending in a dot placed *on* the feature. Check the dot positions after rendering.
- **No decorative frames or inner borders by default.** Plain, full-bleed slides look more premium and avoid double borders inside the page's own card styles.
- Give icon grids one consistent stroke icon set and short two-line tiles (title plus 2–4 word subline).
- Slides must read as one family: same eyebrow style, headline style and colour logic.

### Render

Write one HTML file with one 1080x1350 `overflow:hidden` section per slide, using brand fonts and locally saved source images. Screenshot each section as JPEG with the host browser. Make a contact sheet at 360 to 430 px wide and check:

- every word is readable at that size;
- each slide carries one idea;
- callout dots sit on the right features;
- slide 1 and the last slide work alone.

Fix and re-render before uploading.

### Upload

Upload each JPEG with `lexsis_asset_upload.upload`, with alt text stating the slide's claim. Use new filenames when replacing slides so the CDN does not serve stale copies.

---

## Phase 4: Ship on the page and check

### Carousel markup (minimal, fast, accessible)

- Build a scroll-snap track:
  ```css
  .track { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; }
  .slide { flex: 0 0 100%; aspect-ratio: 4/5; scroll-snap-align: start; scroll-snap-stop: always; }
  ```
  Hide the scrollbar.
- Image loading: slide 1 gets `loading="eager" fetchpriority="high"` plus `srcset` 640/1080; the rest get `loading="lazy"`.
- Alt text on every slide states the slide's message, so screen readers and SEO get the argument too.
- **Default chrome is minimal:**
  - Full width, no border.
  - No arrows and no autoplay; the user swipes.
  - A subtle "1 / N" counter pill in a corner, so people know there is more.
  - A pure-CSS counter is possible: keep a hidden indicator span per slide, toggle `[data-on]` from a small scroll listener, and show `content:"k / N"` on `:nth-child(k)::before`.
  - Add progress bars, arrows, autoplay or a peek of the next slide only if the person asks.
- If the slides carry the headline, hide the page's duplicate visible H1 with an sr-only pattern rather than deleting it; the H1 still matters for SEO and screen readers.
- Keep the offer and price block in live HTML directly below the carousel.

### QA before calling it done

- At 390 px:
  - no horizontal page overflow;
  - the carousel swipes and the counter updates;
  - slide 1 loads first;
  - the offer block is reachable within about 1.5 screens.
- At desktop width, the carousel sits correctly in the hero grid.
- Re-read every on-slide claim against the ledger one last time.
- Report:
  - the slide plan (slide → objection → lever);
  - what is AI-generated and needs merchant sign-off;
  - which stronger slides are blocked on evidence, and what evidence would unlock them;
  - the preview link.

  Publish only on explicit approval.

---

## Output format for the plan (show before producing)

```
Buyer: <who, for whom, from which traffic>
Core promise: <one line>

| # | Slide job | Objection answered | Lever | Headline (≤12 words) | Visual | Evidence |
|---|-----------|--------------------|-------|----------------------|--------|----------|
| 1 | Identity  | What is it / do I want it | Desire, fluency | ... | ... | catalog |
...

Blocked by missing evidence: <slide ideas + what would unlock them>
Assets to generate: <list, flagged for sign-off>
```

Leave out any slide whose evidence is missing, and say what was left out.
