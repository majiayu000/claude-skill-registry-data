---
name: site-phase-6
description: "Phase 6 of build-site — Implement blueprint: navbar, sections, footer, App, main"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
model: opus
effort: high
context: fork
user-invocable: false
---

# Phase 6 — Implement the Blueprint

## Required Reading (in this exact order, before doing anything)

```
Read: sites/$LEAD_ID/mapa-encantamento.md
Read: sites/$LEAD_ID/concept.md
Read: sites/$LEAD_ID/sales-strategy.md
Read: sites/$LEAD_ID/public/images/MANIFEST.json
```

The MANIFEST.json is the SEMANTIC contract for image-to-section assignment. It contains, for each image and video, what the asset actually shows (per Claude's vision analysis in Phase 4) and which sections it is recommended for. **You MUST use this manifest to choose images for sections — never assign by filename heuristic.**

If `sites/$LEAD_ID/palette-animations.json` exists (deep-3b builds), also:
```
Read: sites/$LEAD_ID/palette-animations.json
```

## Objective

Transform the blueprint (mapa-encantamento.md) into a fully functional React site. Every section, animation, layout, and visual technique specified in the blueprint MUST be implemented exactly as written. The blueprint is a CONTRACT, not a suggestion.

## Pre-Gate — Verify Images

```bash
.claude/scripts/gate-images.sh $LEAD_ID
```

## Step 1 — Load Blueprint

Read and memorize from `sites/$LEAD_ID/mapa-encantamento.md`:
1. **Layout Map** — which layout PER SECTION
2. **Animations** PER SECTION (entry animation + scroll animation)
3. **Visual techniques** PER SECTION (grain, blend mode, mask, etc.)
4. **Signature element** — what it is and where it appears
5. **Navbar** — which pattern was chosen
6. **Aesthetic direction** committed in the concept
7. **Semantic color tokens** and their names
8. **Animation Budget** — showstopper, supporting, baseline assignments

**ABSOLUTE RULE: Implement EXACTLY what the blueprint specifies.**
If the blueprint says "bento grid 2fr 1fr 1fr" the code MUST have `grid-template-columns: 2fr 1fr 1fr`.
If the blueprint says "clip-path reveal circular" the code MUST have a `clip-path` animation.
Do NOT substitute with "easier" alternatives.

## Step 2 — Real Images Rule + MANIFEST.json semantic mapping

If the briefing has images, the site MUST use them:
- Hero or About MUST feature the client's professional photo
- `<img>` with `src="/images/name.jpg"`, descriptive `alt`, `loading="lazy"` (hero: `fetchpriority="high"`)
- FORBIDDEN to replace real photos with giant letters, empty gradients, or generic icons
- Stock images ONLY for: textures, patterns, abstract backgrounds. NEVER for people/facades/products.

### Step 2.5 — MANIFEST-driven image selection (MANDATORY, blocking)

Read `sites/$LEAD_ID/public/images/MANIFEST.json`. For each section in the Section Purpose Map:

1. **Filter manifest entries** where `recommended_sections` includes the current section slug (`s1`, `s2`, `s3`, `s4`, `s5`)
2. **Among matches, pick by quality**: prefer entries with the highest `quality_assessment` and the most relevant `subjects[]`
3. **Reject mismatches**: if a candidate entry has `do_not_use_for` containing this section's role, skip it
4. **Use the `fingerprint_summary`** to write the section's `<img alt="...">` text — alt must describe what the image actually shows, derived from the manifest's vision analysis (NOT from the section's title)
5. **Track assignments**: every image used in JSX must come from MANIFEST.json. Every entry in MANIFEST.json marked `recommended_sections: [...]` must be referenced in JSX (no orphans)

### Video usage

For manifest entries with `kind: "video"`:
- If `is_safe_for_autoplay_loop: true` and `recommended_sections` includes a section slug ending in `_background` (e.g., `s1_background`, `s3_demo`), use the MP4 as `<video autoplay muted loop playsinline src="/videos/{file}">`
- Otherwise, use the `poster_file` as a static image only
- Caption excerpt from the manifest can be used as adjacent supporting text — verify it's not duplicating content already in the section copy

### Logo usage

Look for the entry where `is_logo_or_brand_mark: true` OR `content_type: "logo"`. If present, use the actual file in:
- The Guild Seal / signature element (replace any hand-coded SVG fallback)
- The footer brand mark
- The favicon (covered in Phase 4)

If MANIFEST.json declares `logo_real_present: false`, fall back to a hand-coded SVG signature element — but FIRST verify there really is no logo in the manifest. Most clients have one and it gets missed because of filename guessing.

### Forbidden patterns

- ❌ Assigning an image to a section without consulting MANIFEST.json
- ❌ Picking an image because the filename "looks right" (e.g., `portrait-bruno.jpg` could actually show the shop interior)
- ❌ Leaving images orphaned in `public/images/` that have a `recommended_sections` entry — every recommended image must be used somewhere
- ❌ Ignoring videos when `is_safe_for_autoplay_loop: true` and the blueprint allows motion in that section

## Step 3 — Code Principles

```
Read: sites/_templates/code-principles.md
```

Follow all SOLID, Tailwind v4, and animation rules defined in the reference file.

## Step 4 — Build Order

Execute in this exact order: signature element -> navbar -> sections -> footer -> App -> main.

### 4.1 Signature Element (BEFORE sections)

Create as specified in the blueprint. Separate component in `src/components/ui/`.
- If blueprint says animated SVG -> SVG inline with CSS `@keyframes` or Motion
- If blueprint says interactive background -> Canvas or CSS
- If blueprint says custom cursor -> CSS cursor with SVG data URI

**The element MUST be imported in 1+ sections or App.jsx.**

### 4.2 Navbar (MUST differ from last site)

Check what NOT to repeat:
```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2
LAST=$(ls -td sites/*/src/components/layout/Navbar.jsx 2>/dev/null | grep -v "$LEAD_ID" | head -1)
[ -f "$LAST" ] && echo "=== LAST NAVBAR ===" && head -20 "$LAST" && echo "=== DO NOT REPEAT THIS PATTERN ==="
```

For available patterns and functional requirements:
```
Read: sites/_templates/navbar-patterns.md
```

### 4.3 Sections — Implement the Blueprint

For EACH section in the blueprint:
1. **Read LAYOUT** from blueprint -> implement THIS layout (not another)
2. **Use the animation component** created in Phase 5 for ENTRY ANIMATION
3. **Implement SCROLL ANIMATION** if specified
4. **Apply VISUAL TECHNIQUE** described (grain, blend mode, mask shape, etc.)
5. **Follow ANIMATION BUDGET**: showstopper on the designated section, supporting where indicated, baseline elsewhere

For EACH section:
- ALL text via `t('section.key')` — ZERO hardcoded strings
- Images from `/images/` with descriptive alt
- IMAGE-SECTION COHERENCE: image content must match section topic
- MOBILE-FIRST: write for 375px FIRST, then `md:` and `lg:`

**MCP component references (consult BEFORE building from scratch):**
- `mcp__magic-ui` — blur-fade, aurora-text, number-ticker, shimmer-button
- `mcp__aceternity-ui` — parallax-scroll, spotlight, hero-highlight, 3D-card
- `mcp__shadcn-ui` — button, card, tabs, accordion, dialog
- `mcp__gsap` — ScrollTrigger patterns in React

### 4.4 Floating CTA

If the blueprint defined a floating CTA, implement as specified. If not defined, do NOT create one by default.

### 4.5 Footer

Create `src/components/layout/Footer.jsx`:
- Style derived from the design system (no fixed recipe)
- Real data from the briefing
- All text via `t()`

### 4.6 App.jsx + main.jsx

**App.jsx:** Assemble all sections per blueprint order, with Lenis (parameters from blueprint), HelmetProvider, SEO components.

**main.jsx:** Import i18n BEFORE App, `@fontsource` fonts, `index.css`.

Generate `sitemap.xml` and `robots.txt` in `public/`.

## Verification — Build Check

```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2/sites/$LEAD_ID && npm run build 2>&1
```

If ANY error, fix until build passes.

## Exit Gate — Blueprint Fidelity (blocking)

**NEW:** The blueprint is a CONTRACT. This gate validates that the code actually implements what the blueprint specified — not a close-enough version.

```bash
.claude/scripts/gate-blueprint-fidelity.sh $LEAD_ID
```

If FAIL: the gate reports exactly which blueprint claims the code does not honor. Either:
- Fix the code to match the blueprint (preferred — the blueprint was the agreement)
- OR update the blueprint to reflect what was actually built (requires returning to Phase 3b)

Do NOT just delete the blueprint claim to pass the gate. That defeats the purpose.

## Exit Gate — Signature Element (blocking)

```bash
.claude/scripts/gate-signature-element.sh $LEAD_ID
```

## Exit Gate — Anti-Similarity (blocking)

```bash
.claude/scripts/gate-anti-similarity.sh $LEAD_ID
```

## Exit Gate — Image Coherence (blocking)

```bash
.claude/scripts/gate-image-coherence.sh $LEAD_ID
```

This gate validates that:
- Every image used in a section JSX file has a matching entry in MANIFEST.json with `recommended_sections` including that section
- No image in MANIFEST.json with `recommended_sections` is left orphaned (unused)
- No image is used in a section listed under its `do_not_use_for` field
- Logo (if present in manifest with `is_logo_or_brand_mark: true`) is referenced in the signature component or footer

## Constraints

| Constraint | Enforced by |
|---|---|
| Blueprint implemented EXACTLY as written (section count, animation techniques, signature element) | `gate-blueprint-fidelity.sh` |
| Real images used (no stock for people/products) | `gate-images.sh` |
| Signature element exists and is non-trivial | `gate-signature-element.sh` |
| 3+ layout types across sections | `gate-anti-similarity.sh` |
| 3+ animation types across sections | `gate-anti-similarity.sh` |
| No banned template timings | `gate-anti-similarity.sh` |
| Hero layout differs from last site | `gate-anti-similarity.sh` |
| Fonts differ from last 3 sites | `gate-anti-similarity.sh` |
| Navbar pattern differs from last site | Anti-repetition check in step 4.2 |
| All text via `t()`, zero hardcoded strings | Phase 7 validation |
| `npm run build` passes with zero errors | Build check |

## Exit Criteria

- [ ] `npm run build` passes without errors
- [ ] Blueprint implemented faithfully (each section as specified)
- [ ] Navbar uses a DIFFERENT style from the last site
- [ ] Signature element is REAL and non-trivial (gate passed)
- [ ] Anti-similarity gate PASS (diverse layouts, diverse animations, no banned timings, unique hero, original fonts)
- [ ] All text via `t()` — zero hardcoded strings
- [ ] Real client images used prominently (hero/about)
- [ ] Mobile-first responsive design (375px base)
