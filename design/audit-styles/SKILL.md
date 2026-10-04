---
name: audit-styles
description: Audit component CSS for arbitrary colors, font sizes, and spacing that violate ui-design.md token system. Report violations and optionally fix.
allowed-tools: Read, Glob, Grep, Agent, Bash(ls *)
---

# Audit Component Styles

Scan Svelte component `<style>` blocks for values that violate the design token system defined in `docs/ai/ui-design.md`.

## What to check

### 1. Arbitrary colors
- `rgba(30,32,40,*)` not matching any `--lz-*` token opacity step (0.06, 0.08, 0.10, 0.12, 0.15, 0.35, 0.50, 0.55, 0.70)
- `rgba(237,232,220,*)` not matching any `--dz-*` / `--dk-*` token opacity step (0.06, 0.08, 0.10, 0.12, 0.15, 0.25, 0.30, 0.35, 0.45, 0.55, 0.70, 0.85, 0.90)
- `rgba(120,120,69,*)` not matching any `--olive-*` accent overlay (0.08, 0.15, 0.30, 0.40)
- `rgba(68,114,180,*)` not matching any `--blue-*` accent overlay (0.08, 0.13)
- `rgba(232,160,144,*)` not matching any `--salmon-*` accent overlay (0.06, 0.08)
- `rgba(248,113,113,*)` or `rgba(229,115,115,*)` not matching `--danger-border` (0.40) or `--danger-bg-hover` (0.15)
- Any raw hex color (`#xxx` / `#xxxxxx`) that is not a CSS variable reference — exceptions: `#fff` in piano keys, CPU meter semantic colors

### 2. Font sizes
- Any `font-size` value below 7px (minimum per spec)
- Any `font-size` not matching the component's spec table in ui-design.md

### 3. Spacing
- Any `gap`, `padding`, or `margin` value not matching the spacing system (2, 4, 8, 12, 16px)
- Exception: asymmetric padding (e.g., `8px 12px 10px`) is allowed when documented in the component spec

### 4. Border widths
- Border widths other than 1px, 1.5px, 2px, or 3px (selected indicator)

## Scope

If a component name is provided as argument (e.g., `/audit-styles StepGrid`), audit only that component.
Otherwise, audit ALL `.svelte` files in `src/lib/components/`.

## Process

1. **Read `docs/ai/ui-design.md`** to load the current token system and component specs.
2. **For each target component**, read the `<style>` block.
3. **Extract and classify** every color, font-size, gap/padding/margin, and border value.
4. **Compare** against the token system and component spec tables.
5. **Report violations** in this format:

```
## Style Audit Report

### ComponentName.svelte
| Line | Property | Current Value | Expected | Severity |
|------|----------|---------------|----------|----------|
| 123  | color    | #e57373       | var(--color-danger) | error |
| 456  | border   | rgba(30,32,40,0.07) | 0.06 (--lz-divider) | warning |

### ComponentName.svelte — OK (no violations)
```

## Severity levels

- **error**: Raw hex/rgba that has a direct token equivalent
- **warning**: Opacity value between two token steps (e.g., 0.07 between 0.06 and 0.08)
- **info**: Value not in token system but may be intentional (e.g., CPU meter colors)

## Rules

- This is a **read-only** operation by default
- Use parallel Agent tools to audit multiple components concurrently
- Only flag values in `<style>` blocks, not inline `style=` attributes that use dynamic values
- Ignore `var(--*)` references — those are already tokenized
- Ignore `transparent`, `inherit`, `none`, `currentColor`
