---
name: design-systems
description: Use when building or maintaining a component library and design tokens. Covers token architecture, component API design, variants and states, documentation, and governing adoption across a codebase.
metadata:
  category: frontend
  version: 1.0.0
  tags: [design-system, tokens, components, theming, consistency]
---

# Design Systems

## Purpose

Build a component library that teams actually adopt: tokens instead of hardcoded values, components with a small honest API, and documentation that answers "which one do I use" without a meeting.

## When to Use

- Starting a design system or component library.
- Auditing a codebase for inconsistency (fourteen shades of grey, six button implementations).
- Designing the API of a shared component.
- Deciding whether a new pattern belongs in the system.

## Capabilities

- Token architecture: primitive, semantic, and component layers.
- Component API design: variants, sizes, states, composition.
- Theming, including dark mode and per-brand overrides.
- Documentation with live examples and usage guidance.
- Adoption tracking and migration from ad-hoc components.

## Inputs

- The existing visual language, however inconsistent.
- The consuming applications and their frameworks.
- The team's appetite for governance — a system nobody enforces will not hold.

## Outputs

- A token set with three layers and no hardcoded values in components.
- Components with documented variants, states, and accessibility behavior.
- A contribution and deprecation process.

## Workflow

1. **Audit first** — Extract every colour, spacing value, font size, and radius currently in use. The count is always shocking, and it is the argument for the system.
2. **Build tokens in layers** — Primitives (`blue-600`) hold raw values. Semantic tokens (`color-action-primary`) reference primitives and carry meaning. Component tokens (`button-bg-primary`) reference semantic tokens. Only the primitive layer contains literal values.
3. **Design the component API around variants** — `variant`, `size`, `state`. Not fifteen boolean props whose combinations are mostly invalid.
4. **Cover the states** — Default, hover, active, focus-visible, disabled, loading, error. A component missing focus-visible is inaccessible, not merely incomplete.
5. **Document with live examples** — Show the correct usage and the incorrect one. "Do / Don't" prevents more misuse than prose.
6. **Govern adoption** — A lint rule that forbids hardcoded colours is worth more than a style guide nobody reads.

## Best Practices

- Semantic tokens are what let you re-theme. A component referencing `blue-600` directly cannot be themed; one referencing `color-action-primary` can.
- Boolean props multiply: `isPrimary`, `isLarge`, `isDanger` allows `isPrimary + isDanger`, which is meaningless. A `variant` union makes invalid combinations unrepresentable.
- Every interactive component needs a visible focus indicator. Removing the outline without replacing it is the most common accessibility failure in design systems.
- Provide an escape hatch (`className`, `style`) but do not design around it. If every consumer overrides the same thing, the component's API is wrong.
- Version and deprecate properly. Removing a prop without a deprecation cycle breaks consumers you do not know about.
- A component used by one team is not a design-system component. Promote on the second consumer, not on speculation.

## Examples

**Three-layer token architecture:**

```css
:root {
  /* 1. Primitives — raw values, never used directly by components. */
  --blue-600: #2563eb;
  --blue-700: #1d4ed8;
  --grey-100: #f3f4f6;
  --grey-900: #111827;

  /* 2. Semantic — meaning, referencing primitives. This layer is what themes swap. */
  --color-action-primary: var(--blue-600);
  --color-action-primary-hover: var(--blue-700);
  --color-surface: #ffffff;
  --color-text: var(--grey-900);

  /* 3. Component — scoped to one component, referencing semantic tokens. */
  --button-bg-primary: var(--color-action-primary);
  --button-bg-primary-hover: var(--color-action-primary-hover);
}

[data-theme="dark"] {
  /* Only the semantic layer is redefined. Components need no changes. */
  --color-action-primary: #60a5fa;
  --color-surface: var(--grey-900);
  --color-text: var(--grey-100);
}
```

**Component API: variants, not boolean soup:**

```typescript
type ButtonProps = {
  variant?: "primary" | "secondary" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
  disabled?: boolean;
} & ButtonHTMLAttributes<HTMLButtonElement>;
```

Four variants and three sizes yield twelve valid combinations. Four booleans would yield sixteen, of which most are nonsense.

## Notes

- Enforce token usage with a lint rule (`stylelint-declaration-strict-value` or an ESLint rule for inline styles). Without enforcement, hardcoded values return within a month.
- A design system's real adoption metric is the number of hardcoded values remaining in consuming applications, trending toward zero. Track it.
- Do not build a component until it has two real consumers with the same requirements. Building for a hypothetical second consumer produces an API that fits neither.
