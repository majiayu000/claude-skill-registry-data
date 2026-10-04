---
name: geist-design
description: Applies Vercel's Geist design system colors, typography, materials, and brand guidelines to any artifact. Use when building UI components, creating visual artifacts, or applying Vercel/Next.js brand aesthetics. Covers Geist Sans/Mono fonts, the ds-* CSS token system, surface materials, and Vercel trademark rules.
user-invocable: false
---

# Geist Design System

## Overview

Geist is Vercel's design system for building consistent, high-quality web experiences. It powers vercel.com, v0.dev, and all Vercel products.

**Keywords**: Vercel, Geist, design system, brand, typography, color tokens, dark mode, components, Next.js, Turbo, v0

---

## Typography

### Fonts

| Font | Usage |
|------|-------|
| **Geist Sans** | All UI text, headings, body, labels |
| **Geist Mono** | Code, terminal output, technical labels |

Both fonts are open source and available at `https://vercel.com/font`.

```css
/* Install via npm */
/* @vercel/font (Next.js) or import from Google Fonts */
font-family: 'Geist', sans-serif;
font-family: 'Geist Mono', monospace;
```

### Type Scale

**Headings** — for page/section titles:

| Class | Usage |
|-------|-------|
| `text-heading-72` | Hero display |
| `text-heading-64` | Large hero |
| `text-heading-56` | Page hero |
| `text-heading-48` | Section hero |
| `text-heading-40` | Section title |
| `text-heading-32` | Large heading (supports "Subtle" modifier) |
| `text-heading-24` | Heading |
| `text-heading-20` | Subheading |
| `text-heading-16` | Small heading |
| `text-heading-14` | Smallest heading |

**Labels** — single-line UI elements:

| Class | Usage |
|-------|-------|
| `text-label-20` | Large label |
| `text-label-16` | Standard label |
| `text-label-14` | Default label |
| `text-label-13` | Small label (supports tabular spacing) |
| `text-label-12` | Tiny label |
| `text-label-14-mono` | Monospace label |
| `text-label-13-mono` | Small mono label |
| `text-label-12-mono` | Tiny mono label |

**Copy** — multi-line body text:

| Class | Usage |
|-------|-------|
| `text-copy-24` | Large body |
| `text-copy-16` | Default body |
| `text-copy-14` | Small body |
| `text-copy-13` | Smallest body |
| `text-copy-13-mono` | Inline code |

**Buttons** — button components only:

| Class | Usage |
|-------|-------|
| `text-button-16` | Large button |
| `text-button-14` | Default button |
| `text-button-12` | Tiny/input button |

All presets bundle `font-size`, `line-height`, `letter-spacing`, and `font-weight`. Apply `<strong>` inside to activate "Strong" variant.

---

## Colors

### Design Tokens System

Geist uses CSS custom properties with the `--ds-` prefix. Tokens automatically adapt to light/dark mode. Always use tokens, not raw hex values.

### Gray Scale (Primary Palette)

| Token | Usage |
|-------|-------|
| `var(--ds-gray-100)` | Default component background |
| `var(--ds-gray-200)` | Hover state background |
| `var(--ds-gray-300)` | Active state background |
| `var(--ds-gray-400)` | Default border |
| `var(--ds-gray-500)` | Hover border |
| `var(--ds-gray-600)` | Active border |
| `var(--ds-gray-700)` | High contrast background |
| `var(--ds-gray-800)` | Hover high contrast |
| `var(--ds-gray-900)` | Secondary text / icons |
| `var(--ds-gray-1000)` | Primary text / icons |

### Page Backgrounds

| Token | Usage |
|-------|-------|
| `var(--ds-background-100)` | Default page background |
| `var(--ds-background-200)` | Secondary background |

### Alpha Variants

| Token | Usage |
|-------|-------|
| `var(--ds-gray-alpha-100)` | Subtle transparent overlay |
| `var(--ds-gray-alpha-400)` | Border on transparent surface |

### Semantic / Status Colors

| Token | Usage |
|-------|-------|
| `var(--ds-blue-700)` | Info background |
| `var(--ds-blue-900)` | Info text |
| `var(--ds-amber-100)` | Warning background |
| `var(--ds-amber-400)` | Warning border |
| `var(--ds-amber-700)` | Warning icon |
| `var(--ds-amber-900)` | Warning text |
| `var(--ds-green-700)` | Success |
| `var(--ds-red-800)` | Error / destructive |

### Color Scales Available

`gray`, `gray-alpha`, `blue`, `red`, `amber`, `green`, `teal`, `purple`, `pink`

