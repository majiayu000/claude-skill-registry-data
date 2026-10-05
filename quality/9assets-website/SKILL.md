---
name: 9assets-website
description: Build the website stage of the 9Designer pipeline from a prepared production asset export folder. Use as the final modular skill after 9image-design and 9design-assets when the user provides an `asset-exports/...` or similar folder containing separate generated images, logos, icons, UI elements, backgrounds, design tokens, and `asset-export-manifest.json`, and asks to build the full real website.
---

# 9Assets Website

Use this as the final build-stage skill in the image-to-website pipeline.

Pipeline order:

1. `9image-design`: create and approve the first landing-page direction, then prototype the full system.
2. `9design-assets`: generate each logo, icon, UI element, background, and reusable visual as separate image files.
3. `9assets-website`: build the complete working website from those exported assets.

Optional expanded kit step: `9design-kit` can create broader brand-system boards between design and assets when needed.

Bundled optional QA helpers:

- `scripts/create_fast_track_plan.py`: creates `docs/research/FAST_TRACK_PLAN.md` for faster critical-path execution.
- `scripts/create_reconstruction_contract.py`: creates `docs/research/RECONSTRUCTION_CONTRACT.md` before coding.
- `scripts/capture_visual_qa.mjs`: captures desktop, tablet, and mobile screenshots with Playwright when Playwright is installed.
- `scripts/compare_visual_qa.mjs`: creates pixel diff summaries and diff images when `pixelmatch` and `pngjs` are installed.
- `scripts/create_visual_qa_ledger.py`: creates `docs/research/VISUAL_QA_LEDGER.md` with or without automated summaries.
- `scripts/score_visual_qa.py`: scores the final build against the visual benchmark rubric with automated hints and manual category scores.
- `scripts/validate_production_readiness.py`: checks deploy-readiness evidence before final handoff.

These helpers are optional. Do not block a website build only because Playwright, pixelmatch, or pngjs is unavailable; use manual browser screenshots and the same ledger categories instead.

For public examples, benchmark submissions, or final quality review, read `references/visual-benchmark-rubric.md` before scoring the build.

When the user asks for a faster process, read `references/fast-development-mode.md`. Fast mode removes duplicate work, starts the build shell earlier, and uses targeted QA during repair, but it must not skip final build, responsive QA, interaction QA, ledger, benchmark score, or production-readiness validation.

## Core Rule

Treat the exported asset kit as the production source of truth. Do not redesign the brand, regenerate the concept, replace the imagery with stock assets, or fall back to generic sections. Build the website using the supplied assets, manifest, tokens, and reference notes.

If an asset is missing, first check the manifest and notes for alternatives. If the missing asset blocks a faithful build, either generate only that missing asset with image generation or state the gap clearly before proceeding. Do not silently replace it with unrelated placeholder art.

Strict visual clone mode is required. The approved prototype/template screenshots are the visual truth for layout, spacing, typography scale, colors, section order, image placement, and responsive behavior. Build, screenshot, compare, and iterate until the website closely matches the reference.

Do not claim the site is deploy-ready until the production build passes, desktop/iPad/tablet/mobile views are checked, interactions work, visual QA evidence exists, and unresolved blockers are listed.

## Expected Input

Prefer an export folder shaped like:

```text
asset-exports/<project-slug>-YYYYMMDD-HHMM/
  asset-export-manifest.json
  01-logos/
  02-icons/
  03-ui-elements/
  04-backgrounds/
  05-page-assets/
  06-ready-for-builder/
  notes/
```

Also accept:

- `asset-kits/...` folders from `9design-kit`
- A folder of generated prototype screens plus assets
- A manifest file plus referenced asset paths
- Attached asset images when no folder exists

## Five-Step Build Process

### Step 1: Read The Asset Kit

Read these first when present:

- `asset-export-manifest.json`
- `asset-manifest.json`
- `notes/builder-handoff.md`
- `notes/asset-plan.md`
- `notes/font-and-token-notes.md`
- `06-design-tokens/tokens.css`
- `06-design-tokens/tokens.json`
- Files inside `06-ready-for-builder/`

Use exported tokens when available. `tokens.css` should become the source for CSS variables, and `tokens.json` may be used as a machine-readable companion when the stack supports it.

When the 9design-assets validator is available, run it before implementation:

```bash
python <9design-assets-skill-dir>/scripts/validate_asset_manifest.py "<asset-export-folder>" --check-files
```

Warnings from older manifests do not block the build, but missing cleanup fields, missing role/accessibility/icon policy notes, or missing ready files must be recorded as risks before coding.

Inventory every asset path and map it to a website role:

