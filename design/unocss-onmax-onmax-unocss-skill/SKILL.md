---
name: unocss-onmax
description: Use when writing UnoCSS with presetOnmax workflow - covers attribute mode patterns, fluid spacing (f- prefix), scale-to-pixel (1px base), custom variants (hocus, reka-*, data-state), nimiq-css design system (nq-* utilities), and Reka UI integration. Apply when editing .vue files with UnoCSS attributes or configuring uno.config.ts.
---

# UnoCSS with presetOnmax Workflow

Custom UnoCSS workflow using `unocss-preset-onmax` with fluid sizing, 1px-base spacing, and attributify mode.

## Core Concepts

| Concept | Pattern | Example |
|---------|---------|---------|
| **Attribute mode** | `attr="~ value"` | `flex="~ col gap-8"` |
| **Fluid spacing** | `f-{util}-{size}` | `f-px-md`, `f-pt-2xl` |
| **Scale-to-px** | 1rem = 4px | `p-16` = 16px |
| **hocus** | hover + focus | `bg="neutral hocus:blue"` |
| **size-X** | width + height | `size-40` = 40×40px |

## When to Load Sub-Files

**Load based on task:**

| Task | File |
|------|------|
| Configuring uno.config.ts | [preset-onmax.md](preset-onmax.md) |
| Writing component styles | [attributify.md](attributify.md) |
| Responsive typography/spacing | [fluid-sizing.md](fluid-sizing.md) |
| State selectors, dark mode | [variants.md](variants.md) |
| nimiq-css utilities (nq-*) | [nimiq-css.md](nimiq-css.md) |

**DO NOT load all files.** Each ~400-800 tokens. Load only what's needed.

## Quick Reference

### Attribute Mode Syntax
```vue
<div flex="~ col items-center gap-16">
<div text="f-xl neutral-800">
<button bg="neutral-0 hocus:neutral-50">
<div outline="~ 1.5 offset--1.5 neutral/10">
```

### Fluid Sizing Scale
```
2xs=8/12  xs=12/16  sm=16/24  md=24/32  lg=32/48  xl=48/72  2xl=72/96
```

### Common Patterns
```vue
size-40 rounded-full           <!-- Circle button -->
f-px-md f-pt-sm               <!-- Fluid padding -->
outline="1.5 offset--1.5"     <!-- Inset outline -->
hocus:bg-neutral-100          <!-- Hover+focus -->
stack                         <!-- Centered grid overlay -->
```

## Token Budget

- Base: ~250 tokens
- Per sub-file: ~400-800 tokens
