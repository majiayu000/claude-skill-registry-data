---
name: visual-themes
description: "32 curated visual theme packs plus a deep knowledge base on color science, typography, motion, global design culture, and generative aesthetics. Use when building any themed visual artifact (simulations, games, algorithmic art, data visualizations, dashboards, apps) or when making design decisions that benefit from research-backed guidance on color, type, tokens, motion, or cultural inclusivity. Triggers on: themed artifacts, visual design questions, palette construction, typography selection, animation philosophy, design tokens, data visualization styling, cultural design considerations, or any request mentioning a specific theme name."
---

# Visual Themes

> 32 production-grade visual themes + a research-backed knowledge base on color science, typography, motion, texture, global design culture, and generative aesthetics. Each theme is a complete design system: palette, typography, texture, animation philosophy, UI components, and implementation guidance.

## Routing

Each theme lives in its own file under `references/themes/`. Knowledge base articles live under `references/knowledge-base/`. Read only the files needed for the current task — never load everything.

### Theme Files

| Resource | Path |
|---|---|
| Theme files | `references/themes/NN-theme-name.md` |
| Animation patterns | `references/animation-patterns.md` |

### Knowledge Base

Load these when making design decisions or answering design questions — not for every themed artifact.

| Topic | Path | When to load |
|---|---|---|
| Color science & perception | `references/knowledge-base/01-color-science.md` | Palette construction, contrast decisions, wide-gamut, OKLCH |
| Typography & tokens | `references/knowledge-base/02-typography-tokens.md` | Font selection, type scale, design token architecture |
| Motion, texture & materiality | `references/knowledge-base/03-motion-texture.md` | Animation philosophy, easing, texture techniques, glass/noise |
| Global aesthetics & culture | `references/knowledge-base/04-global-aesthetics.md` | Non-Western design, cultural sensitivity, trend context |
| Generative & data viz | `references/knowledge-base/05-generative-dataviz.md` | Generative art principles, data color, chart theming |
| Quick-reference checklists | `references/knowledge-base/06-checklists.md` | Pre-flight checks for palette, type, tokens, motion, a11y |
| Bibliography | `references/knowledge-base/07-bibliography.md` | Source URLs, further reading |
| Theme generation schema | `references/knowledge-base/theme-schema.md` | JSON schema for AI-assisted theme creation |

### Cross-Skill References

| Resource | Location |
|---|---|
| Font pairings | design-maestro `references/themes.md` |
| Advanced CSS/WebGL effects | design-maestro `references/advanced-effects.md` |
| Anti-slop checklist | design-maestro `references/aesthetic-principles.md` |
| Motion library | design-maestro `references/motion-library.md` |

## Feedback Loop

**FEEDBACK.md lives at the skill root.** Read it at the start of every task that uses this skill.

**Cycle:**

1. **Detect** — After delivering a themed artifact, watch for user corrections, preferences, or complaints about any theme element (colors, animations, styling, component look, performance).
2. **Search** — Check `FEEDBACK.md` for prior entries on the same theme or issue category.
3. **Scope** — Determine if the feedback is theme-specific (e.g., "Kintsugi Ledger gold is too bright") or cross-cutting (e.g., "animations are too slow on all themes").
4. **Draft & Ask** — Draft a FEEDBACK.md entry with category tag and theme tag. Confirm with the user before writing.
5. **Write on Approval** — Append the entry to FEEDBACK.md using the tagged format.
6. **Compact at 75** — When entries reach 75, consolidate: merge duplicates, promote recurring feedback into the relevant theme file as a permanent rule, and reset the log.

## Theme Catalog

Read the descriptions below to select the right theme. Load 1–3 theme files as needed.

---

### Pack 1: Original Collection (Themes 1–15)

---

#### 1. Alchemist's Journal
**File:** `references/themes/01-alchemists-journal.md`
**Best for:** Reaction-diffusion, Physarum (slime mold), organic growth, L-systems, erosion
**Vibe:** Da Vinci notebook — living ink bleeding into ancient parchment.
**Palette feel:** Warm cream canvas, deep charcoal ink, antique gold accents, oxidized copper trails
**Animation style:** Slow, viscous, ink-like. Things flow and bleed, never snap.
**Typography:** Serif-heavy (EB Garamond, Libre Caslon). Alchemical manuscript energy.
**Key techniques:** SVG feTurbulence paper grain, multiply blend for overlapping ink, stroke-dashoffset quill animations

