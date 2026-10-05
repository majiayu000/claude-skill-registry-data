---
name: 9design-assets
description: "Generate the production asset stage of the 9Designer pipeline from approved 9image-design prototype images, an existing reference asset kit, mockup folder, or reference boards. Use when the user wants each logo, icon, UI element, texture, background, and website asset generated individually with imagegen, saved into a clean asset-exports folder, and prepared as input for 9assets-website."
---

# 9Design Assets

## Purpose

Take an existing reference asset kit, prototype image set, or approved design board and turn it into separated image files for website implementation. This is the bridge between a visual prototype kit and a real website build.

This skill must generate assets as individual images with the image generation tool, then run real background cleanup for all reusable non-background assets. Do not hand-build low-quality SVG approximations as the primary output.

## Five-Step Process

### Step 1: Reference The Kit

Read the provided asset kit or reference image folder first.

Look for:

- `asset-manifest.json`
- `00-reference/`
- `01-logo/`
- `02-icons/`
- `03-imagery/`
- `04-ui-components/`
- `06-design-tokens/`
- `07-export-sheets/`
- Any page mockups, generated prototype screens, UI boards, icon sheets, or logo sheets

If the user gives only attached images, treat those images as the reference kit.

Do not invent a new visual style. The output must follow the supplied kit exactly: same brand identity, colors, lighting, composition language, typography mood, icon style, UI styling, borders, shadows, masks, and texture system.

Identify which elements should become reusable image assets and which must remain HTML/CSS text. Normal navigation, headings, paragraphs, buttons, cards, CTA text, form labels, and footer copy should stay code-native. Generate text as an image only for a decorative logo, custom wordmark, hand-lettered title, poster, sign, packaging, or artwork where the text is part of the visual object.

Identify every social media/community icon and record whether it is a standard platform glyph, a stylized brand-world glyph, or a text link. Standard platform glyphs should stay vector-quality and visually match the design treatment; stylized glyphs should be generated as clean transparent assets.

Asset fidelity rules:

- Match icon metaphor, stroke/fill style, optical weight, corner style, color, padding, and alignment from the approved design. Do not swap in generic nearby icons.
- Match actual colors from the design; do not warm, cool, mute, or "improve" the palette.
- Preserve the accepted media treatment. If the design has no color overlay on an image, do not add one to the exported asset.
- Generate implementation-friendly assets with stable aspect ratios, clean edges, and enough resolution for desktop and mobile.
- Product/background assets may include text or branding only when that text belongs inside the asset itself, such as a poster, sign, packaging, or card artwork.
- Interactive UI text, buttons, forms, navigation, and page copy should stay code-native in the website build, not baked into decorative images.

### Step 2: Create The Export Plan

Create a short asset checklist before generating.

Default required set and background policy:

- `logo-primary`: isolated, transparent preferred, otherwise flat neutral background
- `logo-wordmark`: isolated, transparent preferred, otherwise flat neutral background
- `logo-mark`: isolated, transparent preferred, otherwise flat neutral background
- `favicon`: isolated square, transparent preferred, otherwise flat neutral background
- Exactly `5` core icons unless the user specifies a different count: isolated, transparent preferred, otherwise flat neutral background
- `social-icon-set`: exact social/community icon glyphs from the approved design, isolated and transparent or vector-quality, including matched container styling when present
- Primary button: isolated component only, no page background
- Secondary button: isolated component only, no page background
- Navigation bar: isolated nav component only, no page screenshot background
- Mobile navigation: isolated component only, no page screenshot background
- Card component: isolated card only, no page screenshot background
- Form input: isolated input only, no page screenshot background
- CTA banner: isolated banner component only; include its internal designed background only if that background is part of the banner itself
- Footer module: isolated footer component only; include its internal designed background only if the footer needs it
- Hero background: full-bleed background image allowed
- Section background or texture: full-bleed or seamless background image allowed
- Decorative overlay or divider: transparent preferred; no full page background

Add extra assets only when the reference kit clearly requires them or the user asks.

Speed-safe prioritization:

- P0 assets: required for the first faithful website build. Generate or validate these first: logo/wordmark/favicon, hero/background art, visual-world icons and social icons, textures/dividers/overlays, and page-specific imagery visible in approved references.
- P1 assets: useful for polish or repeated sections. Generate after P0 if they are visible: gallery cards, decorative objects, CTA/footer visuals, hover/active variants.
- P2 assets: optional boards or alternates. Skip in fast mode unless the user asks or the website builder needs them to resolve ambiguity.
- Do not generate image assets for normal HTML text, simple buttons, basic forms, or plain cards when code-native CSS can faithfully reproduce them faster.

Reference-driven asset coverage:

- Logo mark as transparent PNG.
- Brand wordmark as transparent PNG when the typography is decorative or hard to reproduce with CSS.
- Hero artwork/background as a clean high-resolution image.
- Standalone hero characters, objects, foreground props, or floating motifs with transparency when they layer over the page.
- Section illustrations for story, showcase, gallery, feature, CTA, and footer areas.
- Custom illustrated feature-card icons as transparent PNGs when icons are visual world elements.
- Gallery images, visual cards, framed artwork, or masks matching the reference style.
- CTA background artwork or decorative objects.
- Background textures, patterns, dividers, clouds, waves, leaves, stars, magic effects, mountains, animals, or other motifs found in the reference.
- Footer logo and small decorative visuals when present.

