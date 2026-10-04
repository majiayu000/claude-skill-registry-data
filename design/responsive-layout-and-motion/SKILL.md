---
id: frontend.css.responsive-layout-and-motion
name: Responsive Layout and Motion
description: Design resilient CSS layouts with content-first sizing, progressive enhancement, readable reflow, and reduced-motion support.
stack:
  - CSS
  - HTML
category: styles
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - responsive layout
  - container query
  - CSS grid
  - reduced motion
  - overflow
---

# Responsive Layout and Motion

## Purpose

Guide durable interface layout and motion decisions without tying implementation to a CSS framework, browser plugin, or a fixed viewport catalogue.

## When to Use

Use this skill when:

- a component must work across containers, viewport sizes, text scaling, or localization;
- a layout introduces Grid, Flexbox, container queries, overlays, or animated state changes;
- visual polish risks clipping content, creating layout shift, or obscuring keyboard focus.

## Do

- Define layout constraints from content, interaction priority, and available container space before choosing breakpoints.
- Use Grid and Flexbox for structural layout; use container queries only with a useful fallback or an explicitly supported browser baseline.
- Make overflow intentional: wrap, scroll, truncate with an accessible alternative, or redesign the density.
- Respect `prefers-reduced-motion`; keep animation optional, short, and non-essential to comprehension.
- Keep component styling encapsulated according to the host framework and route Angular host-token patterns to `angular.styles.host-css-custom-properties`.

## Do Not

- Do not hard-code device names, screen dimensions, or absolute filesystem paths.
- Do not use animation as the sole signal of completion, error, or changed state.
- Do not introduce preprocessor, utility, or post-processing dependencies just to follow this skill.
- Do not treat a screenshot at one resolution as responsive validation.

## Review Checklist

- [ ] Long labels, translated strings, and user zoom do not hide essential content.
- [ ] The component remains usable in a narrower parent container.
- [ ] Focus, hover, active, disabled, and loading states remain distinguishable.
- [ ] Motion has a reduced-motion path and does not block interaction.
- [ ] New browser-dependent CSS has a documented support decision or fallback.

## Expected Output

1. Describe the component constraints and responsive states.
2. Identify CSS features that need progressive enhancement or fallback.
3. Provide viewport, container, zoom, and reduced-motion validation evidence.
4. State any browser-baseline assumption.