- Logo and favicon
- Header/navigation assets
- Icons
- Hero backgrounds
- Section backgrounds
- Decorative overlays/dividers/textures
- Cards, forms, CTA, footer, and other UI elements
- Page-specific imagery
- Decorative image-text assets that need accessible hidden text
- Social media/community icons, their exact source asset or glyph, container treatment, and hover/active state

Before building, inspect manifest cleanup fields:

- Assets with `alpha_required: true` must have `background_cleaned: true` and `alpha_verified: true`.
- Do not use assets marked `background_removal_needed: true` in `06-ready-for-builder/`.
- If a reusable asset visibly contains a checkerboard, flat page background, or screenshot background, treat it as unclean and return to `9design-assets` cleanup or regenerate that asset.
- Only true background assets may be full-bleed.
- For assets marked `decorative-image-text`, add equivalent accessible hidden text in the website.
- For social icons, use the exact matched assets or official/vector-quality glyphs recorded by the asset exporter. Do not substitute text labels or generic social icons unless the approved design shows them.

### Step 2: Plan The Real Website

Infer the complete website structure from the prototype references and manifest. Unless the user narrows scope, build all pages represented by the asset kit.

Typical pages:

- Home / landing page
- About / story page
- World / gallery page
- Feature / experience page
- Detail page
- Contact / signup page

For smaller kits, build the pages that are actually supported by the provided assets and notes.

Create a concise implementation plan:

- Pages and routes
- Components
- Asset-to-component mapping
- Design tokens to implement
- Reference screenshot/template for each page
- Pixel-critical visual details: section heights, max widths, typography scale, spacing, image aspect ratios, radii, shadows, borders, and color values
- Missing assets or assumptions
- Verification commands

Then implement. Do not stop with only the plan unless the user explicitly asks for planning only.

Before coding, create a compact implementation inventory:

- Exact visible copy, nav items, CTA labels, headings, body text, captions, form labels, and footer text.
- Design tokens: background, surface, text, muted text, border, accent, shadow, radius, spacing scale, and motion timing.
- Typography system: font family or fallback, type scale, weights, line heights, tracking, label treatment, button text, and responsive behavior.
- Icon inventory: meaning, source asset, outline vs filled, stroke width, size, color, alignment, spacing, and states.
- Social icon inventory: platform or community, exact source file or official/vector glyph, container shape, fill/stroke treatment, size, spacing, accessible label, href placeholder, and hover/active state.
- Component families: buttons, navigation, media frames, cards only where present, forms, tags, galleries, CTA, footer, and responsive variants.
- Container model: full-bleed sections, bands, rails, lists, panels, cards, masks, overlays, or open whitespace.
- Hero/media treatment: no overlay, color overlay, gradient, edge fade, mask, transparent cutout, or matching background color.
- Text policy: which text is real HTML/CSS and which, if any, is decorative image text with hidden accessible text.

Do not invent new visible above-the-fold copy, hero eyebrows/kickers, badges, pills, major carousels, pricing blocks, dashboards, forms, or tab systems unless they appear in the approved design, are in the user request, or are required for a concrete function.

Before coding, create a reconstruction contract:

```bash
python <9assets-website-skill-dir>/scripts/create_reconstruction_contract.py --website-root "." --asset-export "<asset-export-folder>" --reference-root "<approved-reference-folder>"
```

Use `docs/research/RECONSTRUCTION_CONTRACT.md` as a pass/fail checklist. It must lock the approved pages, desktop, iPad/tablet, mobile, small-mobile targets, interactions, and final handoff gates.

If speed matters, also create a fast-track plan:

```bash
python <9assets-website-skill-dir>/scripts/create_fast_track_plan.py --website-root "."
```

Use `docs/research/FAST_TRACK_PLAN.md` to keep the critical path moving: scaffold routes, layout, tokens, asset loading, header, footer, and mobile nav early; then implement sections against the locked references.

Create section specs before coding. For every major visible section, write:

```text
docs/research/components/<section-name>.spec.md
```

Each spec must include target component file, source prototype/reference image, exact copy, asset mapping, icon/social icon requirements, visual tokens, interaction model, hover/active/mobile states, and desktop/tablet/mobile behavior. Do not start coding a section until its spec exists.

### Step 3: Build The Website

Use the existing repo stack if one exists. If starting from an empty or unspecified project, use React + TypeScript + Vite.

Create or update:

- `package.json`
- `index.html`
- `src/main.tsx`
- `src/App.tsx`
- `src/components/*`
- `src/pages/*`
- `src/styles/*`
- `public/assets/*`
- `README.md`

Implementation requirements:

