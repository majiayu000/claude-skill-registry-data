---
name: maintaining-design-system
description: Design system maintenance for the site. Consult when modifying colours, typography, spacing, or themes. Covers token architecture, theme synchronisation, and CSS layers.
---

# Maintaining the Design System

Design system maintenance for the site. Tokens, themes, typography, and CSS architecture.

British English throughout—code, comments, documentation, content.

## When to Use

Consult this skill when modifying design tokens, adding or updating themes, or changing typography scales. Reference [SHIKI.md](./SHIKI.md) for syntax highlighting changes. Reference [COMPONENT_DESIGN.md](./COMPONENT_DESIGN.md) when creating new components or establishing component patterns.

## Philosophy

The design system pays homage to Swiss Style—clean, grid-locked, typographically precise. Every spatial decision aligns to an 8px grid. This constraint breeds coherence.

Discipline over necessity. The project's scale doesn't demand this rigour; the practice itself is valuable. The source will be public—it should exemplify high-quality design decisions.

## Token Architecture

Design tokens live in `src/styles/tokens/`. Each file defines a category of CSS custom properties.

| File | Purpose |
|------|---------|
| `colours.css` | Theme colour definitions (semantic: `--bg`, `--fg`, `--muted`, `--rule`, `--highlight`, `--emphasis`) |
| `typography.css` | Font families, size scale, line heights, letter spacing |
| `spacing.css` | Margin/padding scale (8px base) |
| `sizing.css` | Fixed dimensions |
| `layout.css` | Safe area insets for mobile |
| `z-index.css` | Stacking context scale |
| `transitions.css` | Animation timing tokens |
| `borders.css` | Border width scale |
| `index.css` | Barrel import (order matters: colours first) |

### Using Tokens

Before applying tokens, check the relevant file in `src/styles/tokens/` to verify available values and naming conventions. Token naming is not yet fully consistent across categories—some use pixel values, some use multipliers, some use semantic names. Don't assume a pattern; verify what exists.

### The 8px Grid

All spacing, sizing, and line heights must resolve to multiples of 8px. When adding new tokens:

- Convert target pixels to rem (divide by 16)
- Verify the pixel value is divisible by 8
- Follow the naming convention established in that token file

```css
/* Values must align to 8px grid */
--example: 2rem;    /* 32px, divisible by 8 ✓ */
--example: 1.875rem; /* 30px, breaks grid ✗ */
```

## CSS Layers

Layer order in `src/styles/global.css`:

```css
@layer reset, tokens, base, components, utilities;
```

This cascade ensures:

1. **reset** — Browser normalisation
2. **tokens** — Design variables (no selectors, just definitions)
3. **base** — Element defaults
4. **components** — Scoped component styles
5. **utilities** — Atomic overrides (Tailwind)

### Prose and Unlayering

`src/styles/prose.css` customises rendered MDX content, extending `@tailwindcss/typography`. It deliberately uses no `@layer` directive, placing it outside the layer system entirely.

Why: Tailwind utilities have high specificity within their layer. Prose styles need to override both the typography plugin defaults and base styles without fighting `!important` or specificity hacks. Unlayered styles win over layered styles regardless of specificity, giving prose full control over article typography.

## Theme System

Four themes: steel (default), purple, charcoal, teal. Theme class applied to `<html>`:

```html
<html class="theme-steel">
```

Each theme defines six semantic colours using OKLCH colour space in `src/styles/tokens/colours.css`:

```css
.theme-steel {
  --bg: oklch(...);
  --fg: oklch(...);
  --muted: oklch(...);
  --rule: oklch(...);
  --highlight: oklch(...);
  --emphasis: oklch(...);
}
```

### Theme Synchronisation

Theme colours appear in multiple locations. When modifying any theme colour, update all affected files:

| Location | Purpose | Format |
|----------|---------|--------|
| `src/styles/tokens/colours.css` | Primary token definitions | OKLCH |
| `src/styles/components/shiki.css` | Syntax highlighting overrides | OKLCH |
| `src/lib/theme/palette.ts` | OG images, meta theme-color | Hex |
| `public/sf-[theme].ico` | Per-theme favicon | Binary |
| `public/rss/styles.xsl` | RSS feed styling (steel only) | Hex |

