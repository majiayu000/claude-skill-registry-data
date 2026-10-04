---
name: design-auditor
description: |
  Audit an existing project's design system from its CSS, Tailwind config, and HTML templates. Generates a DESIGN.md documenting what exists, a Tailwind v4 theme (or migration), and an accessibility report. Use when the user says "audit my design", "audit this project's design", "document my design system", "migrate to tailwind", "convert to tailwind", or similar.
allowed-tools:
  - Bash(mkdir *)
  - Read
  - Write
  - Glob
  - Grep
  - Edit
---

# Design Auditor

Reads your project's existing styles, documents the design system, checks accessibility, and generates a Tailwind v4 theme or migration.

**Announce at start:** "I'm using the design-auditor skill."

## Workflow

1. **Discover style sources** — scan the project for all files that define visual styles. Follow the Discovery Instructions below.

2. **Read and analyze** — read all discovered files. Extract colors, typography, spacing, component patterns, and existing tokens. Follow the Analysis Instructions below.

3. **Ask for name** — "What should I call this design?" (used for folder name and frontmatter). Convert the answer to lowercase kebab-case for the folder name.

4. **Generate DESIGN.md** — document the current design system as-is, using the Output Template below. Note where values are inconsistent (e.g., 5 different grays used across files).

5. **Generate tailwind-theme.css** — produce a Tailwind v4 theme. Follow the Tailwind Migration Instructions below based on what was found:
   - If already on Tailwind v4: validate and normalize
   - If on Tailwind v3: convert config to v4 format
   - If no Tailwind: generate fresh theme from extracted values

6. **Run accessibility checks** — follow the Accessibility Check Instructions below. Generate accessibility-report.md.

7. **Save to project** — create `.claude/design/` in the project and write all three files:
   ```bash
   mkdir -p .claude/design
   ```

8. **Save to library** — also save to `~/.claude/designs/<name>/`, update `~/.claude/designs/_index.md` (source = "project audit").
   ```bash
   mkdir -p ~/.claude/designs/<name>
   ```

9. **Report summary** — tell the user: "Found X colors, Y font declarations, Z spacing values. Tailwind v4 theme generated. N of M contrast pairs pass AA. K colorblindness flags."

## Discovery Instructions

Scan the project for style sources using these Glob patterns. Exclude `node_modules/`, `vendor/`, `dist/`, `build/`, `.next/`, `.nuxt/` directories.

### CSS Files

```
**/*.css (excluding node_modules, vendor, dist, build)
```

In each CSS file, look for:
- `:root` or `html` blocks with custom properties (`--color-*`, `--font-*`, `--spacing-*`)
- `@font-face` declarations
- Color values in any format (hex, rgb, hsl, oklch)
- `@media` queries (breakpoints)
- `@theme` blocks (Tailwind v4 indicator)

### Tailwind Config (v3)

```
tailwind.config.js
tailwind.config.ts
tailwind.config.cjs
tailwind.config.mjs
```

If found, this is a Tailwind v3 project. Read the config to extract:
- `theme.colors` and `theme.extend.colors` — color tokens
- `theme.fontFamily` and `theme.extend.fontFamily` — font stacks
- `theme.spacing` and `theme.extend.spacing` — spacing scale
- `theme.borderRadius` — radius values
- `theme.boxShadow` — elevation values
- `theme.screens` — breakpoints

### WordPress theme.json

```
theme.json
```

If found, read:
- `settings.color.palette` — color tokens (each has name, slug, color)
- `settings.typography.fontFamilies` — font families
- `settings.typography.fontSizes` — type scale
- `settings.spacing.spacingSizes` — spacing scale
- `settings.layout.contentSize` and `wideSize` — layout widths

### HTML / Template Files

```
**/*.html
**/*.php
**/*.jsx
**/*.tsx
**/*.vue
**/*.svelte
**/*.astro
```

Scan for:
- Inline `style="..."` attributes — extract color, font, spacing values
- CSS class patterns that reveal the framework:
  - Tailwind classes: `bg-blue-500`, `text-lg`, `p-4`, `rounded-lg`
  - BEM: `block__element--modifier`
  - CSS Modules: `styles.className`