For each asset, decide:

- Source reference image or board
- Target filename
- Target folder
- Aspect ratio and background policy: `transparent`, `flat-neutral`, `full-bleed-background`, or `component-internal-background`
- Whether it must be generated as an isolated object, full-width image, component strip, or square icon
- Exact fidelity notes: color, stroke/fill, typography mood, radius, shadow, padding, crop, and whether text is allowed inside the asset
- Whether the website builder must provide accessible hidden text for a decorative image-text asset

### Step 3: Scaffold The Export Folder

Create a dedicated output folder in the current workspace unless the user gives another path:

```text
asset-exports/<project-slug>-YYYYMMDD-HHMM/
```

Use the bundled script:

```bash
python <skill-dir>/scripts/create_asset_export.py --name "<project name>" --root "<workspace>" --source-kit "<path-to-reference-kit>"
```

Save outputs into:

```text
00-source-kit/          Source kit manifest, copied refs, or source notes
01-logos/              Separate generated logo images
02-icons/              Exactly 5 generated core icon images by default
03-ui-elements/        Buttons, nav, cards, form, CTA, footer images
04-backgrounds/        Hero, section, texture, overlay, divider images
05-page-assets/        Larger page-specific reusable image assets
06-ready-for-builder/  Final renamed copies for the website-building skill
notes/                 Asset plan, prompts, font notes, implementation notes
asset-export-manifest.json
```

Bundled scripts:

- `scripts/create_asset_export.py`: creates the export folder and manifest.
- `scripts/remove_background.py`: removes baked-in flat/checkerboard backgrounds and verifies alpha transparency.
- `scripts/validate_asset_manifest.py`: validates the manifest shape and flags missing Phase 2 fields before website handoff.

Optional cleanup accelerators:

- `rembg` may be used for complex foreground extraction when available.
- Segment Anything/SAM may be used for difficult object boundaries when available.
- Pillow, ImageMagick, or Sharp may be used for resizing, alpha inspection, format conversion, or optimization when available.
- These tools are optional. If they are unavailable, use the bundled cleanup script and regenerate failed assets on a flat neutral background.
- When `remove_background.py --mode auto` cannot use optional `rembg`, it should fall back cleanly and report fallback guidance instead of blocking the workflow.

### Step 4: Generate Each Asset Separately With Imagegen

Use the image generation tool for every visual asset. Generate each requested asset as its own separate image, not one combined sheet, unless the user explicitly asks for a sheet.

Required behavior:

- Generate `logo-primary` separately.
- Generate `logo-wordmark` separately.
- Generate `logo-mark` separately.
- Generate `favicon` separately.
- Generate each of the 5 core icons separately as `icon-01-*` through `icon-05-*`.
- Generate each social/community icon separately when the approved design shows social links. Do not substitute generic icons or text labels.
- Generate each UI element separately: buttons, nav, mobile nav, card, form input, CTA banner, footer module.
- Generate each background or texture separately.
- Generate logos, icons, and UI components without the screenshot/page background. They must be clean isolated implementation assets.
- Save or move each generated image into the correct folder.
- Run background cleanup for every reusable non-background asset before copying it into `06-ready-for-builder/`.
- Copy only cleaned and verified final files into `06-ready-for-builder/`.

Do not satisfy this step by drawing SVGs manually. Optional SVG tracing can happen later, but only after the image exists.

Social icon generation rules:

- Do not generate social icons as text labels unless the approved design shows text labels.
- If the icon is a known platform mark, use an official/vector-quality glyph where available and style its surrounding circle, square, stroke, fill, shadow, or texture to match the design.
- If the approved design uses illustrated or custom social icons, generate each as its own transparent PNG.
- Keep social icon optical size, padding, baseline, stroke/fill weight, and corner style consistent with the rest of the icon set.
- Export hover/active variants when the prototype shows a state change.

Use transparent backgrounds when possible for logos, icons, overlays, dividers, and decorative elements. If imagegen cannot reliably output transparency, use a plain flat neutral background with no texture, no gradient, no scene, no screenshot, then run background cleanup.

Use full-bleed backgrounds only for assets whose purpose is the website background itself, such as `hero-background`, `section-texture`, or a true background pattern. Never put the page background behind a logo, icon, button, card, nav, form, or reusable UI element.

### Step 4.5: Mandatory Background Cleanup

For every asset whose manifest has `background_cleanup_required: true`, run:

```bash
python <skill-dir>/scripts/remove_background.py --input "<generated-image>" --output "<asset-export>/<folder>/<asset-id>.png" --mode auto
```

Then copy the cleaned file into:

```text
06-ready-for-builder/<asset-id>.png
```

Required cleanup behavior:

- Logos, wordmarks, favicons, icons, overlays, dividers, buttons, nav, cards, forms, CTA modules, and footer modules must be cleaned before handoff.
- Optional advanced tools such as `rembg`, Segment Anything/SAM, Pillow, ImageMagick, or Sharp may be used as escalation paths for complex edges, but they are not required dependencies.
- Do not pass through images that show a checkerboard background. A checkerboard pattern inside the PNG means transparency failed; run cleanup or regenerate on a flat neutral background and clean again.
- Do not pass through white/gray/pink/blue gradient backgrounds behind isolated assets.
- Update the manifest with `background_cleaned: true`, `alpha_verified: true`, `background_removal_method`, and `background_removal_needed: false` after cleanup succeeds.
- If alpha cannot be verified, leave `background_removal_needed: true`, do not copy that asset into `06-ready-for-builder/`, and report it as a blocker or regenerate it.
- Full-bleed background assets do not need alpha cleanup unless they are overlays or dividers.

### Step 5: Package For The Next Website Skill

Update `asset-export-manifest.json` so another skill can consume the folder without guessing.

Include for each asset:

- Asset id
- File path
- Folder
- Type: logo, icon, ui-element, background, texture, page-asset
- Asset role: `background`, `foreground-object`, `transparent-overlay`, `icon`, `logo`, `ui-chrome`, `decorative-image-text`, `code-native-reference`, or `texture`
- Source reference
- Generation prompt summary
- Intended website use
- Notes about transparency, aspect ratio, state, and responsive use
- Responsive variants: desktop, tablet, mobile, density-specific, or not-applicable
- Accessibility notes: alt text, decorative empty alt, aria label, or hidden text requirements
- Token dependencies: colors, font notes, radius, shadow, spacing, or motion tokens required by this asset
- Background policy and whether background removal is needed before implementation
- Cleanup fields: `background_cleanup_required`, `background_cleaned`, `alpha_verified`, `background_removal_method`, and `background_removal_needed`
- Text policy: `code-native-text`, `decorative-image-text`, or `no-text`; for decorative image text, include the exact accessible text that the website must expose.
- Icon policy: `official-vector`, `generated-transparent-png`, `custom-svg`, `code-native`, or `not-an-icon`.
- Interaction state: default, hover, active, selected, disabled, or not-applicable.
- QA notes: visual risks, cleanup caveats, expected background, and downstream implementation warnings

Also create:

- `notes/asset-plan.md`
- `notes/generation-prompts.md`
- `notes/font-and-token-notes.md`
- `notes/builder-handoff.md`
- `notes/icon-inventory.md`
- `notes/social-icons.md`

Before handoff, run the manifest validator:

```bash
python <skill-dir>/scripts/validate_asset_manifest.py "<asset-export-folder>" --check-files
```

Use `--strict` for new exports that should include every Phase 2 manifest field. Older manifests may produce warnings instead of failures so existing kits remain readable.

The final response must include the export folder path, number of generated images, and any missing or uncertain assets.

## Imagegen Prompt Requirements

Every prompt must include:

- The source kit or reference images being followed
- The exact single asset being generated
- Instruction to keep the asset visually identical to the kit style
- Background requirement: transparent, flat neutral, component-internal, or full-bleed background
- Output purpose: website implementation asset
- Clean framing with no extra unrelated objects
- Fidelity anchors: exact color family, icon weight, edge treatment, radius, shadow, and asset role

Example:

```text
Generate one separate website implementation image asset: icon-03-search. Use only the supplied reference asset kit for style. Match the exact approved icon language, stroke weight, corner radius, color palette, glow/shadow treatment, and typography mood. Create a clean isolated icon with transparent background if possible; if transparency is not possible, use a perfectly flat neutral background with no texture, gradient, scene, or page screenshot. Center the icon, no labels, no extra icons, no sheet layout.
```

For UI elements:

```text
Generate one separate website implementation image asset: button-primary. Use only the supplied reference asset kit for style. Match the approved button shape, fill, border, glow, shadow, typography mood, and spacing. Output only the isolated button component, not the page background and not a screenshot crop. Use transparent background if possible; otherwise use a flat neutral background suitable for clean background removal.
```

For true backgrounds only:

```text
Generate one separate website implementation image asset: hero-background. Use only the supplied reference asset kit for style. This asset is a full-bleed website background, so include the atmospheric background art, lighting, texture, and composition. Do not include text, logos, buttons, cards, navigation, or UI elements.
```

## Rules

- Always use imagegen for the visual asset itself.
- Always run background cleanup for reusable non-background assets before website handoff.
- Never accept a baked-in checkerboard as transparency.
- Generate separate files, not one giant board.
- Do not crop the supplied screenshot as the primary source for reusable assets unless the user explicitly allows it. Generate clean assets that match the reference instead.
- Keep implementation assets isolated. Logos, icons, UI elements, overlays, and dividers must not include the page background from the screenshot.
- Only true background assets may include full-bleed background art.
- Default to exactly 5 icons unless the user asks for more or fewer.
- Do not redesign the brand.
- Do not create generic icon packs or generic UI components.
- Do not output SVG-only assets as the final deliverable.
- Preserve the source kit as reference and write a manifest for downstream website building.
