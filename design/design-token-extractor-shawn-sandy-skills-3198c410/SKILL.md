---
name: design-token-extractor
description: Extracts design tokens from images and generates CSS custom properties, atomic utility classes (Tailwind-style), and platform-specific formats following W3C standards and modern CSS best practices.
version: 0.2.0
license: Complete terms in LICENSE.txt
---

## Overview

This skill automates the extraction of design tokens from images and mockups, converting them into standards-compliant formats including W3C DTCG JSON, CSS custom properties, SCSS variables, and comprehensive atomic utility classes (Tailwind-style). It generates modern, accessible design systems with cascade layers, container queries, responsive variants, and state management.

**New in v0.2.0:** Comprehensive atomic utility class generation with Tailwind-style naming, including color, spacing (with logical properties), typography, and layout utilities, plus full support for container query variants, state variants (hover/focus/active), and dark mode.

## When to Use This Skill

Invoke this skill when you need to:

- Extract design tokens from UI mockups, screenshots, or design files
- Convert visual design elements into CSS custom properties or SCSS variables
- **Generate atomic utility classes (Tailwind-style) from design tokens**
- **Create utility-first design systems with comprehensive responsive and state variants**
- Generate W3C DTCG-compliant token JSON from design artifacts
- Create cross-platform design tokens (web, iOS, Android)
- Validate existing tokens against W3C specifications
- Implement design systems with modern CSS features (cascade layers, container queries, logical properties)

## Workflow

### 1. Image Analysis and Token Identification

**Action:** When the user provides an image or design mockup, analyze and identify token categories.

**Token Categories:**

- Colors (primary, secondary, neutral palettes with semantic roles)
- Typography (font families, sizes, weights, line-heights using scale ratios)
- Spacing (mathematical progression scales: 0.25rem, 0.5rem, 1rem, 1.5rem, 2rem)
- Dimensions (border radius, shadows, dimensional properties)
- Motion (animation durations and easing functions if present)

### 2. Token Extraction

**Action:** Extract tokens following W3C Design Tokens Community Group standards.

**Extraction Process:**

- Use semantic, hierarchical naming with kebab-case
- Apply mathematical progressions for scales (1.25x, 1.5x, 2x)
- Structure using cascade layers (`@layer reset`, `tokens`, `components`, `utilities`)
- Ensure WCAG 2.2 compliance (4.5:1 contrast for normal text, 3:1 for large text)

### 3. Format Selection

**Prompt for Output Format:**

Ask the user which format to generate (if not specified):

- **W3C JSON** - Design Tokens Community Group specification format
- **CSS** - CSS custom properties with cascade layers
- **CSS (Full)** - CSS with cascade layers + generated atomic utilities
- **Utilities** - Standalone atomic utility classes (Tailwind-style)
- **SCSS** - SCSS variables and mixins
- **iOS** - Swift/UIKit format
- **Android** - Kotlin/XML resources

**New Utility Formats:**

- `utilities` - Comprehensive Tailwind-style atomic utilities (standalone file)
- `css-layers-full` - Complete design system with tokens AND generated utilities

Both utility formats include:
- Color utilities (text, bg, border, fill, stroke)
- Spacing utilities with logical properties (padding, margin, gap)
- Typography utilities (font family, size, weight, line-height)
- Layout utilities (border-radius, shadows, dimensions)
- Container query variants (sm, md, lg, xl breakpoints)
- State variants (hover, focus, active)
- Dark mode variants
- Accessibility variants (reduced-motion, forced-colors)

### 4. Output Generation

**Action:** Generate output using appropriate templates with variable substitution.

**Default Output Location:** `src/styles/` (unless the user specifies a different path)

**Templates Available:**

- `templates/w3c-tokens.template.json` - W3C DTCG format
- `templates/css-variables.template.css` - CSS custom properties
- `templates/css-layers.template.css` - Cascade layers implementation
- `templates/documentation.template.md` - Token documentation

**Variable Substitution:**

- `{{TOKEN_NAME}}` - Token identifier
- `{{TOKEN_VALUE}}` - Token value
- `{{TOKEN_TYPE}}` - Token type (color, dimension, etc.)
- `{{TOKEN_DESCRIPTION}}` - Token description
- `{{COLOR_PRIMARY_500}}`, `{{SPACING_MD}}`, etc. - Specific token values

### 5. Validation

**Action:** Validate generated tokens against W3C DTCG specification.

**Execute Validation Script:**