---

#### 2. Ethereal Porcelain
**File:** `references/themes/02-ethereal-porcelain.md`
**Best for:** Fluid dynamics (smoke/fire), Mandelbulb fractals, ray marching, volumetric rendering
**Vibe:** Museum gallery — chaotic forces sculpted into slow-moving porcelain. Kintsugi gold repairs the cracks.
**Palette feel:** Neutral slate gallery wall, porcelain white sculpture, gold in chaos regions, cool grey shadows
**Animation style:** Slow, heavy, majestic. 0.5x physics. Marble-pour entries, breathing gold glow.
**Typography:** High-contrast editorial (DM Serif Display + Work Sans light). Gallery-label precision.
**Key techniques:** Subsurface scattering look, kintsugi gold on high-vorticity, simulated studio lighting

---

#### 3. Anthropic Serenity
**File:** `references/themes/03-anthropic-serenity.md`
**Best for:** Strange attractors, particle systems, flow fields, generative patterns, mathematical viz
**Vibe:** High-end editorial warmth — intellectual calm, matte watercolor, thoughtful negative space.
**Palette feel:** Warm beige canvas, burnt sienna → soft coral gradient, muted forest for density
**Animation style:** Gentle springs, editorial stagger, watercolor bleed. Deliberate and slow.
**Typography:** Modern professional (Plus Jakarta Sans + DM Sans + Geist Mono). Clean, warm.
**Key techniques:** Matte particles with alpha blending, density-based color mapping, 0.5x speed

---

#### 4. Opalescent Daydream
**File:** `references/themes/04-opalescent-daydream.md`
**Best for:** N-body gravity, orbital mechanics, wave interference, electromagnetic fields
**Vibe:** Holographic foil — prismatic, airy, soap-bubble iridescence on clean white canvas.
**Palette feel:** Ghost white/lavender background, holographic cyan→magenta→yellow shifting by velocity
**Animation style:** Elastic springs (bubble-like overshoot), prismatic scatter, bokeh pulse. Weightless.
**Typography:** Futuristic (Sora + Manrope + Space Mono). Light, geometric.
**Key techniques:** HSL gradient by velocity, chromatic aberration, soft bokeh, additive blending (screen)

---

#### 5. Gouache & Clay
**File:** `references/themes/05-gouache-and-clay.md`
**Best for:** Voronoi, Delaunay, terrain generation, map visualizations, geometric patterns
**Vibe:** Cut-paper editorial illustration — matte acrylic, zero digital gloss, hand-cut imperfection.
**Palette feel:** Strong matte backgrounds (terracotta or sage), eggshell white, deep blue-black, vibrant ochre
**Animation style:** Snappy overshoot (paper snapping into place), stamp-press, hard-shadow lifts.
**Typography:** Quirky editorial (Bricolage Grotesque + Figtree + Fira Code). Woodblock energy.
**Key techniques:** Hard directional drop shadows, rough SVG edges, flat fills, stacked-paper 2.5D

---

#### 6. Liquid Glass
**File:** `references/themes/06-liquid-glass.md`
**Best for:** Modern UI artifacts, settings panels, interactive tools, app mockups, control dashboards
**Vibe:** iOS 26 / Apple design language — frosted translucency, layered depth, refraction.
**Palette feel:** Ultra-light grey base, frosted white glass panels, system blue accents
**Animation style:** Apple springs, glass-slide entries, blur-focus modals, parallax depth.
**Typography:** System-clean (SF Pro fallback to Plus Jakarta Sans + DM Sans + Geist Mono).
**Key techniques:** `backdrop-filter: blur(20px) saturate(1.8)`, layered translucency, refraction edges

---

#### 7. Midnight Observatory
**File:** `references/themes/07-midnight-observatory.md`
**Best for:** Data visualizations, star maps, scientific dashboards, time-series, network graphs
**Vibe:** Deep space cartography — celestial precision, warm gold constellations on infinite navy.
**Palette feel:** Deep navy void, warm gold data points, muted teal connections, dusty rose accents
**Animation style:** Gravitational ease-out, orbital arcs, star-appear glow bloom, constellation lines.
**Typography:** Dashboard precision (Instrument Sans + Albert Sans + JetBrains Mono).
**Key techniques:** Star-field backgrounds, golden-ratio layout, constellation-style data connections