- Common component structures (buttons, cards, forms, navs)

### Package Indicators

Check `package.json` for:
- `tailwindcss` in dependencies (confirms Tailwind, check version for v3 vs v4)
- CSS framework dependencies (Bootstrap, Bulma, etc.)

## Analysis Instructions

After discovering files, extract design tokens by reading them systematically.

### Colors

Collect every color value across all files. Then deduplicate and categorize:

- **Primary** — the most prominent brand/interactive color (buttons, links, headings)
- **Secondary** — a second brand color for supporting elements
- **Accent** — decorative, gradient, or highlight colors
- **Neutral** — text, label, and body copy colors (often a gray scale — pick the most-used dark and light values)
- **Status** — success (green), warning (yellow/orange), error (red)
- **Surface** — background colors (page, card, section)
- **Border** — border and divider colors

Flag inconsistencies: "Found 7 different gray values — consolidated to 3 for the theme."

### Typography

Collect all font-family, font-size, font-weight, line-height, and letter-spacing declarations.

- Identify the primary font family (most frequently used)
- Map sizes to a scale: display, heading, subheading, body, caption, code
- Note which weights are actually used

### Spacing

Collect all margin, padding, and gap values. Identify the underlying scale pattern. Map to semantic names (xxs through xxl).

### Border Radius

Collect all border-radius values. Map to: micro, button, card, featured.

### Shadows

Collect all box-shadow values. Map to elevation levels 0-4.

### Layout

Note max-width values, grid patterns, and container padding.

### Responsive

Collect all @media breakpoint values. Note what changes at each.

### Dark Mode

Look for dark mode patterns in the project files:

1. **`prefers-color-scheme` media queries** — `@media (prefers-color-scheme: dark)` blocks with alternate color values
2. **Dark mode class toggles** — `.dark`, `[data-theme="dark"]`, `.theme-dark`, `[color-scheme="dark"]` selectors
3. **CSS custom property overrides** — `:root` variables redefined inside dark mode selectors or media queries
4. **Tailwind dark mode classes** — `dark:bg-*`, `dark:text-*` patterns in HTML/templates
5. **Tailwind v3 config** — `darkMode: 'class'` or `darkMode: 'media'` in tailwind.config
6. **WordPress theme.json** — `settings.color.palette` entries with dark variants, or separate color sets under `styles.blocks` for dark contexts

If dark mode is detected:
- Extract a complete alternate color palette (all the same roles)
- Note which mechanism is used (media query vs class toggle)
- Include section 10 in DESIGN.md and the dark mode block in tailwind-theme.css
- Run accessibility checks for both light and dark palettes

If no dark mode is detected, skip section 10 and the dark CSS block. Do not fabricate a dark palette.

## Tailwind Migration Instructions

### From Tailwind v4 (already)

If a `@theme` block exists in any CSS file:
1. Copy the existing theme
2. Check for missing standard tokens vs this list: `--color-text`, `--color-background`, `--color-primary`, `--color-secondary`, `--color-accent`, `--color-muted`, `--color-error`, `--color-success`, `--color-warning`, `--color-border`, `--color-card`, `--font-sans`, `--spacing-*` (xxs through xxl), `--radius-*`
3. Add any missing tokens with values inferred from the codebase, or `/* TODO: define */` if no value can be inferred
4. Ensure `color-mix()` light/dark variants exist for primary, secondary, accent
5. Add `/* validated and normalized by design-auditor */` header comment

### From Tailwind v3

If `tailwind.config.*` exists:
1. Read the config file
2. Convert each theme property to `@theme` CSS:
   - `colors.primary` → `--color-primary: #...;`
   - `colors.secondary` → `--color-secondary: #...;`
   - `fontFamily.sans` → `--font-sans: '...', fallbacks;`
   - `spacing.*` → `--spacing-*` with fluid `clamp()` values (map fixed v3 values to the nearest standard fluid step)
   - `borderRadius.*` → `--radius-*`
   - `boxShadow.*` → leave as reference in comments
