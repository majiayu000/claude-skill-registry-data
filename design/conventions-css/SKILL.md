---
name: conventions-css
description: Apply when writing styles. Ensures consistency with design system and project patterns.
---

# CSS Conventions

## No Utility Frameworks

No Tailwind, no utility classes, no CSS-in-JS. Custom CSS only.

## Scoping Rules

- **Atoms:** Unscoped `<style>` — allows design token inheritance
- **Everything else:** `<style scoped>`

## Design Tokens

CSS custom properties exclusively. Never hardcode colors, spacing, typography.

```css
.base-input {
  padding: var(--input-padding);
  border-color: var(--input-border-color);
  font-family: var(--input-font-family);
}
```

## Color System

- Semantic: `--color-primary-{100-400}`, `--color-error-{100-400}`
- Named: `--color-blue-{100-400}`, `--color-amber-{100-400}`
- Contextual: `--text-primary`, `--input-focus-border`

## Native CSS Nesting

```css
.base-input {
  &:focus {
    border-color: var(--input-focus-border);
  }
  &:disabled {
    opacity: var(--input-disabled-opacity);
  }
}
```

## Inline Styles

Only for truly dynamic values (calculated at runtime). Otherwise use CSS custom properties.
