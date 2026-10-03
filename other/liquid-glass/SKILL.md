---
name: liquid-glass
description: Liquid glass — Apple-style frosted, refracting surfaces. Use when the user asks for glassmorphism, frosted/translucent panels, cards, menus or a glass topbar; when a glass surface looks wrong (gray, flat, invisible, unreadable text); or when another skill needs the glass recipe.
---

# Liquid Glass

Glass is **two layers, and the CSS one is not the interesting one**.

1. **CSS** paints the tint and the **rim** — a near-transparent white→gray gradient plus three inset highlights that read as a polished edge. This is what most "glassmorphism" snippets stop at.
2. **Refraction** bends the backdrop through the panel's edge, the way real glass does: a displacement map baked per element and consumed as `backdrop-filter: url(#filter)`. This is what makes it *liquid* rather than a blurred rectangle.

They ship as a pair — a class and a directive on the same element:

```html
<div class="liquid-glass" appLiquidGlass>…</div>
```

`assets/liquid-glass.css` is the CSS layer, self-contained (its own tokens, light and dark).
`assets/liquid-glass.directive.ts` is the refraction layer for Angular. Any other framework: port it, see [`references/refraction.md`](references/refraction.md) — the port is transcription, not design.

## The four rules

Each of these has one failure mode, and in every case the browser shows you something plausible instead of an error.

### 1. Glass needs a backdrop. Build it first.

Glass shows *what is behind it*. Behind a flat background there is nothing to show, so the panel renders as a faintly outlined gray box and the effect reads as broken — which sends people reaching for more blur and more opacity, the exact move that kills it.

So the ambient mesh is **part of the recipe, not decoration**: off-screen radial glows in a few hues (violet / pink / cyan), fixed to the viewport behind the content. Colour that the glass can pick up.

```html
<body class="liquid-glass-backdrop">
```

Verify this before styling a single panel: the page must look subtly *uneven* with no glass on it at all.

### 2. The glass is colorless — the colour arrives from behind.

The tint is white→70%-gray at 6% alpha in **both** themes. That is deliberate: hue in the tint fights the hue coming through the panel and the surface turns muddy. If a surface must be branded (a primary CTA, a FAB), override the **tint** locally and leave the rim, the border and the refraction alone:

```scss
.my-fab {
  /* refraction still comes from the directive */
  background: linear-gradient(155deg, rgba(79, 70, 229, 0.55), rgba(67, 56, 202, 0.42));
  border: 1px solid rgba(79, 70, 229, 0.5);
}
```

### 3. A child of a glass panel paints no surface of its own.

No `background`, no `border`, no second radius — the panel already supplies all three. An opaque fill paints *over* the refracted backdrop, which is the whole effect; a nested border draws a hard edge across the rim. Panels inside a glass dock, rows inside a glass card, a header band inside a glass section: all transparent, separated by spacing and type weight instead.

The cost of getting this wrong is a surface that reads darker and deader than its neighbours, and nothing points at the cause.

### 4. Refraction is progressive enhancement, and you cannot feature-query it.

`backdrop-filter` referencing an SVG filter renders in Chromium only. Safari **parses it and paints nothing** — so `@supports` reports success and the panel goes blank. Gate on engine (`navigator.userAgentData.brands`, `Chrome/` in the UA), and let everything else keep the stylesheet's plain `backdrop-filter: blur(3px) saturate(125%)` fallback. The directive already does this; keep it if you port.

## Pick the tier

Refraction bakes a canvas displacement map per element size, so it is priced per surface. Match the tier to the element:

| Tier | What it is | Use for |
|---|---|---|
| `liquid-glass-chip` | tokens + `blur(6px)`, **no directive** | chips, pills, badges, anything small or repeated in bulk |
| `liquid-glass` + directive | the full effect | cards, panels, topbars, circular controls, FABs |
| `liquid-glass-menu` | `blur(22px)` + a 55% wash of the overlay surface, no directive | dropdowns, popovers, context menus |
| `liquid-glass liquid-glass--modal` + directive | glass with an opaque frost layer over the tint | dialogs |

The menu and modal tiers exist for the same reason: **text has to stay readable**. A dropdown floats over arbitrary page content and a dialog over a scrim, so both trade some transparency for a wash — a menu through heavy blur, a modal through a theme-flipping frost (white in light, dark in dark). Do not "fix" either back to plain `.liquid-glass`.

## Adding glass to a project

1. Copy `assets/liquid-glass.css` in and link it. Confirm the app sets `data-theme="light|dark"` on `<html>` **before first paint** — the CSS keys both themes off that attribute; the file header carries the boot snippet.
2. Put `liquid-glass-backdrop` on the page shell. Stop and look: uneven, colored, no panels yet.
3. Apply a tier per element. Radius stays on the element (the directive reads the computed `border-radius` to shape the map).
4. Non-Angular: port the directive per [`references/refraction.md`](references/refraction.md).
5. Walk the checklist below. Every line is a bug someone shipped.

## Checklist

- [ ] The backdrop is visible with all glass removed.
- [ ] No child of a glass panel sets `background` or `border`.
- [ ] Both themes valued for every token you added, and both eyeballed — a rim tuned for dark disappears on white.
- [ ] Text on glass stays legible over the *busiest* part of the backdrop, not the calm part you happened to screenshot.
- [ ] Non-Chromium (or directive removed): still a decent frosted panel, nothing blank.
- [ ] Chips and repeated elements are on the CSS-only tier, not the directive.
- [ ] Nothing hardcodes a hex where a token exists.

More variants, hover, and the pitfalls behind each rule: [`references/recipes.md`](references/recipes.md).
