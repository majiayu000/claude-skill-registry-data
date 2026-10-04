---
name: a11y-performance
description: Use for release-level accessibility and performance review, including WCAG 2.2 AA, keyboard/focus, target size, reduced motion, semantic controls, Core Web Vitals, images/fonts/JavaScript, and animation or 3D performance budgets.
metadata:
  short-description: Accessibility and performance release gates
---

# Accessibility + Performance

## Accessibility baseline

Target WCAG 2.2 AA for production work unless the project specifies a higher standard.

Check at minimum:
- semantic landmarks/headings/controls and accessible names;
- keyboard order and operation;
- visible focus and focus not fully obscured by authored sticky/fixed content;
- contrast/non-text contrast as applicable;
- pointer target sizing/spacing;
- non-drag alternative for drag interactions where required;
- labels, errors and status communication;
- reduced-motion behavior;
- zoom/reflow and narrow-width usability;
- media alternatives where applicable.

Read `references/gates.md` for numerical gates.

## Performance

Protect the user path before decorative fidelity:
- responsive/compressed images and reserved aspect ratios;
- font subset/weight discipline;
- lazy loading of noncritical creative code;
- animation of compositor-friendly properties when possible;
- no heavy JS work in scroll handlers;
- cap DPR/effects for 3D and stop offscreen render loops;
- avoid duplicated animation/component packages.

Measure rather than infer when a runnable app is available.
