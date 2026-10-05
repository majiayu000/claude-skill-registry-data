---
name: web-typography
license: Apache-2.0
description: >-
  Expert front-end web typography — apply this whenever you are styling text on
  the web or making type decisions in HTML/CSS/JSX/Tailwind. Use it to choose
  and pair fonts, build a type scale, set body copy and headings, tune
  fluid/responsive type with clamp(), fix line-height, rhythm, measure and
  heading wraps, improve web-font loading and CLS, check WCAG 2.2 text
  accessibility, and apply modern CSS type features like text-wrap,
  font-variant-numeric, text-box-trim, and container-query units. Trigger when
  the user says "the text looks off," "make this readable," "set up typography,"
  "pick a font," "fix the headings," or "fonts are causing layout shift."
---

# Web Typography

You are setting type for screens, not print. The goal is text that is **legible**
(can you tell the letters apart), **readable** (is it comfortable to read at
length), and **clear in hierarchy** (does the eye know where to go) — across every
viewport, zoom level, and font preference a real user might have.

This skill encodes a small number of decisions that matter most, in the order you
should make them. Work top-down: get the **system** right (scale, measure, rhythm)
before reaching for clever features. Most "bad typography" on the web is not a
missing OpenType flag — it's a body size that's too small, a measure that's too
wide, line-height that's too tight, and a font that shifts the layout when it loads.

## Provenance — principle, not property

This skill is an **independent synthesis of widely-taught typographic principles**,
not a reproduction of anyone's writing, examples, or designs. Ideas are attributed to
their lineage (e.g. measure from Bringhurst, Letter→Text→Grid from Lupton, the modular
scale from Tim Brown) because crediting an idea is scholarship — but the expression and
the web translation here are this skill's own. When you apply or extend it, do the
same: express principles in your own words, credit the source of an idea where natural,
and never copy a source's prose, sample layouts, or proprietary content. The shared
*knowledge* is yours to use; any individual's *expression* is not.

## The decision order

Make these decisions in sequence. Each one constrains the next.

1. **Font choice** — Default to a fast, good system stack unless the brand needs a
   web font. If you load a web font, plan its loading (step 6) at the same time.
2. **Base size & measure** — Body text ≥ `1rem` (16px), line-length 45–75
   characters (`max-width: ~66ch`). These two do more for readability than anything else.
3. **Type scale** — Pick one modular ratio and derive every size from it. Make it
   fluid with `clamp()`. Don't hand-pick random px values.
4. **Vertical rhythm** — Line-height ~1.5 for body, tighter (1.1–1.3) for large
   headings. Space paragraphs *or* indent them, never both.
5. **Hierarchy & polish** — Weight/size/space contrast, `text-wrap: balance` on
   headings and `pretty` on body, tracking on caps and display, OpenType features.
6. **Loading & performance** — `font-display`, preload the one critical font,
   self-host WOFF2, and **metric-match the fallback** so the page doesn't shift (CLS).
7. **Accessibility pass** — Contrast, zoom to 200%, the WCAG 1.4.12 text-spacing
   overrides, never disable zoom, never justify body text.

## Non-negotiables (the rules that prevent the common failures)

These are the mistakes that show up again and again. Internalize the *why* so you
can apply them in novel situations, not just copy them.

- **Size body text in `rem`, never `px`.** `rem` respects the user's browser
  font-size setting; `px` silently overrides an accessibility preference. Reserve
  `px` for hairline borders and genuinely fixed physical details.
- **Line-height is unitless.** `line-height: 1.5` is inherited as a *ratio*, so
  each element recomputes from its own size. A fixed `line-height: 24px` inherits
  the computed pixel value and breaks on differently-sized children.
- **Never size fonts in pure `vw`.** Viewport units don't respond to zoom or user
  font-size — that fails WCAG 1.4.4. Always wrap fluid sizing in `clamp()` with a
  `rem` term: `clamp(2rem, 1rem + 3vw, 4rem)`. The `rem` keeps zoom working.
- **Constrain the measure.** Lines longer than ~75 characters make the eye lose its
  place on the return sweep; shorter than ~45 gets choppy. `max-width: 66ch` on
  text containers is the single highest-leverage readability fix.
- **Never justify body text on the web.** CSS justification without sophisticated
  hyphenation opens "rivers" of whitespace. Left-align, ragged right.
- **A web font must not shift the layout when it loads.** Pair `font-display` with
  a **metric-matched fallback** (`size-adjust` + `ascent/descent/line-gap-override`)
  so swapping the real font in causes zero reflow. This is the fix for font-driven CLS.

## Quick-start CSS

A sane, accessible baseline you can drop into almost any project. It uses a system
font stack (zero download) and a fluid scale. Adapt the ratio and fonts to the brief.

