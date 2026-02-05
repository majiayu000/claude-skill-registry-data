---
name: css-standards
description: CSS, SCSS, and styling conventions. Use when writing, reviewing, or debugging styles and layouts.
---

# CSS/SCSS Coding Standards

## General Preferences

- **CSS Modules** or **Tailwind CSS** for component styling
- **SCSS** for complex stylesheets when needed
- **CSS Custom Properties** (variables) for theming
- **Mobile-first** responsive design
- **BEM naming** for traditional CSS (when not using modules)

## Naming Conventions

### BEM (Block Element Modifier)
```css
/* Block: standalone component */
.card {}

/* Element: part of a block (double underscore) */
.card__header {}
.card__body {}
.card__footer {}

/* Modifier: variation of block/element (double hyphen) */
.card--featured {}
.card--compact {}
.card__header--large {}

/* Example usage */
.user-profile {}
.user-profile__avatar {}
.user-profile__name {}
.user-profile--verified {}
```

### CSS Modules
```css
/* UserCard.module.css */
.container {}
.header {}
.avatar {}
.name {}

/* Composes for shared styles */
.primaryButton {
  composes: button from './shared.module.css';
  background: var(--color-primary);
}
```

### Utility Classes (Tailwind-style)
```css
/* When creating custom utilities */
.text-center { text-align: center; }
.mt-4 { margin-top: 1rem; }
.flex { display: flex; }
.hidden { display: none; }
```

## CSS Custom Properties

```css
/* Define in :root for global variables */
:root {
  /* Colors */
  --color-primary: #0066cc;
  --color-primary-hover: #0052a3;
  --color-secondary: #6c757d;
  --color-success: #28a745;
  --color-error: #dc3545;
  --color-warning: #ffc107;

  /* Text colors */
  --color-text: #1a1a1a;
  --color-text-muted: #6c757d;
  --color-text-inverse: #ffffff;

  /* Backgrounds */
  --color-bg: #ffffff;
  --color-bg-secondary: #f8f9fa;
  --color-bg-tertiary: #e9ecef;

  /* Spacing scale */
  --space-xs: 0.25rem;   /* 4px */
  --space-sm: 0.5rem;    /* 8px */
  --space-md: 1rem;      /* 16px */
  --space-lg: 1.5rem;    /* 24px */
  --space-xl: 2rem;      /* 32px */
  --space-2xl: 3rem;     /* 48px */

  /* Typography */
  --font-family: system-ui, -apple-system, sans-serif;
  --font-family-mono: 'SF Mono', Consolas, monospace;

  --font-size-xs: 0.75rem;   /* 12px */
  --font-size-sm: 0.875rem;  /* 14px */
  --font-size-md: 1rem;      /* 16px */
  --font-size-lg: 1.125rem;  /* 18px */
  --font-size-xl: 1.25rem;   /* 20px */
  --font-size-2xl: 1.5rem;   /* 24px */

  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;

  /* Borders */
  --border-radius-sm: 0.25rem;
  --border-radius-md: 0.5rem;
  --border-radius-lg: 1rem;
  --border-radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);

  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-normal: 250ms ease;
  --transition-slow: 350ms ease;

  /* Z-index scale */
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-modal: 300;
  --z-tooltip: 400;
}

/* Dark mode override */
@media (prefers-color-scheme: dark) {
  :root {
    --color-text: #f0f0f0;
    --color-bg: #1a1a1a;
    --color-bg-secondary: #2d2d2d;
  }
}

/* Or with class toggle */
.dark {
  --color-text: #f0f0f0;
  --color-bg: #1a1a1a;
}
```

## Layout

### Flexbox
```css
/* Common flex patterns */
.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

.flex-between {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.flex-column {
  display: flex;
  flex-direction: column;
}

/* Gap for spacing (preferred over margins) */
.flex-row {
  display: flex;
  gap: var(--space-md);
}
```

