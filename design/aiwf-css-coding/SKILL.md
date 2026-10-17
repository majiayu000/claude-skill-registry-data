---
name: aiwf-css-coding
description: Use for CSS cascade, layout, responsive behavior, accessibility, visual polish, and rendered UI validation.
---

# AIWF CSS Coding

## Core Rule

Treat CSS changes as rendered behavior, not just text edits. Inspect the styling architecture and validate the affected viewport states. Avoid one-hue themes, accidental cascade leaks, brittle layout shifts, and inaccessible contrast.

## Workflow

1. Inspect the styling system: plain CSS, CSS modules, Tailwind, Sass, CSS-in-JS, component library tokens, reset/base files, and imported order.
2. Identify the affected layout context before editing: flex, grid, absolute positioning, stacking context, container queries, media queries, and overflow.
3. Patch with the smallest selector and scope that solves the issue. Avoid global selectors unless the task is global styling.
4. Check responsive states, hover/focus/disabled/loading states, text wrapping, contrast, and keyboard-visible focus.
5. Validate in a browser or screenshot when practical.

## CSS Guardrails

- Do not describe CSS as a single "CSS3" or "CSS4" target. CSS is module-based; verify feature support for the actual target browsers.
- Keep specificity low and intentional. Prefer local classes, cascade layers, or existing tokens over `!important`.
- Define stable dimensions for boards, grids, toolbars, icon buttons, counters, and fixed-format controls.
- Do not scale font size with viewport width. Use responsive layout, not viewport-driven type, unless the existing design system requires it.
- Avoid hidden overflow that clips focus rings, menus, tooltips, or long labels.
- Add `aiwf-avoid-ai-design` when the visual problem is generic AI-looking UI, default Gradio/shadcn styling, or palette/design cleanup.

## Validation Defaults

Prefer existing commands. Useful fallbacks:

```powershell
npm run lint
npm run build
npm run dev
```

Use the repo's package manager. For visual changes, verify at least one narrow mobile viewport and one desktop viewport when practical.

## Primary Source Anchors

- MDN CSS documentation: https://developer.mozilla.org/en-US/docs/Web/CSS
- W3C CSS current work: https://www.w3.org/Style/CSS/current-work.en.html
- W3C CSS current work and latest snapshot: https://www.w3.org/Style/CSS/current-work.en.html

Verify feature support against the project's browser target before relying on newer CSS.
