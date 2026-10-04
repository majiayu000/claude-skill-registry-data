---
name: frontend-implementation
description: Use when converting a design direction into maintainable production frontend code, selecting architecture within the existing stack, implementing semantics, assets, loading behavior, CSS/layout, components, and progressive enhancement.
metadata:
  short-description: Implement art direction as maintainable frontend code
---

# Frontend Implementation

## Preserve context

Inspect the repository before changing frameworks, routing, styling strategy or component foundations. Extend the existing stack unless a change has a clear user/maintenance benefit.

## Build order

1. semantic document and information hierarchy;
2. responsive layout primitives;
3. design-system tokens;
4. functional states/interactions;
5. imagery/media loading;
6. motion/creative enhancement;
7. QA instrumentation.

## Engineering rules

- Prefer semantic HTML and native controls before recreating them.
- Keep component boundaries aligned to behavior/content responsibility, not every visual box.
- Use CSS Grid/Flex and fluid values before breakpoint proliferation.
- Reserve dimensions/aspect ratios for media to avoid layout shift.
- Subset/preload fonts intentionally; avoid loading families/weights not used.
- Keep server/client boundaries narrow in frameworks that support them.
- Lazy-load noncritical animation/3D code.
- Avoid global event listeners and per-frame React state updates for visual animation.
- Remove dead experimentation code and unused packages before release.

## Visual fidelity

Do not “fix” a difficult art direction by reverting to standard cards. If a composition is hard to implement, solve the layout constraint or explicitly negotiate the tradeoff.