3. Add `color-mix()` variants for primary, secondary, accent
4. Add `/* converted from tailwind.config v3 */` header comment
5. Add `/* original v3 value: <value> */` inline comments where the mapping was non-trivial

### From Plain CSS

If no Tailwind is detected:
1. Map `:root` custom properties to `@theme` tokens by semantic meaning
2. Convert fixed spacing values to the fluid `clamp()` scale (match to nearest standard step)
3. Preserve font-family stacks
4. Add `color-mix()` variants for primary, secondary, accent
5. Add `/* migrated from plain CSS */` header comment
6. Add `/* source: <original-property-name> in <filename> */` comments

### From WordPress theme.json

If `theme.json` is the primary style source:
1. Map `settings.color.palette` entries to semantic color tokens by slug/name
2. Map `settings.typography.fontFamilies` to `--font-sans`
3. Map `settings.spacing.spacingSizes` to `--spacing-*`
4. Map `settings.layout.contentSize` / `wideSize` to max-width references
5. Add `/* migrated from theme.json */` header comment

## Output Templates

### DESIGN.md

```markdown
---
name: "<design-name>"
source: "project audit"
extracted: YYYY-MM-DD
tags:
  - design-system
---

# <Design Name> Design System

## 1. Visual Theme & Atmosphere

One paragraph describing the current aesthetic based on what was found in the codebase: dominant colors, typography feel, overall impression.

## 2. Color Palette

### Primary
| Name | Hex | Role | Source File |
|------|-----|------|-------------|
| ... | #... | ... | `path/to/file.css` |

### Secondary
| Name | Hex | Role | Source File |
|------|-----|------|-------------|
| ... | #... | ... | `path/to/file.css` |

### Accent
| Name | Hex | Role | Source File |
|------|-----|------|-------------|
| ... | #... | ... | `path/to/file.css` |

### Neutral
| Name | Hex | Role | Source File |
|------|-----|------|-------------|
| ... | #... | ... | `path/to/file.css` |

### Status
| Name | Hex | Role | Source File |
|------|-----|------|-------------|
| Success | #... | ... | ... |
| Warning | #... | ... | ... |
| Error | #... | ... | ... |

### Surface & Border
| Name | Hex | Role | Source File |
|------|-----|------|-------------|
| Background | #... | ... | ... |
| Card | #... | ... | ... |
| Border | #... | ... | ... |

### Inconsistencies Found
<!-- List any color inconsistencies: duplicate near-values, undefined colors, etc. -->

## 3. Typography

**Font Family:** `<font-name>`, <fallback-stack>
**Source:** `<where the font was declared>`

| Level | Size | Weight | Line Height | Letter Spacing | Source |
|-------|------|--------|-------------|----------------|--------|
| Display | ...px | ... | ... | ... | `file:line` |
| Heading | ...px | ... | ... | ... | `file:line` |
| Subheading | ...px | ... | ... | ... | `file:line` |
| Body | ...px | ... | ... | ... | `file:line` |
| Caption | ...px | ... | ... | ... | `file:line` |
| Code | ...px | ... | ... | ... | `file:line` |

## 4. Components

### Buttons
| Variant | Background | Text | Border | Radius | Source |
|---------|------------|------|--------|--------|--------|
| Primary | ... | ... | ... | ... | `file:line` |
| Secondary | ... | ... | ... | ... | `file:line` |
| Ghost | ... | ... | ... | ... | `file:line` |

### Cards
- Observed patterns with source references

### Form Elements
- Observed patterns with source references

## 5. Layout

- **Max content width:** ...px (from `file`)
- **Grid patterns observed:** ...
- **Container padding:** ...

## 6. Spacing

| Token | Value | Frequency | Source |
|-------|-------|-----------|--------|
| xxs | ...px | N uses | ... |
| xs | ...px | N uses | ... |
| s | ...px | N uses | ... |
| m | ...px | N uses | ... |
| l | ...px | N uses | ... |
| xl | ...px | N uses | ... |
| xxl | ...px | N uses | ... |

## 7. Border Radius

| Token | Value | Context | Source |
|-------|-------|---------|--------|
| micro | ...px | ... | ... |
| button | ...px | ... | ... |
| card | ...px | ... | ... |
| featured | ...px | ... | ... |

## 8. Elevation

| Level | CSS Value | Usage | Source |
|-------|-----------|-------|--------|
| 0 | none | ... | ... |
| 1 | ... | ... | ... |
| 2 | ... | ... | ... |
| 3 | ... | ... | ... |
| 4 | ... | ... | ... |

## 9. Responsive Behavior

| Breakpoint | Width | Source |
|------------|-------|--------|
| sm | ...px | ... |
| md | ...px | ... |
| lg | ...px | ... |
| xl | ...px | ... |

## 10. Dark Mode (if detected)

**Mechanism:** `<prefers-color-scheme | class toggle (.dark) | data attribute | Tailwind dark: classes>`
**Source:** `<file(s) where dark mode was found>`

### Dark Color Palette
| Token | Light | Dark | Role | Source |
|-------|-------|------|------|--------|
| text | #... | #... | Body text | `file:line` |
| background | #... | #... | Page background | `file:line` |
| primary | #... | #... | Brand, CTA | `file:line` |
| secondary | #... | #... | Supporting brand | `file:line` |
| accent | #... | #... | Decorative | `file:line` |
| muted | #... | #... | Secondary text | `file:line` |
| border | #... | #... | Borders | `file:line` |
| card | #... | #... | Card surfaces | `file:line` |

<!-- Only include this section if dark mode was detected in the project files. Do not fabricate a dark palette. -->

## Migration Notes

<!-- Any notes about what was consolidated, what was ambiguous, what the user should verify -->
```

