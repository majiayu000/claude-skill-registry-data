---
name: rule-frontend-styles
description: MANDATORY when editing files matching ["frontend/src/styles/**/*.scss", "frontend/src/**/*.module.scss", "frontend/src/**/*.scss"]. SCSS styling patterns for the Simpler Grants frontend — USWDS theme token overrides, custom mixins, responsive breakpoints (at-media), and print styles. Complements frontend-components.mdc.
---

# Frontend Styles Rules

## Scope

This rule covers **SCSS, USWDS theme tokens, breakpoints, and print styles**. Component structure, JSX, and USWDS class usage in markup live in `frontend-components.mdc`.

## File Organization

ALL global SCSS lives in `frontend/src/styles/` as a **flat structure** — no subfolders today. The entry point `styles.scss` uses modern Sass `@forward` (NEVER legacy `@import`) in this exact dependency order:

```scss
// styles.scss
@forward "uswds-theme";
@forward "uswds";
@forward "uswds-theme-custom-styles";
@forward "loading";
```

- Token overrides → `_uswds-theme.scss`
- Custom styles, mixins, print rules → `_uswds-theme-custom-styles.scss`
- Loading state → `_loading.scss`

ALWAYS insert new partials in dependency order and add them to `styles.scss`. WHEN `_uswds-theme-custom-styles.scss` grows past ~500 lines, extract cohesive sections (e.g., `_print.scss`, `_mixins.scss`) and `@forward` them in order.

## USWDS Theme Overrides (`_uswds-theme.scss`)

ALWAYS override via USWDS Sass settings variables. NEVER hard-code hex.

```scss
$theme-color-primary-family: "mint";
$theme-respect-user-font-size: true;
```

The project's color families are **fixed** — new components MUST consume these and NEVER introduce ad-hoc palettes:

| Role | Family |
|---|---|
| base | `gray-warm` |
| primary | `mint` |
| secondary | `blue-cool-vivid` |
| accent-warm | `yellow` / `orange-vivid` |
| accent-cool | `violet` |

Other fixed tokens:
- **Fonts:** Public Sans (sans), Newsreader (serif), variable weights 200–800
- **Type scale:** tokens 1–17
- **Container:** `desktop-lg` max-width
- **Column gaps:** `4` mobile / `6` desktop
- **Link colors:** `mint-60` / `mint-70`, visited `violet-60`
- **Button radius:** `2px`
- **Tooltip:** `blue-cool-60v`
- **Identifier bg:** `mint-70`

REUSE these tokens rather than redefining gutters, fonts, or colors. When adding a new override, group it with the matching USWDS settings section and leave a comment linking to the USWDS settings docs.

## Custom Styles & Mixins (`_uswds-theme-custom-styles.scss`)

PREFER USWDS mixins/functions already in use here:
- Mixins: `u-shadow()`, `u-padding-right()`, `at-media()`, `at-media-max()`, `button-unstyled`, `z-index()`
- Functions: `units()`, `color()`, `family()`

REUSE established class patterns:
- `.usa-button--{variant}` for button variants
- `.simpler-{thing}` for project-specific utilities (e.g., `.simpler-responsive-table`)
- BEM-ish suffixes: `__element`, `--modifier` (e.g., `.sf424__table`, `.saved-opportunity-*`)

DO NOT invent new mixins inline. If logic repeats 3+ times, factor it out — and once you have several mixins, extract a `_mixins.scss` partial.

## Responsive Breakpoints

ALWAYS use `@include at-media($breakpoint)` / `at-media-max($breakpoint)` with USWDS named breakpoints: `mobile-lg`, `tablet`, `desktop`, `desktop-lg`. NEVER write raw `@media (min-width: ...)`.

```scss
.pdf-card {
  padding: units(2);

  @include at-media('tablet') {
    padding: units(4);
  }

  @include at-media('desktop') {
    @include u-shadow(2);
  }
}
```

- Mobile-first: base styles, then `at-media('tablet')`, then `desktop`.
- `widescreen` utilities are **disabled** in this project — DO NOT target it.

## Print Styles

Print rules currently live alongside their component in `_uswds-theme-custom-styles.scss` — see `.sf424__table` for the canonical example. Follow that pattern.

In `@media print` blocks:
- Hide nav, footer, and interactive controls
- Force black-on-white text
- Expand table layouts so all columns fit
- Use `page-break-inside: avoid` on key blocks
- Avoid background images
- Ensure form data is fully visible

```scss
.sf424__table {
  @media print {
    display: table;
    width: 100%;
    page-break-inside: avoid;
  }
}
```

WHEN multiple components need print rules, propose extracting a `_print.scss` partial and `@forward` it from `styles.scss` after `_uswds-theme-custom-styles.scss`.

## CSS Modules (`*.module.scss`)

- Co-locate next to the component: `Component.module.scss` beside `Component.tsx`.
- Use **camelCase** class names; access via `styles.className`.
- Modules MUST still consume USWDS tokens via `@use "styles/uswds-theme" as *;` (or the project's established `@use` path) — NEVER hard-code colors or breakpoints.
- Keep modules small. PREFER USWDS utility classes in JSX for one-offs.

> Note: at the time of writing, the codebase uses primarily global SCSS + USWDS utility classes in JSX. CSS Modules are acceptable for genuinely component-local styling, but check for an existing pattern first.

## Accessibility-Related Styling

- PRESERVE the WCAG AA contrast fixes already applied to nav — do not regress them.
- NEVER remove focus outlines without an equivalent visible replacement.
- RESPECT `prefers-reduced-motion` for any new animation (e.g., the existing `.pdf-card` hover transform).

```scss
.pdf-card {
  transition: transform 150ms ease;

  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }
}
```

## Anti-Patterns

- NO legacy `@import` — use `@use` / `@forward`.
- NO hard-coded hex or `px` when a USWDS token exists — use `color('mint-60')`, `units(2)`.
- NO raw media queries — always `at-media`.
- NO targeting `widescreen` (disabled).
- NO nesting deeper than 3 levels.
- NO `!important` except to override third-party styles, with an inline comment explaining why.
- NO new global styles for component-specific concerns — use a CSS Module or add a clearly-scoped block in `_uswds-theme-custom-styles.scss`.

---

## Related Rules

- **`frontend-components.mdc`** — component structure, JSX, USWDS class usage in markup
- **`frontend-i18n.mdc`** — translated strings consumed in styled components
- **`accessibility.mdc`** — WCAG 2.1 AA compliance (contrast, focus, motion)

## Specialist Validation

**Simple changes (token tweak, new variant class):** No specialist needed.

**Moderate changes (new partial, new mixin, print rules for a new component):** Invoke `codebase-conventions-reviewer`.

**Complex changes (USWDS upgrade, new color family, restructuring `styles/`):** Invoke in parallel:
- `architecture-strategist` — validate partial structure and `@forward` order
- `accessibility-auditor` — verify contrast, focus, and reduced-motion compliance
- `performance-oracle` — check CSS bundle impact
