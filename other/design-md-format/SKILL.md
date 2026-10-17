---
name: design-md-format
description: Create and validate DESIGN.md files that give AI coding agents structured understanding of design systems through machine-readable tokens and human-readable rationale.
triggers:
  - create a design.md file for our design system
  - validate this design.md against the spec
  - export design tokens to tailwind config
  - lint our design system file
  - compare two versions of our design system
  - generate design.md from our brand guidelines
  - check wcag contrast ratios in design tokens
  - convert design.md to dtcg format
---

# DESIGN.md Format Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

DESIGN.md is a format specification for describing visual identity to coding agents. It combines machine-readable design tokens (YAML front matter) with human-readable design rationale (markdown prose), giving agents persistent, structured understanding of design systems.

## Installation

```bash
npm install @google/design.md
```

For direct CLI usage without installation:

```bash
npx @google/design.md lint DESIGN.md
```

**Windows note**: When using the CLI in `package.json` scripts on Windows, use the `designmd` alias instead of `design.md` to avoid file association issues:

```json
{
  "scripts": {
    "design:lint": "designmd lint DESIGN.md"
  }
}
```

## File Structure

A DESIGN.md file has two layers:

1. **YAML front matter** — Machine-readable tokens (colors, typography, spacing, etc.)
2. **Markdown body** — Human-readable rationale organized into specific sections

```md
---
name: Heritage
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
typography:
  h1:
    fontFamily: Public Sans
    fontSize: 3rem
  body-md:
    fontFamily: Public Sans
    fontSize: 1rem
rounded:
  sm: 4px
  md: 8px
spacing:
  sm: 8px
  md: 16px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "#ffffff"
    rounded: "{rounded.sm}"
    padding: 12px
---

## Overview

Architectural Minimalism meets Journalistic Gravitas.

## Colors

- **Primary (#1A1C1E):** Deep ink for headlines and core text.
- **Tertiary (#B8422E):** "Boston Clay" — interaction driver.
```

## Creating a DESIGN.md File

### Complete Token Schema

```yaml
version: <string>          # optional, current: "alpha"
name: <string>             # required
description: <string>      # optional
colors:
  <token-name>: <Color>    # "#" + hex (sRGB)
typography:
  <token-name>: <Typography>
rounded:
  <scale-level>: <Dimension>
spacing:
  <scale-level>: <Dimension | number>
components:
  <component-name>:
    <property>: <value | token reference>
```

### Token Types

**Color**: Hex format with `#` prefix
```yaml
colors:
  primary: "#1A1C1E"
  accent: "#B8422E"
  on-primary: "#FFFFFF"
```

**Typography**: Object with font properties
```yaml
typography:
  h1:
    fontFamily: Public Sans
    fontSize: 3rem
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: -0.02em
  body-md:
    fontFamily: Public Sans
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.5
```

**Dimension**: Number + unit (`px`, `em`, `rem`)
```yaml
rounded:
  sm: 4px
  md: 8px
  lg: 16px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
```

**Token Reference**: `{path.to.token}`
```yaml
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
    rounded: "{rounded.sm}"
```

### Component Tokens

Valid component properties:
- `backgroundColor`
- `textColor`
- `typography`
- `rounded`
- `padding`
- `size`
- `height`
- `width`

```yaml
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "#ffffff"
    typography: "{typography.label-caps}"
    rounded: "{rounded.sm}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.tertiary-container}"
  card:
    backgroundColor: "{colors.neutral}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
```

### Section Order

Markdown sections use `##` headings and must appear in this order (all optional):

1. **Overview** (or "Brand & Style")
2. **Colors**
3. **Typography**
4. **Layout** (or "Layout & Spacing")
5. **Elevation & Depth** (or "Elevation")
6. **Shapes**
7. **Components**
8. **Do's and Don'ts**

```md
## Overview

Brief description of the design philosophy.

## Colors

Rationale for each color token and when to use it.

- **Primary (#1A1C1E):** Deep ink for headlines
- **Tertiary (#B8422E):** Interaction driver

## Typography

Font selection rationale and hierarchy guidance.

## Components

How to apply component tokens in context.
```

## CLI Commands

### Lint

Validate a DESIGN.md file for structural correctness, broken references, and WCAG contrast issues:

```bash
# Validate from file
npx @google/design.md lint DESIGN.md

# From stdin
cat DESIGN.md | npx @google/design.md lint -

# Specify output format (only json currently)
npx @google/design.md lint --format json DESIGN.md
```

**Output**: JSON with findings array and summary
```json
{
  "findings": [
    {
      "severity": "warning",
      "path": "components.button-primary",
      "message": "textColor (#ffffff) on backgroundColor (#1A1C1E) has contrast ratio 15.42:1 — passes WCAG AA."
    }
  ],
  "summary": { "errors": 0, "warnings": 1, "info": 1 }
}
```

**Exit codes**:
- `0`: No errors
- `1`: Errors found

### Diff

Compare two DESIGN.md versions to detect token changes and regressions:

```bash
npx @google/design.md diff DESIGN.md DESIGN-v2.md
npx @google/design.md diff --format json old.md new.md
```

**Output**: Token-level changes
```json
{
  "tokens": {
    "colors": { "added": ["accent"], "removed": [], "modified": ["tertiary"] },
    "typography": { "added": [], "removed": [], "modified": [] }
  },
  "regression": false
}
```

**Exit codes**:
- `0`: No regressions
- `1`: Regressions detected (more errors/warnings in "after")

### Export

Convert DESIGN.md tokens to other formats:

```bash
# Tailwind v3 JSON config
npx @google/design.md export --format json-tailwind DESIGN.md > tailwind.theme.json
npx @google/design.md export --format tailwind DESIGN.md > tailwind.theme.json  # alias

# Tailwind v4 CSS theme
npx @google/design.md export --format css-tailwind DESIGN.md > theme.css

# W3C Design Tokens Format (DTCG)
npx @google/design.md export --format dtcg DESIGN.md > tokens.json

# From stdin
cat DESIGN.md | npx @google/design.md export --format dtcg - > tokens.json
```

**Tailwind v3 JSON output** (`json-tailwind`):
```json
{
  "colors": {
    "primary": "#1A1C1E",
    "secondary": "#6C7278",
    "tertiary": "#B8422E"
  },
  "fontFamily": {
    "sans": ["Public Sans", "sans-serif"]
  },
  "fontSize": {
    "h1": "3rem",
    "body-md": "1rem"
  },
  "borderRadius": {
    "sm": "4px",
    "md": "8px"
  },
  "spacing": {
    "sm": "8px",
    "md": "16px"
  }
}
```

**Tailwind v4 CSS output** (`css-tailwind`):
```css
@theme {
  --color-primary: #1A1C1E;
  --color-secondary: #6C7278;
  --color-tertiary: #B8422E;
  --font-sans: "Public Sans", sans-serif;
  --text-h1: 3rem;
  --text-body-md: 1rem;
  --radius-sm: 4px;
  --radius-md: 8px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
}
```

### Spec

Output the DESIGN.md specification (useful for agent prompts):

```bash
# Full spec
npx @google/design.md spec

# Spec + linting rules
npx @google/design.md spec --rules

# Only linting rules
npx @google/design.md spec --rules-only

# JSON format
npx @google/design.md spec --rules-only --format json
```

## Programmatic API

### Linting

```typescript
import { lint } from '@google/design.md/linter';

const markdownString = `
---
name: MyDesign
colors:
  primary: "#1A1C1E"
components:
  button:
    backgroundColor: "{colors.primary}"
    textColor: "#ffffff"
---

## Overview
Modern design system.
`;

const report = lint(markdownString);

console.log(report.findings);
// [
//   {
//     severity: 'warning',
//     path: 'components.button',
//     message: 'textColor (#ffffff) on backgroundColor (#1A1C1E) has contrast ratio 15.42:1 — passes WCAG AA.'
//   }
// ]

console.log(report.summary);
// { errors: 0, warnings: 1, info: 1 }

console.log(report.designSystem);
// Parsed DesignSystemState object
```

### Parsing and Validation

```typescript
import { lint, type Finding } from '@google/design.md/linter';

function validateDesignFile(content: string): boolean {
  const report = lint(content);
  
  const hasErrors = report.findings.some((f: Finding) => f.severity === 'error');
  
  if (hasErrors) {
    console.error('Validation failed:');
    report.findings
      .filter((f: Finding) => f.severity === 'error')
      .forEach((f: Finding) => console.error(`  ${f.path}: ${f.message}`));
    return false;
  }
  
  return true;
}
```

## Common Patterns

### Creating a Design System from Scratch

```md
---
version: alpha
name: ProductName
description: Modern SaaS design system
colors:
  primary: "#2563eb"
  secondary: "#64748b"
  tertiary: "#0ea5e9"
  neutral: "#f8fafc"
  on-primary: "#ffffff"
  on-tertiary: "#ffffff"
typography:
  h1:
    fontFamily: Inter
    fontSize: 2.5rem
    fontWeight: 700
    lineHeight: 1.2
  h2:
    fontFamily: Inter
    fontSize: 2rem
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 500
rounded:
  sm: 4px
  md: 8px
  lg: 12px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  button-primary-hover:
    backgroundColor: "#1d4ed8"
  card:
    backgroundColor: "{colors.neutral}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
  input:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm}"
---

## Overview

Clean, modern SaaS interface prioritizing readability and trust.

## Colors

- **Primary (#2563eb):** Brand blue for primary actions
- **Secondary (#64748b):** Slate for secondary text and borders
- **Tertiary (#0ea5e9):** Sky blue for links and highlights
- **Neutral (#f8fafc):** Near-white background

## Typography

Single font family (Inter) for consistency. Weight and size establish hierarchy.

## Components

All interactive elements use `button-primary` tokens. Cards use `card` tokens.
```

