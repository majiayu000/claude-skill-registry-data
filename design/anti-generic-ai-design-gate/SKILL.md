---
id: frontend.design.anti-generic-ai-design-gate
name: Anti Generic AI Design Gate
description: Detect trend-stacked and brandless interfaces, then require product-specific visual reasoning before design approval.
stack:
  - Frontend
  - Visual Design
  - Design Systems
category: design
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - AI-looking design
  - generic AI UI
  - avoid AI aesthetic
  - design feels generated
---

# Anti Generic AI Design Gate

## Purpose

Block unreasoned accumulation of fashionable patterns while preserving useful, familiar interaction conventions.

## When to Use

- A screen is plausible but interchangeable once its logo is removed.
- Decorative surfaces compete with hierarchy, domain meaning, or task focus.

## Do

- Apply logo-removal and grayscale hierarchy tests across real states and non-hero screens.
- Classify visual signals as purposeful, neutral, or ornamental debt.
- Define a visual thesis: typography, shape, density, contrast, imagery, motion, and a repeatable component fingerprint.

## Do Not

- Do not ban a style merely because generative tools use it often.
- Do not solve genericity with extra decoration, copied references, or novelty that harms comprehension.

## Review Checklist

- [ ] Major visual decisions have product, usability, or brand rationale.
- [ ] Hierarchy survives grayscale and blur checks.
- [ ] Identity works beyond a logo, accent color, and hero section.

## Expected Output

1. Genericity diagnosis and keep/remove/rework table.
2. Visual thesis and component fingerprint.
3. Prioritized redesign actions and pass/fail result.

## References

- [Design Excellence Guide](../../../../docs/design-excellence-guide.md)
