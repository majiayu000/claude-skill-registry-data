---
name: design-extractor
description: |
  Extract a visual design system from any website URL and generate a DESIGN.md, Tailwind v4 theme, and accessibility report. Use when the user says "extract the design from <url>", "grab the design from <url>", "get the design system from <url>", "pull the design from <url>", or similar. Requires Firecrawl CLI.
allowed-tools:
  - Bash(firecrawl *)
  - Bash(npx firecrawl *)
  - Bash(mkdir *)
  - Bash(curl *)
  - Bash(cat */design-extract* | grep *)
  - Bash(cat */design-extract* | tr *)
  - Bash(SCREENSHOT_URL=*)
  - Bash(file *)
  - Bash(cp *)
  - Read
  - Write
  - Glob
  - Grep
  - Edit
---

# Design Extractor

Scrapes a URL, analyzes the visual design system, and generates: DESIGN.md, tailwind-theme.css, accessibility-report.md, and a preview screenshot.

**Announce at start:** "I'm using the design-extractor skill."

## Workflow

1. **Ask for name** — "What should I call this design?" (used for folder naming and frontmatter). Convert the answer to lowercase kebab-case for the folder name.

2. **Scrape the URL** — run:
   ```bash
   firecrawl scrape "<url>" --format html -o /tmp/design-extract-raw.html
   ```
   If that fails or returns thin content, try without `--only-main-content` to get the full page. For JS-heavy sites, add `--wait-for 3000`.

3. **Capture screenshot** — run:
   ```bash
   firecrawl scrape "<url>" --format screenshot -o /tmp/design-extract-screenshot-raw.txt
   ```
   Firecrawl returns a URL to the screenshot, not the binary file. Extract and download it:
   ```bash
   SCREENSHOT_URL=$(head -1 /tmp/design-extract-screenshot-raw.txt | sed 's/Screenshot: //') && curl -sL "$SCREENSHOT_URL" -o /tmp/design-extract-preview.png
   ```
   Verify it's a valid PNG: `file /tmp/design-extract-preview.png` should show "PNG image data".

4. **Read the scraped file** — the HTML file may be very large (500KB+). Don't try to read it all at once. Instead:
   - Extract hex colors: `cat /tmp/design-extract-raw.html | grep -oE '#[0-9a-fA-F]{3,8}' | sort | uniq -c | sort -rn | head -30`
   - Look for font names: `cat /tmp/design-extract-raw.html | grep -ioE 'inter|roboto|SF Pro|system-ui|helvetica|poppins|outfit|geist|sohne' | sort | uniq -c | sort -rn`
   - Check dark mode: `cat /tmp/design-extract-raw.html | grep -oE 'data-theme="[^"]+"' | sort -u` and `cat /tmp/design-extract-raw.html | grep -oE 'color-scheme:[^;"]+' | sort -u`
   - Extract radius values: `cat /tmp/design-extract-raw.html | grep -oE 'border-radius:[^;"]+' | sort | uniq -c | sort -rn | head -10`
   - Then read portions of the file with offset/limit to examine specific style blocks and class patterns.

5. **Extract design tokens** — follow the Analysis Instructions below to identify colors, typography, spacing, shadows, radii, layout patterns, and responsive breakpoints. Also detect dark mode — see Dark Mode Detection below.

6. **Generate DESIGN.md** — structure extracted tokens into the format using the Output Template below. If dark mode was detected, include section 10 (Dark Mode).

7. **Generate tailwind-theme.css** — map extracted tokens to semantic Tailwind v4 theme variables using the Output Template below. If dark mode was detected, include the `@media (prefers-color-scheme: dark)` block.

8. **Run accessibility checks** — follow the Accessibility Check Instructions below. Generate accessibility-report.md. If dark mode was detected, run checks for both light and dark palettes.

9. **Save to library** — write all files to `~/.claude/designs/<name>/`. Create the directory if needed:
   ```bash
   mkdir -p ~/.claude/designs/<name>
   ```
   Copy the screenshot: move `/tmp/design-extract-preview.png` to `~/.claude/designs/<name>/preview.png`.