```bash
python scripts/validate_tokens.py --input tokens.json [--strict]
```

**Validation Checks:**

- Required properties (`$value`, `$type`) present
- Valid token types (color, dimension, fontFamily, etc.)
- Proper alias token references
- Accessibility compliance (contrast ratios, motion preferences)

**Error Handling:**

- Report specific validation errors
- Suggest corrections
- Re-validate after fixes

### 6. Load References (As Needed)

**Action:** Load reference documentation only when detailed specifications are needed.

**When to Load:**

- User asks about W3C token format or validation errors → load `references/w3c-dtcg-spec.md`
- User needs CSS best practices or modern features → load `references/css-standards.md`
- User asks about accessibility or WCAG compliance → load `references/accessibility-guidelines.md`

## Token Extraction Guidelines

### Extract Design Elements

Follow W3C token categories:

- **Colors**: Primary, secondary, neutral palettes with semantic roles
- **Typography**: Font families, sizes, weights, line-heights using scale ratios (1.25x, 1.5x)
- **Spacing**: Mathematical progression scales (0.25rem, 0.5rem, 1rem, 1.5rem, 2rem)
- **Dimensions**: Border radius, shadows, and other dimensional properties
- **Motion**: Animation durations and easing functions if present

### Token Organization

Structure using cascade layers (`@layer reset`, `tokens`, `components`, `utilities`).
For detailed CSS standards, load `references/css-standards.md`.

### Responsive Tokens

- Use container query units (cqi, cqb) for intrinsic sizing
- Create fluid typography: `clamp(1rem, 2.5cqi, 1.5rem)`
- Define breakpoint-agnostic spacing scales

### Accessibility Requirements

Ensure WCAG 2.2 compliance:

- 4.5:1 contrast for normal text, 3:1 for large text
- Focus indicators meet 3:1 contrast against adjacent colors
- Motion tokens respect `prefers-reduced-motion`

For details, load `references/accessibility-guidelines.md`.

## Using Bundled Resources

### Scripts

Execute Python scripts for deterministic tasks. **All output defaults to `src/styles/` unless otherwise specified.**

**extract_tokens.py** - Extract tokens from image analysis

```bash
# Default output to src/styles/tokens.json
python scripts/extract_tokens.py --input-image <path> --output src/styles/tokens.json
```

**transform_tokens.py** - Transform between formats (JSON → CSS/SCSS/iOS/Android/Utilities)

```bash
# Generate CSS custom properties (default to src/styles/)
python scripts/transform_tokens.py --input tokens.json --format css --output src/styles/tokens.css

# Generate standalone atomic utilities (default to src/styles/)
python scripts/transform_tokens.py --input tokens.json --format utilities --output src/styles/utilities.css

# Generate complete design system (tokens + utilities, default to src/styles/)
python scripts/transform_tokens.py --input tokens.json --format css-layers-full --output src/styles/design-system.css
```

**generate_utilities.py** - Generate atomic utility classes from tokens

```bash
# Generate utilities with default configuration (default to src/styles/)
python scripts/generate_utilities.py --input tokens.json --output src/styles/utilities.css

# Generate utilities with custom configuration
python scripts/generate_utilities.py --input tokens.json --output src/styles/utilities.css --config config.json
```

**validate_tokens.py** - Validate against W3C DTCG specification

```bash
python scripts/validate_tokens.py --input tokens.json [--strict]
```

### Templates

Generate consistent output using templates with `{{VARIABLE}}` substitution:

- `templates/w3c-tokens.template.json` - W3C DTCG format
- `templates/css-variables.template.css` - CSS custom properties
- `templates/css-layers.template.css` - Cascade layers implementation
- `templates/documentation.template.md` - Token documentation

Common variables: `{{TOKEN_NAME}}`, `{{TOKEN_VALUE}}`, `{{TOKEN_TYPE}}`, `{{TOKEN_DESCRIPTION}}`, `{{COLOR_PRIMARY_500}}`, `{{SPACING_MD}}`, etc.

### References

Load reference files when detailed information is needed:

- `references/w3c-dtcg-spec.md` - W3C Design Tokens specification (~1k words)
  - Search for: `$value`, `$type`, `composite tokens`, `alias tokens`
- `references/css-standards.md` - Modern CSS features (~1.3k words)
  - Search for: `@layer`, `@container`, `logical properties`, `cascade layers`
- `references/accessibility-guidelines.md` - WCAG 2.2 compliance (~1.3k words)
  - Search for: `contrast ratio`, `focus indicators`, `prefers-reduced-motion`

