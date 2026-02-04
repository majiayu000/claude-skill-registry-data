---
name: material-design-3-expressive
description: Apply Material Design 3 Expressive design principles, animations, and component patterns. Use when designing UI, implementing micro-interactions, color systems, or spring-based animations.
---

# Material Design 3 Expressive

Design guide for Material Design 3 Expressive principles with TailwindCSS integration.

## When to Use This Skill

- UI/UX design and planning
- Implementing micro-interactions
- Designing color systems (Dynamic Color)
- Implementing animations and transitions
- Ensuring accessibility compliance

**When NOT to use:**

- Backend logic implementation → `angular-v21-development`
- Page routing configuration → `analogjs-development`
- Basic styling only → `tailwindcss-v4-styling`

## Core Principles

- **Expressiveness:** Fluid, spring-based animations that feel natural
- **Personalization:** UI that reflects user personality and preferences
- **Context Awareness:** Adaptive UI that responds to context and usage
- **Accessibility:** WCAG AA compliance, clear focus indicators, sufficient contrast
- **Design Characteristics:**
  - Rounded corners for friendly appearance
  - Subtle shadows and elevation
  - Spring-based motion for organic feel
  - Clear focus states for keyboard navigation

## Implementation Guidelines

### Color System

Material Design 3 Expressive color patterns:

1. Define semantic color roles (primary, surface, on-primary, etc.)
2. Use `oklch()` color space for better manipulation
3. Implement Dynamic Color for personalization
4. Ensure WCAG AA contrast ratios

→ Details: [Design Tokens](references/design-tokens.md#color-system)

### Component Styling

Component design patterns:

1. Use generous padding and rounded corners
2. Apply subtle shadows for elevation
3. Implement smooth hover/focus transitions
4. Use consistent spacing scale

→ Details: [Design Tokens](references/design-tokens.md#component-patterns)

### Animation and Motion

Motion design patterns:

1. Use spring-based easing for natural feel
2. Keep animations under 400ms for responsiveness
3. Use transform properties for performance
4. Implement enter/exit animations

→ Details: [Design Tokens](references/design-tokens.md#animation)

### Accessibility

Accessibility requirements:

1. Minimum 4.5:1 contrast ratio for text
2. Visible focus indicators with offset
3. Support for reduced motion preference
4. Semantic HTML and ARIA attributes

→ Details: [Design Tokens](references/design-tokens.md#accessibility)

### Typography

Typography patterns:

1. Use clear hierarchy with size and weight
2. Maintain readable line lengths (45-75 characters)
3. Use appropriate line-height for readability
4. Consider responsive typography

→ Details: [Design Tokens](references/design-tokens.md#typography)

## Workflow

1. **Design Analysis:** Review UX goals and user needs
2. **Color Definition:** Define semantic color roles
3. **Component Design:** Apply M3E patterns to components
4. **Motion Design:** Add animations and transitions
5. **Accessibility Audit:** Verify WCAG AA compliance
6. **Responsive Testing:** Test across breakpoints

## Related Skills

- **tailwindcss-v4-styling:** For implementing styles
- **angular-v21-development:** For component implementation
- **analogjs-development:** For page application

## Reference Documentation

For detailed patterns and code examples, see:

- [Design Tokens](references/design-tokens.md) - Colors, typography, motion, accessibility
