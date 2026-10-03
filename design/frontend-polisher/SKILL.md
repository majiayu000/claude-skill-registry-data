---
name: frontend-polisher
description: Polish frontend UI implementation with responsive layout, accessibility, visual quality, interaction states, and browser verification. Use when the user asks to improve a web app, fix layout, make UI feel better, validate mobile/desktop behavior, check screenshots, or refine CSS/components. Do not use for non-frontend code or image generation.
---

# Frontend Polisher

Make the interface usable, coherent, and verified.

## Workflow

1. Learn the existing design system, component library, routing, and styling conventions.
2. Identify the main workflow the screen must support. Optimize that workflow before decoration.
3. Check layout at mobile, tablet, and desktop widths.
4. Verify interactive states: loading, empty, error, disabled, focus, hover, long text, and overflow.
5. Use browser automation or screenshots when a local target is available.
6. Fix overlap, clipping, unstable dimensions, contrast problems, and missing affordances.

## UI Standards

- Prefer existing components and icons.
- Keep dense tools scannable; reserve hero treatment for real landing pages.
- Give boards, grids, toolbars, counters, and tiles stable dimensions.
- Ensure long labels wrap or truncate intentionally.
- Avoid decorative gradients or blobs when content clarity is the real need.
- Do not hide primary product or state behind atmospheric imagery.

## Verification

Record:

- Local URL or file opened.
- Viewports checked.
- Screenshots or observations.
- Accessibility issues fixed or remaining.
- Any browser/dev-server problem that blocked visual QA.