Each scale runs from `-100` (lightest) to `-1000` (darkest). P3 wide-gamut supported on compatible displays.

---

## Materials (Surface Elevation)

### Page Surfaces

| Material | Border Radius | Usage |
|----------|--------------|-------|
| `material-base` | 6px | Default page elements |
| `material-small` | 6px | Slightly raised elements |
| `material-medium` | 12px | Cards, panels |
| `material-large` | 12px | High-emphasis containers |

### Floating Elements (above page)

| Material | Border Radius | Usage |
|----------|--------------|-------|
| `material-tooltip` | 6px | Lightest shadow, tooltip with stem |
| `material-menu` | 12px | Dropdowns, context menus |
| `material-modal` | 12px | Dialogs, sheets |
| `material-fullscreen` | 16px | Drawers, fullscreen overlays |

---

## Grid System

The Geist Grid is flexible and component-driven rather than fixed-column:

- `columns` prop: configurable column count
- `rows` prop: configurable row count
- `height: "preserve-aspect-ratio"`: maintains proportions
- `Grid.System` with `debug` prop for visual overlay
- No fixed gutter/breakpoint constraints — adapts to container

---

## Components (50+)

Avatar, Badge, Book, Browser, Button, Calendar, Checkbox, Choicebox, Code Block, Collapse, Combobox, Command Menu, Context Card, Context Menu, Description, Drawer, Empty State, Entity, Error, Feedback, Gauge, Grid, Input, Keyboard Input, Loading Dots, Material, Menu, Modal, Multi Select, Note, Pagination, Phone, Pill, Progress, Project Banner, Radio, Relative Time Card, Scroller, Select, Sheet, Show More, Skeleton, Slider, Snippet, Spinner, Split Button, Status Dot, Switch, Table, Tabs, Textarea, Theme Switcher, Toast, Toggle, Tooltip

---

## Brand Guidelines

### Vercel Trademark Rules

**Permitted uses:**
- Truthfully describe Vercel products and services
- State customer/user relationship: *"Our site is hosted on Vercel"*
- Reference the platform in editorial/informational context

**Prohibited uses:**
- Naming a business or product using Vercel marks
- Creating confusingly similar branding
- Implying sponsorship or endorsement by Vercel
- Commercial merchandise featuring Vercel marks
- Modifying or distorting official logos
- Prominence exceeding your own company branding

### Product Naming Conventions

| Brand | Correct Spelling | Notes |
|-------|-----------------|-------|
| Vercel | Vercel | Always capitalized |
| Next.js | Next.js | Include the `.js`; "Next" acceptable after first use on same page |
| Turborepo | Turborepo | One word |
| Turbopack | Turbopack | One word |
| v0 | v0 | Lowercase `v` |
| AI SDK | AI SDK | Two words, both caps |

**URL/hashtag formats:**
- URLs: `nextjs.org`, `nextjs` (no dot in URL slugs)
- Hashtags: `#nextjs`, `#vercel`

### Official Brand Assets

Downloads available for: Vercel (wordmark + symbol), Next.js (wordmark + symbol), Turbo products, v0, AI SDK

Contact for extended use: `brand@vercel.com`

**Required attribution for permitted trademark use:**
> *"Vercel, the Vercel design, Next.js and related marks, designs and logos are trademarks or registered trademarks of Vercel, Inc. or its affiliates"*

---

## Design Principles

- **High contrast**: Accessible color system prioritizes readability
- **Developer-focused**: Typography and iconography tailored for dev tools
- **Dark/light native**: All tokens dual-mode by default
- **Systematic elevation**: Materials define visual hierarchy through shadow/blur, not color
- **Consistent radius**: 6px (small), 12px (medium), 16px (large) — three tiers only

---

## Quick Reference: CSS Variables Cheatsheet

```css
/* Backgrounds */
background: var(--ds-background-100);       /* page */
background: var(--ds-gray-100);             /* component */

/* Text */
color: var(--ds-gray-1000);                 /* primary */
color: var(--ds-gray-900);                  /* secondary */

/* Borders */
border: 1px solid var(--ds-gray-400);       /* default */
border: 1px solid var(--ds-gray-500);       /* hover */

/* Status */
color: var(--ds-red-800);                   /* error */
color: var(--ds-green-700);                 /* success */
color: var(--ds-amber-700);                 /* warning */
color: var(--ds-blue-900);                  /* info */

/* Typography */
font-family: 'Geist', sans-serif;           /* UI text */
font-family: 'Geist Mono', monospace;       /* code */
```