- Copy final website assets from the export kit into `public/assets/`; do not reference generated temp folders directly.
- Preserve filenames or use predictable kebab-case aliases.
- Use the exported logo, icons, imagery, backgrounds, UI references, and tokens.
- Recreate the approved visual system: colors, typography mood, spacing, radii, shadows, borders, overlays, masks, textures, and section rhythm.
- Build real responsive UI, not a single screenshot background.
- Clone the approved template closely. Do not reinterpret layouts, move sections, change hierarchy, swap fonts casually, or invent new component shapes.
- Keep text readable on desktop and mobile.
- Avoid generic SaaS layout unless the asset kit clearly has that style.
- Use CSS variables for tokens.
- Use semantic HTML and accessible controls.
- Use accessible alt text for meaningful images and empty alt text for purely decorative images.
- Use visually hidden accessible text for decorative logo/wordmark/hand-lettered image text.
- Normal website text must be real HTML/CSS text: navigation, headings, paragraphs, buttons, cards, CTA, forms, and footer.
- Social links must use the exact matched social icon assets or official/vector-quality glyphs described in the asset kit. Do not use text labels or generic social icons unless the approved design shows them.
- Implement every visible button, link, nav item, social icon, form control, tab, filter, carousel control, and mobile menu as working UI. Unknown destinations may use `#`, but visual states and accessible labels must be complete.
- Do not hardcode the whole page with absolute positioning. Use modern CSS layout with grid, flexbox, `clamp()`, `minmax()`, `object-fit`, and `aspect-ratio`; reserve absolute positioning for accurate visual layering only.
- Include a README with how to install, run, build, and understand the asset source.
- For faster delivery, create the app shell and shared tokens before all sections are complete. Keep the build passing as each page group lands.

Use generated UI element images as visual references, but implement interactive controls as HTML/CSS unless they are intentionally decorative bitmap elements.

Frontend implementation rules:

- Use the existing repo framework and design system when present; otherwise use React + TypeScript + Vite for a new complex site.
- Keep `App` as composition glue. Build small focused components, reusable primitives, page sections, and shared tokens/styles.
- Implement repeated elements through shared components or style primitives; use explicit variants instead of one-off copied CSS.
- Keep buttons, forms, navigation, tabs, links, cards, and labels code-native and accessible.
- Define typography deliberately for controls; do not rely on browser-default button/input text sizing.
- Preserve the container model. Do not add cards, panels, borders, glows, or wrappers where the reference uses open space or full-bleed composition.
- Use SVG/icon components only when they faithfully match the approved icon style; otherwise use the cleaned exported icon assets.
- Respect `prefers-reduced-motion` for motion.
- Use CSS for code-native UI chrome when it can faithfully match the design faster than generated UI images. Reserve image assets for visual-world elements, decorative typography, logos, icons, scene art, textures, overlays, and dividers.

Default reusable component names for a landing-page build:

- `Header`
- `Hero`
- `StorySection`
- `FeatureSection`
- `ShowcaseSection`
- `GallerySection`
- `CTASection`
- `Footer`
- `Button`
- `Card`

Use the names that fit the actual design; do not force unused sections.

Template cloning requirements:

- Match the approved screenshot/template section-by-section.
- Use the same typography proportions, button sizes, image/card aspect ratios, border radii, shadows, backgrounds, and vertical rhythm.
- Build reusable UI as live HTML/CSS, not pasted screenshots, unless the asset is decorative imagery.
- Keep isolated image assets clean over the real page background; never layer a background-baked logo/icon/UI image over another background.

### Step 4: Verify Fidelity And Responsiveness

Run the smallest meaningful verification, then broaden as needed:

- Install dependencies if needed.
- Confirm `npm install`, `npm run dev`, and `npm run build` work for new Vite projects when practical.
- Run `npm run build`.
- Start the dev server.
- Use browser testing or Playwright screenshots for desktop and mobile.
- Compare screenshots against the approved reference/template at the same viewport sizes. Optional pixelmatch or SSIM-style comparison may be used when available; manual visual comparison remains acceptable.
- Check for broken images, console errors, missing assets, text overflow, incoherent overlap, and mobile navigation issues.
- Check for visual drift: wrong spacing, wrong font weight/size, wrong button height, wrong card ratio, wrong background layering, wrong section order, visible asset backgrounds, and mismatched icon/social icon style.
- Fix issues found during verification.
- During repair, prefer targeted screenshots of the changed route, viewport, or section. Run the full desktop/iPad/tablet/mobile pass only after the repair queue is clear or before final handoff.

Optional screenshot capture:

```bash
node <9assets-website-skill-dir>/scripts/capture_visual_qa.mjs --url "http://localhost:5173" --out visual-qa/screenshots
```

Optional pixel diff when reference PNGs are available and dependencies are installed:

```bash
node <9assets-website-skill-dir>/scripts/compare_visual_qa.mjs --reference-dir visual-qa/reference --actual-dir visual-qa/screenshots --out visual-qa/diffs
```

Ledger generation, with or without automated summaries:

```bash
python <9assets-website-skill-dir>/scripts/create_visual_qa_ledger.py --website-root "." --asset-export "<asset-export-folder>" --summary "visual-qa/diffs/visual-qa-diff-summary.json"
```

Benchmark scoring, after human review:

```bash
python <9assets-website-skill-dir>/scripts/score_visual_qa.py --ledger docs/research/VISUAL_QA_LEDGER.md --diff-summary visual-qa/diffs/visual-qa-diff-summary.json --build-passed --out docs/research/VISUAL_BENCHMARK_SCORE.md
```

Screenshot comparison loop:

1. Capture desktop screenshot, preferably at the same aspect ratio as the approved template.
2. Capture mobile screenshot, preferably at the same width as the mobile reference.
3. Compare against the reference visually and note mismatches.
4. Classify each mismatch as layout, spacing, typography, color, asset, icon, interaction, or responsive behavior.
5. Patch the specific CSS, component, token, or asset responsible.
6. Repeat until the remaining differences are minor or blocked by missing assets/fonts.

Visual QA ledger:

- Before final handoff, write `docs/research/VISUAL_QA_LEDGER.md` and record at least eight comparison points covering copy, layout, typography, palette, asset treatment, icon/social icon fidelity, spacing/container model, responsive behavior, interactions, or motion.
- Check desktop around 1440px, tablet around 768px, and mobile around 390px when practical.
- Check iPad/tablet explicitly: around 1024px x 1366px for iPad portrait and around 768px x 1024px for tablet portrait when practical.
- Inspect hover, click, menu, form, social link, tab/filter/carousel, and scroll states that are visible in the design or required by the UI.
- If a reference dimension cannot be matched exactly, state the blocker and verify the nearest practical viewport.
- If automated diff artifacts exist, link the screenshot and diff files in the ledger, but still summarize the human-visible mismatch and repair decision.

Benchmark score:

- Before public handoff or benchmark submission, create `docs/research/VISUAL_BENCHMARK_SCORE.md` using the scoring helper or the same rubric manually.
- Score reference fidelity, asset quality, responsive quality, accessibility, build reliability, and visual QA completeness from `0` to `5`.
- Public benchmark target is every category at least `4.0` with no unresolved blockers.
- Internal working-build target is an overall score of at least `3.5` with blockers recorded and repairable.
- Do not average away serious blockers such as a failed build, unusable mobile layout, inaccessible primary navigation/form, or checkerboard-backed core asset.

Production-readiness validation:

```bash
python <9assets-website-skill-dir>/scripts/validate_production_readiness.py --website-root "." --strict
```

Run this after build, screenshot review, ledger, and benchmark score. Fix reported errors before calling the website complete. Warnings may be handed off only when they are explicitly explained.

If the repo has graphify instructions and code files changed, run `graphify update .`.

### Step 5: Handoff The Working Site

Final response must include:

- Website folder or key files changed
- Pages/routes built
- Asset export folder used
- Important assets copied into `public/assets/`
- Sections recreated
- Assets generated or used
- Main design decisions
- Verification commands and results
- Visual QA ledger path, visual mismatches fixed, and unresolved visual blockers
- Visual benchmark score path or score summary when a final quality gate was run
- Production-readiness validator result
- Local dev URL or run command
- Remaining risks, especially missing fonts or incomplete asset coverage

## Asset Handling Rules

- Prefer `06-ready-for-builder/` assets when present.
- If duplicate assets exist, prefer the manifest-listed file.
- Do not crop whole-page mockups into sections unless the kit explicitly marks them as production assets.
- Do not invent a new logo, new icon style, or new palette.
- Do not leave placeholder gray boxes.
- Do not use unclean transparent assets, checkerboard-backed images, or screenshot-backed logos/icons/UI components.
- Do not use remote image URLs when local assets are available.
- Keep source kit files untouched; copy into the website project instead.

## Font Rules

- Use exact font files only when they are present in the kit or licensing notes allow download.
- If exact fonts are uncertain, implement the documented fallback stack from `font-and-token-notes.md`.
- Do not claim an exact font if the kit only provides a visual approximation.

## Master Prompt

When the user asks for a reusable prompt, use [references/master-prompt.md](references/master-prompt.md).