Note: the auditor template includes a **Source File** column in each table and a **Migration Notes** section at the end, since knowing where values came from is critical for auditing.

### tailwind-theme.css

```css
/* Design: <design-name>
 * Source: project audit
 * Extracted: YYYY-MM-DD
 * Migration: <from plain CSS | from Tailwind v3 | from theme.json | validated Tailwind v4>
 *
 * Import this file in your main stylesheet:
 *   @import "./tailwind-theme.css";
 *
 * Or copy the @theme block into your existing src/style.css
 */

@theme {
  /* COLORS */
  --color-text: #...;       /* source: <original-property or file> */
  --color-background: #...; /* source: <original> */
  --color-primary: #...;    /* source: <original> */
  --color-secondary: #...;  /* source: <original> */
  --color-accent: #...;     /* source: <original> */
  --color-muted: #...;      /* source: <original> */
  --color-error: #...;      /* source: <original> */
  --color-success: #...;    /* source: <original> */
  --color-warning: #...;    /* source: <original> */
  --color-border: #...;     /* source: <original> */
  --color-card: #...;       /* source: <original> */

  /* FONT FAMILY */
  /* NOTE: Font files need to be sourced and self-hosted as woff2.
   * See: https://gwfh.mranftl.com/fonts
   * Original font detected: <font-name> in <source-file> */
  --font-sans: '<font-name>', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

  /* FLUID SPACING */
  --spacing-0: 0;
  --spacing-xxs: clamp(0.25rem, 1vw, 0.5rem);
  --spacing-xs: clamp(0.5rem, 1.5vw, 0.75rem);
  --spacing-s: clamp(0.75rem, 2vw, 1rem);
  --spacing-m: 1.25rem;
  --spacing-l: clamp(1.25rem, 3vw, 2.5rem);
  --spacing-xl: clamp(1.25rem, 5vw, 3.75rem);
  --spacing-xxl: clamp(1.25rem, 10vw, 7.5rem);

  /* BORDER RADIUS */
  --radius-micro: ...;   /* source: <original> */
  --radius-button: ...;  /* source: <original> */
  --radius-card: ...;    /* source: <original> */
  --radius-featured: ...; /* source: <original> */
}

/* Color variants (auto-generated via color-mix in oklch) */
:root {
  --color-primary-light: color-mix(in oklch, var(--color-primary), white 30%);
  --color-primary-dark: color-mix(in oklch, var(--color-primary), black 20%);
  --color-secondary-light: color-mix(in oklch, var(--color-secondary), white 30%);
  --color-secondary-dark: color-mix(in oklch, var(--color-secondary), black 20%);
  --color-accent-light: color-mix(in oklch, var(--color-accent), white 30%);
  --color-accent-dark: color-mix(in oklch, var(--color-accent), black 20%);
}

/* @font-face — uncomment and update paths after sourcing woff2 files
@font-face {
  font-family: '<font-name>';
  src: url('/fonts/<font-file>-400.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
*/

/* Dark mode — only include if detected in project files
 * Uses prefers-color-scheme by default.
 * If the project uses a class toggle (.dark), replace the @media query
 * with: .dark { ... }
 */
/*
@media (prefers-color-scheme: dark) {
  :root {
    --color-text: #...;       /* source: <original> */
    --color-background: #...; /* source: <original> */
    --color-primary: #...;    /* source: <original> */
    --color-secondary: #...;  /* source: <original> */
    --color-accent: #...;     /* source: <original> */
    --color-muted: #...;      /* source: <original> */
    --color-error: #...;      /* source: <original> */
    --color-success: #...;    /* source: <original> */
    --color-warning: #...;    /* source: <original> */
    --color-border: #...;     /* source: <original> */
    --color-card: #...;       /* source: <original> */

    --color-primary-light: color-mix(in oklch, var(--color-primary), white 30%);
    --color-primary-dark: color-mix(in oklch, var(--color-primary), black 20%);
    --color-secondary-light: color-mix(in oklch, var(--color-secondary), white 30%);
    --color-secondary-dark: color-mix(in oklch, var(--color-secondary), black 20%);
    --color-accent-light: color-mix(in oklch, var(--color-accent), white 30%);
    --color-accent-dark: color-mix(in oklch, var(--color-accent), black 20%);
  }
}
*/
```

