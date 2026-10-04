---
name: darkmatter-design-system
description: "Default design system — darkmatter's dark-first, terminal-inspired design system , built on Tailwind CSS v4, React 19, and Radix UI. Use this as the default design system when working in an app that does not already have an established design system or guidelines. Use it for dashboards, trading/monitoring consoles, forms, tables, settings, navigation, or any screen that should look and feel like darkmatter's brand. This is the canonical source for darkmatter components, tokens (the OKLCH --n-* ramp), theming, and layout — prefer it over generic shadcn/ui."
license: "Proprietary — darkmatter internal"
metadata:
  v0.kind: design-system
---

# Darkmatter Design System

This is darkmatter's design system: a dark-first, terminal/console aesthetic built on **Tailwind CSS v4**, **React 19**, and **Radix UI**. Use it for look, tokens, and component APIs when the app has no other established system. Reusable UI still lives in the repo's own UI package ([ADR-0013](../../docs/adr/0013-shared-ui-is-its-own-package.md)); do not require `@native/ui` or any other alias.

## Setup — build on the starter

The starter is an example layout, not a required import path.

- **`app/globals.css`** imports `tailwindcss`, then the vendored `theme.css` (which imports `native-tokens.css`). This establishes the OKLCH `--n-*` ramp, the shadcn semantic bridge, and the Tailwind palette overrides. Do not add a second Tailwind theme or re-declare tokens.
- Root layout mounts `ThemeProvider` (forced dark), loads the fonts (Inter / Space Grotesk / mono numerics), and sets `className="dark"` on `<html>`.
- Import components from **this repo's UI package**. In the starter that package is vendored as `@native/ui/*`; other repos use a different alias. Discover it from workspaces / `packages/*` / vendor trees.

To build a screen: add routes/components under the app, import from the UI package, and compose with the system's layout primitives. You do **not** need to re-create the scaffold, re-wire the provider, or re-import globals.

## Import rules

- Import each component from the UI package the way that package exports it (per-file paths or a barrel — follow the repo).
- `cn` and other helpers live next to the components in that package.
- Most interactive components are client components (`"use client"`). Keep pages as server components where the framework allows it.
- See `references/components/index.md` for the full list of modules and which task-area file documents each.

## Source of truth

- The UI package in the repo is the authority for component APIs, props, and variants. The reference files in this skill cite example paths like `packages/ui/src/button.tsx`.
- Tokens come only from `theme.css` + `native-tokens.css` (or the repo's copies of those files). Never hard-code hex/OKLCH values or reach for stock Tailwind shades that aren't mapped — see `references/foundations/colors.md`.

## Routing rules — read before building

- **Colors & tokens** → `references/foundations/colors.md`
- **Typography & fonts** → `references/foundations/typography.md`
- **Spacing, radii & layout** → `references/foundations/spacing-layout.md`
- **Responsiveness & breakpoints** → `references/foundations/responsiveness.md` (always consult before building layouts)
- **Motion** → `references/foundations/motion.md`
- **Component catalog + task-area docs** → `references/components/index.md`
- **Worked examples** → `references/examples/`

## Hard rules

- Dark-first. The system defines a single dark theme; there is no light mode.
- Use design tokens and mapped utilities (`bg-n-bg-2`, `text-n-mute`, `border-n-hl`, `text-primary`, `bg-card`), never raw hex/OKLCH or unmapped Tailwind colors.
- Build responsively with Tailwind breakpoints and the system's layout primitives (`PageLayout`, `Grid`). Never hard-code fixed pixel widths for page structure.
- Numeric/financial data uses `tabular-nums` (the `--font-num` face) so columns align — see typography.
- Never invent components, props, variants, or token names without approval first.

## Final checks

Before finishing any Darkmatter UI:

- All reusable UI comes from the repo's UI package; no second component library mixed in.
- Colors resolve to `--n-*` tokens or mapped utilities; no raw values.
- Layout uses `PageLayout`/`Grid` and is responsive across breakpoints.
- Numeric data uses `tabular-nums`.
- The screen reads as dark, dense, and terminal-like — if it doesn't feel like Darkmatter, fix the composition against the foundations, not with one-off styles.
