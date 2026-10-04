---
name: design-system
description: Use when turning an art direction into reusable design tokens, typography, spacing, layout, surface, component, state, motion, responsive, or content rules before or during implementation.
metadata:
  short-description: Build semantic visual, component and motion systems
---

# Design System

## Build semantic rules from the selected art direction

Define only tokens that have meaning in the project.

### Foundations
- semantic color roles, including interactive/focus/error states;
- type roles and fluid scale, not only font family;
- line height, tracking, paragraph measure and language-specific adjustments;
- spacing rhythm and section density modes;
- layout/grid/container/breakout rules;
- radius, border, shadow/material rules;
- imagery aspect/crop treatment;
- motion duration/easing/distance tokens.

### Components
For each recurring component specify:
- anatomy;
- variants only when behavior or hierarchy differs;
- default, hover, focus, active, disabled, loading, error and selected states as relevant;
- content limits and responsive transformation.

## Typography

Treat typography as brand infrastructure. For bilingual KR/EN work, tune Hangul and Latin optical size, weight, line-height and wrapping separately when necessary rather than assuming one numeric setting works equally.

## Constraint

Do not let the design system erase art direction. Systems should make intentional exceptions legible, not force every section into identical cards and spacing.