### accessibility-report.md

```markdown
---
design: "<design-name>"
checked: YYYY-MM-DD
---

# Accessibility Report: <Design Name>

## Contrast Ratio Results

| Pair | Ratio | AA Normal | AA Large | AAA Normal | AAA Large |
|------|-------|-----------|----------|------------|-----------|
| background / text | X.X:1 | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL |
| background / muted | X.X:1 | ... | ... | ... | ... |
| primary / white | X.X:1 | ... | ... | ... | ... |
| primary / background | X.X:1 | ... | ... | ... | ... |
| secondary / white | X.X:1 | ... | ... | ... | ... |
| secondary / background | X.X:1 | ... | ... | ... | ... |
| accent / text | X.X:1 | ... | ... | ... | ... |
| accent / background | X.X:1 | ... | ... | ... | ... |
| card / text | X.X:1 | ... | ... | ... | ... |
| card / muted | X.X:1 | ... | ... | ... | ... |
| error / white | X.X:1 | ... | ... | ... | ... |
| success / white | X.X:1 | ... | ... | ... | ... |
| warning / white | X.X:1 | ... | ... | ... | ... |

## Failures & Suggested Fixes

<!-- Only include this section if there are failures -->

| Pair | Current Ratio | Required | Suggestion |
|------|---------------|----------|------------|
| ... | X.X:1 | 4.5:1 (AA) | Darken/lighten <token> to #... |

## Colorblindness Simulation

| Pair | Protanopia | Deuteranopia | Tritanopia |
|------|------------|--------------|------------|
| ... | OK / FLAG | OK / FLAG | OK / FLAG |

<!-- FLAG means the two colors become difficult to distinguish under this type of color vision deficiency -->

## Summary

- **Total pairs checked:** N
- **AA pass rate:** N/N (X%)
- **AAA pass rate:** N/N (X%)
- **Critical failures (AA normal text):** N
- **Colorblindness flags:** N pairs flagged
```

## Accessibility Check Instructions

When generating the accessibility report, perform these calculations for every surface/text color pair.

### Contrast Ratios

