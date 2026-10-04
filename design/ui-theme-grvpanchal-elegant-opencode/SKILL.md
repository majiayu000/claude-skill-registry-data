---
name: ui-theme
description: Design-token systems — semantic CSS custom properties for colours, spacing, typography, and shadows, with light/dark theme switching via `[data-theme]` overrides. Use when setting up a token catalogue, auditing components for hardcoded colours/magic numbers, or adding dark-mode support via token swaps.
when_to_use: Setting up or extending a design-token catalogue; replacing hardcoded colours/spacing with `var(--token)` references; implementing dark-mode via `[data-theme="dark"]` overrides; enforcing semantic names (--color-error) over value names (--color-red).
paths:
  - "**/theme/**/*.{css,scss,less}"
  - "**/styles/**/*.{css,scss,less}"
  - "**/tokens/**/*"
  - "**/*theme*.{css,js,ts}"
---

# Theme

## What is a Theme?

Themes are systematic design languages implemented through CSS—design tokens covering colors, typography, spacing, shadows, and interactions that ensure visual consistency across your entire application.

## Key Principles

1. **Design Tokens**: Use named tokens (`--color-primary`, `--spacing-md`) not raw values. Tokens are the contract between designers and developers.

2. **CSS Custom Properties**: Prefer CSS variables over preprocessor variables for runtime flexibility (dark mode, user preferences) without recompilation.

3. **Semantic Naming**: Use purpose-based names (`--color-error`) not value-based (`--color-red`). Allows theme changes without renaming.

## Best Practices

✅ **DO**:
- Define all design decisions as tokens
- Use CSS custom properties (variables)
- Support light/dark mode via token switching
- Create semantic color names (primary, error, surface)
- Document token usage and values
- Organize tokens by category (color, spacing, typography)

❌ **DON'T**:
- Hardcode colors/spacing in components
- Use magic numbers (`padding: 17px`)
- Create one-off values outside token system
- Mix token naming conventions
- Forget accessibility (contrast ratios)

## Code Patterns

### Recommended

```css
/* tokens.css - Design token definitions */
:root {
  /* Color tokens - semantic names */
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;
  --color-error: #ef4444;
  --color-success: #22c55e;
  
  /* Surface colors */
  --color-surface: #ffffff;
  --color-surface-elevated: #f8fafc;
  --color-text: #1e293b;
  --color-text-muted: #64748b;
  
  /* Spacing scale */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  
  /* Typography */
  --font-family: system-ui, sans-serif;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.25rem;
}

/* Dark mode via token override */
[data-theme="dark"] {
  --color-surface: #0f172a;
  --color-text: #f1f5f9;
}
```

```jsx
// Component using tokens
const Button = ({ variant }) => (
  <button style={{
    backgroundColor: `var(--color-${variant})`,
    padding: 'var(--spacing-sm) var(--spacing-md)',
    fontFamily: 'var(--font-family)'
  }}>
    Click
  </button>
);
```

### Avoid

```css
/* ❌ WRONG - Hardcoded values */
.button {
  background: #3b82f6;  /* Magic color */
  padding: 8px 16px;    /* Magic numbers */
}

/* ✅ CORRECT - Use tokens */
.button {
  background: var(--color-primary);
  padding: var(--spacing-sm) var(--spacing-md);
}
```

## Related Terminologies

- **Atom** (UI) - Atoms consume theme tokens
- **Component** (UI) - All components reference theme
- **Accessibility** (UI) - Theme must meet contrast requirements
- **Props** (UI) - Theme can be passed as prop context

## Quality Gates

- [ ] All colors defined as tokens
- [ ] All spacing uses scale tokens
- [ ] Semantic naming (not value-based)
- [ ] Dark mode supported
- [ ] Meets WCAG contrast requirements
- [ ] Documented token catalog

**Source**: `/docs/ui/theme.md`
