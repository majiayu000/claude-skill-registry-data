---
name: theming
description: Use when building a theme or theming system for an interface. Covers token architecture, dark mode, contrast preservation across themes, and generating a coherent palette from a seed colour.
metadata:
  category: design
  version: 1.0.0
  tags: [theming, dark-mode, tokens, color, css]
---

# Theming

## Purpose

Build themes that remain readable and coherent when switched. Dark mode is not an inversion; a palette that works on white will not work on black without being redesigned, and inverting it produces the vibrating, exhausting interfaces that dark mode is criticized for.

## When to Use

- Adding dark mode to an interface.
- Building a multi-theme or white-label system.
- Generating a palette from a brand colour.
- Fixing a theme where contrast breaks in one mode.

## Capabilities

- Semantic token architecture that supports theme switching.
- Dark-mode design (as opposed to inversion).
- Palette generation with perceptually uniform colour spaces.
- Contrast verification across every theme.
- Respecting system preference and user override.

## Inputs

- The base palette or the seed colour.
- The themes required: light, dark, high-contrast, per-brand.
- Accessibility requirements.

## Outputs

- Semantic tokens that resolve differently per theme.
- Every theme passing contrast requirements.
- A switch that respects the system preference and remembers an override.

## Workflow

1. **Build on semantic tokens** — Components reference `--color-surface`, never `--grey-900`. Only the semantic layer changes between themes; components do not change at all.
2. **Design the dark theme, do not invert it** — Pure black is harsh and causes halation with white text. Use a very dark grey. Desaturate the accents: a colour that is vivid on white is glaring on dark.
3. **Preserve the contrast relationships** — Verify every text-on-surface pairing in every theme. A ratio that passes in light frequently fails in dark.
4. **Work in a perceptual colour space** — OKLCH lightness is perceptually uniform; HSL's is not. Generating a scale in HSL produces steps that look wrong even though the numbers are even.
5. **Respect the system, allow an override** — Default to `prefers-color-scheme`, and store an explicit user choice.
6. **Handle elevation** — In light mode, elevation is a shadow. In dark mode, shadows are invisible; elevation is a lighter surface.

## Best Practices

- Pure black (`#000`) with pure white text causes halation — the text appears to vibrate. Every well-designed dark theme uses a dark grey around `#121212` to `#1a1a1a`.
- A saturated brand colour that looks correct on white will glow uncomfortably on a dark background. Reduce its saturation and raise its lightness for the dark theme.
- Elevation in dark mode is conveyed by making a surface *lighter*, not by adding a shadow. A shadow on a dark background is invisible.
- Test every theme against the contrast requirements. This is the single most common theming failure, and it is entirely mechanical to check.
- A theme toggle that does not persist is a bug that users notice on every page load.
- Do not animate the theme transition on colours. It looks impressive once and is irritating thereafter.

## Examples

**Semantic tokens, with the dark theme designed rather than inverted:**

```css
:root {
  /* Light: surfaces are near-white; elevation is a shadow. */
  --color-bg:              oklch(99% 0 0);
  --color-surface:         oklch(100% 0 0);
  --color-surface-raised:  oklch(100% 0 0);
  --shadow-raised:         0 1px 3px oklch(0% 0 0 / 0.12);

  --color-text:            oklch(20% 0.01 250);
  --color-text-muted:      oklch(50% 0.01 250);
  --color-border:          oklch(90% 0.005 250);

  --color-action:          oklch(55% 0.20 255);   /* the brand blue */
  --color-action-text:     oklch(100% 0 0);
}

[data-theme="dark"] {
  /* Not an inversion. #121212-equivalent, not black: pure black causes
     halation with white text. */
  --color-bg:              oklch(15% 0.005 250);
  --color-surface:         oklch(19% 0.005 250);

  /* Elevation in dark mode is a LIGHTER surface. A shadow would be invisible. */
  --color-surface-raised:  oklch(24% 0.006 250);
  --shadow-raised:         none;

  --color-text:            oklch(93% 0.005 250);  /* not pure white */
  --color-text-muted:      oklch(65% 0.008 250);
  --color-border:          oklch(30% 0.008 250);

  /* The brand blue, desaturated and lightened. The light-mode value
     (55% 0.20) glows uncomfortably against a dark surface. */
  --color-action:          oklch(68% 0.14 255);
  --color-action-text:     oklch(15% 0.005 250);
}
```

**Verifying contrast mechanically, in every theme:**

```typescript
const PAIRS = [
  ["--color-text",       "--color-surface", 4.5],   // body text: AA
  ["--color-text-muted", "--color-surface", 4.5],
  ["--color-action",     "--color-surface", 3.0],   // UI component boundary
  ["--color-action-text","--color-action",  4.5],   // text on the button
] as const;

for (const theme of ["light", "dark", "high-contrast"] as const) {
  for (const [fg, bg, required] of PAIRS) {
    const ratio = contrastRatio(resolve(fg, theme), resolve(bg, theme));
    if (ratio < required) {
      throw new Error(
        `Theme "${theme}": ${fg} on ${bg} is ${ratio.toFixed(2)}:1, ` +
        `below the required ${required}:1.`
      );
    }
  }
}
```

## Notes

- OKLCH is worth adopting specifically because its lightness channel is perceptually uniform. Generating a ten-step scale by evenly spacing HSL lightness produces steps that appear badly uneven; the same in OKLCH does not.
- The "elevation is a lighter surface" rule is the single detail that most distinguishes a well-designed dark theme from an inverted light one.
- Run the contrast check in CI. Themes drift as colours are adjusted, and a failing contrast ratio is silent until a user cannot read the interface.
