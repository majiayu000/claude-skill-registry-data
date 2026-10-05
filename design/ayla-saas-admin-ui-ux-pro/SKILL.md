---
name: ayla-saas-admin-ui-ux-pro
description: Build Ayla SaaS admin dashboard screens using the blue-accented admin design system. Use when the user asks for Ayla, an admin panel, back-office UI, SaaS console, internal tool, or analytics dashboard.
metadata:
short-description: Ayla SaaS admin dashboard UI system
---

# Ayla SaaS Admin UI/UX Pro

The house design system for admin / analytics dashboards: clean, blue-accented, opinionated. Encodes design tokens, layout grid, component anatomy, table variants, form-element set, and a catalogue of 30+ ready-to-assemble screens.

## When to use this skill

- The user wants an admin panel, back-office UI, SaaS console, internal tool, or analytics dashboard.
- The user references "Ayla" by name — this is the brand identifier for the system.
- The user asks for specific screens like "billing", "kanban board", "invoice detail", "profile page", "login screen", "settings", "pricing plans", "file manager", "FAQs".
- The user wants a single component out of the system (stat card, data table, form element).
- The user wants to convert this design system into a particular framework (React, Vue, plain HTML/CSS, Tailwind, etc.).

This is the default house admin-panel style. If the user has a *different* aesthetic in mind (e.g. a glassmorphic dashboard, a dark trading terminal, a Linear-style UI), mention that this skill produces a specific look and offer to deviate.

## How to use this skill — workflow

1. **Identify the deliverable.** Are we shipping one HTML file, a set of React components, a Tailwind config, just CSS variables, or a multi-page mock? Match the user's target stack.
2. **Read the relevant reference file(s).** Do not write a single line of HTML/CSS/JSX before reading what applies. The reference files are the source of truth — the agent's general knowledge of "admin dashboards" will introduce drift (wrong colors, off spacings, generic gray sidebar) that breaks the look.
3. **Compose, do not invent.** Every screen in this design is built from the same kit: `Sidebar + Navigation + Breadcrumbs + Content (cards/tables/forms in a 1560px-wide grid) + Footer`. Pick the screen template, drop in the right widgets from the catalogue, done.
4. **Use the design tokens, not literals.** Wire colors and font sizes through the CSS variables in `assets/tokens.css` so swapping themes (e.g., the black or navy sidebar variants) stays one-line changes.
5. **Default to drop-in HTML+CSS** when the user hasn't named a stack. The design is built with absolute / flex layout, no JS required for static screens. Use `assets/starter.html` as the scaffold.

## Reference files — read these before generating

| File | Read when… |
| --- | --- |
| `references/design-tokens.md` | Always — colors, typography, radii, shadows. Every screen needs this. |
| `references/layout-and-grid.md` | Building any full screen. Covers page chrome, 1560px content grid, column widths (372/504/636/768/1164/1560), and margin/gap rules. |
| `references/components.md` | Building the sidebar, top navigation, breadcrumbs, footer, or buttons. |
| `references/tables.md` | Building any table — six variants are documented (Basic, Striped, Advanced w/ pagination, Hoverable w/ avatar, Highlight Column, Small). |
| `references/forms.md` | Building inputs, selects, checkboxes, radios, switches, the login / register screens, or any "Add new" modal. |
| `references/widgets.md` | Building dashboard stat cards (Active Visitors, Bounce Rate, etc.), the calendar widget, kanban columns, notification panel, or the right-side settings drawer. |
| `references/screens.md` | When the user names a specific screen ("billing", "invoice detail", "kanban", "register", etc.). Lists every screen with its content blueprint. |

## Bundled assets

| File | Purpose |
| --- | --- |
| `assets/tokens.css` | All CSS custom properties — colors, font stacks, spacing scale, radii. Drop this into any project and the rest of the system works. |
| `assets/starter.html` | A minimal, working page shell: sidebar + top nav + breadcrumbs + empty content + footer. Use this as the starting point for any new screen and fill the content area from the references. |

## Critical rules — common ways generated screens go off-design

These are the failure modes from generic "admin dashboard" pattern-matching. Avoid them:

- **Font is Public Sans, not Inter / Roboto / system-ui.** The whole feel changes if this is wrong. Load it from Google Fonts: `https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600&display=swap`.
- **The sidebar is white, not dark gray.** Inactive nav labels are `#626C70` (Gray 600), the active item has a `#F0F6FF` (Primary 50) background and a 3px `#005CE8` left accent inset shadow. Do not use the black or navy variants unless explicitly asked — they are listed in `references/components.md` as alternatives.
- **The accent blue is `#005CE8` (Primary 500), not `#3B82F6` / `#2563EB` / generic Tailwind blue.** Bars in stat cards render as `#0E5FD9` (a slightly darker active blue).
- **Card padding is 24px and radius is 8px.** Not 16px, not 12px. Inputs use 4px radius. Badges and small pills also use 4px.
- **The content grid is 1560px wide and the gutter between cards is 24px.** All cards snap to widths from the set `{372, 504, 636, 768, 1164, 1560}`. If a layout doesn't fit, you picked wrong widths.
- **Table column headers are 12px uppercase**, not 14px. Cell text is 14px regular `#191B1C` (Gray 900). Row dividers are 1px lines, not borders on every cell.
- **The stat number in a stat card is 24px SemiBold**, paired with a small uppercase label above it (12px Medium Gray 700) and a green/red trend pill to its right (14px Medium, e.g. `#0FAF62` for up, `#E84646` for down).
- **Status pill conventions:** success uses `#0FAF62` text on `#E7F7EF` bg; danger uses `#E84646`; warning uses `#FFD599` bg. Always Medium 12px.
- **Icons are Phosphor Icons.** The "normal" weight is the default. If you don't have access to Phosphor, fall back to Lucide — the visual weight is closest. Do not use Material Icons or Font Awesome solid.

## Quick example — what "a stat card" actually looks like in this system

```html
<article class="ayla-card ayla-stat-card">
  <header class="ayla-stat-card__header">
    <div>
      <p class="ayla-stat-card__label">Active Visitors</p>
      <p class="ayla-stat-card__value">157,367</p>
    </div>
    <span class="ayla-trend ayla-trend--up">↑ 6.7% Increase</span>
  </header>
  <div class="ayla-stat-card__bars">
    <!-- 8 bars; each is a 20px-wide rounded track with an inner filled bar of variable height -->
    <span class="ayla-bar"><span style="--fill: 64px; --offset: 78px"></span></span>
    <!-- … 7 more … -->
  </div>
</article>
```

CSS for these classes lives in `references/widgets.md`. The principle: **everything composes from the tokens**.

## What this skill does NOT cover

- Real data integration (this is a visual / mock skill — wire up your own data layer).
- Interaction state machines beyond basic hover / active. Animation, transitions, and JS behavior are left to the consumer.
- Dark mode. The system has black-sidebar and navy-sidebar variants, but no full dark theme. If the user wants dark mode, say so and offer to derive one — don't pretend the system has it.

## When generating, end with this self-check

Before handing back code, verify:

1. ☐ Public Sans is loaded.
2. ☐ All colors are from the token set or a documented derivation. No raw hexes outside that palette.
3. ☐ Sidebar is 280px, top nav 72px, content grid 1560px wide, page padding 40px from sidebar to content.
4. ☐ Card radius 8px, card padding 24px, card gap 24px.
5. ☐ Tables use 12px uppercase column headers, 14px body, 1px row dividers — no full-cell borders.
6. ☐ Buttons / inputs use 4px radius.
7. ☐ The screen actually matches one of the layouts in `references/screens.md`, or is a documented variation of one.