---

#### 8. Brutalist Concrete
**File:** `references/themes/08-brutalist-concrete.md`
**Best for:** Data-heavy dashboards, developer tools, technical simulations, CLI viz, system monitors
**Vibe:** Tadao Ando meets Swiss typography — raw, exposed, honest. Zero decoration.
**Palette feel:** Raw concrete greys, near-black text, ONE structural red accent. 95% monochrome.
**Animation style:** Mechanical and instant. Hard cuts, typewriter reveals, scan-line sweeps. Linear easing.
**Typography:** Monochrome type (Space Grotesk + JetBrains Mono). Maximum two faces.
**Key techniques:** Exposed grid, zero border-radius, 2px structural borders, concrete feTurbulence

---

#### 9. Bioluminescent Deep
**File:** `references/themes/09-bioluminescent-deep.md`
**Best for:** Particle systems, network viz, flow simulations, audio visualizers, neural networks
**Vibe:** Abyssal ocean — pure darkness punctuated by living, breathing light.
**Palette feel:** Near-black abyss, electric cyan primary, magenta pulse, deep violet, plankton green
**Animation style:** Slow organic springs, bioluminescent pulse, signal trace, depth-emerge fades.
**Typography:** Deep-tech (Sora + Manrope + Fira Code). Clean on dark.
**Key techniques:** Layered glow rendering, additive blending ('lighter'), vignette, filament connections

---

#### 10. Vapor Silk
**File:** `references/themes/10-vapor-silk.md`
**Best for:** Music visualizers, relaxation apps, ambient simulations, creative tools, meditation
**Vibe:** Silk scarves in slow motion — dreamlike pastels, flowing mesh gradients, zero hard edges.
**Palette feel:** Warm cream base, soft lavender, blush pink, pale mint, dusty mauve. All pastel.
**Animation style:** Ultra-smooth and long (800ms–1.5s). Silk wave backgrounds, mist-fade reveals.
**Typography:** Warm approachable (Outfit + Figtree + Space Mono). Friendly, rounded.
**Key techniques:** Animated mesh gradient (20–30s cycle), generous radius, semi-transparent layering

---

#### 11. Solarpunk Brass
**File:** `references/themes/11-solarpunk-brass.md`
**Best for:** Sustainability dashboards, growth simulations, ecosystem models, botanical art
**Vibe:** Organic technology — botanical circuits fused with polished brass instruments.
**Palette feel:** Warm sunlit linen, forest green growth, polished brass, warm wood, spring patina
**Animation style:** Dual motion — organic grows/unfurls, mechanical rotates/clicks. Two languages.
**Typography:** Organic elegance (Fraunces "wonky" + DM Sans + IBM Plex Mono).
**Key techniques:** Organic + geometric hybrid, brass metallic UI, vine-growth SVG, leaf-vein backgrounds

---

#### 12. Neon Noir
**File:** `references/themes/12-neon-noir.md`
**Best for:** Real-time data, monitoring dashboards, game UIs, night-mode, security viz
**Vibe:** Restrained cyberpunk — Blade Runner 2049 color discipline. 90% mono, 10% electric neon.
**Palette feel:** Charcoal black, smoke panels, hot pink primary neon, electric blue secondary
**Animation style:** Fast and precise. Neon flicker on entry, glitch on error, pulse beacon for alerts.
**Typography:** Techy geometric (Space Grotesk + DM Sans + Fira Code with ligatures).
**Key techniques:** Selective color (neon ONLY on active), scan-line texture, glow only on hover/active

---

#### 13. Paper Cut
**File:** `references/themes/13-paper-cut.md`
**Best for:** Infographics, educational simulations, storytelling, terrain/map viz, explainers
**Vibe:** Physical craft digitized — construction paper layers, parallax shadows, pop-up book depth.
**Palette feel:** Kraft paper base, deep indigo + coral red + sage green layers, cream, mustard
**Animation style:** Physical and tactile. Layer-slide parallax, paper-fold transitions, stamp-press.
**Typography:** Crafty editorial (Bricolage Grotesque + Work Sans + Fira Code).
**Key techniques:** Multi-layer parallax with colored hard shadows, cut-edge SVG paths, 3D fold/unfold