10. **Update library index** — read `~/.claude/designs/_index.md` and append a row:
    ```
    | <name> | <url> | <YYYY-MM-DD> | <color-count> | <aa-pass-rate>% | <dark-mode?> |
    ```
    If a design with the same name already exists in the index, ask the user before overwriting.

11. **Ask about project** — "Want me to copy this into your current project's `.claude/design/` directory?" If yes, create `.claude/design/` and copy all files including preview.png.

## Analysis Instructions

When reading the scraped HTML, extract design tokens using these guidelines:

### Colors

Look for color values in all formats: hex (#xxx, #xxxxxx), rgb(), rgba(), hsl(), hsla(), CSS custom properties (--color-*, --*-color). Also look for Tailwind class patterns (bg-blue-500, text-gray-900, etc.) and infer the underlying values.

Categorize by usage context:
- **Primary** — dominant brand color, main CTAs, primary buttons. Look at the most prominent button or link color.
- **Secondary** — supporting brand color, secondary buttons/actions. Look for a second prominent color used for less important interactive elements.
- **Accent** — decorative elements, gradients, highlights, hover states. Look for colors used sparingly for emphasis.
- **Neutral** — text colors, labels, body copy, disabled states. Look at paragraph and heading text colors.
- **Status** — success (green-ish), warning (yellow/orange-ish), error (red-ish). Look in form validation, alerts, badges.
- **Surface** — page backgrounds, card backgrounds, section backgrounds. Look at body background, card/panel backgrounds.
- **Border** — default borders, dividers, focus rings. Look at input borders, card borders, horizontal rules.

### Typography

Look for:
- `font-family` declarations — capture the full stack
- `@font-face` blocks — note the font name, weights available, and file URLs if visible
- Font size patterns — map to a scale (display/hero, heading, subheading, body, caption, code)
- Font weight patterns — note which weights are used where
- Line height and letter-spacing values — associate with each scale level
- `font-feature-settings` — note any OpenType features (tabular numbers, stylistic sets)

### Spacing

Look for repeated margin, padding, and gap values. Identify the scale pattern (e.g., 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px). Note which values appear most frequently.

### Border Radius

Look for `border-radius` values and their context:
- Small (1-2px) — micro, subtle rounding
- Medium (4-6px) — buttons, inputs
- Large (8-12px) — cards, panels
- XL (16px+) — featured elements, pills

### Shadows / Elevation

Look for `box-shadow` values. Categorize by visual depth:
- Level 0 — flat, no shadow
- Level 1 — subtle ambient shadow
- Level 2 — standard card shadow
- Level 3 — elevated, prominent shadow
- Level 4 — deep shadow (dropdowns, modals)
- Focus — ring/outline style for focus states

### Layout

Look for:
- `max-width` on containers — note the site's content width
- Grid patterns (`grid-template-columns`, common column counts)
- Flexbox patterns (common flex arrangements)
- Section padding patterns

### Responsive

Look for `@media` queries. Note:
- Breakpoint values (e.g., 640px, 768px, 1024px, 1280px)
- What changes at each breakpoint (layout shifts, font size changes, visibility toggles)

### When Uncertain

If a token is ambiguous (e.g., a color could be primary or secondary), make your best judgment based on visual prominence and usage frequency. Add a `<!-- uncertain: reason -->` comment in the DESIGN.md output so the user can verify.

## Dark Mode Detection

Look for dark mode indicators in the scraped HTML:

1. **`prefers-color-scheme` media queries** — `@media (prefers-color-scheme: dark)` blocks with alternate color values
2. **Dark mode class toggles** — `.dark`, `[data-theme="dark"]`, `.theme-dark`, `[color-scheme="dark"]` selectors with alternate colors
3. **CSS custom property overrides** — `:root` variables redefined inside dark mode selectors or media queries
4. **Tailwind dark mode classes** — `dark:bg-*`, `dark:text-*` patterns in HTML

If dark mode is detected:
- Extract a complete alternate color palette (all the same roles: primary, secondary, accent, neutral, status, surface, border)
- Note which mechanism is used (media query vs class toggle)
- Include section 10 in DESIGN.md and the dark mode block in tailwind-theme.css
- Run accessibility checks for both light and dark palettes

If the site is **dark-first** (the default/only theme served is dark, like Linear), note this in the DESIGN.md — the main palette IS the dark palette. The tailwind-theme.css should include a comment suggesting where to add light mode overrides if needed, rather than a `prefers-color-scheme: dark` block.

If no dark mode is detected, skip section 10 and the dark CSS block. Do not fabricate a dark palette.

## Output Templates

### DESIGN.md

```markdown
---
name: "<design-name>"
source: "<url>"
extracted: YYYY-MM-DD
tags:
  - design-system
---

# <Design Name> Design System

## 1. Visual Theme & Atmosphere

One paragraph describing the overall aesthetic: mood, visual language, influences, best suited for what kind of projects.

## 2. Color Palette

### Primary
| Name | Hex | Role |
|------|-----|------|
| ... | #... | Brand, CTA |

### Secondary
| Name | Hex | Role |
|------|-----|------|
| ... | #... | Supporting brand, secondary actions |

### Accent
| Name | Hex | Role |
|------|-----|------|
| ... | #... | Decorative, gradients, highlights |

### Neutral
| Name | Hex | Role |
|------|-----|------|
| ... | #... | Text, labels, body |

### Status
| Name | Hex | Role |
|------|-----|------|
| Success | #... | Success states |
| Warning | #... | Warning states |
| Error | #... | Error states |

### Surface & Border
| Name | Hex | Role |
|------|-----|------|
| Background | #... | Page background |
| Card | #... | Card/panel background |
| Border | #... | Default border |

## 3. Typography

**Font Family:** `<font-name>`, <fallback-stack>

| Level | Size | Weight | Line Height | Letter Spacing | Notes |
|-------|------|--------|-------------|----------------|-------|
| Display | ...px | ... | ... | ... | |
| Heading | ...px | ... | ... | ... | |
| Subheading | ...px | ... | ... | ... | |
| Body | ...px | ... | ... | ... | |
| Caption | ...px | ... | ... | ... | |
| Code | ...px | ... | ... | ... | Monospace font |

## 4. Components

### Buttons
| Variant | Background | Text | Border | Radius | Notes |
|---------|------------|------|--------|--------|-------|
| Primary | ... | ... | ... | ... | |
| Secondary | ... | ... | ... | ... | |
| Ghost | ... | ... | ... | ... | |
| Disabled | ... | ... | ... | ... | |

### Cards
- Default: background, border, shadow, radius
- Elevated: shadow variant
- Interactive: hover state

### Form Elements
- Default input: border, radius, padding
- Focus: ring color, ring width
- Error: border color, message color

### Badges
- Variants observed with colors

## 5. Layout

- **Max content width:** ...px
- **Grid:** ... columns, ... gap
- **Container padding:** ...

## 6. Spacing

| Token | Value | Mapped to |
|-------|-------|-----------|
| xxs | ...px | Tight inline gaps |
| xs | ...px | Small gaps |
| s | ...px | Default small |
| m | ...px | Medium (anchor) |
| l | ...px | Sections, cards |
| xl | ...px | Large sections |
| xxl | ...px | Page-level |

## 7. Border Radius

| Token | Value | Context |
|-------|-------|---------|
| micro | ...px | Subtle rounding |
| button | ...px | Buttons, inputs |
| card | ...px | Cards, panels |
| featured | ...px | Featured elements |

## 8. Elevation

| Level | CSS Value | Usage |
|-------|-----------|-------|
| 0 (flat) | none | Default |
| 1 (subtle) | ... | Ambient |
| 2 (standard) | ... | Cards |
| 3 (elevated) | ... | Dropdowns |
| 4 (deep) | ... | Modals |
| Focus | ... | Focus rings |

## 9. Responsive Behavior

| Breakpoint | Width | Changes |
|------------|-------|---------|
| sm | ...px | ... |
| md | ...px | ... |
| lg | ...px | ... |
| xl | ...px | ... |

## 10. Dark Mode (if detected)

**Mechanism:** `<prefers-color-scheme | class toggle (.dark) | data attribute>`

### Dark Color Palette
| Token | Light | Dark | Role |
|-------|-------|------|------|
| text | #... | #... | Body text |
| background | #... | #... | Page background |
| primary | #... | #... | Brand, CTA |
| secondary | #... | #... | Supporting brand |
| accent | #... | #... | Decorative |
| muted | #... | #... | Secondary text |
| border | #... | #... | Borders |
| card | #... | #... | Card surfaces |

<!-- Only include this section if dark mode was detected in the source. Do not fabricate a dark palette. -->
```

### tailwind-theme.css

```css
/* Design: <design-name>
 * Source: <url>
 * Extracted: YYYY-MM-DD
 *
 * Import this file in your main stylesheet:
 *   @import "./tailwind-theme.css";
 *
 * Or copy the @theme block into your existing src/style.css
 */

@theme {
  /* COLORS */
  --color-text: #...;
  --color-background: #...;
  --color-primary: #...;
  --color-secondary: #...;
  --color-accent: #...;
  --color-muted: #...;
  --color-error: #...;
  --color-success: #...;
  --color-warning: #...;
  --color-border: #...;
  --color-card: #...;

  /* FONT FAMILY */
  /* NOTE: Font files need to be sourced and self-hosted as woff2.
   * See: https://gwfh.mranftl.com/fonts
   * Original font detected: <font-name> */
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
  --radius-micro: ...;
  --radius-button: ...;
  --radius-card: ...;
  --radius-featured: ...;
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

/* Dark mode — only include if detected in source
 * Uses prefers-color-scheme by default.
 * If the source uses a class toggle (.dark), replace the @media query
 * with: .dark { ... }
 */
/*
@media (prefers-color-scheme: dark) {
  :root {
    --color-text: #...;
    --color-background: #...;
    --color-primary: #...;
    --color-secondary: #...;
    --color-accent: #...;
    --color-muted: #...;
    --color-error: #...;
    --color-success: #...;
    --color-warning: #...;
    --color-border: #...;
    --color-card: #...;

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

If additional surface/text pairs are evident from the design (e.g., dark section backgrounds with light text), include those too.

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

### Saving to Library

1. Create the design directory: `mkdir -p ~/.claude/designs/<name>`
2. Write all four files to `~/.claude/designs/<name>/` (DESIGN.md, tailwind-theme.css, accessibility-report.md, preview.png)
3. Read `~/.claude/designs/_index.md`
4. Append a new row with: name, source URL, today's date, count of unique colors extracted, AA pass rate from the accessibility report
5. Write the updated `_index.md`

If a design with the same name already exists, ask: "A design called '<name>' already exists in the library. Overwrite it?"

### Copying to Project

When the user says "use the <name> design" in any project:

1. Read files from `~/.claude/designs/<name>/`
2. Create `.claude/design/` in the current project: `mkdir -p .claude/design`
3. Copy all files (DESIGN.md, tailwind-theme.css, accessibility-report.md, preview.png)
4. Confirm: "Copied <name> design to `.claude/design/`. The tailwind-theme.css is ready to import into your stylesheet."

## Next Steps

After extraction completes, suggest these follow-up actions to the user:

1. **"Validate the theme"** — invoke `design-system-standards` to check that the generated tailwind-theme.css meets all token conventions (semantic naming, fluid spacing, contrast pairs documented)
2. **"Build components from this design"** — invoke `frontend-design` to create UI components (buttons, cards, forms, nav) that match the extracted design system. It will read `.claude/design/DESIGN.md` automatically if the design was copied to the project.
3. **"Check Tailwind v4 patterns"** — invoke `tailwind-patterns` to verify the `@theme` block follows current v4 best practices (CSS-first config, container queries, modern utility patterns)

Include these as a bulleted list in your final message to the user after saving the files.

## See Also

- **design-auditor** — audit an existing project's design system instead of extracting from a URL
- **design-system-standards** — token conventions and Tailwind v4 patterns these files follow
- **frontend-design** — build production-grade UI components from a DESIGN.md
- **tailwind-patterns** — Tailwind v4 best practices and modern patterns