The Boids animation reads `--rule` dynamically at runtime—no manual sync required.

### Adding a Theme

1. Add theme ID to `THEME_ORDER` and label to `THEME_LABELS` in `src/config/themes.ts`
2. Define colour tokens in `src/styles/tokens/colours.css`
3. Define syntax tokens in `src/styles/components/shiki.css` (see [SHIKI.md](./SHIKI.md))
4. Add OKLCH values to `THEME_COLOURS` in `src/lib/theme/palette.ts`
5. Create favicon at `public/sf-[theme].ico` (manual step—requires image editor or favicon generator)
6. Test across all page types (home, blog index, blog post, static pages)

## Typography

Two systems handle typography: components for UI chrome, prose.css for rendered content.

### Type Scale

Minor third ratio (1.2) with 8px-aligned line heights. Defined in `src/styles/tokens/typography.css`.

### Typography Components

For UI elements—headers, navigation, metadata, labels. Located in `src/components/typography/`:

| Component | Purpose | Default Colour |
|-----------|---------|----------------|
| `Overline` | Uppercase labels, section headers | muted |
| `Caption` | Dates, metadata, supporting text | muted |
| `Body` | Taglines, descriptions | muted |
| `SheenText` | Interactive text with hover animation | fg |

All accept `tag`, `color`, and spread attributes.

### Prose Styling

For rendered MDX content—blog posts, long-form writing. `src/styles/prose.css` extends `@tailwindcss/typography` and targets elements within `.prose`:

- Headings: size, weight, spacing, anchor link styling
- Paragraphs: measure, spacing
- Lists: marker styling, nesting
- Code: inline and block treatment
- Links: colour, hover states
- Blockquotes: border, indentation

Modify prose.css when changing how blog content renders. Changes affect all existing posts.

## Component Design

See [COMPONENT_DESIGN.md](./COMPONENT_DESIGN.md) for component structure, composability principles, spacing philosophy, and accessibility baseline.

## Technological Constraints

Some libraries don't support CSS custom properties, requiring hardcoded values.

### Satori (OG Images)

`src/lib/og/` generates Open Graph images. Satori renders JSX to SVG but doesn't support CSS variables. Colours must be hex values, defined in `src/lib/theme/palette.ts`:

```typescript
export const THEME_COLOURS: Record<Theme, ThemeColours> = {
  steel: {
    bg: oklchToHex(...),
    fg: oklchToHex(...),
    muted: oklchToHex(...),
    rule: oklchToHex(...),
  },
  // ... other themes
};
```

The OKLCH values here must match those in `colours.css`. When theme colours change, update both files.

### Favicons

Per-theme favicons (`public/sf-*.ico`) are static binary files. No programmatic generation—must be manually created when adding themes or changing brand colours.

### RSS Stylesheet

`public/rss/styles.xsl` uses hardcoded hex values for browser rendering. Currently locked to steel theme. Optional to update when steel changes.

## Checklists

### Modifying a Token

- [ ] Change value in appropriate `src/styles/tokens/*.css` file
- [ ] Verify value aligns to 8px grid (for spacing/sizing/line-height)
- [ ] Check for hardcoded duplicates in `palette.ts` if colour-related
- [ ] Run `npm run check` to verify no type errors
- [ ] Visual review across themes in browser

### Modifying Theme Colours

- [ ] Update `src/styles/tokens/colours.css`
- [ ] Update `src/styles/components/shiki.css` if affects syntax tokens
- [ ] Update `src/lib/theme/palette.ts` with hex equivalents
- [ ] Update favicon if brand colour changes
- [ ] Update RSS XSL if steel theme changes (optional)
- [ ] Test OG image generation at `/og/default.png`

### Adding a New Theme

- [ ] Add to `THEME_ORDER` and `THEME_LABELS` in `src/config/themes.ts`
- [ ] Add colour block in `src/styles/tokens/colours.css`
- [ ] Add syntax overrides in `src/styles/components/shiki.css`
- [ ] Add OKLCH values in `src/lib/theme/palette.ts`
- [ ] Create `public/sf-[theme].ico` (manual—use favicon generator tool)
- [ ] Test theme switcher cycles correctly
- [ ] Test code blocks render with correct syntax colours
- [ ] Test OG images generate with correct colours
