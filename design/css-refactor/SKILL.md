---
name: css-refactor
description: >-
  Upgrade legacy CSS to modern standards. Scans stylesheets for outdated
  patterns (floats, clearfix, vendor prefixes, old flexbox syntax, px media
  queries, @import, !important abuse) and replaces them with modern equivalents.
  Introduces cascade layers, extracts design tokens, and consolidates
  redundancy. Use when refactoring CSS, modernizing stylesheets, upgrading
  legacy code, removing vendor prefixes, or replacing floats with grid/flexbox.
disable-model-invocation: true
license: MIT
---

# css-refactor — Upgrade Legacy CSS

You are a CSS modernization specialist. Your job is to scan CSS files, identify legacy patterns, and replace them with modern equivalents. Always show before/after diffs so the user can review changes.

For the full modern pattern catalog, see the css-expert skill's [modern-patterns.md](../css-expert/references/modern-patterns.md). For the anti-pattern reference, see [anti-patterns.md](../css-expert/references/anti-patterns.md).

## Workflow

Copy this checklist and track progress:

```
Refactor Progress:
- [ ] Step 1: Scan — identify all CSS files in scope
- [ ] Step 2: Audit — catalog legacy patterns found
- [ ] Step 3: Prioritize — rank issues by impact
- [ ] Step 4: Refactor — apply modern replacements
- [ ] Step 5: Extract — pull design tokens into custom properties
- [ ] Step 6: Layer — introduce @layer architecture
- [ ] Step 7: Consolidate — remove redundancy
- [ ] Step 8: Review — present before/after diffs
```

## Step 1: Scan

Find all CSS files in scope. If the user hasn't specified files, search for `**/*.css` and list them with line counts. Flag the largest files first — they typically contain the most legacy code.

## Step 2: Audit Legacy Patterns

Scan every CSS file for the following categories. Report a summary table:

```
| Pattern              | Count | Files           | Severity |
|----------------------|-------|-----------------|----------|
| float layout         |     3 | layout.css:12   | high     |
| clearfix             |     2 | layout.css:45   | high     |
| !important           |    14 | *.css           | high     |
| vendor prefixes      |     8 | components.css  | medium   |
| px media queries     |     5 | responsive.css  | medium   |
| @import              |     2 | main.css:1-2    | medium   |
| old flexbox syntax   |     3 | nav.css         | medium   |
| hardcoded colors     |    22 | *.css           | low      |
| px font sizes        |    11 | typography.css  | low      |
| ID selectors         |     4 | header.css      | low      |
```

### What to Look For

**High severity — fix first:**

- `float: left/right` used for layout (not text wrapping)
- `.clearfix` or `clear: both` hacks
- `!important` (except on utility classes or third-party overrides)
- `@import url(...)` in CSS files
- Deeply nested selectors (4+ levels)

**Medium severity:**

- Vendor prefixes that are no longer needed: `-webkit-`, `-moz-`, `-ms-`
  - Check against [browser-compat.md](../css-expert/references/browser-compat.md) before removing
  - Keep `-webkit-appearance` and other still-needed prefixes
- `@media (max-width: 768px)` — px-based media queries
- Old flexbox: `display: -webkit-flex`, `display: -ms-flexbox`, `-webkit-box`
- `box-sizing` applied per-element instead of with a reset

**Low severity:**

- Hardcoded hex/rgb colors instead of custom properties
- `px` for font sizes instead of `rem`/`clamp()`
- `#id` selectors used for styling
- Physical properties (`margin-left`) instead of logical (`margin-inline-start`)
- Magic numbers without explanation

## Step 3: Prioritize

Rank by impact:

1. **Breaking patterns** — floats, clearfix (affect layout correctness)
2. **Specificity issues** — `!important`, ID selectors (affect maintainability)
3. **Architecture** — `@import`, no layers (affect performance and scale)
4. **Modernization** — vendor prefixes, px units, old color syntax (affect code quality)

## Step 4: Refactor Patterns

Apply these replacements. Always show before/after.

### Float layouts → Grid or Flexbox

```css
/* BEFORE */
.sidebar { float: left; width: 250px; }
.main { margin-left: 270px; }
.clearfix::after { content: ""; display: table; clear: both; }

/* AFTER */
.layout {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: var(--space-m);
}
```

### !important → Cascade layers or :where()

```css
/* BEFORE */
.button { background: blue !important; }
.nav .button { background: green !important; }

/* AFTER */
@layer components {
  .button { background: var(--_bg, var(--color-primary)); }
}
.nav .button { --_bg: var(--color-nav-action); }
```

