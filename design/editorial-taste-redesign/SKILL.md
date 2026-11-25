---
name: editorial-taste-redesign
description: Editorial Taste — redesign or restyle an existing website, app, or page into a monochrome, editorial, photography-led style (Geist + Geist Mono, #151515 / #EDEDED alpha ramps, 5px spacing rhythm, glass blur instead of shadows) while preserving its content, structure, routes, and functionality. Use when the user asks to redesign, restyle, reskin, refresh, modernize, or "make it look editorial / premium / minimal" for a site or codebase that already exists, including Tailwind, React, Next.js, Vue, or plain HTML/CSS. For building a new site from scratch, use editorial-taste-new-site.
---

# Editorial Taste: Redesign

Restyles an existing site in the Editorial Taste style: **monochrome, editorial, photography-led**. A redesign changes the **visual layer**. Content, information architecture, URLs, behavior, forms, SEO metadata, and analytics stay intact unless the user asks otherwise.

## Non-negotiable rules

1. **No accent colors.** Use only the neutral ramp, `--light-*` (#EDEDED alpha), `--dark-*` (#151515 alpha), and semantic tokens. Brand accent colors are removed from the UI; the brand's color lives in its photography. If the user insists on keeping a brand color, confine it to the logo.
2. **Two type voices.** Geist Medium for headings, Geist Regular for body. **Geist Mono only** for buttons, nav, labels, tags, and eyebrows. Never use bold headings. Type roles are fixed: the hero headline (`h1`) is `.h2`, `.h0` belongs only to the statement, section titles are `.h3`, stat values `.h1`.
3. **5px rhythm** for spacing and radii (the compact-scale exceptions are 8, 12, 32, 56, and 96).
4. **Glass, not shadow.** Remove every shadow; use translucent fills plus `backdrop-filter: blur(16px)`, or a `--border-subtle` hairline. The only gradients allowed are black vignettes over photos.
5. **Text on photos always sits on a vignette.**
6. **Radii:** buttons 8 · cards 10 · case cards 20 · chips and pills full. 20 is for case cards only; photos, frames, and panels use 10. Nested radii: `inner = outer − gap`.
7. **Motion is buttery and restrained**: expo-out (`--ease-out`), 200/450/800/1200ms, compositor-only properties, one hero sequence, reveals that play once, and full reduced-motion and no-JS fallbacks (`references/motion.md`).
8. **Preserve before polishing.** Never drop content, links, or accessibility features in exchange for looks.

## Workflow

### 1. Audit what exists (read before you write)
- Identify the stack: plain HTML/CSS, Tailwind (v3 config or v4 `@theme`), CSS Modules, styled-components, or a component library (shadcn, MUI, Chakra).
- List the pages and shared components (layout, nav, footer, buttons, cards, forms).
- Run the token mapper over the source to get a replacement plan:
  `python3 <skill-dir>/scripts/map_tokens.py <src-dir-or-files>`
  It maps every color, font, size, spacing value, radius, shadow, and Tailwind utility to the nearest Editorial Taste token, and flags accents and shadows for removal.
- Run the linter over the source for a baseline count: `python3 <skill-dir>/scripts/lint.py <src-dir>`.
- Note what must not break: forms, auth, routing, JavaScript hooks that depend on class names or IDs, CMS-driven content, and tests or snapshots that assert on markup.
- If the project can run, take "before" screenshots at 1440px and 390px.

### 1b. Diagnose generic patterns
Go through the "Generic patterns" table in `references/pitfalls.md` (gradient blobs, everything centered, three identical icon cards, badge pills above every heading, soft shadows, rounded-2xl everything, filler copy, fake logo walls) and note every one the site uses. Also check:
- **Hierarchy:** is there one clear primary action per screen, or do CTAs compete?
- **Proof:** is proof next to the claims it supports, or buried at the bottom?
- **States:** are focus, pressed, disabled, loading, empty, and error states missing?
- **Ship basics:** OG tags, favicon, 404, legal links, alt text, form validation (`references/ship-checklist.md`).

### 1c. Post the audit before changing code
Post a short audit, then proceed without waiting unless the user asked to review it first:

| Severity | Meaning |
|---|---|
| **Critical** | Breaks use or accessibility: no focus states, contrast failures, broken mobile layout, missing alt text |
| **Style** | Violates Editorial Taste: accents, shadows, wrong fonts, off-scale values, generic patterns |
| **Polish** | Missing states, ship basics, copy filler, layout monotony |

Include the stack, the section-to-block map (step 2), what will be kept as is, and the assets needed (photography, logo SVG).

### 2. Map content to Editorial Taste blocks
Keep the existing content and pick the closest block for each section (see `references/components.md`, and `references/layouts.md` for hero variants and section patterns that suit the content; don't force every redesign into the same layout):

| Existing section | Editorial Taste block |
|---|---|
| Hero / banner | Hero (split or centered): full-bleed photo + vignettes; or, with no photo, a `--bg-base` hero with a large H0/H2 |
| Feature grid with images | Product cards (3) or split cards (2) |
| Feature list without images | Intro (split) + a 3-column grid of news-card surfaces with H4 + body |
| Testimonials / case studies | Case cards |
| Blog / news / resources | Journal (news cards) |
| Stats / metrics | Highlight numbers |
| Logo wall | Monochrome logos (`grayscale(1)`, 64% opacity) in a row with gutter 20 |
| Pricing | News-card surfaces (r10, white), H4 plan name, H1 price, Body Medium list, Primary CTA on the featured plan only. No colored badges; use a mono tag chip |
| FAQ | Hairline-divided list (`--border-subtle`), H6 questions, Body Medium answers, a mono "+" toggle |
| Newsletter / contact CTA | CTA band |
| Mission / about / manifesto paragraph | **Statement**: one H0 line of 2–4 lines with a word-by-word reveal, one per page and never directly under the hero (`references/components.md`) |
| Forms | See Forms in `references/components.md`: 40px inputs, radius 8, mono labels, inline errors, focus ring |
| Repeated "three icon cards" sections | Vary them: a 5/7 split list, feature + list, or split cards (see Layout variety) |

If the site has no photography, say so: the style depends on it. Use the user's existing images with vignettes, or ask for photos. Don't hotlink stock images.

**Photography:** keep the site's own photos. Where a section has no image, a placeholder, or off-style stock (people at laptops, clip-art, heavy filters), pull replacements from Unsplash with `scripts/images.py` (needs `UNSPLASH_ACCESS_KEY`), review `review/contact-sheet.jpg`, use the returned `images.unsplash.com` URLs as is, and link `credits.html` from the footer.

**Illustrations:** replace clip-art, 3D renders, and colorful isometric scenes with **isometric hairline illustrations** generated by `scripts/iso.py` (`references/illustrations.md`). Good targets are "how it works", architecture or platform diagrams, process steps, and feature sections with no honest photo. Keep it to 1–3 per page, each in an Illustration split section.

### 3. Install the foundation (global first)
1. Add the fonts and `references/tokens.css` (or map them in the framework theme; see `references/frameworks.md`).
2. Replace global styles: body background, text color, font families, and base heading and link styles.
3. Retheme shared primitives at the source: the Button component, Card, Input, and theme config (Tailwind or a component library). One change at the source is better than 100 per-instance overrides.
4. Delete the old palette, shadow, and font tokens once nothing references them. Don't leave two systems side by side.

### 4. Restyle section by section
Order: Nav → Footer → Hero → each section top to bottom → remaining pages. For each one:
- Apply the mapped block anatomy (sizes, gaps, text styles).
- Swap colors, fonts, spacing, radii, and shadows using the mapper report.
- Keep the DOM, IDs, `data-*` attributes, ARIA, and event handlers. Change class names only where the styling system requires it, and keep any class that JavaScript or tests query.
- Tighten copy only if the user asked. Otherwise, keep the wording and change only casing (sentence case for headings, uppercase for mono eyebrows). If they did ask, follow `references/copy.md` and never invent facts.
- Add the missing states (hover, pressed, focus, disabled, current, loading, empty, error) as you go, using the specs in `references/components.md`.
- Use the motion tokens (`--ease-out`, 200/450/800/1200ms) for every transition. Remove `transition: all` and default easing.

### 4b. Motion pass
Do this after the visual pass, following `references/motion.md`:
1. **Inventory existing motion**: animation libraries (Framer Motion, GSAP, AOS, Lottie), scroll listeners, CSS keyframes, autoplaying carousels.
2. **Remove what fights the style**: bounces and springs, side slide-ins, fade-in on every element, scroll-jacking, custom cursors, autoplay carousels, animated shadows or blur.
3. **Install the motion system for the stack**: plain HTML gets the template's `motion.js` plus Lenis; React and Next.js get `ReactLenis` and Framer Motion variants with `[0.16, 1, 0.3, 1]`; a GSAP project keeps GSAP with `expo.out` and Lenis synced to `ScrollTrigger`. Don't run two animation systems for the same effect.
4. **Choreograph**: one hero intro sequence, `.reveal` with stagger on content blocks, masked word reveals on section titles, image unmasks on standalone images, count-up on numeric stats.
5. **Fallbacks**: the `html.js` gate, reduced motion, and focus handling on anchor scrolls.
- Work section by section and keep each diff reviewable. Never rewrite the whole site in one pass.

### 5. Verify
1. Run the linter on the changed style and markup files and fix every ERROR:
   `python3 <skill-dir>/scripts/lint.py <files…>`
2. Re-run `map_tokens.py`. The Colors table should contain no `ACCENT` rows and the Shadows section should be empty.
3. Run the project's existing build, type-check, and tests. Nothing that passed before should fail.
4. Run the app and compare against the "before" screenshots at 1440px and 390px. Check that all content is still present, links and forms work, nothing scrolls horizontally, focus rings are visible, and contrast meets AA.
5. Work through `references/ship-checklist.md`, and add any missing basics that don't change content (OG tags, favicon, 404, skip link).

### 6. Report
- **Before and after:** lint error count and `map_tokens.py` accent and shadow counts, then and now.
- **Audit items:** each one marked fixed, kept deliberately (with the reason), or needing user input.
- **What changed:** foundation, primitives, and sections.
- **Not mapped cleanly:** e.g. charts that need a monochrome palette, or third-party embeds.
- **What the user should supply:** photography, logo SVG, real proof that replaces placeholders.

## Quick token reference (web desktop)

| Need | Token |
|---|---|
| Page background | `--bg-base` #EDEDED |
| Hover fill / raised surface | `--bg-lift` #D9D9D9 |
| Primary text, primary button | `--tone-strong` #151515 |
| Secondary text | `--text-muted` #737373 / `--tone-medium` |
| Hairlines, chip fill, disabled | `--border-subtle` / `--tone-faint` |
| Glass on a photo | `--light-16` + `--blur-glass` |
| Container / margin / gutter | 1280 / 40 / 20 (mobile: fluid / 20 / 12) |
| Section padding / title→content | 96 / 32 (mobile 64 / 24) |

| Role | Style |
|---|---|
| Hero headline | H2 40/44/−1.5 |
| Section title | H3 32/36/−1 |
| Card title | H4 24/28/−0.75 |
| Stat value | H1 48/48/−1.5 |
| Paragraph | Body Medium 15/22 |
| Eyebrow / tag / button | Geist Mono 11–13px |

## Accessibility (always include)
`:focus-visible` ring (2px `--tone-strong`, offset 2; `--light-100` on photos) · disabled state (`--tone-faint`) · pressed state · `prefers-reduced-motion` · AA contrast (use `--neutral-600` instead of `--neutral-500` on gray surfaces if needed). Never remove existing accessibility features during a redesign.

## Reference files
- `references/foundations.md`: color, type, spacing, radius, grid, effects, motion, icons, contrast
- `references/components.md`: anatomy of every component and block, forms, states, layout variety
- `references/layouts.md`: hero variants, section patterns by job, variation rules, recipes
- `references/pitfalls.md`: common mistakes plus the generic-pattern diagnosis table
- `references/copy.md`: voice, CTAs, content realism, banned words (for copy passes)
- `references/ship-checklist.md`: final QA, SEO, and ship requirements
- `references/tokens.css`: the drop-in token set
- `references/frameworks.md`: Next.js, Tailwind v3/v4, and shadcn/MUI theme mapping
- `references/figma.md`: redesigning a Figma file instead of code
- `references/motion.md`: motion principles, tokens, recipes, framework setup (Astro, React, GSAP, Tailwind)
- `references/illustrations.md`: isometric hairline illustration rules and compositions
- `scripts/iso.py`: isometric illustration generator
- `scripts/images.py`: pulls photos from Unsplash per image slot, writes URLs and credits
- `scripts/map_tokens.py`: inventories existing styles and maps them to tokens
- `scripts/lint.py`: rule checker