1. Convert each hex color to sRGB values (0-1 range): `R = hex/255`, `G = hex/255`, `B = hex/255`
2. Linearize each channel: `channel <= 0.03928 ? channel/12.92 : ((channel+0.055)/1.055)^2.4`
3. Calculate relative luminance: `L = 0.2126*R_lin + 0.7152*G_lin + 0.0722*B_lin`
4. Calculate contrast ratio: `(L_lighter + 0.05) / (L_darker + 0.05)`
5. Compare against thresholds:
   - **AA normal text**: 4.5:1
   - **AA large text** (18px+ bold or 24px+): 3:1
   - **AAA normal text**: 7:1
   - **AAA large text**: 4.5:1

### Color Pairs to Check

Generate all meaningful surface/text combinations:
- background / text
- background / muted
- primary / white (#FFFFFF)
- primary / background
- secondary / white (#FFFFFF)
- secondary / background
- accent / text
- accent / background
- card / text
- card / muted
- error / white (#FFFFFF)
- success / white (#FFFFFF)
- warning / white (#FFFFFF) — or warning / text if warning is light

If additional surface/text pairs are evident from the project (e.g., dark section backgrounds with light text), include those too.

### Colorblindness Simulation

For each pair of colors that serve different semantic purposes (e.g., success vs error, primary vs accent):

1. Apply approximate transformation matrices for protanopia, deuteranopia, and tritanopia
2. Compare the simulated colors — if they appear very similar (approximate visual delta < 3.0), flag the pair
3. This is an approximation — flag as "possible issue" rather than claiming diagnostic precision

Common problems to watch for:
- Red/green pairs (protanopia, deuteranopia) — success vs error colors
- Blue/purple pairs (tritanopia) — primary vs accent when both are blue-purple range

### Suggested Fixes

For each failing contrast pair, suggest the minimum color adjustment needed:
- Calculate what luminance the text/surface color would need to reach the threshold
- Suggest a specific hex value that meets the requirement
- Prefer darkening text or lightening surfaces (maintain the design intent)

## Library Management

### Saving to Project

1. Create `.claude/design/` in the project: `mkdir -p .claude/design`
2. Write DESIGN.md, tailwind-theme.css, accessibility-report.md
3. If `.claude/design/` already has files, ask before overwriting: "`.claude/design/` already has files. Overwrite?"

### Saving to Library

1. Create the design directory: `mkdir -p ~/.claude/designs/<name>`
2. Write all three files to `~/.claude/designs/<name>/`
3. Read `~/.claude/designs/_index.md`
4. Append a new row: `| <name> | project audit | <YYYY-MM-DD> | <color-count> | <aa-pass-rate>% |`
5. Write the updated `_index.md`

If a design with the same name already exists in the index, ask before overwriting.

### "Use" Command

When the user says "use the <name> design" in any project:

1. Read files from `~/.claude/designs/<name>/`
2. Create `.claude/design/` in the current project: `mkdir -p .claude/design`
3. Copy all three files (DESIGN.md, tailwind-theme.css, accessibility-report.md)
4. Confirm: "Copied <name> design to `.claude/design/`. The tailwind-theme.css is ready to import into your stylesheet."

## Next Steps

After the audit completes, suggest these follow-up actions to the user:

1. **"Validate the theme"** — invoke `design-system-standards` to verify the generated tailwind-theme.css meets all token conventions (semantic naming, fluid spacing, contrast pairs)
2. **"Check Tailwind v4 patterns"** — invoke `tailwind-patterns` to verify the `@theme` block follows current v4 best practices, especially important after a v3→v4 migration
3. **"Build components from this design"** — invoke `frontend-design` to create or rebuild UI components that match the documented design system. It will read `.claude/design/DESIGN.md` automatically.
4. **"Fix accessibility issues"** — if the report flagged contrast failures, suggest specific token adjustments and offer to update the tailwind-theme.css with the fixes

Include these as a bulleted list in your final report message to the user.

## See Also

- **design-extractor** — extract a design system from a website URL instead of auditing local files
- **design-system-standards** — token conventions and Tailwind v4 patterns these files follow
- **frontend-design** — build production-grade UI components from a DESIGN.md
- **tailwind-patterns** — Tailwind v4 best practices and modern patterns
