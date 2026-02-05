---
name: tailwindcss-v4-styling
description: Style with TailwindCSS v4 using @theme directive for theming, responsive design, and dark mode. Use when defining custom colors/fonts, implementing responsive layouts, or adding utility classes.
---

# TailwindCSS v4 Styling

Styling guide for TailwindCSS v4 with CSS-first configuration and @theme directive.

## When to Use This Skill

- Styling components and pages
- Defining custom themes (colors, fonts, spacing)
- Implementing responsive design
- Adding dark mode support
- Using utility-first CSS approach

**When NOT to use:**

- Logic implementation only → `angular-v21-development`
- Page routing configuration → `analogjs-development`
- UI/UX design patterns → `material-design-3-expressive`

## Core Principles

- **CSS-First Configuration:** No `tailwind.config.js` needed, use CSS directly
- **@theme Directive:** Define design tokens in CSS with `@theme { }`
- **Utility-First:** Prefer utility classes over custom CSS
- **Mobile-First:** Use responsive prefixes (md:, lg:, xl:) for larger screens
- **Class Binding:** Use `[class]` binding in Angular instead of `ngClass`
- **Style Binding:** Use `[style]` binding in Angular instead of `ngStyle`
- **Project Setup:**
  ```css
  /* src/styles.css */
  @import "tailwindcss";

  @theme {
    --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  }
  ```

## Implementation Guidelines

### Theme Configuration

Define custom design tokens in CSS:

1. Use `@theme { }` block in `src/styles.css`
2. Define CSS custom properties for colors, fonts, spacing
3. TailwindCSS automatically generates utility classes from theme variables
4. Use `oklch()` color space for better color manipulation

→ Details: [Theme Configuration](references/theme-configuration.md)

### Responsive Design

Responsive layout patterns:

1. Mobile-first approach: base styles for mobile
2. Add breakpoint prefixes for larger screens: `md:`, `lg:`, `xl:`, `2xl:`
3. Use responsive container classes
4. Test across breakpoints

→ Details: [Theme Configuration](references/theme-configuration.md#responsive-design)

### Dark Mode

Dark mode implementation patterns:

1. Use `prefers-color-scheme` media query in `@theme`
2. Override CSS custom properties for dark theme
3. Use `dark:` variant for component-level overrides

→ Details: [Theme Configuration](references/theme-configuration.md#dark-mode)

### Angular Integration

Patterns for using TailwindCSS with Angular:

1. Use `[class]` binding for conditional classes
2. Use `[style]` binding for dynamic styles
3. Avoid `ngClass` and `ngStyle` directives
4. Keep styling in template, use component CSS for complex cases

→ Details: [Theme Configuration](references/theme-configuration.md#angular-integration)

### Layout Patterns

Common layout implementations:

1. Flexbox utilities: `flex`, `justify-*`, `items-*`, `gap-*`
2. Grid utilities: `grid`, `grid-cols-*`, `col-span-*`
3. Container: `container mx-auto px-4`
4. Spacing: `p-*`, `m-*`, `space-*`

→ Details: [Theme Configuration](references/theme-configuration.md#layout-patterns)

## Workflow

1. **Design Analysis:** Review design requirements and identify patterns
2. **Theme Setup:** Define custom tokens in `@theme` if needed
3. **Utility Styling:** Apply utility classes directly in templates
4. **Responsive Adaptation:** Add breakpoint prefixes for responsive behavior
5. **Interaction States:** Add hover:, focus:, active: variants
6. **Dark Mode:** Implement dark theme support if required

## Related Skills

- **angular-v21-development:** For class binding integration
- **material-design-3-expressive:** For design token integration
- **analogjs-development:** For page styling

## Reference Documentation

For detailed patterns and code examples, see:

- [Theme Configuration](references/theme-configuration.md) - @theme directive and customization
