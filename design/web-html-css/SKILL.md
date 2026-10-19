---
name: web-html-css
description: >
  Build accessible, semantic, and responsive web user interfaces using modern
  HTML5 and CSS3. Use when structuring semantic HTML markup, designing layouts
  with Flexbox, CSS Grid, and Container Queries, creating themeable systems with
  CSS Custom Properties, ensuring WCAG 2.1 AA accessibility, or implementing
  responsive mobile-first designs.
compatibility: >
  Agent Skills-compatible coding agents creating or reviewing modern web
  markup and stylesheets.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "html, css, flexbox, grid, accessibility, responsive, wcag, web"
  topics: "programming-languages, software-development"
---

# Modern HTML5 and CSS3 Web Development

Modern frontend development prioritizes semantic HTML markup, accessible document outlines, responsive styling using CSS Grid and Flexbox, and maintainable design tokens via CSS Custom Properties. Never build websites out of generic `<div>` soup or sacrifice keyboard navigation and accessibility.

## Core Rules

1. **Use Semantic HTML elements first**: Use `<button>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<header>`, and `<footer>` rather than generic `<div>` tags with click listeners.
2. **Never remove focus outlines without providing an alternative**: `outline: none` without a custom `:focus-visible` style breaks keyboard accessibility and violates WCAG 2.1 AA.
3. **Adopt Mobile-First Responsive Design**: Use `min-width` media queries and fluid sizing with `clamp()` rather than rigid desktop-first breakpoints.
4. **Use CSS Grid for 2D layouts and Flexbox for 1D alignments**: Avoid float or table hacks.
5. **Always provide accessible names for interactive elements**: Every button or link with only an icon must include an `aria-label` or visually hidden text.
6. **Images must have `alt` attributes**: Provide descriptive text or `alt=""` for purely decorative illustrations.

---

## 1. Semantic Document Architecture

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Analytics Dashboard - SaaS Platform</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="site-header">
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <div class="logo">Acme SaaS</div>
    <nav aria-label="Main Navigation">
      <ul class="nav-list">
        <li><a href="/dashboard">Dashboard</a></li>
        <li><a href="/reports">Reports</a></li>
        <li><a href="/settings">Settings</a></li>
      </ul>
    </nav>
  </header>

  <main id="main-content">
    <article class="report-card">
      <header>
        <h2>Monthly Recurring Revenue</h2>
      </header>
      <p class="metric-value">$42,500</p>
    </article>
  </main>

  <footer class="site-footer">
    <p>&copy; 2026 Acme Corp. All rights reserved.</p>
  </footer>
</body>
</html>
```

---

## 2. Modern CSS: Custom Properties and Fluid Typography

```css
:root {
  /* Design Tokens */
  --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-surface: #ffffff;
  --color-text: #1f2937;
  --color-muted: #6b7280;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;
  --radius-md: 0.5rem;

  /* Fluid typography: scales smoothly from 1rem at 320px to 1.25rem at 1200px */
  --text-base: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-surface: #111827;
    --color-text: #f9fafb;
    --color-muted: #9ca3af;
  }
}

body {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  color: var(--color-text);
  background-color: var(--color-surface);
  line-height: 1.5;
  margin: 0;
}
```

---

## 3. Responsive Layouts: CSS Grid & Flexbox

### Responsive Auto-Fit Grid (Zero Media Queries!)
Automatically wraps cards into multi-column layout based on card minimum width:

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
  gap: var(--space-lg);
  padding: var(--space-md);
}
```

### Accessible Skip-Link Pattern
```css
.skip-link {
  position: absolute;
  top: -999px;
  left: -999px;
  background: var(--color-primary);
  color: #fff;
  padding: var(--space-sm) var(--space-md);
  z-index: 1000;
}

.skip-link:focus {
  top: var(--space-sm);
  left: var(--space-sm);
}

/* Explicit, accessible focus indicators */
a:focus-visible, button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 3px;
}
```

---

## 4. Container Queries (Component-Driven Sizing)

Style components according to the width of their parent container rather than the global browser viewport:

```css
.card-container {
  container-type: inline-size;
}

.profile-card {
  display: flex;
  flex-direction: column;
}

/* When the card container has 450px or more space, switch to horizontal layout */
@container (min-width: 450px) {
  .profile-card {
    flex-direction: row;
    align-items: center;
    gap: var(--space-md);
  }
}
```

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Accessibility / UI Bug | Correct Practice |
| :--- | :--- | :--- |
| `<div onclick="...">` for buttons | Non-focusable by keyboard, not announced as button by screen readers | Use native `<button type="button">` |
| `outline: none;` without replacement | Keyboard users cannot see what element is focused | Use `:focus-visible { outline: 2px solid ... }` |
| Poor color contrast (< 4.5:1 ratio) | Fails WCAG AA; unreadable for low-vision users | Test contrast ratios with Lighthouse / axe |
| Fixed pixel widths (`width: 1200px`) | Causes horizontal overflow on mobile screens | Use max-width and fluid units: `max-width: 1200px; width: 100%` |
| Missing viewport meta tag | Mobile browsers render desktop zoom-out layout | Add `<meta name="viewport" content="width=device-width, initial-scale=1.0">` |

---

## 6. Verification Checklist

- [ ] Validated with W3C HTML validator with 0 errors.
- [ ] Tab navigation works across all interactive elements (`tabindex >= 0`).
- [ ] Color contrast meets WCAG 2.1 AA (4.5:1 for normal text, 3:1 for large text).
- [ ] Page scales seamlessly from 320px mobile viewport to 2560px 4K without horizontal overflow.
- [ ] Lighthouse accessibility score >= 95.