---

#### 14. Crystalline Matrix
**File:** `references/themes/14-crystalline-matrix.md`
**Best for:** Fractal explorers, geometric simulations, Voronoi/Delaunay, molecular viz
**Vibe:** Diamond facets — prismatic light splitting through geometric precision. Math made visible.
**Palette feel:** Cool crystal white, prismatic rainbow at facet edges, platinum structure, graphite depth
**Animation style:** Geometric and symmetric. Facet rotation (slow), light-catch sparkle, crystal growth.
**Typography:** Precision minimalism (Instrument Sans + Albert Sans + Geist Mono).
**Key techniques:** Faceted low-poly rendering, prismatic conic-gradient, wireframe overlay, shard-scatter

---

#### 15. Warm Darkroom
**File:** `references/themes/15-warm-darkroom.md`
**Best for:** Photo galleries, documentary viz, timeline/history artifacts, atmospheric sims
**Vibe:** Analog photography — chemical developing, film grain, sepia warmth, intimate darkness.
**Palette feel:** Warm black, subdued safe-light red, sepia primary, paper white text, chemical blue
**Animation style:** Chemical reveal — elements develop from darkness (opacity layers, 2–3s). Film grain breathes.
**Typography:** Photographic editorial (DM Serif Display + Spectral + IBM Plex Mono).
**Key techniques:** Constant film grain overlay, vignette gradient, photo-develop reveal, dodge-and-burn hover

---

### Pack 2: Research-Informed Collection (Themes 16–30)

---

#### 16. Ionized Parchment
**File:** `references/themes/16-ionized-parchment.md`
**Best for:** Research tools, reading-heavy dashboards, knowledge bases, documentation, writing apps
**Vibe:** High-end longform publication that doubles as an app — editorial clarity on warm "paper."
**Palette feel:** Warm ivory canvas, deep navy ink, oxidized copper accents, slate blue links
**Animation style:** Invisible. Fades and slides for navigation continuity, nothing theatrical.
**Typography:** Text-first serif (Newsreader + Source Serif 4 + JetBrains Mono). Bookish authority.
**Key techniques:** Subtle paper grain, letterpress text-shadow, hierarchy through weight/spacing only

---

#### 17. Ceramic Glaze UI
**File:** `references/themes/17-ceramic-glaze-ui.md`
**Best for:** Wellness apps, creative tools, simulation UIs, calm productivity, habit trackers
**Vibe:** Soft ceramic surfaces with a controlled glaze highlight — calm but tactile.
**Palette feel:** Bisque clay canvas, cobalt glaze accent, celadon secondary, warm taupe neutrals
**Animation style:** Viscous spring with slight overshoot. Tactile, weighted. Elements settle.
**Typography:** Rounded humanist (DM Sans + Figtree + Geist Mono). Smooth, friendly.
**Key techniques:** Matte fills, optional reaction-diffusion shader for empty states, rounded everything

---

#### 18. Voltage Monochrome
**File:** `references/themes/18-voltage-monochrome.md`
**Best for:** Developer tools, ops dashboards, dense tables, IDE-like interfaces, terminal UIs
**Vibe:** High-structure monochrome with one "voltage" accent as a spotlight. Hierarchy and focus.
**Palette feel:** Near white/near black, tight grey ladder, single electric cyan accent used sparingly
**Animation style:** Snappy micro-interactions, no ambient motion. Mechanical precision.
**Typography:** Single family (Inter) + mono (JetBrains Mono). Zero pairing friction.
**Key techniques:** One-accent-only rule, visible grid, zero decoration, density-first spacing

---

#### 19. Sunlit Concrete
**File:** `references/themes/19-sunlit-concrete.md`
**Best for:** Industrial dashboards, IoT monitoring, logistics, manufacturing UIs, fleet ops
**Vibe:** Industrial daylight — concrete, steel, safety labels. Physical control room made modern.
**Palette feel:** Daylight concrete grey, OSHA orange warnings, steel blue links, large metric readouts
**Animation style:** Mechanical easing, sharp starts/stops. Like pneumatic actuators.
**Typography:** Condensed industrial (Barlow Condensed + Barlow + IBM Plex Mono). Big numbers.
**Key techniques:** Concrete noise texture, hard directional shadows, safety color semantics, large KPIs

