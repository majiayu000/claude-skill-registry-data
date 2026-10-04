---
name: CSS
slug: css
version: 1.0.4
description: 'Writes and debugs CSS: flexbox and grid layout, z-index and stacking, responsive breakpoints, theming, and render performance. Use when a layout breaks or overflows, z-index does nothing, the page scrolls sideways, `position: sticky` won''t stick, text won''t truncate, styles lose the cascade or need `!important`, content jumps while loading (CLS), transitions stutter, fonts flash, a modal or dropdown sits behind other content, form controls need restyling, a table needs sticky headers, printing comes out wrong, or a style works in Chrome but not Safari. Also for starting a stylesheet from scratch (reset and base layer), centering, container queries, fluid type with clamp(), design tokens and dark mode, RTL and logical properties, and modernizing old stylesheets with `:has()`, `@layer`, and nesting. Not for visual design taste — palettes, spacing scales, typeface choice.'
homepage: https://clawic.com/skills/css
changelog: 'Full coverage pass: deeper guides, situation-named files, and per-user configuration'
metadata:
  clawdbot:
    emoji: 🎨
    os:
    - linux
    - darwin
    - win32
    displayName: CSS
    configPaths:
    - ~/Clawic/data/css/
    - ~/css/
    - ~/clawic/css/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/css/
      - ~/css/
      - ~/clawic/css/
---

User preferences and memory live in `~/Clawic/data/css/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/css/` or `~/clawic/css/`), move it to `~/Clawic/data/css/`, and say in one line that you moved it and from where.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/css/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| authoring_mode | plain-css \| sass \| tailwind \| css-in-js | plain-css | Syntax of every emitted example, and which advice in `architecture.md` applies (layers and nesting vs utility ordering vs zero-runtime extraction) |
| browser_support | evergreen \| widely-available \| legacy | evergreen | Gates which features ship bare vs behind `@supports`: `legacy` also adds vendor-prefixed fallbacks and blocks the Chromium-first features flagged in `compatibility.md` |
| naming_convention | bem \| utility \| css-modules \| none | none | Class names in examples and the specificity ceiling enforced in reviews (`architecture.md` — Keeping It Clean) |
| rem_base | number px (10-16) | 16 | Every px→rem conversion, including the fluid-type derivation in `responsive.md` (rem term = px ÷ rem_base) |
| a11y_target | aa \| aaa | aa | Which row of Accessibility Floor gates output: AA = 4.5:1 body / 24×24 targets, AAA = 7:1 body / 44×44 targets |
| explanation_depth | mechanism \| fix-only | mechanism | How much of the why ships with each answer: `mechanism` names the cause (stacking context, flex sizing) before the declaration; `fix-only` emits the declaration plus one line |
| output_shape | diff \| full-sheet | diff | Emitted code: `diff` = only the changed declarations in context; `full-sheet` = the complete rewritten stylesheet or component block |

Preference areas to record as the user reveals them:

- **tooling** — build chain (PostCSS, Lightning CSS, bundler), formatter and lint rules, whether native nesting is allowed
- **conventions** — spacing and type scale in use, token naming, file-per-component vs grouped sheets
- **output** — beyond `explanation_depth` and `output_shape`: comment density in emitted CSS, longhand vs shorthand, whether fallbacks and `@supports` branches are shown or assumed, how much of the trade-off to state before choosing
- **platform** — target surfaces (app, marketing site, HTML email, print/PDF), device mix, whether RTL or CJK is in scope
- **risk posture** — appetite for Chromium-first features, tolerance for `!important` in third-party overrides, how loudly to flag accessibility regressions
- **constraints** — banned techniques (CSS-in-JS, utility classes, `@import`), inherited legacy stylesheets that must keep working

## When To Use

- Debugging layout: z-index that won't apply, overflow, dead `height: 100%`, broken `position: sticky`, mystery horizontal scroll
- Building components and starting stylesheets: reset and base layers, flexbox/grid patterns, centering, forms, tables, overlays, responsive behavior without media-query sprawl
- Production hardening: layout shift, animation jank, font loading, print output, the accessibility floor
- Replacing JS or preprocessor hacks with native CSS (`:has()`, `@layer`, `@scope`, container queries, scroll snap, anchor positioning)
- Cross-engine work: a rule that lands in Chrome and not Safari, RTL mirroring, HTML email constraints
- Not for visual design decisions (palettes, spacing scales, typography choice) — this skill covers mechanics, not taste

## Quick Reference

