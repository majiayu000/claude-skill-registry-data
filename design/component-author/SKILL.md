---
name: component-author
description: Write a self-contained, production-quality React UI component to Vitrine's house rules - one TSX file plus one CSS file, no UI libraries, paper and night themes, full keyboard support, reduced motion, realistic demo content and documentation fields. Use when building a new reusable component or cleaning one up for a library.
---

# /component-author

A component should be something another developer can copy into their project and trust. These rules exist so that's true.

## Before writing code

- State the component in **one sentence**. If you can't, it's two components.
- Name the **familiar job** it does (tabs, a save state, a price) and the **one idea** that makes it better than the default. If the idea is only an effect, stop and rethink (see `/interface-critic`).
- Decide what's a prop and what's content. Content comes from props; nothing in the component should say "Lorem ipsum" or "Feature one".

## Files

```
<Name>.tsx     the component: exports, props, behaviour
<name>.css     all styles, prefixed with the component's name (.name__part, .name--variant, [data-state])
demo.tsx       a realistic example using the public props only
meta.ts        documentation (below)
```

- **No UI libraries and no animation libraries.** CSS transitions and animations, the Web Animations API, and `requestAnimationFrame` are enough.
- **Self-contained:** the component imports only React and its own CSS. Types it exposes are exported (`export type Item = …`).
- Style with CSS custom properties defined on the root class (`--x-ink`, `--x-bg`, `--x-line`, `--x-accent`). Themes and accents just override them.

## Behaviour rules

- **Themes:** `theme?: "paper" | "night"` at minimum, as a modifier class that swaps the custom properties.
- **Motion:**
  - Respect `@media (prefers-reduced-motion: reduce)`, and also accept `motion?: "full" | "reduced"` so a page can force it.
  - Reduced motion means no travel, no loops and no parallax; state changes become instant or short fades. The component must still be fully understandable.
- **Keyboard:**
  - Every pointer interaction has a keyboard equivalent.
  - Composite widgets use arrow keys inside with one Tab stop.
  - Escape closes what opened, and focus returns to its opener.
- **Focus:** `:focus-visible` styles on every interactive part, clearly visible in both themes.
- **Semantics:** use the right element first (`button`, `a`, `input`, `ol`, `dialog`), and ARIA only to fill gaps. Announce async changes in a `role="status"` region.
- **Layout:**
  - It must work at 375px wide. Size by the container (`min(100%, …)`, `%`, container queries) rather than viewport breakpoints, so it works in a card as well as a page.
  - Never cause horizontal scroll.
- **Touch:** no hover-only features. Hit areas are at least 24×24px, and grow them with padding or a pseudo-element on `(pointer: coarse)` if the visual must stay small.
- **Motion that measures itself** (FLIP, springs): measure positions relative to the component, not the viewport, so scrolling doesn't read as movement. Remove any in-flight transform before measuring, so a move that's already animating continues instead of jumping.
- **Performance:** animate `transform` and `opacity`; pause loops and `requestAnimationFrame` work when offscreen (IntersectionObserver) or when the tab is hidden.

## The demo

- Realistic content: real-sounding names, places, dates, numbers and sentences, specific to one plausible product.
- Show every state: empty, loading, error and success where they exist, with a small control bar to switch between them.
- Use only public props. If the demo needs to reach inside, the API is wrong.

## meta.ts, the documentation

Write these fields so someone can understand and rebuild the component without reading the code:

- **description**: one or two sentences: the job and the idea.
- **prompt**: a precise build brief. Structure, props, exact timings and easings, states, accessibility, responsive behaviour. It should be good enough that a capable model could rebuild the component from it alone.
- **interaction**: what to try.
- **animation**: every motion with its duration and what it communicates.
- **a11y**: keyboard map, roles and announcements, and reduced-motion behaviour.
- **responsive**: what changes at narrow widths.

## Done means

- Type-checks with no errors, and there are no console errors or warnings.
- Checked in a real browser at 375, 768 and 1280 (see `/responsive-audit`), in both themes, with reduced motion on.
- The keyboard walk passes (see `/accessibility-pass`).
- A still screenshot, with motion off, still looks deliberate.
