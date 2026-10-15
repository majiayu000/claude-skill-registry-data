---
name: web-layout-best-practices
description: |
  Web and Storybook layout and sizing guidance. Use when centering or sizing UI elements, reviewing positioning code, or composing Storybook hosts and decorators.
---

# Web Layout Best Practices

- Center with Flexbox, Grid, or `mx-auto`; transforms do not participate in layout, so avoid `left-1/2` plus `-translate-x-1/2`.
- Use CSS `zoom` when scaling must affect layout; `transform: scale()` changes only visual rendering.
- Prefer `fullscreen` layout in Storybook; use `mx-auto flex min-h-screen w-full max-w-2xl items-center justify-center p-2` for `w-full` container components, while intrinsic-size icons and buttons need only flex centering without a constrained-width host.
- Choose fixed versus adaptive dimensions deliberately; for example, buttons usually use fixed `h-*` and `px-*` with content-driven width for font size and localization, while fixed `w-*` or adaptive height are exceptions.
- Keep elements in flow when possible; use negative margins for overlap, reserving `absolute` for true overlays.