| Situation | Play |
|---|---|
| z-index ignored despite a huge value | Stacking Contexts below — find the context root; never just bump the number |
| Flex item overflows / text won't truncate | `min-width: 0` on the flex child (default min-width is min-content) |
| The rule is written but nothing changes | `debugging.md` — symptom→cause chains, starting with "is it even matching?" |
| Breaks with real content, sticky dead, footer floats, margin leaks | `layout.md` |
| Component must adapt to its container; fluid type; mobile viewport bugs | `responsive.md` |
| Specificity fight, `@layer`, `:has()`, custom-property gotchas | `selectors.md` |
| Jank, layout shift, slow paint, font flash | `performance.md` |
| Transition never fires, enter/exit animation, view transitions, reduced motion | `animations.md` |
| Line-height inheritance, measure, variable fonts, hyphenation, tabular numbers | `typography.md` |
| oklch vs hsl, `color-mix()`, gradient banding, wide gamut | `color.md` |
| Dark mode, design tokens, multi-brand, theme flash on load | `theming.md` |
| Inputs, selects, checkboxes, validation states, autofill styling | `forms.md` |
| Modal behind the header, dropdown clipped, tooltip placement | `overlays.md` |
| Scroll snap, custom scrollbars, anchor link lands under the sticky header | `scrolling.md` |
| Data table: sticky header, responsive behavior, column sizing | `tables.md` |
| Shadows, filters, masks, `clip-path`, blend modes, 3D transforms | `effects.md` |
| Starting a stylesheet: what goes in the reset and base layers, in what order | `reset.md` |
| Sheet organization, layer strategy, nesting, Sass migration, shadow DOM | `architecture.md` |
| Works in Chrome, breaks in Safari or Firefox; HTML email | `compatibility.md` |
| Print or PDF output wrong | `print.md` |
| RTL mirroring, CJK line breaking, logical properties, text expansion | `internationalization.md` |
| Anything else CSS | Core Rules below, then `debugging.md` to name the mechanism |

## Core Rules

1. Diagnose before adding CSS: reproduce, isolate in DevTools, name the mechanism (stacking context, flex sizing algorithm, margin collapse). A property added without a named mechanism is the next bug.
2. Animate only `transform` and `opacity` — the only common properties that skip layout and paint. Frame budget = 1000ms / 60fps ≈ 16.7ms for style, paint, and your JS combined; one layout-triggering animation spends it alone.
3. One centering default: parent `display: grid; place-content: center`. Escape hatch: `position: absolute; inset: 0; margin: auto` when the child must overlay (needs a resolvable size, e.g. `width: fit-content`).
4. Never bare viewport units for text. `font-size: clamp(1rem, 0.77rem + 0.91vw, 1.5rem)` — the rem term is what keeps browser zoom and user font-size working; pure-vw text fails WCAG 1.4.4 (resize to 200%). Derivation of the numbers: `responsive.md`.
5. Size intrinsically first (`min()`, `clamp()`, `fit-content`, `auto-fit` grids), media queries second, container queries when one component lives at different widths.
6. `!important` in component code is a debt marker. Order wars belong in `@layer` — unlayered author styles beat all layered ones regardless of specificity (`selectors.md`).
7. Overlays belong in the top layer, not high in the z-index scale. `<dialog>.showModal()` and `popover` escape every stacking context and every `overflow: hidden` ancestor; a z-index arms race means the wrong mechanism is in use (`overlays.md`).
8. A component styles its inside, never its outside: no `margin`, no `width`, no `position` on the component root — the parent layout owns placement. Components that set their own outer geometry break on the second reuse and get "fixed" with `!important`.

## Stacking Contexts

The single most common CSS debugging failure: raising z-index on an element trapped inside a context.

- Context creators (memorize): positioned element with z-index, flex/grid child with z-index, `opacity < 1`, `transform`, `filter`, `backdrop-filter`, `will-change`, `contain: layout` or `paint`, `position: fixed`/`sticky`, `isolation: isolate`.
- Inside a context, z-index competes only among siblings of that context. A child's `z-index: 9999` never escapes its parent's `z-index: 1`.
- Debug procedure, in order: (1) walk up from the losing element to its first context-creating ancestor; (2) same for the winning element; (3) compare those two ancestors — that comparison decides the paint order; (4) fix z-index there, or delete the accidental trigger (usually a leftover `transform` or `opacity` from an animation).
- `isolation: isolate` creates a context with zero visual side effects — use it to cap a component's internal z-index so it can't leak out.
- `transform`, `filter`, and `will-change` also make the element the containing block for `position: fixed` descendants — the fixed element behaves as absolute with no warning. Same walk-up diagnosis.
- Elements promoted to the top layer (modal `<dialog>`, `popover`) ignore all of the above: they paint above the page and above each other in open order (rule 7).