### Vendor prefixes → Unprefixed

```css
/* BEFORE */
.flex { display: -webkit-flex; display: -ms-flexbox; display: flex; }
.transform { -webkit-transform: rotate(45deg); transform: rotate(45deg); }

/* AFTER */
.flex { display: flex; }
.transform { transform: rotate(45deg); }
```

### px media queries → em

```css
/* BEFORE */
@media (max-width: 768px) { ... }
@media (min-width: 1024px) { ... }

/* AFTER */
@media (max-width: 48em) { ... }
@media (min-width: 64em) { ... }
```

Conversion: divide px by 16 → em.

### @import → HTML link or @layer

```css
/* BEFORE — in CSS */
@import url("reset.css");
@import url("components.css");

/* AFTER — in HTML */
/* <link rel="stylesheet" href="reset.css"> */
/* <link rel="stylesheet" href="components.css"> */

/* OR — if consolidating into one file, use @layer */
@layer reset { /* contents of reset.css */ }
```

### Old flexbox syntax

```css
/* BEFORE */
.box { display: -webkit-box; -webkit-box-orient: horizontal; -webkit-box-pack: center; }

/* AFTER */
.box { display: flex; justify-content: center; }
```

### Hex/RGB colors → oklch

```css
/* BEFORE */
:root { --primary: #3366ff; --danger: rgb(220, 53, 69); }

/* AFTER */
:root { --primary: oklch(55% 0.25 260); --danger: oklch(55% 0.22 25); }
```

### px font sizes → clamp/rem

```css
/* BEFORE */
h1 { font-size: 32px; }
body { font-size: 16px; }

/* AFTER */
h1 { font-size: clamp(1.5rem, 1rem + 2vw, 3rem); }
body { font-size: clamp(1rem, 0.875rem + 0.5vw, 1.125rem); }
```

### Physical → Logical properties

```css
/* BEFORE */
.element { margin-left: 1rem; padding-right: 2rem; text-align: left; }

/* AFTER */
.element { margin-inline-start: 1rem; padding-inline-end: 2rem; text-align: start; }
```

## Step 5: Extract Design Tokens

Find repeated values and extract into custom properties using a three-layer architecture:

```css
/* Layer 1: Primitive tokens (raw values) */
:root {
  --blue-500: oklch(55% 0.25 250);
  --gray-200: oklch(90% 0.01 250);
  --radius-m: 0.5rem;
}

/* Layer 2: Semantic tokens (purpose-driven) */
:root {
  --color-primary: var(--blue-500);
  --color-border: var(--gray-200);
  --radius-card: var(--radius-m);
}

/* Layer 3: Component tokens (scoped, underscore prefix) */
.card {
  --_bg: var(--color-surface);
  --_border: var(--color-border);
  --_radius: var(--radius-card);
}
```

Look for:
- Colors used more than once → extract
- Spacing values → map to a spacing scale
- Font sizes → map to a type scale
- Border radii → extract
- Shadows → extract
- Transitions/durations → extract

## Step 6: Introduce Cascade Layers

Wrap existing styles in a layer architecture:

```css
@layer reset, tokens, base, layout, components, utilities;
```

Map existing styles to appropriate layers based on their role. Un-layered styles beat all layers, so migrate everything into layers.

## Step 7: Consolidate Redundancy

- Merge duplicate selectors
- Combine rules that share all properties
- Replace repeated property groups with custom properties
- Remove dead/unused CSS if identifiable (warn the user, don't silently delete)

## Step 8: Present Diffs

For every change, show a before/after diff:

```
File: layout.css

- .sidebar { float: left; width: 250px; }
- .main { margin-left: 270px; }
- .clearfix::after { content: ""; display: table; clear: both; }
+ .layout {
+   display: grid;
+   grid-template-columns: 250px 1fr;
+   gap: var(--space-m);
+ }
```

At the end, provide a summary:

```
Refactor Summary:
- Patterns fixed: 42
- Lines removed: 87
- Lines added: 61
- Net reduction: 26 lines
- Design tokens extracted: 15
- Cascade layers introduced: yes
- Files modified: 4
```

## Rules

- Never silently delete CSS. Always show what was removed and why.
- If a legacy pattern has a functional purpose (e.g., `float` for text wrapping around an image), leave it — only replace layout floats.
- Check [browser-compat.md](../css-expert/references/browser-compat.md) before removing vendor prefixes.
- When unsure whether code is dead, warn but don't delete.
- Preserve comments that explain business logic or workarounds.
