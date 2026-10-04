---
id: angular.styles.host-css-custom-properties
name: Angular Host CSS Custom Properties
description: Expose style-only component state as CSS custom properties from Angular host bindings so CSS can render layout without imperative DOM mutation.
stack:
  - Angular
category: styles
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - host css custom properties
  - css variables
  - style-only state
---

# Angular Host CSS Custom Properties

Use this skill when Angular should expose visual state to CSS without turning styling into component logic.

## Purpose

Allow Angular components to publish safe, style-only values as CSS custom properties.

## When to Use

Use this skill when a component needs to expose layout values to CSS.

## Do

- keep the source of truth in Angular
- expose only style-only values
- provide CSS fallbacks

## Do Not

- leak business logic into CSS
- use DOM mutation for style values
- expose accessibility or behavioral state as CSS variables

## Review Checklist

- [ ] The value is purely visual or layout-related.
- [ ] The CSS variable has a fallback.
- [ ] No DOM query or imperative style mutation was added.
- [ ] The component still has a clear public API.

## Expected Output

Return:

1. The visual state to expose.
2. The CSS custom property names.
3. The minimal Angular host binding needed.
4. Risks or fallback notes.
