---
name: cupertino-ui-consistency
description: Maintain Cupertino + Lumina visual consistency for the AERA frontend. Use when creating or modifying UI, CSS/tokens, layouts, components, menus/overlays, tables, charts, or interaction states in this repo.
---

# Cupertino Ui Consistency

## Overview

Apply a consistent Cupertino-inspired layer on top of Lumina: clean, recessed surfaces, glass materials, soft shadows, and restrained hierarchy. Use the checklist to align typography, tokens, components, interactions, and accessibility.

## Workflow

1. Define and use tokens first (palette, type, spacing, radii, elevation, motion).
2. Restyle components to match Cupertino + Lumina (materials, shapes, states).
3. Validate interaction completeness and accessibility (keyboard, focus, reduced motion).

## Checklist

- Typography: SF Pro Display/Inter system stack; avoid custom licensed fonts; set `font-variant-numeric: tabular-nums` for numbers.
- Tokens: define palette (single blue, no purple), desaturated red, radii (squircle), shadows, elevation, spacing scale, type scale, icon sizes, and motion tokens.
- Materials: apply glass/blur for sidebar, popovers, dropdowns, sticky headers; keep soft ambient shadows.
- Components: ensure hover/active/focus-visible/disabled/loading/error states; keep weights light and rely on color/spacing.
- Overlay behavior: Esc closes, click-outside closes, focus returns to trigger, viewport-safe positioning.
- Keyboard nav: arrow keys for menus, enter/esc actions, tab order for all controls.
- Motion: Apple-like easing; 150-250ms; opacity/transform only; reduced-motion safe.
- Tables: text left, numbers right, dates centered; no vertical borders; subtle row hover and minimal sort indicators.
- Charts: minimal axes and grid; subtle hover tooltips; tabular numerals in labels.
- Forms/settings: System Settings layout with grouped sections; inspector panel or modal for edits.
- Sidebar: narrow, translucent, pill active state, subtle divider for secondary/profile items.
- Menus/dropdowns/popovers: frosted, soft shadow, consistent radius, subtle separators, full keyboard support.
- Accessibility: WCAG AA contrast, visible focus, keyboard access for all interactive elements.
- Iconography: monoline SF Symbols-like look; consistent stroke weight and sizes.

## Validation

Confirm tokens are used across components, overlays meet interaction rules, and UI changes keep the Lumina aesthetic while applying Cupertino polish.