### Integrating with Tailwind

After exporting to Tailwind format:

```bash
npx @google/design.md export --format json-tailwind DESIGN.md > design-tokens.json
```

**Tailwind v3 config**:
```javascript
// tailwind.config.js
const designTokens = require('./design-tokens.json');

module.exports = {
  theme: {
    extend: designTokens
  }
};
```

**Tailwind v4 with CSS**:
```bash
npx @google/design.md export --format css-tailwind DESIGN.md > src/theme.css
```

```css
/* src/styles.css */
@import "./theme.css";
@import "tailwindcss";
```

### Token References Pattern

Always reference tokens rather than duplicating values:

```yaml
# ✅ Good - uses references
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
  button-secondary:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"

# ❌ Bad - duplicates values
components:
  button-primary:
    backgroundColor: "#2563eb"
    textColor: "#ffffff"
    rounded: 8px
  button-secondary:
    backgroundColor: "#64748b"
    textColor: "#ffffff"
    rounded: 8px
```

### Variant Pattern for Component States

```yaml
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    padding: 12px 24px
  button-primary-hover:
    backgroundColor: "#1d4ed8"
  button-primary-active:
    backgroundColor: "#1e40af"
  button-primary-disabled:
    backgroundColor: "{colors.secondary}"
    textColor: "#94a3b8"
```

## Linting Rules Reference

| Rule | Severity | Description |
|------|----------|-------------|
| `broken-ref` | error | Token reference doesn't resolve (e.g., `{colors.missing}`) |
| `missing-primary` | warning | No `primary` color defined — agents will auto-generate |
| `contrast-ratio` | warning | Component backgroundColor/textColor below WCAG AA (4.5:1) |
| `orphaned-tokens` | warning | Color token defined but never referenced |
| `token-summary` | info | Summary of token counts per section |
| `missing-sections` | info | Optional sections absent when other tokens exist |
| `missing-typography` | warning | Colors defined but no typography tokens |
| `section-order` | warning | Sections appear out of canonical order |

## Troubleshooting

### `npm error ENOVERSIONS`

**Problem**: `No versions available for @google/design.md`

**Cause**: npm not querying public registry (custom registry in `.npmrc`, corporate mirror, misconfigured scope)

**Solution**:
```bash
# Check current registry
npm config get registry

# Should be: https://registry.npmjs.org/

# Clear cache and retry
npm cache clean --force
npm install @google/design.md
```

### Broken Token References

**Problem**: `broken-ref` error for `{colors.accent}`

**Cause**: Token doesn't exist in YAML front matter

**Solution**:
```yaml
colors:
  accent: "#0ea5e9"  # Add the missing token
```

Or update the reference:
```yaml
components:
  button:
    backgroundColor: "{colors.primary}"  # Use existing token
```

### WCAG Contrast Failures

**Problem**: `contrast-ratio` warning for component

**Solution**: Adjust colors to meet 4.5:1 minimum:
```yaml
# Before (low contrast)
components:
  button:
    backgroundColor: "#e0e0e0"
    textColor: "#ffffff"

# After (high contrast)
components:
  button:
    backgroundColor: "#1A1C1E"
    textColor: "#ffffff"
```

Or define explicit on-* colors:
```yaml
colors:
  primary: "#2563eb"
  on-primary: "#ffffff"  # Guaranteed high contrast
components:
  button:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
```

### Section Order Warnings

**Problem**: `section-order` warning

**Cause**: Sections out of canonical order

**Solution**: Reorder markdown sections:
```md
## Overview
...

## Colors
...

## Typography
...

## Components
...
```

### Windows CLI Issues

**Problem**: CLI not executing in `package.json` scripts on Windows

**Solution**: Use `designmd` alias instead of `design.md`:
```json
{
  "scripts": {
    "lint": "designmd lint DESIGN.md",
    "export": "designmd export --format tailwind DESIGN.md > tokens.json"
  }
}
```

## Best Practices

1. **Always define `primary` color** — Prevents agent auto-generation
2. **Use token references** — Single source of truth for design changes
3. **Include typography early** — Prevents agents from using default fonts
4. **Write prose rationale** — Explains *why* tokens exist and *how* to apply them
5. **Validate before committing** — Run `lint` in CI/CD pipeline
6. **Version your DESIGN.md** — Track design evolution with `diff`
7. **Define component variants explicitly** — `button-primary-hover`, not just `button-primary`
8. **Check contrast ratios** — Linter catches WCAG issues automatically

## Integration Examples

### CI/CD Validation

```yaml
# .github/workflows/design.yml
name: Validate Design System
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npx @google/design.md lint DESIGN.md
```

### Pre-commit Hook

```json
{
  "husky": {
    "hooks": {
      "pre-commit": "npx @google/design.md lint DESIGN.md"
    }
  }
}
```

### Build-time Token Export

```json
{
  "scripts": {
    "prebuild": "designmd export --format tailwind DESIGN.md > src/design-tokens.json",
    "build": "vite build"
  }
}
```
