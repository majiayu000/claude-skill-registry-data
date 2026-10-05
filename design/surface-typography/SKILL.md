---
name: surface-typography
description: Build rigorous typography systems for web interfaces. Use this skill whenever setting up a type scale, choosing or pairing fonts, configuring fluid typography with clamp(), implementing vertical rhythm, tuning OpenType features, loading web fonts performantly, working with variable fonts, or diagnosing type rendering issues. Also triggers for any mention of font-size, line-height, letter-spacing, font pairing, type hierarchy, vertical rhythm, baseline grid, or "text looks off". Covers type scales (modular and custom), vertical rhythm and baseline alignment, fluid vs fixed typography, font loading strategy, subsetting, OpenType feature configuration, variable font axes, display/body pairing, and text rendering. Does NOT cover colour, animation, interaction design, platform quirks, or component APIs. Use surface-colour, surface-motion, surface-interaction, surface-details, or system-tokens and system-components for those concerns.
---

# Typography

Typography systems for web interfaces. Type is the primary interface material. It carries meaning before colour, layout, or motion. Getting it right is structural, not decorative.

Type supports the Simplicity pillar from `references/design-philosophy.md`: clear hierarchy guides the eye and reduces cognitive load. For colour systems, use **surface-colour**. For token architecture, use **system-tokens**. For multi-skill task sequencing, see `references/composition.md`.

---

## 1. Type Scale

A type scale is a constrained set of font sizes that maintains visual harmony. Never pick arbitrary sizes.

### Modular scales

A modular scale multiplies a base size by a consistent ratio.

| Ratio | Name | Character |
|---|---|---|
| 1.125 | Major second | Tight, compact UIs, dashboards |
| 1.200 | Minor third | Balanced, general-purpose |
| 1.250 | Major third | Comfortable, editorial |
| 1.333 | Perfect fourth | Expressive, marketing pages |
| 1.500 | Perfect fifth | High contrast, dramatic headlines |

### Fixed vs fluid

**App UIs** (dashboards, tools, SaaS) use a fixed type scale. Font sizes are set in `rem` and do not change with viewport width. Fluid sizing in a tool UI creates an unsettling feeling that the interface is shifting.

**Marketing and content pages** (landing pages, blogs, documentation) benefit from fluid typography using `clamp()`:

```css
font-size: clamp(2rem, 1.2rem + 2.1vw, 3.5rem);
```

Three values: minimum, preferred (scales with viewport), maximum. Always set both bounds to prevent extremes.

### Constructing a scale

Start from a base of 16px (1rem) for body text. Apply the ratio upward for headings and downward for captions. Store as design tokens following system-tokens conventions:

```css
--type-xs:   0.75rem;    /* 12px */
--type-sm:   0.875rem;   /* 14px */
--type-base: 1rem;       /* 16px */
--type-lg:   1.125rem;   /* 18px */
--type-xl:   1.25rem;    /* 20px */
--type-2xl:  1.5rem;     /* 24px */
--type-3xl:  1.875rem;   /* 30px */
--type-4xl:  2.25rem;    /* 36px */
--type-5xl:  3rem;       /* 48px */
```

---

## 2. Vertical Rhythm

All text and spacing aligns to a consistent baseline unit. This creates the visual order that makes a page feel composed.

### Baseline unit

Choose a baseline unit, typically 4px (0.25rem). All line-heights, margins, paddings, and gaps should be multiples of this unit.

### Line height

- Body text: 1.5 to 1.6 (unitless). Most readable range for paragraphs.
- Headings: 1.1 to 1.3 (unitless). Large text has built-in whitespace.
- Caption/small text: 1.4 to 1.5.
- Single-line UI text (buttons, labels, nav): 1.

Always use unitless line-height values. Unitless values scale proportionally with font size. Values with units (`24px`, `1.5rem`) create inheritance bugs in nested elements.

### Spacing

Paragraph margins, section gaps, and component padding snap to the baseline grid:

```css
p        { margin-bottom: 1.5rem; }   /* 24px = 6 units */
h2       { margin-top: 3rem; }        /* 48px = 12 units */
section  { padding: 2rem 0; }         /* 32px = 8 units */
```

---

## 3. Font Loading

Mishandled font loading causes layout shift (text reflows when the web font arrives) and invisible text (FOIT).

### Strategy

```css
@font-face {
  font-family: 'Custom Sans';
  src: url('/fonts/custom-sans.woff2') format('woff2');
  font-display: swap;
  size-adjust: 102%;
  ascent-override: 95%;
  descent-override: 22%;
  line-gap-override: 0%;
}
```

`font-display: swap` shows fallback text immediately, then swaps. The metric overrides (`size-adjust`, `ascent-override`, `descent-override`, `line-gap-override`) match the fallback font's metrics to the custom font, minimising layout shift on swap.

### Subset aggressively

Most fonts ship glyphs for dozens of languages. Subset to what you need:

```bash
pyftsubset CustomSans.woff2 \
  --output-file=CustomSans-latin.woff2 \
  --flavor=woff2 \
  --layout-features='kern,liga,calt' \
  --unicodes='U+0000-007F,U+00A0-00FF,U+2000-206F'
```

A full file is 80-120KB. A Latin subset is typically 15-30KB.

### Preload the primary font

```html
<link rel="preload" href="/fonts/custom-sans.woff2"
      as="font" type="font/woff2" crossorigin>
```

Only preload the body font. Preloading multiple fonts delays overall page load.

### Self-host

Self-hosting gives control over subsetting, caching headers, and avoids DNS lookups to third-party CDNs. Google Fonts can be downloaded and self-hosted.

---

## 4. OpenType Features

Typographic refinements built into the font. Many are off by default.

### Enable for body text