**When to load references:**

- User asks about W3C token format or validation errors → load `w3c-dtcg-spec.md`
- User needs CSS best practices or modern features → load `css-standards.md`
- User asks about accessibility or WCAG compliance → load `accessibility-guidelines.md`

## Atomic Utility Class Generation

### Overview

The skill generates comprehensive Tailwind-style atomic utility classes from extracted design tokens. These utilities enable rapid prototyping and utility-first development with full support for responsive variants, state management, and accessibility.

### Generated Utility Categories

#### Color Utilities

**Text Colors:**
```css
.text-primary-500 { color: var(--color-primary-500); }
.text-neutral-900 { color: var(--color-neutral-900); }
```

**Background Colors:**
```css
.bg-surface-elevated { background-color: var(--color-surface-elevated); }
.bg-primary-500 { background-color: var(--color-primary-500); }
```

**Border Colors:**
```css
.border-accent-600 { border-color: var(--color-accent-600); }
```

**SVG Colors:**
```css
.fill-primary-500 { fill: var(--color-primary-500); }
.stroke-neutral-900 { stroke: var(--color-neutral-900); }
```

#### Spacing Utilities (Logical Properties)

**Padding:**
```css
.p-md { padding: var(--spacing-scale-md); }
.px-lg { padding-inline: var(--spacing-scale-lg); }  /* horizontal */
.py-sm { padding-block: var(--spacing-scale-sm); }   /* vertical */
.pt-xs { padding-block-start: var(--spacing-scale-xs); }  /* top */
```

**Margin:**
```css
.m-md { margin: var(--spacing-scale-md); }
.mx-auto { margin-inline: auto; }  /* center horizontally */
.my-lg { margin-block: var(--spacing-scale-lg); }
```

**Gap (for Grid/Flexbox):**
```css
.gap-md { gap: var(--spacing-scale-md); }
.gap-x-sm { column-gap: var(--spacing-scale-sm); }
.gap-y-lg { row-gap: var(--spacing-scale-lg); }
```

#### Typography Utilities

**Font Family:**
```css
.font-display { font-family: var(--font-family-display); }
.font-body { font-family: var(--font-family-body); }
```

**Font Size:**
```css
.text-xl { font-size: var(--font-size-xl); }
.text-base { font-size: var(--font-size-base); }
```

**Font Weight:**
```css
.font-bold { font-weight: var(--font-weight-bold); }
.font-medium { font-weight: var(--font-weight-medium); }
```

**Line Height:**
```css
.leading-tight { line-height: var(--line-height-tight); }
.leading-relaxed { line-height: var(--line-height-relaxed); }
```

#### Layout Utilities

**Border Radius:**
```css
.rounded-md { border-radius: var(--border-radius-md); }
.rounded-full { border-radius: var(--border-radius-full); }
```

**Shadows:**
```css
.shadow-md { box-shadow: var(--shadow-md); }
.shadow-elevated { box-shadow: var(--shadow-elevated); }
```

### Utility Variants

#### Container Query Variants

Apply utilities at specific container sizes (responsive design):

```html
<div class="text-base md:text-lg lg:text-xl">
  Text that grows with container size
</div>

<div class="p-sm md:p-md lg:p-lg">
  Padding that increases at larger container sizes
</div>
```

**Breakpoints:**
- `sm:` - 640px
- `md:` - 768px
- `lg:` - 1024px
- `xl:` - 1280px

#### State Variants

**Hover:**
```html
<button class="bg-primary-500 hover:bg-primary-600">
  Button with hover state
</button>

<a class="text-neutral-700 hover:text-primary-500">
  Link with hover color
</a>
```

**Focus:**
```html
<input class="outline-neutral-300 focus:outline-primary-500">

<button class="focus:bg-primary-700">
  Button with focus state
</button>
```

**Active:**
```html
<button class="bg-primary-500 active:bg-primary-700">
  Button with active/pressed state
</button>
```

#### Dark Mode Variants

```html
<div class="bg-white dark:bg-neutral-900
            text-neutral-900 dark:text-neutral-100">
  Content that adapts to dark mode
</div>

<p class="text-neutral-700 dark:text-neutral-300">
  Body text with dark mode support
</p>
```

### Usage Examples

#### Utility-First Card Component

