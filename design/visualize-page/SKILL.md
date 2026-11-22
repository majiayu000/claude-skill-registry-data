---
name: visualize-page
description: "Turn an approved storefront page plan into mobile-first concept images for visual review, then infer or generate larger-screen treatments from the approved mobile direction. Supports focused iteration; concepts are not production page assets."
---

# Visualize a Planned Page

Create concept frames that let the user see the planned page before
implementation. This skill is optional. It does not change strategy, produce
production media, author source, or create a hosted page.

Read:

- the complete plan and its `PLAN_APPROVED` record;
- the selected store's `brand.md`, `design.md`, `persona.md`, theme CSS, and
  relevant `products.md` rows;
- live product details and real product media through `lexsis_catalog.get`.

If the plan is blocked, unapproved, missing final copy, or missing section
layout intent, return to `/plan-page`.

## Capability Discovery

Inspect the image-generation and image-editing capabilities available in the
current client. Do not assume a particular external tool exists and do not
hardcode provider names.

Build a small internal matrix for:

- text-to-image and reference-image generation;
- product-preserving compositing;
- aspect ratios and output size;
- editing/inpainting;
- cost or credits;
- permanent output availability.

Use a user-selected available capability when named. Otherwise choose the
best available fit. When no suitable external capability is available, use
`lexsis_assets.capabilities`, check `lexsis_workspace.credits`, obtain
approval for the named batch and cost, then use
`lexsis_drafts.asset_generate`.

Resolve unfamiliar tool schemas through exact router/action discovery. A
concept request does not authorize an undisclosed paid batch.

## Frame the Page

Split the page into contiguous concept frames:

- give a visually dominant section its own frame;
- otherwise combine two neighbouring sections;
- preserve the page order;
- ten sections will commonly produce about five frames, but coverage decides
  the count.

For each frame carry forward:

- section ids and their hierarchy;
- final headline, CTA, and critical labels;
- mobile hierarchy, commerce controls, thumb reach, and media proportions;
- theme palette and typography character;
- real product identity references;
- the one bold moment and surrounding visual restraint.

Generate the 390 mobile concept first for every frame. Mobile is the canonical
visual direction because commerce hierarchy, media height, product controls,
sticky purchase behaviour, and interaction placement are decided there first.

After the mobile frame is approved:

- infer the 768/1280 treatment from the same hierarchy, visual thesis, source
  media, focal point, and section order by default;
- generate a larger-screen concept image only when the user asks for it or
  when visual confirmation is necessary;
- never design desktop independently and then retrofit mobile.

A mobile portrait banner may require a taller source while desktop needs a
wide crop. Record both requirements even when they derive from one master
image. Preserve subject identity, scene, lighting, palette, and focal intent
across sizes.

Concept text may be visually abbreviated when the image tool cannot render
long copy reliably, but the hierarchy and placement must reflect the final
plan. Never treat generated text, prices, reviews, or product labels as
factual.

## Product and Proof Integrity

- Use real product media as the identity reference.
- Do not generate a replacement product, package, logo, certification, press
  mark, customer result, reviewer, or founder.
- A generated approximation is never evidence of product appearance.
- Label every output `concept-only`.
- If a concept is persisted in the Lexsis asset library, import it through
  `lexsis_asset_import.import`, tag its purpose as `concept-only`, and keep it
  out of production asset bindings.

## Review and Iterate

Present concepts in page order:

```markdown
## Concept frames

| Frame | Sections | Mobile output | Larger-screen treatment | Key decisions | Status |
|---|---|---|---|---|---|
| F1 | S1-S2 | <id/url> | inferred from mobile | tall hero, product low-left, quiet upper third | review |
```

Ask the user for frame-specific changes. Regenerate only rejected frames and
retain accepted ones. Track revisions:

```markdown
## Visual decisions

| Decision | Approved direction | Applies to |
|---|---|---|
| Hero composition | product low-left, copy above | F1 / S1 |
```

Record responsive asset implications for `/plan-assets`:

```markdown
## Responsive asset implications

| Slot | Mobile aspect and target | Larger-screen aspect and target | Derivation | Focal/quiet-zone rule |
|---|---|---|---|---|
| A1 | 4:5, 1080x1350 | 3:2, 1800x1200 | same master, art-directed crops | product left; quiet upper/right |
```

If feedback changes final copy, section order, claims, offer, or required
asset jobs, return the affected decision to `/plan-page` for revision and
approval before continuing.

## Status

- `VISUAL_DIRECTION_IN_REVIEW`: at least one frame awaits approval;
- `VISUAL_DIRECTION_APPROVED <who> <ISO date>`: every frame and the recorded
  visual decisions are approved;
- `VISUAL_DIRECTION_SKIPPED`: the user chooses to continue without concepts.

Return the frame table, visual decisions, status, and concept references for
`/plan-assets` and `/design-page`. Concepts guide production and layout; their
URLs are never placed in the page.