---

#### 20. Kintsugi Ledger
**File:** `references/themes/20-kintsugi-ledger.md`
**Best for:** Meditation apps, journaling, narrative games, boutique commerce, personal dashboards
**Vibe:** Japanese ledger paper meets gold-repaired seams — calm surfaces, deliberate "repair lines."
**Palette feel:** Washi paper neutrals, sumi ink text, urushi gold accents (very limited), indigo links
**Animation style:** Ink spreading, contemplative fades. Opacity changes over position changes.
**Typography:** CJK-friendly (Shippori Mincho + Noto Sans JP + IBM Plex Mono). Calligraphic display.
**Key techniques:** Paper fiber texture, gold crack-line dividers, ledger grid lines, extreme negative space

---

#### 21. Mashrabiya Matrix
**File:** `references/themes/21-mashrabiya-matrix.md`
**Best for:** Cultural institutions, educational simulations, data storytelling, museum interactives
**Vibe:** Islamic geometric lattice as systematic grid language — patterns inform layout.
**Palette feel:** Sand ivory, deep indigo text, turquoise tile interactive, lapis gold highlights
**Animation style:** Symmetric and unfolding. Elements expand from center, open like a lattice.
**Typography:** RTL-ready (Playfair Display + IBM Plex Sans Arabic + IBM Plex Mono).
**Key techniques:** SVG tiling patterns, bilateral symmetry layouts, RTL-first, ornament-as-structure

---

#### 22. Monsoon Bazaar Modern
**File:** `references/themes/22-monsoon-bazaar-modern.md`
**Best for:** Music/event apps, playful consumer products, creative coding, festival UIs, food delivery
**Vibe:** South Asian poster energy made systematic — saturated inks, bold labels, halftone textures.
**Palette feel:** Raw cotton base, hot magenta/deep indigo/saffron in defined zones
**Animation style:** Kinetic typography, stamp-press entries, registration jitter. "Controlled loud."
**Typography:** Bold editorial (Bricolage Grotesque + DM Sans + Fira Code). Poster energy.
**Key techniques:** Halftone grain overlay, ink edge roughness, registration offset shadows, saturated zones

---

#### 23. Future Medieval Interface
**File:** `references/themes/23-future-medieval-interface.md`
**Best for:** Games, narrative experiences, interactive fiction, RPG character sheets, art pieces
**Vibe:** Arcane-modern — illuminated manuscript logic with modern UI constraints.
**Palette feel:** Dark vellum base, bone white text, gilded gold accents, oxblood highlights, verdigris links
**Animation style:** Ceremonial and slow. Elements are unveiled, not thrown. Ritual pace.
**Typography:** Blackletter display (Cinzel Decorative, sparingly) + readable body (Crimson Pro + Fira Code).
**Key techniques:** Vellum grain, illuminated gold borders, ink-bleed text-shadow, ornament as punctuation

---

#### 24. Chromed Bloom (Y3K Soft Metal)
**File:** `references/themes/24-chromed-bloom.md`
**Best for:** Consumer tech, product marketing, interactive demos, portfolio showcases, launch pages
**Vibe:** Futuristic chrome tempered with warmth — soft metal, iridescent edges, controlled gloss. Not cyberpunk.
**Palette feel:** Soft silver base, iridescent violet primary, rose chrome secondary, brushed metal surfaces
**Animation style:** Magnetic spring motion. Elements glide, attracted to position. Slight overshoot.
**Typography:** Geometric futuristic (Sora + DM Sans + Space Mono).
**Key techniques:** Soft metal gradients, iridescent border sweeps (conic-gradient), specular highlights, no neon

---

#### 25. Botanical Blueprint
**File:** `references/themes/25-botanical-blueprint.md`
**Best for:** Education, scientific dashboards, simulations, biology tools, environmental data
**Vibe:** Scientific illustration meets botanical field notes — grids, annotations, gentle greens.
**Palette feel:** Cool field paper, leaf green accents, sepia wash annotations, blueprint blue for diagrams
**Animation style:** Diagrammatic. Elements slide along grid axes. Transitions explain relationships.
**Typography:** Scientific precision (Albert Sans + Instrument Sans + JetBrains Mono). Data-clear.
**Key techniques:** Blueprint grid background, watercolor washes, annotation leader-line draw, ink + wash separation