## Flexbox and Grid Mental Model

- `flex: 1` = `1 1 0%`: ALL space divided equally. `flex: auto` = `1 1 auto`: only leftover space divided, so larger content keeps a larger track. Choose per intent; equal columns need basis 0.
- Flex children default to `min-width: min-content` — the root cause of both overflow and un-truncatable text. Release with `min-width: 0` (or `overflow: hidden`). Column direction: same story with `min-height`.
- `1fr` means `minmax(auto, 1fr)`: the track refuses to shrink below its content. `grid-template-columns: 1fr 1fr` is NOT 50/50 with unequal content — write `minmax(0, 1fr)` for true halves.
- `auto-fit` collapses empty tracks (remaining cards stretch); `auto-fill` keeps them (cards hold max width). Card grid default: `repeat(auto-fit, minmax(min(250px, 100%), 1fr))` — the inner `min()` prevents overflow on viewports under 250px.
- `gap` never collapses; margins collapse (vertical, block layout only, including parent-child bleed-through). Prefer gap and treat margin collapse as legacy behavior to route around (`layout.md`).
- `margin: auto` on a flex/grid child absorbs free space: `margin-inline-start: auto` on the last nav item is the entire "push right" pattern.
- Grid when the parent decides both axes (page scaffolding, card grids, overlapping layers via named areas); flex when the children decide and simply wrap (toolbars, tag lists, button rows).

## Modern CSS Worth Using

Compatibility floor: everything here is in all three engines unless marked; version-sensitive items are dated in `compatibility.md`.

- `:has()` — parent and previous-sibling selection; kills a whole class of state-mirroring JS (`selectors.md` for patterns and cost).
- `@starting-style` + `transition-behavior: allow-discrete` — transition from `display: none`; replaces enter-animation JS (all engines since mid-2024).
- `light-dark()` + `color-scheme` — one declaration per token instead of a duplicated dark block (all engines since 2024; `theming.md`).
- `text-wrap: balance` on headings — engines skip long blocks (Chromium caps at 6 lines), so it is safe to apply to all headings.
- `scrollbar-gutter: stable` on scroll containers — reserves the gutter, no shift when the scrollbar appears.
- `overscroll-behavior: contain` on modals and drawers — stops scroll chaining into the page.
- `scroll-snap-type` + `scroll-snap-align` — carousels without JS (`scrolling.md`).
- `aspect-ratio` — reserve media space before load (layout-shift numbers: `performance.md`).
- `accent-color` — form controls on brand without rebuilding them (`forms.md`).
- `@scope` and native nesting — component boundaries without naming conventions; specificity traps in `architecture.md`.
- Individual transforms (`translate`, `rotate`, `scale`) — compose in a fixed order and animate independently, no more one-property transform collisions.
- Anchor positioning (`anchor-name`, `position-area`) — tethered popovers without a positioning library; still needs a fallback, see `overlays.md`.

## Accessibility Floor

Canonical home for these numbers — other files point here.

- Contrast (WCAG 2.2 AA): 4.5:1 body text; 3:1 for large text (≥24px, or ≥18.66px bold) and for UI components and focus indicators (1.4.3, 1.4.11). AAA raises body text to 7:1 and large text to 4.5:1 (1.4.6) — applies when `a11y_target: aaa`.
- Touch targets: ≥24×24 CSS px is the AA minimum (2.5.8); 44×44 matches Apple HIG and WCAG AAA (2.5.5) — use 44 for primary mobile actions and whenever `a11y_target: aaa`.
- Text survives 200% zoom (1.4.4): rem-based sizes plus the clamp rule (Core Rule 4).
- Motion is opt-in: wrap animation in `@media (prefers-reduced-motion: no-preference)` rather than overriding after the fact.
- Style `:focus-visible`; never `outline: none` without a replacement in the same rule.
- `@media (forced-colors: active)`: system colors replace yours — check borders and focus still exist there.
- Dark mode: `@media (prefers-color-scheme: dark)` plus `color-scheme: light dark` so form controls and scrollbars follow.
- Content reflows to a 320px-wide viewport without two-axis scrolling (1.4.10) — the practical floor for "does it work zoomed on a phone".
- Three different hides, chosen deliberately: `display: none` / `visibility: hidden` remove content from the accessibility tree; `aria-hidden` hides from assistive tech while staying visible; screen-reader-only text needs the clip pattern — `position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap`.

