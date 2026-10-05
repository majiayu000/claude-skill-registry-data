---
name: brand-lock-extractor
description: Extract a production-ready brand-lock.md from a brand's existing assets. Point it at a website URL, a brand book PDF, screenshots, or a written description and it produces the nine-section brand-lock the rest of shotkit consumes, with a confidence and source noted for every value. Use when the user wants to onboard a brand, says "build a brand lock", "extract my brand", "make a brand pack from my site", or hands over brand assets. The cold-start killer that turns a blank brand-pack template into a filled, validate-ready file. Pairs with storyboard-architect downstream.
---

# Brand Lock Extractor

The blank brand-pack template (`_template.md`) is the single biggest point of friction in shotkit. Nobody wants to hand-author nine sections of brand parameters before they can produce a single storyboard. This skill removes that wall: hand it what you already have, get a filled brand-lock back.

The output is a `brand-lock.md` in the exact format `validate_brand_lock.py` validates and every other skill consumes. Same file the pipeline reads, produced from your assets instead of from scratch.

This skill extracts. It does not invent. Every value is sampled from a real asset or flagged as an estimate the user must confirm. A confident-sounding wrong hex is worse than a flagged guess.

## Where the tools and packs are

After `./install.sh`, the validators and helpers are in `~/.claude/shotkit-tools/` and the
brand packs are in `~/.claude/shotkit-brand-packs/`. A `--project` install puts both
under `./.claude/` instead. From a repo clone they are `tools/` and `brand-packs/`. The
commands below give the installed path first and the clone path second. The tools need
`pip install pyyaml jsonschema`.

## When to use

Trigger when the user:

- Wants to onboard a brand into shotkit and has assets (a site, a brand book, screenshots)
- Says "extract my brand", "build a brand lock", "make a brand pack from my site/PDF"
- Hands over a URL, a PDF, image files, or a written brand description and asks for a brand-lock
- Has a brand-lock that is half-filled and wants the gaps extracted from assets

If the user has nothing but a vague idea (no assets, no description), they are not extracting, they are authoring. Point them at `~/.claude/shotkit-brand-packs/_template.md` (from a clone, `brand-packs/_template.md`) and help them fill it directly.

## Inputs

You can work from any one of these. More sources is a better extraction.

| Source | How you read it | Best for |
|---|---|---|
| Website URL | `WebFetch` homepage + about + one more page | Voice, positioning, palette, type |
| Brand book PDF | `Read` the PDF | Palette (exact hex), type, motion rules |
| Screenshots / image files | `Read` the images | Palette (sample pixels), mood, layout |
| Written description | Use directly | Identity, archetype, voice posture |

At minimum you need one source. If the user offers none, ask for the one they have: **"What can I work from, a website URL, a brand book PDF, screenshots, or a short description?"** One question.

## Workflow

### Step 1. Gather the source material

- **URL:** `WebFetch` the homepage, then try the about page (`/about`, `/about-us`, `/our-story`) and one more (`/services`, `/work`, recent blog). Skip pages that 404. The homepage is the floor.
- **PDF / images:** `Read` each file. Brand books carry exact hex and type; screenshots are for sampling color and reading mood.
- **Description:** take it as written.

Tell the user what you are pulling. Do not ask follow-ups yet, extract first, confirm gaps at the end.

### Step 2. Extract each section

Read `references/extraction-rubric.md`. It maps every brand-lock section to where the signal lives and how to read it. Work the nine sections in order:

1. **Identity** (brand, one-line description, archetype, voice posture)
2. **Palette** (sampled hex, by role)
3. **Typography** (display, body, optional mono, with weights)
4. **Mood adjectives** (3-5, specific, contrast clauses preferred)
5. **Never list** (what the brand avoids, inferred from consistency)
6. **Aspect ratios**
7. **Color grade direction** (one sentence)
8. **Motion language** (one paragraph)
9. **Voice rules** (copy-level constraints)

For every value, hold two things: the value, and where it came from (which asset, which quote, which sampled swatch). You will need the source for the confidence pass.

### Step 3. Assign confidence and flag estimates

Each value is one of:

- **extracted**, read directly from an asset (a hex in the brand book, a font in the CSS, a quote from the site). State it plainly.
- **inferred**, reasoned from evidence but not stated (archetype from positioning, never-list from consistency). Reasonable to ship, worth noting.
- **needs confirmation**, your best estimate where the assets were silent or ambiguous (a color sampled from a JPEG with compression, a font you could not identify). Fill it, then flag it.

### Step 4. Write the brand-lock

Use `templates/brand-lock.md.tpl`. Fill **every** required section, no placeholders left behind. Then append an `## Extraction notes` section that lists every `inferred` and `needs confirmation` value with its source and your reasoning. This section is the audit trail; it does not break validation (the validator checks the nine required sections are present, extra sections are fine).

Set the footer: `Last updated` to today, `Owner` to the user or "extracted", `Version: 1.0`.

### Step 5. Self-check, then hand off

Before you present it, confirm the file would pass validation:

- All nine required sections present: Identity, Palette, Typography, Mood adjectives, Never list, Aspect ratios, Color grade direction, Motion language, Voice rules.
- Identity contains all four fields: Brand, One-line description, Archetype, Voice posture.
- Palette has at least one real `#RRGGBB` hex (not a placeholder).

Then hand off:

> "Here is your brand-lock. I sampled the palette and type from your assets and flagged N values that need your eyes (see Extraction notes). Save it next to your other brand packs, confirm the flagged values, and run `python ~/.claude/shotkit-tools/validate_brand_lock.py --require-configured path/to/file.md` to verify (from a clone: `python tools/validate_brand_lock.py --require-configured path/to/file.md`). Then: `'30-second explainer. Use brand-packs/your-brand.md as the brand lock.'`"

## Hard rules

### Rule 1. Never invent a hex value

Colors are sampled, never guessed. Read them from a brand book, from CSS, or by sampling pixels in a screenshot. If you genuinely cannot determine a color, fill your closest estimate and mark it `needs confirmation` in Extraction notes. "Navy" is not a palette entry. `#0F1F3A` is. A wrong hex stated confidently corrupts every downstream prompt.

### Rule 2. Never fabricate a typeface

Identify fonts from the brand book, the site's CSS/font files, or clear visual match. If you cannot identify one, say so and flag it, do not name a plausible-sounding font you did not verify.

### Rule 3. Source everything

Every extracted value traces to an asset. Every inferred value traces to reasoning. This is the same audit-trail discipline as the brand-lock snapshot, applied at extraction time.

### Rule 4. The never-list is the highest-value section

It is also the hardest to extract, because brands document what they do, not what they avoid. Infer it from consistency: if every image avoids stock-photo gloss, that is a never. If copy never uses exclamation points, that is a never. Read `references/extraction-rubric.md` for the method. Do not ship an empty never-list.

### Rule 5. Mood adjectives must be specific

"Professional, modern, clean" describes every brand and constrains nothing. Extract contrast clauses that do work: "operator not creator", "warm not precious", "confident without volume". If the assets only support generic adjectives, that is a `needs confirmation` flag, not a license to ship filler.

### Rule 6. No emojis, no hype

The output is a clinical specification. It models the standards the brand-lock enforces. No emojis anywhere. No marketing adjectives about the brand in your own voice, report what the assets show.

## Reference

- `references/extraction-rubric.md`, section-by-section extraction method and confidence definitions.

## Example

`examples/` contains a worked extraction: the source material provided (`input-brief.md`) and the `brand-lock.md` produced from it, including the Extraction notes audit trail. Use it to calibrate the level of specificity and the confidence flagging.