---

#### 26. Night Aquarium
**File:** `references/themes/26-night-aquarium.md`
**Best for:** Media players, ambient data art, night-mode creative tools, audio visualizers, relaxation
**Vibe:** Deep ocean calm with bioluminescent cues — dark teal depths, soft glow highlights.
**Palette feel:** Abyssal teal base, bioluminescent cyan accents, jellyfish pink secondary, plankton green ambient
**Animation style:** Organic and drifting. Slow springs, elements float and settle. Underwater physics.
**Typography:** Clean on dark (Manrope + Sora + Fira Code). Futuristic, readable.
**Key techniques:** Depth layering, organic glow box-shadows, optional WebGL caustics, no hard edges

---

#### 27. Cartographer's Desk
**File:** `references/themes/27-cartographers-desk.md`
**Best for:** Maps, dashboards, investigative journalism, geospatial tools, climate data, urban planning
**Vibe:** Map-room pragmatism — contour lines, layered paper, precise labeling.
**Palette feel:** Chart paper base, meridian blue water, terrain ochre land, forest green, contour brown
**Animation style:** Spatial continuity. Pan, zoom, parallax between layers. Everything has 2D position.
**Typography:** Dashboard (Instrument Sans + Albert Sans + JetBrains Mono). Small-size legibility.
**Key techniques:** Procedural contour SVGs, paper stacking with directional shadow, legend-style small-caps labels

---

#### 28. Signal & Noise Lab
**File:** `references/themes/28-signal-noise-lab.md`
**Best for:** Lab dashboards, simulation UIs, analytics, signal processing, ML experiment trackers
**Vibe:** Research lab aesthetic — clean surfaces, instrument-like components, measured noise textures.
**Palette feel:** Lab white base, oscilloscope blue + spectrum orange dual-channel data, calibrated green
**Animation style:** Instrumental. Transitions show causality (slider → readout), not decoration.
**Typography:** Technical (Space Grotesk + DM Sans + JetBrains Mono). Readout-focused.
**Key techniques:** Instrument panel cards with top-bar, anti-banding noise, dual-channel color, axis-aligned grid

---

#### 29. Riso Playbook
**File:** `references/themes/29-riso-playbook.md`
**Best for:** Creative tools, portfolios, event microsites, generative art UIs, zine-style content
**Vibe:** Riso print meets modern UI — limited inks, playful overlays, registration offsets.
**Palette feel:** Newsprint base, riso blue + red + yellow (3 inks only), overprint purple from multiply blend
**Animation style:** Stamped and physical. Print registration shift on load, ink stamp entries, rapid stagger.
**Typography:** Bold quirky (Bricolage Grotesque + Work Sans + Fira Code). Poster meets playbook.
**Key techniques:** Limited ink rule (3 colors + overprints), halftone texture, registration offset text-shadow, flat fills only

---

#### 30. Quiet Lattice Dashboard
**File:** `references/themes/30-quiet-lattice-dashboard.md`
**Best for:** Financial dashboards, admin panels, BI tools, SaaS analytics, enterprise software
**Vibe:** Premium dashboard without low-contrast gimmicks — calm neutrals, micro-structure, disciplined hierarchy.
**Palette feel:** Warm quiet white, panel grey surfaces, calm blue interactive, semantic-only color use
**Animation style:** Nearly invisible. Quick fades, value morphs. If you notice the animation, it's too much.
**Typography:** Refined professional (Plus Jakarta Sans + DM Sans + Geist Mono). Three levels only.
**Key techniques:** Micro-grid at 8% opacity, zero decoration, strict 3-level hierarchy, semantic colors only for semantics

---

