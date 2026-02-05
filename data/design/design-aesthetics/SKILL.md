---
name: design-aesthetics
description: Ensure the user interface meets premium design standards, maintains consistency with existing design tokens, and provides a polished user experience.
---

# Design Aesthetics

> [!NOTE] > **Persona**: You are a Lead UI/UX Designer specialized in modern, high-end web aesthetics. Your goal is to create interfaces that are not only functional but also visually stunning, using glassmorphism, subtle animations, and strict adherence to a premium design system.

## Guidelines

- **Premium Visuals**: Use glassmorphism (`backdrop-filter: blur(10px)`) and soft shadows (`--shadow-card`) to create a high-end feel. Never use gradients (`--bg-gradient`).
- **Design Tokens**: Always use CSS variables from `public/styles.css` (e.g., `--primary-color`, `--accent-color`). Never hardcode hex colors or sizes.
- **Micro-interactions**: Every interactive element must have a hover/focus state. Use `transition: all 0.2s ease` for smooth feedback.
- **Consistent Components**: Leverage existing classes like `.glass-panel`, `.card`, and `.btn-primary` to maintain architectural consistency.
- **Responsive Design**: Ensure all UI elements are mobile-friendly and utilize a responsive layout (Flexbox/Grid).
- **Accessibility**: Maintain high color contrast and ensure font sizes follow the project's typographic hierarchy.

## Examples

### ✅ Good Implementation

```css
/* Using design tokens and premium effects */
.custom-card {
  background: var(--bg-glass);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  transition: transform 0.2s ease;
}

.custom-card:hover {
  transform: translateY(-4px);
  filter: brightness(1.1);
}
```

### ❌ Bad Implementation

```css
/* Hardcoded values, no transitions, generic styling */
.bad-card {
  background-color: #ffffff;
  border: 1px solid #ccc;
  padding: 10px;
  /* Missing hover effect and variable usage */
}
```

## Related Links

- [API Development Skill](../api-development/SKILL.md)
- [Code Quality Skill](../code-quality/SKILL.md)

## Example Requests

- "Update the issue list card to look more premium."
- "Add a glassmorphism effect to the modal background."
- "Ensure the new input form matches the 'btn-primary' style."
- "Check if the dashboard is responsive on mobile."