```html
<article class="bg-white dark:bg-neutral-800
                p-lg rounded-lg shadow-md
                border border-neutral-200 dark:border-neutral-700">
  <h2 class="font-display text-2xl font-bold
             text-neutral-900 dark:text-white
             mb-md">
    Card Title
  </h2>
  <p class="text-base leading-relaxed
            text-neutral-700 dark:text-neutral-300
            mb-lg">
    Card content with proper spacing and typography.
  </p>
  <button class="px-lg py-md
                 bg-primary-600 hover:bg-primary-700 active:scale-95
                 text-white rounded-sm font-semibold
                 focus:outline-accent-500">
    Action Button
  </button>
</article>
```

#### Responsive Grid Layout

```html
<div class="grid gap-md md:gap-lg
            grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  <div class="p-md bg-neutral-50 dark:bg-neutral-800 rounded-md">
    Grid Item 1
  </div>
  <div class="p-md bg-neutral-50 dark:bg-neutral-800 rounded-md">
    Grid Item 2
  </div>
  <div class="p-md bg-neutral-50 dark:bg-neutral-800 rounded-md">
    Grid Item 3
  </div>
</div>
```

### Configuration Options

Customize utility generation with a config JSON file:

```json
{
  "categories": ["colors", "spacing", "typography", "layout"],
  "variants": ["container", "state", "dark-mode"],
  "prefix": ""
}
```

**Configuration Properties:**
- `categories` - Which utility types to generate (array)
- `variants` - Which variants to include (array)
- `prefix` - Optional prefix for all utilities (string, e.g., "tw-")

**Example with custom configuration:**
```bash
python scripts/generate_utilities.py \
  --input tokens.json \
  --output utilities.css \
  --config custom-config.json
```

### Accessibility Features

All generated utilities include automatic accessibility support:

- **Reduced Motion**: Respects `prefers-reduced-motion` preference
- **Forced Colors**: Adapts to high contrast mode
- **Dark Mode**: Supports `prefers-color-scheme: dark`
- **Logical Properties**: Better i18n support (RTL languages)
- **Focus Indicators**: WCAG-compliant focus states

### Modern CSS Features

Generated utilities leverage modern CSS:

- **Cascade Layers**: Organized with `@layer utilities.colors`, etc.
- **Container Queries**: Responsive variants based on container size
- **Logical Properties**: `padding-inline`, `margin-block` for better i18n
- **CSS Custom Properties**: All values reference design tokens

### Browser Support

**Target Browsers:**
- Chrome/Edge: 88+ (container queries)
- Firefox: 110+
- Safari: 16+

**Progressive Enhancement:**
- Base utilities work in all browsers with custom property support
- Container query variants gracefully degrade on older browsers

## Decision Tree

```text
User provides image/mockup
    ↓
Extract tokens (colors, typography, spacing, dimensions, motion)
    ↓
Format specified?
    ├─ No  → Ask: W3C JSON, CSS, CSS (Full), Utilities, SCSS, iOS, Android?
    └─ Yes → Continue
        ↓
Utility generation requested?
    ├─ Yes → Generate utilities (standalone or with tokens)
    │         ├─ Format: utilities → Standalone atomic utilities
    │         └─ Format: css-layers-full → Tokens + utilities
    └─ No  → Standard token transformation
        ↓
Select template and generate output to src/styles/ (or user-specified path)
    ↓
Validate with validate_tokens.py (if JSON format)
    ↓
Validation passes?
    ├─ Yes → Deliver output with documentation
    └─ No  → Fix errors, re-validate
```

## Naming Conventions

Use semantic, hierarchical naming with kebab-case:

- **Colors**: `--color-{role}-{variant}` → `--color-primary-500`, `--color-text-primary`
- **Typography**: `--font-{property}-{size}` → `--font-size-lg`, `--font-weight-bold`
- **Spacing**: `--spacing-{scale}-{size}` → `--spacing-scale-md`, `--spacing-fluid-sm`
- **Dimensions**: `--{element}-{property}` → `--border-radius-sm`, `--shadow-md`

## Best Practices

1. **Semantic naming** - Use role-based names (primary/secondary) over descriptive (blue/red)
2. **Scale consistency** - Use mathematical progressions (1.25x, 1.5x, 2x)
3. **Cross-platform** - Ensure tokens work across web, mobile, and design tools
4. **Accessibility first** - Validate contrast ratios and motion preferences
5. **Modern CSS** - Leverage cascade layers, container queries, logical properties
6. **W3C compliance** - Follow Design Tokens Community Group specification

Generate modern, standards-compliant tokens that balance cutting-edge CSS features with cross-platform compatibility and accessibility.