### Grid
```css
/* Auto-fit responsive grid */
.grid-auto {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-lg);
}

/* Fixed columns */
.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-md);
}

/* Named areas for complex layouts */
.page-layout {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  grid-template-columns: 250px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }
```

## Responsive Design

```css
/* Mobile-first breakpoints */
/* Base styles = mobile */
.container {
  padding: var(--space-md);
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    padding: var(--space-lg);
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container {
    padding: var(--space-xl);
    max-width: 1200px;
    margin: 0 auto;
  }
}

/* Large desktop */
@media (min-width: 1280px) {
  .container {
    max-width: 1400px;
  }
}

/* Custom properties for breakpoint-aware values */
:root {
  --container-padding: var(--space-md);
}

@media (min-width: 768px) {
  :root {
    --container-padding: var(--space-lg);
  }
}
```

## Components

### Buttons
```css
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-xs);

  padding: var(--space-sm) var(--space-md);
  font-size: var(--font-size-md);
  font-weight: 500;
  line-height: 1;

  border: none;
  border-radius: var(--border-radius-md);
  cursor: pointer;

  transition: background-color var(--transition-fast),
              transform var(--transition-fast);
}

.button:hover {
  transform: translateY(-1px);
}

.button:active {
  transform: translateY(0);
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.button--primary {
  background-color: var(--color-primary);
  color: var(--color-text-inverse);
}

.button--primary:hover {
  background-color: var(--color-primary-hover);
}

.button--secondary {
  background-color: transparent;
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
}
```

### Form Inputs
```css
.input {
  width: 100%;
  padding: var(--space-sm) var(--space-md);

  font-size: var(--font-size-md);
  line-height: var(--line-height-normal);

  background-color: var(--color-bg);
  border: 1px solid var(--color-bg-tertiary);
  border-radius: var(--border-radius-md);

  transition: border-color var(--transition-fast),
              box-shadow var(--transition-fast);
}

.input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.input:invalid {
  border-color: var(--color-error);
}

.input::placeholder {
  color: var(--color-text-muted);
}
```

### Cards
```css
.card {
  background-color: var(--color-bg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  overflow: hidden;
}

.card__header {
  padding: var(--space-md) var(--space-lg);
  border-bottom: 1px solid var(--color-bg-tertiary);
}

.card__body {
  padding: var(--space-lg);
}

.card__footer {
  padding: var(--space-md) var(--space-lg);
  background-color: var(--color-bg-secondary);
}
```

## Accessibility

```css
/* Focus styles - never remove, only enhance */
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Skip link for keyboard navigation */
.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
  padding: var(--space-sm) var(--space-md);
  background: var(--color-primary);
  color: var(--color-text-inverse);
  z-index: var(--z-tooltip);
}

.skip-link:focus {
  top: 0;
}

/* Visually hidden but accessible */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .button {
    border: 2px solid currentColor;
  }
}
```

## SCSS Patterns

```scss
// Variables (or use CSS custom properties)
$breakpoint-tablet: 768px;
$breakpoint-desktop: 1024px;

// Mixins
@mixin respond-to($breakpoint) {
  @if $breakpoint == tablet {
    @media (min-width: $breakpoint-tablet) { @content; }
  } @else if $breakpoint == desktop {
    @media (min-width: $breakpoint-desktop) { @content; }
  }
}

@mixin flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

// Usage
.hero {
  padding: var(--space-lg);
  @include flex-center;

  @include respond-to(tablet) {
    padding: var(--space-xl);
  }
}

// Nesting (keep shallow - max 3 levels)
.card {
  background: var(--color-bg);

  &__header {
    padding: var(--space-md);
  }

  &--featured {
    border: 2px solid var(--color-primary);
  }

  &:hover {
    box-shadow: var(--shadow-lg);
  }
}
```

## Project Commands

Check `.claude/commands.md` for project-specific commands. Common CSS commands:

```bash
# Build CSS
npm run build:css

# Watch for changes
npm run watch:css

# Lint CSS
npx stylelint "**/*.css"
npx stylelint "**/*.scss"

# Format
npx prettier --write "**/*.css"
```