#### 31. Gazette Pixel
**File:** `references/themes/31-gazette-pixel.md`
**Best for:** Mission control dashboards, multi-agent monitors, DevOps status walls, CI/CD pipelines, real-time telemetry, terminal-adjacent UIs
**Vibe:** Broadsheet newspaper set in dark concrete with pixel-art instrumentation — editorial authority meets 8-bit telemetry.
**Palette feel:** Warm charcoal canvas, cream ink, Anthropic sienna accent, per-agent accent system, coral focus text
**Animation style:** Quantized. Tick-based updates (800ms), steps() easing, pixel-bar growth. Zero physics, zero spring, zero bounce.
**Typography:** Space Grotesk (headline grotesque, 800 weight, ALL CAPS mastheads) + JetBrains Mono (data teletype). Two families only.
**Key techniques:** 7×7 pixel icons per agent role, 40-block mosaic status bars with role-specific fill patterns, 3×3 status grids, pixel bar charts (10×6 block grids), square step-block progress, newspaper-column KPI layout, full-card semantic color shift on error/warning

---

#### 32. TUI Block Grid
**File:** `references/themes/32-tui-block-grid.md`
**Best for:** Mission control dashboards, multi-agent monitors, DevOps status walls, CI/CD pipelines, real-time telemetry, terminal-adjacent UIs, agent orchestration panels
**Vibe:** Terminal UI meets pixel-art telemetry on Vercel-dark canvas — cool blacks, vivid accent pops, quantized data.
**Palette feel:** True black page, near-black cards, pure neutral greys, vivid saturated agent accents (emerald, amber, blue, purple)
**Animation style:** Quantized. Tick-based updates (800ms), steps() easing. Only smooth transition: dark↔light mode toggle at 300ms.
**Typography:** Inter 600 (headlines, sentence case) + Geist Mono 500–800 (all data/labels). Vercel-native stack.
**Key techniques:** Vercel-dark aesthetic, full light mode variant with accent darkening, 1.5px borders, zero border-radius, pixel blocks (mosaic bars, 3×3 grids, 10×6 bar charts, step blocks), segmented mode toggle

---

## Per-Theme File Anatomy

Every theme file follows this structure:
- **Identity** — Name, tagline, best-for use cases
- **Color Palette** — 6–8 colors with hex, role, and usage guidance
- **Typography** — Display + body + mono recommendation
- **Visual Style** — Texture, grain, rendering philosophy, compositing/blend modes
- **Animation Philosophy** — Easing character, timing, motion personality, physics model
- **Signature Animations** — 3–5 specific effects native to this theme
- **UI Components** — Buttons, sliders, cards, tooltips, borders
- **Dark Mode Variant** — Adjusted palette + rules (or light variant if natively dark)
- **Mobile Notes** — Performance tips, simplified effects, touch considerations

## Knowledge Base Quick Reference

The knowledge base files contain deep, research-backed guidance. Key takeaways:

**Color:** Build palettes in OKLCH, not HSL. Use chroma bell curves. APCA Lc ≥ 75 for body text. Apply gamut masking for harmony. Validate cultural color semantics.

**Typography:** Pick fonts by role (text/display/data). Variable fonts with optical sizing. Fluid scales via `clamp()`. Tabular numerals (`tnum`) in data. Tighten tracking on large type.

**Tokens:** Three tiers — primitive → semantic → component. Theme-switch by swapping semantic layer. Include motion/radius/density tokens.

**Motion:** Define intent classes (feedback/transition/attention/ambient). `prefers-reduced-motion` as first-class mode. Interruptible animation for app-like feel.

**Global:** Whitespace ≠ luxury universally. Red ≠ danger universally. Support RTL as first-class. Density toggles for high-info cultures.

**Generative:** Seeded randomness, probability distributions over uniform random. fBM for organic textures. SDFs for resolution-independent UI. Sequential scales vary luminance; categorical scales vary hue at constant luminance.

## Usage Rules

1. **Themes are starting points.** Adapt colors, timing, and effects to fit the specific artifact.
2. **Always pair with design-maestro.** Load `aesthetic-principles.md` for anti-slop rules.
3. **Accessibility is non-negotiable.** WCAG AA contrast, focus indicators, keyboard nav, 44px touch targets.
4. **prefers-reduced-motion always.** Every animation must have a reduced-motion fallback.
5. **Performance budgets.** Follow design-maestro limits. Animate only `transform`, `opacity`, `filter`.
6. **Theme mixing.** Combining elements from two themes is fine if intentional.
7. **Dark themes on dark canvases.** Themes 9, 12, 15, 23, 26, 31, 32 are natively dark — they provide light variants instead of dark mode.
8. **Knowledge base for decisions.** Load knowledge base files when making design choices, not for routine theme application.
