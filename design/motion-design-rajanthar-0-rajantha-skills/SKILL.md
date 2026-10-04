---
name: motion-design
description: Design and implement accessible UI motion systems for React, Next.js, and frontend interfaces. Use for animation, transitions, gestures, drag and drop, page transitions, staggered reveals, SVG motion, loaders, motion tokens, reduced-motion behavior, or the old motion-foundations/motion-patterns/motion-advanced/motion-ui skills.
---

# Motion Design

Use this skill when motion should improve comprehension, feedback, continuity, or perceived quality.

## Routing

- Read `references/motion-foundations.md` for tokens, springs, reduced motion, SSR safety, and performance rules.
- Read `references/motion-patterns.md` for common UI patterns such as buttons, modals, toasts, page transitions, scroll, layout, and staggered reveals.
- Read `references/motion-advanced.md` for gestures, drag and drop, text animation, SVG paths, custom hooks, and imperative sequences.
- Read `references/motion-ui.md` when the user asks for a broad production UI motion system.

## Default Rules

1. Respect `prefers-reduced-motion`.
2. Animate transform and opacity before layout-affecting properties.
3. Keep motion purposeful, quick, and tied to state changes.
4. Avoid decorative motion that competes with task completion.
5. Verify entering, exiting, loading, error, disabled, hover, focus, and mobile states when relevant.

## Output

State what motion was added, what states it covers, and how reduced-motion behavior is handled.