## Output Gates

Before shipping a stylesheet or component styles, verify:

- Hostile content survives: longest word (URL, German compound), empty state, missing image, 3-line title where you designed one line?
- 200% zoom and a 320px viewport reflow without horizontal scroll?
- Every interactive element has a visible `:focus-visible` style and meets the contrast and target-size rows above?
- Animation wrapped in `prefers-reduced-motion: no-preference`, and only `transform`/`opacity` in the frame loop?
- Media and embeds have reserved space (`aspect-ratio` or width/height attributes)?
- No `!important` outside a third-party override, and no new selector above single-class specificity?
- Dark mode checked if the project themes, and RTL checked if `internationalization.md` is in scope?

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Bumping z-index to 9999 | Element is inside a stacking context; only the context root competes outside | Walk-up procedure (→ Stacking Contexts) |
| Animating height/top/left/margin | Layout runs every frame and blows the 16.7ms budget (Core Rule 2) | `transform`; for height-to-auto, the grid-rows trick (→ layout.md) |
| `overflow: hidden` to kill a stray scrollbar | Hides the symptom and creates a scroll container: breaks sticky descendants, clips shadows and focus rings | Find the overflowing element first; when it cannot be removed, `html { overflow-x: clip }` — clip creates no scroll container, so sticky survives (→ layout.md) |
| `var(--x, fallback)` as a safety net | A declared-but-invalid value skips the fallback ("invalid at computed-value time") | `@property` with `initial-value` (→ selectors.md) |
| Global `will-change` or `translateZ(0)` "GPU hints" | Every layer holds GPU memory; hundreds of layers slow compositing | `will-change` only on elements actually animating, only while animating (→ performance.md) |
| `100vh` full-screen sections | Mobile browser UI overlaps the bottom of the section | `100svh`; `dvh` only when live resize is acceptable (→ responsive.md) |
| `!important` to win a specificity fight | Escalation is one-way; the next override needs another `!important` | `@layer` ordering (→ selectors.md) |
| `:empty` for empty states | Whitespace text nodes count as content in most engines | Control the markup, or a class set by the renderer |
| `transition: all` | Animates properties added later — including layout ones — and turns theme swaps into visible sweeps | Enumerate the properties you mean (→ animations.md) |
| `:invalid` for error styling | Matches an untouched empty required field on first paint: the form is red before typing | `:user-invalid` (→ forms.md) |
| `line-height: 150%` | Percentages inherit the COMPUTED value, so a big heading inherits the body's pixel leading | Unitless `line-height: 1.5` (→ typography.md) |
| `display: none` for screen-reader-only text | Removes it from the accessibility tree — nobody hears it | The clip pattern (→ Accessibility Floor) |
| `text-align: left` and `margin-left` in a themeable product | The first RTL locale mirrors everything except your CSS | Logical properties (→ internationalization.md) |

## Where Experts Disagree

- Selector performance: the old guard writes selectors for right-to-left matching cost; modern engines bucket by rightmost simple selector, making it negligible. Boundary: only act on a DevTools trace showing Style/Recalculate cost — usually `:has()` or universal selectors on large, frequently-mutating DOMs (`performance.md`).
- Utility-first vs handwritten CSS: utilities win on team consistency and dead-code elimination; handwritten wins for animation-heavy and design-led work. Boundary: follow whichever the codebase already uses; never mix systems inside one component.
- CSS-in-JS: colocation and typed themes vs runtime cost. Boundary: server-rendered, performance-critical pages want zero-runtime extraction (or plain CSS + `@layer`); internal dashboards can afford runtime styling.
- Contrast math: WCAG 2.x ratios are the legally referenced standard but misjudge dark backgrounds and thin type; APCA (the WCAG 3 candidate) models them better and is not yet normative. Boundary: ship to WCAG 2.2 numbers for compliance, use APCA as a tiebreaker when two palettes both pass.

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/css (install if the user confirms):
- `html` - semantic structure and document-level concerns the CSS hooks into
- `frontend` - component architecture, frameworks, and build tooling around the styles
- `animations` - motion design and choreography beyond single-property transitions
- `accessibility-audit` - full WCAG review beyond the CSS floor here
- `design-system` - tokens, theming, and scaling styles across a product

## Feedback

- If useful, star it: https://clawic.com/skills/css
- Latest version: https://clawic.com/skills/css

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/css.
