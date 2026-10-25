---
name: "dark-surface-depth"
description: "Use when a page or section looks flat and needs real depth — layered same-hue gradient plus grain, without neon-glow clichés or stacking-context bugs."
---

# Dark surface depth

A flat `bg-black` or `bg-zinc-950` looks cheap for two real reasons: there is no implied light source, and 8-bit gradients on dark screens band visibly. Fix both, in that order, without turning the page into a synthwave poster.

Follow `ui-design-guardrails` for palette and layout decisions; this skill is only the surface technique.

## The three layers

1. **Base** — a solid near-black that is not `#000`: `#0b0b0d`, `#0d0c10`, or a brand-tinted equivalent. True black crushes shadows and kills every elevation cue.
2. **Light** — one large radial gradient in the *same hue family as the accent*, at low chroma, positioned where a light source would plausibly sit (usually above and behind the main content).
3. **Grain** — an SVG `feTurbulence` tile at 3–5% opacity. This is the part that removes banding; it is not decoration.

A kinetic layer (beams, dot grid, mesh) is optional and usually wrong. Add it only if the user asks, only one, and gate it on `prefers-reduced-motion` and viewport width.

## Working CSS

```css
@layer utilities {
  .surface-depth {
    position: relative;
    isolation: isolate;                 /* children stack above the grain */
    background-color: var(--surface, #0b0b0d);
    background-image:
      radial-gradient(
        120% 80% at 50% -10%,
        color-mix(in oklab, var(--accent) 16%, transparent),
        transparent 70%
      );
  }

  .surface-depth::after {
    content: "";
    position: fixed;                    /* viewport-wide: no seams on long pages */
    inset: 0;
    z-index: -1;                        /* behind content, above the base */
    pointer-events: none;
    opacity: 0.04;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  }
}
```

## Details that bite

- `isolation: isolate` plus `z-index: -1` is what keeps the grain behind the content. A `::before` with `z-index: 1` and no isolation sits *on top of* everything and swallows the layout — check this if text goes dim or unclickable.
- `position: fixed` inside an ancestor with `transform`, `filter`, `backdrop-filter`, or `will-change` is no longer viewport-fixed. Put `.surface-depth` above any animated wrapper.
- One accent hue. Two is a stretch; three is the purple/cyan/magenta cliché.
- Grain above ~6% reads as dirt and hurts text legibility on small type.
- Light mode needs this too: `#fff` bands the same way. Same recipe, tinted-white base, grain at 2–3%.
- Verify by screenshot, not by reasoning — banding and over-bright glows only show up when looked at.

## What this is not

There is no ambient occlusion, volumetric light, or shader in this technique, and CSS gradients do not simulate one. It is a tinted gradient plus a noise tile. Do not describe it to the user as anything more.