```css
.body-text {
  font-feature-settings: 'kern' 1, 'liga' 1, 'calt' 1;
}
```

`kern`: adjust spacing between specific letter pairs. `liga`: standard ligatures (fi, fl). `calt`: contextual alternates.

### Numeric figures

```css
/* Tables, counters, timers: fixed-width digits for alignment */
.tabular { font-variant-numeric: tabular-nums; }

/* Headings, display: full-height digits */
.heading { font-variant-numeric: lining-nums; }

/* Body prose: text-height digits that blend with lowercase */
.prose { font-variant-numeric: oldstyle-nums; }
```

Use `tabular-nums` wherever numbers appear in columns, change dynamically (counters, prices, timers), or need to align vertically. Without it, digits have different widths and columns look ragged.

### Check availability

Not all fonts support all features. Verify with [Wakamai Fondue](https://wakamaifondue.com) before enabling features the font doesn't have.

---

## 5. Variable Fonts

A single file containing multiple styles (weight, width, slant, optical size).

### Axes

| Axis | CSS | Tag | Typical range |
|---|---|---|---|
| Weight | `font-weight` | `wght` | 100-900 |
| Width | `font-stretch` | `wdth` | 75%-125% |
| Slant | `font-style: oblique Xdeg` | `slnt` | -12 to 0 |
| Optical size | `font-optical-sizing: auto` | `opsz` | 8-144 |

### Benefits

- **Performance.** One 50-80KB file replaces 4-6 static files (200-400KB total).
- **Precision.** Use intermediate weights (450, 550) that static fonts cannot provide.
- **Optical sizing.** The font adapts its design to its rendered size. Small sizes get wider spacing and open counters. Large sizes get tighter, more refined details.

Enable optical sizing (on by default in most browsers, don't turn it off):

```css
body { font-optical-sizing: auto; }
```

---

## 6. Font Pairing

### The rule of contrast

Pair fonts that are clearly different. Two similar sans-serifs look like a mistake. A geometric sans with a humanist serif creates clear contrast.

### Strategies

- **One font, two weights.** A variable font at 400 for body and 600-700 for headings. No pairing needed. The simplest and safest option.
- **Sans display + serif body.** Geometric or grotesque sans for headings, readable serif for body. Classic editorial.
- **Serif display + sans body.** High-contrast or display serif for headings, clean sans for body. Sophisticated and modern.
- **Monospace accent.** Monospace for code, metadata, or technical labels alongside a proportional font for everything else.

### Avoid

- Two fonts from the same classification (two geometric sans-serifs, two transitional serifs).
- More than two typeface families. A third for code/mono is the only acceptable exception.
- Display or decorative fonts for body text. They are designed for large sizes and become illegible at 14-18px.
- Font weights below 400 for body text. Thin weights are for headings only.

---

## 7. Rendering

```css
body {
  -webkit-font-smoothing: antialiased;     /* Sharper on macOS/iOS */
  text-rendering: optimizeLegibility;       /* Better kerning and ligatures */
  -webkit-text-size-adjust: 100%;           /* Prevent iOS landscape resizing */
}

h1, h2, h3 {
  text-wrap: balance;   /* Prevent orphans in headings */
}

p {
  text-wrap: pretty;    /* Better line-break decisions */
}
```

Note: `text-rendering: optimizeLegibility` can be slow on very large text blocks. Apply to body and heading text, not to massive data tables.

Use `text-wrap: balance` only for headings and short text blocks. Browsers limit balancing to short content because it is expensive. Use `text-wrap: pretty` for short and medium paragraphs, and leave long prose, code, and data tables to normal wrapping.

---

## Anti-Patterns

1. **Arbitrary font sizes.** If a size doesn't come from the scale, it shouldn't exist.
2. **`line-height` with units.** Using `24px` or `1.5rem` instead of the unitless `1.5`. Unitless values inherit correctly.
3. **`font-weight` change on hover.** Weight change shifts character widths and causes layout reflow. Use colour, underline, or opacity for hover states.
4. **Unsubsetted fonts.** Shipping 120KB when 20KB would do.
5. **No `font-display: swap`.** Text is invisible until the custom font loads.
6. **Heading sizes that leap.** 16px body to 48px h2 with nothing between. The scale should be gradual.
7. **Three or more type families.** Every additional family competes for attention. Two plus monospace is the ceiling.

---

## Checklist

### Scale
- All font sizes come from a defined type scale
- Scale uses a consistent ratio or intentionally custom steps
- Font sizes use `rem` (never `px` for text)
- App UIs use fixed scale; marketing pages may use fluid `clamp()`

### Rhythm
- Line heights are unitless
- Body: 1.5-1.6. Headings: 1.1-1.3. Captions: 1.4-1.5
- Spacing aligns to the baseline unit (4px)

### Loading
- Primary body font is preloaded
- `font-display: swap` on all `@font-face`
- Fonts are subsetted to required character ranges
- Metric overrides configured to minimise layout shift
- Fonts are self-hosted

### Features
- `kern`, `liga`, `calt` enabled for body text
- `tabular-nums` applied to columns, counters, and dynamic numbers
- `font-optical-sizing: auto` for variable fonts

### Pairing
- Two families maximum (plus monospace for code)
- Paired fonts have clear contrast
- No weight below 400 for body text
- Display fonts only at large sizes

### Rendering
- `-webkit-font-smoothing: antialiased`
- `text-rendering: optimizeLegibility`
- `text-wrap: balance` on headings
- `text-wrap: pretty` on paragraphs
- Long prose, code, and dense tables avoid forced wrapping rules

---

## Learning from Usage

After completing a typography task, review the output against the checklist. Append findings to `learnings.md` in this skill's folder. Installed learnings are local runtime notes preserved across suite updates; consult `learnings.md` before starting any new task.