```css
:root {
  /* Fonts — system stack by default (instant, no CLS, native feel) */
  --font-sans: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial,
               "Apple Color Emoji", "Segoe UI Emoji", sans-serif;
  --font-serif: Charter, "Bitstream Charter", "Sitka Text", Cambria, Georgia, serif;
  --font-mono: ui-monospace, "SF Mono", "Cascadia Code", Menlo, Consolas, monospace;

  /* Fluid type scale (≈ Major Third 1.25 at desktop). Generate real projects with Utopia.fyi */
  --step--1: clamp(0.833rem, 0.80rem + 0.17vw, 0.9rem);
  --step-0:  clamp(1rem,    0.95rem + 0.25vw, 1.125rem);   /* body */
  --step-1:  clamp(1.25rem, 1.15rem + 0.50vw, 1.5rem);
  --step-2:  clamp(1.563rem,1.40rem + 0.80vw, 1.953rem);
  --step-3:  clamp(1.953rem,1.70rem + 1.25vw, 2.441rem);
  --step-4:  clamp(2.441rem,2.00rem + 2.00vw, 3.052rem);

  --measure: 66ch;
}

html { font-size: 100%; -webkit-text-size-adjust: 100%; }

body {
  font-family: var(--font-sans);
  font-size: var(--step-0);
  line-height: 1.5;
  font-synthesis: none;            /* don't fake bold/italic */
  text-rendering: optimizeLegibility;
}

h1, h2, h3, h4 { line-height: 1.15; text-wrap: balance; }   /* tight + even line lengths */
h1 { font-size: var(--step-4); }
h2 { font-size: var(--step-3); }
h3 { font-size: var(--step-2); }
h4 { font-size: var(--step-1); }

p, li, blockquote { max-width: var(--measure); text-wrap: pretty; }  /* measure + no orphans */
p + p { margin-block-start: 1em; }                                   /* space, don't indent */

:is(h1, h2, h3, h4) + * { margin-block-start: 0.5em; }

/* Data/figures align in columns */
table, .tabular-nums { font-variant-numeric: tabular-nums; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
}
```

A more complete, commented starter — including a metric-matched web-font example —
is in `assets/starter.css`. Read it when scaffolding a project's type from scratch.

## Reference files — read the one you need

Keep this file in context; pull a reference in when the task calls for it.

- **`references/decision-records.md`** — The distilled *reasoning* of the field: five
  meta-patterns (how typographers think) plus ADR-style decision records linking each
  rule to its rationale and the alternatives it rejects. **Read this when you face a
  novel judgment the other files don't directly cover** — the meta-patterns let you
  derive the right answer the way an expert would. Also the home of the "principle,
  not property" boundary.
- **`references/foundations.md`** — The classical principles (Lupton's *Letter /
  Text / Grid*, Bringhurst, Butterick) translated to the web: anatomy, measure,
  hierarchy, pairing, alignment. **Read this when choosing/pairing fonts or when a
  layout "feels off" but no single rule is obviously broken.**
- **`references/fluid-scale.md`** — Fluid type with `clamp()`, the `clamp()` math,
  modular-scale ratios, Utopia, container-query units (`cqi`) for component-level
  type. **Read this when building or adjusting a type scale, or making type respond
  to a container rather than the viewport.**
- **`references/font-loading.md`** — Web-font performance: `font-display`,
  preloading, self-hosting vs Google Fonts (GDPR), WOFF2, subsetting,
  `unicode-range`, variable fonts, and **eliminating CLS with metric-matched
  fallbacks** (`size-adjust`, `*-override`, Fontaine, next/font). **Read this
  whenever a project loads a custom web font or has layout-shift / slow-text issues.**
- **`references/accessibility.md`** — WCAG 2.2 for text: contrast ratios, resize to
  200% (1.4.4), text-spacing overrides (1.4.12), zoom, dyslexia/readability,
  reduced motion. **Read this before claiming type work is done, and any time the
  task mentions accessibility, a11y, contrast, or compliance.**
- **`references/modern-css.md`** — Current CSS type features with browser-support
  status: `text-wrap: balance/pretty`, OpenType (`font-variant-*`,
  `font-feature-settings`), `text-box-trim`/`text-box-edge`, `hanging-punctuation`,
  `initial-letter`, font-relative units (`lh`, `cap`, `ch`, `ic`), `line-clamp`,
  `color-mix` for tints. **Read this when reaching for a polish feature, and to
  check whether something needs progressive enhancement.**

## How to deliver

- When you change type, **explain the decision, not just the code** — "body bumped
  to 1.125rem and measure capped at 66ch so lines aren't 120 characters wide."
  Typography is judged by feel; tell the user what to look at.
- Prefer editing the project's existing tokens/scale over inventing a parallel one.
  If the project uses Tailwind, set the scale in `theme.fontSize` / CSS variables
  rather than scattering arbitrary values.
- Browser-support-sensitive features (flagged in `modern-css.md`) go in as
  **progressive enhancement** — the page must still read correctly without them.
- After non-trivial changes, do the **accessibility pass** (`references/accessibility.md`)
  before declaring done. Verify contrast and that the layout survives 200% zoom and
  the text-spacing overrides.
